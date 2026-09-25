# 医疗叙述错误检出：逐案例结果

100 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| ms-val-314 | {"clinical_text": "A 38-year-old man comes to the physician because of white lesions in his mouth for 4 days. … | 1 | 100.0% | 0.0% |
| ms-val-295 | {"clinical_text": "A 39-year-old woman comes to the physician because of fever, generalized fatigue, and chill… | 1 | 0.0% | 0.0% |
| ms-val-252 | {"clinical_text": "A 57-year-old woman presents to her primary care physician for weakness. The patient states… | 1 | 0.0% | 0.0% |
| ms-val-112 | {"clinical_text": "A 53-year-old man is brought to the emergency department following an episode of loss of co… | 1 | 100.0% | 100.0% |
| ms-val-568 | {"clinical_text": "A 53-year-old man presents to your office with a 2 month history of abdominal bloating. He … | 1 | 0.0% | 0.0% |
| ms-val-41 | {"clinical_text": "A 48-year-old man comes to the physician for the evaluation of dyspnea and cough. He was di… | 1 | 100.0% | 100.0% |
| ms-val-232 | {"clinical_text": "A 59-year-old woman comes to the emergency department because of a 2-day history of worseni… | 1 | 0.0% | 0.0% |
| ms-val-364 | {"clinical_text": "A 40-year-old woman comes to the physician with a 5-day history of mild shortness of breath… | 1 | 0.0% | 0.0% |
| ms-val-48 | {"clinical_text": "A 49-year-old woman comes to the physician with a 2-month history of mild abdominal pain, n… | 1 | 100.0% | 0.0% |
| ms-val-547 | {"clinical_text": "A 23-year-old pregnant woman at 22 weeks gestation presents with burning upon urination. Sh… | 1 | 100.0% | 100.0% |
| ms-val-119 | {"clinical_text": "An 18-year-old woman is brought to the emergency department by her coach, 30 minutes after … | 1 | 0.0% | 100.0% |
| ms-val-316 | {"clinical_text": "A 45-year-old woman comes to the physician because of a 2-week history of fatigue and exces… | 1 | 0.0% | 0.0% |
| ms-val-224 | {"clinical_text": "A 67-year-old man comes to the physician for a routine medical check-up prior to a schedule… | 1 | 100.0% | 100.0% |
| ms-val-368 | {"clinical_text": "A 16-year-old boy comes to the physician for the evaluation of fatigue over the past month.… | 1 | 100.0% | 100.0% |
| ms-val-222 | {"clinical_text": "A 3-year-old boy presents to the pediatrician crying with ear pain and his temperature has … | 1 | 100.0% | 100.0% |
| ms-val-142 | {"clinical_text": "An 8-year-old boy is brought to the physician because he has excessively dry skin. His moth… | 1 | 100.0% | 100.0% |
| ms-val-233 | {"clinical_text": "A 59-year-old woman comes to the emergency department because of a 2-day history of worseni… | 1 | 100.0% | 100.0% |
| ms-val-245 | {"clinical_text": "A 3500-g (7.7-lbs) girl is delivered at 39 weeks' gestation to a 27-year-old woman, gravida… | 1 | 100.0% | 100.0% |
| ms-val-461 | {"clinical_text": "A 19-year-old G1P0000 presents for her first obstetric ultrasound after having a positive h… | 1 | 0.0% | 0.0% |
| ms-val-515 | {"clinical_text": "A 27-year-old woman is brought to the emergency department by her coworker after having a g… | 1 | 100.0% | 100.0% |
| ms-val-323 | {"clinical_text": "A 59-year-old man comes to the physician because of a 3-month history of frequent urination… | 1 | 0.0% | 0.0% |
| ms-val-453 | {"clinical_text": "An 86-year-old man with a history of COPD, hypertension, and diabetes presents to the emerg… | 1 | 100.0% | 100.0% |
| ms-val-387 | {"clinical_text": "A 30-year-old male presents with a testicular mass of unknown duration. The patient states … | 1 | 0.0% | 0.0% |
| ms-val-244 | {"clinical_text": "A 3500-g (7.7-lbs) girl is delivered at 39 weeks' gestation to a 27-year-old woman, gravida… | 1 | 100.0% | 0.0% |
| ms-val-127 | {"clinical_text": "A 38-year-old woman comes to the physician for a 3-month history of bloody discharge from t… | 1 | 100.0% | 100.0% |
| ms-val-384 | {"clinical_text": "A 57-year-old woman comes to the emergency department because of severe pain around her rig… | 1 | 100.0% | 100.0% |
| ms-val-514 | {"clinical_text": "A 27-year-old woman is brought to the emergency department by her coworker after having a g… | 1 | 0.0% | 0.0% |
| ms-val-474 | {"clinical_text": "A 55-year-old man comes to the physician for a follow-up examination. During the past month… | 1 | 0.0% | 0.0% |
| ms-val-68 | {"clinical_text": "A 35-year-old woman presents to her family physician with a complaint of painful joints for… | 1 | 100.0% | 100.0% |
| ms-val-172 | {"clinical_text": "A 29-year-old woman with suspected schizophrenia is brought to the physician by her father … | 1 | 100.0% | 100.0% |
| ms-val-332 | {"clinical_text": "A 56-year-old woman is brought to the emergency department by her husband because of increa… | 1 | 0.0% | 0.0% |
| ms-val-179 | {"clinical_text": "A 67-year-old man comes to the emergency department for the evaluation of two episodes of r… | 1 | 100.0% | 100.0% |
| ms-val-45 | {"clinical_text": "A 64-year-old female presents to her primary care physician for an annual checkup. She stat… | 1 | 100.0% | 0.0% |
| ms-val-193 | {"clinical_text": "A previously healthy 36-year-old woman comes to the emergency department because of a progr… | 1 | 100.0% | 100.0% |
| ms-val-74 | {"clinical_text": "A 26-year-old woman comes to the physician because of a progressive swelling in her mouth t… | 1 | 100.0% | 100.0% |
| ms-val-454 | {"clinical_text": "An 86-year-old man with a history of COPD, hypertension, and diabetes presents to the emerg… | 1 | 0.0% | 0.0% |
| ms-val-564 | {"clinical_text": "A 29-year-old woman, gravida 1, para 0, at 36 weeks' gestation is brought to the emergency … | 1 | 100.0% | 100.0% |
| ms-val-184 | {"clinical_text": "A 5-year-old girl is brought to the emergency department because of abdominal pain, vomitin… | 1 | 100.0% | 100.0% |
| ms-val-507 | {"clinical_text": "A 53-year-old woman comes to the physician for evaluation of a 5-month history of painful s… | 1 | 100.0% | 100.0% |
| ms-val-275 | {"clinical_text": "A 53-year-old woman comes to the physician in February because of a 1-day history of fever,… | 1 | 100.0% | 0.0% |
| ms-val-264 | {"clinical_text": "A 31-year-old G6P6 woman with a history of fibroids gives birth to twins via vaginal delive… | 1 | 100.0% | 100.0% |
| ms-val-226 | {"clinical_text": "A 25-year-old G1P0000 presents to her obstetricianâ€™s office for a routine prenatal visit … | 1 | 100.0% | 0.0% |
| ms-val-260 | {"clinical_text": "A previously healthy 5-year-old boy is brought to the physician with a recurring fever and … | 1 | 0.0% | 0.0% |
| ms-val-259 | {"clinical_text": "A 55-year-old woman comes to the physician 10 days after noticing a mass in her left breast… | 1 | 0.0% | 0.0% |
| ms-val-149 | {"clinical_text": "A 2-year-old boy presents to the pediatrician for a well-child visit. The child has been do… | 1 | 100.0% | 100.0% |
| ms-val-221 | {"clinical_text": "A 3-year-old boy presents to the pediatrician crying with ear pain and his temperature has … | 1 | 0.0% | 100.0% |
| ms-val-5 | {"clinical_text": "A previously healthy 25-year-old man comes to the physician because of a 1-week history of … | 1 | 100.0% | 0.0% |
| ms-val-412 | {"clinical_text": "A 30-year-old G4P3 woman at 38 weeks gestation is admitted to the labor and delivery unit c… | 1 | 100.0% | 100.0% |
| ms-val-508 | {"clinical_text": "A 50-year-old man comes to the physician because of swelling of his legs for 2 months. Thre… | 1 | 0.0% | 100.0% |
| ms-val-145 | {"clinical_text": "A 30-year-old woman comes to the physician because of difficulty sleeping. She is afraid of… | 1 | 100.0% | 100.0% |
| ms-val-43 | {"clinical_text": "A 25-year-old man comes to the physician because of a 4-day history of bloody stools. Durin… | 1 | 100.0% | 100.0% |
| ms-val-288 | {"clinical_text": "A 60-year-old man comes to the physician because of a 6-month history of progressively wors… | 1 | 100.0% | 100.0% |
| ms-val-330 | {"clinical_text": "A 23-year-old woman gravida 2, para 1 at 12 weeks' gestation comes to the physician for her… | 1 | 100.0% | 100.0% |
| ms-val-176 | {"clinical_text": "A 59-year-old woman comes to the physician because of worsening shortness of breath for the… | 1 | 0.0% | 100.0% |
| ms-val-449 | {"clinical_text": "A 23-year-old primigravid woman comes to the physician at 36 weeks' gestation for her first… | 1 | 100.0% | 100.0% |
| ms-val-502 | {"clinical_text": "A 28-year-old man comes to the physician because of a 9-month history of sleep disturbances… | 1 | 0.0% | 0.0% |
| ms-val-440 | {"clinical_text": "A 78-year-old man is brought in to the emergency department by ambulance after his wife not… | 1 | 100.0% | 100.0% |
| ms-val-92 | {"clinical_text": "A 62-year-old Caucasian male presents to his primary care physician following a week long h… | 1 | 100.0% | 0.0% |
| ms-val-173 | {"clinical_text": "A 60-year-old woman is brought to the emergency department because of sudden, painless loss… | 1 | 100.0% | 100.0% |
| ms-val-312 | {"clinical_text": "A 33-year-old woman, gravida 2, para 1, at 26 weeks' gestation comes to the emergency depar… | 1 | 0.0% | 0.0% |
| ms-val-183 | {"clinical_text": "A 5-year-old girl is brought to the emergency department because of abdominal pain, vomitin… | 1 | 0.0% | 0.0% |
| ms-val-535 | {"clinical_text": "A 1-year-old girl is brought to the pediatrician because of a 6-month history of diarrhea. … | 1 | 100.0% | 100.0% |
| ms-val-94 | {"clinical_text": "A 35-year-old woman presents to clinic in emotional distress. She states she has been unhap… | 1 | 100.0% | 100.0% |
| ms-val-299 | {"clinical_text": "A 42-year-old woman comes to the physician for a follow-up appointment. Two months ago, she… | 1 | 0.0% | 0.0% |
| ms-val-520 | {"clinical_text": "a 34-year-old G2P2 woman presents to her obstetrician because of new onset discharge from h… | 1 | 100.0% | 100.0% |
| ms-val-567 | {"clinical_text": "A 53-year-old man presents to your office with a 2 month history of abdominal bloating. He … | 1 | 100.0% | 0.0% |
| ms-val-415 | {"clinical_text": "A 46-year-old Caucasian male with past medical history of HIV (CD4: 77/mm^3), hypertension,… | 1 | 100.0% | 100.0% |
| ms-val-466 | {"clinical_text": "A 35-year-old woman comes to the physician because of blurred vision for the past 2 months.… | 1 | 0.0% | 0.0% |
| ms-val-35 | {"clinical_text": "A previously healthy 56-year-old woman comes to the family physician for a 1-month history … | 1 | 100.0% | 100.0% |
| ms-val-530 | {"clinical_text": "A 22-year-old woman is brought to the emergency department 20 minutes after being detained … | 1 | 100.0% | 100.0% |
| ms-val-162 | {"clinical_text": "A 17-year-old rugby player limped into the emergency room and says he â€œrolled his ankleâ€… | 1 | 100.0% | 100.0% |
| ms-val-442 | {"clinical_text": "A 5-week-old infant born at 36 weeks' gestation is brought to the physician for a well-chil… | 1 | 100.0% | 0.0% |
| ms-val-269 | {"clinical_text": "A 12-year-old boy is brought to his pediatrician by his mother who is concerned about his r… | 1 | 0.0% | 0.0% |
| ms-val-266 | {"clinical_text": "A 35-year-old male is brought into the emergency department for a trauma emergency. The eme… | 1 | 100.0% | 100.0% |
| ms-val-196 | {"clinical_text": "A 14-year-old girl presents to the pediatrician for behavior issues. The girl has been havi… | 1 | 0.0% | 100.0% |
| ms-val-198 | {"clinical_text": "A 72-year-old woman is brought to the emergency department because of increasing abdominal … | 1 | 100.0% | 100.0% |
| ms-val-420 | {"clinical_text": "A 24-year-old man comes to the physician because of a painful swelling above his buttocks f… | 1 | 100.0% | 100.0% |
| ms-val-98 | {"clinical_text": "A 56-year-old man comes to the physician for a follow-up examination one week after a chest… | 1 | 100.0% | 100.0% |
| ms-val-283 | {"clinical_text": "A 53-year-old woman comes to the physician for a follow-up examination. One month ago, she … | 1 | 100.0% | 100.0% |
| ms-val-457 | {"clinical_text": "An excisional biopsy is performed and the diagnosis of superficial spreading melanoma is co… | 1 | 0.0% | 0.0% |
| ms-val-21 | {"clinical_text": "A 25-year-old woman comes to the physician because of vaginal discharge for 4 days. She has… | 1 | 100.0% | 100.0% |
| ms-val-421 | {"clinical_text": "A 44-year-old woman comes to the physician because of a 3-week history of progressive pain … | 1 | 0.0% | 100.0% |
| ms-val-560 | {"clinical_text": "A 10-year-old boy is brought to the emergency department because he has not been able to wa… | 1 | 100.0% | 100.0% |
| ms-val-169 | {"clinical_text": "A 32-year-old woman with cluster headaches comes to the physician because of a 3-month hist… | 1 | 100.0% | 0.0% |
| ms-val-527 | {"clinical_text": "An otherwise healthy 76-year-old man is brought to the physician because of poor sleep for … | 1 | 100.0% | 0.0% |
| ms-val-363 | {"clinical_text": "A 4-year-old boy is brought to the physician by his father because of a 3-day history of ge… | 1 | 100.0% | 100.0% |
| ms-val-170 | {"clinical_text": "A 32-year-old woman comes to the physician because of a 3-month history of recurrent headac… | 1 | 100.0% | 100.0% |
| ms-val-317 | {"clinical_text": "A 52-year-old man is brought to the emergency department with a 2-hour history of severe, s… | 1 | 0.0% | 0.0% |
| ms-val-289 | {"clinical_text": "A previously healthy 37-year-old man comes to the physician for the evaluation of a 8-week … | 1 | 0.0% | 100.0% |
| ms-val-308 | {"clinical_text": "A 24-year-old woman comes to the physician for a routine gynecological examination and to r… | 1 | 100.0% | 100.0% |
| ms-val-428 | {"clinical_text": "A 27-year-old woman, gravida 2, para 1, at 36 weeks' gestation comes to the physician for a… | 1 | 0.0% | 0.0% |
| ms-val-537 | {"clinical_text": "A 69-year-old man comes to the physician because of a 3-month history of urinary urgency, n… | 1 | 100.0% | 100.0% |
| ms-val-7 | {"clinical_text": "A 14-year-old girl is brought to the physician by her father because of fever, chills, abdo… | 1 | 0.0% | 100.0% |
| ms-val-327 | {"clinical_text": "A 30-year-old G3P0 woman who is 28 weeks pregnant presents for a prenatal care visit. She r… | 1 | 100.0% | 100.0% |
| ms-val-544 | {"clinical_text": "A 19-year-old woman presents to the ED after multiple episodes of vomiting in the last 6 ho… | 1 | 0.0% | 0.0% |
| ms-val-208 | {"clinical_text": "A 2-week-old female newborn is brought to the physician for the evaluation of red eyes with… | 1 | 100.0% | 0.0% |
| ms-val-322 | {"clinical_text": "A 59-year-old man comes to the emergency department because of progressive abdominal swelli… | 1 | 100.0% | 100.0% |
| ms-val-491 | {"clinical_text": "A 43-year-old female presents to her endocrinologist for a new patient appointment. She ini… | 1 | 0.0% | 0.0% |
| ms-val-483 | {"clinical_text": "A 35-year-old woman, gravida 3, para 2, at 37 weeks' gestation comes to the physician for a… | 1 | 0.0% | 0.0% |
| ms-val-73 | {"clinical_text": "A 26-year-old woman comes to the physician because of a progressive swelling in her mouth t… | 1 | 100.0% | 100.0% |
