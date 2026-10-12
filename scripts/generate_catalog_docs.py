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

    def performance_details(family):
        if not performance:
            return []
        item = performance['families'][family]
        parts = ['## 多问题与并发性能']
        if not item['selected']:
            return parts + ['本任务尚无可用原题，多问题与并发测试均待补；不以其他任务或合成规则结果代填。']
        parts += [f"固定本任务 {item['selected']} 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。",
                  '取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。',
                  '表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。']
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

    def scene_performance(scene_families):
        if not performance:
            return []
        batch_rows, concurrency_rows = [], []
        for family in scene_families:
            item = performance['families'][family['id']]
            name = link(family['title'], f"docs/tasks/{family['id']}.md#多问题与并发性能")
            n = item['selected']
            if not n:
                batch_rows.append([name, '待补', '—', '—', '—', '—'])
                concurrency_rows.append([name, '待补', '—', '—', '—', '—'])
                continue
            batch = max(item['batch_targets'])
            concurrency = max(item['concurrency'])
            batches = [next(m for m in item['modes'] if m['batch'] == batch and m['concurrency'] == 1 and m['model'] == model)
                       for model in performance['models']]
            baselines = [next(m for m in item['modes'] if m['batch'] == 1 and m['concurrency'] == 1 and m['model'] == model)
                         for model in performance['models']]
            concurrent = [next(m for m in item['modes'] if m['batch'] == 1 and m['concurrency'] == concurrency and m['model'] == model)
                          for model in performance['models']]
            flag = lambda m: ' ⚠' if m['complete_requests'] < m['requests'] else ''
            name += f"（{n} 题" + ('，小样本' if item['small_sample'] else '') + '）'
            for label, modes in [('逐题串行（每次 1 题）', baselines),
                                 (f'多题打包（每次 {packet_range(batches[0])} 题）', batches)]:
                values = []
                for mode in modes:
                    values.extend([f"{mode['accuracy']:.2%}{flag(mode)}", f"{mode['mean_batch_wall_s']:.3f}"])
                batch_rows.append([name, label] + values)
            for label, modes in [('逐题串行（同时 1 个请求）', baselines),
                                 (f'逐题并发（同时 {concurrency} 个请求）', concurrent)]:
                values = []
                for mode in modes:
                    values.extend([f"{mode['valid_decisions_per_s']:.2f}",
                                   f"{mode['correct_decisions_per_s']:.2f}{flag(mode)}"])
                concurrency_rows.append([name, label] + values)
        names = [comparison['models'][m]['label'] for m in performance['models']]
        return ['**同任务多题打包**：同一批题分别逐题发送和打包发送，两种方式都一次只发一个请求。耗时是做完该任务所列全部题目的总时间（三轮平均），不是每题耗时。多题展示最大打包档；材料过长时拆成多包。',
                table(['任务与测试题数', '测试方式'] +
                      [heading for name in names for heading in [name + ' 准确率', name + ' 全部题目耗时（秒）']], batch_rows, numeric_from=2),
                '**逐题并发**：每个请求仍只含 1 题，比较依次发送和同时发送多个请求。有效表示返回合法选项，正确表示与标准答案一致；吞吐单位均为题/秒，越高越好。并发结果展示本任务最高并发档。',
                table(['任务与测试题数', '测试方式'] +
                      [heading for name in names for heading in [name + ' 有效（题/秒）', name + ' 正确（题/秒）']], concurrency_rows, numeric_from=2)]

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
                "根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。" + ("固定语义标签计算准确率、宏 F1、召回与混淆矩阵。" if rule["label_semantics"] == "fixed" else "按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。"),
                "暂停任务仅保留来源与构造示例，不导出、不评分。" if rule["scope"] == "suspended" else "合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。",
                "本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。" if comparison and rule['scope'] == 'clinical' else "后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。",
            ])
            if comparison and rule['scope'] == 'clinical':
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
             f"共 {clinical['defined_families']} 个任务定义、{clinical['populated_families']} 个有题任务，{clinical['records']:,} 题。病例诊断的两个来源子集合并计分；所有有题任务均计入总分，少于 20 题仅标记小样本。状态按完整临床范围展示，实际评分按本次许可子集计算题数与成绩。"]
    if performance:
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
    if comparison:
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

    used_tags = sorted({d for f in families for d in f['ability_tags']})
    parts = ['# Jev Healthcare Lab',
        '![医疗决策场景 · JEV 评测：使用医疗决策类题目比较准确率与用时；8 个场景，29 个任务，26 项有题，1,514 道题](assets/readme/jev-medical-evaluation-v1.gif)',
        '本项目从公开数据集中筛选并整理医疗决策类题目，用于评测 **JEV 模型在医疗场景中的决策表现**，并与其他模型逐任务比较准确率和完整运行耗时。题目要求模型根据病例、检查结果或规则材料，从给定候选中选择判断或行动。',
        f"评测按 **{len(scenes)} 个医疗场景、{clinical['defined_families']} 个任务**组织：从接诊与分诊、检查与检验、诊断与鉴别，到治疗与用药、住院与护理、出院与随访，并涵盖临床试验筛选和病历与医疗质量控制。",
        f"目前 **{clinical['populated_families']} 个任务有题，共 {clinical['records']:,} 题**（中文 {clinical['languages'].get('zh', 0):,} 题），来自 {len(clinical['sources'])} 个数据来源；另有 {sum(f['status'] == 'empty' for f in families)} 个任务待补。任务另按 {len(used_tags)} 个能力标签标注。全部有题任务计入总分，其中 {sum(f['small_sample'] for f in families)} 个不足 20 题，标记为小样本。" + (f"已完成 {len(comparison['models'])} 个模型的同题评测。" if comparison else '当前尚无模型对比成绩。'),
        '[场景与任务](#场景与任务) · [评测方案：请求与提示词](docs/EVALUATION.md) · [任务说明与样例](docs/tasks/README.md) · [数据集说明与样例](docs/datasets/README.md) · [辅助任务](docs/tasks/AUXILIARY.md)',
        '## 能力维度',
        '场景表示医疗流程环节；能力标签描述判断方式，可以重叠。任务是逐项比较的单位，数据来源或语言子集不重复算作独立任务。',
        table(['能力维度', '关联任务数（含待补）'], [[dimensions[d], sum(d in f['ability_tags'] for f in families)] for d in used_tags]),
        '## 场景与任务',
        '每个场景先列原单题评测的准确率与平均耗时，再按任务列多题打包与并发性能。**加粗**表示原单题表的最高准确率或最短用时；按显示精度并列时同时加粗，全部相同则不标记。',
        '逐任务性能测试固定抽取最多 32 道原题，各模式运行三轮，JEV 与 Flash 使用相同题目和金标。多题打包对照同一子集逐题与最大打包档的准确率及整组平均耗时，逐题并发对照并发 1 到最高并发档的有效／正确决策吞吐；全部档位、失败和成本见任务详情。空任务保留待补，小任务不复制题目凑数。其他三模型尚未进行本轮性能测试。[参数与数据协议](docs/TASK_PERFORMANCE.md)。',
        '用时单位为秒，包含网络与响应处理；原单题评测含重试，逐任务性能测试不自动重试。⚠ 表示该模型在此任务有请求失败或无效回答，失败计错且耗时保留；不能只凭较短用时判断优劣。标为“小样本”的任务不足 20 题，仍计入总分，结果可能波动较大；— 表示尚无数据。点击任务名称查看详情，展开场景末尾的来源表查看数据集。',
        table(['医疗场景', '有题任务 / 定义任务', '题数'], [[s['title'], f"{sum(f['records'] > 0 for f in families if f['scenario'] == sid)} / {sum(f['scenario'] == sid for f in families)}", sum(f['records'] for f in families if f['scenario'] == sid)] for sid, s in scenes.items()])]
    if comparison:
        ranked = sorted(comparison['models'].values(), key=lambda m: -m['primary_clinical_score'])
        best, second = ranked[:2]
        fastest = min(ranked, key=lambda m: m['timing']['mean_elapsed_s'])
        parts[parts.index('## 能力维度'):parts.index('## 能力维度')] = [
            '## 评测速览',
            f"**{best['label']} 本轮主分数最高：{best['primary_clinical_score']:.2%}**，领先第二名 {(best['primary_clinical_score']-second['primary_clinical_score'])*100:.2f} 个百分点。原单题评测中，**{fastest['label']} 平均用时最短：{fastest['timing']['mean_elapsed_s']:.3f} 秒/题**。",
            '![医疗决策场景 · JEV 评测：五个模型的临床主分数与平均用时对比，完整数值见下方模型得分与耗时表](assets/readme/jev-medical-score-time-v1.svg)',
            '![医疗决策场景 · JEV 评测：八个场景的模型得分热力图，标注题数、小样本任务数和场景最高值，完整结果见各任务表](assets/readme/jev-medical-scenario-accuracy-v1.svg)',
            '![医疗决策场景 · JEV 评测：八个场景的平均单题用时热力图，单位为秒，越低越快，描边标记各场景最短用时](assets/readme/jev-medical-scenario-time-v1.svg)',
            '主分数按场景内任务等权、再对场景等权计算；全部 26 个有题任务计入。11 个任务不足 20 题，医疗质量控制场景仅 3 题。以上为本轮观测结果，不代表统计显著性或临床有效性；用时受网络和平台服务条件影响。',
            '[完整模型结果](docs/MODEL_RESULTS.md) · [逐题原始记录](results/clinical-v1/README.md) · [图表数据](assets/readme/metrics-v1.json)']
    for sid, scene in scenes.items():
        scene_families = [f for f in families if f['scenario'] == sid]
        parts.append(f"### {scene['title']}")
        if comparison:
            models = list(comparison['models'].values())
            headers = ['任务', '题数'] + [m['label'] for m in models]
            for timing, heading in [(False, '准确率 ↑ · 越高越好'), (True, '平均用时 ↓ · 秒，越低越好')]:
                rows = []
                for f in scene_families:
                    results = [m['tasks'].get(f['id']) for m in models]
                    values = [None if q is None else q['timing']['mean_elapsed_s'] if timing else q['accuracy'] for q in results]
                    cells = best_cells(values, higher=not timing, precision=3 if timing else 2, percent=not timing)
                    cells = [cell + (' ⚠' if q and q['timing']['success'] < q['timing']['total'] else '') for cell, q in zip(cells, results)]
                    count = str(f['records']) + (' · 小样本' if f['small_sample'] else ' · 待补' if not f['records'] else '')
                    rows.append([link(f['title'], f"docs/tasks/{f['id']}.md"), count] + cells)
                parts.extend([f'**{heading}**', table(headers, rows, numeric_from=1)])
        parts.extend(scene_performance(scene_families))
        source_table = table(['任务', '能力维度', '题数', '状态', '数据集来源（题数）'], [
            [link(f['title'], f"docs/tasks/{f['id']}.md"), '、'.join(dimensions[d] for d in f['ability_tags']), f['records'], status_names[f['status']] + ('（小样本）' if f['small_sample'] else ''),
             '；'.join(link(sources[source]['name'], f'docs/datasets/{source}.md') + ('†' if sources[source]['distribution']=='research_noncommercial' else '') + f'（{n}）' for source,n in sorted(f['sources'].items())) or '待补数据']
            for f in scene_families])
        if comparison:
            parts.append('<details>\n<summary>数据来源与能力维度</summary>\n\n' + source_table + '\n\n† 非商业附加来源。来源后的数字为实际题数。\n\n</details>')
        else:
            parts.append(source_table)
    parts.extend(['## 模型得分与耗时对比',
        '每个模型使用相同题目、候选项和许可范围，分别报告逐任务准确率、完整决策耗时（均值、P50、P95）、任务总耗时及失败率。多阶段调用、工具与重试计入完整决策耗时，运行配置随结果保存。',
        '病例诊断的两个来源子集合并为一个任务。汇总先对场景内所有有题任务等权，再对有分数场景等权；小样本同样计入，空任务不计零分。小样本任务与其他任务具有相同权重，个别题目对其成绩的影响更大。固定语义分类额外报告 F1、召回、混淆矩阵与多数类基线；A/B/C 等随题变化的选项不报告临床类别 F1。',
        '请求格式、完整提示词、模型参数、重试与计分计时口径见 [评测方案](docs/EVALUATION.md)。'])
    if comparison:
        models = list(comparison['models'].values())
        scores = best_cells([m['primary_clinical_score'] for m in models], percent=True)
        means = best_cells([m['timing']['mean_elapsed_s'] for m in models], higher=False, precision=3)
        p95s = best_cells([m['timing']['p95_elapsed_s'] for m in models], higher=False, precision=3)
        parts.extend([table(['模型', '临床主分数 ↑', '平均秒 ↓', 'P95 秒 ↓', '有效回答 / 题数'], [
            [m['label'], scores[i], means[i], p95s[i], f"{m['timing']['success']} / {m['timing']['total']}"]
            for i, m in enumerate(models)], numeric_from=1),
            '生成式对照模型均关闭思考；每模型并发 8。主分数为场景等权汇总，不是全部题目的简单准确率。加粗仅标记本轮较优数值，不代表差异具有统计显著性。耗时为实际 API 调用的客户端时间，包含网络和重试；不同服务商和运行时段分别记录。',
            '[全部逐任务得分与耗时](docs/MODEL_RESULTS.md) · [原始响应与运行配置](results/clinical-v1/README.md)',
            '以上汇总仅对应原单题 Choice、8 路并发配置。多题打包与并发性能已按任务展示在各场景表中；原全量准确率与性能子集准确率不混算。[逐任务性能协议](docs/TASK_PERFORMANCE.md)。'])
    parts.extend(['## 许可', '第三方数据保留各自的原始许可；见 [第三方声明](THIRD_PARTY_NOTICES.md) 和包内 LICENSE-DATA.md。'])
    output[ROOT / 'README.md'] = '\n\n'.join(parts) + '\n'
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
