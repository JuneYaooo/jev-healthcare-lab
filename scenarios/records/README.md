# 病历实体、否定状态与术语标准化

**18 个任务条件，1,128 条主评测记录。** [全部场景](../../README.md)

给定实体边界的类型分类与端到端抽取分开看；LongHealth 为 20 个虚构患者的 100 个问题。

| 任务（点击查看完整方法与数据） | 类型 | 记录数 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [中文症状肯否定状态](imcs_assertion_oracle_span/README.md) | 数据适配 | 100 | Accuracy | 79.0% |
| [中文给定实体类型识别](imcs_entity_type_oracle_span/README.md) | 数据适配 | 100 | Accuracy | 96.0% |
| [中文词典候选实体抽取](imcs_ner_dictionary_pipeline/README.md) | 数据适配 | 100 | micro-F1 | 59.5% |
| [中文症状术语归一化](imcs_normalization_top20/README.md) | 数据适配 | 100 | Accuracy | 93.0% |
| [英文句子否定与不确定线索](bioscope_sentence_cues/README.md) | 数据适配 | 100 | Accuracy | 83.0% |
| [西班牙文否定与不确定性](nubes_scope_status/README.md) | 数据适配 | 100 | Accuracy | 72.0% |
| [给定疾病实体类别](ncbi_disease_category_oracle_span/README.md) | 数据适配 | 100 | Accuracy | 58.0% |
| [medspaCy 候选与 Jev 疾病实体筛选](ncbi_medspacy_jev_ner/README.md) | 数据适配 | 100 | micro-F1 | 69.4% |
| [医学实体 UMLS 语义类型](medmentions_type_oracle_span/README.md) | 数据适配 | 100 | Accuracy | 60.0% |
| [医学缩写消歧](medal_demo_disambiguation/README.md) | 数据适配 | 100 | Accuracy | 67.0% |
| [长病历跨文档问答](longhealth_full_context/README.md) | 数据适配 | 100 | Accuracy | 95.0% |
| [边界挑战：编码证据](challenge_coding_evidence/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
| [边界挑战：症状所属人](challenge_experiencer/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
| [边界挑战：中英混合文本](challenge_mixed_language/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
| [边界挑战：否定状态](challenge_negation/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
| [边界挑战：相对日期](challenge_relative_date/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
| [边界挑战：社会背景](challenge_social_context/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
| [边界挑战：事件时态](challenge_temporality/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
