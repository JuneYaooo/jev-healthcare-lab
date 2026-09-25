# 边界挑战：文书缺项：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| documentation:1 | {"note": "过敏史：无已知药物过敏。"}… | 1 | 100.0% | 100.0% |
| documentation:2 | {"note": "过敏史：待询问。"}… | 1 | 100.0% | 100.0% |
| documentation:3 | {"note": "既往体健。过敏史字段空白。"}… | 1 | 100.0% | 100.0% |
| documentation:4 | {"note": "青霉素过敏，曾出现皮疹。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:1 | {"note": "过敏史：明确否认相关情况。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:2 | {"note": "过敏史：待询问；其他病史已完成。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:3 | {"note": "过敏史栏未填写，不能用“既往体健”代替。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:4 | {"note": "过敏史已经问诊并记录为阳性。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:5 | {"note": "手术史：明确否认相关情况。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:6 | {"note": "手术史：待询问；其他病史已完成。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:7 | {"note": "手术史栏未填写，不能用“既往体健”代替。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:8 | {"note": "手术史已经问诊并记录为阳性。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:9 | {"note": "吸烟史：明确否认相关情况。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:10 | {"note": "吸烟史：待询问；其他病史已完成。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:11 | {"note": "吸烟史栏未填写，不能用“既往体健”代替。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:12 | {"note": "吸烟史已经问诊并记录为阳性。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:13 | {"note": "家族史：明确否认相关情况。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:14 | {"note": "家族史：待询问；其他病史已完成。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:15 | {"note": "家族史栏未填写，不能用“既往体健”代替。"}… | 1 | 100.0% | 100.0% |
| expansion:documentation:16 | {"note": "家族史已经问诊并记录为阳性。"}… | 1 | 100.0% | 100.0% |
