# 英文医疗文本错误检出：逐案例结果

100 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| en-test-43 | A 66-year-old man comes to the physician because of a 3-week history of shortness of breath with exertion. He … | 1 | 100.0% | 100.0% |
| en-test-154 | A 22-year-old man comes to the physician for the evaluation of a skin rash over both of his shoulders and elbo… | 1 | 100.0% | 100.0% |
| en-test-163 | A 6-year-old boy is brought to the physician by his mother for coughing, nasal congestion, and intermittent wh… | 1 | 0.0% | 0.0% |
| en-test-46 | A 44-year-old woman is brought to the emergency department after she was found lying in the park mumbling to h… | 1 | 100.0% | 100.0% |
| en-test-98 | A 45-year-old woman comes to the physician because of a 6-month history of progressive irritability, palpitati… | 1 | 100.0% | 0.0% |
| en-test-166 | A 93-year-old woman is brought to the physician because of a purple area on her right arm that has been growin… | 1 | 100.0% | 100.0% |
| en-test-37 | A 65-year-old man comes to his primary care physician with a 6-month history of bilateral calf pain. The pain … | 1 | 100.0% | 0.0% |
| en-test-87 | A 42-year-old woman comes to the physician because of episodic abdominal pain and fullness for 1 month. The pa… | 1 | 0.0% | 100.0% |
| en-test-197 | A 36-year-old nulligravid woman comes to the physician because of a 1-year history of pelvic discomfort and he… | 1 | 100.0% | 100.0% |
| en-test-8 | A 34-year-old woman comes to the emergency department with midsternal chest pain, shortness of breath, and cou… | 1 | 100.0% | 100.0% |
| en-test-18 | Four days after undergoing a total abdominal hysterectomy for atypical endometrial hyperplasia, a 59 year-old … | 1 | 100.0% | 100.0% |
| en-test-126 | An 18-year-old man is brought to the emergency department by his girlfriend because of a pruritic rash on his … | 1 | 100.0% | 100.0% |
| en-test-1 | A 45-year-old man comes to the physician because of severe left knee pain and swelling. He has hypercholestero… | 1 | 0.0% | 0.0% |
| en-test-165 | A 68-year-old man comes to the physician because of recurrent episodes of nausea and abdominal discomfort for … | 1 | 0.0% | 0.0% |
| en-test-90 | A 45-year-old man is brought to the physician by his wife because of difficulty sleeping and poor appetite for… | 1 | 0.0% | 0.0% |
| en-test-77 | A 14-year-old boy is brought to the physician by his parents for a follow-up examination. Since early childhoo… | 1 | 100.0% | 100.0% |
| en-test-26 | A 12-year-old boy is brought to the physician for a well-child examination. He feels well. He has no history o… | 1 | 100.0% | 100.0% |
| en-test-167 | A 93-year-old woman is brought to the physician because of a purple area on her right arm that has been growin… | 1 | 100.0% | 100.0% |
| en-test-106 | A 44-year-old woman comes to the physician because of a 2-year history of progressive dysphagia. She initially… | 1 | 100.0% | 100.0% |
| en-test-117 | A 62-year-old man comes to the emergency department for severe, acute right leg pain. The patient's symptoms b… | 1 | 100.0% | 100.0% |
| en-test-39 | A 3-month-old girl is brought to the emergency department because of a 2-day history of progressive difficulty… | 1 | 0.0% | 100.0% |
| en-test-19 | Four days after undergoing a total abdominal hysterectomy for atypical endometrial hyperplasia, a 59 year-old … | 1 | 100.0% | 100.0% |
| en-test-191 | A 27-year-old woman, gravida 2, para 1, at 36 weeks' gestation comes to the physician for a prenatal visit. Sh… | 1 | 100.0% | 100.0% |
| en-test-142 | A 17-year-old boy comes to the physician because of body aches and sore throat for 1 week. He has no history o… | 1 | 100.0% | 100.0% |
| en-test-146 | A physician at an internal medicine ward notices that several of his patients have hyponatremia without any as… | 1 | 100.0% | 100.0% |
| en-test-132 | A 7-year-old boy is brought to the physician because his parents are concerned about his early sexual developm… | 1 | 100.0% | 100.0% |
| en-test-91 | A 45-year-old man is brought to the physician by his wife because of difficulty sleeping and poor appetite for… | 1 | 0.0% | 0.0% |
| en-test-2 | A 50-year-old man comes to the physician because of a 6-month history of difficulties having sexual intercours… | 1 | 100.0% | 100.0% |
| en-test-108 | A 50-year-old man comes to the physician after a fall on a flight of stairs earlier that day. He slipped, caus… | 1 | 100.0% | 100.0% |
| en-test-136 | A 6-year-old girl is brought to the physician for pain and increasing swelling over her scalp for 1 month. She… | 1 | 100.0% | 100.0% |
| en-test-177 | A 57-year-old woman comes to the emergency department 1 hour after experiencing a distressing 10-minute episod… | 1 | 100.0% | 100.0% |
| en-test-40 | A 63-year-old woman is brought to the physician by her husband for the evaluation of progressive memory loss f… | 1 | 100.0% | 0.0% |
| en-test-99 | A 45-year-old woman comes to the physician because of a 6-month history of progressive irritability, palpitati… | 1 | 100.0% | 100.0% |
| en-test-81 | A 60-year-old man comes to the physician because of a 6-month history of progressively worsening urinary frequ… | 1 | 100.0% | 100.0% |
| en-test-16 | A 21-year-old primigravid woman comes to the physician at 10 weeks' gestation because of progressive fatigue f… | 1 | 100.0% | 0.0% |
| en-test-110 | A 51-year-old woman comes to the physician because of daytime sleepiness and dry mouth for one month. She says… | 1 | 100.0% | 100.0% |
| en-test-125 | A 16-year-old girl is brought to the physician by her mother because she has not attained menarche. She has no… | 1 | 100.0% | 100.0% |
| en-test-155 | A 22-year-old man comes to the physician for the evaluation of a skin rash over both of his shoulders and elbo… | 1 | 100.0% | 0.0% |
| en-test-64 | A 37-year-old primigravid woman at 36 weeks' gestation is admitted to the hospital 30 minutes after the onset … | 1 | 100.0% | 100.0% |
| en-test-35 | A 28-year-old man comes to the physician because of a 3-month history of a recurrent pruritic rash on his face… | 1 | 100.0% | 100.0% |
| en-test-49 | An obese 52-year-old man is brought to the emergency department because of increasing shortness of breath for … | 1 | 100.0% | 100.0% |
| en-test-61 | A 61-year-old man comes to the physician because of several episodes of dark urine over the past 2 weeks. He d… | 1 | 100.0% | 100.0% |
| en-test-122 | A 25-year-old woman comes to the physician because of vaginal discharge for 4 days. She has no pain or pruritu… | 1 | 100.0% | 100.0% |
| en-test-182 | An 11-month-old boy is brought to the emergency department because of intermittent episodes of inconsolable cr… | 1 | 100.0% | 100.0% |
| en-test-100 | A 25-year-old woman, gravida 2, para 1, at 25 weeks' gestation comes to the emergency department because of a … | 1 | 100.0% | 100.0% |
| en-test-172 | A 45-year-old woman comes to the physician because of a 3-month history of worsening fatigue, loss of appetite… | 1 | 100.0% | 0.0% |
| en-test-34 | A 28-year-old man comes to the physician because of a 3-month history of a recurrent pruritic rash on his face… | 1 | 100.0% | 100.0% |
| en-test-168 | Five minutes after arriving in the postoperative care unit following total knee replacement under general anes… | 1 | 100.0% | 100.0% |
| en-test-138 | A 9-year-old boy is brought to the emergency department because of progressively worsening shortness of breath… | 1 | 100.0% | 100.0% |
| en-test-104 | A 28-year-old woman comes to the physician because of a two-month history of fatigue and low-grade fevers. Ove… | 1 | 100.0% | 100.0% |
| en-test-52 | A 55-year-old woman comes to the physician because of increased blurring of vision in both eyes for the past 4… | 1 | 100.0% | 100.0% |
| en-test-7 | A 26-year-old primigravid woman at 39 weeks' gestation is admitted to the hospital in active labor. Pregnancy … | 1 | 0.0% | 100.0% |
| en-test-102 | A 16-year-old boy comes to the physician with a 4-day history of sore throat and mild fever. He is on the vars… | 1 | 100.0% | 0.0% |
| en-test-83 | A 3466-g (7-lb, 10-oz) female newborn is delivered at 38 weeks' gestation to a 32-year-old woman, gravida 2, p… | 1 | 0.0% | 100.0% |
| en-test-171 | A 21-month-old boy is brought to the physician for a well-child examination. His mother noticed deformities in… | 1 | 100.0% | 100.0% |
| en-test-89 | A 52-year-old man comes to the physician because of a 3-month history of upper abdominal pain and nausea that … | 1 | 100.0% | 100.0% |
| en-test-78 | A 4-week-old infant is brought to the physician by his mother because of blood-tinged stools for 3 days. He ha… | 1 | 100.0% | 100.0% |
| en-test-6 | A 26-year-old primigravid woman at 39 weeks' gestation is admitted to the hospital in active labor. Pregnancy … | 1 | 100.0% | 100.0% |
| en-test-114 | A 50-year-old man comes to the physician for his annual health maintenance examination. The patient feels well… | 1 | 100.0% | 100.0% |
| en-test-178 | A 28-year-old primigravid woman comes to the emergency department because of a 12-hour history of lower abdomi… | 1 | 100.0% | 100.0% |
| en-test-93 | Five days after undergoing surgical repair of a hip fracture, a 71-year-old man is agitated and confused. Last… | 1 | 0.0% | 100.0% |
| en-test-153 | A 55-year-old nulligravid woman comes to the physician because of a 3-day history of heavy vaginal bleeding, r… | 1 | 100.0% | 100.0% |
| en-test-4 | A 24-year-old man with chronic back pain comes to the physician to establish care after moving to Florida. He … | 1 | 100.0% | 100.0% |
| en-test-62 | A 22-year-old man comes to the emergency department for pain and swelling of his left knee one day after injur… | 1 | 100.0% | 100.0% |
| en-test-80 | A 60-year-old man comes to the physician because of a 6-month history of progressively worsening urinary frequ… | 1 | 100.0% | 100.0% |
| en-test-151 | A 53-year-old woman comes to the physician for a follow-up examination. One month ago, she was diagnosed with … | 1 | 100.0% | 100.0% |
| en-test-41 | A 63-year-old woman is brought to the physician by her husband for the evaluation of progressive memory loss f… | 1 | 100.0% | 100.0% |
| en-test-173 | A 45-year-old woman comes to the physician because of a 3-month history of worsening fatigue, loss of appetite… | 1 | 100.0% | 100.0% |
| en-test-84 | A 67-year-old woman comes to the emergency department 1 hour after her husband saw her faint shortly after get… | 1 | 100.0% | 100.0% |
| en-test-135 | A 25-year-old male graduate student is brought to the emergency department for respiratory distress after he w… | 1 | 100.0% | 100.0% |
| en-test-53 | A 55-year-old woman comes to the physician because of increased blurring of vision in both eyes for the past 4… | 1 | 0.0% | 0.0% |
| en-test-38 | A 3-month-old girl is brought to the emergency department because of a 2-day history of progressive difficulty… | 1 | 100.0% | 100.0% |
| en-test-137 | A 6-year-old girl is brought to the physician for pain and increasing swelling over her scalp for 1 month. She… | 1 | 100.0% | 100.0% |
| en-test-42 | A 66-year-old man comes to the physician because of a 3-week history of shortness of breath with exertion. He … | 1 | 0.0% | 0.0% |
| en-test-28 | A 16-year-old girl comes to the physician with her mother because of intermittent abdominal cramps, fatigue, a… | 1 | 100.0% | 100.0% |
| en-test-180 | A previously healthy 10-year-old boy is brought to the emergency department for the evaluation of one episode … | 1 | 100.0% | 0.0% |
| en-test-25 | A 25-year-old woman, gravida 2, para 1, is brought to the emergency department at 39 weeks' gestation in activ… | 1 | 0.0% | 100.0% |
| en-test-131 | A 36-year-old man is brought to the emergency department 25 minutes after being involved in a high speed motor… | 1 | 100.0% | 100.0% |
| en-test-97 | A 68-year-old man is brought to the emergency department for increasing colicky lower abdominal pain and diste… | 1 | 0.0% | 100.0% |
| en-test-141 | Two weeks after undergoing coronary artery bypass surgery for acute myocardial infarction, a 62-year-old man c… | 1 | 100.0% | 100.0% |
| en-test-159 | A 74-year-old male is brought to the emergency department 1 hour after he fell from the top of the staircase a… | 1 | 100.0% | 100.0% |
| en-test-13 | A 7-year-old boy is brought to the physician by his mother because his teachers have noticed him staring blank… | 1 | 100.0% | 100.0% |
| en-test-69 | A 37-year-old woman comes to the physician because of a 2-week history of generalized fatigue and malaise. Dur… | 1 | 0.0% | 0.0% |
| en-test-9 | A 34-year-old woman comes to the emergency department with midsternal chest pain, shortness of breath, and cou… | 1 | 0.0% | 100.0% |
| en-test-187 | A 22-year-old woman comes to the physician for a routine health examination. She feels well but asks for advic… | 1 | 0.0% | 0.0% |
| en-test-5 | A 24-year-old man with chronic back pain comes to the physician to establish care after moving to Florida. He … | 1 | 100.0% | 0.0% |
| en-test-189 | A 70-year-old man comes to the physician for a follow-up evaluation. Eight months ago, he presented with a 6-m… | 1 | 100.0% | 100.0% |
| en-test-12 | A 7-year-old boy is brought to the physician by his mother because his teachers have noticed him staring blank… | 1 | 100.0% | 0.0% |
| en-test-56 | A 59-year-old woman comes to the physician for a routine health maintenance examination. She feels well. She h… | 1 | 100.0% | 100.0% |
| en-test-190 | A 27-year-old woman, gravida 2, para 1, at 36 weeks' gestation comes to the physician for a prenatal visit. Sh… | 1 | 100.0% | 0.0% |
| en-test-185 | A 35-year-old man comes to the physician because of a 6-month history of fatigue and increased sweating at nig… | 1 | 100.0% | 0.0% |
| en-test-54 | A 58-year-old man comes to the emergency department because of increasing shortness of breath and a nonproduct… | 1 | 100.0% | 100.0% |
| en-test-161 | A 30-year-old African-American woman comes to the physician for a routine checkup. She feels well. She has a h… | 1 | 100.0% | 100.0% |
| en-test-147 | A physician at an internal medicine ward notices that several of his patients have hyponatremia without any as… | 1 | 0.0% | 100.0% |
| en-test-58 | A 32-year-old woman comes to the physician because of a 2-week history of involuntary loss of urine. She loses… | 1 | 100.0% | 100.0% |
| en-test-127 | An 18-year-old man is brought to the emergency department by his girlfriend because of a pruritic rash on his … | 1 | 0.0% | 100.0% |
| en-test-50 | A 42-year-old man is brought to the physician 25 minutes after an episode of violent jerky movements of his ha… | 1 | 100.0% | 100.0% |
| en-test-68 | A 37-year-old woman comes to the physician because of a 2-week history of generalized fatigue and malaise. Dur… | 1 | 100.0% | 100.0% |
| en-test-48 | An obese 52-year-old man is brought to the emergency department because of increasing shortness of breath for … | 1 | 100.0% | 100.0% |
| en-test-183 | An 11-month-old boy is brought to the emergency department because of intermittent episodes of inconsolable cr… | 1 | 100.0% | 100.0% |
