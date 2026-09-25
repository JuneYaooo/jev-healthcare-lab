# 边界挑战：用药变更：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| medication_change:1 | {"note": "今日医嘱：开始服用阿司匹林。"}… | 1 | 100.0% | 100.0% |
| medication_change:2 | {"note": "出院时已停用阿司匹林。"}… | 1 | 100.0% | 100.0% |
| medication_change:3 | {"note": "继续原剂量阿司匹林。"}… | 1 | 100.0% | 100.0% |
| medication_change:4 | {"note": "下次复诊讨论是否停用阿司匹林，目前没有停药医嘱。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:1 | {"note": "原未服用药物甲，今日新医嘱开始服用；其他药维持。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:2 | {"note": "医生撤销药物甲处方并要求停止；其他药继续。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:3 | {"note": "复诊医嘱明确药物甲维持原方案。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:4 | {"note": "医生准备讨论是否调整药物甲，目前没有变更决定。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:5 | {"note": "原未服用药物乙，今日新医嘱开始服用；其他药维持。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:6 | {"note": "医生撤销药物乙处方并要求停止；其他药继续。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:7 | {"note": "复诊医嘱明确药物乙维持原方案。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:8 | {"note": "医生准备讨论是否调整药物乙，目前没有变更决定。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:9 | {"note": "原未服用药物丙，今日新医嘱开始服用；其他药维持。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:10 | {"note": "医生撤销药物丙处方并要求停止；其他药继续。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:11 | {"note": "复诊医嘱明确药物丙维持原方案。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:12 | {"note": "医生准备讨论是否调整药物丙，目前没有变更决定。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:13 | {"note": "原未服用药物丁，今日新医嘱开始服用；其他药维持。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:14 | {"note": "医生撤销药物丁处方并要求停止；其他药继续。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:15 | {"note": "复诊医嘱明确药物丁维持原方案。"}… | 1 | 100.0% | 100.0% |
| expansion:medication_change:16 | {"note": "医生准备讨论是否调整药物丁，目前没有变更决定。"}… | 1 | 100.0% | 100.0% |
