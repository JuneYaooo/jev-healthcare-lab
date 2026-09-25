# 边界挑战：过敏状态：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| allergy_state:1 | {"note": "已确认青霉素过敏。"}… | 1 | 100.0% | 100.0% |
| allergy_state:2 | {"note": "否认青霉素过敏。"}… | 1 | 100.0% | 100.0% |
| allergy_state:3 | {"note": "疑似青霉素过敏，等待进一步核查。"}… | 1 | 100.0% | 100.0% |
| allergy_state:4 | {"note": "使用过青霉素，未记录是否过敏。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:1 | {"note": "过敏史核查已确认药物甲过敏，曾有皮疹。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:2 | {"note": "患者明确否认药物甲过敏；对另一药过敏。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:3 | {"note": "皮疹疑与药物甲有关，待进一步核实。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:4 | {"note": "既往曾用药物甲，过敏情况一栏空白。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:5 | {"note": "过敏史核查已确认药物乙过敏，曾有皮疹。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:6 | {"note": "患者明确否认药物乙过敏；对另一药过敏。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:7 | {"note": "皮疹疑与药物乙有关，待进一步核实。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:8 | {"note": "既往曾用药物乙，过敏情况一栏空白。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:9 | {"note": "过敏史核查已确认药物丙过敏，曾有皮疹。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:10 | {"note": "患者明确否认药物丙过敏；对另一药过敏。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:11 | {"note": "皮疹疑与药物丙有关，待进一步核实。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:12 | {"note": "既往曾用药物丙，过敏情况一栏空白。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:13 | {"note": "过敏史核查已确认药物丁过敏，曾有皮疹。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:14 | {"note": "患者明确否认药物丁过敏；对另一药过敏。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:15 | {"note": "皮疹疑与药物丁有关，待进一步核实。"}… | 1 | 100.0% | 100.0% |
| expansion:allergy_state:16 | {"note": "既往曾用药物丁，过敏情况一栏空白。"}… | 1 | 100.0% | 100.0% |
