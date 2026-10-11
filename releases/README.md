# 医疗决策数据集下载

每个包都含整理后的题目、独立答案、无答案请求、逐题溯源索引、原许可与引用，以及离线校验/评分工具。解压即可使用，Python 3.10+，无第三方依赖。

| 数据包 | 题数 | 使用范围 |
| --- | ---: | --- |
| [临床主评测 · 开放许可](jev-medical-decision-clinical-open.zip) | 1,284 | 遵循各来源署名及相同方式共享等条件 |
| [临床主评测 · 非商业附加](jev-medical-decision-clinical-research-noncommercial.zip) | 230 | 保留非商业等限制 |
| [辅助评测 · 开放许可](jev-medical-decision-auxiliary-open.zip) | 2,950 | 遵循各来源署名及相同方式共享等条件 |
| [辅助评测 · 非商业附加](jev-medical-decision-auxiliary-research-noncommercial.zip) | 1,343 | 保留非商业等限制 |

[校验和](SHA256SUMS) · [场景与任务](../benchmarks/medical_decision_v1/README.md) · [全部来源登记](../benchmarks/medical_decision_v1/SOURCES.md)

四个包互不重复；临床与辅助分开计分，暂停任务不打包。每个范围的开放包可独立使用，非商业附加包保留原限制；共同使用时仍分别遵守原许可。数据为评测子集，实际训练会影响后续同题对比。

重建：`python3 scripts/medical_decision_release.py build`。压缩包按固定顺序和时间戳生成，可重复校验字节一致性。
