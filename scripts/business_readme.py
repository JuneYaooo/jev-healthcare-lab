"""Plain-language homepage for healthcare readers, driven by comparison results."""
import json
from pathlib import Path
from question_count_report import table as question_table

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
    question_groups=json.loads((ROOT/'comparisons/batch-time/question_counts.json').read_text())
    replay_cheaper='Jev' if tj['cost_usd']<td['cost_usd'] else 'DeepSeek'
    replay_saving=100*(1-min(tj['cost_usd'],td['cost_usd'])/max(tj['cost_usd'],td['cost_usd']))
    failures={p:sum(v for k,v in r['counts'].items() if k!='ok') for p,r in timing.items()}
    lines=['# Jev 医疗场景评测', '',
           f'覆盖 **12 类医疗场景、96 项任务、{total:,} 条测试输入**，了解 Jev 适合做哪些医疗工作、表现怎样、使用成本多高。DeepSeek Flash 作为同题参考。', '',
           '## 先看结论', '',
           '- **信息分类是目前更值得尝试的方向。** 医疗实体类型识别、病历章节归类、患者问题分类的正确率为 96%–99%；本批效果评测中，相较 DeepSeek，分数接近或更高，模型调用费用低约 39%–56%，适合优先试用在批量整理和分流环节。',
           '- **长病历中的指定问题回答，也显示出较好的性价比。** 在 100 道给定完整病历的选择题上，Jev 正确率为 95%，DeepSeek 为 83%；Jev 的调用费用低约 68%。这一结果对应指定问题回答，整份病历的自动总结仍需另行验证。',
           f'- **批量处理速度需结合实测判断。** 同样以 8 并发处理 {total:,} 条输入，Jev 用时 {tj["batch_elapsed_s"]/60:.1f} 分钟，DeepSeek 用时 {td["batch_elapsed_s"]/60:.1f} 分钟；最终未能作答的输入分别为 {failures["jev"]} 和 {failures["deepseek"]} 条。',
           '- **复杂医疗判断仍有明显短板。** 试验入组判断正确率 48%、临床量表数值判断 25%、中医证型判断 33%；这些任务即使调用便宜，也不足以支持自动决策。', '',
           '## 哪些工作更值得优先试用？', '',
           '以下任务兼具较好的答对率和较低的调用费用。费用按每千条同类输入估算，单位为美元。', '',
           '| 具体工作 | 测试题数 | Jev 正确率 | DeepSeek 正确率 | 每千条费用：Jev / DeepSeek |',
           '| --- | ---: | ---: | ---: | ---: |']
    for scene,t,label in PRIORITIES:
        r=tasks[t]
        lines.append(f'| [{label}](scenarios/{scene}/{t}/README.md) | {r["planned"]} | {score(r["jev"]["quality"]):.1%} | {score(r["deepseek"]["quality"]):.1%} | {money(r["jev"]["cost_per_1000_usd"])} / {money(r["deepseek"]["cost_per_1000_usd"])} |')
    lines += ['', '## 花多少钱，等多久？', '',
              f'在这批效果评测中，Jev 的模型调用费用比 DeepSeek **低约 {saving:.0f}%**；重新调用同样内容测速时，**{replay_cheaper} 的费用低约 {replay_saving:.0f}%**。具体能否节省业务成本，还取决于缓存利用、该任务的准确率和人工复核量。', '',
              '| 对比项 | Jev | DeepSeek Flash |', '| --- | ---: | ---: |',
              f'| 效果评测：每千条输入费用 | {money(j["cost_per_1000_usd"])} | {money(d["cost_per_1000_usd"])} |',
              f'| 重复输入测速：每千条输入费用 | {money(tj["cost_usd"]/total*1000)} | {money(td["cost_usd"]/total*1000)} |',
              f'| 整批 {total:,} 条输入总耗时（8 并发） | {tj["batch_elapsed_s"]/60:.1f} 分钟 | {td["batch_elapsed_s"]/60:.1f} 分钟 |',
              f'| 测速最终未能作答的输入 | {failures["jev"]} 条 | {failures["deepseek"]} 条 |', '',
              '费用为美元估算，仅含模型调用，不含文档识别、语音转写、系统接入和人工复核；一条输入不等于一份完整病历。重复输入可能使 DeepSeek 更多命中缓存，从而显著降价；性价比需要结合实际业务的重复程度判断。总耗时包含重试与失败等待，详见[整批测速](comparisons/batch-time/README.md)。', '',
              '### 单项判断与多项同时判断', '',
              '单项判断，例如给一段病历内容归类；多项同时判断，例如在同一份材料中核对多个候选实体。上面的 8 并发表示同时处理 8 份输入，与每份输入包含几个判断是两回事。', '',
              *question_table(question_groups), '',
              f'本批约 {question_groups["groups"][0]["inputs"]/total:.0%} 的输入只有一个问题。单问题组中 DeepSeek 更快，11 项及以上组中 Jev 更快。表内是单份输入的等待中位数，包含重试与最终失败；整批总耗时仍以上表为准。', '',
              '各组材料和任务不同，以上是现有记录的分组观察，尚不能证明同一份病历合并多个判断后能加速多少。DeepSeek 使用非思考模式、只返回简短答案；重复输入缓存也会影响费用。详见[单项与多项对照](comparisons/batch-time/question_counts.md)。', '',
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
