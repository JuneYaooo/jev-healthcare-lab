# 三类医疗工作的新增案例对照

新增 140 份材料、1,400 个不同判断：60 篇临床试验摘要、40 段中文问诊、40 组医学主张与文献。与此前 20 篇摘要没有材料重合；主评测 96 项任务的统计单独保留。每种配置测两轮。

| 医疗工作（材料数） | 每次判断数 | 正确率：Jev / DeepSeek | 整批总耗时：Jev / DeepSeek | 每千项判断费用：Jev / DeepSeek |
| --- | ---: | ---: | ---: | ---: |
| [临床试验摘要整理（60）](../../scenarios/evidence/pubmed_rct_section/paired-expanded/README.md) | 1 | 84.9% / 86.7% | 41.4 / 99.2 秒 | $0.040 / $0.077 |
| [临床试验摘要整理（60）](../../scenarios/evidence/pubmed_rct_section/paired-expanded/README.md) | 5 | 84.8% / 84.5% | 8.9 / 21.1 秒 | $0.012 / $0.018 |
| [临床试验摘要整理（60）](../../scenarios/evidence/pubmed_rct_section/paired-expanded/README.md) | 10 | 84.6% / 85.4% | 5.1 / 12.5 秒 | $0.008 / $0.012 |
| [中文问诊内容归类（40）](../../scenarios/service/imcs_dialogue_act/paired-expanded/README.md) | 1 | 73.9% / 72.4% | 30.5 / 65.9 秒 | $0.075 / $0.093 |
| [中文问诊内容归类（40）](../../scenarios/service/imcs_dialogue_act/paired-expanded/README.md) | 5 | 73.4% / 70.6% | 21.1 / 16.7 秒 | $0.029 / $0.036 |
| [中文问诊内容归类（40）](../../scenarios/service/imcs_dialogue_act/paired-expanded/README.md) | 10 | 73.8% / 71.0% | 4.9 / 9.7 秒 | $0.023 / $0.024 |
| [医学文献证据句筛选（40）](../../scenarios/evidence/scifact_cited_abstract/paired-expanded/README.md) | 1 | 87.8% / 80.4% | 32.6 / 82.0 秒 | $0.047 / $0.093 |
| [医学文献证据句筛选（40）](../../scenarios/evidence/scifact_cited_abstract/paired-expanded/README.md) | 5 | 87.5% / 86.8% | 6.1 / 14.5 秒 | $0.013 / $0.022 |
| [医学文献证据句筛选（40）](../../scenarios/evidence/scifact_cited_abstract/paired-expanded/README.md) | 10 | 88.0% / 88.1% | 18.8 / 8.1 秒 | $0.008 / $0.016 |

总耗时按本场景整批材料计，两轮取平均；每家同时处理 4 份材料，每份内部依次请求。每份均有相同的 10 个问题：每次 1 项调用 10 次，每次 5 项调用 2 次，每次 10 项调用 1 次。单项配置仍传完整上下文，因此不代表孤立短句调用的最低成本。

正确率、成本均计入全部输入，缺失答案算错，失败重试耗时不剔除。费用包括有用量的重试。缓存未控制，重复轮次可能使 DeepSeek 更便宜；各场景明细提供分轮费用与命中率。证据筛选还需结合子页中的查准率、召回率及 F1 判断，不能只看正确率。

这些任务评估内容整理和证据筛选，不能据此判断诊疗决策能力。每个场景的完整案例、提示词、原答案、原始响应、选择范围和逐案例对比均在对应目录。

[首次 20 篇摘要对照](../../scenarios/evidence/pubmed_rct_section/paired-new/README.md) · [实验清单](manifest.json) · [汇总数据](summary.json)
