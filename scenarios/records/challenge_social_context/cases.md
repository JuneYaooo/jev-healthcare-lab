# 边界挑战：社会背景：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| social_context:1 | {"note": "患者每天吸烟10支，尚未戒烟。"}… | 1 | 100.0% | 100.0% |
| social_context:2 | {"note": "吸烟20年，三年前已戒烟，至今未复吸。"}… | 1 | 100.0% | 100.0% |
| social_context:3 | {"note": "患者从不吸烟，丈夫吸烟。"}… | 1 | 100.0% | 100.0% |
| social_context:4 | {"note": "吸烟史未询问。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:1 | {"note": "术前访谈：每天仍吸烟，尚未戒掉。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:2 | {"note": "术前访谈：以前每天吸烟，已完全戒除且没有复吸。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:3 | {"note": "术前访谈：本人一生未吸烟。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:4 | {"note": "术前访谈：只记录父亲吸烟，本人的吸烟情况未询问。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:5 | {"note": "出院核对：每天仍吸烟，尚未戒掉。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:6 | {"note": "出院核对：以前每天吸烟，已完全戒除且没有复吸。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:7 | {"note": "出院核对：本人一生未吸烟。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:8 | {"note": "出院核对：只记录父亲吸烟，本人的吸烟情况未询问。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:9 | {"note": "门诊随访：每天仍吸烟，尚未戒掉。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:10 | {"note": "门诊随访：以前每天吸烟，已完全戒除且没有复吸。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:11 | {"note": "门诊随访：本人一生未吸烟。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:12 | {"note": "门诊随访：只记录父亲吸烟，本人的吸烟情况未询问。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:13 | {"note": "入院问诊：每天仍吸烟，尚未戒掉。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:14 | {"note": "入院问诊：以前每天吸烟，已完全戒除且没有复吸。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:15 | {"note": "入院问诊：本人一生未吸烟。"}… | 1 | 100.0% | 100.0% |
| expansion:social_context:16 | {"note": "入院问诊：只记录父亲吸烟，本人的吸烟情况未询问。"}… | 1 | 100.0% | 100.0% |
