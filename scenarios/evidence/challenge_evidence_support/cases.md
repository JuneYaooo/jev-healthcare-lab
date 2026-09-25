# 边界挑战：证据支持：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| evidence_support:1 | {"note": "证据：母亲有哮喘。结论：患者本人有哮喘。"}… | 1 | 100.0% | 0.0% |
| evidence_support:2 | {"note": "证据：患者否认胸痛。结论：患者有胸痛。"}… | 1 | 100.0% | 100.0% |
| evidence_support:3 | {"note": "证据：已预约下周复查血常规。结论：存在后续检验计划。"}… | 1 | 100.0% | 100.0% |
| evidence_support:4 | {"note": "证据：CT未发现结节。结论：CT发现结节。"}… | 1 | 100.0% | 100.0% |
| expansion:evidence_support:1 | {"note": "证据：患者当前有头痛。结论：患者当前有头痛。"}… | 1 | 100.0% | 100.0% |
| expansion:evidence_support:2 | {"note": "证据：患者否认头痛。结论：患者有头痛。"}… | 1 | 100.0% | 100.0% |
| expansion:evidence_support:3 | {"note": "证据：父亲有头痛，患者未询问。结论：患者有头痛。"}… | 1 | 100.0% | 0.0% |
| expansion:evidence_support:4 | {"note": "证据：患者头痛情况未采集。结论：患者没有头痛。"}… | 1 | 100.0% | 100.0% |
| expansion:evidence_support:5 | {"note": "证据：患者当前有腹痛。结论：患者当前有腹痛。"}… | 1 | 100.0% | 100.0% |
| expansion:evidence_support:6 | {"note": "证据：患者否认腹痛。结论：患者有腹痛。"}… | 1 | 100.0% | 100.0% |
| expansion:evidence_support:7 | {"note": "证据：父亲有腹痛，患者未询问。结论：患者有腹痛。"}… | 1 | 100.0% | 0.0% |
| expansion:evidence_support:8 | {"note": "证据：患者腹痛情况未采集。结论：患者没有腹痛。"}… | 1 | 100.0% | 100.0% |
| expansion:evidence_support:9 | {"note": "证据：患者当前有咳嗽。结论：患者当前有咳嗽。"}… | 1 | 100.0% | 100.0% |
| expansion:evidence_support:10 | {"note": "证据：患者否认咳嗽。结论：患者有咳嗽。"}… | 1 | 100.0% | 100.0% |
| expansion:evidence_support:11 | {"note": "证据：父亲有咳嗽，患者未询问。结论：患者有咳嗽。"}… | 1 | 100.0% | 0.0% |
| expansion:evidence_support:12 | {"note": "证据：患者咳嗽情况未采集。结论：患者没有咳嗽。"}… | 1 | 100.0% | 100.0% |
| expansion:evidence_support:13 | {"note": "证据：患者当前有乏力。结论：患者当前有乏力。"}… | 1 | 100.0% | 100.0% |
| expansion:evidence_support:14 | {"note": "证据：患者否认乏力。结论：患者有乏力。"}… | 1 | 100.0% | 100.0% |
| expansion:evidence_support:15 | {"note": "证据：父亲有乏力，患者未询问。结论：患者有乏力。"}… | 1 | 100.0% | 0.0% |
| expansion:evidence_support:16 | {"note": "证据：患者乏力情况未采集。结论：患者没有乏力。"}… | 1 | 100.0% | 100.0% |
