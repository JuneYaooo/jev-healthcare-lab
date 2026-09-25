"""Plain-language homepage for healthcare readers, driven by comparison results."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
# Fixed representative examples chosen before the comparison completed.
EXAMPLES=[
('records','病历信息整理','imcs_entity_type_oracle_span','识别已圈出的症状、药品等实体类型','这里只判断类型，实体位置已给出'),
('records','病历信息整理','imcs_ner_dictionary_pipeline','从中文句子中找出医疗实体','同时看漏检和误报'),
('documentation','文书归档','aci_note_section','判断文本属于哪一类病历章节','章节边界已给出，不是自动写病历'),
('service','患者咨询','medquad_question_type','判断患者在问症状、病因还是其他信息','评测问题分类，不是回复质量'),
('quality','病历质控','medec_error_detection','发现病历中的医学错误','不能只看总体分，还要看漏错'),
('quality','回答核查','medhallu_with_evidence','结合参考证据识别医学回答幻觉','已提供证据，不含联网检索'),
('medication','药物信息','cdrugred_discharge_candidate_pipeline','筛选出院带药候选','不是可直接用于处方的验证'),
('trials','临床试验','trialgpt_sigir_referral','初筛患者是否适合某个试验','还需人工逐条核对纳排标准'),
('evidence','医学研究','ebm_pico_fixed_windows','识别研究人群、干预和结局片段','评测固定文本窗口，不是全文综述'),
('calculators','临床评分','medcalc_verified_bounded_score','从病历判断五种量表的数值','未提供公式，不能外推所有计算器'),
('knowledge','医学知识','medqa_zh_test','回答中文医学选择题','考试成绩不等于临床诊断能力'),
('multimodal','语音病历','primock_asr_fields','从语音转写中判断病史字段','只有一段扮演患者音频、12 个字段'),
('acute','病例判断','ddxplus_synthetic_primary','为合成病例选择主要诊断','合成病例，不是真实临床诊断'),
('tcm','中医辨证','tcm_syndrome','从中医病例中选择证型','候选共 148 个证型及无法判断选项'),
]

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
    j=summary['jev'];d=summary['deepseek']
    saving=100*(1-j['cost_per_1000_usd']/d['cost_per_1000_usd'])
    lines=['# Jev 医疗场景评测', '',
           '覆盖 **12 类医疗场景、96 项任务、6,586 条测试输入**，了解 Jev 适合做哪些医疗工作、表现怎样、使用成本多高。DeepSeek Flash 作为同题参考。', '',
           '## 先看结论', '',
           '- **信息分类是目前更值得尝试的方向。** 医疗实体类型识别、病历章节归类、患者问题分类的正确率为 96%–99%；相较 DeepSeek，分数接近或更高，模型调用费用低约 39%–56%，适合优先试用在批量整理和分流环节。',
           '- **长病历中的指定问题回答，也显示出较好的性价比。** 在 100 道给定完整病历的选择题上，Jev 正确率为 95%，DeepSeek 为 83%；Jev 的调用费用低约 68%。这一结果对应指定问题回答，整份病历的自动总结仍需另行验证。',
           '- **复杂医疗判断仍有明显短板。** 试验入组判断正确率 48%、临床量表数值判断 25%、中医证型判断 33%；这些任务即使调用便宜，也不足以支持自动决策。', '',
           '## 哪些工作更值得优先试用？', '',
           '以下任务兼具较好的答对率和较低的调用费用。费用按每千条同类输入估算，单位为美元。', '',
           '| 具体工作 | 测试题数 | Jev 正确率 | DeepSeek 正确率 | 每千条费用：Jev / DeepSeek |',
           '| --- | ---: | ---: | ---: | ---: |']
    for scene,t,label in PRIORITIES:
        r=tasks[t]
        lines.append(f'| [{label}](scenarios/{scene}/{t}/README.md) | {r["planned"]} | {score(r["jev"]["quality"]):.1%} | {score(r["deepseek"]["quality"]):.1%} | {money(r["jev"]["cost_per_1000_usd"])} / {money(r["deepseek"]["cost_per_1000_usd"])} |')
    lines += ['', '## 其他医疗工作表现怎样？', '',
              '下表展示各场景中的具体测试。正确率表示答对比例；抽取综合分兼顾漏检和误报，满分 100。每行代表一个任务，不能当作整个场景的平均水平。', '',
              '| 医疗工作与测试内容 | 题数 | Jev | DeepSeek | 适用范围 |',
              '| --- | ---: | ---: | ---: | --- |']
    priorities={t for _,t,_ in PRIORITIES}
    for scene,label,t,work,note in EXAMPLES:
        if t in priorities:continue
        r=tasks[t]
        lines.append(f'| [{label}：{work}](scenarios/{scene}/{t}/README.md) | {r["planned"]} | {display(r["jev"]["quality"])} | {display(r["deepseek"]["quality"])} | {note} |')
    lines += ['', '## 花多少钱，等多久？', '',
              f'按全部测试输入合计，Jev 的模型调用费用比 DeepSeek **低约 {saving:.0f}%**。具体能否节省业务成本，还取决于该任务的准确率和人工复核量。', '',
              '| 对比项 | Jev | DeepSeek Flash |', '| --- | ---: | ---: |',
              f'| 每千条输入的模型调用费用 | {money(j["cost_per_1000_usd"])} | {money(d["cost_per_1000_usd"])} |',
              '| 整批任务总耗时（相同并发） | 待实测 | 待实测 |', '',
              '费用为美元估算，仅含模型调用，不含文档识别、语音转写、系统接入和人工复核；一条输入不等于一份完整病历。现有记录尚不能比较同等条件下的整批处理速度。', '',
              '## 覆盖哪些医疗场景？', '',
              '共 72 项公开数据任务和 24 项自编边界测试。点击场景可查看全部任务，点击任务可查看测试数据、方法和结果。', '',
              '| 场景 | 具体测试数 | 输入记录数 |', '| --- | ---: | ---: |']
    scenes=json.loads((ROOT/'results/scenario_manifest.json').read_text())['scenes']
    for s in scenes:
        lines.append(f'| [{s["title"]}](scenarios/{s["id"]}/README.md) | {len(s["task_ids"])} | {sum(tasks[t]["planned"] for t in s["task_ids"]):,} |')
    lines += ['| **合计** | **96** | **6,586** |', '',
              '[完整任务结果](docs/完整任务统计.md) · [对比实验详情](comparisons/deepseek-flash/README.md)', '']
    return '\n'.join(lines)
