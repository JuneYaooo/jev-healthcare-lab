# 边界挑战：给药频次：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| frequency:1 | {"note": "该药每12小时一次，连续用药。"}… | 1 | 100.0% | 100.0% |
| frequency:2 | {"note": "该药每日晨起服一次。"}… | 1 | 100.0% | 100.0% |
| frequency:3 | {"note": "该药每日三次。"}… | 1 | 100.0% | 100.0% |
| frequency:4 | {"note": "该药仅在症状出现时按需服用。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:1 | {"note": "药物甲每24小时一次，另一药每12小时一次。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:2 | {"note": "药物甲早晚各一次，午间不服。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:3 | {"note": "药物甲早、中、晚各一次。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:4 | {"note": "药物甲无固定次数，仅需要时按医嘱服用。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:5 | {"note": "药物乙每24小时一次，另一药每12小时一次。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:6 | {"note": "药物乙早晚各一次，午间不服。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:7 | {"note": "药物乙早、中、晚各一次。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:8 | {"note": "药物乙无固定次数，仅需要时按医嘱服用。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:9 | {"note": "药物丙每24小时一次，另一药每12小时一次。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:10 | {"note": "药物丙早晚各一次，午间不服。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:11 | {"note": "药物丙早、中、晚各一次。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:12 | {"note": "药物丙无固定次数，仅需要时按医嘱服用。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:13 | {"note": "药物丁每24小时一次，另一药每12小时一次。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:14 | {"note": "药物丁早晚各一次，午间不服。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:15 | {"note": "药物丁早、中、晚各一次。"}… | 1 | 100.0% | 100.0% |
| expansion:frequency:16 | {"note": "药物丁无固定次数，仅需要时按医嘱服用。"}… | 1 | 100.0% | 100.0% |
