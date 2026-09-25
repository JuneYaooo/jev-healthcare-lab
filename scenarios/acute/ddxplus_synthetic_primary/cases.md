# 合成病例主要诊断：逐案例结果

100 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 383 | {"age": "66", "observed_positive_or_categorical_findings": [{"question": "Do you have a known severe food alle… | 1 | 100.0% | 100.0% |
| 1097 | {"age": "8", "observed_positive_or_categorical_findings": [{"question": "Have you been in contact with a perso… | 1 | 0.0% | 0.0% |
| 1143 | {"age": "62", "observed_positive_or_categorical_findings": [{"question": "Are you currently using intravenous … | 1 | 0.0% | 0.0% |
| 1557 | {"age": "42", "observed_positive_or_categorical_findings": [{"question": "Do you have metastatic cancer?", "va… | 1 | 0.0% | 0.0% |
| 1464 | {"age": "8", "observed_positive_or_categorical_findings": [{"question": "Have you had significantly increased … | 1 | 100.0% | 100.0% |
| 325 | {"age": "18", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 100.0% |
| 901 | {"age": "34", "observed_positive_or_categorical_findings": [{"question": "Do you smoke cigarettes?", "value": … | 1 | 0.0% | 0.0% |
| 1010 | {"age": "50", "observed_positive_or_categorical_findings": [{"question": "Have you been in contact with a pers… | 1 | 0.0% | 100.0% |
| 1027 | {"age": "73", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 100.0% |
| 813 | {"age": "9", "observed_positive_or_categorical_findings": [{"question": "Have you been coughing up blood?", "v… | 1 | 100.0% | 100.0% |
| 463 | {"age": "75", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 0.0% |
| 1512 | {"age": "39", "observed_positive_or_categorical_findings": [{"question": "Do you have a known issue with one o… | 1 | 0.0% | 100.0% |
| 128 | {"age": "57", "observed_positive_or_categorical_findings": [{"question": "Do you live with 4 or more people?",… | 1 | 0.0% | 100.0% |
| 1032 | {"age": "58", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 0.0% |
| 1083 | {"age": "43", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 0.0% | 0.0% |
| 1442 | {"age": "78", "observed_positive_or_categorical_findings": [{"question": "Have you ever had fluid in your lung… | 1 | 100.0% | 100.0% |
| 1248 | {"age": "58", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 0.0% |
| 1552 | {"age": "47", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 100.0% |
| 308 | {"age": "29", "observed_positive_or_categorical_findings": [{"question": "Do you have swollen or painful lymph… | 1 | 100.0% | 100.0% |
| 353 | {"age": "12", "observed_positive_or_categorical_findings": [{"question": "Do you feel your abdomen is bloated … | 1 | 100.0% | 100.0% |
| 248 | {"age": "46", "observed_positive_or_categorical_findings": [{"question": "Do you have chronic pancreatitis?", … | 1 | 100.0% | 100.0% |
| 220 | {"age": "1", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related t… | 1 | 100.0% | 100.0% |
| 940 | {"age": "45", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 0.0% | 0.0% |
| 757 | {"age": "70", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 100.0% |
| 513 | {"age": "33", "observed_positive_or_categorical_findings": [{"question": "Have you been in contact with a pers… | 1 | 0.0% | 0.0% |
| 1371 | {"age": "45", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 100.0% |
| 76 | {"age": "27", "observed_positive_or_categorical_findings": [{"question": "Are you infected with the human immu… | 1 | 100.0% | 100.0% |
| 482 | {"age": "24", "observed_positive_or_categorical_findings": [{"question": "Do you have a poor diet?", "value": … | 1 | 100.0% | 100.0% |
| 1419 | {"age": "27", "observed_positive_or_categorical_findings": [{"question": "Have you been in contact with a pers… | 1 | 0.0% | 100.0% |
| 1270 | {"age": "30", "observed_positive_or_categorical_findings": [{"question": "Do you have a cough that produces co… | 1 | 100.0% | 100.0% |
| 701 | {"age": "22", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 0.0% | 0.0% |
| 1516 | {"age": "10", "observed_positive_or_categorical_findings": [{"question": "Do you have swollen or painful lymph… | 1 | 100.0% | 100.0% |
| 478 | {"age": "26", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 100.0% |
| 864 | {"age": "56", "observed_positive_or_categorical_findings": [{"question": "Do you have severe Chronic Obstructi… | 1 | 100.0% | 100.0% |
| 44 | {"age": "35", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 100.0% |
| 126 | {"age": "21", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 0.0% | 0.0% |
| 558 | {"age": "31", "observed_positive_or_categorical_findings": [{"question": "Do you have swollen or painful lymph… | 1 | 100.0% | 100.0% |
| 722 | {"age": "46", "observed_positive_or_categorical_findings": [{"question": "Have you recently had a viral infect… | 1 | 100.0% | 100.0% |
| 1573 | {"age": "52", "observed_positive_or_categorical_findings": [{"question": "Do you have severe Chronic Obstructi… | 1 | 100.0% | 100.0% |
| 47 | {"age": "34", "observed_positive_or_categorical_findings": [{"question": "Have you recently had a viral infect… | 1 | 100.0% | 100.0% |
| 1522 | {"age": "53", "observed_positive_or_categorical_findings": [{"question": "Are you currently taking or have you… | 1 | 100.0% | 100.0% |
| 539 | {"age": "65", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 0.0% | 0.0% |
| 692 | {"age": "69", "observed_positive_or_categorical_findings": [{"question": "Have you had significantly increased… | 1 | 100.0% | 0.0% |
| 479 | {"age": "9", "observed_positive_or_categorical_findings": [{"question": "Do you have any family members who ha… | 1 | 100.0% | 100.0% |
| 174 | {"age": "38", "observed_positive_or_categorical_findings": [{"question": "Have you had significantly increased… | 1 | 0.0% | 100.0% |
| 399 | {"age": "29", "observed_positive_or_categorical_findings": [{"question": "Do you have an active cancer?", "val… | 1 | 100.0% | 100.0% |
| 86 | {"age": "10", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 100.0% |
| 1397 | {"age": "50", "observed_positive_or_categorical_findings": [{"question": "Have you ever had a sexually transmi… | 1 | 100.0% | 100.0% |
| 278 | {"age": "11", "observed_positive_or_categorical_findings": [{"question": "Do you have pain that improves when … | 1 | 100.0% | 0.0% |
| 318 | {"age": "16", "observed_positive_or_categorical_findings": [{"question": "Are you infected with the human immu… | 1 | 0.0% | 0.0% |
| 388 | {"age": "77", "observed_positive_or_categorical_findings": [{"question": "Do you feel your abdomen is bloated … | 1 | 100.0% | 100.0% |
| 1029 | {"age": "65", "observed_positive_or_categorical_findings": [{"question": "Are you infected with the human immu… | 1 | 100.0% | 100.0% |
| 709 | {"age": "13", "observed_positive_or_categorical_findings": [{"question": "Are you infected with the human immu… | 1 | 100.0% | 0.0% |
| 162 | {"age": "91", "observed_positive_or_categorical_findings": [{"question": "Have you had significantly increased… | 1 | 100.0% | 0.0% |
| 1053 | {"age": "88", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 0.0% | 0.0% |
| 179 | {"age": "81", "observed_positive_or_categorical_findings": [{"question": "Have you been coughing up blood?", "… | 1 | 100.0% | 100.0% |
| 859 | {"age": "42", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 0.0% | 0.0% |
| 33 | {"age": "54", "observed_positive_or_categorical_findings": [{"question": "Have you been in contact with a pers… | 1 | 0.0% | 100.0% |
| 1072 | {"age": "5", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related t… | 1 | 100.0% | 100.0% |
| 245 | {"age": "75", "observed_positive_or_categorical_findings": [{"question": "Do you have a poor diet?", "value": … | 1 | 100.0% | 100.0% |
| 889 | {"age": "1", "observed_positive_or_categorical_findings": [{"question": "Have you been in contact with a perso… | 1 | 0.0% | 100.0% |
| 1504 | {"age": "60", "observed_positive_or_categorical_findings": [{"question": "Have you been in contact with a pers… | 1 | 0.0% | 0.0% |
| 1228 | {"age": "79", "observed_positive_or_categorical_findings": [{"question": "Have you ever had a pericarditis?", … | 1 | 100.0% | 100.0% |
| 801 | {"age": "47", "observed_positive_or_categorical_findings": [{"question": "Have you recently had a viral infect… | 1 | 100.0% | 100.0% |
| 799 | {"age": "78", "observed_positive_or_categorical_findings": [{"question": "Do you live with 4 or more people?",… | 1 | 100.0% | 100.0% |
| 1511 | {"age": "2", "observed_positive_or_categorical_findings": [{"question": "Do you have a poor diet?", "value": "… | 1 | 100.0% | 100.0% |
| 1199 | {"age": "44", "observed_positive_or_categorical_findings": [{"question": "Have you been in contact with a pers… | 1 | 0.0% | 0.0% |
| 810 | {"age": "70", "observed_positive_or_categorical_findings": [{"question": "Do you have a known severe food alle… | 1 | 100.0% | 100.0% |
| 329 | {"age": "16", "observed_positive_or_categorical_findings": [{"question": "Do you have a poor diet?", "value": … | 1 | 100.0% | 100.0% |
| 654 | {"age": "48", "observed_positive_or_categorical_findings": [{"question": "Have you ever had a diagnosis of ane… | 1 | 100.0% | 100.0% |
| 1307 | {"age": "33", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 0.0% | 100.0% |
| 343 | {"age": "3", "observed_positive_or_categorical_findings": [{"question": "Have you been in contact with a perso… | 1 | 0.0% | 100.0% |
| 79 | {"age": "48", "observed_positive_or_categorical_findings": [{"question": "Do you have Rheumatoid Arthritis?", … | 1 | 0.0% | 100.0% |
| 1513 | {"age": "27", "observed_positive_or_categorical_findings": [{"question": "Are you currently being treated or h… | 1 | 100.0% | 100.0% |
| 876 | {"age": "42", "observed_positive_or_categorical_findings": [{"question": "Are you infected with the human immu… | 1 | 100.0% | 100.0% |
| 750 | {"age": "37", "observed_positive_or_categorical_findings": [{"question": "Have you been in contact with a pers… | 1 | 0.0% | 100.0% |
| 1031 | {"age": "36", "observed_positive_or_categorical_findings": [{"question": "Have you noticed weakness in your fa… | 1 | 100.0% | 100.0% |
| 608 | {"age": "9", "observed_positive_or_categorical_findings": [{"question": "Do you have swollen or painful lymph … | 1 | 0.0% | 0.0% |
| 726 | {"age": "33", "observed_positive_or_categorical_findings": [{"question": "Have you recently had a viral infect… | 1 | 100.0% | 100.0% |
| 921 | {"age": "46", "observed_positive_or_categorical_findings": [{"question": "Have you recently had a viral infect… | 1 | 100.0% | 100.0% |
| 430 | {"age": "19", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 0.0% |
| 152 | {"age": "41", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 0.0% | 0.0% |
| 1253 | {"age": "10", "observed_positive_or_categorical_findings": [{"question": "Do you live with 4 or more people?",… | 1 | 0.0% | 100.0% |
| 462 | {"age": "65", "observed_positive_or_categorical_findings": [{"question": "Have you recently had a viral infect… | 1 | 100.0% | 100.0% |
| 839 | {"age": "31", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 100.0% |
| 1247 | {"age": "57", "observed_positive_or_categorical_findings": [{"question": "Have you had diarrhea or an increase… | 1 | 100.0% | 100.0% |
| 1145 | {"age": "54", "observed_positive_or_categorical_findings": [{"question": "Have you recently had a viral infect… | 1 | 100.0% | 100.0% |
| 1193 | {"age": "7", "observed_positive_or_categorical_findings": [{"question": "Do you have a poor diet?", "value": "… | 1 | 100.0% | 100.0% |
| 320 | {"age": "53", "observed_positive_or_categorical_findings": [{"question": "Have you been coughing up blood?", "… | 1 | 0.0% | 0.0% |
| 1303 | {"age": "65", "observed_positive_or_categorical_findings": [{"question": "Do you find that your symptoms have … | 1 | 0.0% | 0.0% |
| 857 | {"age": "36", "observed_positive_or_categorical_findings": [{"question": "Do you have swollen or painful lymph… | 1 | 0.0% | 0.0% |
| 585 | {"age": "72", "observed_positive_or_categorical_findings": [{"question": "Are you experiencing shortness of br… | 1 | 100.0% | 100.0% |
| 773 | {"age": "33", "observed_positive_or_categorical_findings": [{"question": "Do you have pain somewhere, related … | 1 | 100.0% | 100.0% |
| 592 | {"age": "36", "observed_positive_or_categorical_findings": [{"question": "Do you feel anxious?", "value": "yes… | 1 | 100.0% | 100.0% |
| 395 | {"age": "67", "observed_positive_or_categorical_findings": [{"question": "Do you feel your abdomen is bloated … | 1 | 100.0% | 100.0% |
| 488 | {"age": "47", "observed_positive_or_categorical_findings": [{"question": "Have you started or taken any antips… | 1 | 100.0% | 100.0% |
| 357 | {"age": "24", "observed_positive_or_categorical_findings": [{"question": "Have you recently had a viral infect… | 1 | 0.0% | 0.0% |
| 1493 | {"age": "30", "observed_positive_or_categorical_findings": [{"question": "Have you ever had a diagnosis of ane… | 1 | 100.0% | 100.0% |
| 1456 | {"age": "103", "observed_positive_or_categorical_findings": [{"question": "Do you find that your symptoms have… | 1 | 100.0% | 100.0% |
| 1051 | {"age": "44", "observed_positive_or_categorical_findings": [{"question": "Have you been in contact with a pers… | 1 | 100.0% | 100.0% |
