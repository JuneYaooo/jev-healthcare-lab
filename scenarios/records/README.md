# 病历实体、否定状态与术语标准化

**18 个任务条件，1,128 条主评测记录。** [全部场景](../../README.md)

给定实体边界的类型分类与端到端抽取分开看；LongHealth 为 20 个虚构患者的 100 个问题。

| 任务（点击查看方法与费用） | 任务类型 | 记录数 | 指标 | Jev | DeepSeek |
| --- | --- | ---: | --- | ---: | ---: |
| [中文症状肯否定状态](imcs_assertion_oracle_span/README.md) | 实体状态分类 | 100 | Accuracy | 79.0% | 73.0% |
| [中文给定实体类型识别](imcs_entity_type_oracle_span/README.md) | 实体类型分类 | 100 | Accuracy | 96.0% | 92.0% |
| [中文词典候选实体抽取](imcs_ner_dictionary_pipeline/README.md) | 实体抽取与筛选 | 100 | micro-F1 | 59.5% | 59.2% |
| [中文症状术语归一化](imcs_normalization_top20/README.md) | 术语归一化 | 100 | Accuracy | 93.0% | 92.0% |
| [英文句子否定与不确定线索](bioscope_sentence_cues/README.md) | 句子线索分类 | 100 | Accuracy | 83.0% | 77.0% |
| [西班牙文否定与不确定性](nubes_scope_status/README.md) | 实体状态分类 | 100 | Accuracy | 72.0% | 77.0% |
| [给定疾病实体类别](ncbi_disease_category_oracle_span/README.md) | 实体类型分类 | 100 | Accuracy | 58.0% | 61.0% |
| [medspaCy 候选与 Jev 疾病实体筛选](ncbi_medspacy_jev_ner/README.md) | 实体抽取与筛选 | 100 | micro-F1 | 69.4% | 68.7% |
| [医学实体 UMLS 语义类型](medmentions_type_oracle_span/README.md) | 实体类型分类 | 100 | Accuracy | 60.0% | 51.0% |
| [医学缩写消歧](medal_demo_disambiguation/README.md) | 缩写消歧 | 100 | Accuracy | 67.0% | 35.0% |
| [长病历跨文档问答](longhealth_full_context/README.md) | 证据问答 | 100 | Accuracy | 95.0% | 83.0% |
| [边界挑战：编码证据](challenge_coding_evidence/README.md) | 编码证据判断 | 4 | Accuracy | 100.0% | 100.0% |
| [边界挑战：症状所属人](challenge_experiencer/README.md) | 主体归属判断 | 4 | Accuracy | 100.0% | 100.0% |
| [边界挑战：中英混合文本](challenge_mixed_language/README.md) | 跨语言语义判断 | 4 | Accuracy | 100.0% | 100.0% |
| [边界挑战：否定状态](challenge_negation/README.md) | 否定识别 | 4 | Accuracy | 100.0% | 100.0% |
| [边界挑战：相对日期](challenge_relative_date/README.md) | 相对时间解析 | 4 | Accuracy | 100.0% | 100.0% |
| [边界挑战：社会背景](challenge_social_context/README.md) | 社会背景识别 | 4 | Accuracy | 100.0% | 100.0% |
| [边界挑战：事件时态](challenge_temporality/README.md) | 事件时态判断 | 4 | Accuracy | 100.0% | 75.0% |
