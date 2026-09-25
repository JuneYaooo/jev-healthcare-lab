# 问诊对话对应病历章节：逐案例结果

100 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 55 | {"dialogue": "Doctor: How are you today? \nPatient: I am doing okay. \nDoctor: Just to confirm, you are fifty … | 1 | 0.0% | 0.0% |
| 39 | {"dialogue": "Doctor: How are you related to the patient?\nGuest_family: I am his friend; I work with him in a… | 1 | 100.0% | 0.0% |
| 16 | {"dialogue": "Doctor: Just to go over few things let me ask, any aches and pains?\nPatient: Currently I just h… | 1 | 100.0% | 0.0% |
| 72 | {"dialogue": "Doctor: Do you have any medical conditions that I should know about? \nPatient: Actually yes, I … | 1 | 100.0% | 100.0% |
| 88 | {"dialogue": "Doctor: Any medication intolerances? \nPatient: No."}… | 1 | 100.0% | 100.0% |
| 46 | {"dialogue": "Doctor: Are you a smoker? \nPatient: Yes. I do not drink if that is any constellation. \nDoctor:… | 1 | 100.0% | 100.0% |
| 73 | {"dialogue": "Doctor: Hello, I will ask you a few basic questions, okay?\nPatient: Okay. \nDoctor: What is you… | 1 | 100.0% | 100.0% |
| 80 | {"dialogue": "Doctor: Any past surgeries? \nPatient: Nah."}… | 1 | 100.0% | 100.0% |
| 21 | {"dialogue": "Doctor: Do you smoke? \nPatient: No, I do not.\nDoctor: How about alcohol.\nPatient: No, I don't… | 1 | 100.0% | 100.0% |
| 3 | {"dialogue": "Doctor: How've you been treating your acne? \nPatient: The dermatologist started me on Accutane.… | 1 | 0.0% | 100.0% |
| 48 | {"dialogue": "Doctor: Any difficulty in hearing? \nPatient: No.\nDoctor: Difficulty swallowing?\nPatient: Um n… | 1 | 100.0% | 100.0% |
| 63 | {"dialogue": "Doctor: How is everything else?\nPatient: Fine.\nDoctor: Anything from head to toe?\nPatient: I … | 1 | 100.0% | 0.0% |
| 97 | {"dialogue": "Doctor: Well, I have your E K G report, shows you have sinus tachycardia. In other words, your h… | 1 | 0.0% | 0.0% |
| 53 | {"dialogue": "Doctor: How are you Miss G? \nPatient: I am good doctor, thank you for asking. \nDoctor: So, tel… | 1 | 100.0% | 100.0% |
| 37 | {"dialogue": "Doctor: Good morning. So, you are here for your follow up today. \nPatient: Yes, sir. \nDoctor: … | 1 | 0.0% | 0.0% |
| 34 | {"dialogue": "Doctor: Can you tell me about cancer in your family?\nPatient: Yes, my mom had stomach cancer an… | 1 | 100.0% | 100.0% |
| 84 | {"dialogue": "Doctor: It seems like you are not feeling very well today? \nPatient: Yeah. I have had diarrhea … | 1 | 0.0% | 100.0% |
| 52 | {"dialogue": "Doctor: Do you have a history of tobacco, alcohol or recreational drug use? \nPatient: No."}… | 1 | 100.0% | 100.0% |
| 1 | {"dialogue": "Doctor: Hey, bud. What brings you in today? \nPatient: A rash on my upper arms and torso. \nDoct… | 1 | 0.0% | 0.0% |
| 49 | {"dialogue": "Guest_clinician: I did a review of her systems, and everything looks normal other than what was … | 1 | 100.0% | 100.0% |
| 58 | {"dialogue": "Doctor: Do you know any familiar diseases in your family? \nPatient: Do you mean like B P, high … | 1 | 100.0% | 100.0% |
| 78 | {"dialogue": "Doctor: Do you drink or smoke? Or take any other kind of drugs? \nPatient: I used to smoke and d… | 1 | 100.0% | 100.0% |
| 47 | {"dialogue": "Doctor: Let me add Flagyl intra venously. It will be five hundred M G every eight hours and I wo… | 1 | 100.0% | 0.0% |
| 22 | {"dialogue": "Doctor: I looked over your report from urgent care. \nPatient: They didn't do much other than te… | 1 | 0.0% | 0.0% |
| 93 | {"dialogue": "Doctor: What medications are you taking currently? \nPatient: Well, I'm taking Remeron for depre… | 1 | 100.0% | 100.0% |
| 50 | {"dialogue": "Doctor: Okay, so let's go over the plan again. I'd like you to apply Acticoat dressing daily and… | 1 | 100.0% | 100.0% |
| 60 | {"dialogue": "Doctor: Do you have any prior history of surgeries? \nPatient: I had surgery on my back and shou… | 1 | 100.0% | 100.0% |
| 56 | {"dialogue": "Doctor: Welcome to the office, Miss A. I am Doctor Luna. \nPatient: Thank you. It is nice to mee… | 1 | 100.0% | 100.0% |
| 20 | {"dialogue": "Guest_clinician: I see that the patient was in yesterday. \nDoctor: Yes, she's a frequent flyer.… | 1 | 0.0% | 0.0% |
| 87 | {"dialogue": "Doctor: So, tell me what is going on?\nPatient: Well, I have this wound on my thigh from my surg… | 1 | 100.0% | 100.0% |
| 36 | {"dialogue": "Doctor: I looked at your labs. Everything looks normal for the most part. You do have abnormal l… | 1 | 100.0% | 100.0% |
| 89 | {"dialogue": "Doctor: Good morning, young man. \nPatient: Hello, doctor. \nDoctor: So, before we get started h… | 1 | 0.0% | 0.0% |
| 44 | {"dialogue": "Doctor: Are you in pain?\nPatient: Yes, I want something strong for this. \nDoctor: We can give … | 1 | 100.0% | 0.0% |
| 7 | {"dialogue": "Doctor: Hello. How are you doing today? \nPatient: Not great. My back is killing me. \nDoctor: W… | 1 | 100.0% | 0.0% |
| 70 | {"dialogue": "Doctor: Are you allergic to anything, food or medicines?\nPatient: No allergies that I know of."… | 1 | 100.0% | 100.0% |
| 27 | {"dialogue": "Doctor: Have you ever had surgery? \nPatient: One too many times. \nDoctor: Which ones? \nPatien… | 1 | 100.0% | 100.0% |
| 81 | {"dialogue": "Doctor: I hear someone just had a birthday! How young are you now, ma'am? \nPatient: Hello, doct… | 1 | 0.0% | 0.0% |
| 98 | {"dialogue": "Doctor: Good news! No need for any shots today. He is up to date on his immunizations. \nGuest_f… | 1 | 100.0% | 100.0% |
| 10 | {"dialogue": "Doctor: Hi, I will ask about some birth related questions about your baby, okay?\nGuest_family: … | 1 | 0.0% | 100.0% |
| 38 | {"dialogue": "Doctor: I'd like to know more about your family's medical history. \nPatient: Buckle up. This is… | 1 | 100.0% | 100.0% |
| 64 | {"dialogue": "Doctor: Did you had any surgery in the past? \nPatient: Yes, I had this major trauma surgery som… | 1 | 100.0% | 100.0% |
| 41 | {"dialogue": "Doctor: It looks like your white blood cell count is normal according to your most recent labs. … | 1 | 0.0% | 0.0% |
| 94 | {"dialogue": "Guest_clinician: Did you get a chance to review patient's chart? \nDoctor: Yes, I reviewed his p… | 1 | 0.0% | 0.0% |
| 79 | {"dialogue": "Guest_clinician: Has she taken anything for her symptoms? \nDoctor: She's tried Loratadine Beclo… | 1 | 100.0% | 100.0% |
| 59 | {"dialogue": "Doctor: Hi sir, let me start by getting your age.\nGuest_family: He is fifty three!\nDoctor: So,… | 1 | 100.0% | 100.0% |
| 65 | {"dialogue": "Doctor: How old are you young man?\nPatient: I am nineteen. \nDoctor: What happened? How did you… | 1 | 100.0% | 100.0% |
| 28 | {"dialogue": "Doctor: What is your surgical history? \nPatient: I had cataract surgery on both eyes. I also ha… | 1 | 100.0% | 100.0% |
| 8 | {"dialogue": "Doctor: When are you planning to quit your I V and inhalation drugs Mister X Y Z?\nPatient: I am… | 1 | 100.0% | 100.0% |
| 2 | {"dialogue": "Doctor: Has anything changed in your medical history since you last visit on April fifteenth two… | 1 | 100.0% | 100.0% |
| 32 | {"dialogue": "Doctor: Tell me a little more about your family. Are there any significant conditions that your … | 1 | 100.0% | 100.0% |
| 4 | {"dialogue": "Doctor: Have you been experiencing any mental difficulties or confusion? \nPatient: No. Doctor: … | 1 | 0.0% | 0.0% |
| 25 | {"dialogue": "Doctor: Are you keeping up with your food journal? \nPatient: Yes, and I have it with me today. … | 1 | 100.0% | 100.0% |
| 74 | {"dialogue": "Doctor: Hello, miss. What brings you into the practice today?\nPatient: I have been missing a lo… | 1 | 100.0% | 100.0% |
| 57 | {"dialogue": "Doctor: Are you taking any medications? \nPatient: No.\nDoctor: Any over the counter drugs or an… | 1 | 100.0% | 100.0% |
| 95 | {"dialogue": "Doctor: How are you feeling? \nPatient: I am well.\nDoctor: So, we have placed a permanent pacem… | 1 | 100.0% | 100.0% |
| 66 | {"dialogue": "Doctor: Hello, miss. How are you doing today? \nPatient: My skin has been going crazy. \nDoctor:… | 1 | 0.0% | 0.0% |
| 12 | {"dialogue": "Doctor: Who are going to stay with? \nPatient: I am going home with my son. I will stay with him… | 1 | 100.0% | 100.0% |
| 69 | {"dialogue": "Doctor: Any fever, chills?\nPatient: No.\nDoctor: How about cough cold symptoms?\nPatient: Nope … | 1 | 100.0% | 100.0% |
| 15 | {"dialogue": "Doctor: Hi, how can I help?\nPatient: No, I just came in for follow up.\nDoctor: Okay so just a … | 1 | 100.0% | 100.0% |
| 68 | {"dialogue": "Doctor: Do you have a history of any surgical procedures? \nPatient: I had my gallbladder remove… | 1 | 100.0% | 100.0% |
| 31 | {"dialogue": "Doctor: Anyone sick in your family?\nPatient: No one.\nDoctor: Okay.\nPatient: Everyone is healt… | 1 | 100.0% | 100.0% |
| 71 | {"dialogue": "Doctor: How many days has it been since your headaches started? \nPatient: About two days now. \… | 1 | 0.0% | 0.0% |
| 30 | {"dialogue": "Doctor: Hi mister Jones. Do you remember me from the last time you were here? How old are you no… | 1 | 100.0% | 100.0% |
| 24 | {"dialogue": "Doctor: Hello, ma'am. How are you doing today? \nPatient: My right hand hurts. \nDoctor: Is that… | 1 | 0.0% | 0.0% |
| 42 | {"dialogue": "Doctor: How are you feeling? \nPatient: I feel good. I feel like I am getting stronger every day… | 1 | 100.0% | 100.0% |
| 5 | {"dialogue": "Doctor: How is his birth history? Was he born normal? Or was there any abnormality? \nGuest_fami… | 1 | 0.0% | 100.0% |
| 99 | {"dialogue": "Doctor: I'm glad to hear that your Afib is under control. I'd like for you to start taking baby … | 1 | 0.0% | 0.0% |
| 62 | {"dialogue": "Doctor: Hello, this is my assistant, and she will be working with me today for your care. Can yo… | 1 | 100.0% | 100.0% |
| 51 | {"dialogue": "Doctor: When are you planning to quit? \nPatient: I always plan to do it.\nDoctor: Okay let me r… | 1 | 0.0% | 0.0% |
| 6 | {"dialogue": "Doctor: Have you had any surgeries in the past?\nPatient: Nope I have not. \nDoctor: Anything?\n… | 1 | 100.0% | 100.0% |
| 43 | {"dialogue": "Doctor: Hello, sir. What brought you in today? \nPatient: Do you not see the swelling on my righ… | 1 | 100.0% | 100.0% |
| 11 | {"dialogue": "Doctor: So, where do you work? \nPatient: Oh, I am a data operator for an I T company. \nDoctor:… | 1 | 100.0% | 100.0% |
| 26 | {"dialogue": "Guest_clinician: Any significant family history of disease? \nDoctor: None according to my recor… | 1 | 100.0% | 100.0% |
| 67 | {"dialogue": "Doctor: Has she had any surgeries in the past? \nGuest_family: I couldn't tell ya even if I want… | 1 | 100.0% | 100.0% |
| 96 | {"dialogue": "Doctor: How has our little man being doing?\nGuest_family: Before today he has been doing well, … | 1 | 100.0% | 0.0% |
| 35 | {"dialogue": "Doctor: Does she have any past medical history or health problems? \nGuest_family: No. She is a … | 1 | 100.0% | 100.0% |
| 33 | {"dialogue": "Doctor: I have sent over your referral for physical therapy, occupational therapy and speech the… | 1 | 100.0% | 100.0% |
| 40 | {"dialogue": "Doctor: Are you ready for home?\nPatient: Yes.\nDoctor: Who will help at home?\nPatient: Just my… | 1 | 100.0% | 100.0% |
| 13 | {"dialogue": "Doctor: When did you move here from Philippines, sir?\nPatient: I think somewhere around ninetee… | 1 | 100.0% | 100.0% |
| 86 | {"dialogue": "Doctor: Have you had any thoughts of harming yourself or others? \nPatient: I've had thoughts of… | 1 | 100.0% | 100.0% |
| 29 | {"dialogue": "Doctor: Hi, there. How are you doing? \nPatient: I think I have some sort of condition.\nDoctor:… | 1 | 100.0% | 100.0% |
| 85 | {"dialogue": "Doctor: Do you know about any medical problems running in your family? \nPatient: No, I don't kn… | 1 | 100.0% | 100.0% |
| 77 | {"dialogue": "Doctor: Can you tell me some illness that might run in your family?\nPatient: No I don't know.\n… | 1 | 100.0% | 100.0% |
| 14 | {"dialogue": "Doctor: How old are you, sir? \nPatient: I am sixty two year old African American. \nDoctor: Do … | 1 | 100.0% | 100.0% |
| 45 | {"dialogue": "Doctor: Do you smoke cigarettes? \nPatient: No. No cigarettes. \nDoctor: Do you drink alcohol or… | 1 | 100.0% | 100.0% |
| 75 | {"dialogue": "Doctor: How long have you been having this pain in your ear?\nPatient: It's been three or four d… | 1 | 0.0% | 100.0% |
| 82 | {"dialogue": "Doctor: I reviewed all your systems, everything looks fine. \nPatient: Nice."}… | 1 | 100.0% | 100.0% |
| 23 | {"dialogue": "Doctor: Let me write you a prescription for Cipro and Flagyl.\nPatient: Okay."}… | 1 | 0.0% | 0.0% |
| 90 | {"dialogue": "Doctor: Do you drink alcohol or smoke cigarettes?\nPatient: No, I do not.\nDoctor: Are you sure?… | 1 | 100.0% | 100.0% |
| 76 | {"dialogue": "Doctor: When were you diagnosed with type two diabetes? \nPatient: Two years ago. \nDoctor: Does… | 1 | 100.0% | 100.0% |
| 0 | {"dialogue": "Doctor: When did your pain begin? \nPatient: I've had low back pain for about eight years now.\n… | 1 | 100.0% | 100.0% |
| 18 | {"dialogue": "Doctor: What brings you here today, sir?\nPatient: I'm feeling a lot of lightheadedness and I ju… | 1 | 100.0% | 100.0% |
| 9 | {"dialogue": "Doctor: Good afternoon, ma'am. \nPatient: Good afternoon, doctor. \nDoctor: Before we begin, how… | 1 | 100.0% | 100.0% |
| 61 | {"dialogue": "Doctor: So, ma'am, what brings you in for a visit today? \nPatient: Well, a few things, I have h… | 1 | 0.0% | 0.0% |
| 83 | {"dialogue": "Doctor: Let me give you some medication in your I V. \nPatient: Please make this all go away. I … | 1 | 100.0% | 0.0% |
| 17 | {"dialogue": "Doctor: Hi there! I am Doctor Frankland. \nPatient: Hi. It is nice to meet you.\nDoctor: How are… | 1 | 100.0% | 100.0% |
| 92 | {"dialogue": "Doctor: And you mentioned that you have a history of migraine?\nPatient: Yes, that's correct."}… | 1 | 100.0% | 100.0% |
| 54 | {"dialogue": "Doctor: So, I have the evaluation report from your psychiatrist.\nPatient: Ah, okay and what doe… | 1 | 0.0% | 0.0% |
| 91 | {"dialogue": "Doctor: I will do some examinations on you. I will check your chest and then I will talk to you … | 1 | 100.0% | 100.0% |
| 19 | {"dialogue": "Doctor: Are you taking any medication?\nGuest_family: Yes, I am taking that antibiotic.\nDoctor:… | 1 | 100.0% | 100.0% |
