# Jev 在医疗领域表现怎么样？

Jev Healthcare Lab · 医疗任务实测与原始记录

**从病历整理到临床判断，实测 Jev 能做对多少、花多少、等多久。**

这个仓库专门评测 Jev 在医疗文本任务中的表现：哪些任务得分高，哪些错误值得注意，调用速度和费用如何。DeepSeek 与 Qwen3.5-9B 作为同题参照；每项测试都保留材料、模型回答和评分记录，可以一路查到原题。

**8 个业务领域 · 96 个评测条件 · 7,133 条测试输入**

**[看 Jev 的全部测试数据 →](#全部领域与任务的详细测试数据)　[按领域查看 →](#领域导航)　[查看原题与回答 →](scenarios/README.md)**

## Jev 的表现：章节分类 99%，量表评分 25%

Jev 给已分段的病历归类时答对 99/100；从给定选项中选出临床量表分数时，答对 25/100。这轮测试中，Jev 在部分分类任务上得分较高，入组预筛和数值评分仍有明显短板。

耗时为历史成功请求的中位响应时间（秒）；三家主评测并非同期测速。

| 医疗任务 | Jev 准确率 | Jev 耗时（秒） | DeepSeek 准确率 | DeepSeek 耗时（秒） | Qwen 准确率 | Qwen 耗时（秒） | 实际测的是什么 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [把病历内容归入对应章节](scenarios/documentation/aci_note_section/README.md) | 99.0% | 0.62 | **100.0%** | **0.55** | **100.0%** | 0.66 | 已给定章节边界 |
| [读长病历，回答指定问题](scenarios/records/longhealth_full_context/README.md) | **95.0%** | 1.43 | 83.0% | **0.62** | 71.0% | 6.67 | 20 个虚构患者的 100 道选择题 |
| [判断患者是否适配临床试验](scenarios/trials/trialgpt_sigir_referral/README.md) | 48.0% | 0.65 | **54.7%** | **0.50** | 52.7% | 0.69 | 给定患者与试验材料，直接三分类 |
| [给临床量表选出数值评分](scenarios/calculators/medcalc_verified_bounded_score/README.md) | 25.0% | 0.66 | **31.0%** | **0.60** | 22.0% | 0.74 | 5 种量表，答案来自给定选项 |

这些是全部 96 项中的四个例子。长病历问答虽然答对 95/100 道题，但只有 16/20 个来源病例的题目全部答对。判断 Jev 是否适合你的业务，还要看它错在哪里、会漏掉什么，以及需要多少人工复核。[完整成绩](#全部领域与任务的详细测试数据) · [错误、区间与复核量](docs/医疗适用性审计.md)

## Jev 的速度和费用怎么样

Jev 在主效果评测中的调用费用更低；在独立重复输入测速中，DeepSeek 的费用更低：

- **主效果评测**：每千条输入，Jev **$0.054**，DeepSeek **$0.123**。
- **独立重复输入测速**：每千条输入，Jev **$0.055**，DeepSeek **$0.048**。

以上为美元估算，按归档费率和可核验用量计算。重复输入可能提高缓存命中；两组分别为 7,133 条和 7,032 条输入，费用也不含 OCR、语音转写、系统接入和人工复核。[费用、耗时与调用条件](comparisons/batch-time/README.md)

**速度方面**：独立测速以相同的 8 并发处理 7,032 条输入，Jev 用时 **22.1 分钟**，DeepSeek 用时 **18.2 分钟**，包含重试与失败等待。

如果你的产品需要对一份材料连续做多个判断，还可以看 [140 份新材料的逐项／合并处理实验](comparisons/paired-suite/README.md)：每次处理 1 项、5 项、10 项，对比准确率、总耗时和费用。

**Qwen3.5-9B 补充对照**：通过硅基流动中国站完成同样的 7,133 条主评测输入，关闭思考模式。每千条输入约 **¥2.044**（人民币公开费率估算，含重试用量）；人民币与美元费用分别展示。[完整运行记录与计费口径](comparisons/qwen3.5-9b/README.md)

## 领域导航

| 业务领域 | Jev 的测试内容 | 任务数 | 记录数 |
| --- | --- | ---: | ---: |
| [患者服务 →](#results-service) | 给患者提问分类、推荐科室、按规则分流 | 5 | 340 |
| [病历与文书 →](#results-records) | 整理病历、识别肯否定、统一术语、查找错误 | 31 | 2,099 |
| [检验与报告 →](#results-reports) | 把检验数值对上项目、读懂报告里的肯否定 | 3 | 60 |
| [用药管理 →](#results-medication) | 识别药物关系、用药变更、剂量与频次 | 8 | 530 |
| [诊疗支持 →](#results-clinical) | 比较诊断、检查、治疗、量表及中医相关题目 | 26 | 1,982 |
| [出院与随访 →](#results-followup) | 识别复诊、复查等后续行动 | 1 | 20 |
| [科研与循证 →](#results-research) | 筛选研究证据、整理 PICO、做患者入组预筛 | 13 | 1,225 |
| [数据治理与运营 →](#results-governance) | 核对编码依据、识别隐私候选和有害请求 | 9 | 877 |

任务目录同时标明已有实测、独立训练扩展和未测部分；训练扩展不计入 Jev 主评测成绩。中医、OCR 和 ASR 等条件也有单独标记。[查看任务与实验的对应关系](docs/医疗任务映射.md)

## 全部领域与任务的详细测试数据

以下按 8 个业务领域展开全部 **96 个主评测条件**。每行并排比较 Jev、DeepSeek 和 Qwen3.5-9B 的准确率或 F1 与中位响应时间；展开领域下方的详细数据，可查看区间、费用、失败数和原始回答。

- **指标**：Accuracy 为准确率；micro-F1 为集合抽取指标，以下均按 0–100 展示，不能混算总体准确率。差值为 Jev 减 DeepSeek，单位为百分点或 F1 分。
- **样本量与区间**：记录数／来源案例数分别列示；来源可能是病例、文档或题目，不等于独立患者。区间按来源案例配对重采样，未校正多重比较。不同任务可能复用来源，案例数不跨任务相加。
- **时间与费用**：中位响应时间只统计成功 API 请求，是历史调用的单次耗时，不是同期测速或整批总时间。每千条费用以全部计分输入为分母；Jev／DeepSeek 为美元，Qwen 为人民币，按归档费率估算，未做汇率换算。
- **失败与原始材料**：未作答包括最终调用或格式失败，仍保留在评分分母；43 条无实体候选记录由规则输出空集，不计为调用失败。“题目”含输入与金标，“Jev／DeepSeek／Qwen”链接三家的原始回答。

<a id="results-service"></a>

### 患者服务

**5 项任务 · 340 条测试记录** · [任务定义与覆盖边界](docs/医疗任务总目录.md#service)

| 任务 | 记录／来源案例 | 指标 | Jev 得分 | Jev 耗时（秒） | DeepSeek 得分 | DeepSeek 耗时（秒） | Qwen 得分 | Qwen 耗时（秒） |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [中文问诊对话行为分类](scenarios/service/imcs_dialogue_act/README.md) | 100／[95](scenarios/service/imcs_dialogue_act/cases.md) | 准确率（%） | **70.0** | 0.90 | 68.0 | **0.54** | 57.0 | 0.68 |
| [患者问题信息需求分类](scenarios/service/medquad_question_type/README.md) | 100／[98](scenarios/service/medquad_question_type/cases.md) | 准确率（%） | 96.0 | 0.63 | **97.0** | **0.53** | 88.0 | 0.68 |
| [边界挑战：服务路由](scenarios/service/challenge_service_route/README.md) | 20／[20](scenarios/service/challenge_service_route/cases.md) | 准确率（%） | 95.0 | 0.59 | **100.0** | **0.51** | **100.0** | 0.66 |
| [主诉推荐就诊科室](scenarios/service/medjourney_departments/README.md) | 100／[100](scenarios/service/medjourney_departments/cases.md) | micro-F1（分） | **36.9** | **1.39** | 34.9 | 1.60 | 17.1 | 12.75 |
| [边界挑战：给定规则紧急程度](scenarios/service/challenge_urgency_given_policy/README.md) | 20／[20](scenarios/service/challenge_urgency_given_policy/cases.md) | 准确率（%） | 100.0 | 0.59 | 100.0 | **0.57** | 100.0 | 0.70 |

<details>
<summary>展开详细数据：得分差值、费用、失败与原始材料</summary>

差值为 Jev 减 DeepSeek；美元费用顺序为 **Jev／DeepSeek**，未作答数顺序为 **Jev／DeepSeek／Qwen**。Qwen 人民币费用另列。

| 任务 | 得分差值［95% 区间］ | Jev 案例全对 | 每千条费用（美元） | Qwen 每千条（人民币） | 最终未作答（条） | 原始数据 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [中文问诊对话行为分类](scenarios/service/imcs_dialogue_act/README.md) | +2.0 ［-4.1, 8.2］ | 65/95 | $0.033／$0.042 | ¥0.849 | 0／0／0 | [题目](scenarios/service/imcs_dialogue_act/samples.jsonl) · [提示词](scenarios/service/imcs_dialogue_act/prompts.json) · [Jev](scenarios/service/imcs_dialogue_act/responses.jsonl) · [DeepSeek](scenarios/service/imcs_dialogue_act/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/service/imcs_dialogue_act/comparison/qwen_responses.jsonl) |
| [患者问题信息需求分类](scenarios/service/medquad_question_type/README.md) | -1.0 ［-3.1, 0.0］ | 94/98 | $0.020／$0.034 | ¥0.581 | 0／0／0 | [题目](scenarios/service/medquad_question_type/samples.jsonl) · [提示词](scenarios/service/medquad_question_type/prompts.json) · [Jev](scenarios/service/medquad_question_type/responses.jsonl) · [DeepSeek](scenarios/service/medquad_question_type/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/service/medquad_question_type/comparison/qwen_responses.jsonl) |
| [边界挑战：服务路由](scenarios/service/challenge_service_route/README.md) | -5.0 ［-15.0, 0.0］ | 19/20 | $0.016／$0.042 | ¥0.438 | 0／0／0 | [题目](scenarios/service/challenge_service_route/samples.jsonl) · [提示词](scenarios/service/challenge_service_route/prompts.json) · [Jev](scenarios/service/challenge_service_route/responses.jsonl) · [DeepSeek](scenarios/service/challenge_service_route/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/service/challenge_service_route/comparison/qwen_responses.jsonl) |
| [主诉推荐就诊科室](scenarios/service/medjourney_departments/README.md) | +2.0 ［-0.6, 4.5］ | 2/100 | $0.360／$0.373 | ¥17.933 | 0／1／0 | [题目](scenarios/service/medjourney_departments/samples.jsonl) · [提示词](scenarios/service/medjourney_departments/prompts.json) · [Jev](scenarios/service/medjourney_departments/responses.jsonl) · [DeepSeek](scenarios/service/medjourney_departments/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/service/medjourney_departments/comparison/qwen_responses.jsonl) |
| [边界挑战：给定规则紧急程度](scenarios/service/challenge_urgency_given_policy/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.018／$0.031 | ¥0.483 | 0／0／0 | [题目](scenarios/service/challenge_urgency_given_policy/samples.jsonl) · [提示词](scenarios/service/challenge_urgency_given_policy/prompts.json) · [Jev](scenarios/service/challenge_urgency_given_policy/responses.jsonl) · [DeepSeek](scenarios/service/challenge_urgency_given_policy/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/service/challenge_urgency_given_policy/comparison/qwen_responses.jsonl) |

</details>

[返回领域导航](#领域导航)

<a id="results-records"></a>

### 病历与文书

**31 项任务 · 2,099 条测试记录** · [任务定义与覆盖边界](docs/医疗任务总目录.md#records)

| 任务 | 记录／来源案例 | 指标 | Jev 得分 | Jev 耗时（秒） | DeepSeek 得分 | DeepSeek 耗时（秒） | Qwen 得分 | Qwen 耗时（秒） |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [中文给定实体类型识别](scenarios/records/imcs_entity_type_oracle_span/README.md) | 100／[95](scenarios/records/imcs_entity_type_oracle_span/cases.md) | 准确率（%） | **96.0** | 0.87 | 92.0 | **0.48** | 85.0 | 0.85 |
| [中文词典候选实体抽取](scenarios/records/imcs_ner_dictionary_pipeline/README.md) | 100／[92](scenarios/records/imcs_ner_dictionary_pipeline/cases.md) | micro-F1（分） | 59.5 | 0.90 | 59.2 | **0.53** | **61.4** | 1.23 |
| [给定疾病实体类别](scenarios/records/ncbi_disease_category_oracle_span/README.md) | 100／[60](scenarios/records/ncbi_disease_category_oracle_span/cases.md) | 准确率（%） | 58.0 | 0.62 | **61.0** | **0.56** | 55.0 | 0.82 |
| [medspaCy 候选与 Jev 疾病实体筛选](scenarios/records/ncbi_medspacy_jev_ner/README.md) | 100／[100](scenarios/records/ncbi_medspacy_jev_ner/cases.md) | micro-F1（分） | **69.4** | **0.66** | 68.7 | 0.71 | 66.9 | 3.17 |
| [医学实体 UMLS 语义类型](scenarios/records/medmentions_type_oracle_span/README.md) | 100／[94](scenarios/records/medmentions_type_oracle_span/cases.md) | 准确率（%） | **60.0** | 0.64 | 51.0 | **0.54** | 41.0 | 0.78 |
| [中文症状肯否定状态](scenarios/records/imcs_assertion_oracle_span/README.md) | 100／[91](scenarios/records/imcs_assertion_oracle_span/cases.md) | 准确率（%） | **79.0** | 0.98 | 73.0 | **0.54** | 64.0 | 0.95 |
| [英文句子否定与不确定线索](scenarios/records/bioscope_sentence_cues/README.md) | 100／[94](scenarios/records/bioscope_sentence_cues/cases.md) | 准确率（%） | **83.0** | 0.63 | 77.0 | **0.50** | 62.0 | 0.89 |
| [西班牙文否定与不确定性](scenarios/records/nubes_scope_status/README.md) | 100／[79](scenarios/records/nubes_scope_status/cases.md) | 准确率（%） | 72.0 | 0.62 | **77.0** | **0.56** | 57.0 | 0.63 |
| [边界挑战：症状所属人](scenarios/records/challenge_experiencer/README.md) | 20／[20](scenarios/records/challenge_experiencer/cases.md) | 准确率（%） | **100.0** | **0.61** | **100.0** | 0.72 | 75.0 | 0.83 |
| [边界挑战：否定状态](scenarios/records/challenge_negation/README.md) | 20／[20](scenarios/records/challenge_negation/cases.md) | 准确率（%） | 100.0 | **0.59** | 100.0 | 0.65 | 100.0 | 0.77 |
| [边界挑战：社会背景](scenarios/records/challenge_social_context/README.md) | 20／[20](scenarios/records/challenge_social_context/cases.md) | 准确率（%） | 100.0 | 0.62 | 100.0 | **0.61** | 100.0 | 0.70 |
| [边界挑战：中英混合文本](scenarios/records/challenge_mixed_language/README.md) | 20／[20](scenarios/records/challenge_mixed_language/cases.md) | 准确率（%） | 100.0 | 0.61 | 100.0 | **0.55** | 100.0 | 0.79 |
| [边界挑战：相对日期](scenarios/records/challenge_relative_date/README.md) | 20／[20](scenarios/records/challenge_relative_date/cases.md) | 准确率（%） | **100.0** | 0.61 | **100.0** | **0.57** | 90.0 | 0.92 |
| [边界挑战：事件时态](scenarios/records/challenge_temporality/README.md) | 20／[20](scenarios/records/challenge_temporality/cases.md) | 准确率（%） | **100.0** | **0.61** | 75.0 | 0.73 | 85.0 | 0.78 |
| [中文症状术语归一化](scenarios/records/imcs_normalization_top20/README.md) | 100／[92](scenarios/records/imcs_normalization_top20/cases.md) | 准确率（%） | **93.0** | 0.90 | 92.0 | **0.52** | 90.0 | 0.86 |
| [医学缩写消歧](scenarios/records/medal_demo_disambiguation/README.md) | 100／[34](scenarios/records/medal_demo_disambiguation/cases.md) | 准确率（%） | **67.0** | 0.67 | 35.0 | **0.58** | 5.0 | 1.05 |
| [问诊对话对应病历章节](scenarios/documentation/mts_section_classification/README.md) | 100／[100](scenarios/documentation/mts_section_classification/cases.md) | 准确率（%） | **76.0** | 0.92 | 73.0 | **0.57** | 68.0 | 0.70 |
| [已分段病历章节分类](scenarios/documentation/aci_note_section/README.md) | 100／[40](scenarios/documentation/aci_note_section/cases.md) | 准确率（%） | 99.0 | 0.62 | **100.0** | **0.55** | **100.0** | 0.66 |
| [边界挑战：文档类型](scenarios/documentation/challenge_document_type/README.md) | 20／[20](scenarios/documentation/challenge_document_type/cases.md) | 准确率（%） | 100.0 | 0.59 | 100.0 | **0.58** | 100.0 | 0.62 |
| [OCR 文本医疗文档类型识别](scenarios/multimodal/clinocr_ocr_doctype/README.md) | 24／[20](scenarios/multimodal/clinocr_ocr_doctype/cases.md) | 准确率（%） | **95.8** | 0.63 | 87.5 | **0.53** | 75.0 | 0.80 |
| [参考文本医疗文档类型识别](scenarios/multimodal/clinocr_reference_doctype/README.md) | 24／[20](scenarios/multimodal/clinocr_reference_doctype/cases.md) | 准确率（%） | **95.8** | 0.61 | **95.8** | **0.53** | 79.2 | 0.78 |
| [ASR 转写病史字段判断](scenarios/multimodal/primock_asr_fields/README.md) | 37／[20](scenarios/multimodal/primock_asr_fields/cases.md) | 准确率（%） | **91.9** | 0.62 | 89.2 | **0.60** | 89.2 | 0.74 |
| [参考转写病史字段判断](scenarios/multimodal/primock_reference_fields/README.md) | 37／[20](scenarios/multimodal/primock_reference_fields/cases.md) | 准确率（%） | 100.0 | 0.66 | 100.0 | **0.57** | 100.0 | 0.83 |
| [长病历跨文档问答](scenarios/records/longhealth_full_context/README.md) | 100／[20](scenarios/records/longhealth_full_context/cases.md) | 准确率（%） | **95.0** | 1.43 | 83.0 | **0.62** | 71.0 | 6.67 |
| [边界挑战：文书缺项](scenarios/documentation/challenge_documentation/README.md) | 20／[20](scenarios/documentation/challenge_documentation/cases.md) | 准确率（%） | 100.0 | 0.60 | 100.0 | **0.57** | 100.0 | 0.62 |
| [边界挑战：病历矛盾](scenarios/quality/challenge_contradiction/README.md) | 20／[20](scenarios/quality/challenge_contradiction/cases.md) | 准确率（%） | **100.0** | 0.58 | 95.0 | **0.57** | 70.0 | 0.73 |
| [医疗叙述错误检出](scenarios/quality/medec_error_detection/README.md) | 100／[100](scenarios/quality/medec_error_detection/cases.md) | 准确率（%） | **65.0** | 0.94 | 60.0 | **0.54** | 57.0 | 0.77 |
| [医疗叙述错误定位](scenarios/quality/medec_error_localization/README.md) | 100／[100](scenarios/quality/medec_error_localization/cases.md) | 准确率（%） | **72.0** | 0.95 | 70.0 | **0.54** | 57.0 | 0.77 |
| [阿拉伯文医疗文本错误检出](scenarios/quality/mederrbench_ARA/README.md) | 97／[97](scenarios/quality/mederrbench_ARA/cases.md) | 准确率（%） | **69.1** | 0.62 | 59.8 | **0.53** | 57.7 | 0.77 |
| [中文医疗文本错误检出](scenarios/quality/mederrbench_CN/README.md) | 100／[100](scenarios/quality/mederrbench_CN/cases.md) | 准确率（%） | 73.0 | 0.61 | **74.0** | **0.56** | 58.0 | 0.84 |
| [英文医疗文本错误检出](scenarios/quality/mederrbench_EN/README.md) | 100／[100](scenarios/quality/mederrbench_EN/cases.md) | 准确率（%） | **81.0** | 0.63 | 79.0 | **0.58** | 53.0 | 0.85 |

<details>
<summary>展开详细数据：得分差值、费用、失败与原始材料</summary>

差值为 Jev 减 DeepSeek；美元费用顺序为 **Jev／DeepSeek**，未作答数顺序为 **Jev／DeepSeek／Qwen**。Qwen 人民币费用另列。

| 任务 | 得分差值［95% 区间］ | Jev 案例全对 | 每千条费用（美元） | Qwen 每千条（人民币） | 最终未作答（条） | 原始数据 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [中文给定实体类型识别](scenarios/records/imcs_entity_type_oracle_span/README.md) | +4.0 ［-1.0, 10.1］ | 91/95 | $0.019／$0.031 | ¥0.519 | 0／0／0 | [题目](scenarios/records/imcs_entity_type_oracle_span/samples.jsonl) · [提示词](scenarios/records/imcs_entity_type_oracle_span/prompts.json) · [Jev](scenarios/records/imcs_entity_type_oracle_span/responses.jsonl) · [DeepSeek](scenarios/records/imcs_entity_type_oracle_span/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/imcs_entity_type_oracle_span/comparison/qwen_responses.jsonl) |
| [中文词典候选实体抽取](scenarios/records/imcs_ner_dictionary_pipeline/README.md) | +0.3 ［-15.4, 18.9］ | 57/92 | $0.021／$0.045 | ¥0.631 | 0／1／0 | [题目](scenarios/records/imcs_ner_dictionary_pipeline/samples.jsonl) · [提示词](scenarios/records/imcs_ner_dictionary_pipeline/prompts.json) · [Jev](scenarios/records/imcs_ner_dictionary_pipeline/responses.jsonl) · [DeepSeek](scenarios/records/imcs_ner_dictionary_pipeline/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/imcs_ner_dictionary_pipeline/comparison/qwen_responses.jsonl) |
| [给定疾病实体类别](scenarios/records/ncbi_disease_category_oracle_span/README.md) | -3.0 ［-8.4, 2.1］ | 28/60 | $0.030／$0.058 | ¥0.972 | 0／0／0 | [题目](scenarios/records/ncbi_disease_category_oracle_span/samples.jsonl) · [提示词](scenarios/records/ncbi_disease_category_oracle_span/prompts.json) · [Jev](scenarios/records/ncbi_disease_category_oracle_span/responses.jsonl) · [DeepSeek](scenarios/records/ncbi_disease_category_oracle_span/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/ncbi_disease_category_oracle_span/comparison/qwen_responses.jsonl) |
| [medspaCy 候选与 Jev 疾病实体筛选](scenarios/records/ncbi_medspacy_jev_ner/README.md) | +0.7 ［-0.9, 2.4］ | 20/100 | $0.049／$0.191 | ¥3.255 | 0／0／0 | [题目](scenarios/records/ncbi_medspacy_jev_ner/samples.jsonl) · [提示词](scenarios/records/ncbi_medspacy_jev_ner/prompts.json) · [Jev](scenarios/records/ncbi_medspacy_jev_ner/responses.jsonl) · [DeepSeek](scenarios/records/ncbi_medspacy_jev_ner/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/ncbi_medspacy_jev_ner/comparison/qwen_responses.jsonl) |
| [医学实体 UMLS 语义类型](scenarios/records/medmentions_type_oracle_span/README.md) | +9.0 ［1.0, 17.8］ | 55/94 | $0.044／$0.096 | ¥1.364 | 0／5／1 | [题目](scenarios/records/medmentions_type_oracle_span/samples.jsonl) · [提示词](scenarios/records/medmentions_type_oracle_span/prompts.json) · [Jev](scenarios/records/medmentions_type_oracle_span/responses.jsonl) · [DeepSeek](scenarios/records/medmentions_type_oracle_span/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/medmentions_type_oracle_span/comparison/qwen_responses.jsonl) |
| [中文症状肯否定状态](scenarios/records/imcs_assertion_oracle_span/README.md) | +6.0 ［0.0, 12.5］ | 70/91 | $0.096／$0.209 | ¥2.313 | 0／0／0 | [题目](scenarios/records/imcs_assertion_oracle_span/samples.jsonl) · [提示词](scenarios/records/imcs_assertion_oracle_span/prompts.json) · [Jev](scenarios/records/imcs_assertion_oracle_span/responses.jsonl) · [DeepSeek](scenarios/records/imcs_assertion_oracle_span/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/imcs_assertion_oracle_span/comparison/qwen_responses.jsonl) |
| [英文句子否定与不确定线索](scenarios/records/bioscope_sentence_cues/README.md) | +6.0 ［-2.1, 14.4］ | 77/94 | $0.018／$0.032 | ¥0.548 | 0／0／0 | [题目](scenarios/records/bioscope_sentence_cues/samples.jsonl) · [提示词](scenarios/records/bioscope_sentence_cues/prompts.json) · [Jev](scenarios/records/bioscope_sentence_cues/responses.jsonl) · [DeepSeek](scenarios/records/bioscope_sentence_cues/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/bioscope_sentence_cues/comparison/qwen_responses.jsonl) |
| [西班牙文否定与不确定性](scenarios/records/nubes_scope_status/README.md) | -5.0 ［-11.2, 1.1］ | 57/79 | $0.019／$0.039 | ¥0.591 | 0／0／0 | [题目](scenarios/records/nubes_scope_status/samples.jsonl) · [提示词](scenarios/records/nubes_scope_status/prompts.json) · [Jev](scenarios/records/nubes_scope_status/responses.jsonl) · [DeepSeek](scenarios/records/nubes_scope_status/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/nubes_scope_status/comparison/qwen_responses.jsonl) |
| [边界挑战：症状所属人](scenarios/records/challenge_experiencer/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.016／$0.041 | ¥0.440 | 0／0／0 | [题目](scenarios/records/challenge_experiencer/samples.jsonl) · [提示词](scenarios/records/challenge_experiencer/prompts.json) · [Jev](scenarios/records/challenge_experiencer/responses.jsonl) · [DeepSeek](scenarios/records/challenge_experiencer/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/challenge_experiencer/comparison/qwen_responses.jsonl) |
| [边界挑战：否定状态](scenarios/records/challenge_negation/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.015／$0.041 | ¥0.438 | 0／0／0 | [题目](scenarios/records/challenge_negation/samples.jsonl) · [提示词](scenarios/records/challenge_negation/prompts.json) · [Jev](scenarios/records/challenge_negation/responses.jsonl) · [DeepSeek](scenarios/records/challenge_negation/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/challenge_negation/comparison/qwen_responses.jsonl) |
| [边界挑战：社会背景](scenarios/records/challenge_social_context/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.016／$0.041 | ¥0.440 | 0／0／0 | [题目](scenarios/records/challenge_social_context/samples.jsonl) · [提示词](scenarios/records/challenge_social_context/prompts.json) · [Jev](scenarios/records/challenge_social_context/responses.jsonl) · [DeepSeek](scenarios/records/challenge_social_context/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/challenge_social_context/comparison/qwen_responses.jsonl) |
| [边界挑战：中英混合文本](scenarios/records/challenge_mixed_language/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.015／$0.039 | ¥0.430 | 0／0／0 | [题目](scenarios/records/challenge_mixed_language/samples.jsonl) · [提示词](scenarios/records/challenge_mixed_language/prompts.json) · [Jev](scenarios/records/challenge_mixed_language/responses.jsonl) · [DeepSeek](scenarios/records/challenge_mixed_language/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/challenge_mixed_language/comparison/qwen_responses.jsonl) |
| [边界挑战：相对日期](scenarios/records/challenge_relative_date/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.018／$0.030 | ¥0.610 | 0／0／0 | [题目](scenarios/records/challenge_relative_date/samples.jsonl) · [提示词](scenarios/records/challenge_relative_date/prompts.json) · [Jev](scenarios/records/challenge_relative_date/responses.jsonl) · [DeepSeek](scenarios/records/challenge_relative_date/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/challenge_relative_date/comparison/qwen_responses.jsonl) |
| [边界挑战：事件时态](scenarios/records/challenge_temporality/README.md) | +25.0 ［10.0, 45.0］ | 20/20 | $0.016／$0.042 | ¥0.450 | 0／0／0 | [题目](scenarios/records/challenge_temporality/samples.jsonl) · [提示词](scenarios/records/challenge_temporality/prompts.json) · [Jev](scenarios/records/challenge_temporality/responses.jsonl) · [DeepSeek](scenarios/records/challenge_temporality/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/challenge_temporality/comparison/qwen_responses.jsonl) |
| [中文症状术语归一化](scenarios/records/imcs_normalization_top20/README.md) | +1.0 ［-4.1, 6.1］ | 85/92 | $0.037／$0.049 | ¥0.864 | 0／0／0 | [题目](scenarios/records/imcs_normalization_top20/samples.jsonl) · [提示词](scenarios/records/imcs_normalization_top20/prompts.json) · [Jev](scenarios/records/imcs_normalization_top20/responses.jsonl) · [DeepSeek](scenarios/records/imcs_normalization_top20/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/imcs_normalization_top20/comparison/qwen_responses.jsonl) |
| [医学缩写消歧](scenarios/records/medal_demo_disambiguation/README.md) | +32.0 ［21.4, 44.3］ | 13/34 | $0.116／$0.082 | ¥5.661 | 0／17／52 | [题目](scenarios/records/medal_demo_disambiguation/samples.jsonl) · [提示词](scenarios/records/medal_demo_disambiguation/prompts.json) · [Jev](scenarios/records/medal_demo_disambiguation/responses.jsonl) · [DeepSeek](scenarios/records/medal_demo_disambiguation/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/medal_demo_disambiguation/comparison/qwen_responses.jsonl) |
| [问诊对话对应病历章节](scenarios/documentation/mts_section_classification/README.md) | +3.0 ［-4.0, 10.0］ | 76/100 | $0.031／$0.044 | ¥0.899 | 0／0／0 | [题目](scenarios/documentation/mts_section_classification/samples.jsonl) · [提示词](scenarios/documentation/mts_section_classification/prompts.json) · [Jev](scenarios/documentation/mts_section_classification/responses.jsonl) · [DeepSeek](scenarios/documentation/mts_section_classification/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/documentation/mts_section_classification/comparison/qwen_responses.jsonl) |
| [已分段病历章节分类](scenarios/documentation/aci_note_section/README.md) | -1.0 ［-3.2, 0.0］ | 39/40 | $0.021／$0.048 | ¥0.684 | 0／0／0 | [题目](scenarios/documentation/aci_note_section/samples.jsonl) · [提示词](scenarios/documentation/aci_note_section/prompts.json) · [Jev](scenarios/documentation/aci_note_section/responses.jsonl) · [DeepSeek](scenarios/documentation/aci_note_section/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/documentation/aci_note_section/comparison/qwen_responses.jsonl) |
| [边界挑战：文档类型](scenarios/documentation/challenge_document_type/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.016／$0.042 | ¥0.448 | 0／0／0 | [题目](scenarios/documentation/challenge_document_type/samples.jsonl) · [提示词](scenarios/documentation/challenge_document_type/prompts.json) · [Jev](scenarios/documentation/challenge_document_type/responses.jsonl) · [DeepSeek](scenarios/documentation/challenge_document_type/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/documentation/challenge_document_type/comparison/qwen_responses.jsonl) |
| [OCR 文本医疗文档类型识别](scenarios/multimodal/clinocr_ocr_doctype/README.md) | +8.3 ［0.0, 20.8］ | 19/20 | $0.037／$0.090 | ¥1.210 | 0／0／0 | [题目](scenarios/multimodal/clinocr_ocr_doctype/samples.jsonl) · [提示词](scenarios/multimodal/clinocr_ocr_doctype/prompts.json) · [Jev](scenarios/multimodal/clinocr_ocr_doctype/responses.jsonl) · [DeepSeek](scenarios/multimodal/clinocr_ocr_doctype/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/multimodal/clinocr_ocr_doctype/comparison/qwen_responses.jsonl) |
| [参考文本医疗文档类型识别](scenarios/multimodal/clinocr_reference_doctype/README.md) | +0.0 ［0.0, 0.0］ | 19/20 | $0.038／$0.081 | ¥1.217 | 0／0／0 | [题目](scenarios/multimodal/clinocr_reference_doctype/samples.jsonl) · [提示词](scenarios/multimodal/clinocr_reference_doctype/prompts.json) · [Jev](scenarios/multimodal/clinocr_reference_doctype/responses.jsonl) · [DeepSeek](scenarios/multimodal/clinocr_reference_doctype/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/multimodal/clinocr_reference_doctype/comparison/qwen_responses.jsonl) |
| [ASR 转写病史字段判断](scenarios/multimodal/primock_asr_fields/README.md) | +2.7 ［0.0, 11.5］ | 17/20 | $0.024／$0.060 | ¥0.774 | 0／0／0 | [题目](scenarios/multimodal/primock_asr_fields/samples.jsonl) · [提示词](scenarios/multimodal/primock_asr_fields/prompts.json) · [Jev](scenarios/multimodal/primock_asr_fields/responses.jsonl) · [DeepSeek](scenarios/multimodal/primock_asr_fields/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/multimodal/primock_asr_fields/comparison/qwen_responses.jsonl) |
| [参考转写病史字段判断](scenarios/multimodal/primock_reference_fields/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.027／$0.071 | ¥0.882 | 0／0／0 | [题目](scenarios/multimodal/primock_reference_fields/samples.jsonl) · [提示词](scenarios/multimodal/primock_reference_fields/prompts.json) · [Jev](scenarios/multimodal/primock_reference_fields/responses.jsonl) · [DeepSeek](scenarios/multimodal/primock_reference_fields/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/multimodal/primock_reference_fields/comparison/qwen_responses.jsonl) |
| [长病历跨文档问答](scenarios/records/longhealth_full_context/README.md) | +12.0 ［8.0, 16.0］ | 16/20 | $0.537／$1.697 | ¥20.887 | 0／1／7 | [题目](scenarios/records/longhealth_full_context/samples.jsonl) · [提示词](scenarios/records/longhealth_full_context/prompts.json) · [Jev](scenarios/records/longhealth_full_context/responses.jsonl) · [DeepSeek](scenarios/records/longhealth_full_context/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/longhealth_full_context/comparison/qwen_responses.jsonl) |
| [边界挑战：文书缺项](scenarios/documentation/challenge_documentation/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.016／$0.042 | ¥0.455 | 0／0／0 | [题目](scenarios/documentation/challenge_documentation/samples.jsonl) · [提示词](scenarios/documentation/challenge_documentation/prompts.json) · [Jev](scenarios/documentation/challenge_documentation/responses.jsonl) · [DeepSeek](scenarios/documentation/challenge_documentation/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/documentation/challenge_documentation/comparison/qwen_responses.jsonl) |
| [边界挑战：病历矛盾](scenarios/quality/challenge_contradiction/README.md) | +5.0 ［0.0, 15.0］ | 20/20 | $0.016／$0.042 | ¥0.446 | 0／0／0 | [题目](scenarios/quality/challenge_contradiction/samples.jsonl) · [提示词](scenarios/quality/challenge_contradiction/prompts.json) · [Jev](scenarios/quality/challenge_contradiction/responses.jsonl) · [DeepSeek](scenarios/quality/challenge_contradiction/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/quality/challenge_contradiction/comparison/qwen_responses.jsonl) |
| [医疗叙述错误检出](scenarios/quality/medec_error_detection/README.md) | +5.0 ［-4.0, 14.0］ | 65/100 | $0.031／$0.077 | ¥1.031 | 0／0／0 | [题目](scenarios/quality/medec_error_detection/samples.jsonl) · [提示词](scenarios/quality/medec_error_detection/prompts.json) · [Jev](scenarios/quality/medec_error_detection/responses.jsonl) · [DeepSeek](scenarios/quality/medec_error_detection/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/quality/medec_error_detection/comparison/qwen_responses.jsonl) |
| [医疗叙述错误定位](scenarios/quality/medec_error_localization/README.md) | +2.0 ［-6.0, 10.0］ | 72/100 | $0.039／$0.089 | ¥1.206 | 0／0／0 | [题目](scenarios/quality/medec_error_localization/samples.jsonl) · [提示词](scenarios/quality/medec_error_localization/prompts.json) · [Jev](scenarios/quality/medec_error_localization/responses.jsonl) · [DeepSeek](scenarios/quality/medec_error_localization/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/quality/medec_error_localization/comparison/qwen_responses.jsonl) |
| [阿拉伯文医疗文本错误检出](scenarios/quality/mederrbench_ARA/README.md) | +9.3 ［-2.1, 20.6］ | 67/97 | $0.019／$0.035 | ¥0.504 | 0／0／0 | [题目](scenarios/quality/mederrbench_ARA/samples.jsonl) · [提示词](scenarios/quality/mederrbench_ARA/prompts.json) · [Jev](scenarios/quality/mederrbench_ARA/responses.jsonl) · [DeepSeek](scenarios/quality/mederrbench_ARA/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/quality/mederrbench_ARA/comparison/qwen_responses.jsonl) |
| [中文医疗文本错误检出](scenarios/quality/mederrbench_CN/README.md) | -1.0 ［-10.0, 8.0］ | 73/100 | $0.018／$0.033 | ¥0.529 | 0／0／0 | [题目](scenarios/quality/mederrbench_CN/samples.jsonl) · [提示词](scenarios/quality/mederrbench_CN/prompts.json) · [Jev](scenarios/quality/mederrbench_CN/responses.jsonl) · [DeepSeek](scenarios/quality/mederrbench_CN/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/quality/mederrbench_CN/comparison/qwen_responses.jsonl) |
| [英文医疗文本错误检出](scenarios/quality/mederrbench_EN/README.md) | +2.0 ［-7.0, 11.0］ | 81/100 | $0.023／$0.049 | ¥0.744 | 0／0／0 | [题目](scenarios/quality/mederrbench_EN/samples.jsonl) · [提示词](scenarios/quality/mederrbench_EN/prompts.json) · [Jev](scenarios/quality/mederrbench_EN/responses.jsonl) · [DeepSeek](scenarios/quality/mederrbench_EN/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/quality/mederrbench_EN/comparison/qwen_responses.jsonl) |

</details>

[返回领域导航](#领域导航)

<a id="results-reports"></a>

### 检验与报告

**3 项任务 · 60 条测试记录** · [任务定义与覆盖边界](docs/医疗任务总目录.md#reports)

| 任务 | 记录／来源案例 | 指标 | Jev 得分 | Jev 耗时（秒） | DeepSeek 得分 | DeepSeek 耗时（秒） | Qwen 得分 | Qwen 耗时（秒） |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [边界挑战：检验数值关联](scenarios/calculators/challenge_lab_link/README.md) | 20／[20](scenarios/calculators/challenge_lab_link/cases.md) | 准确率（%） | 100.0 | **0.60** | 100.0 | 0.63 | 100.0 | 0.68 |
| [边界挑战：单位等价](scenarios/calculators/challenge_unit_equivalence/README.md) | 20／[20](scenarios/calculators/challenge_unit_equivalence/cases.md) | 准确率（%） | 95.0 | **0.60** | **100.0** | 0.64 | 80.0 | 0.70 |
| [边界挑战：影像报告断言](scenarios/multimodal/challenge_radiology_assertion/README.md) | 20／[20](scenarios/multimodal/challenge_radiology_assertion/cases.md) | 准确率（%） | **100.0** | 0.60 | **100.0** | **0.57** | 95.0 | 0.73 |

<details>
<summary>展开详细数据：得分差值、费用、失败与原始材料</summary>

差值为 Jev 减 DeepSeek；美元费用顺序为 **Jev／DeepSeek**，未作答数顺序为 **Jev／DeepSeek／Qwen**。Qwen 人民币费用另列。

| 任务 | 得分差值［95% 区间］ | Jev 案例全对 | 每千条费用（美元） | Qwen 每千条（人民币） | 最终未作答（条） | 原始数据 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [边界挑战：检验数值关联](scenarios/calculators/challenge_lab_link/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.017／$0.041 | ¥0.503 | 0／0／0 | [题目](scenarios/calculators/challenge_lab_link/samples.jsonl) · [提示词](scenarios/calculators/challenge_lab_link/prompts.json) · [Jev](scenarios/calculators/challenge_lab_link/responses.jsonl) · [DeepSeek](scenarios/calculators/challenge_lab_link/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/calculators/challenge_lab_link/comparison/qwen_responses.jsonl) |
| [边界挑战：单位等价](scenarios/calculators/challenge_unit_equivalence/README.md) | -5.0 ［-15.0, 0.0］ | 19/20 | $0.015／$0.042 | ¥0.458 | 0／0／0 | [题目](scenarios/calculators/challenge_unit_equivalence/samples.jsonl) · [提示词](scenarios/calculators/challenge_unit_equivalence/prompts.json) · [Jev](scenarios/calculators/challenge_unit_equivalence/responses.jsonl) · [DeepSeek](scenarios/calculators/challenge_unit_equivalence/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/calculators/challenge_unit_equivalence/comparison/qwen_responses.jsonl) |
| [边界挑战：影像报告断言](scenarios/multimodal/challenge_radiology_assertion/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.016／$0.043 | ¥0.468 | 0／0／0 | [题目](scenarios/multimodal/challenge_radiology_assertion/samples.jsonl) · [提示词](scenarios/multimodal/challenge_radiology_assertion/prompts.json) · [Jev](scenarios/multimodal/challenge_radiology_assertion/responses.jsonl) · [DeepSeek](scenarios/multimodal/challenge_radiology_assertion/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/multimodal/challenge_radiology_assertion/comparison/qwen_responses.jsonl) |

</details>

[返回领域导航](#领域导航)

<a id="results-medication"></a>

### 用药管理

**8 项任务 · 530 条测试记录** · [任务定义与覆盖边界](docs/医疗任务总目录.md#medication)

| 任务 | 记录／来源案例 | 指标 | Jev 得分 | Jev 耗时（秒） | DeepSeek 得分 | DeepSeek 耗时（秒） | Qwen 得分 | Qwen 耗时（秒） |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [化学物致病关系判断](scenarios/medication/bc5cdr_relation_oracle_entities/README.md) | 100／[82](scenarios/medication/bc5cdr_relation_oracle_entities/cases.md) | 准确率（%） | 57.0 | 0.64 | **66.0** | **0.52** | 56.0 | 0.86 |
| [给定药物对相互作用分类](scenarios/medication/ddi_relation_oracle_pairs/README.md) | 150／[77](scenarios/medication/ddi_relation_oracle_pairs/cases.md) | 准确率（%） | **79.3** | 0.91 | 74.7 | **0.53** | 66.7 | 0.79 |
| [边界挑战：过敏状态](scenarios/medication/challenge_allergy_state/README.md) | 20／[20](scenarios/medication/challenge_allergy_state/cases.md) | 准确率（%） | 100.0 | 0.62 | 100.0 | **0.61** | 100.0 | 0.81 |
| [出院带药候选筛选](scenarios/medication/cdrugred_discharge_candidate_pipeline/README.md) | 100／[83](scenarios/medication/cdrugred_discharge_candidate_pipeline/cases.md) | micro-F1（分） | **48.6** | **0.78** | 47.9 | 0.93 | 35.3 | 6.24 |
| [边界挑战：用药变更](scenarios/medication/challenge_medication_change/README.md) | 20／[20](scenarios/medication/challenge_medication_change/cases.md) | 准确率（%） | 100.0 | **0.59** | 100.0 | 0.62 | 100.0 | 0.74 |
| [边界挑战：药物剂量关联](scenarios/medication/challenge_dose_link/README.md) | 20／[20](scenarios/medication/challenge_dose_link/cases.md) | 准确率（%） | 100.0 | 0.62 | 100.0 | **0.61** | 100.0 | 0.77 |
| [边界挑战：给药频次](scenarios/medication/challenge_frequency/README.md) | 20／[20](scenarios/medication/challenge_frequency/cases.md) | 准确率（%） | 100.0 | **0.60** | 100.0 | 0.64 | 100.0 | 0.79 |
| [MedJourney 用药预测选择题](scenarios/service/medjourney_mp_mcq/README.md) | 100／[100](scenarios/service/medjourney_mp_mcq/cases.md) | 准确率（%） | 86.0 | 0.61 | **88.0** | **0.51** | 80.0 | 0.67 |

<details>
<summary>展开详细数据：得分差值、费用、失败与原始材料</summary>

差值为 Jev 减 DeepSeek；美元费用顺序为 **Jev／DeepSeek**，未作答数顺序为 **Jev／DeepSeek／Qwen**。Qwen 人民币费用另列。

| 任务 | 得分差值［95% 区间］ | Jev 案例全对 | 每千条费用（美元） | Qwen 每千条（人民币） | 最终未作答（条） | 原始数据 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [化学物致病关系判断](scenarios/medication/bc5cdr_relation_oracle_entities/README.md) | -9.0 ［-20.0, 2.1］ | 46/82 | $0.031／$0.069 | ¥1.011 | 0／0／0 | [题目](scenarios/medication/bc5cdr_relation_oracle_entities/samples.jsonl) · [提示词](scenarios/medication/bc5cdr_relation_oracle_entities/prompts.json) · [Jev](scenarios/medication/bc5cdr_relation_oracle_entities/responses.jsonl) · [DeepSeek](scenarios/medication/bc5cdr_relation_oracle_entities/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/medication/bc5cdr_relation_oracle_entities/comparison/qwen_responses.jsonl) |
| [给定药物对相互作用分类](scenarios/medication/ddi_relation_oracle_pairs/README.md) | +4.7 ［1.2, 8.7］ | 59/77 | $0.024／$0.038 | ¥0.700 | 0／0／0 | [题目](scenarios/medication/ddi_relation_oracle_pairs/samples.jsonl) · [提示词](scenarios/medication/ddi_relation_oracle_pairs/prompts.json) · [Jev](scenarios/medication/ddi_relation_oracle_pairs/responses.jsonl) · [DeepSeek](scenarios/medication/ddi_relation_oracle_pairs/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/medication/ddi_relation_oracle_pairs/comparison/qwen_responses.jsonl) |
| [边界挑战：过敏状态](scenarios/medication/challenge_allergy_state/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.016／$0.043 | ¥0.460 | 0／0／0 | [题目](scenarios/medication/challenge_allergy_state/samples.jsonl) · [提示词](scenarios/medication/challenge_allergy_state/prompts.json) · [Jev](scenarios/medication/challenge_allergy_state/responses.jsonl) · [DeepSeek](scenarios/medication/challenge_allergy_state/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/medication/challenge_allergy_state/comparison/qwen_responses.jsonl) |
| [出院带药候选筛选](scenarios/medication/cdrugred_discharge_candidate_pipeline/README.md) | +0.7 ［-2.2, 3.8］ | 3/83 | $0.218／$0.587 | ¥8.147 | 0／0／0 | [题目](scenarios/medication/cdrugred_discharge_candidate_pipeline/samples.jsonl) · [提示词](scenarios/medication/cdrugred_discharge_candidate_pipeline/prompts.json) · [Jev](scenarios/medication/cdrugred_discharge_candidate_pipeline/responses.jsonl) · [DeepSeek](scenarios/medication/cdrugred_discharge_candidate_pipeline/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/medication/cdrugred_discharge_candidate_pipeline/comparison/qwen_responses.jsonl) |
| [边界挑战：用药变更](scenarios/medication/challenge_medication_change/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.016／$0.043 | ¥0.453 | 0／0／0 | [题目](scenarios/medication/challenge_medication_change/samples.jsonl) · [提示词](scenarios/medication/challenge_medication_change/prompts.json) · [Jev](scenarios/medication/challenge_medication_change/responses.jsonl) · [DeepSeek](scenarios/medication/challenge_medication_change/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/medication/challenge_medication_change/comparison/qwen_responses.jsonl) |
| [边界挑战：药物剂量关联](scenarios/medication/challenge_dose_link/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.016／$0.043 | ¥0.505 | 0／0／0 | [题目](scenarios/medication/challenge_dose_link/samples.jsonl) · [提示词](scenarios/medication/challenge_dose_link/prompts.json) · [Jev](scenarios/medication/challenge_dose_link/responses.jsonl) · [DeepSeek](scenarios/medication/challenge_dose_link/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/medication/challenge_dose_link/comparison/qwen_responses.jsonl) |
| [边界挑战：给药频次](scenarios/medication/challenge_frequency/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.016／$0.043 | ¥0.456 | 0／0／0 | [题目](scenarios/medication/challenge_frequency/samples.jsonl) · [提示词](scenarios/medication/challenge_frequency/prompts.json) · [Jev](scenarios/medication/challenge_frequency/responses.jsonl) · [DeepSeek](scenarios/medication/challenge_frequency/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/medication/challenge_frequency/comparison/qwen_responses.jsonl) |
| [MedJourney 用药预测选择题](scenarios/service/medjourney_mp_mcq/README.md) | -2.0 ［-8.0, 3.0］ | 86/100 | $0.020／$0.034 | ¥0.550 | 0／1／0 | [题目](scenarios/service/medjourney_mp_mcq/samples.jsonl) · [提示词](scenarios/service/medjourney_mp_mcq/prompts.json) · [Jev](scenarios/service/medjourney_mp_mcq/responses.jsonl) · [DeepSeek](scenarios/service/medjourney_mp_mcq/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/service/medjourney_mp_mcq/comparison/qwen_responses.jsonl) |

</details>

[返回领域导航](#领域导航)

<a id="results-clinical"></a>

### 诊疗支持

**26 项任务 · 1,982 条测试记录** · [任务定义与覆盖边界](docs/医疗任务总目录.md#clinical)

| 任务 | 记录／来源案例 | 指标 | Jev 得分 | Jev 耗时（秒） | DeepSeek 得分 | DeepSeek 耗时（秒） | Qwen 得分 | Qwen 耗时（秒） |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [MedJourney 诊断预测选择题](scenarios/service/medjourney_dp_mcq/README.md) | 100／[100](scenarios/service/medjourney_dp_mcq/cases.md) | 准确率（%） | **92.0** | 0.63 | 91.0 | **0.53** | 80.0 | 0.68 |
| [合成病例主要诊断](scenarios/acute/ddxplus_synthetic_primary/README.md) | 100／[100](scenarios/acute/ddxplus_synthetic_primary/cases.md) | 准确率（%） | 67.0 | 0.69 | **71.0** | **0.58** | 60.0 | 0.82 |
| [中医病历证型分类](scenarios/tcm/tcm_syndrome/README.md) | 100／[100](scenarios/tcm/tcm_syndrome/cases.md) | 准确率（%） | 33.0 | 1.16 | **40.0** | **0.54** | 36.0 | 0.87 |
| [中医病位单选](scenarios/tcm/tcm_best_location/README.md) | 21／[21](scenarios/tcm/tcm_best_location/cases.md) | 准确率（%） | **81.0** | 0.64 | 76.2 | **0.48** | 52.4 | 0.67 |
| [中医病位多选](scenarios/tcm/tcm_best_location_multi/README.md) | 79／[79](scenarios/tcm/tcm_best_location_multi/cases.md) | micro-F1（分） | 64.8 | **0.62** | **66.7** | **0.62** | 32.4 | 1.39 |
| [中医病性单选](scenarios/tcm/tcm_best_nature/README.md) | 99／[99](scenarios/tcm/tcm_best_nature/cases.md) | 准确率（%） | **69.7** | 0.65 | 59.6 | **0.54** | 53.5 | 0.64 |
| [中医病性与要素多选](scenarios/tcm/tcm_best_nature_multi/README.md) | 20／[20](scenarios/tcm/tcm_best_nature_multi/cases.md) | micro-F1（分） | **85.4** | **0.60** | 79.1 | **0.60** | 76.9 | 0.86 |
| [中医证型单选](scenarios/tcm/tcm_best_syndrome/README.md) | 68／[68](scenarios/tcm/tcm_best_syndrome/cases.md) | 准确率（%） | **80.9** | 0.63 | 72.1 | **0.50** | 66.2 | 0.63 |
| [中医证型多选](scenarios/tcm/tcm_best_syndrome_multi/README.md) | 32／[32](scenarios/tcm/tcm_best_syndrome_multi/cases.md) | micro-F1（分） | **52.8** | 0.65 | 36.7 | **0.59** | 26.7 | 1.33 |
| [MedJourney 检查预测选择题](scenarios/service/medjourney_ep_mcq/README.md) | 100／[100](scenarios/service/medjourney_ep_mcq/cases.md) | 准确率（%） | **82.0** | 0.61 | 79.0 | **0.54** | 72.0 | 0.69 |
| [MedJourney 治疗预测选择题](scenarios/service/medjourney_tp_mcq/README.md) | 100／[100](scenarios/service/medjourney_tp_mcq/cases.md) | 准确率（%） | **83.0** | 0.62 | 82.0 | **0.51** | 66.0 | 0.66 |
| [中医治则治法单选](scenarios/tcm/tcm_best_principles/README.md) | 20／[20](scenarios/tcm/tcm_best_principles/cases.md) | 准确率（%） | **90.0** | 0.62 | 70.0 | **0.51** | 75.0 | 0.62 |
| [中医治则治法多选](scenarios/tcm/tcm_best_principles_multi/README.md) | 97／[97](scenarios/tcm/tcm_best_principles_multi/cases.md) | micro-F1（分） | **70.3** | 0.63 | 62.3 | **0.60** | 47.0 | 1.34 |
| [BMI 当前身高参数选择](scenarios/calculators/bmi_height_selection/README.md) | 20／[20](scenarios/calculators/bmi_height_selection/cases.md) | 准确率（%） | **95.0** | 0.64 | **95.0** | **0.52** | 80.0 | 0.75 |
| [BMI 当前体重参数选择](scenarios/calculators/bmi_weight_selection/README.md) | 20／[20](scenarios/calculators/bmi_weight_selection/cases.md) | 准确率（%） | **95.0** | 0.63 | 90.0 | **0.49** | 70.0 | 0.97 |
| [临床计算输入充分性](scenarios/calculators/cmedcalc_input_sufficiency/README.md) | 200／[200](scenarios/calculators/cmedcalc_input_sufficiency/cases.md) | 准确率（%） | 81.5 | 0.93 | **84.0** | **0.55** | 72.5 | 0.74 |
| [临床量表语义分级](scenarios/calculators/cmedcalc_semantic_grade/README.md) | 162／[162](scenarios/calculators/cmedcalc_semantic_grade/cases.md) | 准确率（%） | **60.5** | 0.89 | 39.5 | **0.61** | 30.2 | 0.73 |
| [五种临床量表闭集数值评分](scenarios/calculators/medcalc_verified_bounded_score/README.md) | 100／[100](scenarios/calculators/medcalc_verified_bounded_score/cases.md) | 准确率（%） | 25.0 | 0.66 | **31.0** | **0.60** | 22.0 | 0.74 |
| [边界挑战：缺失计算参数](scenarios/calculators/challenge_missing_parameter/README.md) | 20／[20](scenarios/calculators/challenge_missing_parameter/cases.md) | 准确率（%） | **100.0** | 0.60 | **100.0** | **0.59** | 80.0 | 0.80 |
| [英文 MedQA医学考试](scenarios/knowledge/medqa_en_test/README.md) | 100／[100](scenarios/knowledge/medqa_en_test/cases.md) | 准确率（%） | **83.0** | 0.62 | 78.0 | **0.61** | 62.0 | 0.80 |
| [中文 MedQA医学考试](scenarios/knowledge/medqa_zh_test/README.md) | 100／[100](scenarios/knowledge/medqa_zh_test/cases.md) | 准确率（%） | **89.0** | 0.63 | 84.0 | **0.53** | 63.0 | 0.78 |
| [MedMCQA医学考试](scenarios/knowledge/medmcqa_validation/README.md) | 100／[100](scenarios/knowledge/medmcqa_validation/cases.md) | 准确率（%） | **72.0** | 0.63 | 67.0 | **0.54** | 53.0 | 0.78 |
| [中文医学考试单选](scenarios/knowledge/cmexam_mcq/README.md) | 95／[95](scenarios/knowledge/cmexam_mcq/cases.md) | 准确率（%） | **92.6** | 0.86 | 85.3 | **0.58** | 66.3 | 0.69 |
| [中文医学考试多选](scenarios/knowledge/cmexam_mcq_multi/README.md) | 20／[20](scenarios/knowledge/cmexam_mcq_multi/cases.md) | micro-F1（分） | 83.2 | **0.60** | **90.3** | 0.69 | 66.7 | 1.17 |
| [中医基础知识单选](scenarios/tcm/tcm_best_knowledge/README.md) | 89／[89](scenarios/tcm/tcm_best_knowledge/cases.md) | 准确率（%） | **91.0** | 0.63 | 83.1 | **0.51** | 64.0 | 0.63 |
| [中医基础知识多选](scenarios/tcm/tcm_best_knowledge_multi/README.md) | 20／[20](scenarios/tcm/tcm_best_knowledge_multi/cases.md) | micro-F1（分） | 81.5 | 0.66 | **87.9** | **0.62** | 76.6 | 0.93 |

<details>
<summary>展开详细数据：得分差值、费用、失败与原始材料</summary>

差值为 Jev 减 DeepSeek；美元费用顺序为 **Jev／DeepSeek**，未作答数顺序为 **Jev／DeepSeek／Qwen**。Qwen 人民币费用另列。

| 任务 | 得分差值［95% 区间］ | Jev 案例全对 | 每千条费用（美元） | Qwen 每千条（人民币） | 最终未作答（条） | 原始数据 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [MedJourney 诊断预测选择题](scenarios/service/medjourney_dp_mcq/README.md) | +1.0 ［-4.0, 6.0］ | 92/100 | $0.022／$0.037 | ¥0.582 | 0／0／0 | [题目](scenarios/service/medjourney_dp_mcq/samples.jsonl) · [提示词](scenarios/service/medjourney_dp_mcq/prompts.json) · [Jev](scenarios/service/medjourney_dp_mcq/responses.jsonl) · [DeepSeek](scenarios/service/medjourney_dp_mcq/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/service/medjourney_dp_mcq/comparison/qwen_responses.jsonl) |
| [合成病例主要诊断](scenarios/acute/ddxplus_synthetic_primary/README.md) | -4.0 ［-12.0, 5.0］ | 67/100 | $0.072／$0.095 | ¥1.823 | 0／0／0 | [题目](scenarios/acute/ddxplus_synthetic_primary/samples.jsonl) · [提示词](scenarios/acute/ddxplus_synthetic_primary/prompts.json) · [Jev](scenarios/acute/ddxplus_synthetic_primary/responses.jsonl) · [DeepSeek](scenarios/acute/ddxplus_synthetic_primary/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/acute/ddxplus_synthetic_primary/comparison/qwen_responses.jsonl) |
| [中医病历证型分类](scenarios/tcm/tcm_syndrome/README.md) | -7.0 ［-16.0, 2.0］ | 33/100 | $0.170／$0.098 | ¥4.004 | 0／0／1 | [题目](scenarios/tcm/tcm_syndrome/samples.jsonl) · [提示词](scenarios/tcm/tcm_syndrome/prompts.json) · [Jev](scenarios/tcm/tcm_syndrome/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_syndrome/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_syndrome/comparison/qwen_responses.jsonl) |
| [中医病位单选](scenarios/tcm/tcm_best_location/README.md) | +4.8 ［-9.5, 23.8］ | 17/21 | $0.024／$0.041 | ¥0.624 | 0／0／0 | [题目](scenarios/tcm/tcm_best_location/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_location/prompts.json) · [Jev](scenarios/tcm/tcm_best_location/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_location/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_location/comparison/qwen_responses.jsonl) |
| [中医病位多选](scenarios/tcm/tcm_best_location_multi/README.md) | -1.8 ［-7.5, 3.3］ | 12/79 | $0.033／$0.102 | ¥1.557 | 0／0／0 | [题目](scenarios/tcm/tcm_best_location_multi/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_location_multi/prompts.json) · [Jev](scenarios/tcm/tcm_best_location_multi/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_location_multi/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_location_multi/comparison/qwen_responses.jsonl) |
| [中医病性单选](scenarios/tcm/tcm_best_nature/README.md) | +10.1 ［2.0, 19.2］ | 69/99 | $0.024／$0.045 | ¥0.667 | 0／0／0 | [题目](scenarios/tcm/tcm_best_nature/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_nature/prompts.json) · [Jev](scenarios/tcm/tcm_best_nature/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_nature/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_nature/comparison/qwen_responses.jsonl) |
| [中医病性与要素多选](scenarios/tcm/tcm_best_nature_multi/README.md) | +6.3 ［-0.7, 13.5］ | 9/20 | $0.025／$0.064 | ¥0.918 | 0／0／0 | [题目](scenarios/tcm/tcm_best_nature_multi/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_nature_multi/prompts.json) · [Jev](scenarios/tcm/tcm_best_nature_multi/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_nature_multi/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_nature_multi/comparison/qwen_responses.jsonl) |
| [中医证型单选](scenarios/tcm/tcm_best_syndrome/README.md) | +8.8 ［0.0, 19.1］ | 55/68 | $0.027／$0.051 | ¥0.726 | 0／0／0 | [题目](scenarios/tcm/tcm_best_syndrome/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_syndrome/prompts.json) · [Jev](scenarios/tcm/tcm_best_syndrome/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_syndrome/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_syndrome/comparison/qwen_responses.jsonl) |
| [中医证型多选](scenarios/tcm/tcm_best_syndrome_multi/README.md) | +16.1 ［5.8, 27.6］ | 0/32 | $0.036／$0.110 | ¥1.623 | 0／0／0 | [题目](scenarios/tcm/tcm_best_syndrome_multi/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_syndrome_multi/prompts.json) · [Jev](scenarios/tcm/tcm_best_syndrome_multi/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_syndrome_multi/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_syndrome_multi/comparison/qwen_responses.jsonl) |
| [MedJourney 检查预测选择题](scenarios/service/medjourney_ep_mcq/README.md) | +3.0 ［-3.0, 9.0］ | 82/100 | $0.022／$0.038 | ¥0.577 | 0／3／0 | [题目](scenarios/service/medjourney_ep_mcq/samples.jsonl) · [提示词](scenarios/service/medjourney_ep_mcq/prompts.json) · [Jev](scenarios/service/medjourney_ep_mcq/responses.jsonl) · [DeepSeek](scenarios/service/medjourney_ep_mcq/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/service/medjourney_ep_mcq/comparison/qwen_responses.jsonl) |
| [MedJourney 治疗预测选择题](scenarios/service/medjourney_tp_mcq/README.md) | +1.0 ［-6.0, 9.0］ | 83/100 | $0.024／$0.040 | ¥0.617 | 0／0／0 | [题目](scenarios/service/medjourney_tp_mcq/samples.jsonl) · [提示词](scenarios/service/medjourney_tp_mcq/prompts.json) · [Jev](scenarios/service/medjourney_tp_mcq/responses.jsonl) · [DeepSeek](scenarios/service/medjourney_tp_mcq/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/service/medjourney_tp_mcq/comparison/qwen_responses.jsonl) |
| [中医治则治法单选](scenarios/tcm/tcm_best_principles/README.md) | +20.0 ［5.0, 40.0］ | 18/20 | $0.020／$0.049 | ¥0.549 | 0／0／0 | [题目](scenarios/tcm/tcm_best_principles/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_principles/prompts.json) · [Jev](scenarios/tcm/tcm_best_principles/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_principles/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_principles/comparison/qwen_responses.jsonl) |
| [中医治则治法多选](scenarios/tcm/tcm_best_principles_multi/README.md) | +8.0 ［3.5, 12.7］ | 23/97 | $0.035／$0.107 | ¥1.601 | 0／0／0 | [题目](scenarios/tcm/tcm_best_principles_multi/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_principles_multi/prompts.json) · [Jev](scenarios/tcm/tcm_best_principles_multi/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_principles_multi/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_principles_multi/comparison/qwen_responses.jsonl) |
| [BMI 当前身高参数选择](scenarios/calculators/bmi_height_selection/README.md) | +0.0 ［0.0, 0.0］ | 19/20 | $0.045／$0.116 | ¥1.768 | 0／0／2 | [题目](scenarios/calculators/bmi_height_selection/samples.jsonl) · [提示词](scenarios/calculators/bmi_height_selection/prompts.json) · [Jev](scenarios/calculators/bmi_height_selection/responses.jsonl) · [DeepSeek](scenarios/calculators/bmi_height_selection/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/calculators/bmi_height_selection/comparison/qwen_responses.jsonl) |
| [BMI 当前体重参数选择](scenarios/calculators/bmi_weight_selection/README.md) | +5.0 ［0.0, 15.0］ | 19/20 | $0.043／$0.111 | ¥1.891 | 0／0／6 | [题目](scenarios/calculators/bmi_weight_selection/samples.jsonl) · [提示词](scenarios/calculators/bmi_weight_selection/prompts.json) · [Jev](scenarios/calculators/bmi_weight_selection/responses.jsonl) · [DeepSeek](scenarios/calculators/bmi_weight_selection/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/calculators/bmi_weight_selection/comparison/qwen_responses.jsonl) |
| [临床计算输入充分性](scenarios/calculators/cmedcalc_input_sufficiency/README.md) | -2.5 ［-7.5, 2.5］ | 163/200 | $0.043／$0.078 | ¥1.130 | 0／0／0 | [题目](scenarios/calculators/cmedcalc_input_sufficiency/samples.jsonl) · [提示词](scenarios/calculators/cmedcalc_input_sufficiency/prompts.json) · [Jev](scenarios/calculators/cmedcalc_input_sufficiency/responses.jsonl) · [DeepSeek](scenarios/calculators/cmedcalc_input_sufficiency/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/calculators/cmedcalc_input_sufficiency/comparison/qwen_responses.jsonl) |
| [临床量表语义分级](scenarios/calculators/cmedcalc_semantic_grade/README.md) | +21.0 ［13.0, 29.6］ | 98/162 | $0.027／$0.046 | ¥0.751 | 0／0／2 | [题目](scenarios/calculators/cmedcalc_semantic_grade/samples.jsonl) · [提示词](scenarios/calculators/cmedcalc_semantic_grade/prompts.json) · [Jev](scenarios/calculators/cmedcalc_semantic_grade/responses.jsonl) · [DeepSeek](scenarios/calculators/cmedcalc_semantic_grade/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/calculators/cmedcalc_semantic_grade/comparison/qwen_responses.jsonl) |
| [五种临床量表闭集数值评分](scenarios/calculators/medcalc_verified_bounded_score/README.md) | -6.0 ［-17.0, 6.0］ | 25/100 | $0.051／$0.136 | ¥1.662 | 0／0／0 | [题目](scenarios/calculators/medcalc_verified_bounded_score/samples.jsonl) · [提示词](scenarios/calculators/medcalc_verified_bounded_score/prompts.json) · [Jev](scenarios/calculators/medcalc_verified_bounded_score/responses.jsonl) · [DeepSeek](scenarios/calculators/medcalc_verified_bounded_score/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/calculators/medcalc_verified_bounded_score/comparison/qwen_responses.jsonl) |
| [边界挑战：缺失计算参数](scenarios/calculators/challenge_missing_parameter/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.016／$0.043 | ¥0.459 | 0／0／0 | [题目](scenarios/calculators/challenge_missing_parameter/samples.jsonl) · [提示词](scenarios/calculators/challenge_missing_parameter/prompts.json) · [Jev](scenarios/calculators/challenge_missing_parameter/responses.jsonl) · [DeepSeek](scenarios/calculators/challenge_missing_parameter/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/calculators/challenge_missing_parameter/comparison/qwen_responses.jsonl) |
| [英文 MedQA医学考试](scenarios/knowledge/medqa_en_test/README.md) | +5.0 ［-2.0, 12.0］ | 83/100 | $0.024／$0.053 | ¥0.765 | 0／0／0 | [题目](scenarios/knowledge/medqa_en_test/samples.jsonl) · [提示词](scenarios/knowledge/medqa_en_test/prompts.json) · [Jev](scenarios/knowledge/medqa_en_test/responses.jsonl) · [DeepSeek](scenarios/knowledge/medqa_en_test/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/knowledge/medqa_en_test/comparison/qwen_responses.jsonl) |
| [中文 MedQA医学考试](scenarios/knowledge/medqa_zh_test/README.md) | +5.0 ［-1.0, 11.0］ | 89/100 | $0.018／$0.034 | ¥0.516 | 0／0／0 | [题目](scenarios/knowledge/medqa_zh_test/samples.jsonl) · [提示词](scenarios/knowledge/medqa_zh_test/prompts.json) · [Jev](scenarios/knowledge/medqa_zh_test/responses.jsonl) · [DeepSeek](scenarios/knowledge/medqa_zh_test/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/knowledge/medqa_zh_test/comparison/qwen_responses.jsonl) |
| [MedMCQA医学考试](scenarios/knowledge/medmcqa_validation/README.md) | +5.0 ［-4.0, 15.0］ | 72/100 | $0.016／$0.037 | ¥0.513 | 0／0／2 | [题目](scenarios/knowledge/medmcqa_validation/samples.jsonl) · [提示词](scenarios/knowledge/medmcqa_validation/prompts.json) · [Jev](scenarios/knowledge/medmcqa_validation/responses.jsonl) · [DeepSeek](scenarios/knowledge/medmcqa_validation/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/knowledge/medmcqa_validation/comparison/qwen_responses.jsonl) |
| [中文医学考试单选](scenarios/knowledge/cmexam_mcq/README.md) | +7.4 ［0.0, 14.7］ | 88/95 | $0.017／$0.039 | ¥0.468 | 0／0／0 | [题目](scenarios/knowledge/cmexam_mcq/samples.jsonl) · [提示词](scenarios/knowledge/cmexam_mcq/prompts.json) · [Jev](scenarios/knowledge/cmexam_mcq/responses.jsonl) · [DeepSeek](scenarios/knowledge/cmexam_mcq/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/knowledge/cmexam_mcq/comparison/qwen_responses.jsonl) |
| [中文医学考试多选](scenarios/knowledge/cmexam_mcq_multi/README.md) | -7.1 ［-16.6, 0.2］ | 9/20 | $0.020／$0.061 | ¥0.800 | 0／0／0 | [题目](scenarios/knowledge/cmexam_mcq_multi/samples.jsonl) · [提示词](scenarios/knowledge/cmexam_mcq_multi/prompts.json) · [Jev](scenarios/knowledge/cmexam_mcq_multi/responses.jsonl) · [DeepSeek](scenarios/knowledge/cmexam_mcq_multi/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/knowledge/cmexam_mcq_multi/comparison/qwen_responses.jsonl) |
| [中医基础知识单选](scenarios/tcm/tcm_best_knowledge/README.md) | +7.9 ［0.0, 16.9］ | 81/89 | $0.016／$0.040 | ¥0.463 | 0／0／0 | [题目](scenarios/tcm/tcm_best_knowledge/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_knowledge/prompts.json) · [Jev](scenarios/tcm/tcm_best_knowledge/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_knowledge/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_knowledge/comparison/qwen_responses.jsonl) |
| [中医基础知识多选](scenarios/tcm/tcm_best_knowledge_multi/README.md) | -6.4 ［-17.5, 2.2］ | 7/20 | $0.018／$0.055 | ¥0.807 | 0／0／0 | [题目](scenarios/tcm/tcm_best_knowledge_multi/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_knowledge_multi/prompts.json) · [Jev](scenarios/tcm/tcm_best_knowledge_multi/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_knowledge_multi/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_knowledge_multi/comparison/qwen_responses.jsonl) |

</details>

[返回领域导航](#领域导航)

<a id="results-followup"></a>

### 出院与随访

**1 项任务 · 20 条测试记录** · [任务定义与覆盖边界](docs/医疗任务总目录.md#followup)

| 任务 | 记录／来源案例 | 指标 | Jev 得分 | Jev 耗时（秒） | DeepSeek 得分 | DeepSeek 耗时（秒） | Qwen 得分 | Qwen 耗时（秒） |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [边界挑战：随访行动](scenarios/documentation/challenge_followup_action/README.md) | 20／[20](scenarios/documentation/challenge_followup_action/cases.md) | 准确率（%） | 95.0 | 0.61 | **100.0** | **0.56** | 85.0 | 0.63 |

<details>
<summary>展开详细数据：得分差值、费用、失败与原始材料</summary>

差值为 Jev 减 DeepSeek；美元费用顺序为 **Jev／DeepSeek**，未作答数顺序为 **Jev／DeepSeek／Qwen**。Qwen 人民币费用另列。

| 任务 | 得分差值［95% 区间］ | Jev 案例全对 | 每千条费用（美元） | Qwen 每千条（人民币） | 最终未作答（条） | 原始数据 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [边界挑战：随访行动](scenarios/documentation/challenge_followup_action/README.md) | -5.0 ［-15.0, 0.0］ | 19/20 | $0.016／$0.043 | ¥0.458 | 0／0／0 | [题目](scenarios/documentation/challenge_followup_action/samples.jsonl) · [提示词](scenarios/documentation/challenge_followup_action/prompts.json) · [Jev](scenarios/documentation/challenge_followup_action/responses.jsonl) · [DeepSeek](scenarios/documentation/challenge_followup_action/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/documentation/challenge_followup_action/comparison/qwen_responses.jsonl) |

</details>

[返回领域导航](#领域导航)

<a id="results-research"></a>

### 科研与循证

**13 项任务 · 1,225 条测试记录** · [任务定义与覆盖边界](docs/医疗任务总目录.md#research)

| 任务 | 记录／来源案例 | 指标 | Jev 得分 | Jev 耗时（秒） | DeepSeek 得分 | DeepSeek 耗时（秒） | Qwen 得分 | Qwen 耗时（秒） |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [PICO 固定窗口识别](scenarios/evidence/ebm_pico_fixed_windows/README.md) | 100／[76](scenarios/evidence/ebm_pico_fixed_windows/cases.md) | micro-F1（分） | 12.7 | 0.63 | 25.4 | **0.56** | **28.6** | 0.90 |
| [研究结局固定窗口分类](scenarios/evidence/evidenceoutcomes_fixed_window/README.md) | 100／[92](scenarios/evidence/evidenceoutcomes_fixed_window/cases.md) | 准确率（%） | **88.0** | 0.66 | 67.0 | **0.55** | 67.0 | 0.73 |
| [RCT 摘要句功能分类](scenarios/evidence/pubmed_rct_section/README.md) | 100／[98](scenarios/evidence/pubmed_rct_section/cases.md) | 准确率（%） | 75.0 | 0.90 | **77.0** | **0.53** | 73.0 | 0.67 |
| [临床研究干预结果方向](scenarios/evidence/evidence_inference_fulltext/README.md) | 100／[84](scenarios/evidence/evidence_inference_fulltext/cases.md) | 准确率（%） | **89.0** | 0.87 | 76.0 | **0.57** | 61.0 | 1.40 |
| [全文证据句筛选](scenarios/evidence/evidencebench_sentence_selection/README.md) | 37／[37](scenarios/evidence/evidencebench_sentence_selection/cases.md) | micro-F1（分） | **29.4** | **1.15** | 25.9 | 2.31 | 20.6 | 25.66 |
| [摘要支持的研究问题回答](scenarios/evidence/pubmedqa_evidence_qa/README.md) | 100／[100](scenarios/evidence/pubmedqa_evidence_qa/cases.md) | 准确率（%） | 74.0 | 0.91 | **76.0** | **0.54** | 72.0 | 0.65 |
| [科学论断与给定摘要一致性](scenarios/evidence/scifact_cited_abstract/README.md) | 118／[100](scenarios/evidence/scifact_cited_abstract/cases.md) | 准确率（%） | 85.6 | 0.64 | **89.0** | **0.54** | 83.9 | 0.73 |
| [边界挑战：证据支持](scenarios/evidence/challenge_evidence_support/README.md) | 20／[20](scenarios/evidence/challenge_evidence_support/cases.md) | 准确率（%） | **100.0** | 0.60 | 75.0 | **0.58** | **100.0** | 0.65 |
| [临床试验证据支持判断](scenarios/trials/nli4ct_entailment/README.md) | 100／[70](scenarios/trials/nli4ct_entailment/cases.md) | 准确率（%） | **88.0** | 0.91 | 87.0 | **0.51** | 77.0 | 0.66 |
| [临床试验证据句定位](scenarios/trials/nli4ct_evidence/README.md) | 100／[74](scenarios/trials/nli4ct_evidence/cases.md) | micro-F1（分） | 49.9 | 0.94 | **68.3** | **0.82** | 22.1 | 2.50 |
| [患者与临床试验入组预筛](scenarios/trials/trialgpt_sigir_referral/README.md) | 150／[45](scenarios/trials/trialgpt_sigir_referral/cases.md) | 准确率（%） | 48.0 | 0.65 | **54.7** | **0.50** | 52.7 | 0.69 |
| [公共卫生核查：仅论断](scenarios/evidence/pubhealth_claim_only/README.md) | 100／[100](scenarios/evidence/pubhealth_claim_only/cases.md) | 准确率（%） | 20.0 | 0.77 | **44.0** | **0.55** | 42.0 | 0.66 |
| [公共卫生核查：提供核查文章](scenarios/evidence/pubhealth_with_article/README.md) | 100／[100](scenarios/evidence/pubhealth_with_article/cases.md) | 准确率（%） | 67.0 | 0.82 | **72.0** | **0.55** | 49.0 | 0.69 |

<details>
<summary>展开详细数据：得分差值、费用、失败与原始材料</summary>

差值为 Jev 减 DeepSeek；美元费用顺序为 **Jev／DeepSeek**，未作答数顺序为 **Jev／DeepSeek／Qwen**。Qwen 人民币费用另列。

| 任务 | 得分差值［95% 区间］ | Jev 案例全对 | 每千条费用（美元） | Qwen 每千条（人民币） | 最终未作答（条） | 原始数据 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [PICO 固定窗口识别](scenarios/evidence/ebm_pico_fixed_windows/README.md) | -12.7 ［-24.4, -2.1］ | 29/76 | $0.034／$0.084 | ¥1.283 | 0／0／0 | [题目](scenarios/evidence/ebm_pico_fixed_windows/samples.jsonl) · [提示词](scenarios/evidence/ebm_pico_fixed_windows/prompts.json) · [Jev](scenarios/evidence/ebm_pico_fixed_windows/responses.jsonl) · [DeepSeek](scenarios/evidence/ebm_pico_fixed_windows/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/evidence/ebm_pico_fixed_windows/comparison/qwen_responses.jsonl) |
| [研究结局固定窗口分类](scenarios/evidence/evidenceoutcomes_fixed_window/README.md) | +21.0 ［11.9, 30.3］ | 80/92 | $0.044／$0.108 | ¥1.451 | 0／0／0 | [题目](scenarios/evidence/evidenceoutcomes_fixed_window/samples.jsonl) · [提示词](scenarios/evidence/evidenceoutcomes_fixed_window/prompts.json) · [Jev](scenarios/evidence/evidenceoutcomes_fixed_window/responses.jsonl) · [DeepSeek](scenarios/evidence/evidenceoutcomes_fixed_window/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/evidence/evidenceoutcomes_fixed_window/comparison/qwen_responses.jsonl) |
| [RCT 摘要句功能分类](scenarios/evidence/pubmed_rct_section/README.md) | -2.0 ［-6.1, 2.0］ | 73/98 | $0.017／$0.036 | ¥0.501 | 0／0／0 | [题目](scenarios/evidence/pubmed_rct_section/samples.jsonl) · [提示词](scenarios/evidence/pubmed_rct_section/prompts.json) · [Jev](scenarios/evidence/pubmed_rct_section/responses.jsonl) · [DeepSeek](scenarios/evidence/pubmed_rct_section/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/evidence/pubmed_rct_section/comparison/qwen_responses.jsonl) |
| [临床研究干预结果方向](scenarios/evidence/evidence_inference_fulltext/README.md) | +13.0 ［4.2, 22.4］ | 73/84 | $0.325／$1.041 | ¥11.401 | 0／0／0 | [题目](scenarios/evidence/evidence_inference_fulltext/samples.jsonl) · [提示词](scenarios/evidence/evidence_inference_fulltext/prompts.json) · [Jev](scenarios/evidence/evidence_inference_fulltext/responses.jsonl) · [DeepSeek](scenarios/evidence/evidence_inference_fulltext/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/evidence/evidence_inference_fulltext/comparison/qwen_responses.jsonl) |
| [全文证据句筛选](scenarios/evidence/evidencebench_sentence_selection/README.md) | +3.5 ［0.6, 6.8］ | 0/37 | $0.609／$1.927 | ¥40.115 | 0／0／2 | [题目](scenarios/evidence/evidencebench_sentence_selection/samples.jsonl) · [提示词](scenarios/evidence/evidencebench_sentence_selection/prompts.json) · [Jev](scenarios/evidence/evidencebench_sentence_selection/responses.jsonl) · [DeepSeek](scenarios/evidence/evidencebench_sentence_selection/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/evidence/evidencebench_sentence_selection/comparison/qwen_responses.jsonl) |
| [摘要支持的研究问题回答](scenarios/evidence/pubmedqa_evidence_qa/README.md) | -2.0 ［-9.0, 5.0］ | 74/100 | $0.030／$0.069 | ¥0.947 | 0／0／0 | [题目](scenarios/evidence/pubmedqa_evidence_qa/samples.jsonl) · [提示词](scenarios/evidence/pubmedqa_evidence_qa/prompts.json) · [Jev](scenarios/evidence/pubmedqa_evidence_qa/responses.jsonl) · [DeepSeek](scenarios/evidence/pubmedqa_evidence_qa/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/evidence/pubmedqa_evidence_qa/comparison/qwen_responses.jsonl) |
| [科学论断与给定摘要一致性](scenarios/evidence/scifact_cited_abstract/README.md) | -3.4 ［-8.7, 1.7］ | 83/100 | $0.033／$0.077 | ¥1.074 | 0／0／0 | [题目](scenarios/evidence/scifact_cited_abstract/samples.jsonl) · [提示词](scenarios/evidence/scifact_cited_abstract/prompts.json) · [Jev](scenarios/evidence/scifact_cited_abstract/responses.jsonl) · [DeepSeek](scenarios/evidence/scifact_cited_abstract/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/evidence/scifact_cited_abstract/comparison/qwen_responses.jsonl) |
| [边界挑战：证据支持](scenarios/evidence/challenge_evidence_support/README.md) | +25.0 ［5.0, 45.0］ | 20/20 | $0.016／$0.043 | ¥0.457 | 0／0／0 | [题目](scenarios/evidence/challenge_evidence_support/samples.jsonl) · [提示词](scenarios/evidence/challenge_evidence_support/prompts.json) · [Jev](scenarios/evidence/challenge_evidence_support/responses.jsonl) · [DeepSeek](scenarios/evidence/challenge_evidence_support/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/evidence/challenge_evidence_support/comparison/qwen_responses.jsonl) |
| [临床试验证据支持判断](scenarios/trials/nli4ct_entailment/README.md) | +1.0 ［-4.0, 6.1］ | 58/70 | $0.040／$0.080 | ¥1.273 | 0／0／0 | [题目](scenarios/trials/nli4ct_entailment/samples.jsonl) · [提示词](scenarios/trials/nli4ct_entailment/prompts.json) · [Jev](scenarios/trials/nli4ct_entailment/responses.jsonl) · [DeepSeek](scenarios/trials/nli4ct_entailment/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/trials/nli4ct_entailment/comparison/qwen_responses.jsonl) |
| [临床试验证据句定位](scenarios/trials/nli4ct_evidence/README.md) | -18.4 ［-26.7, -8.6］ | 3/74 | $0.073／$0.200 | ¥4.525 | 0／0／0 | [题目](scenarios/trials/nli4ct_evidence/samples.jsonl) · [提示词](scenarios/trials/nli4ct_evidence/prompts.json) · [Jev](scenarios/trials/nli4ct_evidence/responses.jsonl) · [DeepSeek](scenarios/trials/nli4ct_evidence/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/trials/nli4ct_evidence/comparison/qwen_responses.jsonl) |
| [患者与临床试验入组预筛](scenarios/trials/trialgpt_sigir_referral/README.md) | -6.7 ［-12.1, -1.6］ | 11/45 | $0.038／$0.096 | ¥1.246 | 0／0／0 | [题目](scenarios/trials/trialgpt_sigir_referral/samples.jsonl) · [提示词](scenarios/trials/trialgpt_sigir_referral/prompts.json) · [Jev](scenarios/trials/trialgpt_sigir_referral/responses.jsonl) · [DeepSeek](scenarios/trials/trialgpt_sigir_referral/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/trials/trialgpt_sigir_referral/comparison/qwen_responses.jsonl) |
| [公共卫生核查：仅论断](scenarios/evidence/pubhealth_claim_only/README.md) | -24.0 ［-35.0, -13.0］ | 20/100 | $0.016／$0.033 | ¥0.679 | 0／0／17 | [题目](scenarios/evidence/pubhealth_claim_only/samples.jsonl) · [提示词](scenarios/evidence/pubhealth_claim_only/prompts.json) · [Jev](scenarios/evidence/pubhealth_claim_only/responses.jsonl) · [DeepSeek](scenarios/evidence/pubhealth_claim_only/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/evidence/pubhealth_claim_only/comparison/qwen_responses.jsonl) |
| [公共卫生核查：提供核查文章](scenarios/evidence/pubhealth_with_article/README.md) | -5.0 ［-14.0, 3.0］ | 67/100 | $0.052／$0.151 | ¥2.404 | 0／0／17 | [题目](scenarios/evidence/pubhealth_with_article/samples.jsonl) · [提示词](scenarios/evidence/pubhealth_with_article/prompts.json) · [Jev](scenarios/evidence/pubhealth_with_article/responses.jsonl) · [DeepSeek](scenarios/evidence/pubhealth_with_article/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/evidence/pubhealth_with_article/comparison/qwen_responses.jsonl) |

</details>

[返回领域导航](#领域导航)

<a id="results-governance"></a>

### 数据治理与运营

**9 项任务 · 877 条测试记录** · [任务定义与覆盖边界](docs/医疗任务总目录.md#governance)

| 任务 | 记录／来源案例 | 指标 | Jev 得分 | Jev 耗时（秒） | DeepSeek 得分 | DeepSeek 耗时（秒） | Qwen 得分 | Qwen 耗时（秒） |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [边界挑战：编码证据](scenarios/records/challenge_coding_evidence/README.md) | 20／[20](scenarios/records/challenge_coding_evidence/cases.md) | 准确率（%） | 100.0 | 0.59 | 100.0 | **0.58** | 100.0 | 0.85 |
| [边界挑战：隐私信息候选](scenarios/quality/challenge_phi_candidate/README.md) | 20／[20](scenarios/quality/challenge_phi_candidate/cases.md) | 准确率（%） | **95.0** | 0.61 | **95.0** | **0.59** | 75.0 | 0.78 |
| [医学回答幻觉识别：有证据](scenarios/quality/medhallu_with_evidence/README.md) | 200／[100](scenarios/quality/medhallu_with_evidence/cases.md) | 准确率（%） | 82.0 | 0.64 | **82.5** | **0.54** | 61.0 | 0.83 |
| [医学回答幻觉识别：无证据](scenarios/quality/medhallu_without_evidence/README.md) | 200／[100](scenarios/quality/medhallu_without_evidence/cases.md) | 准确率（%） | 60.0 | 0.63 | **69.5** | **0.52** | 58.5 | 0.80 |
| [医疗有害请求筛查](scenarios/quality/medsafety_request_gate/README.md) | 200／[200](scenarios/quality/medsafety_request_gate/cases.md) | 准确率（%） | 93.5 | 0.63 | 96.0 | **0.52** | **99.0** | 0.92 |
| [边界挑战：提示注入](scenarios/quality/challenge_prompt_injection/README.md) | 20／[20](scenarios/quality/challenge_prompt_injection/cases.md) | 准确率（%） | **100.0** | 0.61 | **100.0** | **0.58** | 65.0 | 0.80 |
| [医学伦理单选](scenarios/tcm/tcm_best_ethics/README.md) | 97／[97](scenarios/tcm/tcm_best_ethics/cases.md) | 准确率（%） | **89.7** | 0.61 | 79.4 | **0.52** | 72.2 | 0.65 |
| [医学伦理与执业规范多选](scenarios/tcm/tcm_best_ethics_multi/README.md) | 20／[20](scenarios/tcm/tcm_best_ethics_multi/cases.md) | micro-F1（分） | 88.9 | 0.61 | **89.4** | **0.57** | 86.1 | 0.96 |
| [中医安全问题标签一致性](scenarios/tcm/tcm_best_安全问题/README.md) | 100／[100](scenarios/tcm/tcm_best_安全问题/cases.md) | 准确率（%） | 27.0 | 0.64 | 29.0 | **0.53** | **32.0** | 0.62 |

<details>
<summary>展开详细数据：得分差值、费用、失败与原始材料</summary>

差值为 Jev 减 DeepSeek；美元费用顺序为 **Jev／DeepSeek**，未作答数顺序为 **Jev／DeepSeek／Qwen**。Qwen 人民币费用另列。

| 任务 | 得分差值［95% 区间］ | Jev 案例全对 | 每千条费用（美元） | Qwen 每千条（人民币） | 最终未作答（条） | 原始数据 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [边界挑战：编码证据](scenarios/records/challenge_coding_evidence/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.016／$0.044 | ¥0.464 | 0／0／0 | [题目](scenarios/records/challenge_coding_evidence/samples.jsonl) · [提示词](scenarios/records/challenge_coding_evidence/prompts.json) · [Jev](scenarios/records/challenge_coding_evidence/responses.jsonl) · [DeepSeek](scenarios/records/challenge_coding_evidence/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/records/challenge_coding_evidence/comparison/qwen_responses.jsonl) |
| [边界挑战：隐私信息候选](scenarios/quality/challenge_phi_candidate/README.md) | +0.0 ［0.0, 0.0］ | 19/20 | $0.016／$0.043 | ¥0.470 | 0／0／0 | [题目](scenarios/quality/challenge_phi_candidate/samples.jsonl) · [提示词](scenarios/quality/challenge_phi_candidate/prompts.json) · [Jev](scenarios/quality/challenge_phi_candidate/responses.jsonl) · [DeepSeek](scenarios/quality/challenge_phi_candidate/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/quality/challenge_phi_candidate/comparison/qwen_responses.jsonl) |
| [医学回答幻觉识别：有证据](scenarios/quality/medhallu_with_evidence/README.md) | -0.5 ［-5.5, 5.0］ | 67/100 | $0.032／$0.077 | ¥1.037 | 0／0／0 | [题目](scenarios/quality/medhallu_with_evidence/samples.jsonl) · [提示词](scenarios/quality/medhallu_with_evidence/prompts.json) · [Jev](scenarios/quality/medhallu_with_evidence/responses.jsonl) · [DeepSeek](scenarios/quality/medhallu_with_evidence/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/quality/medhallu_with_evidence/comparison/qwen_responses.jsonl) |
| [医学回答幻觉识别：无证据](scenarios/quality/medhallu_without_evidence/README.md) | -9.5 ［-16.0, -3.0］ | 38/100 | $0.017／$0.032 | ¥0.543 | 0／0／0 | [题目](scenarios/quality/medhallu_without_evidence/samples.jsonl) · [提示词](scenarios/quality/medhallu_without_evidence/prompts.json) · [Jev](scenarios/quality/medhallu_without_evidence/responses.jsonl) · [DeepSeek](scenarios/quality/medhallu_without_evidence/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/quality/medhallu_without_evidence/comparison/qwen_responses.jsonl) |
| [医疗有害请求筛查](scenarios/quality/medsafety_request_gate/README.md) | -2.5 ［-5.5, 1.0］ | 187/200 | $0.015／$0.042 | ¥0.490 | 0／0／0 | [题目](scenarios/quality/medsafety_request_gate/samples.jsonl) · [提示词](scenarios/quality/medsafety_request_gate/prompts.json) · [Jev](scenarios/quality/medsafety_request_gate/responses.jsonl) · [DeepSeek](scenarios/quality/medsafety_request_gate/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/quality/medsafety_request_gate/comparison/qwen_responses.jsonl) |
| [边界挑战：提示注入](scenarios/quality/challenge_prompt_injection/README.md) | +0.0 ［0.0, 0.0］ | 20/20 | $0.017／$0.043 | ¥0.469 | 0／0／0 | [题目](scenarios/quality/challenge_prompt_injection/samples.jsonl) · [提示词](scenarios/quality/challenge_prompt_injection/prompts.json) · [Jev](scenarios/quality/challenge_prompt_injection/responses.jsonl) · [DeepSeek](scenarios/quality/challenge_prompt_injection/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/quality/challenge_prompt_injection/comparison/qwen_responses.jsonl) |
| [医学伦理单选](scenarios/tcm/tcm_best_ethics/README.md) | +10.3 ［4.1, 17.5］ | 87/97 | $0.020／$0.038 | ¥0.531 | 0／0／0 | [题目](scenarios/tcm/tcm_best_ethics/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_ethics/prompts.json) · [Jev](scenarios/tcm/tcm_best_ethics/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_ethics/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_ethics/comparison/qwen_responses.jsonl) |
| [医学伦理与执业规范多选](scenarios/tcm/tcm_best_ethics_multi/README.md) | -0.5 ［-10.6, 8.0］ | 12/20 | $0.021／$0.066 | ¥0.833 | 0／0／0 | [题目](scenarios/tcm/tcm_best_ethics_multi/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_ethics_multi/prompts.json) · [Jev](scenarios/tcm/tcm_best_ethics_multi/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_ethics_multi/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_ethics_multi/comparison/qwen_responses.jsonl) |
| [中医安全问题标签一致性](scenarios/tcm/tcm_best_安全问题/README.md) | -2.0 ［-9.0, 5.0］ | 27/100 | $0.019／$0.034 | ¥0.491 | 0／0／0 | [题目](scenarios/tcm/tcm_best_安全问题/samples.jsonl) · [提示词](scenarios/tcm/tcm_best_安全问题/prompts.json) · [Jev](scenarios/tcm/tcm_best_安全问题/responses.jsonl) · [DeepSeek](scenarios/tcm/tcm_best_安全问题/comparison/deepseek_responses.jsonl) · [Qwen](scenarios/tcm/tcm_best_安全问题/comparison/qwen_responses.jsonl) |

</details>

[返回领域导航](#领域导航)

<details>
<summary><strong>评测口径、模型版本与使用边界</strong></summary>

- **测了什么**：72 项公开材料适配条件、24 项自编边界挑战。条件数不等于独立医疗工作数，输入数不等于患者数；给定实体、候选或章节边界的任务要按原条件理解。
- **怎么比较**：Jev 为 `jev-1.13.0`；DeepSeek 请求名为 `deepseek-flash`，归档配置记为 V4.1 Flash、关闭思考模式。Qwen 为硅基流动 `Qwen/Qwen3.5-9B`、关闭思考模式。三者使用相同材料与判断目标；主效果评测不是同期测速。
- **怎么计分**：首页四个例子在分析后选取，全部任务在上方按领域展开。分类报告准确率，集合抽取报告 micro-F1，不混成一个总分。失败留在分母；配对区间按来源案例聚合，属于探索性分析，未校正多重比较。
- **能得出什么**：公开材料、合成病例和小样本测试可帮助筛选下一步验证方向。当前没有真实医院的前瞻性流程验证、独立医生全量审核或患者结局证据。
- **哪些另算**：批处理与扰动实验分别报告；27 类训练任务只作为独立扩展映射，不计入主评测成绩。

[详细方法](docs/EVALUATION.md) · [同题对比配置](comparisons/deepseek-flash/README.md) · [来源与未完成项](docs/覆盖与阻塞账本.md)

</details>

代码使用 [MIT 许可证](LICENSE)；评测文本、标注、媒体和服务输出遵循各自的[第三方使用条件](THIRD_PARTY_NOTICES.md)。引用结果时请记录提交号、任务 ID 和模型版本。
