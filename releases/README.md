# 医疗决策数据集下载

每个包都含整理后的题目、独立答案、无答案请求、逐题溯源索引、原许可与引用，以及离线校验/评分工具。解压即可使用，Python 3.10+，无第三方依赖。

| 数据包 | 题数 | 使用范围 |
| --- | ---: | --- |
| [jev-medical-decision-v0.5.0-open.zip](jev-medical-decision-v0.5.0-open.zip) | 3,667 | 开放许可核心集；遵循各来源署名及相同方式共享等条件 |
| [jev-medical-decision-v0.5.0-research-noncommercial.zip](jev-medical-decision-v0.5.0-research-noncommercial.zip) | 1,543 | 非商业研究附加集；不得按开放核心许可混用 |

[校验和](SHA256SUMS) · [场景与任务](../benchmarks/medical_decision_v1/README.md) · [全部来源登记](../benchmarks/medical_decision_v1/SOURCES.md)

两个包互不重复；共同使用时仍分别遵守原许可。开放核心集可独立运行，不依赖非商业附加集。数据为评测子集，实际训练会影响后续同题对比。

重建：`python3 scripts/medical_decision_release.py build`。压缩包按固定顺序和时间戳生成，可重复校验字节一致性。
