"""Render reader-facing task/source cards from the committed benchmark records.

No network, model calls, new examples, or modifications to benchmark data.
Run with --check to detect outdated cards without writing files.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import medical_decision_dataset as data

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "benchmarks/medical_decision_v1"
DATA_LINK = "../../benchmarks/medical_decision_v1"
STAGES = {
    "material_judgment": "材料判断",
    "clinical_choice": "临床候选方案选择",
    "outcome_prediction": "结局预测",
    "clinical_action": "临床行动选择",
    "risk_classification": "风险分类",
}
DISTRIBUTIONS = {
    "open": "开放许可部分",
    "research_noncommercial": "非商业研究附加集",
    "reference_only": "仅作参考，未收录题目",
}
LANGUAGES = {"zh": "中文", "en": "英语", "es": "西班牙语"}
SCOPES = {"clinical": "临床主评测", "auxiliary": "辅助评测（不计临床主分数）", "suspended": "暂停使用（不导出、不评分）"}
CATEGORIES = {"support": "临床计算、解读与证据", "risk": "风险、结局与历史去向预测", "workflow": "流程与记录核对", "text": "文本理解与标注"}


def read_json(path):
    return json.loads(path.read_text())


def inline(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def prose(value):
    # Project release labels are not part of the user-facing catalog.
    return re.sub(r"\bv0\.\d+\.\d+\s*", "", str(value)).strip()


def link(title, target):
    return f"[{inline(title)}]({target})"


def table(headers, rows, numeric_from=None):
    align = ['---:' if numeric_from is not None and i >= numeric_from else '---' for i in range(len(headers))]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(align) + " |"]
    lines.extend("| " + " | ".join(map(inline, row)) + " |" for row in rows)
    return "\n".join(lines)


def best_cells(values, *, higher=True, precision=2, percent=False):
    """Highlight displayed extrema; retain ties, but avoid bolding an all-equal row."""
    displayed = [None if v is None else f'{v * (100 if percent else 1):.{precision}f}' for v in values]
    numbers = {float(v) for v in displayed if v is not None}
    best = (max(numbers) if higher else min(numbers)) if numbers else None
    return ['—' if v is None else
            ('**' + v + ('%' if percent else '') + '**' if len(numbers) > 1 and float(v) == best
             else v + ('%' if percent else '')) for v in displayed]


def block(value, *, compact=False):
    body = json.dumps(value, ensure_ascii=False, indent=None if compact else 2)
    runs = re.findall(r"`+", body)
    fence = "`" * max(3, max(map(len, runs), default=0) + 1)
    return f"{fence}json\n{body}\n{fence}"


def counts_text(counts, names=None):
    names = names or {}
    return "、".join(f"{names.get(key, key)} {count} 题" for key, count in sorted(counts.items()))


def example(rows):
    return min(rows, key=lambda row: (len(json.dumps(row["request"], ensure_ascii=False)), row["id"]))


def example_sections(row):
    p = row["provenance"]
    request = row["request"]
    criteria = request["questions"]["decision"]["criteria"]
    assert row["gold"] in criteria
    parts = [
        "## 收录样例",
        "以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。",
        f"题目 ID：`{row['id']}`；语种：{LANGUAGES.get(row['language'], row['language'])}；来源组：`{row['group_id']}`。",
        "### 模型输入",
        "只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。",
        block(request),
        "### 标准答案与预测格式",
        f"原始标注映射后的正确选项键为 `{row['gold']}`，对应选项：",
        block(criteria[row["gold"]]),
        "评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：",
        block({"id": row["id"], "choice": row["gold"]}, compact=True),
        "### 样例溯源",
        f"[上游资源]({p['resource_url']}) · [数据集说明](../datasets/{p['source_id']}.md)",
        "以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：",
        block(p),
    ]
    adaptation = row.get("metadata", {}).get("adaptation")
    if adaptation:
        parts.extend(["该题的格式转换说明：", prose(adaptation)])
    return parts



def render_performance_readme(performance, scenes, families):
    """Present medical-task outcomes; historical single-question runs stay linked."""
    if not performance:
        return '# Jev Healthcare Lab\n\n多题与并发评测尚无完整结果。[任务与数据集](docs/tasks/README.md)。\n'

    def modes(fid, kind):
        f = performance['families'][fid]
        batch, concurrency = (max(f['batch_targets']), 1) if kind == 'batch' else (1, max(f['concurrency']))
        return [next(m for m in f['modes'] if m['batch'] == batch and
                     m['concurrency'] == concurrency and m['model'] == model)
                for model in ['jev-1.13.0', 'deepseek-flash']]

    def cost_text(mode):
        c = mode['cost']
        lo, hi = c['usd_per_1000_correct_lower'], c['usd_per_1000_correct_upper']
        if c['unpriced_requests'] or lo is None:
            return '待核算' if c['unpriced_requests'] else '无正确结果'
        return f'{lo:.4f}' if lo == hi else f'{lo:.4f}–{hi:.4f}'

    def task_link(fid):
        return link(performance['families'][fid]['title'], f'docs/tasks/{fid}.md#多问题与并发性能')

    cj, cf = modes('case_complication', 'batch')
    pj, pf = modes('case_complication', 'concurrent')
    tj, tf = modes('tcm_syndrome', 'batch')
    diagnosis_j, diagnosis_f = modes('diagnosis', 'concurrent')
    selected = sum(f['selected'] for f in performance['families'].values())
    populated = sum(bool(f['selected']) for f in performance['families'].values())
    small = sum(bool(f['selected']) and f['small_sample'] for f in performance['families'].values())
    parts = [
        '# Jev Healthcare Lab',
        '**评估 JEV 在医疗任务批量处理中的准确率、速度和成本。** 按具体任务比较优势与短板，观察它在哪些判断上更有价值。',
        f'本轮比较 **JEV 1.13 与 DeepSeek V4.1 Flash**，覆盖 {len(scenes)} 个医疗场景、{populated} 个有题任务、{selected} 道固定原题。每项设置重复三轮，共 {performance["measured_requests"]:,} 次正式请求。',
        '[优势与短板](#优势与短板) · [场景与任务](#场景与任务) · [测试范围](#测试范围) · [原始结果](results/task-performance-v1/README.md)',
        '## 优势与短板',
        '以下是本轮相同题目、相同处理方式下的观测，不代表所有医疗任务或所有运行环境。',
        table(['观察', '医疗任务', '证据与限制'], [
            ['两种模式均有优势', task_link('case_complication'),
             f'多题准确率 JEV {cj["accuracy"]:.2%}、Flash {cf["accuracy"]:.2%}；完成整组分别耗时 {cj["mean_batch_wall_s"]:.3f}、{cf["mean_batch_wall_s"]:.3f} 秒。并发时分别为 {pj["mean_batch_wall_s"]:.3f}、{pf["mean_batch_wall_s"]:.3f} 秒，JEV 准确率仍较高。两种模式的单位正确判断成本均较低。'],
            ['判断与速度均有优势，部分成本待核算', task_link('nursing_priority') + '、' + task_link('medication_choice'),
             '两种模式下 JEV 的准确率更高、整组耗时更短。多题模式成本更低；并发记录有请求缺少用量，不能确认完整成本。'],
            ['优势取决于处理方式', task_link('examination_choice') + '、' + task_link('patient_contraindication') + '、' + task_link('clinical_grade'),
             '多题模式下 JEV 更准、更快、成本更低；并发模式的速度优势未复现，不能概括为始终更快。'],
            ['准确率仍有劣势', task_link('diagnosis') + '、' + task_link('trial_referral') + '、' + task_link('tcm_pathogenesis_candidate'),
             f'两种模式下 JEV 准确率均低于 Flash。例如病例诊断并发准确率为 {diagnosis_j["accuracy"]:.2%}，Flash 为 {diagnosis_f["accuracy"]:.2%}。部分设置中的速度优势不代表判断质量更好。'],
            ['多题成本与准确率均不占优', task_link('tcm_syndrome'),
             f'多题准确率 JEV {tj["accuracy"]:.2%}、Flash {tf["accuracy"]:.2%}；每千次正确判断成本分别为 ${cost_text(tj)}、${cost_text(tf)}。两种模式下，两模型准确率都不足 40%。'],
        ]),
        '延迟也有明显波动：部分 JEV 请求出现约 30 秒的长尾，已计入整组耗时。各任务详情保留逐轮范围、失败与原始响应；小幅速度差异不代表稳定优势。',
        '## 场景与任务',
        '**每行是一种处理方式下，一个模型完成该任务整组题目的结果。** 同任务两模型使用相同题目和金标。准确率越高越好，整组耗时和单位正确判断成本越低越好。',
        '多题：一次请求包含多道题，长材料按相同规则拆包。并发：每个请求含 1 题，同时发送多个请求。',
        '**耗时**是完成全部题目的三轮平均总秒数；**成本**是估算美元／千次正确判断，包含答错所消耗的费用，Flash 区间对应闲时至高峰价格。⚠ 表示该行存在失败或无效回答，已计错；“待核算”表示用量不完整，不代表免费。',
    ]
    for sid, scene in scenes.items():
        parts.append(f'### {scene["title"]}')
        rows, pending = [], []
        for family in [f for f in families if f['scenario'] == sid]:
            f = performance['families'][family['id']]
            if not f['selected']:
                pending.append(task_link(family['id']))
                continue
            name = task_link(family['id']) + f'（{f["selected"]} 题' + ('，小样本' if f['small_sample'] else '') + '）'
            for kind in ['batch', 'concurrent']:
                pair = modes(family['id'], kind)
                sizes = pair[0]['packet_sizes']
                packet_count = str(min(sizes)) if min(sizes) == max(sizes) else f'{min(sizes)}–{max(sizes)}'
                label = f'多题：每包 {packet_count} 题' if kind == 'batch' else f'并发：同时 {pair[0]["concurrency"]} 个请求'
                for model_name, mode in zip(['JEV 1.13', 'Flash'], pair):
                    flag = ' ⚠' if mode['complete_requests'] < mode['requests'] else ''
                    rows.append([name, label, model_name, f'{mode["accuracy"]:.2%}' + flag,
                                 f'{mode["mean_batch_wall_s"]:.3f}', cost_text(mode)])
        if rows:
            parts.append(table(['任务与测试题数', '处理方式', '模型', '准确率', '整组耗时（秒）', '成本（美元／千次正确）'], rows, numeric_from=3))
        if pending:
            parts.append('待补数据：' + '、'.join(pending) + '。')
    parts += [
        '## 测试范围',
        f'- 从原有 1,514 道医疗题中，按固定规则在每个任务抽取最多 32 道，共 {selected} 道；不改金标，不复制题目凑并发。{small} 个任务不足 20 题，三轮重复不增加独立病例数。',
        '- 两组独立测试：多题使用预先规定的最大打包档、并发 1；并发使用本任务最高并发档、每请求 1 题。没有按结果挑选最快档。**多题请求同时并发的组合尚未测试**，现有结果也不是持续负载容量测试。',
        '- 多题材料来自同任务的不同病例或记录；尚未覆盖同一患者的多项临床判断。长材料拆包后，耗时仍包含完成全部题目的时间。',
        '- Flash 关闭思考并输出精简 JSON；JEV 使用原生 questions。连接预热、关闭自动重试，网络延迟和失败拖尾均保留。',
        '- 费用按归档的 2026-10-12 价目与实际 usage 估算，包含缓存计费影响，不是账单金额。只有 JEV／Flash 完成了这轮多题与并发评测，不能把优势外推到其他模型。',
        '- 公开题库成绩用于模型比较，不等同于临床有效性验证。结果来自考试、模拟或规则材料，任务来源及适用边界见详情。',
        '## 数据与复核',
        '[任务与样例](docs/tasks/README.md) · [数据来源](docs/datasets/README.md) · [完整测试协议](docs/TASK_PERFORMANCE.md) · [逐轮原始结果](results/task-performance-v1/README.md) · [历史五模型评测](docs/MODEL_RESULTS.md)',
        '原题、金标、请求、原始响应和运行配置均保留。多题及并发成绩使用同一性能子集，未与历史全量成绩混算。',
        '```bash\npython3 scripts/build_task_performance_report.py --check\npython3 scripts/generate_catalog_docs.py --check\n```',
        '## 许可',
        '第三方数据保留各自的原始许可，包括非商业研究限制；见 [第三方声明](THIRD_PARTY_NOTICES.md) 和任务来源页。',
    ]
    return '\n\n'.join(parts) + '\n'


def render():
    taxonomy = read_json(DATA / "taxonomy.json")
    tasks = {t["id"]: t for t in taxonomy["tasks"]}
    reports = {t["id"]: t for t in read_json(DATA / "summary.json")["tasks"]}
    sources = {s["id"]: s for s in read_json(DATA / "sources.json")["sources"]}
    scenes = {s["id"]: s for s in taxonomy["scenarios"]}
    dimensions = {d["id"]: d["title"] for d in taxonomy["dimensions"]}
    policy = data.evaluation_policy(DATA)
    inventory = data.evaluation_inventory(DATA)
    rules = policy["tasks"]
    comparison_path = ROOT / 'results/clinical-v1/comparison.json'
    comparison = read_json(comparison_path) if comparison_path.exists() else None
    if comparison and comparison['scope_policy_sha256'] != data.file_sha(DATA / 'evaluation_scope.json'):
        raise ValueError('Model comparison uses an outdated scope policy')

    performance_path = ROOT / 'results/task-performance-v1/comparison.json'
    performance = read_json(performance_path) if performance_path.exists() else None
    if performance and performance['dataset_manifest_sha256'] != data.file_sha(ROOT / 'benchmarks/task_performance_v1/manifest.json'):
        raise ValueError('Task performance uses an outdated workload')
    throughput_path = ROOT / 'results/sustained-throughput-v1/comparison.json'
    throughput = read_json(throughput_path) if throughput_path.exists() else None
    if throughput:
        import render_throughput_docs as throughput_docs
        if throughput['config']['clinical_manifest_sha256'] != data.file_sha(ROOT / 'benchmarks/task_performance_v1/manifest.json'):
            raise ValueError('Sustained throughput uses an outdated workload')
    medical_path = ROOT / 'results/medical-load-v2/comparison.json'
    medical = read_json(medical_path) if medical_path.exists() else None
    if medical:
        import render_medical_load_docs as medical_docs
        if medical['config']['clinical_manifest_sha256'] != data.file_sha(DATA / 'manifest.json'):
            raise ValueError('Medical load benchmark uses an outdated dataset')

    def model_task_table(family):
        rows = []
        models = list(comparison['models'].values())
        scores = best_cells([m['tasks'][family]['accuracy'] for m in models], percent=True)
        time_cells = {key: best_cells([m['tasks'][family]['timing'][key] for m in models], higher=False, precision=3)
                      for key in ['mean_elapsed_s', 'p50_elapsed_s', 'p95_elapsed_s', 'task_wall_s']}
        for index, (model, m) in enumerate(comparison['models'].items()):
            q = m['tasks'][family]
            t = q['timing']
            rows.append([m['label'], scores[index], f"{t['success']} / {t['total']}",
                *[time_cells[key][index] for key in
                  ['mean_elapsed_s', 'p50_elapsed_s', 'p95_elapsed_s', 'task_wall_s']],
                ' / '.join(str(t['status_counts'].get(status, 0)) for status in
                           ['timeout', 'request_error', 'invalid_answer']),
                link('配置', f'../../results/clinical-v1/{model}/config.json') + ' · '
                + link('响应', f'../../results/clinical-v1/{model}/responses.jsonl') + ' · '
                + link('评分', f'../../results/clinical-v1/{model}/scores.json')])
        return '加粗表示本任务的最高准确率或最短用时；按显示精度并列时同时加粗，全部相同则不标记。\n\n' + table(['模型', '准确率 ↑', '有效回答 / 题数', '平均秒 ↓', 'P50 秒 ↓', 'P95 秒 ↓', '任务总秒 ↓',
                      '超时 / 请求失败 / 无效回答', '原始记录'], rows)
    def packet_range(mode):
        sizes = mode['packet_sizes']
        return str(min(sizes)) if min(sizes) == max(sizes) else f"{min(sizes)}–{max(sizes)}"

    def task_findings(family):
        item = performance['families'][family]
        if not item['selected']:
            return ['待补'] * 4
        full = comparison['models']['jev-1.13.0']['tasks'][family]['accuracy']
        highest = max(m['tasks'][family]['accuracy'] for m in comparison['models'].values())
        full_cell = f'JEV {full:.2%}；' + ('本轮最高（含并列）' if full == highest else f'最高 {highest:.2%}')
        jev, flash = [next(m for m in item['modes'] if m['model'] == model and
                          m['batch'] == max(item['batch_targets']) and m['concurrency'] == 1)
                      for model in ['jev-1.13.0', 'deepseek-flash']]
        accuracy = f"JEV {jev['accuracy']:.2%}，Flash {flash['accuracy']:.2%}"
        ratio = jev['mean_batch_wall_s'] / flash['mean_batch_wall_s']
        speed = f'JEV 耗时少 {1 - ratio:.1%}' if ratio < 1 else f'JEV 耗时多 {ratio - 1:.1%}' if ratio > 1 else '耗时相同'
        jc, fc = jev['cost'], flash['cost']
        jl, jh = jc['usd_per_1000_correct_lower'], jc['usd_per_1000_correct_upper']
        fl, fh = fc['usd_per_1000_correct_lower'], fc['usd_per_1000_correct_upper']
        if jc['unpriced_requests'] or fc['unpriced_requests'] or None in (jl, jh, fl, fh):
            cost = '数据不足，暂不比较'
        elif jh < fl:
            cost = f'JEV 成本低 {1 - jh / fl:.1%}–{1 - jl / fh:.1%}'
        elif jl > fh:
            cost = f'JEV 成本更高（{jl / fh:.2f}–{jh / fl:.2f} 倍）' if fl else 'JEV 成本更高'
        elif jl == jh == fl == fh:
            cost = '成本相同'
        else:
            cost = '取决于 Flash 闲时／高峰价格'
        if any(m['complete_requests'] < m['requests'] for m in [jev, flash]):
            accuracy += ' ⚠'
        return [full_cell, accuracy, speed, cost]

    def performance_details(family):
        if medical:
            if family in medical['families']:
                index = list(medical['families']).index(family) + 2
                return ['## 多问题与并发性能', *medical_docs.task_sections(medical, family, index)]
            return ['## 多问题与并发性能', '本任务尚无可用原题，多问题与并发测试均待补。']
        if not performance:
            return []
        item = performance['families'][family]
        parts = ['## 多问题与并发性能']
        if throughput:
            if family in {f['id'] for f in throughput['config']['families']}:
                parts.extend(throughput_docs.task_intro(throughput, family))
            else:
                parts += ['持续多题并发尚未测试。以下为历史有限批次结果，不作为高并发高吞吐证据。', '### 历史有限批次测试']
        if not item['selected']:
            return parts + ['本任务尚无可用原题，多问题与并发测试均待补；不以其他任务或合成规则结果代填。']
        parts += [f"固定本任务 {item['selected']} 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。",
                  '取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。',
                  '表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。']
        findings = task_findings(family)
        parts.append('历史多题结果（固定最大打包档，对比 Flash）：' + '；'.join(findings[1:]) + '。具体准确率与费用仅对应下述性能子集，不代表全量成绩或其他调用方式。')
        if item['small_sample']:
            parts.append('**小样本任务：** 重复运行只观察性能波动，不增加独立题目数，不能据此稳定估计临床准确率或尾延迟。')
        rows, detail_rows, cost_rows = [], [], []
        for mode in item['modes']:
            name = comparison['models'][mode['model']]['label']
            kind = '逐题' if mode['batch'] == 1 else '多题打包'
            failed = mode['requests'] - mode['complete_requests']
            rows.append([kind, mode['concurrency'], packet_range(mode), name,
                         f"{mode['accuracy']:.2%}", f"{mode['mean_batch_wall_s']:.3f}",
                         f"{mode['valid_decisions_per_s']:.2f} / {mode['correct_decisions_per_s']:.2f}",
                         f"{mode['complete_requests']} / {mode['requests']}", failed])
            detail_rows.append([f"{kind} B≤{mode['batch']} / C{mode['concurrency']}", name,
                f"{min(mode['wall_per_repeat_s']):.3f}–{max(mode['wall_per_repeat_s']):.3f}",
                f"{mode['p50_s']:.3f}", f"{mode['p95_s']:.3f}" if mode['requests'] >= 20 else '样本不足',
                f"{mode['max_elapsed_s']:.3f}", mode['http_429'],
                ' / '.join(str(mode['status_counts'].get(k, 0)) for k in ['request_error', 'timeout', 'invalid_answer']),
                ' · '.join(link(f'轮{i + 1}', '../../results/task-performance-v1/' + filename) for i, filename in enumerate(mode['records_files']))])
            cost = mode['cost']
            if cost['unpriced_requests'] or cost['usd_per_1000_correct_lower'] is None:
                unit = '—'
            else:
                lo, hi = cost['usd_per_1000_correct_lower'], cost['usd_per_1000_correct_upper']
                unit = f'{lo:.4f}' if lo == hi else f'{lo:.4f}–{hi:.4f}'
            cost_rows.append([f"{kind} B≤{mode['batch']} / C{mode['concurrency']}", name, unit, cost['unpriced_requests']])
        parts.append(table(['模式', '并发', '每请求实际题数', '模型', '准确率', '整组平均秒', '有效 / 正确决策每秒', '完整包 / 请求', '失败或无效请求'], rows))
        parts.append('<details>\n<summary>重复波动、请求耗时、失败与原始响应</summary>\n\n' +
            table(['模式', '模型', '整组秒范围', '请求 P50 秒', '请求 P95 秒', '最长请求秒', '429', '请求失败 / 超时 / 无效', '原始响应'], detail_rows) +
            '\n\n请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。\n\n</details>')
        parts.append('<details>\n<summary>每千次正确决策成本</summary>\n\n' +
            table(['模式', '模型', '估算 USD / 千次正确决策', '缺用量请求'], cost_rows) +
            '\n\n按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。\n\n</details>')
        parts.append('连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)')
        return parts

    for tid, task in tasks.items():
        task["title"] = rules[tid]["title"]
    by_task, by_source = defaultdict(list), defaultdict(list)
    for line in (DATA / "samples.jsonl").read_text().splitlines():
        row = json.loads(line)
        by_task[row["task"]].append(row)
        by_source[row["provenance"]["source_id"]].append(row)
    assert set(by_task) <= tasks.keys()
    assert set(by_source) <= sources.keys()
    output = {}

    def source_link(sid):
        return link(sources[sid]["name"], f"../datasets/{sid}.md")

    def task_link(tid):
        return link(tasks[tid]["title"], f"../tasks/{tid}.md")

    for tid, task in tasks.items():
        rows, report = by_task[tid], reports[tid]
        rule = rules[tid]
        source_counts = Counter(r["provenance"]["source_id"] for r in rows)
        assert len(rows) == report["count"]
        assert dict(source_counts) == report["source_counts"]
        parts = [
            f"# {task['title']}",
            "[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)",
            f"**当前用途：{SCOPES[rule['scope']]}。** {rule['notes']}",
            "## 任务是什么",
            task["definition"],
            table(["项目", "说明"], [
                ["任务 ID", f"`{tid}`"],
                ["医疗场景", scenes[task["primary_scenario"]]["title"]],
                ["能力维度", "、".join(dimensions[d] for d in task["ability_tags"])],
                ["评测类别", "临床判断与行动" if rule["scope"] == "clinical" else CATEGORIES[rule["category"]]],
                ["当前题数 / 目标题数", f"{len(rows)} / {task['target_count']}"],
                ["来源组数", str(len({r["group_id"] for r in rows}))],
                ["语种", counts_text(Counter(r["language"] for r in rows), LANGUAGES) or "待补"],
                ["数据范围", counts_text(Counter(r["provenance"]["distribution"] for r in rows), DISTRIBUTIONS) or "待补"],
            ]),
            "## 数据集来源",
        ]
        if rows:
            parts.append(table(["数据集说明", "收录题数", "上游入口"], [
                [source_link(sid), str(n), link("原始来源", sources[sid]["url"])]
                for sid, n in sorted(source_counts.items())
            ]))
            parts.extend([
                "## 如何作答与评分",
                "根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。" + ("本轮指标见下方任务表；固定临床类别与题内位置选项分开处理。" if medical and rule['scope'] == 'clinical' else ("固定语义标签计算准确率、宏 F1、召回与混淆矩阵。" if rule["label_semantics"] == "fixed" else "按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。")),
                ("本轮按任务报告；少于 20 题作为探索性结果，不计入首页汇总图。" if medical and rule['scope'] == 'clinical' else ("暂停任务仅保留来源与构造示例，不导出、不评分。" if rule["scope"] == "suspended" else "合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。")),
                ("当前比较的材料、计分和额度条件见[医疗多问题评估方法](../MEDICAL_LOAD.md)。" if medical and rule['scope'] == 'clinical' else ("本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。" if comparison and rule['scope'] == 'clinical' else "后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。")),
            ])
            if medical and rule['scope'] == 'clinical':
                parts.extend(performance_details(rule['family']))
                parts.append('[历史单题测试](../MODEL_RESULTS.md) · [历史有限批次测试](../TASK_PERFORMANCE.md)；与本轮分开归档。')
            elif comparison and rule['scope'] == 'clinical':
                parts.extend(['## 模型结果',
                    '以下为合并后的病例诊断任务成绩，两个来源子集共 200 题；逐来源结果保存在评分文件中。' if rule['family'] == 'diagnosis' else '以下成绩使用本页全部已收录题目；耗时包括请求、响应处理及重试等待。',
                    '有效回答表示返回合法选项，不代表正确；平均值和分位数包含已启动题目的失败耗时。任务总秒为含并发调度的墙钟时间，不是单题耗时之和。响应链接包含该模型全部题目，可按本页任务的题目 ID 查找。',
                    model_task_table(rule['family'])])
                parts.extend(performance_details(rule['family']))
            parts.extend(example_sections(example(rows)))
            parts.extend([
                "## 覆盖与使用边界",
                "题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。",
                f"当前标准标签分布：{counts_text(Counter(r['gold'] for r in rows))}。",
            ])
            if len(rows) < task["target_count"]:
                parts.append("当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。")
            for sid in sorted(source_counts):
                source = sources[sid]
                parts.append(f"**{source_link(sid)}**：{prose(source['authenticity'])} 答案依据：{prose(source['gold_provenance'])}")
                if source.get("evaluation_limits"):
                    parts.append(prose(source["evaluation_limits"]))
            historical = sum(r["exposure"]["historical_material_signature_match"] for r in rows)
            if historical:
                parts.append(f"其中 {historical} 题材料或片段命中过往评测指纹；训练效果对比应核查材料暴露，并对各模型冻结相同子集。")
        else:
            parts.extend([
                "当前没有收录题目，不参与评分。",
                "## 样例与缺口",
                "**样例待补。** 尚无符合此任务定义的可用题目，不提供虚构输入、选项或答案。",
                prose(task.get("missing_reason") or "尚无可用于本任务的已核验数据。"),
            ])
            if rule["scope"] == "clinical":
                parts.extend(performance_details(rule["family"]))
        candidates = sorted((set(task.get("source_ids", [])) | set(task.get("candidate_source_ids", []))) - set(source_counts))
        if candidates:
            parts.extend([
                "## 调研过的其他来源",
                "这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。",
                table(["来源说明", "登记情况"], [
                    [source_link(sid), prose(sources[sid].get("reason") or "本任务暂无收录，是否适用需按任务定义核验。")]
                    for sid in candidates
                ]),
            ])
        parts.extend([
            "## 数据文件",
            f"[本任务全部记录]({DATA_LINK}/tasks/{tid}/samples.jsonl) · [任务定义与统计]({DATA_LINK}/tasks/{tid}/task.json) · [格式与使用方法](../REPRODUCING.md)",
            "[返回首页](../../README.md)",
        ])
        if rule["family"] != tid:
            parts.insert(3, f"本页为来源子集，统一并入 [{rule['family_title']}]({rule['family']}.md) 计分，不另增加任务权重。")
        output[ROOT / f"docs/tasks/{tid}.md"] = "\n\n".join(parts) + "\n"

    for sid, source in sources.items():
        rows = by_source[sid]
        task_counts = Counter(r["task"] for r in rows)
        related = [tid for tid, task in tasks.items() if sid in task.get("source_ids", []) + task.get("candidate_source_ids", []) and tid not in task_counts]
        parts = [
            f"# {source['name']}",
            "[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)",
            "## 这是什么数据",
            prose(source.get("authenticity") or source.get("reason") or "尚未收录题目，材料性质待核验。"),
            table(["项目", "说明"], [
                ["来源 ID", f"`{sid}`"],
                ["上游入口", link("发布方页面", source["url"])],
                ["收录情况", f"{len(rows)} 题 / {len(task_counts)} 个任务" if rows else "0 题；仅作参考"],
                ["评测用途", counts_text(Counter(rules[r["task"]]["scope"] for r in rows), SCOPES) or "仅作参考"],
                ["使用范围", DISTRIBUTIONS[source["distribution"]]],
                ["登记的数据许可", source.get("data_license", "未确认；不据此再分发数据")],
                ["收录语种", counts_text(Counter(r["language"] for r in rows), LANGUAGES) or "无收录题目"],
            ]),
            "## 来源与引用",
        ]
        if source.get("attribution"):
            parts.append(prose(source["attribution"]))
        urls = [("论文或项目引用", source.get("citation_url")), ("数据许可", source.get("license_url")), ("补充核验依据", source.get("evidence_url"))]
        parts.append(" · ".join(link(title, url) for title, url in urls if url) or f"已登记入口：[上游页面]({source['url']})。独立论文引用与数据许可未完整登记。")
        snapshots = source.get("license_evidence", [])
        if snapshots:
            parts.append("许可与说明快照：" + " · ".join(link(Path(path).name, f"{DATA_LINK}/{path}") for path in snapshots))
        if source.get("reason"):
            parts.extend(["### 登记边界", prose(source["reason"])])
        if source.get("evaluation_limits"):
            parts.extend(["### 使用限制", prose(source["evaluation_limits"])])
        parts.append("## 用于哪些任务")
        if rows:
            parts.append(table(["任务或来源子集", "用途", "此来源贡献题数", "评测内容"], [
                [task_link(tid), SCOPES[rules[tid]["scope"]], str(n), tasks[tid]["definition"]]
                for tid, n in sorted(task_counts.items())
            ]))
            parts.extend([
                "## 答案与格式转换",
                prose(source["gold_provenance"]),
                "这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。",
            ])
            parts.extend(example_sections(example(rows)))
            parts.append(f"更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：{task_link(example(rows)['task'])}。")
        else:
            parts.extend([
                "当前没有使用该来源的评测任务。",
                "## 样例数据",
                "**样例留空。** 当前未收录可用于本评测集的题目，仅保留来源与调研信息；不复制许可未闭合或需受控访问的原文。",
            ])
        if related:
            parts.extend([
                "## 相关任务调研",
                "以下为曾考虑使用此来源的任务，不代表已采用：",
                table(["任务说明", "任务内容"], [[task_link(tid), tasks[tid]["definition"]] for tid in related]),
            ])
        parts.extend([
            "## 追溯与使用",
            f"来源元数据保存在 [来源登记文件]({DATA_LINK}/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件]({DATA_LINK}/sources.lock.json)。原始数据各自的许可独立适用。",
            "[返回首页](../../README.md)",
        ])
        output[ROOT / f"docs/datasets/{sid}.md"] = "\n\n".join(parts) + "\n"

    clinical = inventory['clinical']
    families = clinical['families']
    status_names = {'empty': '待补', 'exploratory': '探索性', 'summary_eligible': '计入总分'}
    parts = ['# 临床主评测任务', '[返回首页](../../README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)',
             f"共 {clinical['defined_families']} 个任务定义、{clinical['populated_families']} 个有题任务，{clinical['records']:,} 题。病例诊断的两个来源子集合并计分。" + ("本轮逐任务展示，首页图仅汇总至少 20 题的既有任务；下方状态是原始数据集的登记状态。" if medical else "所有有题任务均计入总分，少于 20 题仅标记小样本。状态按完整临床范围展示，实际评分按本次许可子集计算题数与成绩。")]
    if medical:
        parts.append('所有 26 个有题任务均列出四模型多问题与持续并发测试状态，另加[同一患者的多项试验筛选](trial_shared_patient.md)。每请求最多 8 项，配置并发 8／32，各两轮；题量、准确率、速度和成本按任务展示。[当前评估方法](../MEDICAL_LOAD.md)。')
    elif throughput:
        parts.append('病例并发症、用药方案、病例诊断和中医证型任务页新增持续多题并发结果：每请求 8 题，配置 8／32／64 并发，持续补入请求。其余任务的持续负载尚未测试。[持续负载协议](../SUSTAINED_THROUGHPUT.md)。原单题与有限批次成绩作为历史记录保留。')
    elif performance:
        parts.append('每个任务页包含原单题结果，以及 JEV／Flash 在同一原题子集上的多题打包、逐题并发、准确率、完整率与成本。三轮结果和全部档位按任务保留；空任务标记待补。[测试协议](../TASK_PERFORMANCE.md)。')
    for scene_id, scene in scenes.items():
        parts.extend([f"## {scene['title']}", table(['任务说明', '能力维度', '题数', '状态'], [
            [link(f['title'], f"{f['id']}.md"), '、'.join(dimensions[d] for d in f['ability_tags']), f['records'], status_names[f['status']] + ('（小样本）' if f['small_sample'] else '')]
            for f in families if f['scenario'] == scene_id])])
    output[ROOT / 'docs/tasks/README.md'] = '\n\n'.join(parts) + '\n'
    parts = ['# 辅助与暂停任务', '[返回首页](../../README.md) · [临床主评测任务](README.md)',
             '这些任务不计入临床主分数。辅助任务可通过 --scope auxiliary 单独导出和评分；暂停任务仅保留追溯材料。']
    for category, title in CATEGORIES.items():
        parts.extend([f'## {title}', table(['任务说明', '题数', '当前用途'], [
            [task_link(tid), len(by_task[tid]), rules[tid]['notes']] for tid in tasks
            if rules[tid]['scope'] == 'auxiliary' and rules[tid]['category'] == category])])
    parts.extend(['## 暂停使用', table(['任务说明', '底稿题数', '原因'], [
        [task_link(tid), len(by_task[tid]), rules[tid]['notes']] for tid in tasks if rules[tid]['scope'] == 'suspended'])])
    output[ROOT / 'docs/tasks/AUXILIARY.md'] = '\n\n'.join(parts) + '\n'
    diagnosis = next(f for f in families if f['id'] == 'diagnosis')
    parts = ['# 病例诊断选择', '[返回首页](../../README.md) · [临床主评测任务](README.md)',
             '根据给定病例资料，从候选中选择诊断。考试病例与模拟病例作为同一个评测任务的来源子集；题目和原答案保留，不因拆分来源重复增加任务权重。',
             f"共 {diagnosis['records']} 题。合并后按全部题目计算任务准确率，并保留每个来源子集的结果。选项含义随题变化，不计算临床类别 F1。",
             table(['来源子集与完整样例', '题数'], [[task_link(tid), len(by_task[tid])] for tid in diagnosis['task_ids']]),
             '## 样例与来源', '两个来源子集的说明页分别给出完整输入、原选项、标准答案和溯源。以下为考试病例子集中的一题：']
    parts.extend(example_sections(example(by_task['diagnosis_choice'])))
    if medical:
        parts.extend(performance_details('diagnosis'))
    elif comparison:
        parts.extend(['## 模型结果', '两个诊断来源合并为 200 题。有效回答不代表答对；任务总秒为墙钟时间，单题平均值与分位数包含失败耗时。响应链接包含该模型全部题目。', model_task_table('diagnosis'), '[完整得分、耗时与运行条件](../MODEL_RESULTS.md)'])
        parts.extend(performance_details('diagnosis'))
    parts.extend(['## 评测边界', '考试病例与模拟病例分别报告，不能把模拟患者当成真实患者。候选数量与题型不同，比较模型时冻结同一批题目和选项。', '[返回首页](../../README.md)'])
    output[ROOT / 'docs/tasks/diagnosis.md'] = '\n\n'.join(parts) + '\n'

    parts = ['# 数据集与参考来源目录', '[返回首页](../../README.md) · [临床主评测任务](../tasks/README.md) · [辅助与暂停任务](../tasks/AUXILIARY.md)',
             f"临床主评测使用 {len(clinical['sources'])} 个来源。底稿累计登记 {len(sources)} 个来源，其中 {sum(bool(by_source[s]) for s in sources)} 个有收录记录；其余仅作参考。下表按当前用途统计，底稿题数不等于主评测题数。"]
    for distribution, title in DISTRIBUTIONS.items():
        parts.extend([f'## {title}', table(['数据集 / 来源说明', '主评测题数', '辅助题数', '暂停题数', '材料性质或未采用原因'], [
            [link(s['name'], f'{sid}.md'),
             sum(rules[r['task']]['scope'] == 'clinical' for r in by_source[sid]),
             sum(rules[r['task']]['scope'] == 'auxiliary' for r in by_source[sid]),
             sum(rules[r['task']]['scope'] == 'suspended' for r in by_source[sid]),
             prose(s.get('authenticity') if by_source[sid] else s.get('reason') or s.get('authenticity') or '待核验')]
            for sid, s in sources.items() if s['distribution'] == distribution])])
    output[ROOT / 'docs/datasets/README.md'] = '\n\n'.join(parts) + '\n'

    if medical:
        output[ROOT / 'README.md'] = medical_docs.render(medical)
        output[ROOT / 'docs/MEDICAL_LOAD.md'] = medical_docs.protocol(medical)
        output[ROOT / 'results/medical-load-v2/README.md'] = medical_docs.archive_readme(medical)
        output[ROOT / 'docs/tasks/trial_shared_patient.md'] = '\n\n'.join([
            '# 同一患者的多项试验转介筛选', '[返回首页](../../README.md) · [原始来源](../datasets/trialgpt.md)',
            '## 多问题与并发性能',
            *medical_docs.task_sections(medical, 'trial_shared_patient', list(medical['families']).index('trial_shared_patient') + 2)]) + '\n'
    else:
        output[ROOT / 'README.md'] = throughput_docs.render(throughput) if throughput else render_performance_readme(performance, scenes, families)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files = render()
    stale = []
    for path, content in files.items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    if stale:
        raise SystemExit("Outdated catalog pages:\n" + "\n".join(stale))
    print(f"{'Checked' if args.check else 'Wrote'} {len(files)} catalog pages.")


if __name__ == "__main__":
    main()
