"""Render a Jev-focused project homepage and full comparison from archived evidence."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


def score(q):return q.get('accuracy',q.get('micro_f1'))
def display(q):
    if not q:return '待完成'
    return f'{score(q)*100:.1f}'+('% 正确率' if 'accuracy' in q else ' 分·抽取综合分')
def money(v):return f'${v:.3f}'
def highlight_pair(jev, deepseek, *, digits, lower_is_better=False, suffix=''):
    """Bold a strict winner at display precision; missing values cannot win."""
    values = [None if v is None else float(f'{v:.{digits}f}') for v in (jev, deepseek)]
    labels = ['—' if v is None else f'{v:.{digits}f}{suffix}' for v in values]
    if None not in values and values[0] != values[1]:
        winner = 0 if (values[0] < values[1]) == lower_is_better else 1
        labels[winner] = f'**{labels[winner]}**'
    return labels

def research_extensions():
    """Preserve the explicitly maintained extension block during report rebuilds."""
    path = ROOT / 'README.md'
    content = path.read_text() if path.exists() else ''
    start, end = '<!-- research-extensions:start -->', '<!-- research-extensions:end -->'
    if start not in content and end not in content:
        return []
    if content.count(start) != 1 or content.count(end) != 1 or content.index(start) > content.index(end):
        raise ValueError('README research extension markers must form one ordered pair')
    block = content[content.index(start) + len(start):content.index(end)].strip()
    return ['### 研究扩展', '', start, '', block, '', end, '']


# Concrete task examples; full results remain linked alongside the selection.
TASK_EXAMPLES = [
    ('aci_note_section', '把病历内容归入对应章节', '已给定章节边界'),
    ('longhealth_full_context', '读长病历，回答指定问题', '20 个虚构患者的 100 道选择题'),
    ('trialgpt_sigir_referral', '判断患者是否适配临床试验', '给定患者与试验材料，直接三分类'),
    ('medcalc_verified_bounded_score', '给临床量表选出数值评分', '5 种量表，答案来自给定选项'),
]

DOMAIN_EXAMPLES = {
    'service': '给患者提问分类、推荐科室、按规则分流',
    'records': '整理病历、识别肯否定、统一术语、查找错误',
    'reports': '把检验数值对上项目、读懂报告里的肯否定',
    'medication': '识别药物关系、用药变更、剂量与频次',
    'clinical': '比较诊断、检查、治疗、量表及中医相关题目',
    'followup': '识别复诊、复查等后续行动',
    'research': '筛选研究证据、整理 PICO、做患者入组预筛',
    'governance': '核对编码依据、识别隐私候选和有害请求',
}


def render_domain_results(taxonomy, comparison, audit, owner):
    """Show every archived condition once per results view, grouped by business domain."""
    tasks = comparison['tasks']
    mapping = taxonomy['benchmark_tasks']
    if set(mapping) != set(tasks) or set(mapping) != set(audit):
        raise ValueError('README task coverage differs from the comparison or evidence audit')
    families = {f['id']: f for f in taxonomy['families']}
    methods = load('results/task_methods.json')
    inventory = load('results/case_inventory.json')['tasks']
    lines = [
        '## 全部领域与任务的详细测试数据', '',
        f'以下按 {len(taxonomy["domains"])} 个业务领域展开全部 **{len(tasks)} 个主评测条件**。每行并排比较两家的准确率或 F1 与中位响应时间；展开领域下方的详细数据，可查看区间、费用、失败数和原始回答。', '',
        '- **指标**：Accuracy 为准确率；micro-F1 为集合抽取指标，以下均按 0–100 展示，不能混算总体准确率。差值为 Jev 减 DeepSeek，单位为百分点或 F1 分。',
        '- **样本量与区间**：记录数／来源案例数分别列示；来源可能是病例、文档或题目，不等于独立患者。区间按来源案例配对重采样，未校正多重比较。不同任务可能复用来源，案例数不跨任务相加。',
        '- **时间与费用**：中位响应时间只统计成功 API 请求，是历史调用的单次耗时，不是同期测速或整批总时间。每千条费用以全部计分输入为分母，单位为美元，按归档费率估算。',
        '- **失败与原始材料**：未作答包括最终调用或格式失败，仍保留在评分分母；43 条无实体候选记录由规则输出空集，不计为调用失败。“题目”含输入与金标，“Jev／对照”链接两家的原始回答。', '',
    ]
    for domain, title in taxonomy['domains'].items():
        ids = [t for t, r in mapping.items() if families[r['family']]['domain'] == domain]
        records = sum(tasks[t]['planned'] for t in ids)
        lines += [f'<a id="results-{domain}"></a>', '', f'### {title}', '',
                  f'**{len(ids)} 项任务 · {records:,} 条测试记录** · [任务定义与覆盖边界](docs/医疗任务总目录.md#{domain})', '',
                  '| 任务 | 记录／来源案例 | 指标 | Jev 得分 | Jev 耗时（秒） | DeepSeek 得分 | DeepSeek 耗时（秒） |',
                  '| --- | ---: | --- | ---: | ---: | ---: | ---: |']
        for task in ids:
            row = tasks[task]
            a = audit[task]
            folder = f'scenarios/{owner[task]}/{task}'
            metric = '准确率（%）' if a['metric'] == 'accuracy' else 'micro-F1（分）'
            pair = a['paired']
            if row['planned'] != a['records'] or inventory[task]['cases'] != a['cases']:
                raise ValueError(f'Inconsistent README record/case count: {task}')
            scores = highlight_pair(pair['jev']*100, pair['deepseek']*100, digits=1)
            times = highlight_pair(row['jev']['latency_median_s'], row['deepseek']['latency_median_s'], digits=2, lower_is_better=True)
            lines.append(f'| [{methods[task]["title"]}]({folder}/README.md) | {row["planned"]}／[{a["cases"]}]({folder}/cases.md) | {metric} | {scores[0]} | {times[0]} | {scores[1]} | {times[1]} |')
        lines += ['', '<details>', '<summary>展开详细数据：得分差值、费用、失败与原始材料</summary>', '',
                  '差值为 Jev 减 DeepSeek；费用与未作答数的顺序为 **Jev／DeepSeek**。', '',
                  '| 任务 | 得分差值［95% 区间］ | Jev 案例全对 | 每千条费用（美元） | 最终未作答（条） | 原始数据 |',
                  '| --- | ---: | ---: | ---: | ---: | --- |']
        for task in ids:
            row = tasks[task]
            folder = f'scenarios/{owner[task]}/{task}'
            a = audit[task]
            pair = a['paired']
            ci = pair['ci95']['difference']
            cases = a['case_all_correct']['jev']
            cost = '／'.join(money(row[p]['cost_per_1000_usd']) for p in ('jev', 'deepseek'))
            failures = '／'.join(str(audit[task]['failures'][p]) for p in ('jev', 'deepseek'))
            links = f'[题目]({folder}/samples.jsonl) · [提示词]({folder}/prompts.json) · [Jev]({folder}/responses.jsonl) · [对照]({folder}/comparison/deepseek_responses.jsonl)'
            lines.append(f'| [{methods[task]["title"]}]({folder}/README.md) | {pair["difference"]*100:+.1f} ［{ci["lower"]*100:.1f}, {ci["upper"]*100:.1f}］ | {cases["correct"]}/{cases["total"]} | {cost} | {failures} | {links} |')
        lines += ['', '</details>', '', '[返回领域导航](#领域导航)', '']
    return lines


def render():
    comparison = load('comparisons/deepseek-flash/summary.json')
    if not comparison['summary']['complete']:
        raise ValueError('Do not publish an incomplete comparison as final')
    audit = load('results/evidence_audit.json')['tasks']
    taxonomy = load('results/task_taxonomy.json')
    scenes = load('results/scenario_manifest.json')['scenes']
    owner = {t: s['id'] for s in scenes for t in s['task_ids']}
    total = comparison['summary']['planned_rows']
    n_tasks = len(taxonomy['benchmark_tasks'])
    j, d = (comparison['summary'][provider] for provider in ('jev', 'deepseek'))
    timing = {provider: load(f'comparisons/batch-time/{provider}/summary.json') for provider in ('jev', 'deepseek')}
    replay_total = timing['jev']['rows']
    if replay_total != timing['deepseek']['rows']:
        raise ValueError('Timing comparison uses different cohorts')
    long_case = audit['longhealth_full_context']['case_all_correct']['jev']
    out = [
        '# Jev 在医疗领域表现怎么样？', '',
        'Jev Healthcare Lab · 医疗任务实测与原始记录', '',
        '**从病历整理到临床判断，实测 Jev 能做对多少、花多少、等多久。**', '',
        '这个仓库专门评测 Jev 在医疗文本任务中的表现：哪些任务得分高，哪些错误值得注意，调用速度和费用如何。DeepSeek 作为同题参照；每项测试都保留材料、模型回答和评分记录，可以一路查到原题。', '',
        f'**{len(taxonomy["domains"])} 个业务领域 · {n_tasks} 个评测条件 · {total:,} 条测试输入**', '',
        '**[看 Jev 的全部测试数据 →](#全部领域与任务的详细测试数据)　[按领域查看 →](#领域导航)　[查看原题与回答 →](scenarios/README.md)**', '',
        '## Jev 的表现：章节分类 99%，量表评分 25%', '',
        'Jev 给已分段的病历归类时答对 99/100；从给定选项中选出临床量表分数时，答对 25/100。这轮测试中，Jev 在部分分类任务上得分较高，入组预筛和数值评分仍有明显短板。', '',
        '耗时为历史成功请求的中位响应时间（秒）；两家主评测并非同期测速。', '',
        '| 医疗任务 | Jev 准确率 | Jev 耗时（秒） | DeepSeek 准确率 | DeepSeek 耗时（秒） | 实际测的是什么 |',
        '| --- | ---: | ---: | ---: | ---: | --- |',
    ]
    for task, title, boundary in TASK_EXAMPLES:
        pair = audit[task]['paired']
        row = comparison['tasks'][task]
        scores = highlight_pair(pair['jev']*100, pair['deepseek']*100, digits=1, suffix='%')
        times = highlight_pair(row['jev']['latency_median_s'], row['deepseek']['latency_median_s'], digits=2, lower_is_better=True)
        out.append(f'| [{title}](scenarios/{owner[task]}/{task}/README.md) | {scores[0]} | {times[0]} | {scores[1]} | {times[1]} | {boundary} |')
    out += [
        '',
        f'这些是全部 {n_tasks} 项中的四个例子。长病历问答虽然答对 95/100 道题，但只有 {long_case["correct"]}/{long_case["total"]} 个来源病例的题目全部答对。判断 Jev 是否适合你的业务，还要看它错在哪里、会漏掉什么，以及需要多少人工复核。[完整成绩](#全部领域与任务的详细测试数据) · [错误、区间与复核量](docs/医疗适用性审计.md)', '',
        '## Jev 的速度和费用怎么样', '',
        'Jev 在主效果评测中的调用费用更低；在独立重复输入测速中，DeepSeek 的费用更低：', '',
        f'- **主效果评测**：每千条输入，Jev **{money(j["cost_per_1000_usd"])}**，DeepSeek **{money(d["cost_per_1000_usd"])}**。',
        f'- **独立重复输入测速**：每千条输入，Jev **{money(timing["jev"]["cost_usd"]/replay_total*1000)}**，DeepSeek **{money(timing["deepseek"]["cost_usd"]/replay_total*1000)}**。', '',
        f'以上为美元估算，按归档费率和可核验用量计算。重复输入可能提高缓存命中；两组分别为 {total:,} 条和 {replay_total:,} 条输入，费用也不含 OCR、语音转写、系统接入和人工复核。[费用、耗时与调用条件](comparisons/batch-time/README.md)', '',
        f'**速度方面**：独立测速以相同的 8 并发处理 {replay_total:,} 条输入，Jev 用时 **{timing["jev"]["batch_elapsed_s"]/60:.1f} 分钟**，DeepSeek 用时 **{timing["deepseek"]["batch_elapsed_s"]/60:.1f} 分钟**，包含重试与失败等待。', '',
        '如果你的产品需要对一份材料连续做多个判断，还可以看 [140 份新材料的逐项／合并处理实验](comparisons/paired-suite/README.md)：每次处理 1 项、5 项、10 项，对比准确率、总耗时和费用。', '',
        '## 领域导航', '',
        '| 业务领域 | Jev 的测试内容 | 任务数 | 记录数 |',
        '| --- | --- | ---: | ---: |',
    ]
    families = {f['id']: f for f in taxonomy['families']}
    for domain, title in taxonomy['domains'].items():
        ids = [t for t, r in taxonomy['benchmark_tasks'].items() if families[r['family']]['domain'] == domain]
        records = sum(comparison['tasks'][t]['planned'] for t in ids)
        out.append(f'| [{title} →](#results-{domain}) | {DOMAIN_EXAMPLES[domain]} | {len(ids)} | {records:,} |')
    out += [
        '',
        '任务目录同时标明已有实测、独立训练扩展和未测部分；训练扩展不计入 Jev 主评测成绩。中医、OCR 和 ASR 等条件也有单独标记。[查看任务与实验的对应关系](docs/医疗任务映射.md)', '',
        *render_domain_results(taxonomy, comparison, audit, owner),
        '<details>',
        '<summary><strong>评测口径、模型版本与使用边界</strong></summary>', '',
        '- **测了什么**：72 项公开材料适配条件、24 项自编边界挑战。条件数不等于独立医疗工作数，输入数不等于患者数；给定实体、候选或章节边界的任务要按原条件理解。',
        '- **怎么比较**：Jev 为 `jev-1.13.0`；DeepSeek 请求名为 `deepseek-flash`，归档配置记为 V4.1 Flash、关闭思考模式。两者使用相同材料与判断目标；主效果评测不是同期测速。',
        '- **怎么计分**：首页四个例子在分析后选取，全部任务在上方按领域展开。分类报告准确率，集合抽取报告 micro-F1，不混成一个总分。失败留在分母；配对区间按来源案例聚合，属于探索性分析，未校正多重比较。',
        '- **能得出什么**：公开材料、合成病例和小样本测试可帮助筛选下一步验证方向。当前没有真实医院的前瞻性流程验证、独立医生全量审核或患者结局证据。',
        '- **哪些另算**：批处理与扰动实验分别报告；27 类训练任务只作为独立扩展映射，不计入主评测成绩。', '',
        '[详细方法](docs/EVALUATION.md) · [同题对比配置](comparisons/deepseek-flash/README.md) · [来源与未完成项](docs/覆盖与阻塞账本.md)', '',
        '</details>', '',
        '代码使用 [MIT 许可证](LICENSE)；评测文本、标注、媒体和服务输出遵循各自的[第三方使用条件](THIRD_PARTY_NOTICES.md)。引用结果时请记录提交号、任务 ID 和模型版本。', '',
    ]
    extensions = research_extensions()
    if extensions:
        out += ['<details>', '<summary>研究扩展导航</summary>', '', *extensions, '</details>', '']
    return '\n'.join(out)


def render_task_table():
    comparison=load('comparisons/deepseek-flash/summary.json')
    if not comparison['summary']['complete']:
        raise ValueError('Do not publish an incomplete comparison as final')
    tasks=comparison['tasks']
    inventory=load('results/case_inventory.json')['tasks']
    scenes=load('results/scenario_manifest.json')['scenes']
    lines=['', '',
           '以下按场景列出全部 96 项任务。正确率表示答对比例；抽取综合分兼顾漏检和误报，满分 100。费用为每千条同类输入的美元估算。', '',
           '案例按来源中的病例、会话、文档、临床片段或题目计数；同一案例的多个字段不重复算案例，自编测试另有标注。点击案例数可查看逐案例成绩及来源分组，点击任务名称可查看评测方法。', '']
    methods=json.loads((ROOT/'results/task_methods.json').read_text())
    for scene in scenes:
        lines += [f'### {scene["title"]}', '',
                  '| 任务 | 任务类型 | 案例数 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |',
                  '| --- | --- | ---: | ---: | ---: | ---: | ---: |']
        for task in scene['task_ids']:
            r=tasks[task];method=methods[task]
            lines.append(f'| [{method["title"]}](scenarios/{scene["id"]}/{task}/README.md) | {method["task_type"]} | [{inventory[task]['cases']}](scenarios/{scene['id']}/{task}/cases.md) | {r["planned"]} | {display(r["jev"]["quality"])} | {display(r["deepseek"]["quality"])} | {money(r["jev"]["cost_per_1000_usd"])} / {money(r["deepseek"]["cost_per_1000_usd"])} |')
        lines.append('')
    lines += ['[原始实验统计](docs/完整任务统计.md) · [对比实验详情](comparisons/deepseek-flash/README.md)', '']
    body='\n'.join(lines)
    return '# 全部任务的对比表现\n\n[首页](../README.md) · [统计与风险审计](医疗适用性审计.md)\n'+body.replace('](scenarios/', '](../scenarios/').replace('](docs/', '](').replace('](comparisons/', '](../comparisons/')
