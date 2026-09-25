"""Plain-language homepage for healthcare readers, driven by comparison results."""
import json
from pathlib import Path
from analyze_paired_suite import table as suite_table

ROOT=Path(__file__).resolve().parents[1]
def score(q):return q.get('accuracy',q.get('micro_f1'))
def display(q):
    if not q:return '待完成'
    return f'{score(q)*100:.1f}'+('% 正确率' if 'accuracy' in q else ' 分·抽取综合分')
def money(v):return f'${v:.3f}'

# Highlight bounded workflows where measured quality and per-task cost support a pilot.
PRIORITIES=[
    ('records','imcs_entity_type_oracle_span','给已圈出的症状、药品等信息分类'),
    ('documentation','aci_note_section','把已分段的病历内容归入对应章节'),
    ('service','medquad_question_type','把患者提问分为症状、病因等类别'),
    ('records','longhealth_full_context','根据完整长病历回答指定选择题'),
]


def render():
    comparison=json.loads((ROOT/'comparisons/deepseek-flash/summary.json').read_text())
    summary=comparison['summary'];tasks=comparison['tasks']
    if not summary['complete']:raise ValueError('Do not publish an incomplete comparison as final')
    j=summary['jev'];d=summary['deepseek'];total=summary['planned_rows']
    saving=100*(1-j['cost_per_1000_usd']/d['cost_per_1000_usd'])
    timing={p:json.loads((ROOT/f'comparisons/batch-time/{p}/summary.json').read_text()) for p in ['jev','deepseek']}
    tj,td=timing['jev'],timing['deepseek']
    suite=json.loads((ROOT/'comparisons/paired-suite/summary.json').read_text())
    expanded=suite['experiments']
    merged=[next(r for r in e['summary']['results'] if r['group_size']==10) for e in expanded]
    faster=sum(r['jev']['batch_elapsed_mean_s']<r['deepseek']['batch_elapsed_mean_s'] for r in merged)
    evidence=merged[2]
    evidence_single=expanded[2]['summary']['results'][0]
    evidence_f1={p:evidence[p]['quality_detail']['per_class']['evidence']['f1'] for p in ['jev','deepseek']}
    replay_cheaper='Jev' if tj['cost_usd']<td['cost_usd'] else 'DeepSeek'
    replay_saving=100*(1-min(tj['cost_usd'],td['cost_usd'])/max(tj['cost_usd'],td['cost_usd']))
    failures={p:sum(v for k,v in r['counts'].items() if k!='ok') for p,r in timing.items()}
    lines=['# Jev 医疗场景评测', '',
           f'主评测覆盖 **12 类医疗场景、96 项任务、{total:,} 条测试输入**，了解 Jev 适合做哪些医疗工作、表现怎样、使用成本多高。DeepSeek Flash 作为同题参考。', '',
           '## 先看结论', '',
           '- **信息分类是目前更值得尝试的方向。** 医疗实体类型识别、病历章节归类、患者问题分类的正确率为 96%–99%；本批效果评测中，相较 DeepSeek，分数接近或更高，模型调用费用低约 39%–56%，适合优先试用在批量整理和分流环节。',
           '- **长病历中的指定问题回答，也显示出较好的性价比。** 在 100 道给定完整病历的选择题上，Jev 正确率为 95%，DeepSeek 为 83%；Jev 的调用费用低约 68%。这一结果对应指定问题回答，整份病历的自动总结仍需另行验证。',
           f'- **新增 140 份材料检验批量处理。** 在摘要整理、中文问诊归类和证据句筛选三个任务中，每份合并处理 10 项判断时，Jev 在 {faster} 个任务完成整批更快。各场景的正确率、费用和完整批次时间见下表；速度优势需要与该场景的答对率一起看。',
           '- **复杂医疗判断仍有明显短板。** 试验入组判断正确率 48%、临床量表数值判断 25%、中医证型判断 33%；这些任务即使调用便宜，也不足以支持自动决策。', '',
           '## 哪些工作更值得优先试用？', '',
           '以下任务兼具较好的答对率和较低的调用费用。费用按每千条同类输入估算，单位为美元。', '',
           '| 具体工作 | 测试题数 | Jev 正确率 | DeepSeek 正确率 | 每千条费用：Jev / DeepSeek |',
           '| --- | ---: | ---: | ---: | ---: |']
    for scene,t,label in PRIORITIES:
        r=tasks[t]
        lines.append(f'| [{label}](scenarios/{scene}/{t}/README.md) | {r["planned"]} | {score(r["jev"]["quality"]):.1%} | {score(r["deepseek"]["quality"]):.1%} | {money(r["jev"]["cost_per_1000_usd"])} / {money(r["deepseek"]["cost_per_1000_usd"])} |')
    lines += ['', '## 花多少钱，等多久？', '',
              f'在原主评测的 {total:,} 条输入中，Jev 的模型调用费用比 DeepSeek **低约 {saving:.0f}%**；重新调用同样内容测速时，**{replay_cheaper} 的费用低约 {replay_saving:.0f}%**。具体能否节省业务成本，还取决于缓存利用、该任务的准确率和人工复核量。', '',
              '| 对比项 | Jev | DeepSeek Flash |', '| --- | ---: | ---: |',
              f'| 效果评测：每千条输入费用 | {money(j["cost_per_1000_usd"])} | {money(d["cost_per_1000_usd"])} |',
              f'| 重复输入测速：每千条输入费用 | {money(tj["cost_usd"]/total*1000)} | {money(td["cost_usd"]/total*1000)} |',
              f'| 整批 {total:,} 条输入总耗时（8 并发） | {tj["batch_elapsed_s"]/60:.1f} 分钟 | {td["batch_elapsed_s"]/60:.1f} 分钟 |',
              f'| 测速最终未能作答的输入 | {failures["jev"]} 条 | {failures["deepseek"]} 条 |', '',
              '费用为美元估算，仅含模型调用，不含文档识别、语音转写、系统接入和人工复核；一条输入不等于一份完整病历。重复输入可能使 DeepSeek 更多命中缓存，从而显著降价；性价比需要结合实际业务的重复程度判断。总耗时包含重试与失败等待，详见[整批测速](comparisons/batch-time/README.md)。', '',
              '### 新材料实测：逐项处理，还是合并处理？', '',
              '新增 **140 份材料、1,400 个不同判断**：60 篇临床试验摘要、40 段中文问诊、40 组医学主张与文献。每份固定 10 项判断，两家读取相同全文、回答相同问题，分别按每次 1 项、5 项、10 项处理。每种配置测两轮，重复调用不计作新案例。', '',
              *suite_table(expanded), '',
              '总耗时是完成该行场景全部材料的时间，两轮取平均，包含重试和失败等待；同时处理 4 份材料，每份内部依次请求。费用单位为美元。重复内容命中缓存后，费用排序可能改变，各场景子页保留分轮明细。', '',
              f'证据筛选合并 10 项时，Jev 两轮分别用时 {evidence["jev"]["batch_elapsed_s"][0]:.1f} 秒和 {evidence["jev"]["batch_elapsed_s"][1]:.1f} 秒，其中一轮发生超时重试，因此表中平均总时间更长。', '',
              f'证据筛选还需要关注漏检和误报：每次合并 10 项时，Jev 的证据筛选综合分为 {evidence_f1["jev"]*100:.1f}，DeepSeek 为 {evidence_f1["deepseek"]*100:.1f}（满分 100）。整理、分类任务中的优势不能直接推广为诊疗能力。', '',
              f'证据筛选中，DeepSeek 部分答案因格式不符触发重试；按答案含义补充识别后，逐项处理的正确率为 {evidence_single["deepseek"]["semantic_review"]["accuracy"]:.1%}，证据综合分为 {evidence_single["deepseek"]["semantic_review"]["per_class"]["evidence"]["f1"]*100:.1f}。主表仍保留按指定格式完成任务的结果与实际耗时。', '',
              '查看[全部新增案例与对比详情](comparisons/paired-suite/README.md)，可进入各场景查看逐案例成绩、完整测试材料和问题。[此前 20 篇摘要实验](scenarios/evidence/pubmed_rct_section/paired-new/README.md)单独保留，未并入这 140 份材料。', '',
              '## 覆盖哪些医疗场景？', '',
              '共 72 项公开数据任务和 24 项自编边界测试。点击场景可查看全部任务，点击任务可查看测试数据、方法和结果。', '',
              '| 场景 | 具体测试数 | 输入记录数 |', '| --- | ---: | ---: |']
    scenes=json.loads((ROOT/'results/scenario_manifest.json').read_text())['scenes']
    for s in scenes:
        lines.append(f'| [{s["title"]}](scenarios/{s["id"]}/README.md) | {len(s["task_ids"])} | {sum(tasks[t]["planned"] for t in s["task_ids"]):,} |')
    lines += [f'| **合计** | **96** | **{total:,}** |', '',
              '## 全部任务的对比表现', '',
              '以下按场景列出全部 96 项任务。正确率表示答对比例；抽取综合分兼顾漏检和误报，满分 100。费用为每千条同类输入的美元估算。', '',
              '测试记录可能来自同一病例的多个字段，不等于独立病例数；只有几条记录的结果仅作初步观察，不能据此判断稳定性。点击任务名称可查看具体数据与评测方法。', '']
    methods=json.loads((ROOT/'results/task_methods.json').read_text())
    for scene in scenes:
        lines += [f'### {scene["title"]}', '',
                  '| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |',
                  '| --- | --- | ---: | ---: | ---: | ---: |']
        for task in scene['task_ids']:
            r=tasks[task];method=methods[task]
            lines.append(f'| [{method["title"]}](scenarios/{scene["id"]}/{task}/README.md) | {method["task_type"]} | {r["planned"]} | {display(r["jev"]["quality"])} | {display(r["deepseek"]["quality"])} | {money(r["jev"]["cost_per_1000_usd"])} / {money(r["deepseek"]["cost_per_1000_usd"])} |')
        lines.append('')
    lines += ['[原始实验统计](docs/完整任务统计.md) · [对比实验详情](comparisons/deepseek-flash/README.md)', '']
    return '\n'.join(lines)
