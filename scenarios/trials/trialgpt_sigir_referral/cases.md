# 患者与临床试验入组预筛：逐案例结果

45 个案例，共 150 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| sigir-20157 | {"patient": "A 20 yo female college student with no significant past medical history presents with a chief com… | 4 | 25.0% | 75.0% |
| sigir-201417 | {"patient": "A 48-year-old white male with history of common variable immunodeficiency (CVID) with acute abdom… | 4 | 75.0% | 75.0% |
| sigir-201430 | {"patient": "A 72-year-old man complains of increasing calf pain when walking uphill. The symptoms have gradua… | 3 | 100.0% | 100.0% |
| sigir-20149 | {"patient": "A 43-year-old woman visits her dermatologist for lesions on her neck. On examination, multiple le… | 4 | 25.0% | 25.0% |
| sigir-201514 | {"patient": "A 27-year-old woman at 11 weeks gestation in her second pregnancy is found to have a hemoglobin (… | 1 | 100.0% | 100.0% |
| sigir-201410 | {"patient": "A physician is called to see a 67-year-old woman who underwent cardiac catheterization via the ri… | 3 | 66.7% | 66.7% |
| sigir-201518 | {"patient": "A 65 yo African-American male with shortness of breath related to exertion that has been worsenin… | 7 | 42.9% | 57.1% |
| sigir-201515 | {"patient": "Karen is a 72-year-old woman with hypertension and type 2 diabetes, who was hospitalized for cryp… | 4 | 25.0% | 25.0% |
| sigir-201413 | {"patient": "A 30-year-old generally healthy woman presents with shortness of breath that had started 2 hours … | 7 | 28.6% | 42.9% |
| sigir-201521 | {"patient": "A 32-year-old male presents to your office complaining of diarrhea, abdominal cramping and flatul… | 2 | 50.0% | 50.0% |
| sigir-201421 | {"patient": "A 21-year-old female is evaluated for progressive arthralgias and malaise. On examination she is … | 9 | 33.3% | 33.3% |
| sigir-20143 | {"patient": "A 58-year-old nonsmoker white female with mild exertional dyspnea and occasional cough is found t… | 5 | 40.0% | 80.0% |
| sigir-201524 | {"patient": "A 31 yo male with no significant past medical history presents with productive cough and chest pa… | 7 | 71.4% | 85.7% |
| sigir-201429 | {"patient": "A 51-year-old woman is seen in clinic for advice on osteoporosis. She has a past medical history … | 4 | 25.0% | 50.0% |
| sigir-20154 | {"patient": "An 82-year-old woman comes to the emergency department because of chest pain and shortness of bre… | 3 | 66.7% | 66.7% |
| sigir-20146 | {"patient": "64-year-old obese female with diagnosis of diabetes mellitus and persistently elevated HbA1c. She… | 5 | 60.0% | 60.0% |
| sigir-20152 | {"patient": "A 62 yo male presents with four days of non-productive cough and one day of fever. He is on immun… | 3 | 66.7% | 66.7% |
| sigir-20147 | {"patient": "A 26-year-old obese woman with a history of bipolar disorder complains that her recent struggles … | 9 | 22.2% | 22.2% |
| sigir-201511 | {"patient": "A 56-year old Caucasian female complains of being markedly more sensitive to the cold than most p… | 2 | 100.0% | 100.0% |
| sigir-201527 | {"patient": "A 15 yo girl accompanied by her mother is referred for evaluation by the school. The girl has mor… | 1 | 100.0% | 100.0% |
| sigir-201512 | {"patient": "A 44-year-old man was recently in an automobile accident where he sustained a skull fracture. In … | 2 | 100.0% | 50.0% |
| sigir-20155 | {"patient": "A 31-year-old woman with no previous medical problems comes to the emergency room with a history … | 2 | 50.0% | 50.0% |
| sigir-20156 | {"patient": "A 46-year-old woman presents with a 9 month history of weight loss (20 lb), sweating, insomnia an… | 5 | 40.0% | 40.0% |
| sigir-201422 | {"patient": "A 15-year-old girl presents to the ER with abdominal pain. The pain appeared gradually and was pe… | 4 | 50.0% | 75.0% |
| sigir-201419 | {"patient": "A 52-year-old African American man with a history of heavy smoking and drinking, describes progre… | 5 | 80.0% | 80.0% |
| sigir-201528 | {"patient": "A previously healthy 8-year-old boy presents with a complaint of right lower extremity pain and f… | 1 | 100.0% | 100.0% |
| sigir-201425 | {"patient": "An 8-year-old boy fell from his bike striking his left temple on the pavement. There was no immed… | 1 | 100.0% | 100.0% |
| sigir-201522 | {"patient": "A 65-year-old male with a history of tuberculosis has started to complain of productive cough wit… | 3 | 66.7% | 66.7% |
| sigir-20144 | {"patient": "A 2-year-old boy is brought to the emergency department by his parents for 5 days of high fever a… | 3 | 66.7% | 66.7% |
| sigir-201420 | {"patient": "A 32-year-old woman is admitted to the ER following a car accident. She has sustained multiple in… | 2 | 100.0% | 100.0% |
| sigir-20153 | {"patient": "A 65 yo male with no significant history of cardiovascular disease presents to the emergency room… | 3 | 66.7% | 66.7% |
| sigir-201519 | {"patient": "A 66yo female with significant smoking history and chronic cough for the past two years presents … | 5 | 40.0% | 40.0% |
| sigir-20151 | {"patient": "A 44 yo male is brought to the emergency room after multiple bouts of vomiting that has a \"coffe… | 5 | 0.0% | 0.0% |
| sigir-201523 | {"patient": "An 18-year-old male returning from a recent vacation in Asia presents to the ER with a sudden ons… | 1 | 100.0% | 100.0% |
| sigir-201423 | {"patient": "A 63-year-old man presents with cough and shortness of breath. His past medical history is notabl… | 4 | 75.0% | 75.0% |
| sigir-20148 | {"patient": "A 62-year-old man sees a neurologist for progressive memory loss and jerking movements of the low… | 2 | 0.0% | 0.0% |
| sigir-201526 | {"patient": "A 28 yo female G1P0A0 is admitted to the Ob/Gyn service for non-ruptured ectopic pregnancy. Past … | 3 | 0.0% | 0.0% |
| sigir-201517 | {"patient": "A 32 year old female with no previous medical history presents to clinic to discuss lab results f… | 1 | 100.0% | 0.0% |
| sigir-201414 | {"patient": "An 85-year-old man is brought to the ER because of gradual decrease in his level of consciousness… | 1 | 100.0% | 100.0% |
| sigir-201525 | {"patient": "A 10-year-old boy comes to the emergency department for evaluation of right knee pain. The child'… | 1 | 0.0% | 100.0% |
| sigir-20141 | {"patient": "A 58-year-old African-American woman presents to the ER with episodic pressing/burning anterior c… | 2 | 0.0% | 0.0% |
| sigir-201516 | {"patient": "A 4 year old boy presents to the emergency room with wheezing. He has had a history of allergic r… | 2 | 0.0% | 50.0% |
| sigir-201412 | {"patient": "A 25-year-old woman presents to the clinic complaining of prolonged fatigue. She denies difficult… | 1 | 0.0% | 0.0% |
| sigir-20145 | {"patient": "A 56-year-old female on 20th day post-left mastectomy presents to the emergency department compla… | 3 | 66.7% | 66.7% |
| sigir-201424 | {"patient": "A 33-year-old male athlete presented to the ER with acute abdominal pain. Family member says the … | 1 | 0.0% | 100.0% |
