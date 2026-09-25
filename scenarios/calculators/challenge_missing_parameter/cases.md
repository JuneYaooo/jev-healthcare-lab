# 边界挑战：缺失计算参数：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| missing_parameter:1 | {"note": "体重60kg，身高1.70m。"}… | 1 | 100.0% | 100.0% |
| missing_parameter:2 | {"note": "身高1.70m，体重未记录。"}… | 1 | 100.0% | 100.0% |
| missing_parameter:3 | {"note": "同次测量体重一处记60kg、一处记90kg，无更正说明；身高1.70m。"}… | 1 | 100.0% | 100.0% |
| missing_parameter:4 | {"note": "体重60000g，身高170cm。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:1 | {"note": "同次测量体重50kg、身高150cm。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:2 | {"note": "体重51kg，身高缺失。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:3 | {"note": "同次测量体重52kg与72kg两种记录，未更正；身高152cm。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:4 | {"note": "同次测量体重53000g、身高1.53m。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:5 | {"note": "同次测量体重54kg、身高154cm。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:6 | {"note": "体重55kg，身高缺失。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:7 | {"note": "同次测量体重56kg与76kg两种记录，未更正；身高156cm。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:8 | {"note": "同次测量体重57000g、身高1.57m。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:9 | {"note": "同次测量体重58kg、身高158cm。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:10 | {"note": "体重59kg，身高缺失。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:11 | {"note": "同次测量体重60kg与80kg两种记录，未更正；身高160cm。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:12 | {"note": "同次测量体重61000g、身高1.61m。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:13 | {"note": "同次测量体重62kg、身高162cm。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:14 | {"note": "体重63kg，身高缺失。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:15 | {"note": "同次测量体重64kg与84kg两种记录，未更正；身高164cm。"}… | 1 | 100.0% | 100.0% |
| expansion:missing_parameter:16 | {"note": "同次测量体重65000g、身高1.65m。"}… | 1 | 100.0% | 100.0% |
