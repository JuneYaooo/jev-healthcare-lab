# 边界挑战：相对日期：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| relative_date:1 | {"note": "明天复诊。"}… | 1 | 100.0% | 100.0% |
| relative_date:2 | {"note": "三天后复诊。"}… | 1 | 100.0% | 100.0% |
| relative_date:3 | {"note": "一周后复诊。"}… | 1 | 100.0% | 100.0% |
| relative_date:4 | {"note": "症状加重时复诊，未约定日期。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:1 | {"note": "复诊安排：明天。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:2 | {"note": "复诊安排：三天后。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:3 | {"note": "复诊安排：一周后。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:4 | {"note": "复诊安排：症状变化时，未预约具体日期。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:5 | {"note": "复诊安排：明天。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:6 | {"note": "复诊安排：三天后。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:7 | {"note": "复诊安排：一周后。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:8 | {"note": "复诊安排：症状变化时，未预约具体日期。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:9 | {"note": "复诊安排：明天。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:10 | {"note": "复诊安排：三天后。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:11 | {"note": "复诊安排：一周后。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:12 | {"note": "复诊安排：症状变化时，未预约具体日期。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:13 | {"note": "复诊安排：明天。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:14 | {"note": "复诊安排：三天后。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:15 | {"note": "复诊安排：一周后。"}… | 1 | 100.0% | 100.0% |
| expansion:relative_date:16 | {"note": "复诊安排：症状变化时，未预约具体日期。"}… | 1 | 100.0% | 100.0% |
