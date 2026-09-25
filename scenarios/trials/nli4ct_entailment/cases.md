# 临床试验证据支持判断：逐案例结果

70 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| NCT00445458 | {"primary": {"0": "Outcome Measurement: ", "1": " Dose Limiting Toxicity Incidence of Neratinib in Combination… | 1 | 100.0% | 100.0% |
| NCT00274469 | {"primary": {"0": "Inclusion Criteria:", "1": " Confirmed hormone receptor positive advanced breast cancer, po… | 2 | 100.0% | 100.0% |
| NCT01118624 | {"primary": {"0": "INTERVENTION 1: ", "1": " Pralatrexate", "2": " Study drug 190 mg/m^2 for 2 to 4 weeks."}, … | 2 | 100.0% | 100.0% |
| NCT03012477 | {"primary": {"0": "Outcome Measurement: ", "1": " Objective Response Rate", "10": " Measure Type: Number", "11… | 1 | 100.0% | 100.0% |
| NCT01439945 | {"primary": {"0": "DISEASE CHARACTERISTICS:", "1": " Women with a history of breast cancer (currently without … | 2 | 100.0% | 100.0% |
| NCT02419807 | {"primary": {"0": "Outcome Measurement: ", "1": " Proportion of Sentinel Lymph Nodes (SLNs) Flagged by the Two… | 1 | 100.0% | 100.0% |
| NCT00121134 | {"primary": {"0": "Inclusion Criteria:", "1": " Histologically or cytologically confirmed invasive breast canc… | 1 | 100.0% | 100.0% |
| NCT01307891 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 3/39 (7.69%)", "10": " Fever 1/21 (4.76%)", "11": " Empye… | 1 | 100.0% | 100.0% |
| NCT01905592 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 4/65 (6.15%)", "10": " Vomiting * 21/65 (1.54%)", "11": "… | 2 | 100.0% | 50.0% |
| NCT00375427 | {"primary": {"0": "Inclusion criteria:", "1": " Female patients 18 years of age.", "10": " Serum creatinine ＞ … | 2 | 100.0% | 100.0% |
| NCT01929395 | {"primary": {"0": "Inclusion Criteria Phase 1", "1": " Age greater than/equal to 18 years", "10": " Patient de… | 2 | 50.0% | 50.0% |
| NCT00357110 | {"primary": {"0": "Outcome Measurement: ", "1": " Patients Event-free at 12 Months (Where Event = Death (From … | 2 | 50.0% | 50.0% |
| NCT01830933 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 0/655 (0.00%)", "2": "Adverse Events 2:", "3": " Total: 0… | 1 | 100.0% | 100.0% |
| NCT02273973 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 20/167 (11.98%)", "10": " Postoperative wound infection 2… | 2 | 100.0% | 100.0% |
| NCT02370238 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 13/61 (21.31%)", "10": " Condition aggravated 1/61 (1.64%… | 2 | 50.0% | 50.0% |
| NCT00944047 | {"primary": {"0": "Outcome Measurement: ", "1": " Pathologic Complete Response", "10": " cyclophosphamide: 600… | 2 | 50.0% | 100.0% |
| NCT01125566 | {"primary": {"0": "Inclusion criteria:", "1": " Histologically confirmed diagnosis of HER2-overexpression brea… | 2 | 100.0% | 100.0% |
| NCT00093795 | {"primary": {"0": "Outcome Measurement: ", "1": " Disease-free Survival: Any Recurrence, Contralateral Breast … | 2 | 100.0% | 100.0% |
| NCT00263588 | {"primary": {"0": "Inclusion criteria:", "1": " Signed Informed Consent", "10": "Exclusion criteria:", "11": "… | 2 | 100.0% | 100.0% |
| NCT00733408 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 5/55 (9.09%)", "2": " Infection 2/55 (3.64%)", "3": " Pai… | 2 | 100.0% | 100.0% |
| NCT00091442 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 59/373 (15.82%)", "10": " Cardiac failure congestive 1/37… | 2 | 50.0% | 50.0% |
| NCT00106002 | {"primary": {"0": "INTERVENTION 1: ", "1": " Pemetrexed", "2": " 600 mg/m2, intravenous (IV), every 14 days un… | 1 | 100.0% | 100.0% |
| NCT01912612 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 1/35 (2.86%)", "2": " congestive heart failure *1/35 (2.8… | 2 | 100.0% | 50.0% |
| NCT00617539 | {"primary": {"0": "DISEASE CHARACTERISTICS:", "1": " Histologically or cytologically confirmed breast cancer w… | 2 | 100.0% | 100.0% |
| NCT01644890 | {"primary": {"0": "Outcome Measurement: ", "1": " Progression Free Survival", "10": " Unit of Measure: months … | 2 | 50.0% | 50.0% |
| NCT01011946 | {"primary": {"0": "INTERVENTION 1: ", "1": " Positron Emission Mammography", "2": " Positron Emission Mammogra… | 2 | 100.0% | 100.0% |
| NCT00572728 | {"primary": {"0": "Inclusion Criteria:", "1": " Pathologically confirmed breast cancer, determined to be a can… | 1 | 100.0% | 100.0% |
| NCT02679755 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 18/100 (18.00%)", "10": " Abdominal pain upper * 0/100 (0… | 1 | 100.0% | 100.0% |
| NCT02915744 | {"primary": {"0": "INTERVENTION 1: ", "1": " NKTR-102", "2": " In Group A, NKTR-102 will be administered at a … | 1 | 100.0% | 100.0% |
| NCT00438100 | {"primary": {"0": "Inclusion Criteria:", "1": " Biopsy-diagnosed breast cancer with metastasis in multiple org… | 1 | 100.0% | 100.0% |
| NCT00924352 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 11/56 (19.64%)", "10": " Edema due to Cardiac Disease * 1… | 2 | 100.0% | 100.0% |
| NCT01042535 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 14/41 (34.15%)", "10": " Skin infection 2/41 (4.88%)", "1… | 1 | 100.0% | 100.0% |
| NCT02301988 | {"primary": {"0": "INTERVENTION 1: ", "1": " Ipatasertib + Paclitaxel", "2": " Participants received ipatasert… | 2 | 50.0% | 50.0% |
| NCT00376597 | {"primary": {"0": "Eligibility Criteria:", "1": " Newly diagnosed with stage I-III cancer of the female breast… | 2 | 100.0% | 100.0% |
| NCT00290758 | {"primary": {"0": "Inclusion Criteria:", "1": " No known soy intolerance", "10": " Claus score ＞= 1.0% for wom… | 2 | 50.0% | 50.0% |
| NCT00688909 | {"primary": {"0": "INTERVENTION 1: ", "1": " Letrozole", "2": " Participants received 2.5 milligram (mg) of Le… | 1 | 100.0% | 100.0% |
| NCT00876395 | {"primary": {"0": "Inclusion Criteria:", "1": " Adult Women ( 18 years old).", "10": " Prior mTOR inhibitors f… | 1 | 100.0% | 100.0% |
| NCT02131064 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 70/219 (31.96%)", "10": " Abdominal pain upper * 1/219 (0… | 2 | 100.0% | 50.0% |
| NCT01416389 | {"primary": {"0": "Outcome Measurement: ", "1": " Change in Tumor Size (CTS) From Baseline to the End of Cycle… | 1 | 100.0% | 100.0% |
| NCT01581619 | {"primary": {"0": "Outcome Measurement: ", "1": " Safety of External-beam PBI Utilizing 40Gy in Ten Daily Frac… | 1 | 100.0% | 100.0% |
| NCT02186015 | {"primary": {"0": "Inclusion Criteria:", "1": " Metastatic breast cancer (Stage IV)", "10": " English speaking… | 2 | 100.0% | 100.0% |
| NCT00503750 | {"primary": {"0": "Outcome Measurement: ", "1": " Number of Participants With Complete Pathologic Response.", … | 2 | 100.0% | 100.0% |
| NCT00612560 | {"primary": {"0": "INTERVENTION 1: ", "1": " Arm A - Flaxseed & Active Anastrazole", "2": " 25 mg flaxseed per… | 1 | 100.0% | 100.0% |
| NCT00570921 | {"primary": {"0": "INTERVENTION 1: ", "1": " Fulvestrant + Everolimus", "2": " Fulvestrant + Everolimus", "3":… | 1 | 100.0% | 100.0% |
| NCT01852032 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 0/23 (0.00%)"}, "secondary": {"0": "Adverse Events 1:", "… | 1 | 100.0% | 100.0% |
| NCT01042938 | {"primary": {"0": "Outcome Measurement: ", "1": " Severity of Dermatitis in Radiation Treatment Site in Breast… | 1 | 100.0% | 100.0% |
| NCT00820170 | {"primary": {"0": "Inclusion Criteria:", "1": " Female or male patients with diagnosis of invasive adenocarcin… | 1 | 100.0% | 100.0% |
| NCT00191815 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 6", "10": " Renal failure acute 1/67 (1.49%)", "11": " Pl… | 1 | 100.0% | 100.0% |
| NCT01572727 | {"primary": {"0": "INTERVENTION 1: ", "1": " BKM120 and Paclitaxel", "2": " Adult females with histologically … | 2 | 50.0% | 50.0% |
| NCT00852930 | {"primary": {"0": "Outcome Measurement: ", "1": " LDex Change-", "10": " Unit of Measure: LDex 28.0 (17 to 35)… | 1 | 100.0% | 100.0% |
| NCT01998906 | {"primary": {"0": "INTERVENTION 1: ", "1": " HER2+ TC", "10": " Cycles 1-3 (3-week cycles): doxorubicin 60 mg/… | 1 | 100.0% | 100.0% |
| NCT03098550 | {"primary": {"0": "INTERVENTION 1: ", "1": " Nivolumab + Daratumumab (TNBC)", "2": " Triple-negative breast ca… | 1 | 100.0% | 100.0% |
| NCT00325234 | {"primary": {"0": "Inclusion Criteria:", "1": " Females with histologic or cytologic diagnosis of advanced bre… | 2 | 100.0% | 100.0% |
| NCT00425854 | {"primary": {"0": "Inclusion criteria:", "1": "Inclusion Criteria:", "10": "Exclusion Criteria:", "11": " Acti… | 1 | 0.0% | 0.0% |
| NCT00240071 | {"primary": {"0": "INTERVENTION 1: ", "1": " Avastin (Bevacizumab) Plus Hormone", "2": " All patients received… | 1 | 100.0% | 100.0% |
| NCT00217399 | {"primary": {"0": "Outcome Measurement: ", "1": " Complete Response + Partial Response + Stable Disease ＞ 24 W… | 1 | 100.0% | 0.0% |
| NCT00193037 | {"primary": {"0": "Outcome Measurement: ", "1": " Overall Response Rate (ORR), the Percentage of Patients Who … | 2 | 100.0% | 100.0% |
| NCT00450723 | {"primary": {"0": "Adverse Events 1:", "1": " Total: 0/34 (0.00%)"}, "secondary": {"0": "Adverse Events 1:", "… | 1 | 0.0% | 100.0% |
| NCT00593346 | {"primary": {"0": "Outcome Measurement: ", "1": " Local Control Using Ipsilateral Breast Tumor Recurrence Rate… | 1 | 100.0% | 100.0% |
| NCT00305448 | {"primary": {"0": "Outcome Measurement: ", "1": " Objective Response Rate (ORR)", "10": " Unit of Measure: per… | 2 | 100.0% | 100.0% |
| NCT00374322 | {"primary": {"0": "INTERVENTION 1: ", "1": " Lapatinib 1500 mg", "2": " Participants received lapatinib 1500 m… | 1 | 100.0% | 100.0% |
| NCT00066573 | {"primary": {"0": "Outcome Measurement: ", "1": " Event-free Survival", "10": " Unit of Measure: percentage of… | 1 | 100.0% | 100.0% |
| NCT00856492 | {"primary": {"0": "Outcome Measurement: ", "1": " Number of Patients With Pathological Complete Response Rate"… | 1 | 100.0% | 100.0% |
| NCT00063570 | {"primary": {"0": "Inclusion Criteria:", "1": " Must have received prior chemotherapy with Taxol (paclitaxel) … | 1 | 100.0% | 100.0% |
| NCT00333775 | {"primary": {"0": "INTERVENTION 1: ", "1": " Docetaxel 100 mg/m^2 Plus Placebo", "2": " Participants received … | 1 | 100.0% | 100.0% |
| NCT02924883 | {"primary": {"0": "Inclusion Criteria:", "1": " Archival tumor samples must be obtained from primary and/or me… | 1 | 100.0% | 100.0% |
| NCT00281697 | {"primary": {"0": "Inclusion Criteria:", "1": " Signed informed consent form.", "10": " Prior hormonal therapy… | 1 | 100.0% | 100.0% |
| NCT00290732 | {"primary": {"0": "INTERVENTION 1: ", "1": " Intraductal Arm", "2": " Participants received intraductal admini… | 1 | 100.0% | 100.0% |
| NCT00915603 | {"primary": {"0": "Outcome Measurement: ", "1": " Progression-Free Survival (PFS)", "10": "Results 2: ", "11":… | 1 | 0.0% | 100.0% |
| NCT00127933 | {"primary": {"0": "Inclusion Criteria:", "1": " women ＞=18 years of age;", "2": " newly diagnosed;", "3": " in… | 1 | 100.0% | 100.0% |
