# 边界挑战：给定规则紧急程度：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| urgency_given_policy:1 | {"note": "我当前无法呼吸。"}… | 1 | 100.0% | 100.0% |
| urgency_given_policy:2 | {"note": "去年有过呼吸困难，如今已无症状。"}… | 1 | 100.0% | 100.0% |
| urgency_given_policy:3 | {"note": "只是想询问检查费用。"}… | 1 | 100.0% | 100.0% |
| urgency_given_policy:4 | {"note": "我现在无法呼吸，能不能先等明天？"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:1 | {"note": "患者明确说：我当前无法呼吸。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:2 | {"note": "过去曾无法呼吸，如今已经恢复。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:3 | {"note": "患者只询问账单，其他情况没有描述。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:4 | {"note": "家属确认患者当前无法呼吸，询问能否等明天。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:5 | {"note": "患者明确说：我当前无法吞咽。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:6 | {"note": "过去曾无法吞咽，如今已经恢复。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:7 | {"note": "患者只询问账单，其他情况没有描述。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:8 | {"note": "家属确认患者当前无法吞咽，询问能否等明天。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:9 | {"note": "患者明确说：我当前无法站立。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:10 | {"note": "过去曾无法站立，如今已经恢复。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:11 | {"note": "患者只询问账单，其他情况没有描述。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:12 | {"note": "家属确认患者当前无法站立，询问能否等明天。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:13 | {"note": "患者明确说：我当前无法睁眼。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:14 | {"note": "过去曾无法睁眼，如今已经恢复。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:15 | {"note": "患者只询问账单，其他情况没有描述。"}… | 1 | 100.0% | 100.0% |
| expansion:urgency_given_policy:16 | {"note": "家属确认患者当前无法睁眼，询问能否等明天。"}… | 1 | 100.0% | 100.0% |
