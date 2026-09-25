# 英文 MedQA医学考试：逐案例结果

100 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 1006 | A 25-year-old Hispanic male presents with heat intolerance and recent weight loss. Serum analysis shows increa… | 1 | 100.0% | 100.0% |
| 1009 | A 45-year-old woman comes to the physician because of a 2-week history of painful ulcers in her mouth. Over th… | 1 | 100.0% | 0.0% |
| 1237 | A 57-year-old man comes to the physician because of a 1-year history of increasing shortness of breath on exer… | 1 | 100.0% | 100.0% |
| 94 | A 24-year-old man is brought to the emergency department 15 minutes after he sustained a stab wound to the lef… | 1 | 100.0% | 100.0% |
| 701 | A 4-year-old boy is brought to his primary care physician for a physical prior to beginning a preschool progra… | 1 | 100.0% | 100.0% |
| 82 | A 44-year-old African-American woman comes to the physician for a routine examination. She is concerned about … | 1 | 100.0% | 100.0% |
| 522 | A 54-year-old man comes to the emergency department because of a 2-day history of increasingly severe abdomina… | 1 | 100.0% | 100.0% |
| 1063 | A 54-year-old woman presents with sudden onset, mild vaginal bleeding for the past day. She says she is postme… | 1 | 100.0% | 100.0% |
| 958 | A 61-year-old man presents to the clinic with complaints of excessive thirst, frequent urination, and partial … | 1 | 100.0% | 100.0% |
| 534 | A 48-year-old man is brought to the emergency department for sudden onset of difficulty breathing 6 hours ago.… | 1 | 100.0% | 100.0% |
| 1081 | A 62-year-old woman comes to the physician because of a 6-month history of progressive pain and stiffness of t… | 1 | 100.0% | 100.0% |
| 876 | A 42-year-old woman with a history of depression and headaches presents to the emergency room with severe, pul… | 1 | 100.0% | 100.0% |
| 959 | A 65-year-old male presents to his primary care physician for stiffness in his arm. He states that he has been… | 1 | 100.0% | 100.0% |
| 1028 | A 45-year-old man presents to a surgeon with painless swelling over his right leg. He noticed the swelling 6 m… | 1 | 100.0% | 100.0% |
| 352 | Five days after undergoing an emergency appendectomy under general inhalational anesthesia while on a trip to … | 1 | 100.0% | 0.0% |
| 293 | An 8-year-old girl presents to the emergency department with respiratory distress, facial edema, and a skin ra… | 1 | 100.0% | 100.0% |
| 468 | A 24-year-old man is brought in to the emergency department by his parents who found him in his room barely re… | 1 | 100.0% | 0.0% |
| 773 | A 21-year-old female presents to the office after a health screening in which she was found to have high blood… | 1 | 100.0% | 100.0% |
| 802 | Three patients present to the pediatrician for routine well-child visits. The first child’s mother reports tha… | 1 | 100.0% | 0.0% |
| 653 | A 45-year-old woman is brought to the emergency department by her husband due to upper abdominal pain, nausea,… | 1 | 100.0% | 100.0% |
| 555 | A previously healthy 14-year-old boy is brought to the physician for evaluation because of loss of appetite, s… | 1 | 100.0% | 100.0% |
| 148 | A 65-year-old man presents to his primary care physician for a change in his behavior over the past few months… | 1 | 100.0% | 100.0% |
| 1224 | A 25-year-old man presents to his primary care physician for pain in his back. The patient describes the pain … | 1 | 0.0% | 0.0% |
| 295 | A 32-year-old female complains to her gynecologist that she has had irregular periods for several years. She h… | 1 | 100.0% | 100.0% |
| 997 | A 47-year-old woman is brought to the emergency department by paramedics. She was found unconscious on a park … | 1 | 100.0% | 100.0% |
| 536 | A 63-year-old man with diverticular disease comes to the emergency department because of painless rectal bleed… | 1 | 100.0% | 100.0% |
| 608 | A 10-year-old boy is brought to the emergency room by his grandparents. He is in a wheelchair with soft restra… | 1 | 100.0% | 100.0% |
| 543 | A 39-year-old man presents to the emergency department complaining of a sharp pain that radiates along his rig… | 1 | 100.0% | 100.0% |
| 224 | A 25-year-old male is hospitalized for acute agitation, photophobia, and dysphagia. His parents report that he… | 1 | 100.0% | 100.0% |
| 558 | A 44-year-old man presents to the family medicine clinic for some small bumps on his left thigh. The lesions a… | 1 | 100.0% | 100.0% |
| 977 | A 77-year-old man comes to your office for a routine visit. He is doing well, and his only complaint is the re… | 1 | 100.0% | 100.0% |
| 22 | A 30-year-old African American woman comes to the physician for the evaluation of a dry cough and chest discom… | 1 | 100.0% | 100.0% |
| 289 | A previously healthy 2-year-old boy is brought to the physician because of a 10-day history of unsteady gait, … | 1 | 100.0% | 100.0% |
| 212 | In order to assess the feasibility and evaluate the outcomes of cerclage wiring as a supportive approach to os… | 1 | 0.0% | 0.0% |
| 706 | A 24-year-old woman presents to the emergency department after an episode of altered mental status. She was at… | 1 | 0.0% | 0.0% |
| 852 | A 48-year-old man presents to the clinic with nausea, vomiting, fever, and pain in the right upper quadrant of… | 1 | 100.0% | 0.0% |
| 1184 | A 62-year-old Caucasian male presents to the emergency room with severe substernal chest pain, diaphoresis, an… | 1 | 0.0% | 100.0% |
| 60 | A 14-year-old girl is brought to the physician by her father because of fever, chills, abdominal pain, and pro… | 1 | 100.0% | 100.0% |
| 640 | A 4-year-old boy presents for a routine checkup. The patient’s parents say he was doing well until a few weeks… | 1 | 100.0% | 0.0% |
| 250 | A 35-year-old woman is brought into the clinic by a concerned neighbor who says that the patient is often seen… | 1 | 0.0% | 0.0% |
| 34 | A 27-year-old man presents to the emergency department. He was brought in by staff from the homeless shelter w… | 1 | 0.0% | 100.0% |
| 1076 | A 78-year-old woman presents to the emergency department with weight loss, abdominal pain, and jaundice. CT de… | 1 | 100.0% | 100.0% |
| 357 | A 24-year-old man is brought to the emergency department by the police. He was found unconscious and covered i… | 1 | 100.0% | 100.0% |
| 626 | A 21-year-old man is brought to the emergency department 30 minutes after being found unconscious in his apart… | 1 | 100.0% | 100.0% |
| 1068 | A 63-year-old man presents to his primary care physician for follow-up. He reports a slow and steady weight ga… | 1 | 100.0% | 0.0% |
| 744 | An 18-year-old college student presents to the student health clinic complaining of excessive sleepiness. He f… | 1 | 100.0% | 100.0% |
| 1033 | A 35-year-old woman presents to the emergency department after losing consciousness at work. On presentation, … | 1 | 100.0% | 100.0% |
| 192 | Please refer to the summary above to answer this question The authors of the study have decided to conduct a f… | 1 | 100.0% | 100.0% |
| 383 | A 5-month-old boy is brought to the physician with a 3-day history of fever and cough. His mother reports that… | 1 | 100.0% | 100.0% |
| 1141 | A 35-year-old woman comes to the physician for sleeping problems and the inability to concentrate for 3 months… | 1 | 100.0% | 100.0% |
| 504 | A 3-year-old boy is brought to the physician for a well-child examination. Over the past 8 months, his mother … | 1 | 100.0% | 100.0% |
| 595 | A 19-year-old female college soccer player presents to a sports medicine clinic with right knee pain. One day … | 1 | 100.0% | 100.0% |
| 988 | A researcher hypothesizes that low birth weight is related to obesity later in life. He conducts a study with … | 1 | 0.0% | 0.0% |
| 791 | A 5-year-old boy is brought to his pediatrician’s office by his parents after they noticed blood in his urine.… | 1 | 0.0% | 0.0% |
| 582 | A 27-year-old male suddenly develops severe abdominal cramping and bloody diarrhea. The patient reports consum… | 1 | 100.0% | 0.0% |
| 191 | A stillborn infant is delivered at 38 weeks' gestation to a 32-year-old woman. The mother had no prenatal care… | 1 | 100.0% | 100.0% |
| 881 | A 52-year-old man presents to the physician with a 6-month history of shortness of breath and nonproductive co… | 1 | 100.0% | 100.0% |
| 722 | A 20-day-old child is brought to the emergency department by her parents. They are concerned about lethargy an… | 1 | 100.0% | 100.0% |
| 763 | A 42-year-old chronic alcoholic man was admitted to the hospital for inappropriate behavior and disturbed memo… | 1 | 100.0% | 100.0% |
| 1149 | A 21-month-old boy is brought to the physician for a well-child examination. His mother noticed deformities in… | 1 | 100.0% | 100.0% |
| 87 | A 50-year-old man visits his physician after 20 years of not seeking any medical care. He is concerned about h… | 1 | 100.0% | 100.0% |
| 1038 | A 32-year-old male presents to the ED with acute-onset chest pain. His blood pressure is 157/90 mmHg and his h… | 1 | 100.0% | 100.0% |
| 417 | A 55-year-old woman with papillary thyroid carcinoma underwent total thyroidectomy. She has no significant med… | 1 | 100.0% | 100.0% |
| 928 | A 45-year-old man presents to the emergency department with severe dyspnea, wheezing, and palpitations. His sy… | 1 | 100.0% | 0.0% |
| 796 | While traveling abroad a physician is asked to attend a meeting regarding healthcare in the region. The rate o… | 1 | 100.0% | 100.0% |
| 774 | A 25-year-old African American man presents to his primary care provider for routine blood work. He is a well-… | 1 | 100.0% | 100.0% |
| 222 | A 60-year-old woman presents to a physician for worsening shortness of breath and increasing abdominal distent… | 1 | 0.0% | 0.0% |
| 830 | A 72-year-old man in a nursing home was brought to the emergency department with right hand and leg weakness f… | 1 | 100.0% | 100.0% |
| 1092 | A 69-year-old man presents to his primary care physician for trouble sleeping. The patient states that he rece… | 1 | 100.0% | 100.0% |
| 186 | A laboratory primarily involved with studying cellular proofreading mechanisms is investigating the question o… | 1 | 100.0% | 100.0% |
| 929 | A 74-year-old man has been treated for prostate cancer for the past 6 months. He is on an experimental drug (d… | 1 | 100.0% | 100.0% |
| 1131 | A 78-year-old right-handed man is brought to the emergency department by his daughter for sudden onset speech … | 1 | 100.0% | 100.0% |
| 1079 | A 65-year-old man presents with left-sided numbness, diplopia, and blurring of vision. The diplopia is more pr… | 1 | 0.0% | 100.0% |
| 573 | A previously healthy 46-year-old woman comes to the physician because of progressive shortness of breath, fati… | 1 | 0.0% | 100.0% |
| 1159 | A 68-year-old man presents to the emergency department because of fever, abdominal pain, and rapidly progressi… | 1 | 100.0% | 100.0% |
| 724 | A 32-year-old man presents to the emergency department with fever, nausea, and vomiting. The patient states th… | 1 | 0.0% | 0.0% |
| 495 | A 55-year-old woman is found to have an abnormal mass on routine mammography. The mass is biopsied and cytolog… | 1 | 0.0% | 0.0% |
| 119 | A 25-year-old zookeeper presents to the office complaining of a dry cough, fever, and chills for the past mont… | 1 | 100.0% | 100.0% |
| 1148 | A researcher evaluates healthy breast tissue from 100 women, 50 women that were pregnant at the time of the st… | 1 | 100.0% | 100.0% |
| 1174 | A 40-year-old woman presents to her family physician with a 3-week history of swollen neck. The small, round, … | 1 | 0.0% | 100.0% |
| 864 | A 26-year-old man with no significant past medical history presents to the ED following a motor vehicle accide… | 1 | 100.0% | 100.0% |
| 1185 | A previously healthy, 24-year-old man comes to the physician because of a 6-week history of loose, nonbloody s… | 1 | 100.0% | 100.0% |
| 223 | A 15-year-old girl comes to the physician because of episodic pelvic pain radiating to her back and thighs for… | 1 | 100.0% | 100.0% |
| 366 | A 28-year-old female comes to the physician’s office with a complaint of episodic chest pain. She describes th… | 1 | 100.0% | 100.0% |
| 127 | A 67-year-old man with peripheral neuropathy comes to the physician for a follow-up examination after the resu… | 1 | 100.0% | 100.0% |
| 601 | An investigator is studying the pattern of glutamate release from presynaptic nerve terminals in human volunte… | 1 | 100.0% | 100.0% |
| 1233 | A 30-year-old Japanese woman is brought to the emergency department after fainting at work. She says she was o… | 1 | 0.0% | 0.0% |
| 1198 | A 27-year-old man with a history of cocaine abuse comes to the physician 2 weeks after undergoing successful a… | 1 | 100.0% | 100.0% |
| 379 | A 52-year-old man is brought to the emergency department because of worsening shortness of breath for 6 hours.… | 1 | 100.0% | 100.0% |
| 538 | A 25-year-old female presents to urgent care with complaints of one day of burning and pain with urination, ur… | 1 | 0.0% | 0.0% |
| 143 | A 68-year-old man comes to the physician with a 1-week history of painless hematuria. A CT scan of the urinary… | 1 | 100.0% | 100.0% |
| 1098 | A 32-year-old woman presents to the emergency department with complaints of a headache. The last menstrual per… | 1 | 100.0% | 100.0% |
| 121 | A 40-year-old man presents to the physician with progressive weight loss for the last 3 months. He also says h… | 1 | 100.0% | 100.0% |
| 1010 | A 25-year-old woman presents to her primary care provider for evaluation of a "painful mass in my left groin."… | 1 | 0.0% | 0.0% |
| 577 | A 63-year-old man from the countryside presents with leg swelling and right upper abdominal tenderness. He rep… | 1 | 100.0% | 0.0% |
| 974 | A 45-year-old man presents to the doctor’s office with shortness of breath, cough, and fatigue for 3 days. Thi… | 1 | 100.0% | 100.0% |
| 873 | A 2-hour-old, 3.2 kg (7.0 lb) newborn boy born by cesarean delivery is being evaluated by the resident on-call… | 1 | 100.0% | 100.0% |
| 1153 | A 68-year-old man presents to his primary care physician with complaints of increased fatigue and back pain fo… | 1 | 100.0% | 100.0% |
| 680 | A 25-year-old man presents to the office because of extreme fatigue for the past 2 days. He is also worried ab… | 1 | 100.0% | 100.0% |
| 453 | A 34-year-old man presents to the emergency department complaining of headache, fever, chills, cough, shortnes… | 1 | 100.0% | 100.0% |
