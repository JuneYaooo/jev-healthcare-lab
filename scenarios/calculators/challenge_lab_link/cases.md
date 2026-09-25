# 边界挑战：检验数值关联：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| lab_link:1 | {"note": "本次空腹血糖5.6 mmol/L，餐后血糖7.8 mmol/L。"}… | 1 | 100.0% | 100.0% |
| lab_link:2 | {"note": "本次空腹血糖7.8 mmol/L，上次5.6 mmol/L。"}… | 1 | 100.0% | 100.0% |
| lab_link:3 | {"note": "仅测餐后血糖12.0 mmol/L，未测空腹值。"}… | 1 | 100.0% | 100.0% |
| lab_link:4 | {"note": "空腹血糖12.0 mmol/L，另一个项目值为5.6。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:1 | {"note": "上次血钠140 mmol/L；本次血钠135 mmol/L。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:2 | {"note": "上次血钠145 mmol/L；本次血钠140 mmol/L。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:3 | {"note": "上次血钠135 mmol/L；本次血钠145 mmol/L。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:4 | {"note": "上次血钠140 mmol/L；本次血钠标本未检测。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:5 | {"note": "上次血钾4.0 mmol/L；本次血钾3.5 mmol/L。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:6 | {"note": "上次血钾5.0 mmol/L；本次血钾4.0 mmol/L。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:7 | {"note": "上次血钾3.5 mmol/L；本次血钾5.0 mmol/L。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:8 | {"note": "上次血钾4.0 mmol/L；本次血钾标本未检测。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:9 | {"note": "上次血红蛋白120 g/L；本次血红蛋白100 g/L。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:10 | {"note": "上次血红蛋白140 g/L；本次血红蛋白120 g/L。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:11 | {"note": "上次血红蛋白100 g/L；本次血红蛋白140 g/L。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:12 | {"note": "上次血红蛋白120 g/L；本次血红蛋白标本未检测。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:13 | {"note": "上次肌酐90 μmol/L；本次肌酐60 μmol/L。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:14 | {"note": "上次肌酐120 μmol/L；本次肌酐90 μmol/L。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:15 | {"note": "上次肌酐60 μmol/L；本次肌酐120 μmol/L。"}… | 1 | 100.0% | 100.0% |
| expansion:lab_link:16 | {"note": "上次肌酐90 μmol/L；本次肌酐标本未检测。"}… | 1 | 100.0% | 100.0% |
