# 五种临床量表闭集数值评分：逐案例结果

100 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| pmc-7196137-1 | {"patient_note": "Our patient is a 38-year-old woman with a past medical history most significant for a Roux-e… | 1 | 100.0% | 0.0% |
| pmc-7099753-3 | {"patient_note": "A 68-year-old woman was admitted to the hospital with dizziness, disequilibrium, and dysarth… | 1 | 0.0% | 0.0% |
| pmc-8136881-1 | {"patient_note": "An 86-year-old woman with a history of atrial fibrillation, aortic stenosis, and hypertensio… | 1 | 0.0% | 0.0% |
| pmc-7294161-1 | {"patient_note": "A 68-year-old man with the left hemiparesis from 2 h previously visited the emergency room. … | 1 | 0.0% | 100.0% |
| pmc-6959961-2 | {"patient_note": "The patient that admitted into our department was a 75-year-old male, diagnosed with osteopo… | 1 | 100.0% | 100.0% |
| pmc-3317869-1 | {"patient_note": "A 56-year-old woman with a significant history of RCA stenosis with prior bare metal stentin… | 1 | 0.0% | 100.0% |
| pmc-3888688-1 | {"patient_note": "DH 21-year-old primigravida presented for her booking visit at 11+2/40. Her history was nota… | 1 | 0.0% | 0.0% |
| pmc-6939804-1 | {"patient_note": "A 75-year-old man with persistent AF and a HAS-BLED score of 4 with recurrent gastrointestin… | 1 | 0.0% | 0.0% |
| pmc-8096577-1 | {"patient_note": "A 90-year-old African American female with a history of type 2 diabetes, essential hypertens… | 1 | 100.0% | 0.0% |
| pmc-4369977-1 | {"patient_note": "A 55-year-old right-handed male presented to the emergency department after a syncopal episo… | 1 | 0.0% | 0.0% |
| pmc-3318870-1 | {"patient_note": "A 63-year-old man with history of hypertension and glucose intolerance since age 59 years wa… | 1 | 0.0% | 0.0% |
| pmc-4967640-1 | {"patient_note": "A 59-year-old man diagnosed with obstructive hydrocephalus was scheduled for an ETV. The pat… | 1 | 0.0% | 0.0% |
| pmc-3286501-2 | {"patient_note": "A 78-year-old female patient, temporarily admitted to the recovery department after ECT, dev… | 1 | 100.0% | 100.0% |
| pmc-7437123-4 | {"patient_note": "The patient was a 64-year-old man affected by a persistent nodular lesion of the cheek mucos… | 1 | 0.0% | 0.0% |
| pmc-6533936-1 | {"patient_note": "A 57-year-old man who had alcoholic liver disease and chronic hepatitis C-related Child-Pugh… | 1 | 0.0% | 0.0% |
| pmc-4157480-1 | {"patient_note": "A 62-year-old male presented to Samsung Medical Center with a 40-year history of paroxysmal … | 1 | 0.0% | 0.0% |
| pmc-8515802-1 | {"patient_note": "A 73-year-old female presented with a chief complaint for evaluation of an incidental findin… | 1 | 0.0% | 0.0% |
| pmc-7229273-1 | {"patient_note": "The patient was a 76-year-old man with a history of mild dysphasia. He had a prior history o… | 1 | 0.0% | 0.0% |
| pmc-6296059-1 | {"patient_note": "An obese 42-year-old African American male with diabetes mellitus, hypertension, heart failu… | 1 | 0.0% | 0.0% |
| pmc-4464016-1 | {"patient_note": "An 83-year-old male with a history of arterial hypertension and diabetes developed acute rig… | 1 | 0.0% | 0.0% |
| usmle-3456 | {"patient_note": "A 17-year-old girl comes to the physician because of a sore throat, fevers, and fatigue for … | 1 | 100.0% | 0.0% |
| usmle-6072 | {"patient_note": "A 16-year-old female presents to her primary care provider for fatigue. She reports feeling … | 1 | 0.0% | 0.0% |
| pmc-8628097-1 | {"patient_note": "The patient is a 23-year-old with a temperature of 101°F female presented with acute tonsill… | 1 | 100.0% | 0.0% |
| pmc-3603656-1 | {"patient_note": "A 32-year-old lady presented to our emergency ENT service complaining of a sore throat. She … | 1 | 100.0% | 0.0% |
| usmle-585 | {"patient_note": "A 43-year-old man comes to the physician because of nasal congestion and fatigue for 12 days… | 1 | 0.0% | 0.0% |
| pmc-5661752-1 | {"patient_note": "A previously healthy 3-year-old boy is evaluated for a 3-day history of fever and swelling o… | 1 | 0.0% | 0.0% |
| pmc-7219994-1 | {"patient_note": "A 45-year-old African-American female presented to the emergency department (ED) of a rural,… | 1 | 0.0% | 100.0% |
| usmle-1376 | {"patient_note": "A 4-year-old boy is brought to the physician by his father because of a 3-day history of gen… | 1 | 0.0% | 0.0% |
| usmle-262 | {"patient_note": "A 7-year-old boy is brought to the physician for the evaluation of sore throat for the past … | 1 | 100.0% | 0.0% |
| pmc-8380012-1 | {"patient_note": "The case is of a 69-year-old man with HNPCC (Lynch Syndrome, mutation in exon 15 of hMSH2), … | 1 | 0.0% | 0.0% |
| usmle-7961 | {"patient_note": "A 6-year-old boy is presented to a pediatric clinic by his mother with complaints of fever, … | 1 | 100.0% | 0.0% |
| pmc-3034928-1 | {"patient_note": "A 28-year-old man presented with severe neck pain mainly on the left side with painful swall… | 1 | 0.0% | 0.0% |
| usmle-1375 | {"patient_note": "A 17-year-old boy comes to the physician because of body aches and sore throat for 1 week. H… | 1 | 0.0% | 100.0% |
| usmle-11773 | {"patient_note": "A 16-year-old boy is brought to the clinic for a sore throat and fever. He began feeling a d… | 1 | 0.0% | 0.0% |
| pmc-7979303-1 | {"patient_note": "On Nov 28th, 2020, a 28-year-old man was referred to our emergency department (ED) in Amir A… | 1 | 0.0% | 100.0% |
| usmle-965 | {"patient_note": "A 6-year-old boy is brought to the physician because of headache, cough, runny nose, and a l… | 1 | 0.0% | 0.0% |
| usmle-6762 | {"patient_note": "A 15-year-old girl presents to her primary care physician with her parents. She is complaini… | 1 | 0.0% | 100.0% |
| usmle-414 | {"patient_note": "A 4-year-old boy is brought to the physician because of a 5-day history of sore throat and a… | 1 | 100.0% | 100.0% |
| usmle-7401 | {"patient_note": "A 28-year-old man presents to the office complaining of a sore throat, difficulty swallowing… | 1 | 0.0% | 0.0% |
| pmc-7463145-1 | {"patient_note": "A boy named D, 15 years old, with a diagnosis of LMA, 5th day of care. At the time of assess… | 1 | 0.0% | 0.0% |
| usmle-4969 | {"patient_note": "A 38-year-old female presents to the emergency department for cough. She reports that two da… | 1 | 0.0% | 0.0% |
| pmc-7038555-1 | {"patient_note": "An 18-year-old Black female who had been diagnosed with SCD in childhood, subsequently suffe… | 1 | 0.0% | 100.0% |
| pmc-5519313-1 | {"patient_note": "The patient is a 63-year-old man with a past medical history of MALToma of the lung who pres… | 1 | 100.0% | 100.0% |
| pmc-7425612-1 | {"patient_note": "A 78-year-old man with high-grade T1 urothelial carcinoma status post-transurethral resectio… | 1 | 100.0% | 0.0% |
| pmc-8327293-1 | {"patient_note": "A 67-year-old male with a 6-day history of fever and shortness of breath was admitted to the… | 1 | 0.0% | 0.0% |
| pmc-7725203-1 | {"patient_note": "A 70-year-old man with a past medical history significant for hypertension, diabetes mellitu… | 1 | 0.0% | 0.0% |
| pmc-7916639-1 | {"patient_note": "A 70-year-old Caucasian male initially presented to the emergency department (ED) of our hos… | 1 | 0.0% | 100.0% |
| pmc-3743519-1 | {"patient_note": "An eighteen year old African American male presented to the emergency room with a 1-week his… | 1 | 0.0% | 100.0% |
| pmc-7294477-1 | {"patient_note": "A 60-year-old man presented with fever and productive cough for 2 days. He had a history of … | 1 | 0.0% | 0.0% |
| pmc-8236776-1 | {"patient_note": "The patient was a 42-year-old male with previous hypertension who presented with a 5-day his… | 1 | 0.0% | 100.0% |
| pmc-7571607-1 | {"patient_note": "A 65-year-old Hispanic male was brought to the emergency department (ED) complaining of wors… | 1 | 0.0% | 0.0% |
| usmle-1885 | {"patient_note": "A 52-year-old man is brought to the emergency department with dry cough, shortness of breath… | 1 | 0.0% | 0.0% |
| pmc-5754342-1 | {"patient_note": "A 78-year-old man presented to the emergency department with dyspnea and fever for 6 hours. … | 1 | 0.0% | 0.0% |
| pmc-7220071-1 | {"patient_note": "An 82-year-old Japanese man presented at the emergency department with 4 weeks of generalize… | 1 | 0.0% | 100.0% |
| pmc-7142028-1 | {"patient_note": "A 72-year-old female was referred to our hospital with unresolved dyspnea. She had a history… | 1 | 0.0% | 0.0% |
| pmc-4974841-1 | {"patient_note": "Our patient is a 43-year-old male with no significant past medical history who presented to … | 1 | 0.0% | 0.0% |
| pmc-3991870-1 | {"patient_note": "A delirious 44-year-old woman was brought to our emergency room complaining of shortness of … | 1 | 0.0% | 100.0% |
| usmle-8555 | {"patient_note": "A 68-year-old man is admitted to the emergency department after 2 days of difficulty breathi… | 1 | 0.0% | 0.0% |
| pmc-3874924-1 | {"patient_note": "A 43-year-old man presented with a 2-day history of dyspnea and chest pain after shouting in… | 1 | 0.0% | 100.0% |
| pmc-5646314-1 | {"patient_note": "A 51-year-old male with a past medical history of HIV, COPD, and hypertension presented with… | 1 | 0.0% | 0.0% |
| pmc-6935617-1 | {"patient_note": "A 56-year-old woman was referred to our center, with a complaint of abdominal pain and const… | 1 | 0.0% | 0.0% |
| pmc-6311171-1 | {"patient_note": "An 80-year-old male with hypertension and chronic kidney disease was admitted to our hospita… | 1 | 0.0% | 100.0% |
| pmc-2474644-1 | {"patient_note": "A 67-year-old woman presented to the hospital complaining of fever, shortness of breath and … | 1 | 100.0% | 0.0% |
| pmc-5578525-1 | {"patient_note": "A 28-year-old female patient was admitted to the emergency department with fever, fatigue, n… | 1 | 0.0% | 0.0% |
| pmc-6171780-1 | {"patient_note": "A 66-year-old male with a past medical history of hypertension and pancreatic adenocarcinoma… | 1 | 100.0% | 0.0% |
| pmc-6029742-1 | {"patient_note": "A 25-year-old man with no past medical history presented to the emergency department (ED) wi… | 1 | 0.0% | 0.0% |
| pmc-5406774-1 | {"patient_note": "Twenty-year-old male presented with an influenza-like illness (LI) with fever, cough, wheezi… | 1 | 0.0% | 0.0% |
| pmc-7189307-1 | {"patient_note": "A 52-year-old male presented to the emergency department with four days of sore throat, odyn… | 1 | 100.0% | 100.0% |
| pmc-4499596-1 | {"patient_note": "A 67-year-old man was admitted to our hospital with febrile sensation and cough for 3 days. … | 1 | 0.0% | 0.0% |
| pmc-3048475-1 | {"patient_note": "A 22-year-old South Indian man with a previous history of Fontan surgery at the age of 13 fo… | 1 | 0.0% | 0.0% |
| pmc-5500273-1 | {"patient_note": "A 58-year-old woman was admitted to the emergency department owing to generalized weakness, … | 1 | 0.0% | 100.0% |
| trec-cds-2016-23 | {"patient_note": "85M dementia, colon cancer and recent colectomy with primary reanastomosis p/w melena. HCT 3… | 1 | 100.0% | 100.0% |
| pmc-5997433-1 | {"patient_note": "A 78-year-old African-American female presented to the hospital with complaints of worsening… | 1 | 100.0% | 0.0% |
| pmc-1780062-1 | {"patient_note": "The patient was a 40-year-old male admitted for chronic cough and a 2-month history of inter… | 1 | 100.0% | 100.0% |
| pmc-8404025-2 | {"patient_note": "A 59-year-old Hispanic male patient with a medical history of hypertension, obesity, and poo… | 1 | 0.0% | 0.0% |
| pmc-4378701-1 | {"patient_note": "A 62-year-old female patient underwent a laparoscopic anterior resection procedure for sigmo… | 1 | 0.0% | 100.0% |
| pmc-6423866-1 | {"patient_note": "A previously healthy 62-year-old woman living in a rural area developed fever, headache, and… | 1 | 0.0% | 100.0% |
| pmc-7370682-1 | {"patient_note": "A 32-year-old female with a past medical history of obesity (body mass index of 42) and gast… | 1 | 0.0% | 0.0% |
| pmc-7652029-1 | {"patient_note": "A 57-year-old lady was brought to the ED by family with complaints of severe generalized bod… | 1 | 100.0% | 0.0% |
| usmle-1182 | {"patient_note": "A previously healthy 38-year-old woman is brought to the emergency department by her husband… | 1 | 0.0% | 100.0% |
| 1 | {"patient_note": "A 57-year-old male arrived at the emergency department following a reported fall down a flig… | 1 | 0.0% | 0.0% |
| 2 | {"patient_note": "A 53-year-old female was brought to the emergency department by ambulance after slipping on … | 1 | 100.0% | 100.0% |
| 3 | {"patient_note": "A 54-year-old man was brought to the emergency department by local emergency medical service… | 1 | 0.0% | 0.0% |
| 4 | {"patient_note": "A 46-year-old female was transported to the emergency department following a witnessed colla… | 1 | 0.0% | 0.0% |
| 5 | {"patient_note": "A 41-year-old woman was brought to the emergency department by her family, who reported that… | 1 | 0.0% | 0.0% |
| 6 | {"patient_note": "A 49-year-old male arrived at the emergency department after being discovered lying on the g… | 1 | 100.0% | 0.0% |
| 7 | {"patient_note": "A 64-year-old female was brought to the emergency department by paramedics after being disco… | 1 | 0.0% | 100.0% |
| 8 | {"patient_note": "A 66-year-old female was brought to the emergency department by local emergency services aft… | 1 | 0.0% | 100.0% |
| 9 | {"patient_note": "A 42-year-old female arrived at the emergency department via private vehicle after experienc… | 1 | 100.0% | 100.0% |
| 10 | {"patient_note": "A 62-year-old female was brought to the emergency department after being found in a drowsy a… | 1 | 0.0% | 0.0% |
| 11 | {"patient_note": "A 63-year-old male was brought to the emergency department by coworkers who discovered him c… | 1 | 0.0% | 0.0% |
| 12 | {"patient_note": "A 60-year-old male was brought to the emergency department after a concerned neighbor found … | 1 | 0.0% | 0.0% |
| 13 | {"patient_note": "A 58-year-old male was transported to the emergency department by local emergency services a… | 1 | 100.0% | 100.0% |
| 14 | {"patient_note": "A 58-year-old male was brought to the emergency department after being found disoriented and… | 1 | 0.0% | 0.0% |
| 15 | {"patient_note": "A 57-year-old male arrived at the hospital by ambulance after being found in a dimly lit par… | 1 | 0.0% | 0.0% |
| 16 | {"patient_note": "A 57-year-old male arrived at the emergency department after being discovered sitting on a n… | 1 | 0.0% | 0.0% |
| 17 | {"patient_note": "A 67-year-old male was brought to the emergency department by his neighbor after being found… | 1 | 100.0% | 0.0% |
| 18 | {"patient_note": "A 57-year-old male was brought to the emergency department by a neighbor who found him lying… | 1 | 100.0% | 0.0% |
| 19 | {"patient_note": "A 47-year-old male was brought in by emergency personnel after coworkers found him lying on … | 1 | 0.0% | 0.0% |
| 20 | {"patient_note": "A 64-year-old female was brought to the emergency department after being found slumped in th… | 1 | 0.0% | 100.0% |
