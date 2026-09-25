# 边界挑战：药物剂量关联：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| dose_link:1 | {"note": "阿莫西林每次500mg，维生素C每次250mg。"}… | 1 | 100.0% | 100.0% |
| dose_link:2 | {"note": "阿莫西林每次250mg。另有其他药物500mg。"}… | 1 | 100.0% | 100.0% |
| dose_link:3 | {"note": "阿莫西林每次1g。"}… | 1 | 100.0% | 100.0% |
| dose_link:4 | {"note": "阿莫西林每日三次，未记录每次剂量。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:1 | {"note": "药物甲每次250mg，另一药每次500mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:2 | {"note": "另一药每天总量1g；药物甲每次500mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:3 | {"note": "药物甲每次1g，另一药每次250mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:4 | {"note": "药物甲每日两次，单次剂量空白；另一药500mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:5 | {"note": "药物乙每次250mg，另一药每次500mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:6 | {"note": "另一药每天总量1g；药物乙每次500mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:7 | {"note": "药物乙每次1g，另一药每次250mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:8 | {"note": "药物乙每日两次，单次剂量空白；另一药500mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:9 | {"note": "药物丙每次250mg，另一药每次500mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:10 | {"note": "另一药每天总量1g；药物丙每次500mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:11 | {"note": "药物丙每次1g，另一药每次250mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:12 | {"note": "药物丙每日两次，单次剂量空白；另一药500mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:13 | {"note": "药物丁每次250mg，另一药每次500mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:14 | {"note": "另一药每天总量1g；药物丁每次500mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:15 | {"note": "药物丁每次1g，另一药每次250mg。"}… | 1 | 100.0% | 100.0% |
| expansion:dose_link:16 | {"note": "药物丁每日两次，单次剂量空白；另一药500mg。"}… | 1 | 100.0% | 100.0% |
