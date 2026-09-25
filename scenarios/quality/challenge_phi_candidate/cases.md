# 边界挑战：隐私信息候选：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| phi_candidate:1 | {"note": "虚构患者姓名：[张测试]。"}… | 1 | 100.0% | 100.0% |
| phi_candidate:2 | {"note": "虚构住院号：[TEST-000123]。"}… | 1 | 100.0% | 100.0% |
| phi_candidate:3 | {"note": "血压为[120/80]mmHg。"}… | 1 | 100.0% | 100.0% |
| phi_candidate:4 | {"note": "检验结果：[阴性]。"}… | 1 | 0.0% | 0.0% |
| expansion:phi_candidate:1 | {"note": "虚构姓名：[测试患者A]，就诊号另列。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:2 | {"note": "合成病例号：[DEMO-410]，不是化验值。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:3 | {"note": "检验浓度：[2.5] mmol/L，未出现身份信息。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:4 | {"note": "流程状态：[待报告]。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:5 | {"note": "虚构姓名：[测试患者B]，就诊号另列。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:6 | {"note": "合成病例号：[DEMO-411]，不是化验值。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:7 | {"note": "检验浓度：[3.5] mmol/L，未出现身份信息。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:8 | {"note": "流程状态：[已签收]。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:9 | {"note": "虚构姓名：[测试患者C]，就诊号另列。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:10 | {"note": "合成病例号：[DEMO-412]，不是化验值。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:11 | {"note": "检验浓度：[4.5] mmol/L，未出现身份信息。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:12 | {"note": "流程状态：[已复核]。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:13 | {"note": "虚构姓名：[测试患者D]，就诊号另列。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:14 | {"note": "合成病例号：[DEMO-413]，不是化验值。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:15 | {"note": "检验浓度：[5.5] mmol/L，未出现身份信息。"}… | 1 | 100.0% | 100.0% |
| expansion:phi_candidate:16 | {"note": "流程状态：[未预约]。"}… | 1 | 100.0% | 100.0% |
