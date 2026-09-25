# 患者问题信息需求分类：逐案例结果

98 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0003593.xml | What are the treatments for Liddle syndrome ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0001302.xml | Do I need to see a doctor for Duodenal atresia ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0002224.xml | Do you have information about Intravenous… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/11_MPlusDrugs_QA/0000591.xml | Who should get Hydromorphone Rectal and why is it prescribed ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0001900.xml | What are the treatments for Dominant optic atrophy ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/1_CancerGov_QA/0000019_2.xml | What is (are) Ovarian Germ Cell Tumors ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0001813.xml | Do you have information about Haptoglobin blood test… | 1 | 0.0% | 0.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0001094.xml | What are the symptoms of Charcot-Marie-Tooth disease type 1E ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0002514.xml | What are the treatments for Mallory-Weiss tear ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000705.xml | What is the outlook for Cat-scratch disease ?… | 2 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/1_CancerGov_QA/0000024_7.xml | What are the treatments for Paranasal Sinus and Nasal Cavity Cancer ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0004316.xml | What causes Wilms tumor ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/4_MPlus_Health_Topics_QA/0000144.xml | What is (are) Cancer in Children ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/3_GHR_QA/0000103.xml | What is (are) autosomal recessive spastic ataxia of Charlevoix-Saguenay ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0004005.xml | What causes Microcephalic osteodysplastic primordial dwarfism type 1 ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0002071.xml | Do I need to see a doctor for Hyperaldosteronism - primary and secondary ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/1_CancerGov_QA/0000003_3.xml | What are the treatments for Kaposi Sarcoma ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0004129.xml | What is the outlook for Urination - painful ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0002945.xml | What is (are) Parainfluenza ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0002561.xml | Is Glass-Chapman-Hockley syndrome inherited ?… | 2 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0002794.xml | What is (are) Newborn jaundice ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0002152.xml | What are the symptoms of Impacted tooth ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0001755.xml | How to diagnose Gonococcal arthritis ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/8_NHLBI_QA_XML/0000066.xml | What is (are) Heart Valve Disease ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000877.xml | What is the outlook for Clubfoot repair ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0001937.xml | What are the symptoms of Duodenal atresia ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000212.xml | What causes Anemia ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0002892.xml | Do you have information about Ostomy - resources… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/11_MPlusDrugs_QA/0001119.xml | Are there safety concerns or special precautions about Sitagliptin ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0005542.xml | What are the symptoms of Senior Loken Syndrome ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0003913.xml | How to diagnose Throat or larynx cancer ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/11_MPlusDrugs_QA/0000558.xml | Are there safety concerns or special precautions about Glyburide and Metformin ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/11_MPlusDrugs_QA/0001023.xml | What other information should I know about Prochlorperazine ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0002367.xml | What are the symptoms of Fibrodysplasia ossificans progressiva ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0003105.xml | How to diagnose Plague ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0003306.xml | What causes Jones syndrome ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0001136.xml | What causes Chiari malformation type 1 ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0003520.xml | What are the symptoms of Leber hereditary optic neuropathy ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/6_NINDS_QA/0000152.xml | What is the outlook for Huntington's Disease ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0002001.xml | What are the symptoms of Dystonia 8 ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/11_MPlusDrugs_QA/0001181.xml | Who should get Terbutaline and why is it prescribed ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000842.xml | Do I need to see a doctor for Chronic motor tic disorder ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/11_MPlusDrugs_QA/0000779.xml | What other information should I know about Methyldopa ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/6_NINDS_QA/0000212.xml | What is (are) Neurofibromatosis ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0002772.xml | How to diagnose Nephrocalcinosis ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0004143.xml | Do you have information about Urine pH test… | 1 | 0.0% | 0.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/3_GHR_QA/0000785.xml | Is Perrault syndrome inherited ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000739.xml | What causes Cerebral palsy ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0001743.xml | What is the outlook for Glossitis ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/11_MPlusDrugs_QA/0000748.xml | Are there safety concerns or special precautions about Megestrol ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0002219.xml | What is (are) Intraductal papilloma ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0003234.xml | What causes Prolactinoma ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000395.xml | What is (are) Barbiturate intoxication and overdose ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000712.xml | How to diagnose Catheter-related UTI ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/3_GHR_QA/0000548.xml | What are the treatments for juvenile myoclonic epilepsy ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000128.xml | Do you have information about Aging changes in the senses… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0003246.xml | Do you have information about Prostate cancer screenings… | 1 | 0.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0002109.xml | What causes Hypothalamic dysfunction ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/3_GHR_QA/0000031.xml | What is (are) Alexander disease ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000670.xml | What are the treatments for Canker sore ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0003054.xml | What is (are) Hypohidrotic ectodermal dysplasia ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0001446.xml | What are the symptoms of Common variable immunodeficiency ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0003210.xml | What is (are) Pressure ulcers - what to ask your doctor ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/4_MPlus_Health_Topics_QA/0000290.xml | What is (are) Disabilities ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/4_MPlus_Health_Topics_QA/0000787.xml | What is (are) Rubella ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0003153.xml | How to diagnose Polymyositis - adult ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/3_GHR_QA/0000312.xml | Is early-onset primary dystonia inherited ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0004441.xml | What are the treatments for Non-involuting congenital hemangioma ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0006564.xml | What are the symptoms of 19p13.12 microdeletion syndrome ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0003708.xml | What are the symptoms of Stasis dermatitis and ulcers ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/11_MPlusDrugs_QA/0000710.xml | What are the side effects or risks of Liotrix ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000017.xml | What is (are) Abdominal pain - children under age 12 ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000442.xml | How to diagnose Biliary stricture ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/11_MPlusDrugs_QA/0000800.xml | What are the side effects or risks of Mifepristone (Mifeprex) ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0001655.xml | What are the symptoms of Fungal arthritis ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000771.xml | Do I need to see a doctor for Chemosis ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/7_SeniorHealth_QA/0000006.xml | What are the treatments for Balance Problems ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0000308.xml | What are the symptoms of Amyotonia congenita ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0004740.xml | What are the symptoms of Parkinson disease ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/6_NINDS_QA/0000045.xml | What is the outlook for Pseudotumor Cerebri ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0001854.xml | How to diagnose Heart attack ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0000147.xml | What is (are) Adenocarcinoma of the appendix ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0004159.xml | What is (are) Mucopolysaccharidosis type IIIB ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000992.xml | What are the symptoms of Corns and calluses ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0000086.xml | What are the treatments for Addison disease ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/11_MPlusDrugs_QA/0000270.xml | Who should get Clioquinol Topical and why is it prescribed ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0001983.xml | What are the symptoms of Dyssegmental dysplasia Silverman-Handmaker type ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/9_CDC_QA/0000087.xml | How to diagnose Crimean-Congo Hemorrhagic Fever (CCHF) ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/11_MPlusDrugs_QA/0000540.xml | Are there safety concerns or special precautions about Furosemide ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0002085.xml | What are the symptoms of Hypersensitivity pneumonitis ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/4_MPlus_Health_Topics_QA/0000035.xml | What is (are) Anesthesia ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0001269.xml | Do you have information about Doppler ultrasound exam of an arm or leg… | 1 | 0.0% | 0.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0000993.xml | What are the symptoms of Cataract congenital Volkmann type ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/2_GARD_QA/0001395.xml | What are the symptoms of Cockayne syndrome ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0001284.xml | What is (are) Drug allergies ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/10_MPlus_ADAM_QA/0001903.xml | What are the symptoms of Hemochromatosis ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/3_GHR_QA/0001081.xml | Is 2-hydroxyglutaric aciduria inherited ?… | 1 | 100.0% | 100.0% |
| /Users/june/Documents/Codex/2026-09-23/github-x20/work/medical-bench/more/MedQuAD/11_MPlusDrugs_QA/0001133.xml | What other information should I know about Spironolactone ?… | 1 | 100.0% | 100.0% |
