# 长病历跨文档问答：逐案例结果

20 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| patient_01 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe wish to provide an update regarding Mrs. Anna Sa… | 5 | 80.0% | 60.0% |
| patient_02 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe wish to provide an update regarding Mrs. Jane Do… | 5 | 100.0% | 80.0% |
| patient_03 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nHerewith we report on Mr. John Williams, born 08/08… | 5 | 100.0% | 80.0% |
| patient_04 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe report about your outpatient treatment on 09/01/… | 5 | 100.0% | 80.0% |
| patient_05 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nPatient: Miller, John, born 04/07/1961\n\nWe report… | 5 | 100.0% | 80.0% |
| patient_06 | {"clinical_documents": {"text_0": "**Dear colleague, ****Dear colleague, **\n\n \n\nWe are writing to provide … | 5 | 100.0% | 100.0% |
| patient_07 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe report to you about Mrs. Linda Mayer, born on 01… | 5 | 100.0% | 80.0% |
| patient_08 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\n\nWe are writing to report on the outpatient treatm… | 5 | 100.0% | 100.0% |
| patient_09 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe report to you on Mr. Paul Wells, born on 04/02/1… | 5 | 100.0% | 100.0% |
| patient_10 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe would like to inform you about our patient, Mr. … | 5 | 100.0% | 100.0% |
| patient_11 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe are reporting on Mr. Bruno Hurley, born on 12/24… | 5 | 100.0% | 80.0% |
| patient_12 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe are reporting to you regarding our patient, Mr. … | 5 | 80.0% | 60.0% |
| patient_13 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe are reporting on Mr. Ben Harder, born on 08/02/1… | 5 | 100.0% | 80.0% |
| patient_14 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe are reporting on our patient, John Havers, born … | 5 | 60.0% | 60.0% |
| patient_15 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe are reporting on the patient Mr. George Davies, … | 5 | 100.0% | 100.0% |
| patient_16 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe are reporting on our shared patient, Mr. John Ch… | 5 | 100.0% | 80.0% |
| patient_17 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe are reporting on our mutual patient, Mr. Brian C… | 5 | 100.0% | 100.0% |
| patient_18 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe would like to report to you about our patient, M… | 5 | 100.0% | 100.0% |
| patient_19 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe are reporting on the inpatient stay of our patie… | 5 | 100.0% | 80.0% |
| patient_20 | {"clinical_documents": {"text_0": "**Dear colleague, **\n\nWe are writing to provide an update on the examinat… | 5 | 80.0% | 60.0% |
