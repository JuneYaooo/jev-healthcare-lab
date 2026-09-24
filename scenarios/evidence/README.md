# 循证研究、PICO 与公共卫生核查

**10 个任务条件，859 条主评测记录。** [全部场景](../../README.md)

提供证据的判断不能替代检索评价；固定窗口分类与原始序列抽取指标不同。

| 任务（点击查看方法与费用） | 任务类型 | 记录数 | 指标 | Jev | DeepSeek |
| --- | --- | ---: | --- | ---: | ---: |
| [PICO 固定窗口识别](ebm_pico_fixed_windows/README.md) | PICO 多标签识别 | 100 | micro-F1 | 12.7% | 25.4% |
| [临床研究干预结果方向](evidence_inference_fulltext/README.md) | 干预效果方向分类 | 100 | Accuracy | 89.0% | 76.0% |
| [研究结局固定窗口分类](evidenceoutcomes_fixed_window/README.md) | 研究结局识别 | 100 | Accuracy | 88.0% | 67.0% |
| [全文证据句筛选](evidencebench_sentence_selection/README.md) | 证据句筛选 | 37 | micro-F1 | 29.4% | 25.9% |
| [摘要支持的研究问题回答](pubmedqa_evidence_qa/README.md) | 证据问答 | 100 | Accuracy | 74.0% | 76.0% |
| [RCT 摘要句功能分类](pubmed_rct_section/README.md) | 章节分类 | 100 | Accuracy | 75.0% | 77.0% |
| [科学论断与给定摘要一致性](scifact_cited_abstract/README.md) | 文本蕴含判断 | 118 | Accuracy | 85.6% | 89.0% |
| [公共卫生核查：仅论断](pubhealth_claim_only/README.md) | 事实核查分类 | 100 | Accuracy | 20.0% | 44.0% |
| [公共卫生核查：提供核查文章](pubhealth_with_article/README.md) | 事实核查分类 | 100 | Accuracy | 67.0% | 72.0% |
| [边界挑战：证据支持](challenge_evidence_support/README.md) | 证据支持判断 | 4 | Accuracy | 100.0% | 75.0% |
