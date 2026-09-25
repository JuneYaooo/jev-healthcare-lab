# 边界挑战：编码证据：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| coding_evidence:1 | {"note": "出院诊断：2型糖尿病。"}… | 1 | 100.0% | 100.0% |
| coding_evidence:2 | {"note": "糖尿病待排，尚未确诊。"}… | 1 | 100.0% | 100.0% |
| coding_evidence:3 | {"note": "已排除糖尿病。"}… | 1 | 100.0% | 100.0% |
| coding_evidence:4 | {"note": "母亲患糖尿病，患者本次血糖偏高，未下诊断。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:1 | {"note": "出院诊断写明哮喘，已确诊。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:2 | {"note": "哮喘待排，尚无确定诊断。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:3 | {"note": "医生已明确排除哮喘。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:4 | {"note": "家属患哮喘；患者相关检查异常，但尚未诊断。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:5 | {"note": "出院诊断写明高血压，已确诊。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:6 | {"note": "高血压待排，尚无确定诊断。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:7 | {"note": "医生已明确排除高血压。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:8 | {"note": "家属患高血压；患者相关检查异常，但尚未诊断。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:9 | {"note": "出院诊断写明偏头痛，已确诊。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:10 | {"note": "偏头痛待排，尚无确定诊断。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:11 | {"note": "医生已明确排除偏头痛。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:12 | {"note": "家属患偏头痛；患者相关检查异常，但尚未诊断。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:13 | {"note": "出院诊断写明甲状腺疾病，已确诊。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:14 | {"note": "甲状腺疾病待排，尚无确定诊断。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:15 | {"note": "医生已明确排除甲状腺疾病。"}… | 1 | 100.0% | 100.0% |
| expansion:coding_evidence:16 | {"note": "家属患甲状腺疾病；患者相关检查异常，但尚未诊断。"}… | 1 | 100.0% | 100.0% |
