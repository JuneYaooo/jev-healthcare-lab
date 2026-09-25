# 医疗叙述错误定位：逐案例结果

100 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| ms-val-320 | {"clinical_text": "A 31-year-old woman comes to the doctor because of episodic nosebleeds and gingival bleedin… | 1 | 100.0% | 100.0% |
| ms-val-496 | {"clinical_text": "A 60-year-old man with a 1-year history of recurrent aspiration pneumonia is brought to the… | 1 | 100.0% | 100.0% |
| ms-val-516 | {"clinical_text": "A 45-year-old man comes to the physician because of a 3-day history of pain in his mouth an… | 1 | 100.0% | 100.0% |
| ms-val-380 | {"clinical_text": "A 53-year-old woman with type 2 diabetes mellitus is admitted for evaluation of recurrent e… | 1 | 100.0% | 100.0% |
| ms-val-29 | {"clinical_text": "A 63-year-old man comes to the physician with a 4-week history of fatigue, crampy abdominal… | 1 | 100.0% | 100.0% |
| ms-val-59 | {"clinical_text": "A 2-month-old boy is brought to the emergency department by his mother because of an 8-hour… | 1 | 0.0% | 0.0% |
| ms-val-523 | {"clinical_text": "A 45-year-old woman comes to the physician because of early satiety and intermittent nausea… | 1 | 100.0% | 100.0% |
| ms-val-215 | {"clinical_text": "A 46-year-old woman comes to the physician for a follow-up examination. She had a blood pre… | 1 | 0.0% | 0.0% |
| ms-val-529 | {"clinical_text": "A 26-year-old woman comes to the physician because of a 3-day history of redness, foreign b… | 1 | 100.0% | 100.0% |
| ms-val-85 | {"clinical_text": "A 3-year-old boy is brought to the physician for the evaluation of recurrent skin lesions. … | 1 | 100.0% | 100.0% |
| ms-val-21 | {"clinical_text": "A 25-year-old woman comes to the physician because of vaginal discharge for 4 days. She has… | 1 | 100.0% | 100.0% |
| ms-val-384 | {"clinical_text": "A 57-year-old woman comes to the emergency department because of severe pain around her rig… | 1 | 100.0% | 100.0% |
| ms-val-390 | {"clinical_text": "A 23-year-old woman with Ehlers-Danlos syndrome is brought to the emergency department with… | 1 | 100.0% | 100.0% |
| ms-val-154 | {"clinical_text": "A 20-year-old woman is brought to the physician by her mother because she has been worried … | 1 | 100.0% | 100.0% |
| ms-val-131 | {"clinical_text": "Five days after undergoing an open abdominal aortic aneurysm repair, a 68-year-old woman ha… | 1 | 100.0% | 100.0% |
| ms-val-73 | {"clinical_text": "A 26-year-old woman comes to the physician because of a progressive swelling in her mouth t… | 1 | 100.0% | 100.0% |
| ms-val-449 | {"clinical_text": "A 23-year-old primigravid woman comes to the physician at 36 weeks' gestation for her first… | 1 | 100.0% | 100.0% |
| ms-val-477 | {"clinical_text": "A 45-year-old man undergoes a parathyroidectomy given recurrent episodes of dehydration and… | 1 | 100.0% | 100.0% |
| ms-val-47 | {"clinical_text": "A 3000-g (6.6-lb) female newborn is delivered at term to a 23-year-old primigravid woman. T… | 1 | 0.0% | 0.0% |
| ms-val-12 | {"clinical_text": "A 45-year-old man with HIV comes to the physician because of multiple lesions on his lower … | 1 | 0.0% | 0.0% |
| ms-val-82 | {"clinical_text": "A 31-year-old man is brought to the emergency department because of fever and increasing co… | 1 | 100.0% | 100.0% |
| ms-val-392 | {"clinical_text": "A 19-year-old woman comes to the physician because of severe headaches for the past 3 month… | 1 | 100.0% | 100.0% |
| ms-val-83 | {"clinical_text": "A 31-year-old man is brought to the emergency department because of fever and increasing co… | 1 | 0.0% | 100.0% |
| ms-val-389 | {"clinical_text": "A 23-year-old woman with Ehlers-Danlos syndrome is brought to the emergency department with… | 1 | 0.0% | 0.0% |
| ms-val-479 | {"clinical_text": "Five days after undergoing right knee arthroplasty for osteoarthritis, a 68-year-old man ha… | 1 | 100.0% | 0.0% |
| ms-val-163 | {"clinical_text": "\"A 25-year-old female with Hodgkin's lymphoma presents with a several day history of edema… | 1 | 0.0% | 0.0% |
| ms-val-198 | {"clinical_text": "A 72-year-old woman is brought to the emergency department because of increasing abdominal … | 1 | 100.0% | 100.0% |
| ms-val-229 | {"clinical_text": "A 40-year-old woman comes to the physician for a preoperative examination before undergoing… | 1 | 0.0% | 0.0% |
| ms-val-462 | {"clinical_text": "A 19-year-old G1P0000 presents for her first obstetric ultrasound after having a positive h… | 1 | 0.0% | 0.0% |
| ms-val-492 | {"clinical_text": "A 42-year-old man is admitted to the hospital for pain and swelling in his right foot. His … | 1 | 0.0% | 100.0% |
| ms-val-451 | {"clinical_text": "A 36-year-old man is seen in the emergency department for back pain that has been getting p… | 1 | 0.0% | 0.0% |
| ms-val-322 | {"clinical_text": "A 59-year-old man comes to the emergency department because of progressive abdominal swelli… | 1 | 100.0% | 100.0% |
| ms-val-533 | {"clinical_text": "A 44-year-old man comes to the emergency department because of a severe headache and blurry… | 1 | 100.0% | 100.0% |
| ms-val-410 | {"clinical_text": "A 27-year-old woman, gravida 2, para 1, at 38 weeks' gestation comes to the emergency depar… | 1 | 100.0% | 100.0% |
| ms-val-141 | {"clinical_text": "A 34-year-old woman comes to the emergency department because of right flank pain and vomit… | 1 | 100.0% | 100.0% |
| ms-val-58 | {"clinical_text": "A 2-month-old boy is brought to the emergency department by his mother because of an 8-hour… | 1 | 100.0% | 100.0% |
| ms-val-81 | {"clinical_text": "A 65-year-old Asian woman comes to the physician for a routine health maintenance examinati… | 1 | 0.0% | 0.0% |
| ms-val-366 | {"clinical_text": "A 56-year-old man is brought to the emergency department for the evaluation of a 3-day hist… | 1 | 100.0% | 100.0% |
| ms-val-373 | {"clinical_text": "A 58-year-old man comes to the physician for a follow-up examination dressed in a vampire c… | 1 | 100.0% | 0.0% |
| ms-val-116 | {"clinical_text": "A 75-year-old man presents to his primary care physician with a painful rash. He notes his … | 1 | 100.0% | 100.0% |
| ms-val-550 | {"clinical_text": "A 68-year-old man presents to his primary care physician with complaints of intermittent dy… | 1 | 100.0% | 100.0% |
| ms-val-32 | {"clinical_text": "A 55-year-old man is brought to the physician because of inappropriate behavior for the pas… | 1 | 100.0% | 100.0% |
| ms-val-26 | {"clinical_text": "A 4-year-old boy is brought to the physician in December for episodic shortness of breath a… | 1 | 100.0% | 100.0% |
| ms-val-164 | {"clinical_text": "\"A 25-year-old female with Hodgkin's lymphoma presents with a several day history of edema… | 1 | 100.0% | 100.0% |
| ms-val-353 | {"clinical_text": "A 36-year-old primigravid woman at 8 weeks' gestation comes to the emergency department bec… | 1 | 100.0% | 100.0% |
| ms-val-16 | {"clinical_text": "A 32-year-old man is brought to the physician by his wife for a 3-day history of fever, hea… | 1 | 100.0% | 100.0% |
| ms-val-233 | {"clinical_text": "A 59-year-old woman comes to the emergency department because of a 2-day history of worseni… | 1 | 100.0% | 100.0% |
| ms-val-497 | {"clinical_text": "A 34-year-old man comes to the physician for a 1-week history of fever and generalized fati… | 1 | 100.0% | 100.0% |
| ms-val-192 | {"clinical_text": "A previously healthy 36-year-old woman comes to the emergency department because of a progr… | 1 | 100.0% | 100.0% |
| ms-val-548 | {"clinical_text": "A 27-year-old woman is brought to the physician after passing out at home. Her husband repo… | 1 | 100.0% | 100.0% |
| ms-val-555 | {"clinical_text": "A 4-year-old boy is brought to the physician by his parents because of fever and mild abdom… | 1 | 100.0% | 100.0% |
| ms-val-500 | {"clinical_text": "A 38-year-old woman comes to the physician because of difficulty falling asleep for the pas… | 1 | 100.0% | 100.0% |
| ms-val-210 | {"clinical_text": "A 27-year old woman comes to the physician for a rash that began 5 days ago. The rash invol… | 1 | 100.0% | 100.0% |
| ms-val-364 | {"clinical_text": "A 40-year-old woman comes to the physician with a 5-day history of mild shortness of breath… | 1 | 0.0% | 0.0% |
| ms-val-207 | {"clinical_text": "A 2-week-old female newborn is brought to the physician for the evaluation of red eyes with… | 1 | 100.0% | 100.0% |
| ms-val-235 | {"clinical_text": "A previously healthy 30-year-old woman comes to the physician for the evaluation of pain du… | 1 | 0.0% | 0.0% |
| ms-val-332 | {"clinical_text": "A 56-year-old woman is brought to the emergency department by her husband because of increa… | 1 | 0.0% | 0.0% |
| ms-val-429 | {"clinical_text": "A 27-year-old woman, gravida 2, para 1, at 36 weeks' gestation comes to the physician for a… | 1 | 100.0% | 100.0% |
| ms-val-301 | {"clinical_text": "A 57-year-old woman with type 2 diabetes mellitus comes to the physician for a follow-up ex… | 1 | 0.0% | 0.0% |
| ms-val-510 | {"clinical_text": "A 5-year-old girl is brought to the physician because of a 2-day history of redness and for… | 1 | 100.0% | 100.0% |
| ms-val-314 | {"clinical_text": "A 38-year-old man comes to the physician because of white lesions in his mouth for 4 days. … | 1 | 100.0% | 0.0% |
| ms-val-223 | {"clinical_text": "A 67-year-old man comes to the physician for a routine medical check-up prior to a schedule… | 1 | 0.0% | 100.0% |
| ms-val-358 | {"clinical_text": "A 19-month-old girl is brought for a well-child examination. She was born at term and has b… | 1 | 100.0% | 0.0% |
| ms-val-177 | {"clinical_text": "A 35-year-old woman comes to the physician because of a 1-month history of double vision, d… | 1 | 100.0% | 100.0% |
| ms-val-144 | {"clinical_text": "A 30-year-old woman comes to the physician because of difficulty sleeping. She is afraid of… | 1 | 100.0% | 100.0% |
| ms-val-176 | {"clinical_text": "A 59-year-old woman comes to the physician because of worsening shortness of breath for the… | 1 | 0.0% | 100.0% |
| ms-val-111 | {"clinical_text": "A 53-year-old man is brought to the emergency department following an episode of loss of co… | 1 | 100.0% | 100.0% |
| ms-val-511 | {"clinical_text": "A 5-year-old girl is brought to the physician because of a 2-day history of redness and for… | 1 | 100.0% | 100.0% |
| ms-val-18 | {"clinical_text": "A 71-year-old man comes to the emergency department because of pain and swelling in his lef… | 1 | 100.0% | 100.0% |
| ms-val-518 | {"clinical_text": "A 52-year-old man comes to the physician because of generalized pruritus and raised, erythe… | 1 | 100.0% | 100.0% |
| ms-val-96 | {"clinical_text": "A 37-year-old woman, gravida 4, para 3, at 35 weeks' gestation is admitted to the hospital … | 1 | 0.0% | 0.0% |
| ms-val-324 | {"clinical_text": "A 59-year-old man comes to the physician because of a 3-month history of frequent urination… | 1 | 100.0% | 100.0% |
| ms-val-348 | {"clinical_text": "A 24-year-old graduate student is brought to the emergency department by her boyfriend beca… | 1 | 100.0% | 100.0% |
| ms-val-24 | {"clinical_text": "A 66-year-old man with possible diabetic neuropathy comes to the physician for a follow-up … | 1 | 0.0% | 0.0% |
| ms-val-571 | {"clinical_text": "A 26-year-old male comes into your clinic complaining of worsening asthma symptoms. He repo… | 1 | 100.0% | 0.0% |
| ms-val-130 | {"clinical_text": "Five days after undergoing an open abdominal aortic aneurysm repair, a 68-year-old woman ha… | 1 | 100.0% | 100.0% |
| ms-val-263 | {"clinical_text": "A 31-year-old G6P6 woman with a history of fibroids gives birth to twins via vaginal delive… | 1 | 0.0% | 0.0% |
| ms-val-512 | {"clinical_text": "A 65-year-old man with hypertension and paroxysmal atrial fibrillation presents to his card… | 1 | 0.0% | 100.0% |
| ms-val-173 | {"clinical_text": "A 60-year-old woman is brought to the emergency department because of sudden, painless loss… | 1 | 100.0% | 100.0% |
| ms-val-260 | {"clinical_text": "A previously healthy 5-year-old boy is brought to the physician with a recurring fever and … | 1 | 100.0% | 0.0% |
| ms-val-561 | {"clinical_text": "Two weeks after hospitalization for acute psychosis, a 27-year-old woman with a history of … | 1 | 100.0% | 100.0% |
| ms-val-436 | {"clinical_text": "A 20-year-old woman is brought to the emergency department by her boyfriend for right arm a… | 1 | 0.0% | 100.0% |
| ms-val-563 | {"clinical_text": "A 34-year-old woman presents to the emergency department with sudden onset of painful visio… | 1 | 0.0% | 0.0% |
| ms-val-54 | {"clinical_text": "A 31-year-old G1P0 woman with a history of hypertension presents to the emergency departmen… | 1 | 100.0% | 100.0% |
| ms-val-401 | {"clinical_text": "A 5-year-old boy is brought to the emergency department for evaluation of a progressive ras… | 1 | 0.0% | 100.0% |
| ms-val-538 | {"clinical_text": "A 69-year-old man comes to the physician because of a 3-month history of urinary urgency, n… | 1 | 100.0% | 100.0% |
| ms-val-247 | {"clinical_text": "A 45-year-old man is brought to the emergency department 20 minutes after being rescued fro… | 1 | 0.0% | 0.0% |
| ms-val-515 | {"clinical_text": "A 27-year-old woman is brought to the emergency department by her coworker after having a g… | 1 | 100.0% | 100.0% |
| ms-val-564 | {"clinical_text": "A 29-year-old woman, gravida 1, para 0, at 36 weeks' gestation is brought to the emergency … | 1 | 100.0% | 100.0% |
| ms-val-261 | {"clinical_text": "An 11-month-old boy is brought to the emergency department because of intermittent episodes… | 1 | 0.0% | 0.0% |
| ms-val-143 | {"clinical_text": "An 8-year-old boy is brought to the physician because he has excessively dry skin. His moth… | 1 | 100.0% | 100.0% |
| ms-val-188 | {"clinical_text": "Three days after surgical repair of a distal right radius fracture, a 62-year-old man devel… | 1 | 100.0% | 100.0% |
| ms-val-303 | {"clinical_text": "A 22-year-old woman is brought to the emergency department 4 hours after the ingestion of 2… | 1 | 100.0% | 100.0% |
| ms-val-556 | {"clinical_text": "A 4-year-old boy is brought to the physician by his parents because of fever and mild abdom… | 1 | 100.0% | 0.0% |
| ms-val-402 | {"clinical_text": "A 5-year-old boy is brought to the emergency department for evaluation of a progressive ras… | 1 | 100.0% | 0.0% |
| ms-val-250 | {"clinical_text": "An 83-year-old man is admitted to the hospital with fever, weakness, and decreased responsi… | 1 | 100.0% | 100.0% |
| ms-val-242 | {"clinical_text": "A 27-year-old woman, gravida 2, para 1, at 37 weeks' gestation is admitted to the hospital … | 1 | 100.0% | 0.0% |
| ms-val-560 | {"clinical_text": "A 10-year-old boy is brought to the emergency department because he has not been able to wa… | 1 | 100.0% | 100.0% |
| ms-val-284 | {"clinical_text": "A 45-year-old male is presenting for routine health maintenance. He has no complaints. His … | 1 | 0.0% | 0.0% |
| ms-val-262 | {"clinical_text": "An 11-month-old boy is brought to the emergency department because of intermittent episodes… | 1 | 100.0% | 100.0% |
