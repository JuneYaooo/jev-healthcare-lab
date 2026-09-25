# 边界挑战：单位等价：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| unit_equivalence:1 | {"note": "记录A为0.5g，记录B为500mg。"}… | 1 | 100.0% | 100.0% |
| unit_equivalence:2 | {"note": "记录A为0.5mg，记录B为500mg。"}… | 1 | 100.0% | 100.0% |
| unit_equivalence:3 | {"note": "记录A为250μg，记录B为0.25mg。"}… | 1 | 100.0% | 100.0% |
| unit_equivalence:4 | {"note": "记录A为5mg，记录B为0.5mg。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:1 | {"note": "记录A为25mg，记录B为0.025g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:2 | {"note": "记录A为50mg，记录B为0.5g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:3 | {"note": "记录A为75mg，记录B为0.075g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:4 | {"note": "记录A为100mg，记录B为1g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:5 | {"note": "记录A为125mg，记录B为0.125g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:6 | {"note": "记录A为150mg，记录B为1.5g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:7 | {"note": "记录A为175mg，记录B为0.175g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:8 | {"note": "记录A为200mg，记录B为2g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:9 | {"note": "记录A为225mg，记录B为0.225g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:10 | {"note": "记录A为250mg，记录B为2.5g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:11 | {"note": "记录A为275mg，记录B为0.275g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:12 | {"note": "记录A为300mg，记录B为3g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:13 | {"note": "记录A为325mg，记录B为0.325g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:14 | {"note": "记录A为350mg，记录B为3.5g。"}… | 1 | 0.0% | 100.0% |
| expansion:unit_equivalence:15 | {"note": "记录A为375mg，记录B为0.375g。"}… | 1 | 100.0% | 100.0% |
| expansion:unit_equivalence:16 | {"note": "记录A为400mg，记录B为4g。"}… | 1 | 100.0% | 100.0% |
