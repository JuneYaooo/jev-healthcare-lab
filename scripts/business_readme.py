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

def render():
    comparison=json.loads((ROOT/'comparisons/deepseek-flash/summary.json').read_text())
    summary=comparison['summary'];tasks=comparison['tasks']
    if not summary['complete']:raise ValueError('Do not publish an incomplete comparison as final')
    benchmark=[t for t in tasks.values() if not t['synthetic']]
    jwin=sum(score(t['jev']['quality'])>score(t['deepseek']['quality'])+1e-12 for t in benchmark)
    dwin=sum(score(t['deepseek']['quality'])>score(t['jev']['quality'])+1e-12 for t in benchmark)
    tie=len(benchmark)-jwin-dwin
    j=summary['jev'];d=summary['deepseek']
    winner='DeepSeek' if dwin>jwin else 'Jev' if jwin>dwin else '两者'
    lines=['# Jev 在医疗任务中表现如何？', '',
           '这份对比帮助医疗机构、医疗产品团队和行业从业者判断：**Jev 能做好哪些工作，和 DeepSeek 相比准不准、快不快、花多少钱。**', '',
           '## 先看结论', '',
           '- **Jev 在部分明确、范围小的判断任务上表现较好。** 已分段病历的章节分类正确率 99%，已给定实体的类型识别 96%，给定完整长病历的选择题 95%。这些结果支持进一步做场景验证，不能当作整份病历处理准确率。',
           '- **入组判断、复杂抽取和临床评分仍不可靠。** 患者与试验适配三分类正确率 48%，五种量表数值判断 25%，研究要素抽取综合分 12.7/100；这些任务目前不能直接交给 Jev 自动决策。',
           f'- **同题对比中，{winner} 在更多任务上得分更高。** 72 项公开数据测试中，Jev 更高 {jwin} 项，DeepSeek 更高 {dwin} 项，持平 {tie} 项。不同任务不能混成一个“医疗总准确率”。',
           f'- **费用和速度要分开看。** 这批题每千条 API 费用约为 Jev {money(j["cost_per_1000_usd"])}、DeepSeek {money(d["cost_per_1000_usd"])}，Jev 费用约低 {100*(1-j["cost_per_1000_usd"]/d["cost_per_1000_usd"]):.0f}%；典型等待分别为 {j["latency_median_s"]:.2f} 秒和 {d["latency_median_s"]:.2f} 秒。下面列出具体口径。', '',
           '## Jev 与 DeepSeek：效果、等待时间、费用', '',
           '两者使用同一批 **6,586 条输入**，覆盖 **12 类医疗工作、96 项具体测试**。其中 72 项来自公开数据，24 项为自编小样本边界测试；上面的胜负统计只使用前 72 项。', '',
           '| 对比项 | Jev 1.13 | DeepSeek V4.1 Flash（非思考模式） |', '| --- | ---: | ---: |',
           f'| 得分更高的公开数据任务 | {jwin} / 72 | {dwin} / 72 |',
           f'| 最终未能按要求作答的输入 | 0 | {summary["failed_rows"]} |',
           f'| 成功请求典型等待：一半在此时间内完成 | {j["latency_median_s"]:.2f} 秒 | {d["latency_median_s"]:.2f} 秒 |',
           f'| 每千条输入的 API 费用估算 | {money(j["cost_per_1000_usd"])} | {money(d["cost_per_1000_usd"])} |',
           f'| 这批 6,586 条输入的 API 费用估算 | {money(j["cost_usd"])} | {money(d["cost_usd"])} |', '',
           '**怎么看时间和费用**：时间是成功请求从发出到收到完整回答的网络等待，失败尝试和重试前的等待不计入中位数，Jev 来自历史真实记录，DeepSeek 为本次调用，**不是同期测速**。费用按实际 token 用量和官方价格估算，以美元统一列示；DeepSeek 包含实际缓存命中折扣。每条输入可能是一段文本、一道题或一个字段，**不是一份完整病历**；费用不包含 OCR、语音识别、人工复核和系统接入。', '',
           'DeepSeek 的旧名 `deepseek-v4-flash` 已转接到 V4.1 Flash，本表使用实际提供服务的版本。两者接收相同内容和问题，输出格式按各自接口适配。未能作答的输入仍计入评分，不从题数中删除；完整计分方法、失败记录及用量见 [对比实验详情](comparisons/deepseek-flash/README.md)。', '',
           '## 放到具体医疗工作里，表现怎样？', '',
           '下表为事先选定的代表任务，不是各场景平均分。**正确率**表示有多少题答对；**抽取综合分**同时衡量漏检和误报，满分 100，不能当作正确率。', '',
           '| 医疗工作 | 测了什么 | 题数 | Jev | DeepSeek | 读结果时注意 |', '| --- | --- | ---: | ---: | ---: | --- |']
    for scene,label,t,work,note in EXAMPLES:
        r=tasks[t];lines.append(f'| {label} | [{work}](scenarios/{scene}/{t}/README.md) | {r["planned"]} | {display(r["jev"]["quality"])} | {display(r["deepseek"]["quality"])} | {note} |')
    lines += ['', '## 有哪些场景和测试？', '', '| 场景 | 具体测试数 | 输入记录数 |', '| --- | ---: | ---: |']
    scenes=json.loads((ROOT/'results/scenario_manifest.json').read_text())['scenes']
    for s in scenes:
        lines.append(f'| [{s["title"]}](scenarios/{s["id"]}/README.md) | {len(s["task_ids"])} | {sum(tasks[t]["planned"] for t in s["task_ids"]):,} |')
    lines += ['| **合计** | **96** | **6,586** |', '',
              '点击场景可看全部任务；点击任务可看测试数据、提示词、模型回答、逐项分数和费用。原有的重复调用、选项换序等稳定性测试保留在 [实验统计详情](docs/完整任务统计.md)，不计入本次模型对比分数。', '',
              '这些是公开数据及人工构造材料上的离线测试，尚未证明医院实际节省了多少工时。选择模型时，应以准备接入的具体工作为准，尤其要核对错误类型和人工复核成本。', '']
    return '\n'.join(lines)
