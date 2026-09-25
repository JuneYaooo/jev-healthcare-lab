# 边界挑战：症状所属人：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| experiencer:1 | {"note": "母亲患糖尿病多年。患者无糖尿病史。"}… | 1 | 100.0% | 100.0% |
| experiencer:2 | {"note": "患者糖尿病5年，父母身体健康。"}… | 1 | 100.0% | 100.0% |
| experiencer:3 | {"note": "否认本人及家属糖尿病史。"}… | 1 | 100.0% | 100.0% |
| experiencer:4 | {"note": "入院记录：糖尿病史5年，未注明该条描述的是患者还是陪诊者。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:1 | {"note": "父亲患哮喘；患者明确否认该病。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:2 | {"note": "患者确诊哮喘，母亲无该病。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:3 | {"note": "患者和家人均明确否认哮喘。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:4 | {"note": "便签记有哮喘病史，未标明对应本人还是家属。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:5 | {"note": "父亲患高血压；患者明确否认该病。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:6 | {"note": "患者确诊高血压，母亲无该病。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:7 | {"note": "患者和家人均明确否认高血压。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:8 | {"note": "便签记有高血压病史，未标明对应本人还是家属。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:9 | {"note": "父亲患偏头痛；患者明确否认该病。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:10 | {"note": "患者确诊偏头痛，母亲无该病。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:11 | {"note": "患者和家人均明确否认偏头痛。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:12 | {"note": "便签记有偏头痛病史，未标明对应本人还是家属。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:13 | {"note": "父亲患甲状腺疾病；患者明确否认该病。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:14 | {"note": "患者确诊甲状腺疾病，母亲无该病。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:15 | {"note": "患者和家人均明确否认甲状腺疾病。"}… | 1 | 100.0% | 100.0% |
| expansion:experiencer:16 | {"note": "便签记有甲状腺疾病病史，未标明对应本人还是家属。"}… | 1 | 100.0% | 100.0% |
