# 临床试验证据句定位：逐案例结果

74 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| NCT00258960 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 16/48 (33.33%)", "2": " Febrile neutropenia grade 3 3/48 … | 1 | 20.0 分 F1 | 14.3 分 F1 |
| NCT00191789 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 17/65 (26.15%)", "10": " Vomiting 2/65 (3.08%)", "11": " … | 1 | 27.3 分 F1 | 27.3 分 F1 |
| NCT01644890 | {"primary": {"0": "Outcome Measurement: ", "1": " Progression Free Survival", "10": " Unit of Measure: months … | 2 | 8.7 分 F1 | 74.1 分 F1 |
| NCT00093795 | {"primary": {"0": "Outcome Measurement: ", "1": " Disease-free Survival: Any Recurrence, Contralateral Breast … | 2 | 34.9 分 F1 | 98.0 分 F1 |
| NCT01830933 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 0/655 (0.00%)", "2": "Adverse Events 2:", "3": " Total: 0… | 1 | 85.7 分 F1 | 66.7 分 F1 |
| NCT01852032 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 0/23 (0.00%)"}, "secondary": {"0": "Adverse Events 1:", "… | 1 | 66.7 分 F1 | 66.7 分 F1 |
| NCT00425854 | {"primary": {"0": "Inclusion criteria:", "1": "Inclusion Criteria:", "10": "Exclusion Criteria:", "11": " Acti… | 1 | 10.0 分 F1 | 20.0 分 F1 |
| NCT00593346 | {"primary": {"0": "Outcome Measurement: ", "1": " Local Control Using Ipsilateral Breast Tumor Recurrence Rate… | 2 | 22.2 分 F1 | 42.1 分 F1 |
| NCT00290732 | {"primary": {"0": "INTERVENTION 1: ", "1": " Intraductal Arm", "2": " Participants received intraductal admini… | 1 | 57.1 分 F1 | 75.0 分 F1 |
| NCT00063570 | {"primary": {"0": "Inclusion Criteria:", "1": " Must have received prior chemotherapy with Taxol (paclitaxel) … | 2 | 80.0 分 F1 | 100.0 分 F1 |
| NCT00572728 | {"primary": {"0": "Inclusion Criteria:", "1": " Pathologically confirmed breast cancer, determined to be a can… | 2 | 26.7 分 F1 | 14.3 分 F1 |
| NCT02679755 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 18/100 (18.00%)", "10": " Abdominal pain upper * 0/100 (0… | 1 | 63.2 分 F1 | 90.9 分 F1 |
| NCT00606931 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 0"}, "section": "Adverse Events", "statement": "There is … | 2 | 85.7 分 F1 | 66.7 分 F1 |
| NCT00127933 | {"primary": {"0": "Inclusion Criteria:", "1": " women ＞=18 years of age;", "2": " newly diagnosed;", "3": " in… | 1 | 33.3 分 F1 | 66.7 分 F1 |
| NCT00820170 | {"primary": {"0": "Inclusion Criteria:", "1": " Female or male patients with diagnosis of invasive adenocarcin… | 2 | 69.3 分 F1 | 98.5 分 F1 |
| NCT00333775 | {"primary": {"0": "INTERVENTION 1: ", "1": " Docetaxel 100 mg/m^2 Plus Placebo", "2": " Participants received … | 2 | 73.7 分 F1 | 80.0 分 F1 |
| NCT00121134 | {"primary": {"0": "Inclusion Criteria:", "1": " Histologically or cytologically confirmed invasive breast canc… | 1 | 23.5 分 F1 | 58.8 分 F1 |
| NCT01262027 | {"primary": {"0": "Outcome Measurement: ", "1": " Overall Response (Complete Response [CR], Partial Response [… | 1 | 75.0 分 F1 | 85.7 分 F1 |
| NCT00477464 | {"primary": {"0": "INTERVENTION 1: ", "1": " Lapatinib 1250 mg and Capecitabine 2000 mg/m^2", "2": " Participa… | 2 | 66.7 分 F1 | 80.0 分 F1 |
| NCT01011946 | {"primary": {"0": "INTERVENTION 1: ", "1": " Positron Emission Mammography", "2": " Positron Emission Mammogra… | 2 | 42.9 分 F1 | 53.3 分 F1 |
| NCT00305448 | {"primary": {"0": "Outcome Measurement: ", "1": " Objective Response Rate (ORR)", "10": " Unit of Measure: per… | 2 | 75.9 分 F1 | 50.0 分 F1 |
| NCT00688909 | {"primary": {"0": "INTERVENTION 1: ", "1": " Letrozole", "2": " Participants received 2.5 milligram (mg) of Le… | 2 | 66.7 分 F1 | 66.7 分 F1 |
| NCT00009945 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 340/1612 (21.09%)", "10": " Sinus bradycardia 2/1612 (0.1… | 1 | 70.6 分 F1 | 90.0 分 F1 |
| NCT02340221 | {"primary": {"0": "Inclusion Criteria:", "1": " Postmenopausal women with histologically or cytologically conf… | 1 | 50.0 分 F1 | 66.7 分 F1 |
| NCT00856492 | {"primary": {"0": "Outcome Measurement: ", "1": " Number of Patients With Pathological Complete Response Rate"… | 2 | 59.3 分 F1 | 38.1 分 F1 |
| NCT03012477 | {"primary": {"0": "Outcome Measurement: ", "1": " Objective Response Rate", "10": " Measure Type: Number", "11… | 1 | 25.0 分 F1 | 44.4 分 F1 |
| NCT02419807 | {"primary": {"0": "Outcome Measurement: ", "1": " Proportion of Sentinel Lymph Nodes (SLNs) Flagged by the Two… | 1 | 53.3 分 F1 | 30.8 分 F1 |
| NCT03098550 | {"primary": {"0": "INTERVENTION 1: ", "1": " Nivolumab + Daratumumab (TNBC)", "2": " Triple-negative breast ca… | 2 | 66.7 分 F1 | 80.0 分 F1 |
| NCT01596751 | {"primary": {"0": "Inclusion Criteria:", "1": " Pathologically confirmed diagnosis of breast cancer with docum… | 1 | 40.0 分 F1 | 100.0 分 F1 |
| NCT01307891 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 3/39 (7.69%)", "10": " Fever 1/21 (4.76%)", "11": " Empye… | 1 | 44.4 分 F1 | 50.0 分 F1 |
| NCT02445586 | {"primary": {"0": "Inclusion Criteria:", "1": " For women of childbearing potential and men with partners of c… | 2 | 88.9 分 F1 | 100.0 分 F1 |
| NCT00820222 | {"primary": {"0": "Outcome Measurement: ", "1": " Number of Participants With Central Nervous System (CNS) Met… | 1 | 0.0 分 F1 | 0.0 分 F1 |
| NCT00357110 | {"primary": {"0": "Outcome Measurement: ", "1": " Patients Event-free at 12 Months (Where Event = Death (From … | 1 | 11.8 分 F1 | 89.7 分 F1 |
| NCT00281697 | {"primary": {"0": "Inclusion Criteria:", "1": " Signed informed consent form.", "10": " Prior hormonal therapy… | 2 | 80.0 分 F1 | 100.0 分 F1 |
| NCT01439945 | {"primary": {"0": "DISEASE CHARACTERISTICS:", "1": " Women with a history of breast cancer (currently without … | 2 | 30.8 分 F1 | 40.0 分 F1 |
| NCT01416389 | {"primary": {"0": "Outcome Measurement: ", "1": " Change in Tumor Size (CTS) From Baseline to the End of Cycle… | 1 | 66.7 分 F1 | 33.3 分 F1 |
| NCT00944047 | {"primary": {"0": "Outcome Measurement: ", "1": " Pathologic Complete Response", "10": " cyclophosphamide: 600… | 1 | 36.4 分 F1 | 61.5 分 F1 |
| NCT00263588 | {"primary": {"0": "Inclusion criteria:", "1": " Signed Informed Consent", "10": "Exclusion criteria:", "11": "… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| NCT00193037 | {"primary": {"0": "Outcome Measurement: ", "1": " Overall Response Rate (ORR), the Percentage of Patients Who … | 2 | 48.0 分 F1 | 97.3 分 F1 |
| NCT01572727 | {"primary": {"0": "INTERVENTION 1: ", "1": " BKM120 and Paclitaxel", "2": " Adult females with histologically … | 1 | 0.0 分 F1 | 82.4 分 F1 |
| NCT01042938 | {"primary": {"0": "Outcome Measurement: ", "1": " Severity of Dermatitis in Radiation Treatment Site in Breast… | 1 | 66.7 分 F1 | 89.7 分 F1 |
| NCT00904033 | {"primary": {"0": "INTERVENTION 1: ", "1": " No Exercise", "2": " Multivitamin Arm + Calcitriol Arm:Calcitriol… | 1 | 0.0 分 F1 | 0.0 分 F1 |
| NCT02244580 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 0/0", "2": "Adverse Events 2:", "3": " "}, "secondary": {… | 1 | 37.5 分 F1 | 46.2 分 F1 |
| NCT00325234 | {"primary": {"0": "Inclusion Criteria:", "1": " Females with histologic or cytologic diagnosis of advanced bre… | 1 | 50.0 分 F1 | 66.7 分 F1 |
| NCT02924883 | {"primary": {"0": "Inclusion Criteria:", "1": " Archival tumor samples must be obtained from primary and/or me… | 2 | 57.1 分 F1 | 80.0 分 F1 |
| NCT02658734 | {"primary": {"0": "Outcome Measurement: ", "1": " Severity of Adverse Events", "10": " Grade 2: 40 57.1%", "11… | 1 | 66.7 分 F1 | 92.3 分 F1 |
| NCT00022516 | {"primary": {"0": "DISEASE CHARACTERISTICS:", "1": " Histologically confirmed stage I, II, or III breast cance… | 2 | 23.5 分 F1 | 44.4 分 F1 |
| NCT02370238 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 13/61 (21.31%)", "10": " Condition aggravated 1/61 (1.64%… | 1 | 28.6 分 F1 | 15.4 分 F1 |
| NCT00328783 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 0/0"}, "section": "Adverse Events", "statement": "The adv… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| NCT00438100 | {"primary": {"0": "Inclusion Criteria:", "1": " Biopsy-diagnosed breast cancer with metastasis in multiple org… | 1 | 66.7 分 F1 | 100.0 分 F1 |
| NCT01581619 | {"primary": {"0": "Outcome Measurement: ", "1": " Safety of External-beam PBI Utilizing 40Gy in Ten Daily Frac… | 2 | 44.4 分 F1 | 48.8 分 F1 |
| NCT02301988 | {"primary": {"0": "INTERVENTION 1: ", "1": " Ipatasertib + Paclitaxel", "2": " Participants received ipatasert… | 2 | 80.0 分 F1 | 50.0 分 F1 |
| NCT02186015 | {"primary": {"0": "Inclusion Criteria:", "1": " Metastatic breast cancer (Stage IV)", "10": " English speaking… | 2 | 44.4 分 F1 | 100.0 分 F1 |
| NCT00274469 | {"primary": {"0": "Inclusion Criteria:", "1": " Confirmed hormone receptor positive advanced breast cancer, po… | 1 | 85.7 分 F1 | 66.7 分 F1 |
| NCT01808573 | {"primary": {"0": "Outcome Measurement: ", "1": " Centrally Assessed Progression Free Survival", "10": "Result… | 2 | 41.4 分 F1 | 42.9 分 F1 |
| NCT00503906 | {"primary": {"0": "INTERVENTION 1: ", "1": " Abraxane, Avastin and Gemcitabine", "2": " Each treatment cycle i… | 1 | 28.6 分 F1 | 28.6 分 F1 |
| NCT00005879 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 5/101 (4.95%)", "10": " OVARIAN CYST * 1/101 (0.99%)", "1… | 1 | 50.0 分 F1 | 100.0 分 F1 |
| NCT00754325 | {"primary": {"0": "Outcome Measurement: ", "1": " Number of Participants With Disease Progression (PD) or Deat… | 1 | 41.7 分 F1 | 97.3 分 F1 |
| NCT00876395 | {"primary": {"0": "Inclusion Criteria:", "1": " Adult Women ( 18 years old).", "10": " Prior mTOR inhibitors f… | 1 | 40.0 分 F1 | 80.0 分 F1 |
| NCT01998906 | {"primary": {"0": "INTERVENTION 1: ", "1": " HER2+ TC", "10": " Cycles 1-3 (3-week cycles): doxorubicin 60 mg/… | 1 | 63.2 分 F1 | 81.8 分 F1 |
| NCT00121992 | {"primary": {"0": "Inclusion Criteria:", "1": " Written informed consent", "10": " Adequate hematology levels.… | 1 | 100.0 分 F1 | 100.0 分 F1 |
| NCT00550771 | {"primary": {"0": "Inclusion Criteria:", "1": " Subjects with operable, node-positive or high-risk node-negati… | 2 | 56.0 分 F1 | 56.0 分 F1 |
| NCT00106002 | {"primary": {"0": "INTERVENTION 1: ", "1": " Pemetrexed", "2": " 600 mg/m2, intravenous (IV), every 14 days un… | 1 | 50.0 分 F1 | 50.0 分 F1 |
| NCT00374322 | {"primary": {"0": "INTERVENTION 1: ", "1": " Lapatinib 1500 mg", "2": " Participants received lapatinib 1500 m… | 1 | 66.7 分 F1 | 50.0 分 F1 |
| NCT00570921 | {"primary": {"0": "INTERVENTION 1: ", "1": " Fulvestrant + Everolimus", "2": " Fulvestrant + Everolimus", "3":… | 1 | 40.0 分 F1 | 40.0 分 F1 |
| NCT00633464 | {"primary": {"0": "Outcome Measurement: ", "1": " Percentage of Participants With Objective Response (OR; Usin… | 2 | 58.1 分 F1 | 71.4 分 F1 |
| NCT02131064 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 70/219 (31.96%)", "10": " Abdominal pain upper * 1/219 (0… | 1 | 66.7 分 F1 | 100.0 分 F1 |
| NCT02915744 | {"primary": {"0": "INTERVENTION 1: ", "1": " NKTR-102", "2": " In Group A, NKTR-102 will be administered at a … | 1 | 50.0 分 F1 | 50.0 分 F1 |
| NCT00852930 | {"primary": {"0": "Outcome Measurement: ", "1": " LDex Change-", "10": " Unit of Measure: LDex 28.0 (17 to 35)… | 1 | 43.5 分 F1 | 50.0 分 F1 |
| NCT01042535 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 14/41 (34.15%)", "10": " Skin infection 2/41 (4.88%)", "1… | 1 | 26.7 分 F1 | 26.7 分 F1 |
| NCT01216176 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 3/12 (25.00%)", "10": " Rash [3]0/12 (0.00%)", "2": " Atr… | 1 | 0.0 分 F1 | 0.0 分 F1 |
| NCT00733408 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 5/55 (9.09%)", "2": " Infection 2/55 (3.64%)", "3": " Pai… | 1 | 50.0 分 F1 | 90.9 分 F1 |
| NCT00331630 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 2/30 (6.67%)", "2": " Dry Eyes [1]1/30 (3.33%)", "3": " D… | 1 | 66.7 分 F1 | 40.0 分 F1 |
| NCT00915603 | {"primary": {"0": "Outcome Measurement: ", "1": " Progression-Free Survival (PFS)", "10": "Results 2: ", "11":… | 1 | 22.2 分 F1 | 11.8 分 F1 |
