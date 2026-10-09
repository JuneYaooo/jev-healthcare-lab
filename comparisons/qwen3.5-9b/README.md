# Qwen3.5-9B：同题医疗任务对照

[返回三模型对比](../../README.md#全部领域与任务的详细测试数据)

通过硅基流动中国站调用 `Qwen/Qwen3.5-9B`，覆盖 **96 项任务、7,133 条输入**。Jev 和 DeepSeek 使用已归档的同题结果；Qwen 为本次新增调用。

| 项目 | 结果 |
| --- | ---: |
| 可评分记录（含规则空集） | 7,024 |
| 最终调用或格式失败 | 109 |
| 无候选、无需 API 的规则空集 | 43 |
| 保留的早期尝试 | 866 |
| 成功请求中位响应 | 0.79 秒 |
| 输入／输出 tokens（含重试） | 7,796,362／240,595 |
| 全部评测调用的估算费用 | ¥14.5817 |
| 每千条输入的估算费用 | ¥2.044 |

## 比较方法

- **题目不变**：读取已冻结的 `samples.jsonl`，仅向模型发送 `request`，不发送金标或评分元数据。每条记录保留原始请求与供应商请求的 SHA-256。
- **输出接口一致**：沿用 DeepSeek 的系统提示词、JSON 输出格式与 choice／布尔值适配器。设置 `temperature=0`、`enable_thinking=false`；输出上限沿用相同的按问题数计算规则。
- **评分一致**：单标签任务报告准确率，集合任务报告 micro-F1；保留调用和格式失败在分母中，失败分类计错、失败集合按空集评分。
- **格式要求**：choice 必须返回给定选项的键，不能用选项说明或提取出的数值代替。只允许与既有 DeepSeek 适配器相同的无歧义整数键转字符串，不针对某个模型追加答案修复。格式失败原因和原始内容均保留。
- **分数含义**：这里衡量既定输入与输出约定下的端到端任务表现；医学判断与结构化输出能力都会影响得分，不能把格式失败全部解释为医学知识错误。
- **重试透明**：单次执行最多尝试三次；首轮遇到限流后增加共享 60 秒等待，并对传输失败补跑。成功答案不重跑，格式失败不在恢复阶段额外重跑，所有早期尝试嵌入最终记录的 `prior_attempts`。不按答案正误决定重跑。
- **时间口径**：8 并发；表内耗时为成功最终请求从发出到完整响应的中位时间，排除规则空集和早期重试。三家调用日期、服务端负载与接口不同，不能据此认定为同期速度排名。分阶段运行未合成为整批总时间。

## 费用口径

按[硅基流动中国站公开模型目录](https://www.siliconflow.cn/models)在 `2026-10-09T08:25:59.315130+00:00` 的费率快照估算：每百万输入 tokens **¥1.5**，每百万输出 tokens **¥12**。保留[原始费率字段](pricing_source.json)。

计入所有有用量记录的最终调用和早期重试；不假设缓存折扣，不包含未返回用量的调用、接口连通性试跑、上游 OCR／ASR 或人工成本。该数值是公开标价估算，不是账单实付金额。Jev／DeepSeek 原表为美元，未做汇率换算。

## 各任务结果

| 任务 | 输入数 | 指标 | Jev | DeepSeek | Qwen | Qwen 中位耗时（秒） | Qwen 每千条（人民币） | 失败数 | 原始回答 |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [合成病例主要诊断](../../scenarios/acute/ddxplus_synthetic_primary/README.md) | 100 | 准确率（%） | 67.0 | 71.0 | 60.0 | 0.82 | ¥1.823 | 0 | [Qwen](../../scenarios/acute/ddxplus_synthetic_primary/comparison/qwen_responses.jsonl) |
| [BMI 当前身高参数选择](../../scenarios/calculators/bmi_height_selection/README.md) | 20 | 准确率（%） | 95.0 | 95.0 | 80.0 | 0.75 | ¥1.768 | 2 | [Qwen](../../scenarios/calculators/bmi_height_selection/comparison/qwen_responses.jsonl) |
| [BMI 当前体重参数选择](../../scenarios/calculators/bmi_weight_selection/README.md) | 20 | 准确率（%） | 95.0 | 90.0 | 70.0 | 0.97 | ¥1.891 | 6 | [Qwen](../../scenarios/calculators/bmi_weight_selection/comparison/qwen_responses.jsonl) |
| [边界挑战：检验数值关联](../../scenarios/calculators/challenge_lab_link/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.68 | ¥0.503 | 0 | [Qwen](../../scenarios/calculators/challenge_lab_link/comparison/qwen_responses.jsonl) |
| [边界挑战：缺失计算参数](../../scenarios/calculators/challenge_missing_parameter/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 80.0 | 0.80 | ¥0.459 | 0 | [Qwen](../../scenarios/calculators/challenge_missing_parameter/comparison/qwen_responses.jsonl) |
| [边界挑战：单位等价](../../scenarios/calculators/challenge_unit_equivalence/README.md) | 20 | 准确率（%） | 95.0 | 100.0 | 80.0 | 0.70 | ¥0.458 | 0 | [Qwen](../../scenarios/calculators/challenge_unit_equivalence/comparison/qwen_responses.jsonl) |
| [临床计算输入充分性](../../scenarios/calculators/cmedcalc_input_sufficiency/README.md) | 200 | 准确率（%） | 81.5 | 84.0 | 72.5 | 0.74 | ¥1.130 | 0 | [Qwen](../../scenarios/calculators/cmedcalc_input_sufficiency/comparison/qwen_responses.jsonl) |
| [临床量表语义分级](../../scenarios/calculators/cmedcalc_semantic_grade/README.md) | 162 | 准确率（%） | 60.5 | 39.5 | 30.2 | 0.73 | ¥0.751 | 2 | [Qwen](../../scenarios/calculators/cmedcalc_semantic_grade/comparison/qwen_responses.jsonl) |
| [五种临床量表闭集数值评分](../../scenarios/calculators/medcalc_verified_bounded_score/README.md) | 100 | 准确率（%） | 25.0 | 31.0 | 22.0 | 0.74 | ¥1.662 | 0 | [Qwen](../../scenarios/calculators/medcalc_verified_bounded_score/comparison/qwen_responses.jsonl) |
| [已分段病历章节分类](../../scenarios/documentation/aci_note_section/README.md) | 100 | 准确率（%） | 99.0 | 100.0 | 100.0 | 0.66 | ¥0.684 | 0 | [Qwen](../../scenarios/documentation/aci_note_section/comparison/qwen_responses.jsonl) |
| [边界挑战：文档类型](../../scenarios/documentation/challenge_document_type/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.62 | ¥0.448 | 0 | [Qwen](../../scenarios/documentation/challenge_document_type/comparison/qwen_responses.jsonl) |
| [边界挑战：文书缺项](../../scenarios/documentation/challenge_documentation/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.62 | ¥0.455 | 0 | [Qwen](../../scenarios/documentation/challenge_documentation/comparison/qwen_responses.jsonl) |
| [边界挑战：随访行动](../../scenarios/documentation/challenge_followup_action/README.md) | 20 | 准确率（%） | 95.0 | 100.0 | 85.0 | 0.63 | ¥0.458 | 0 | [Qwen](../../scenarios/documentation/challenge_followup_action/comparison/qwen_responses.jsonl) |
| [问诊对话对应病历章节](../../scenarios/documentation/mts_section_classification/README.md) | 100 | 准确率（%） | 76.0 | 73.0 | 68.0 | 0.70 | ¥0.899 | 0 | [Qwen](../../scenarios/documentation/mts_section_classification/comparison/qwen_responses.jsonl) |
| [边界挑战：证据支持](../../scenarios/evidence/challenge_evidence_support/README.md) | 20 | 准确率（%） | 100.0 | 75.0 | 100.0 | 0.65 | ¥0.457 | 0 | [Qwen](../../scenarios/evidence/challenge_evidence_support/comparison/qwen_responses.jsonl) |
| [PICO 固定窗口识别](../../scenarios/evidence/ebm_pico_fixed_windows/README.md) | 100 | micro-F1（分） | 12.7 | 25.4 | 28.6 | 0.90 | ¥1.283 | 0 | [Qwen](../../scenarios/evidence/ebm_pico_fixed_windows/comparison/qwen_responses.jsonl) |
| [临床研究干预结果方向](../../scenarios/evidence/evidence_inference_fulltext/README.md) | 100 | 准确率（%） | 89.0 | 76.0 | 61.0 | 1.40 | ¥11.401 | 0 | [Qwen](../../scenarios/evidence/evidence_inference_fulltext/comparison/qwen_responses.jsonl) |
| [全文证据句筛选](../../scenarios/evidence/evidencebench_sentence_selection/README.md) | 37 | micro-F1（分） | 29.4 | 25.9 | 20.6 | 25.66 | ¥40.115 | 2 | [Qwen](../../scenarios/evidence/evidencebench_sentence_selection/comparison/qwen_responses.jsonl) |
| [研究结局固定窗口分类](../../scenarios/evidence/evidenceoutcomes_fixed_window/README.md) | 100 | 准确率（%） | 88.0 | 67.0 | 67.0 | 0.73 | ¥1.451 | 0 | [Qwen](../../scenarios/evidence/evidenceoutcomes_fixed_window/comparison/qwen_responses.jsonl) |
| [公共卫生核查：仅论断](../../scenarios/evidence/pubhealth_claim_only/README.md) | 100 | 准确率（%） | 20.0 | 44.0 | 42.0 | 0.66 | ¥0.679 | 17 | [Qwen](../../scenarios/evidence/pubhealth_claim_only/comparison/qwen_responses.jsonl) |
| [公共卫生核查：提供核查文章](../../scenarios/evidence/pubhealth_with_article/README.md) | 100 | 准确率（%） | 67.0 | 72.0 | 49.0 | 0.69 | ¥2.404 | 17 | [Qwen](../../scenarios/evidence/pubhealth_with_article/comparison/qwen_responses.jsonl) |
| [RCT 摘要句功能分类](../../scenarios/evidence/pubmed_rct_section/README.md) | 100 | 准确率（%） | 75.0 | 77.0 | 73.0 | 0.67 | ¥0.501 | 0 | [Qwen](../../scenarios/evidence/pubmed_rct_section/comparison/qwen_responses.jsonl) |
| [摘要支持的研究问题回答](../../scenarios/evidence/pubmedqa_evidence_qa/README.md) | 100 | 准确率（%） | 74.0 | 76.0 | 72.0 | 0.65 | ¥0.947 | 0 | [Qwen](../../scenarios/evidence/pubmedqa_evidence_qa/comparison/qwen_responses.jsonl) |
| [科学论断与给定摘要一致性](../../scenarios/evidence/scifact_cited_abstract/README.md) | 118 | 准确率（%） | 85.6 | 89.0 | 83.9 | 0.73 | ¥1.074 | 0 | [Qwen](../../scenarios/evidence/scifact_cited_abstract/comparison/qwen_responses.jsonl) |
| [中文医学考试单选](../../scenarios/knowledge/cmexam_mcq/README.md) | 95 | 准确率（%） | 92.6 | 85.3 | 66.3 | 0.69 | ¥0.468 | 0 | [Qwen](../../scenarios/knowledge/cmexam_mcq/comparison/qwen_responses.jsonl) |
| [中文医学考试多选](../../scenarios/knowledge/cmexam_mcq_multi/README.md) | 20 | micro-F1（分） | 83.2 | 90.3 | 66.7 | 1.17 | ¥0.800 | 0 | [Qwen](../../scenarios/knowledge/cmexam_mcq_multi/comparison/qwen_responses.jsonl) |
| [MedMCQA医学考试](../../scenarios/knowledge/medmcqa_validation/README.md) | 100 | 准确率（%） | 72.0 | 67.0 | 53.0 | 0.78 | ¥0.513 | 2 | [Qwen](../../scenarios/knowledge/medmcqa_validation/comparison/qwen_responses.jsonl) |
| [英文 MedQA医学考试](../../scenarios/knowledge/medqa_en_test/README.md) | 100 | 准确率（%） | 83.0 | 78.0 | 62.0 | 0.80 | ¥0.765 | 0 | [Qwen](../../scenarios/knowledge/medqa_en_test/comparison/qwen_responses.jsonl) |
| [中文 MedQA医学考试](../../scenarios/knowledge/medqa_zh_test/README.md) | 100 | 准确率（%） | 89.0 | 84.0 | 63.0 | 0.78 | ¥0.516 | 0 | [Qwen](../../scenarios/knowledge/medqa_zh_test/comparison/qwen_responses.jsonl) |
| [化学物致病关系判断](../../scenarios/medication/bc5cdr_relation_oracle_entities/README.md) | 100 | 准确率（%） | 57.0 | 66.0 | 56.0 | 0.86 | ¥1.011 | 0 | [Qwen](../../scenarios/medication/bc5cdr_relation_oracle_entities/comparison/qwen_responses.jsonl) |
| [出院带药候选筛选](../../scenarios/medication/cdrugred_discharge_candidate_pipeline/README.md) | 100 | micro-F1（分） | 48.6 | 47.9 | 35.3 | 6.24 | ¥8.147 | 0 | [Qwen](../../scenarios/medication/cdrugred_discharge_candidate_pipeline/comparison/qwen_responses.jsonl) |
| [边界挑战：过敏状态](../../scenarios/medication/challenge_allergy_state/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.81 | ¥0.460 | 0 | [Qwen](../../scenarios/medication/challenge_allergy_state/comparison/qwen_responses.jsonl) |
| [边界挑战：药物剂量关联](../../scenarios/medication/challenge_dose_link/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.77 | ¥0.505 | 0 | [Qwen](../../scenarios/medication/challenge_dose_link/comparison/qwen_responses.jsonl) |
| [边界挑战：给药频次](../../scenarios/medication/challenge_frequency/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.79 | ¥0.456 | 0 | [Qwen](../../scenarios/medication/challenge_frequency/comparison/qwen_responses.jsonl) |
| [边界挑战：用药变更](../../scenarios/medication/challenge_medication_change/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.74 | ¥0.453 | 0 | [Qwen](../../scenarios/medication/challenge_medication_change/comparison/qwen_responses.jsonl) |
| [给定药物对相互作用分类](../../scenarios/medication/ddi_relation_oracle_pairs/README.md) | 150 | 准确率（%） | 79.3 | 74.7 | 66.7 | 0.79 | ¥0.700 | 0 | [Qwen](../../scenarios/medication/ddi_relation_oracle_pairs/comparison/qwen_responses.jsonl) |
| [边界挑战：影像报告断言](../../scenarios/multimodal/challenge_radiology_assertion/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 95.0 | 0.73 | ¥0.468 | 0 | [Qwen](../../scenarios/multimodal/challenge_radiology_assertion/comparison/qwen_responses.jsonl) |
| [OCR 文本医疗文档类型识别](../../scenarios/multimodal/clinocr_ocr_doctype/README.md) | 24 | 准确率（%） | 95.8 | 87.5 | 75.0 | 0.80 | ¥1.210 | 0 | [Qwen](../../scenarios/multimodal/clinocr_ocr_doctype/comparison/qwen_responses.jsonl) |
| [参考文本医疗文档类型识别](../../scenarios/multimodal/clinocr_reference_doctype/README.md) | 24 | 准确率（%） | 95.8 | 95.8 | 79.2 | 0.78 | ¥1.217 | 0 | [Qwen](../../scenarios/multimodal/clinocr_reference_doctype/comparison/qwen_responses.jsonl) |
| [ASR 转写病史字段判断](../../scenarios/multimodal/primock_asr_fields/README.md) | 37 | 准确率（%） | 91.9 | 89.2 | 89.2 | 0.74 | ¥0.774 | 0 | [Qwen](../../scenarios/multimodal/primock_asr_fields/comparison/qwen_responses.jsonl) |
| [参考转写病史字段判断](../../scenarios/multimodal/primock_reference_fields/README.md) | 37 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.83 | ¥0.882 | 0 | [Qwen](../../scenarios/multimodal/primock_reference_fields/comparison/qwen_responses.jsonl) |
| [边界挑战：病历矛盾](../../scenarios/quality/challenge_contradiction/README.md) | 20 | 准确率（%） | 100.0 | 95.0 | 70.0 | 0.73 | ¥0.446 | 0 | [Qwen](../../scenarios/quality/challenge_contradiction/comparison/qwen_responses.jsonl) |
| [边界挑战：隐私信息候选](../../scenarios/quality/challenge_phi_candidate/README.md) | 20 | 准确率（%） | 95.0 | 95.0 | 75.0 | 0.78 | ¥0.470 | 0 | [Qwen](../../scenarios/quality/challenge_phi_candidate/comparison/qwen_responses.jsonl) |
| [边界挑战：提示注入](../../scenarios/quality/challenge_prompt_injection/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 65.0 | 0.80 | ¥0.469 | 0 | [Qwen](../../scenarios/quality/challenge_prompt_injection/comparison/qwen_responses.jsonl) |
| [医疗叙述错误检出](../../scenarios/quality/medec_error_detection/README.md) | 100 | 准确率（%） | 65.0 | 60.0 | 57.0 | 0.77 | ¥1.031 | 0 | [Qwen](../../scenarios/quality/medec_error_detection/comparison/qwen_responses.jsonl) |
| [医疗叙述错误定位](../../scenarios/quality/medec_error_localization/README.md) | 100 | 准确率（%） | 72.0 | 70.0 | 57.0 | 0.77 | ¥1.206 | 0 | [Qwen](../../scenarios/quality/medec_error_localization/comparison/qwen_responses.jsonl) |
| [阿拉伯文医疗文本错误检出](../../scenarios/quality/mederrbench_ARA/README.md) | 97 | 准确率（%） | 69.1 | 59.8 | 57.7 | 0.77 | ¥0.504 | 0 | [Qwen](../../scenarios/quality/mederrbench_ARA/comparison/qwen_responses.jsonl) |
| [中文医疗文本错误检出](../../scenarios/quality/mederrbench_CN/README.md) | 100 | 准确率（%） | 73.0 | 74.0 | 58.0 | 0.84 | ¥0.529 | 0 | [Qwen](../../scenarios/quality/mederrbench_CN/comparison/qwen_responses.jsonl) |
| [英文医疗文本错误检出](../../scenarios/quality/mederrbench_EN/README.md) | 100 | 准确率（%） | 81.0 | 79.0 | 53.0 | 0.85 | ¥0.744 | 0 | [Qwen](../../scenarios/quality/mederrbench_EN/comparison/qwen_responses.jsonl) |
| [医学回答幻觉识别：有证据](../../scenarios/quality/medhallu_with_evidence/README.md) | 200 | 准确率（%） | 82.0 | 82.5 | 61.0 | 0.83 | ¥1.037 | 0 | [Qwen](../../scenarios/quality/medhallu_with_evidence/comparison/qwen_responses.jsonl) |
| [医学回答幻觉识别：无证据](../../scenarios/quality/medhallu_without_evidence/README.md) | 200 | 准确率（%） | 60.0 | 69.5 | 58.5 | 0.80 | ¥0.543 | 0 | [Qwen](../../scenarios/quality/medhallu_without_evidence/comparison/qwen_responses.jsonl) |
| [医疗有害请求筛查](../../scenarios/quality/medsafety_request_gate/README.md) | 200 | 准确率（%） | 93.5 | 96.0 | 99.0 | 0.92 | ¥0.490 | 0 | [Qwen](../../scenarios/quality/medsafety_request_gate/comparison/qwen_responses.jsonl) |
| [英文句子否定与不确定线索](../../scenarios/records/bioscope_sentence_cues/README.md) | 100 | 准确率（%） | 83.0 | 77.0 | 62.0 | 0.89 | ¥0.548 | 0 | [Qwen](../../scenarios/records/bioscope_sentence_cues/comparison/qwen_responses.jsonl) |
| [边界挑战：编码证据](../../scenarios/records/challenge_coding_evidence/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.85 | ¥0.464 | 0 | [Qwen](../../scenarios/records/challenge_coding_evidence/comparison/qwen_responses.jsonl) |
| [边界挑战：症状所属人](../../scenarios/records/challenge_experiencer/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 75.0 | 0.83 | ¥0.440 | 0 | [Qwen](../../scenarios/records/challenge_experiencer/comparison/qwen_responses.jsonl) |
| [边界挑战：中英混合文本](../../scenarios/records/challenge_mixed_language/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.79 | ¥0.430 | 0 | [Qwen](../../scenarios/records/challenge_mixed_language/comparison/qwen_responses.jsonl) |
| [边界挑战：否定状态](../../scenarios/records/challenge_negation/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.77 | ¥0.438 | 0 | [Qwen](../../scenarios/records/challenge_negation/comparison/qwen_responses.jsonl) |
| [边界挑战：相对日期](../../scenarios/records/challenge_relative_date/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 90.0 | 0.92 | ¥0.610 | 0 | [Qwen](../../scenarios/records/challenge_relative_date/comparison/qwen_responses.jsonl) |
| [边界挑战：社会背景](../../scenarios/records/challenge_social_context/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.70 | ¥0.440 | 0 | [Qwen](../../scenarios/records/challenge_social_context/comparison/qwen_responses.jsonl) |
| [边界挑战：事件时态](../../scenarios/records/challenge_temporality/README.md) | 20 | 准确率（%） | 100.0 | 75.0 | 85.0 | 0.78 | ¥0.450 | 0 | [Qwen](../../scenarios/records/challenge_temporality/comparison/qwen_responses.jsonl) |
| [中文症状肯否定状态](../../scenarios/records/imcs_assertion_oracle_span/README.md) | 100 | 准确率（%） | 79.0 | 73.0 | 64.0 | 0.95 | ¥2.313 | 0 | [Qwen](../../scenarios/records/imcs_assertion_oracle_span/comparison/qwen_responses.jsonl) |
| [中文给定实体类型识别](../../scenarios/records/imcs_entity_type_oracle_span/README.md) | 100 | 准确率（%） | 96.0 | 92.0 | 85.0 | 0.85 | ¥0.519 | 0 | [Qwen](../../scenarios/records/imcs_entity_type_oracle_span/comparison/qwen_responses.jsonl) |
| [中文词典候选实体抽取](../../scenarios/records/imcs_ner_dictionary_pipeline/README.md) | 100 | micro-F1（分） | 59.5 | 59.2 | 61.4 | 1.23 | ¥0.631 | 0 | [Qwen](../../scenarios/records/imcs_ner_dictionary_pipeline/comparison/qwen_responses.jsonl) |
| [中文症状术语归一化](../../scenarios/records/imcs_normalization_top20/README.md) | 100 | 准确率（%） | 93.0 | 92.0 | 90.0 | 0.86 | ¥0.864 | 0 | [Qwen](../../scenarios/records/imcs_normalization_top20/comparison/qwen_responses.jsonl) |
| [长病历跨文档问答](../../scenarios/records/longhealth_full_context/README.md) | 100 | 准确率（%） | 95.0 | 83.0 | 71.0 | 6.67 | ¥20.887 | 7 | [Qwen](../../scenarios/records/longhealth_full_context/comparison/qwen_responses.jsonl) |
| [医学缩写消歧](../../scenarios/records/medal_demo_disambiguation/README.md) | 100 | 准确率（%） | 67.0 | 35.0 | 5.0 | 1.05 | ¥5.661 | 52 | [Qwen](../../scenarios/records/medal_demo_disambiguation/comparison/qwen_responses.jsonl) |
| [医学实体 UMLS 语义类型](../../scenarios/records/medmentions_type_oracle_span/README.md) | 100 | 准确率（%） | 60.0 | 51.0 | 41.0 | 0.78 | ¥1.364 | 1 | [Qwen](../../scenarios/records/medmentions_type_oracle_span/comparison/qwen_responses.jsonl) |
| [给定疾病实体类别](../../scenarios/records/ncbi_disease_category_oracle_span/README.md) | 100 | 准确率（%） | 58.0 | 61.0 | 55.0 | 0.82 | ¥0.972 | 0 | [Qwen](../../scenarios/records/ncbi_disease_category_oracle_span/comparison/qwen_responses.jsonl) |
| [medspaCy 候选与 Jev 疾病实体筛选](../../scenarios/records/ncbi_medspacy_jev_ner/README.md) | 100 | micro-F1（分） | 69.4 | 68.7 | 66.9 | 3.17 | ¥3.255 | 0 | [Qwen](../../scenarios/records/ncbi_medspacy_jev_ner/comparison/qwen_responses.jsonl) |
| [西班牙文否定与不确定性](../../scenarios/records/nubes_scope_status/README.md) | 100 | 准确率（%） | 72.0 | 77.0 | 57.0 | 0.63 | ¥0.591 | 0 | [Qwen](../../scenarios/records/nubes_scope_status/comparison/qwen_responses.jsonl) |
| [边界挑战：服务路由](../../scenarios/service/challenge_service_route/README.md) | 20 | 准确率（%） | 95.0 | 100.0 | 100.0 | 0.66 | ¥0.438 | 0 | [Qwen](../../scenarios/service/challenge_service_route/comparison/qwen_responses.jsonl) |
| [边界挑战：给定规则紧急程度](../../scenarios/service/challenge_urgency_given_policy/README.md) | 20 | 准确率（%） | 100.0 | 100.0 | 100.0 | 0.70 | ¥0.483 | 0 | [Qwen](../../scenarios/service/challenge_urgency_given_policy/comparison/qwen_responses.jsonl) |
| [中文问诊对话行为分类](../../scenarios/service/imcs_dialogue_act/README.md) | 100 | 准确率（%） | 70.0 | 68.0 | 57.0 | 0.68 | ¥0.849 | 0 | [Qwen](../../scenarios/service/imcs_dialogue_act/comparison/qwen_responses.jsonl) |
| [主诉推荐就诊科室](../../scenarios/service/medjourney_departments/README.md) | 100 | micro-F1（分） | 36.9 | 34.9 | 17.1 | 12.75 | ¥17.933 | 0 | [Qwen](../../scenarios/service/medjourney_departments/comparison/qwen_responses.jsonl) |
| [MedJourney 诊断预测选择题](../../scenarios/service/medjourney_dp_mcq/README.md) | 100 | 准确率（%） | 92.0 | 91.0 | 80.0 | 0.68 | ¥0.582 | 0 | [Qwen](../../scenarios/service/medjourney_dp_mcq/comparison/qwen_responses.jsonl) |
| [MedJourney 检查预测选择题](../../scenarios/service/medjourney_ep_mcq/README.md) | 100 | 准确率（%） | 82.0 | 79.0 | 72.0 | 0.69 | ¥0.577 | 0 | [Qwen](../../scenarios/service/medjourney_ep_mcq/comparison/qwen_responses.jsonl) |
| [MedJourney 用药预测选择题](../../scenarios/service/medjourney_mp_mcq/README.md) | 100 | 准确率（%） | 86.0 | 88.0 | 80.0 | 0.67 | ¥0.550 | 0 | [Qwen](../../scenarios/service/medjourney_mp_mcq/comparison/qwen_responses.jsonl) |
| [MedJourney 治疗预测选择题](../../scenarios/service/medjourney_tp_mcq/README.md) | 100 | 准确率（%） | 83.0 | 82.0 | 66.0 | 0.66 | ¥0.617 | 0 | [Qwen](../../scenarios/service/medjourney_tp_mcq/comparison/qwen_responses.jsonl) |
| [患者问题信息需求分类](../../scenarios/service/medquad_question_type/README.md) | 100 | 准确率（%） | 96.0 | 97.0 | 88.0 | 0.68 | ¥0.581 | 0 | [Qwen](../../scenarios/service/medquad_question_type/comparison/qwen_responses.jsonl) |
| [医学伦理单选](../../scenarios/tcm/tcm_best_ethics/README.md) | 97 | 准确率（%） | 89.7 | 79.4 | 72.2 | 0.65 | ¥0.531 | 0 | [Qwen](../../scenarios/tcm/tcm_best_ethics/comparison/qwen_responses.jsonl) |
| [医学伦理与执业规范多选](../../scenarios/tcm/tcm_best_ethics_multi/README.md) | 20 | micro-F1（分） | 88.9 | 89.4 | 86.1 | 0.96 | ¥0.833 | 0 | [Qwen](../../scenarios/tcm/tcm_best_ethics_multi/comparison/qwen_responses.jsonl) |
| [中医基础知识单选](../../scenarios/tcm/tcm_best_knowledge/README.md) | 89 | 准确率（%） | 91.0 | 83.1 | 64.0 | 0.63 | ¥0.463 | 0 | [Qwen](../../scenarios/tcm/tcm_best_knowledge/comparison/qwen_responses.jsonl) |
| [中医基础知识多选](../../scenarios/tcm/tcm_best_knowledge_multi/README.md) | 20 | micro-F1（分） | 81.5 | 87.9 | 76.6 | 0.93 | ¥0.807 | 0 | [Qwen](../../scenarios/tcm/tcm_best_knowledge_multi/comparison/qwen_responses.jsonl) |
| [中医病位单选](../../scenarios/tcm/tcm_best_location/README.md) | 21 | 准确率（%） | 81.0 | 76.2 | 52.4 | 0.67 | ¥0.624 | 0 | [Qwen](../../scenarios/tcm/tcm_best_location/comparison/qwen_responses.jsonl) |
| [中医病位多选](../../scenarios/tcm/tcm_best_location_multi/README.md) | 79 | micro-F1（分） | 64.8 | 66.7 | 32.4 | 1.39 | ¥1.557 | 0 | [Qwen](../../scenarios/tcm/tcm_best_location_multi/comparison/qwen_responses.jsonl) |
| [中医病性单选](../../scenarios/tcm/tcm_best_nature/README.md) | 99 | 准确率（%） | 69.7 | 59.6 | 53.5 | 0.64 | ¥0.667 | 0 | [Qwen](../../scenarios/tcm/tcm_best_nature/comparison/qwen_responses.jsonl) |
| [中医病性与要素多选](../../scenarios/tcm/tcm_best_nature_multi/README.md) | 20 | micro-F1（分） | 85.4 | 79.1 | 76.9 | 0.86 | ¥0.918 | 0 | [Qwen](../../scenarios/tcm/tcm_best_nature_multi/comparison/qwen_responses.jsonl) |
| [中医治则治法单选](../../scenarios/tcm/tcm_best_principles/README.md) | 20 | 准确率（%） | 90.0 | 70.0 | 75.0 | 0.62 | ¥0.549 | 0 | [Qwen](../../scenarios/tcm/tcm_best_principles/comparison/qwen_responses.jsonl) |
| [中医治则治法多选](../../scenarios/tcm/tcm_best_principles_multi/README.md) | 97 | micro-F1（分） | 70.3 | 62.3 | 47.0 | 1.34 | ¥1.601 | 0 | [Qwen](../../scenarios/tcm/tcm_best_principles_multi/comparison/qwen_responses.jsonl) |
| [中医证型单选](../../scenarios/tcm/tcm_best_syndrome/README.md) | 68 | 准确率（%） | 80.9 | 72.1 | 66.2 | 0.63 | ¥0.726 | 0 | [Qwen](../../scenarios/tcm/tcm_best_syndrome/comparison/qwen_responses.jsonl) |
| [中医证型多选](../../scenarios/tcm/tcm_best_syndrome_multi/README.md) | 32 | micro-F1（分） | 52.8 | 36.7 | 26.7 | 1.33 | ¥1.623 | 0 | [Qwen](../../scenarios/tcm/tcm_best_syndrome_multi/comparison/qwen_responses.jsonl) |
| [中医安全问题标签一致性](../../scenarios/tcm/tcm_best_安全问题/README.md) | 100 | 准确率（%） | 27.0 | 29.0 | 32.0 | 0.62 | ¥0.491 | 0 | [Qwen](../../scenarios/tcm/tcm_best_安全问题/comparison/qwen_responses.jsonl) |
| [中医病历证型分类](../../scenarios/tcm/tcm_syndrome/README.md) | 100 | 准确率（%） | 33.0 | 40.0 | 36.0 | 0.87 | ¥4.004 | 1 | [Qwen](../../scenarios/tcm/tcm_syndrome/comparison/qwen_responses.jsonl) |
| [临床试验证据支持判断](../../scenarios/trials/nli4ct_entailment/README.md) | 100 | 准确率（%） | 88.0 | 87.0 | 77.0 | 0.66 | ¥1.273 | 0 | [Qwen](../../scenarios/trials/nli4ct_entailment/comparison/qwen_responses.jsonl) |
| [临床试验证据句定位](../../scenarios/trials/nli4ct_evidence/README.md) | 100 | micro-F1（分） | 49.9 | 68.3 | 22.1 | 2.50 | ¥4.525 | 0 | [Qwen](../../scenarios/trials/nli4ct_evidence/comparison/qwen_responses.jsonl) |
| [患者与临床试验入组预筛](../../scenarios/trials/trialgpt_sigir_referral/README.md) | 150 | 准确率（%） | 48.0 | 54.7 | 52.7 | 0.69 | ¥1.246 | 0 | [Qwen](../../scenarios/trials/trialgpt_sigir_referral/comparison/qwen_responses.jsonl) |

## 归档与核验

[配置](config.json) · [汇总](summary.json) · [运行阶段](sessions.jsonl) · [归档校验清单](archive_manifest.json) · [接口文档](https://docs.siliconflow.cn/docs/api/chat-completions-post)

无需密钥即可在仓库根目录核验原始回答、请求指纹、重试用量与重算得分：

```sh
python3 scripts/analyze_qwen.py --verify
```

重新运行会产生 API 费用；脚本从环境变量 `SILICONFLOW_API_KEY` 或仓库外的私有密钥文件读取凭据：

```sh
python3 scripts/compare_qwen.py
python3 scripts/analyze_qwen.py
```

本地缓存位于被 Git 忽略的 `work/qwen3.5-9b/`；脚本会跳过已有最终记录。仅恢复限流、服务器或网络失败时使用 `--retry-transport`，保留先前尝试。
