# 边界挑战：随访行动：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| followup_action:1 | {"note": "出院后一周复查血常规。"}… | 1 | 100.0% | 100.0% |
| followup_action:2 | {"note": "三个月后复查胸部CT。"}… | 1 | 100.0% | 100.0% |
| followup_action:3 | {"note": "明日上午门诊复诊。"}… | 1 | 100.0% | 100.0% |
| followup_action:4 | {"note": "昨日已完成血常规检查，未安排后续事项。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:1 | {"note": "已做门诊随访，下一步预约复查血常规。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:2 | {"note": "血常规已查完，下次安排腹部超声检查。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:3 | {"note": "血常规已完成，后天回门诊看结果。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:4 | {"note": "血常规及随访均已完成，没有后续安排。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:5 | {"note": "已做门诊随访，下一步预约复查肝功能。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:6 | {"note": "肝功能已查完，下次安排腹部超声检查。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:7 | {"note": "肝功能已完成，后天回门诊看结果。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:8 | {"note": "肝功能及随访均已完成，没有后续安排。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:9 | {"note": "已做门诊随访，下一步预约复查肾功能。"}… | 1 | 0.0% | 100.0% |
| expansion:followup_action:10 | {"note": "肾功能已查完，下次安排腹部超声检查。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:11 | {"note": "肾功能已完成，后天回门诊看结果。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:12 | {"note": "肾功能及随访均已完成，没有后续安排。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:13 | {"note": "已做门诊随访，下一步预约复查血脂。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:14 | {"note": "血脂已查完，下次安排腹部超声检查。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:15 | {"note": "血脂已完成，后天回门诊看结果。"}… | 1 | 100.0% | 100.0% |
| expansion:followup_action:16 | {"note": "血脂及随访均已完成，没有后续安排。"}… | 1 | 100.0% | 100.0% |
