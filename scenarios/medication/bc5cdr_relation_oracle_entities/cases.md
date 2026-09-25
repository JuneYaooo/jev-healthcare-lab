# 化学物致病关系判断：逐案例结果

82 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 17356399 | {"abstract": "Acute encephalopathy and cerebral vasospasm after multiagent chemotherapy including PEG-asparagi… | 4 | 0.0% | 75.0% |
| 15696449 | {"abstract": "Acute renal insufficiency after high-dose melphalan in patients with primary systemic amyloidosi… | 1 | 100.0% | 100.0% |
| 10087562 | {"abstract": "Torsade de pointes ventricular tachycardia during low dose intermittent dobutamine treatment in … | 1 | 100.0% | 100.0% |
| 17151160 | {"abstract": "Randomized comparison of olanzapine versus risperidone for the treatment of first-episode schizo… | 1 | 0.0% | 0.0% |
| 12059909 | {"abstract": "Delayed toxicity of cyclophosphamide on the bladder of DBA/2 and C57BL/6 female mouse. The prese… | 1 | 100.0% | 100.0% |
| 15630069 | {"abstract": "Glucose metabolism in patients with schizophrenia treated with atypical antipsychotic agents: a … | 2 | 100.0% | 100.0% |
| 851038 | {"abstract": "Kaliuretic effect of L-dopa treatment in parkinsonian patients. Hypokalemia, sometimes severe, w… | 1 | 100.0% | 100.0% |
| 6615679 | {"abstract": "Intraoperative bradycardia and hypotension associated with timolol and pilocarpine eye drops. A … | 1 | 100.0% | 100.0% |
| 10726030 | {"abstract": "Clinical aspects of heparin-induced thrombocytopenia and thrombosis and other side effects of he… | 2 | 100.0% | 0.0% |
| 24658375 | {"abstract": "All-trans retinoic acid-induced inflammatory myositis in a patient with acute promyelocytic leuk… | 1 | 100.0% | 100.0% |
| 25951420 | {"abstract": "Associations of Ozone and PM2.5 Concentrations With Parkinson's Disease Among Participants in th… | 1 | 100.0% | 100.0% |
| 24881749 | {"abstract": "Neuroleptic malignant syndrome induced by combination therapy with tetrabenazine and tiapride in… | 1 | 100.0% | 100.0% |
| 15276093 | {"abstract": "Safety and compliance with once-daily niacin extended-release/lovastatin as initial therapy in t… | 2 | 100.0% | 100.0% |
| 16034922 | {"abstract": "Long term hormone therapy for perimenopausal and postmenopausal women. BACKGROUND: Hormone thera… | 3 | 66.7% | 66.7% |
| 24999722 | {"abstract": "Safety and efficacy of fluocinolone acetonide intravitreal implant (0.59 mg) in birdshot retinoc… | 1 | 0.0% | 100.0% |
| 8825380 | {"abstract": "The effect of recombinant human insulin-like growth factor-I on chronic puromycin aminonucleosid… | 1 | 100.0% | 0.0% |
| 26002693 | {"abstract": "1,3-Butadiene, CML and the t(9:22) translocation: A reality check. UNASSIGNED: Epidemiological s… | 1 | 0.0% | 0.0% |
| 11799346 | {"abstract": "Antimicrobial-induced mania (antibiomania): a review of spontaneous reports. The authors reviewe… | 1 | 100.0% | 100.0% |
| 6585590 | {"abstract": "Antitumor effect, cardiotoxicity, and nephrotoxicity of doxorubicin in the IgM solid immunocytom… | 1 | 100.0% | 0.0% |
| 23433219 | {"abstract": "The risk and associated factors of methamphetamine psychosis in methamphetamine-dependent patien… | 1 | 100.0% | 100.0% |
| 19914299 | {"abstract": "Fluoxetine improves the memory deficits caused by the chemotherapy agent 5-fluorouracil. Cancer … | 1 | 100.0% | 100.0% |
| 8667442 | {"abstract": "Milk-alkali syndrome induced by 1,25(OH)2D in a patient with hypoparathyroidism. Milk-alkali syn… | 4 | 50.0% | 50.0% |
| 1760851 | {"abstract": "Reduced cardiotoxicity of doxorubicin given in the form of N-(2-hydroxypropyl)methacrylamide con… | 1 | 100.0% | 100.0% |
| 24091473 | {"abstract": "Resuscitation with lipid, epinephrine, or both in levobupivacaine-induced cardiac toxicity in ne… | 1 | 100.0% | 100.0% |
| 24928523 | {"abstract": "Combination of bortezomib, thalidomide, and dexamethasone (VTD) as a consolidation therapy after… | 1 | 0.0% | 100.0% |
| 8312343 | {"abstract": "Pediatric heart transplantation without chronic maintenance steroids. From 1986 to February 1993… | 1 | 100.0% | 100.0% |
| 18189308 | {"abstract": "p75NTR expression in rat urinary bladder sensory neurons and spinal cord with cyclophosphamide-i… | 1 | 100.0% | 100.0% |
| 1563460 | {"abstract": "Thoracic hematomyelia secondary to coumadin anticoagulant therapy: a case report. A case of thor… | 1 | 100.0% | 100.0% |
| 10985896 | {"abstract": "Phase 2 trial of liposomal doxorubicin (40 mg/m(2)) in platinum/paclitaxel-refractory ovarian an… | 1 | 0.0% | 100.0% |
| 16723784 | {"abstract": "Clinical evaluation of adverse effects during bepridil administration for atrial fibrillation an… | 1 | 100.0% | 100.0% |
| 11745287 | {"abstract": "Phase II study of carboplatin and liposomal doxorubicin in patients with recurrent squamous cell… | 1 | 0.0% | 0.0% |
| 7479194 | {"abstract": "A large population-based follow-up study of trimethoprim-sulfamethoxazole, trimethoprim, and cep… | 1 | 100.0% | 100.0% |
| 3383127 | {"abstract": "Hypotension as a manifestation of cardiotoxicity in three patients receiving cisplatin and 5-flu… | 1 | 100.0% | 100.0% |
| 11105626 | {"abstract": "A case of isotretinoin embryopathy with bilateral anotia and Taussig-Bing malformation. We repor… | 1 | 100.0% | 100.0% |
| 1779253 | {"abstract": "Topical 0.025% capsaicin in chronic post-herpetic neuralgia: efficacy, predictors of response an… | 1 | 100.0% | 0.0% |
| 19515070 | {"abstract": "Intraoperative dialysis during liver transplantation with citrate dialysate. Liver transplantati… | 1 | 100.0% | 100.0% |
| 12165618 | {"abstract": "Persistent sterile leukocyturia is associated with impaired renal function in human immunodefici… | 1 | 100.0% | 100.0% |
| 20447294 | {"abstract": "Studies of synergy between morphine and a novel sodium channel blocker, CNSB002, in rat models o… | 1 | 100.0% | 100.0% |
| 17035713 | {"abstract": "Chloroacetaldehyde as a sulfhydryl reagent: the role of critical thiol groups in ifosfamide neph… | 1 | 100.0% | 100.0% |
| 12523489 | {"abstract": "Cocaine-induced hyperactivity is more influenced by adenosine receptor agonists than amphetamine… | 1 | 0.0% | 0.0% |
| 19815465 | {"abstract": "Binasal visual field defects are not specific to vigabatrin. This study investigated the visual … | 1 | 100.0% | 100.0% |
| 2782734 | {"abstract": "Tachyphylaxis to systemic but not to airway responses during prolonged therapy with high dose in… | 1 | 0.0% | 0.0% |
| 24072398 | {"abstract": "A single neurotoxic dose of methamphetamine induces a long-lasting depressive-like behaviour in … | 1 | 100.0% | 100.0% |
| 16309808 | {"abstract": "Does domperidone potentiate mirtazapine-associated restless legs syndrome? There is now evidence… | 1 | 0.0% | 100.0% |
| 12498738 | {"abstract": "Carvedilol protects against doxorubicin-induced mitochondrial cardiomyopathy. Several cytopathic… | 1 | 0.0% | 0.0% |
| 2429800 | {"abstract": "Histamine antagonists and d-tubocurarine-induced hypotension in cardiac surgical patients. Hemod… | 1 | 0.0% | 100.0% |
| 2710809 | {"abstract": "Bradycardia due to biperiden. In a 38-year-old male patient suffering from a severe postzosteric… | 2 | 0.0% | 50.0% |
| 3323259 | {"abstract": "Differential effects of 1,4-dihydropyridine calcium channel blockers: therapeutic implications. … | 2 | 100.0% | 100.0% |
| 20566328 | {"abstract": "Mitochondrial impairment contributes to cocaine-induced cardiac dysfunction: Prevention by the t… | 1 | 0.0% | 0.0% |
| 17496739 | {"abstract": "Piperacillin/tazobactam-induced seizure rapidly reversed by high flux hemodialysis in a patient … | 1 | 0.0% | 0.0% |
| 1424076 | {"abstract": "Syndrome of inappropriate secretion of antidiuretic hormone after infusional vincristine. A 77-y… | 1 | 0.0% | 100.0% |
| 15096374 | {"abstract": "Induction of rosaceiform dermatitis during treatment of facial inflammatory dermatoses with tacr… | 2 | 100.0% | 50.0% |
| 9061777 | {"abstract": "MK-801 augments pilocarpine-induced electrographic seizure but protects against brain damage in … | 1 | 0.0% | 100.0% |
| 3864191 | {"abstract": "Salicylate nephropathy in the Gunn rat: potential role of prostaglandins. We examined the potent… | 2 | 0.0% | 50.0% |
| 2907577 | {"abstract": "Effect of alkylxanthines on gentamicin-induced acute renal failure in the rat. Adenosine antagon… | 1 | 0.0% | 0.0% |
| 18422462 | {"abstract": "Spectrum of adverse events after generic HAART in southern Indian HIV-infected patients. To dete… | 2 | 100.0% | 100.0% |
| 24742750 | {"abstract": "Availability of human induced pluripotent stem cell-derived cardiomyocytes in assessment of drug… | 1 | 0.0% | 0.0% |
| 24283660 | {"abstract": "Tacrolimus-related seizure after pediatric liver transplantation--a single-center experience. To… | 1 | 0.0% | 0.0% |
| 7411769 | {"abstract": "Indomethacin-induced hyperkalemia in three patients with gouty arthritis. We describe three pati… | 1 | 100.0% | 100.0% |
| 19338378 | {"abstract": "Reducing harm associated with anticoagulation: practical considerations of argatroban therapy in… | 1 | 100.0% | 100.0% |
| 16911931 | {"abstract": "Intramuscular hepatitis B immune globulin combined with lamivudine in prevention of hepatitis B … | 1 | 100.0% | 100.0% |
| 8996419 | {"abstract": "Population-based study of risk of venous thromboembolism associated with various oral contracept… | 1 | 0.0% | 0.0% |
| 20495512 | {"abstract": "Heparin-induced thrombocytopenia: a practical review. Heparin-induced thrombocytopenia (HIT) rem… | 1 | 100.0% | 0.0% |
| 17028363 | {"abstract": "Acute renal failure associated with prolonged intake of slimming pills containing anthraquinones… | 1 | 100.0% | 100.0% |
| 24438483 | {"abstract": "Pre-treatment of bupivacaine-induced cardiovascular depression using different lipid formulation… | 1 | 0.0% | 100.0% |
| 19392810 | {"abstract": "Rhabdomyolysis and brain ischemic stroke in a heroin-dependent male under methadone maintenance … | 2 | 0.0% | 50.0% |
| 19549709 | {"abstract": "Efficacy of everolimus (RAD001) in patients with advanced NSCLC previously treated with chemothe… | 1 | 100.0% | 0.0% |
| 733189 | {"abstract": "Bilateral retinal artery and choriocapillaris occlusion following the injection of long-acting c… | 1 | 0.0% | 0.0% |
| 2453942 | {"abstract": "Convulsant effect of lindane and regional brain concentration of GABA and dopamine. Lindane (gam… | 1 | 0.0% | 100.0% |
| 16083708 | {"abstract": "Drug-induced liver injury: an analysis of 461 incidences submitted to the Spanish registry over … | 1 | 0.0% | 100.0% |
| 7644931 | {"abstract": "Paclitaxel 3-hour infusion given alone and combined with carboplatin: preliminary results of dos… | 1 | 100.0% | 100.0% |
| 12119460 | {"abstract": "High-dose 5-fluorouracil / folinic acid in combination with three-weekly mitomycin C in the trea… | 1 | 100.0% | 100.0% |
| 25907210 | {"abstract": "Incidence of solid tumours among pesticide applicators exposed to the organophosphate insecticid… | 1 | 0.0% | 0.0% |
| 12912689 | {"abstract": "Ocular motility changes after subtenon carboplatin chemotherapy for retinoblastoma. BACKGROUND: … | 1 | 100.0% | 100.0% |
| 24927617 | {"abstract": "Rhabdomyolysis in a hepatitis C virus infected patient treated with telaprevir and simvastatin. … | 2 | 100.0% | 100.0% |
| 19728177 | {"abstract": "Prolonged hypothermia as a bridge to recovery for cerebral edema and intracranial hypertension a… | 1 | 0.0% | 100.0% |
| 753803 | {"abstract": "Experimental progressive muscular dystrophy and its treatment with high doses anabolizing agents… | 1 | 0.0% | 0.0% |
| 6299641 | {"abstract": "Evidence for cardiac beta 2-adrenoceptors in man. We compared the effects of single doses of 50 … | 1 | 100.0% | 100.0% |
| 24434397 | {"abstract": "Tranexamic acid overdosage-induced generalized seizure in renal failure. We report a 45-year-old… | 1 | 0.0% | 0.0% |
| 25006961 | {"abstract": "Absence of PKC-alpha attenuates lithium-induced nephrogenic diabetes insipidus. Lithium, an effe… | 1 | 0.0% | 0.0% |
| 24675088 | {"abstract": "An integrated characterization of serological, pathological, and functional events in doxorubici… | 1 | 0.0% | 0.0% |
| 3375885 | {"abstract": "Hyperkalemia induced by indomethacin and naproxen and reversed by fludrocortisone. We have descr… | 1 | 0.0% | 0.0% |
