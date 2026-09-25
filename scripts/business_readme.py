"""Plain-language homepage for healthcare readers, driven by comparison results."""
import json
from pathlib import Path
from analyze_paired_new import table as paired_table

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
    paired=json.loads((ROOT/'scenarios/evidence/pubmed_rct_section/paired-new/summary.json').read_text())
    merged=next(r for r in paired['results'] if r['group_size']==10)
    replay_cheaper='Jev' if tj['cost_usd']<td['cost_usd'] else 'DeepSeek'
    replay_saving=100*(1-min(tj['cost_usd'],td['cost_usd'])/max(tj['cost_usd'],td['cost_usd']))
    failures={p:sum(v for k,v in r['counts'].items() if k!='ok') for p,r in timing.items()}
    lines=['# Jev 医疗场景评测', '',
           f'主评测覆盖 **12 类医疗场景、96 项任务、{total:,} 条测试输入**，了解 Jev 适合做哪些医疗工作、表现怎样、使用成本多高。DeepSeek Flash 作为同题参考。', '',
           '## 先看结论', '',
           '- **信息分类是目前更值得尝试的方向。** 医疗实体类型识别、病历章节归类、患者问题分类的正确率为 96%–99%；本批效果评测中，相较 DeepSeek，分数接近或更高，模型调用费用低约 39%–56%，适合优先试用在批量整理和分流环节。',
           '- **长病历中的指定问题回答，也显示出较好的性价比。** 在 100 道给定完整病历的选择题上，Jev 正确率为 95%，DeepSeek 为 83%；Jev 的调用费用低约 68%。这一结果对应指定问题回答，整份病历的自动总结仍需另行验证。',
           f'- **同一份材料的多项判断，值得合并处理。** 在另选的 20 篇临床试验摘要上，每篇 10 项判断合并调用，Jev 完成整批平均用时 {merged["jev"]["batch_elapsed_mean_s"]:.1f} 秒，DeepSeek 为 {merged["deepseek"]["batch_elapsed_mean_s"]:.1f} 秒；正确率分别为 {merged["jev"]["accuracy"]:.1%} 和 {merged["deepseek"]["accuracy"]:.1%}。这是新材料、相同问题的配对测试，详见下表。',
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
              '另选 20 篇未进入主评测的临床试验摘要，每篇固定 10 个句子，判断其属于背景、目的、方法、结果还是结论。两家读取相同全文、回答相同问题，分别按每次 1 项、5 项、10 项调用。共 200 个不同判断，每种配置测两轮。', '',
              *paired_table(paired), '',
              '这里比较完成整批 200 项判断的总时间，两轮取平均；同时处理 4 篇摘要，每篇内部依次完成请求。两家均复用连接，DeepSeek 关闭思考；本次没有失败或重试。两轮平均费用显示 Jev 更低，但第二轮缓存增加后，DeepSeek 在 10 项合并组的费用更低。', '',
              '这是医学文献整理的小规模配对实验，不能直接推广到诊断或所有医疗任务。两轮明细、提示词、原始答案与真实响应见[新材料对照实验](scenarios/evidence/pubmed_rct_section/paired-new/README.md)；原主评测的[按问题数量分组观察](comparisons/batch-time/question_counts.md)另行保留。', '',
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
