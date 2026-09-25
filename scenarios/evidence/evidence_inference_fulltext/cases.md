# 临床研究干预结果方向：逐案例结果

84 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 5789513 | {"Comparator": "Group II -IV amikacin 20 mg/kg/24 h and meropenem 2 g over 30 min/8 h in addition to nebulized… | 1 | 100.0% | 100.0% |
| 3936115 | {"Comparator": "control group was administered placebo", "Intervention": "Microencapsulated sodium butyrate (M… | 1 | 100.0% | 100.0% |
| 4190894 | {"Comparator": "Control", "Intervention": "Dexmedetomidine ", "Outcome": "Brain-derived neurotrophic factor 10… | 2 | 100.0% | 100.0% |
| 1569640 | {"Comparator": "gliclazide", "Intervention": "nateglinide", "Outcome": "The postprandial glucose AUC0−4 h", "a… | 1 | 100.0% | 100.0% |
| 3757635 | {"Comparator": "absorbable sutures", "Intervention": "autologous cryoprecipitate", "Outcome": "intraoperative … | 1 | 100.0% | 100.0% |
| 5656289 | {"Comparator": "AC (attention control) group (healthy aging education)", "Intervention": "LISTEN group (Loneli… | 1 | 100.0% | 0.0% |
| 3659039 | {"Comparator": "without (control group) omega-3 PUFAs", "Intervention": "72 hour infusion of total parenteral … | 2 | 100.0% | 50.0% |
| 4274041 | {"Comparator": "Amorphous rifaximin 200 mg", "Intervention": "Polymorph alpha rifaximin 200 mg", "Outcome": "A… | 2 | 100.0% | 0.0% |
| 5600923 | {"Comparator": "Placebo (CG group)", "Intervention": "Alginate oligosaccharide (AOS; AG group)", "Outcome": "L… | 2 | 50.0% | 100.0% |
| 5551214 | {"Comparator": "control group", "Intervention": "horse riding intervention", "Outcome": "the Aberrant Behaviou… | 1 | 0.0% | 0.0% |
| 4145879 | {"Comparator": "Control", "Intervention": "Transcranial direct-current stimulation condition", "Outcome": "Go … | 2 | 100.0% | 100.0% |
| 4663612 | {"Comparator": "Caffeine", "Intervention": "Theacrine", "Outcome": "Depressed condition", "article": "TITLE: C… | 2 | 100.0% | 0.0% |
| 5498678 | {"Comparator": "Vycross® 20 mg/ml HA gel (VYC-20)", "Intervention": "Cohesive Polydensified Matrix® 26 mg/mL H… | 1 | 100.0% | 100.0% |
| 4836696 | {"Comparator": "placebo", "Intervention": "GSK457 (10% w/w) combined with the exendin-4 AlbudAb", "Outcome": "… | 1 | 100.0% | 0.0% |
| 3571894 | {"Comparator": "Busulfan plus fludarabine", "Intervention": "Busulfan plus cyclophosphamide ", "Outcome": "Cit… | 1 | 100.0% | 100.0% |
| 4868921 | {"Comparator": "Control", "Intervention": "Learning therapy", "Outcome": "Performance in Stroop", "article": "… | 2 | 100.0% | 100.0% |
| 5835896 | {"Comparator": "patients without HLA-A*2402", "Intervention": "patients with HLA-A*2402", "Outcome": "Number o… | 1 | 100.0% | 100.0% |
| 1871574 | {"Comparator": "Usual care", "Intervention": "Smoking cessation advice and NRT offered", "Outcome": "Baseline … | 3 | 100.0% | 100.0% |
| 5599448 | {"Comparator": "Pirfenidone capsules", "Intervention": "Pirfenidone tablet", "Outcome": "AUC 0–∞ ", "article":… | 1 | 100.0% | 100.0% |
| 3159986 | {"Comparator": "Baseline characteristics", "Intervention": "Respiratory muscle endurance training", "Outcome":… | 1 | 100.0% | 100.0% |
| 5746709 | {"Comparator": "other treatment", "Intervention": "isolated lumbar extension", "Outcome": "pain", "article": "… | 1 | 0.0% | 0.0% |
| 4076224 | {"Comparator": "Risk assessment + a nasal flow monitor", "Intervention": "Risk assessment ", "Outcome": "Compl… | 1 | 100.0% | 100.0% |
| 4674480 | {"Comparator": "Basal bolus", "Intervention": "Insulin degludec and liraglutide", "Outcome": "Systolic blood p… | 1 | 100.0% | 0.0% |
| 5057302 | {"Comparator": "Placebo", "Intervention": "Sublingual immunotherapy (SLIT) 40 000 AUN/ml", "Outcome": "Improve… | 2 | 100.0% | 100.0% |
| 4745915 | {"Comparator": "sedentary control group", "Intervention": "12-week combined exercise program", "Outcome": "abs… | 1 | 100.0% | 100.0% |
| 5244277 | {"Comparator": "mometasone furoate nasal spray", "Intervention": "fluticasone furoate nasal spray", "Outcome":… | 1 | 100.0% | 100.0% |
| 4824463 | {"Comparator": "Clinical judgement", "Intervention": "Rapid diagnostic tests", "Outcome": "Incidence of the ov… | 1 | 100.0% | 100.0% |
| 4598102 | {"Comparator": "No additional treatment", "Intervention": "Adjunctive aripiprazole", "Outcome": "PANSS-negativ… | 1 | 100.0% | 0.0% |
| 4759876 | {"Comparator": "intraarticular indwelling closed suction drainage method", "Intervention": "subcutaneous indwe… | 1 | 100.0% | 100.0% |
| 5852933 | {"Comparator": "no dentin pretreatment done or dentin pretreatment with 6.5% proanthocyanidin (PA) for 5 min (… | 1 | 100.0% | 100.0% |
| 3333807 | {"Comparator": "Control", "Intervention": "Aliskiren", "Outcome": "Plasma renin activity", "article": "TITLE: … | 1 | 100.0% | 0.0% |
| 3872585 | {"Comparator": " intravenous acetaminophen", "Intervention": "intravenous morphine", "Outcome": "the mean of p… | 1 | 100.0% | 0.0% |
| 5292014 | {"Comparator": "Routine treatment", "Intervention": "Educational intervention", "Outcome": "Improvement in mea… | 2 | 100.0% | 100.0% |
| 1713239 | {"Comparator": "placebo", "Intervention": "budesonide/formoterol and salbutamol", "Outcome": "Borg score", "ar… | 1 | 100.0% | 0.0% |
| 4143738 | {"Comparator": "previous-evening (PM) PEG solutio", "Intervention": "morning (AM) PEG (polyethylene glycol) so… | 1 | 100.0% | 100.0% |
| 4558453 | {"Comparator": "No exercise", "Intervention": "Exercise of moderate intensity", "Outcome": "Assessment of Ment… | 1 | 100.0% | 100.0% |
| 4435250 | {"Comparator": "Men's Health CoOp/Women's Health CoOp [MHC/WHC]", "Intervention": "Couples Health CoOp [CHC]",… | 2 | 100.0% | 100.0% |
| 2784386 | {"Comparator": "liposomal amphotericin B (3 mg/kg/day)", "Intervention": "micafungin (100 mg/day for subjects … | 1 | 100.0% | 100.0% |
| 4755968 | {"Comparator": "virtual-reality (VR) balance training", "Intervention": "Biodex Balance System (BBS) balance t… | 1 | 0.0% | 0.0% |
| 3883373 | {"Comparator": "Antibiotics alone ", "Intervention": "Probiotics + antibiotics ", "Outcome": "Afebrile urianry… | 1 | 100.0% | 100.0% |
| 4424841 | {"Comparator": "Control", "Intervention": "Transcranial alternating current stimulation", "Outcome": "Task per… | 2 | 50.0% | 50.0% |
| 3162205 | {"Comparator": "Autograft alone", "Intervention": "Porous β-calcium pyrophosphate (β-CPP) plus autograft", "Ou… | 2 | 50.0% | 50.0% |
| 5816528 | {"Comparator": "flapless surgical intervention ", "Intervention": "piezocision or laser-assisted flapless cort… | 1 | 100.0% | 100.0% |
| 5409660 | {"Comparator": "Cooked ham", "Intervention": "Dry-cured ham", "Outcome": "Monocyte Chemoattractant Protein-1",… | 1 | 100.0% | 100.0% |
| 4744955 | {"Comparator": "Control", "Intervention": "Lauroyl arginate‐containing mouthrinse ", "Outcome": "Adverse event… | 1 | 100.0% | 100.0% |
| 5153622 | {"Comparator": "placebo ", "Intervention": "onabotulinumtoxinA (100 U)", "Outcome": "International Prostate Sy… | 1 | 0.0% | 0.0% |
| 3925077 | {"Comparator": "placebo", "Intervention": "low dose penicillin V", "Outcome": "probability of antibiotic proph… | 1 | 100.0% | 100.0% |
| 5947263 | {"Comparator": "Approved inhaler", "Intervention": "Procaterol hydrochloride inhaler", "Outcome": "Period effe… | 1 | 100.0% | 100.0% |
| 2361654 | {"Comparator": "cytological screening", "Intervention": "primary hrHPV screening", "Outcome": "colposcopy refe… | 1 | 100.0% | 100.0% |
| 4893758 | {"Comparator": "Fentanyl/midazolam", "Intervention": "Remifentanil ", "Outcome": "Respiratory adverse events",… | 1 | 100.0% | 100.0% |
| 5047648 | {"Comparator": "healthy women (CON)", "Intervention": "women with Fibromyalgia syndrome (FMS)", "Outcome": "in… | 1 | 100.0% | 100.0% |
| 1783667 | {"Comparator": "baseline", "Intervention": "comprehensive lifestyle intervention study", "Outcome": "Positive … | 1 | 0.0% | 0.0% |
| 3021887 | {"Comparator": "placebo", "Intervention": "rimonabant 20 mg", "Outcome": "weight", "article": "TITLE: Perspect… | 1 | 100.0% | 0.0% |
| 5799931 | {"Comparator": "Group B: 0.2 mg GnRHa 35 h prior to oocyte retrieval + repeat dose of 0.1 mg 12 h following th… | 1 | 100.0% | 100.0% |
| 5880517 | {"Comparator": "nonpainful analogs to these testing procedures", "Intervention": "moderately painful Quantitat… | 1 | 100.0% | 100.0% |
| 4296355 | {"Comparator": "Ropivacaine plus clonidine (group B)", "Intervention": "Ropivacaine (group A)", "Outcome": "On… | 1 | 100.0% | 100.0% |
| 4889182 | {"Comparator": "no social media exposure (control)", "Intervention": "social media exposure", "Outcome": "numb… | 1 | 100.0% | 100.0% |
| 4968528 | {"Comparator": "diabetes mellitus patients without neuropathy (GI)", "Intervention": "diabetic peripheral neur… | 1 | 100.0% | 100.0% |
| 4249579 | {"Comparator": "primaquine phosphate", "Intervention": "primaquine phosphate and dihydroartemisinin-piperaquin… | 1 | 100.0% | 100.0% |
| 4258972 | {"Comparator": "clonidine (Group 2)", "Intervention": "midazolam (Group 1)", "Outcome": "consumption of propof… | 2 | 100.0% | 100.0% |
| 4109867 | {"Comparator": "basal diet", "Intervention": "2% seamustard", "Outcome": "IgG concentrations", "article": "TIT… | 1 | 100.0% | 100.0% |
| 2361948 | {"Comparator": "palliative radiotherapy schedules for inoperable symptomatic non-small-cell lung cancer 16 Gy/… | 1 | 100.0% | 100.0% |
| 3406192 | {"Comparator": "Benign result", "Intervention": "Prostate cancer", "Outcome": "PSA change ratio", "article": "… | 1 | 0.0% | 100.0% |
| 5411411 | {"Comparator": "group II included patients who were examined using conventional variable stiffness colonoscopi… | 1 | 100.0% | 0.0% |
| 5873424 | {"Comparator": "placebo tablets", "Intervention": "paracetamol/buprenorphine", "Outcome": "total sleep time", … | 1 | 0.0% | 0.0% |
| 4286912 | {"Comparator": "PHiD-CV Commercial lot (Com group)", "Intervention": "PHiD-CV Phase III Clinical (Clin group)"… | 2 | 100.0% | 100.0% |
| 4367028 | {"Comparator": "Trendelenburg (TBG) tilt ＜30°", "Intervention": "Trendelenburg (TBG) tilt ＞30°", "Outcome": "N… | 1 | 100.0% | 100.0% |
| 4513485 | {"Comparator": "UK Lung Cancer Screening (UKLS) among highest socioeconomic group", "Intervention": "UK Lung C… | 1 | 100.0% | 100.0% |
| 4218710 | {"Comparator": "traditional surgery group (group B)", "Intervention": "endoscopy procedure group (group A)", "… | 1 | 100.0% | 100.0% |
| 32174 | {"Comparator": "control", "Intervention": "patient-held record (PHR)", "Outcome": "number of patients who felt… | 1 | 100.0% | 100.0% |
| 2858204 | {"Comparator": "placebo", "Intervention": "HBOT ", "Outcome": "downsizing of ucler area 2 weeks after treatmen… | 1 | 100.0% | 100.0% |
| 3682293 | {"Comparator": "propofol", "Intervention": "sevoflurane", "Outcome": "postoperative pulmonary complications af… | 1 | 100.0% | 100.0% |
| 3843300 | {"Comparator": "control group", "Intervention": "N-acetylcysteine (NAC) (150 mg/kg)", "Outcome": "creatinine (… | 1 | 100.0% | 100.0% |
| 3714019 | {"Comparator": "non–erythropoiesis-stimulating agent (ESA)", "Intervention": "epoetin alfa", "Outcome": "numbe… | 1 | 100.0% | 0.0% |
| 3199893 | {"Comparator": "placebo", "Intervention": "rivastigmine", "Outcome": "AD Cooperative Study-Activities of Daily… | 1 | 100.0% | 100.0% |
| 3646538 | {"Comparator": "placebo", "Intervention": "mometasone furoate nasal spray (MFNS) 100 μg", "Outcome": "congesti… | 1 | 100.0% | 0.0% |
| 4918678 | {"Comparator": "nothing", "Intervention": "soundfield amplification devices in the classroom", "Outcome": "Sil… | 1 | 100.0% | 100.0% |
| 3311713 | {"Comparator": "NOEX no-exercise treatment for the regain (+50% of weight lost) phase", "Intervention": "EX ex… | 1 | 100.0% | 100.0% |
| 5836868 | {"Comparator": "placebo", "Intervention": "alogliptin", "Outcome": "HbA1c level", "article": "Aims\r\nTo inves… | 1 | 100.0% | 100.0% |
| 5551190 | {"Comparator": "Nature-based images", "Intervention": "Self-selected entertainment", "Outcome": "Distance ran"… | 1 | 100.0% | 100.0% |
| 4836241 | {"Comparator": "baseline", "Intervention": "Kuntai, Tibolone, Control", "Outcome": "follicle-stimulating hormo… | 1 | 0.0% | 100.0% |
| 5511020 | {"Comparator": "Placebo", "Intervention": "Glycopyrronium bromide 50 μg", "Outcome": "FEV1", "article": "TITLE… | 1 | 100.0% | 100.0% |
| 5541727 | {"Comparator": "Control", "Intervention": "Allogeneic mesenchymal precursor cells", "Outcome": "SF-36 bodily p… | 1 | 100.0% | 100.0% |
| 5940475 | {"Comparator": "7 in the chest expansion exercise with placebo TENS (control group)", "Intervention": "7 in th… | 1 | 100.0% | 100.0% |
