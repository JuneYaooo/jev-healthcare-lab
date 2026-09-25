# 边界挑战：中英混合文本：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| mixed_language:1 | {"note": "患者 denies chest pain，咳嗽持续。"}… | 1 | 100.0% | 100.0% |
| mixed_language:2 | {"note": "No chest pain at present."}… | 1 | 100.0% | 100.0% |
| mixed_language:3 | {"note": "Current chest pain for 2 hours."}… | 1 | 100.0% | 100.0% |
| mixed_language:4 | {"note": "Chest pain? 尚未回答。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:1 | {"note": "患者 denies headache，仍有其他不适。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:2 | {"note": "Current headache，就诊时仍未缓解。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:3 | {"note": "headache? 该问题尚未作答。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:4 | {"note": "No headache now，昨日症状已消失。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:5 | {"note": "患者 denies nausea，仍有其他不适。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:6 | {"note": "Current nausea，就诊时仍未缓解。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:7 | {"note": "nausea? 该问题尚未作答。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:8 | {"note": "No nausea now，昨日症状已消失。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:9 | {"note": "患者 denies cough，仍有其他不适。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:10 | {"note": "Current cough，就诊时仍未缓解。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:11 | {"note": "cough? 该问题尚未作答。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:12 | {"note": "No cough now，昨日症状已消失。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:13 | {"note": "患者 denies abdominal pain，仍有其他不适。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:14 | {"note": "Current abdominal pain，就诊时仍未缓解。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:15 | {"note": "abdominal pain? 该问题尚未作答。"}… | 1 | 100.0% | 100.0% |
| expansion:mixed_language:16 | {"note": "No abdominal pain now，昨日症状已消失。"}… | 1 | 100.0% | 100.0% |
