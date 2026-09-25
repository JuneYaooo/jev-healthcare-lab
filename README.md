# Jev 医疗场景评测

主评测覆盖 **12 类医疗场景、96 项任务、7,032 条测试输入**，了解 Jev 适合做哪些医疗工作、表现怎样、使用成本多高。DeepSeek Flash 作为同题参考。

## 先看结论

- **信息分类是目前更值得尝试的方向。** 医疗实体类型识别、病历章节归类、患者问题分类的正确率为 96%–99%；本批效果评测中，相较 DeepSeek，分数接近或更高，模型调用费用低约 39%–56%，适合优先试用在批量整理和分流环节。
- **长病历中的指定问题回答，也显示出较好的性价比。** 在 100 道给定完整病历的选择题上，Jev 正确率为 95%，DeepSeek 为 83%；Jev 的调用费用低约 68%。这一结果对应指定问题回答，整份病历的自动总结仍需另行验证。
- **同一份材料的多项判断，值得合并处理。** 在另选的 20 篇临床试验摘要上，每篇 10 项判断合并调用，Jev 完成整批平均用时 1.7 秒，DeepSeek 为 4.5 秒；正确率分别为 88.0% 和 89.2%。这是新材料、相同问题的配对测试，详见下表。
- **复杂医疗判断仍有明显短板。** 试验入组判断正确率 48%、临床量表数值判断 25%、中医证型判断 33%；这些任务即使调用便宜，也不足以支持自动决策。

## 哪些工作更值得优先试用？

以下任务兼具较好的答对率和较低的调用费用。费用按每千条同类输入估算，单位为美元。

| 具体工作 | 测试题数 | Jev 正确率 | DeepSeek 正确率 | 每千条费用：Jev / DeepSeek |
| --- | ---: | ---: | ---: | ---: |
| [给已圈出的症状、药品等信息分类](scenarios/records/imcs_entity_type_oracle_span/README.md) | 100 | 96.0% | 92.0% | $0.019 / $0.031 |
| [把已分段的病历内容归入对应章节](scenarios/documentation/aci_note_section/README.md) | 100 | 99.0% | 100.0% | $0.021 / $0.048 |
| [把患者提问分为症状、病因等类别](scenarios/service/medquad_question_type/README.md) | 100 | 96.0% | 97.0% | $0.020 / $0.034 |
| [根据完整长病历回答指定选择题](scenarios/records/longhealth_full_context/README.md) | 100 | 95.0% | 83.0% | $0.537 / $1.697 |

## 花多少钱，等多久？

在原主评测的 7,032 条输入中，Jev 的模型调用费用比 DeepSeek **低约 56%**；重新调用同样内容测速时，**DeepSeek 的费用低约 13%**。具体能否节省业务成本，还取决于缓存利用、该任务的准确率和人工复核量。

| 对比项 | Jev | DeepSeek Flash |
| --- | ---: | ---: |
| 效果评测：每千条输入费用 | $0.055 | $0.124 |
| 重复输入测速：每千条输入费用 | $0.055 | $0.048 |
| 整批 7,032 条输入总耗时（8 并发） | 22.1 分钟 | 18.2 分钟 |
| 测速最终未能作答的输入 | 1 条 | 38 条 |

费用为美元估算，仅含模型调用，不含文档识别、语音转写、系统接入和人工复核；一条输入不等于一份完整病历。重复输入可能使 DeepSeek 更多命中缓存，从而显著降价；性价比需要结合实际业务的重复程度判断。总耗时包含重试与失败等待，详见[整批测速](comparisons/batch-time/README.md)。

### 新材料实测：逐项处理，还是合并处理？

另选 20 篇未进入主评测的临床试验摘要，每篇固定 10 个句子，判断其属于背景、目的、方法、结果还是结论。两家读取相同全文、回答相同问题，分别按每次 1 项、5 项、10 项调用。共 200 个不同判断，每种配置测两轮。

| 每次处理的判断数 | 正确率：Jev / DeepSeek | 完成全部 20 篇总耗时：Jev / DeepSeek | 每千项判断费用：Jev / DeepSeek |
| --- | ---: | ---: | ---: |
| 1 项 | 88.0% / 89.2% | 14.5 / 34.6 秒 | $0.040 / $0.076 |
| 5 项 | 88.0% / 88.8% | 3.4 / 8.0 秒 | $0.012 / $0.019 |
| 10 项 | 88.0% / 89.2% | 1.7 / 4.5 秒 | $0.008 / $0.015 |

这里比较完成整批 200 项判断的总时间，两轮取平均；同时处理 4 篇摘要，每篇内部依次完成请求。两家均复用连接，DeepSeek 关闭思考；本次没有失败或重试。两轮平均费用显示 Jev 更低，但第二轮缓存增加后，DeepSeek 在三个分组的费用均更低。

这是医学文献整理的小规模配对实验，不能直接推广到诊断或所有医疗任务。两轮明细、提示词、原始答案与真实响应见[新材料对照实验](scenarios/evidence/pubmed_rct_section/paired-new/README.md)；原主评测的[按问题数量分组观察](comparisons/batch-time/question_counts.md)另行保留。

## 覆盖哪些医疗场景？

共 72 项公开数据任务和 24 项自编边界测试。点击场景可查看全部任务，点击任务可查看测试数据、方法和结果。

| 场景 | 具体测试数 | 输入记录数 |
| --- | ---: | ---: |
| [病历实体、否定状态与术语标准化](scenarios/records/README.md) | 18 | 1,240 |
| [病历章节、文书质控与随访记录](scenarios/documentation/README.md) | 5 | 260 |
| [患者咨询、服务路由与就医流程](scenarios/service/README.md) | 9 | 740 |
| [医疗质控、幻觉识别与请求安全](scenarios/quality/README.md) | 11 | 1,157 |
| [药物关系、用药变更与出院带药](scenarios/medication/README.md) | 7 | 430 |
| [患者入组预筛与临床试验匹配](scenarios/trials/README.md) | 3 | 350 |
| [循证研究、PICO 与公共卫生核查](scenarios/evidence/README.md) | 10 | 875 |
| [临床计算、参数选择与评分量表](scenarios/calculators/README.md) | 8 | 562 |
| [医学知识与考试对照](scenarios/knowledge/README.md) | 5 | 415 |
| [语音病历、医疗文档 OCR 与报告断言](scenarios/multimodal/README.md) | 5 | 100 |
| [合成病例主要诊断](scenarios/acute/README.md) | 1 | 100 |
| [中医知识、辨证与安全](scenarios/tcm/README.md) | 14 | 803 |
| **合计** | **96** | **7,032** |

## 全部任务的对比表现

以下按场景列出全部 96 项任务。正确率表示答对比例；抽取综合分兼顾漏检和误报，满分 100。费用为每千条同类输入的美元估算。

测试记录可能来自同一病例的多个字段，不等于独立病例数；只有几条记录的结果仅作初步观察，不能据此判断稳定性。点击任务名称可查看具体数据与评测方法。

### 病历实体、否定状态与术语标准化

| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |
| --- | --- | ---: | ---: | ---: | ---: |
| [中文症状肯否定状态](scenarios/records/imcs_assertion_oracle_span/README.md) | 实体状态分类 | 100 | 79.0% 正确率 | 73.0% 正确率 | $0.096 / $0.209 |
| [中文给定实体类型识别](scenarios/records/imcs_entity_type_oracle_span/README.md) | 实体类型分类 | 100 | 96.0% 正确率 | 92.0% 正确率 | $0.019 / $0.031 |
| [中文词典候选实体抽取](scenarios/records/imcs_ner_dictionary_pipeline/README.md) | 实体抽取与筛选 | 100 | 59.5 分·抽取综合分 | 59.2 分·抽取综合分 | $0.021 / $0.045 |
| [中文症状术语归一化](scenarios/records/imcs_normalization_top20/README.md) | 术语归一化 | 100 | 93.0% 正确率 | 92.0% 正确率 | $0.037 / $0.049 |
| [英文句子否定与不确定线索](scenarios/records/bioscope_sentence_cues/README.md) | 句子线索分类 | 100 | 83.0% 正确率 | 77.0% 正确率 | $0.018 / $0.032 |
| [西班牙文否定与不确定性](scenarios/records/nubes_scope_status/README.md) | 实体状态分类 | 100 | 72.0% 正确率 | 77.0% 正确率 | $0.019 / $0.039 |
| [给定疾病实体类别](scenarios/records/ncbi_disease_category_oracle_span/README.md) | 实体类型分类 | 100 | 58.0% 正确率 | 61.0% 正确率 | $0.030 / $0.058 |
| [medspaCy 候选与 Jev 疾病实体筛选](scenarios/records/ncbi_medspacy_jev_ner/README.md) | 实体抽取与筛选 | 100 | 69.4 分·抽取综合分 | 68.7 分·抽取综合分 | $0.049 / $0.191 |
| [医学实体 UMLS 语义类型](scenarios/records/medmentions_type_oracle_span/README.md) | 实体类型分类 | 100 | 60.0% 正确率 | 51.0% 正确率 | $0.044 / $0.096 |
| [医学缩写消歧](scenarios/records/medal_demo_disambiguation/README.md) | 缩写消歧 | 100 | 67.0% 正确率 | 35.0% 正确率 | $0.116 / $0.082 |
| [长病历跨文档问答](scenarios/records/longhealth_full_context/README.md) | 证据问答 | 100 | 95.0% 正确率 | 83.0% 正确率 | $0.537 / $1.697 |
| [边界挑战：编码证据](scenarios/records/challenge_coding_evidence/README.md) | 编码证据判断 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.016 / $0.044 |
| [边界挑战：症状所属人](scenarios/records/challenge_experiencer/README.md) | 主体归属判断 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.016 / $0.041 |
| [边界挑战：中英混合文本](scenarios/records/challenge_mixed_language/README.md) | 跨语言语义判断 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.015 / $0.039 |
| [边界挑战：否定状态](scenarios/records/challenge_negation/README.md) | 否定识别 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.015 / $0.041 |
| [边界挑战：相对日期](scenarios/records/challenge_relative_date/README.md) | 相对时间解析 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.018 / $0.030 |
| [边界挑战：社会背景](scenarios/records/challenge_social_context/README.md) | 社会背景识别 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.016 / $0.041 |
| [边界挑战：事件时态](scenarios/records/challenge_temporality/README.md) | 事件时态判断 | 20 | 100.0% 正确率 | 75.0% 正确率 | $0.016 / $0.042 |

### 病历章节、文书质控与随访记录

| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |
| --- | --- | ---: | ---: | ---: | ---: |
| [问诊对话对应病历章节](scenarios/documentation/mts_section_classification/README.md) | 章节分类 | 100 | 76.0% 正确率 | 73.0% 正确率 | $0.031 / $0.044 |
| [已分段病历章节分类](scenarios/documentation/aci_note_section/README.md) | 章节分类 | 100 | 99.0% 正确率 | 100.0% 正确率 | $0.021 / $0.048 |
| [边界挑战：文档类型](scenarios/documentation/challenge_document_type/README.md) | 文档类型分类 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.016 / $0.042 |
| [边界挑战：文书缺项](scenarios/documentation/challenge_documentation/README.md) | 文书缺项判断 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.016 / $0.042 |
| [边界挑战：随访行动](scenarios/documentation/challenge_followup_action/README.md) | 行动项识别 | 20 | 95.0% 正确率 | 100.0% 正确率 | $0.016 / $0.043 |

### 患者咨询、服务路由与就医流程

| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |
| --- | --- | ---: | ---: | ---: | ---: |
| [中文问诊对话行为分类](scenarios/service/imcs_dialogue_act/README.md) | 意图分类 | 100 | 70.0% 正确率 | 68.0% 正确率 | $0.033 / $0.042 |
| [患者问题信息需求分类](scenarios/service/medquad_question_type/README.md) | 意图分类 | 100 | 96.0% 正确率 | 97.0% 正确率 | $0.020 / $0.034 |
| [主诉推荐就诊科室](scenarios/service/medjourney_departments/README.md) | 多标签科室推荐 | 100 | 36.9 分·抽取综合分 | 34.9 分·抽取综合分 | $0.360 / $0.373 |
| [MedJourney 诊断预测选择题](scenarios/service/medjourney_dp_mcq/README.md) | 单选问答 | 100 | 92.0% 正确率 | 91.0% 正确率 | $0.022 / $0.037 |
| [MedJourney 检查预测选择题](scenarios/service/medjourney_ep_mcq/README.md) | 单选问答 | 100 | 82.0% 正确率 | 79.0% 正确率 | $0.022 / $0.038 |
| [MedJourney 用药预测选择题](scenarios/service/medjourney_mp_mcq/README.md) | 单选问答 | 100 | 86.0% 正确率 | 88.0% 正确率 | $0.020 / $0.034 |
| [MedJourney 治疗预测选择题](scenarios/service/medjourney_tp_mcq/README.md) | 单选问答 | 100 | 83.0% 正确率 | 82.0% 正确率 | $0.024 / $0.040 |
| [边界挑战：服务路由](scenarios/service/challenge_service_route/README.md) | 服务路由分类 | 20 | 95.0% 正确率 | 100.0% 正确率 | $0.016 / $0.042 |
| [边界挑战：给定规则紧急程度](scenarios/service/challenge_urgency_given_policy/README.md) | 规则紧急程度分类 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.018 / $0.031 |

### 医疗质控、幻觉识别与请求安全

| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |
| --- | --- | ---: | ---: | ---: | ---: |
| [医疗叙述错误检出](scenarios/quality/medec_error_detection/README.md) | 错误检出 | 100 | 65.0% 正确率 | 60.0% 正确率 | $0.031 / $0.077 |
| [医疗叙述错误定位](scenarios/quality/medec_error_localization/README.md) | 错误定位 | 100 | 72.0% 正确率 | 70.0% 正确率 | $0.039 / $0.089 |
| [阿拉伯文医疗文本错误检出](scenarios/quality/mederrbench_ARA/README.md) | 错误检出 | 97 | 69.1% 正确率 | 59.8% 正确率 | $0.019 / $0.035 |
| [中文医疗文本错误检出](scenarios/quality/mederrbench_CN/README.md) | 错误检出 | 100 | 73.0% 正确率 | 74.0% 正确率 | $0.018 / $0.033 |
| [英文医疗文本错误检出](scenarios/quality/mederrbench_EN/README.md) | 错误检出 | 100 | 81.0% 正确率 | 79.0% 正确率 | $0.023 / $0.049 |
| [医学回答幻觉识别：有证据](scenarios/quality/medhallu_with_evidence/README.md) | 幻觉识别 | 200 | 82.0% 正确率 | 82.5% 正确率 | $0.032 / $0.077 |
| [医学回答幻觉识别：无证据](scenarios/quality/medhallu_without_evidence/README.md) | 幻觉识别 | 200 | 60.0% 正确率 | 69.5% 正确率 | $0.017 / $0.032 |
| [医疗有害请求筛查](scenarios/quality/medsafety_request_gate/README.md) | 请求安全分类 | 200 | 93.5% 正确率 | 96.0% 正确率 | $0.015 / $0.042 |
| [边界挑战：病历矛盾](scenarios/quality/challenge_contradiction/README.md) | 矛盾检测 | 20 | 100.0% 正确率 | 95.0% 正确率 | $0.016 / $0.042 |
| [边界挑战：隐私信息候选](scenarios/quality/challenge_phi_candidate/README.md) | 隐私信息识别 | 20 | 95.0% 正确率 | 95.0% 正确率 | $0.016 / $0.043 |
| [边界挑战：提示注入](scenarios/quality/challenge_prompt_injection/README.md) | 提示注入抵抗 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.017 / $0.043 |

### 药物关系、用药变更与出院带药

| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |
| --- | --- | ---: | ---: | ---: | ---: |
| [化学物致病关系判断](scenarios/medication/bc5cdr_relation_oracle_entities/README.md) | 关系分类 | 100 | 57.0% 正确率 | 66.0% 正确率 | $0.031 / $0.069 |
| [给定药物对相互作用分类](scenarios/medication/ddi_relation_oracle_pairs/README.md) | 关系分类 | 150 | 79.3% 正确率 | 74.7% 正确率 | $0.024 / $0.038 |
| [出院带药候选筛选](scenarios/medication/cdrugred_discharge_candidate_pipeline/README.md) | 多标签候选筛选 | 100 | 48.6 分·抽取综合分 | 47.9 分·抽取综合分 | $0.218 / $0.587 |
| [边界挑战：过敏状态](scenarios/medication/challenge_allergy_state/README.md) | 过敏状态判断 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.016 / $0.043 |
| [边界挑战：药物剂量关联](scenarios/medication/challenge_dose_link/README.md) | 剂量关联判断 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.016 / $0.043 |
| [边界挑战：给药频次](scenarios/medication/challenge_frequency/README.md) | 频次解析 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.016 / $0.043 |
| [边界挑战：用药变更](scenarios/medication/challenge_medication_change/README.md) | 用药变更判断 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.016 / $0.043 |

### 患者入组预筛与临床试验匹配

| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |
| --- | --- | ---: | ---: | ---: | ---: |
| [临床试验证据支持判断](scenarios/trials/nli4ct_entailment/README.md) | 文本蕴含判断 | 100 | 88.0% 正确率 | 87.0% 正确率 | $0.040 / $0.080 |
| [临床试验证据句定位](scenarios/trials/nli4ct_evidence/README.md) | 证据句筛选 | 100 | 49.9 分·抽取综合分 | 68.3 分·抽取综合分 | $0.073 / $0.200 |
| [患者与临床试验入组预筛](scenarios/trials/trialgpt_sigir_referral/README.md) | 入组适配分类 | 150 | 48.0% 正确率 | 54.7% 正确率 | $0.038 / $0.096 |

### 循证研究、PICO 与公共卫生核查

| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |
| --- | --- | ---: | ---: | ---: | ---: |
| [PICO 固定窗口识别](scenarios/evidence/ebm_pico_fixed_windows/README.md) | PICO 多标签识别 | 100 | 12.7 分·抽取综合分 | 25.4 分·抽取综合分 | $0.034 / $0.084 |
| [临床研究干预结果方向](scenarios/evidence/evidence_inference_fulltext/README.md) | 干预效果方向分类 | 100 | 89.0% 正确率 | 76.0% 正确率 | $0.325 / $1.041 |
| [研究结局固定窗口分类](scenarios/evidence/evidenceoutcomes_fixed_window/README.md) | 研究结局识别 | 100 | 88.0% 正确率 | 67.0% 正确率 | $0.044 / $0.108 |
| [全文证据句筛选](scenarios/evidence/evidencebench_sentence_selection/README.md) | 证据句筛选 | 37 | 29.4 分·抽取综合分 | 25.9 分·抽取综合分 | $0.609 / $1.927 |
| [摘要支持的研究问题回答](scenarios/evidence/pubmedqa_evidence_qa/README.md) | 证据问答 | 100 | 74.0% 正确率 | 76.0% 正确率 | $0.030 / $0.069 |
| [RCT 摘要句功能分类](scenarios/evidence/pubmed_rct_section/README.md) | 章节分类 | 100 | 75.0% 正确率 | 77.0% 正确率 | $0.017 / $0.036 |
| [科学论断与给定摘要一致性](scenarios/evidence/scifact_cited_abstract/README.md) | 文本蕴含判断 | 118 | 85.6% 正确率 | 89.0% 正确率 | $0.033 / $0.077 |
| [公共卫生核查：仅论断](scenarios/evidence/pubhealth_claim_only/README.md) | 事实核查分类 | 100 | 20.0% 正确率 | 44.0% 正确率 | $0.016 / $0.033 |
| [公共卫生核查：提供核查文章](scenarios/evidence/pubhealth_with_article/README.md) | 事实核查分类 | 100 | 67.0% 正确率 | 72.0% 正确率 | $0.052 / $0.151 |
| [边界挑战：证据支持](scenarios/evidence/challenge_evidence_support/README.md) | 证据支持判断 | 20 | 100.0% 正确率 | 75.0% 正确率 | $0.016 / $0.043 |

### 临床计算、参数选择与评分量表

| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |
| --- | --- | ---: | ---: | ---: | ---: |
| [BMI 当前身高参数选择](scenarios/calculators/bmi_height_selection/README.md) | 数值参数选择 | 20 | 95.0% 正确率 | 95.0% 正确率 | $0.045 / $0.116 |
| [BMI 当前体重参数选择](scenarios/calculators/bmi_weight_selection/README.md) | 数值参数选择 | 20 | 95.0% 正确率 | 90.0% 正确率 | $0.043 / $0.111 |
| [临床计算输入充分性](scenarios/calculators/cmedcalc_input_sufficiency/README.md) | 输入充分性判断 | 200 | 81.5% 正确率 | 84.0% 正确率 | $0.043 / $0.078 |
| [临床量表语义分级](scenarios/calculators/cmedcalc_semantic_grade/README.md) | 量表分级 | 162 | 60.5% 正确率 | 39.5% 正确率 | $0.027 / $0.046 |
| [五种临床量表闭集数值评分](scenarios/calculators/medcalc_verified_bounded_score/README.md) | 闭集数值评分 | 100 | 25.0% 正确率 | 31.0% 正确率 | $0.051 / $0.136 |
| [边界挑战：检验数值关联](scenarios/calculators/challenge_lab_link/README.md) | 检验数值关联 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.017 / $0.041 |
| [边界挑战：缺失计算参数](scenarios/calculators/challenge_missing_parameter/README.md) | 输入充分性判断 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.016 / $0.043 |
| [边界挑战：单位等价](scenarios/calculators/challenge_unit_equivalence/README.md) | 单位等价判断 | 20 | 95.0% 正确率 | 100.0% 正确率 | $0.015 / $0.042 |

### 医学知识与考试对照

| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |
| --- | --- | ---: | ---: | ---: | ---: |
| [英文 MedQA医学考试](scenarios/knowledge/medqa_en_test/README.md) | 单选问答 | 100 | 83.0% 正确率 | 78.0% 正确率 | $0.024 / $0.053 |
| [中文 MedQA医学考试](scenarios/knowledge/medqa_zh_test/README.md) | 单选问答 | 100 | 89.0% 正确率 | 84.0% 正确率 | $0.018 / $0.034 |
| [MedMCQA医学考试](scenarios/knowledge/medmcqa_validation/README.md) | 单选问答 | 100 | 72.0% 正确率 | 67.0% 正确率 | $0.016 / $0.037 |
| [中文医学考试单选](scenarios/knowledge/cmexam_mcq/README.md) | 单选问答 | 95 | 92.6% 正确率 | 85.3% 正确率 | $0.017 / $0.039 |
| [中文医学考试多选](scenarios/knowledge/cmexam_mcq_multi/README.md) | 多选问答 | 20 | 83.2 分·抽取综合分 | 90.3 分·抽取综合分 | $0.020 / $0.061 |

### 语音病历、医疗文档 OCR 与报告断言

| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |
| --- | --- | ---: | ---: | ---: | ---: |
| [ASR 转写病史字段判断](scenarios/multimodal/primock_asr_fields/README.md) | 病史字段判断 | 20 | 95.0% 正确率 | 95.0% 正确率 | $0.031 / $0.079 |
| [参考转写病史字段判断](scenarios/multimodal/primock_reference_fields/README.md) | 病史字段判断 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.036 / $0.100 |
| [OCR 文本医疗文档类型识别](scenarios/multimodal/clinocr_ocr_doctype/README.md) | 文档类型分类 | 20 | 95.0% 正确率 | 85.0% 正确率 | $0.037 / $0.088 |
| [参考文本医疗文档类型识别](scenarios/multimodal/clinocr_reference_doctype/README.md) | 文档类型分类 | 20 | 95.0% 正确率 | 95.0% 正确率 | $0.038 / $0.079 |
| [边界挑战：影像报告断言](scenarios/multimodal/challenge_radiology_assertion/README.md) | 报告断言判断 | 20 | 100.0% 正确率 | 100.0% 正确率 | $0.016 / $0.043 |

### 合成病例主要诊断

| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |
| --- | --- | ---: | ---: | ---: | ---: |
| [合成病例主要诊断](scenarios/acute/ddxplus_synthetic_primary/README.md) | 诊断分类 | 100 | 67.0% 正确率 | 71.0% 正确率 | $0.072 / $0.095 |

### 中医知识、辨证与安全

| 任务 | 任务类型 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |
| --- | --- | ---: | ---: | ---: | ---: |
| [中医病历证型分类](scenarios/tcm/tcm_syndrome/README.md) | 证型分类 | 100 | 33.0% 正确率 | 40.0% 正确率 | $0.170 / $0.098 |
| [医学伦理单选](scenarios/tcm/tcm_best_ethics/README.md) | 单选问答 | 97 | 89.7% 正确率 | 79.4% 正确率 | $0.020 / $0.038 |
| [医学伦理多选](scenarios/tcm/tcm_best_ethics_multi/README.md) | 多选问答 | 3 | 81.8 分·抽取综合分 | 96.0 分·抽取综合分 | $0.020 / $0.050 |
| [中医基础知识单选](scenarios/tcm/tcm_best_knowledge/README.md) | 单选问答 | 89 | 91.0% 正确率 | 83.1% 正确率 | $0.016 / $0.040 |
| [中医基础知识多选](scenarios/tcm/tcm_best_knowledge_multi/README.md) | 多选问答 | 11 | 79.3 分·抽取综合分 | 84.9 分·抽取综合分 | $0.018 / $0.046 |
| [中医病位单选](scenarios/tcm/tcm_best_location/README.md) | 单选问答 | 21 | 81.0% 正确率 | 76.2% 正确率 | $0.024 / $0.041 |
| [中医病位多选](scenarios/tcm/tcm_best_location_multi/README.md) | 多选问答 | 79 | 64.8 分·抽取综合分 | 66.7 分·抽取综合分 | $0.033 / $0.102 |
| [中医病性单选](scenarios/tcm/tcm_best_nature/README.md) | 单选问答 | 99 | 69.7% 正确率 | 59.6% 正确率 | $0.024 / $0.045 |
| [中医病性多选](scenarios/tcm/tcm_best_nature_multi/README.md) | 多选问答 | 2 | 80.0 分·抽取综合分 | 66.7 分·抽取综合分 | $0.021 / $0.059 |
| [中医治则治法单选](scenarios/tcm/tcm_best_principles/README.md) | 单选问答 | 5 | 100.0% 正确率 | 40.0% 正确率 | $0.023 / $0.047 |
| [中医治则治法多选](scenarios/tcm/tcm_best_principles_multi/README.md) | 多选问答 | 97 | 70.3 分·抽取综合分 | 62.3 分·抽取综合分 | $0.035 / $0.107 |
| [中医证型单选](scenarios/tcm/tcm_best_syndrome/README.md) | 单选问答 | 68 | 80.9% 正确率 | 72.1% 正确率 | $0.027 / $0.051 |
| [中医证型多选](scenarios/tcm/tcm_best_syndrome_multi/README.md) | 多选问答 | 32 | 52.8 分·抽取综合分 | 36.7 分·抽取综合分 | $0.036 / $0.110 |
| [中医安全问题标签一致性](scenarios/tcm/tcm_best_安全问题/README.md) | 安全标签分类 | 100 | 27.0% 正确率 | 29.0% 正确率 | $0.019 / $0.034 |

[原始实验统计](docs/完整任务统计.md) · [对比实验详情](comparisons/deepseek-flash/README.md)
