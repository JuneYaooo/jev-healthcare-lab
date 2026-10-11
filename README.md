# Jev Healthcare Lab

用于逐任务比较 **JEV 与其他模型的医疗决策质量和运行耗时**。评测任务提供材料、规则或候选项，要求输出可计分的选择，覆盖临床方案选择及其所需的信息判断；不包含病历生成、自由问答或建议生成任务。

**目前覆盖 8 个医疗场景、9 个能力维度、89 个任务定义。** 其中 73 个任务已有数据，共 5,907 题（中文 1,191 题）；53 个任务各 100 题，20 个任务保留实际数量，16 个任务待补数据。实际采用 34 个上游来源。当前尚未发布模型得分或耗时结果。

[场景与任务](#场景与任务) · [能力维度](#能力维度) · [模型得分与耗时对比](#模型得分与耗时对比) · [下载与使用](#下载与使用)

## 如何组织评测

**场景**说明任务发生在医疗流程的哪个环节；**能力维度**说明任务考查什么判断能力；**任务**是抽样、评分和耗时比较的基本单位。每个任务归属一个主要场景，可以同时带有多个能力维度。不同疾病或语言的同类题目不单独计为新任务。

## 能力维度

下表统计当前已有数据的任务；同一任务可出现在多个维度，任务数不能相加作为总数。待补任务仍保留在后面的场景目录中。

| 能力维度 | 考查内容 | 有题任务数 |
| --- | --- | ---: |
| 事实与状态 | 判断否定、不确定、时间和执行状态。 | 5 |
| 关联与匹配 | 判断药物、剂量、检验、事件等信息之间的对应关系。 | 17 |
| 分类与标准化 | 将给定材料归入明确类别或标准化结果。 | 8 |
| 规则与数值 | 依据量表、区间或条件完成数值与规则判断。 | 7 |
| 证据与一致性 | 定位证据，判断论断支持关系及叙述错误。 | 9 |
| 资格与适宜性 | 判断入排条件、禁忌和患者适用性。 | 7 |
| 风险与升级 | 判断风险等级、结局或处理优先级。 | 8 |
| 流程与下一步行动 | 选择护理、执行、随访等环节的行动。 | 10 |
| 临床候选方案 | 在给定候选中选择诊断、检查、治疗或其他临床方案。 | 16 |

## 场景与任务

| 医疗场景 | 有题任务 / 定义任务 | 题数 |
| --- | ---: | ---: |
| [接诊与分诊](#接诊与分诊) | 6 / 7 | 530 |
| [检查与检验](#检查与检验) | 6 / 10 | 556 |
| [诊断与鉴别](#诊断与鉴别) | 13 / 14 | 1,300 |
| [治疗与用药](#治疗与用药) | 13 / 16 | 943 |
| [住院与护理](#住院与护理) | 11 / 14 | 641 |
| [出院与随访](#出院与随访) | 6 / 8 | 234 |
| [临床试验筛选](#临床试验筛选) | 8 / 8 | 800 |
| [病历与医疗质量控制](#病历与医疗质量控制) | 10 / 12 | 903 |

下面完整列出 89 个任务。来源后的数字是该任务实际收录的题数，链接指向上游数据集；**†** 表示非商业研究附加来源。题数为 0 的任务没有纳入评分，候选数据源不作为已收录来源展示。任务名称链接到对应的数据目录，括号内为评分和结果关联使用的任务 ID。

### 接诊与分诊

识别就诊诉求、资料缺口及处理优先级。

| 任务（ID） | 能力维度 | 题数 | 数据集来源（题数） |
| --- | --- | ---: | --- |
| [事实主体归属](benchmarks/medical_decision_v1/tasks/experiencer)（`experiencer`） | 事实与状态 | 100 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)†（100） |
| [医疗问题意图](benchmarks/medical_decision_v1/tasks/query_intent)（`query_intent`） | 分类与标准化 | 100 | [MedQuAD](https://github.com/abachaa/MedQuAD)（100） |
| [决策资料充分性](benchmarks/medical_decision_v1/tasks/input_sufficiency)（`input_sufficiency`） | 规则与数值 | 100 | [LongHealth](https://github.com/kbressem/LongHealth)（100） |
| [当前分诊与升级行动](benchmarks/medical_decision_v1/tasks/triage_urgency)（`triage_urgency`） | 风险与升级 | 100 | [CARE-Bench](https://github.com/ningkko/CARE-bench)†（100） |
| [候选科室分流](benchmarks/medical_decision_v1/tasks/department_routing)（`department_routing`） | 临床候选方案 | 0 | 待补数据 |
| [患者消息紧急性比较](benchmarks/medical_decision_v1/tasks/message_urgency_pair)（`message_urgency_pair`） | 风险与升级 | 30 | [PMR-Synth annotated pairs](https://huggingface.co/datasets/PortalPal-AI/PMP-Synth-AllPairs-Annotated)†（30） |
| [孕产风险等级识别](benchmarks/medical_decision_v1/tasks/maternal_risk)（`maternal_risk`） | 风险与升级 | 100 | [Maternal Health Risk](https://archive.ics.uci.edu/dataset/863/maternal+health+risk)（100） |

### 检查与检验

选择检查、关联结果并判断结果的适用性与处理需求。

| 任务（ID） | 能力维度 | 题数 | 数据集来源（题数） |
| --- | --- | ---: | --- |
| [检查检验数值关联](benchmarks/medical_decision_v1/tasks/lab_link)（`lab_link`） | 关联与匹配、证据与一致性 | 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)（100） |
| [标本身份与来源链](benchmarks/medical_decision_v1/tasks/specimen_lineage)（`specimen_lineage`） | 关联与匹配 | 0 | 待补数据 |
| [数值与单位等价](benchmarks/medical_decision_v1/tasks/unit_equivalence)（`unit_equivalence`） | 规则与数值 | 0 | 待补数据 |
| [参考区间适用性](benchmarks/medical_decision_v1/tasks/reference_range)（`reference_range`） | 规则与数值 | 72 | [LabQAR](https://doi.org/10.6084/m9.figshare.29189894)（72） |
| [临床事件变化趋势](benchmarks/medical_decision_v1/tasks/result_trend)（`result_trend`） | 事实与状态 | 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)（100） |
| [危急结果与人工升级](benchmarks/medical_decision_v1/tasks/critical_result_escalation)（`critical_result_escalation`） | 风险与升级 | 0 | 待补数据 |
| [报告阶段与效力](benchmarks/medical_decision_v1/tasks/report_stage)（`report_stage`） | 流程与下一步行动 | 0 | 待补数据 |
| [检查方案选择](benchmarks/medical_decision_v1/tasks/examination_choice)（`examination_choice`） | 临床候选方案 | 100 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（19）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（81） |
| [检验数值高低判读](benchmarks/medical_decision_v1/tasks/lab_value_classification)（`lab_value_classification`） | 规则与数值 | 100 | [LabQAR](https://doi.org/10.6084/m9.figshare.29189894)（100） |
| [药物基因检测功能表型判定](benchmarks/medical_decision_v1/tasks/pgx_function_phenotype)（`pgx_function_phenotype`） | 分类与标准化 | 84 | [CPIC curated pharmacogenomic tables](https://www.clinpgx.org/cpic)（84） |

### 诊断与鉴别

根据已有材料判断诊断、状态和临床分级。

| 任务（ID） | 能力维度 | 题数 | 数据集来源（题数） |
| --- | --- | ---: | --- |
| [否定与不确定状态](benchmarks/medical_decision_v1/tasks/assertion_scope)（`assertion_scope`） | 事实与状态 | 100 | [NUBes SAMPLE-001](https://github.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus)（100） |
| [事件与文档时间关系](benchmarks/medical_decision_v1/tasks/temporality)（`temporality`） | 事实与状态 | 100 | [E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus)†（100） |
| [诊断核实状态](benchmarks/medical_decision_v1/tasks/diagnosis_verification)（`diagnosis_verification`） | 事实与状态 | 0 | 待补数据 |
| [有界临床量表评分](benchmarks/medical_decision_v1/tasks/bounded_score)（`bounded_score`） | 规则与数值、证据与一致性 | 100 | [MedCalc-Bench GitHub test release](https://github.com/ncbi-nlp/MedCalc-Bench)（100） |
| [临床分级与分期选择](benchmarks/medical_decision_v1/tasks/clinical_grade)（`clinical_grade`） | 规则与数值 | 100 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（70）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（30） |
| [模拟病例主诊断选择](benchmarks/medical_decision_v1/tasks/synthetic_diagnosis)（`synthetic_diagnosis`） | 临床候选方案 | 100 | [DDXPlus](https://doi.org/10.6084/m9.figshare.20043374)（100） |
| [临床病例候选诊断](benchmarks/medical_decision_v1/tasks/diagnosis_choice)（`diagnosis_choice`） | 临床候选方案 | 100 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（50）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（50） |
| [中医证型选择](benchmarks/medical_decision_v1/tasks/tcm_syndrome)（`tcm_syndrome`） | 临床候选方案 | 100 | [TCM-SD](https://github.com/borororo/zy-bert)†（100） |
| [临床事件先后关系](benchmarks/medical_decision_v1/tasks/event_temporal_order)（`event_temporal_order`） | 关联与匹配 | 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)（100） |
| [临床事件与解剖部位关联](benchmarks/medical_decision_v1/tasks/anatomical_site_link)（`anatomical_site_link`） | 关联与匹配 | 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)（100） |
| [严重程度与临床事件关联](benchmarks/medical_decision_v1/tasks/severity_link)（`severity_link`） | 关联与匹配 | 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)（100） |
| [事件与时间表达关联](benchmarks/medical_decision_v1/tasks/event_date_link)（`event_date_link`） | 关联与匹配 | 100 | [E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus)†（85）；[MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)（15） |
| [病例病因与原因判断](benchmarks/medical_decision_v1/tasks/case_etiology)（`case_etiology`） | 临床候选方案 | 100 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（50）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（50） |
| [中医病机候选核验](benchmarks/medical_decision_v1/tasks/tcm_pathogenesis_candidate)（`tcm_pathogenesis_candidate`） | 分类与标准化 | 100 | [TCMEval-SDT](https://doi.org/10.6084/m9.figshare.27184596.v5)（100） |

### 治疗与用药

判断治疗选择、用药关系及患者特异性适宜性。

| 任务（ID） | 能力维度 | 题数 | 数据集来源（题数） |
| --- | --- | ---: | --- |
| [用药状态与变更](benchmarks/medical_decision_v1/tasks/medication_status)（`medication_status`） | 事实与状态 | 0 | 待补数据 |
| [药物相互作用关系](benchmarks/medical_decision_v1/tasks/drug_interaction)（`drug_interaction`） | 关联与匹配 | 100 | [DDI Corpus 2013](https://github.com/isegura/DDICorpus)†（100） |
| [药物与剂量关联](benchmarks/medical_decision_v1/tasks/dose_link)（`dose_link`） | 关联与匹配、证据与一致性 | 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)（100） |
| [患者特异性禁忌选择](benchmarks/medical_decision_v1/tasks/patient_contraindication)（`patient_contraindication`） | 资格与适宜性 | 54 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（33）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（21） |
| [剂量适宜性](benchmarks/medical_decision_v1/tasks/dose_appropriateness)（`dose_appropriateness`） | 资格与适宜性 | 0 | 待补数据 |
| [治疗方案选择](benchmarks/medical_decision_v1/tasks/treatment_choice)（`treatment_choice`） | 临床候选方案 | 100 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（46）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（54） |
| [用药方案选择](benchmarks/medical_decision_v1/tasks/medication_choice)（`medication_choice`） | 临床候选方案 | 100 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（12）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（88） |
| [治疗相关不良事件预测](benchmarks/medical_decision_v1/tasks/adverse_event_prediction)（`adverse_event_prediction`） | 风险与升级 | 0 | 待补数据 |
| [给药途径关联](benchmarks/medical_decision_v1/tasks/route_link)（`route_link`） | 关联与匹配 | 100 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)†（100） |
| [用药或操作频次关联](benchmarks/medical_decision_v1/tasks/frequency_link)（`frequency_link`） | 关联与匹配 | 81 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)†（81） |
| [药物剂型关联](benchmarks/medical_decision_v1/tasks/drug_form_link)（`drug_form_link`） | 关联与匹配 | 77 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)†（77） |
| [补液方案选择](benchmarks/medical_decision_v1/tasks/fluid_plan)（`fluid_plan`） | 规则与数值 | 16 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（9）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（7） |
| [药物基因结果用药建议匹配](benchmarks/medical_decision_v1/tasks/pgx_guideline_recommendation)（`pgx_guideline_recommendation`） | 资格与适宜性 | 100 | [CPIC curated pharmacogenomic tables](https://www.clinpgx.org/cpic)（100） |
| [试验干预效果方向判定](benchmarks/medical_decision_v1/tasks/trial_effect_direction)（`trial_effect_direction`） | 证据与一致性 | 100 | [Evidence Inference 2.0 — CC-BY article subset](https://github.com/jayded/evidence-inference)（100） |
| [处方审核处置选择](benchmarks/medical_decision_v1/tasks/prescription_audit_action)（`prescription_audit_action`） | 分类与标准化 | 11 | [TCMEval-PA](https://doi.org/10.6084/m9.figshare.29651261.v3)（11） |
| [给药途径与方法选择](benchmarks/medical_decision_v1/tasks/administration_route_choice)（`administration_route_choice`） | 临床候选方案、流程与下一步行动 | 4 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（3）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（1） |

### 住院与护理

核对病情证据、操作执行和病情恶化风险。

| 任务（ID） | 能力维度 | 题数 | 数据集来源（题数） |
| --- | --- | ---: | --- |
| [患者与记录身份匹配](benchmarks/medical_decision_v1/tasks/patient_identity)（`patient_identity`） | 关联与匹配 | 0 | 待补数据 |
| [长病历证据选择](benchmarks/medical_decision_v1/tasks/long_record_evidence)（`long_record_evidence`） | 证据与一致性 | 100 | [LongHealth](https://github.com/kbressem/LongHealth)（100） |
| [医疗操作进度](benchmarks/medical_decision_v1/tasks/procedure_progress)（`procedure_progress`） | 流程与下一步行动 | 0 | 待补数据 |
| [单次给药执行状态](benchmarks/medical_decision_v1/tasks/administration_status)（`administration_status`） | 流程与下一步行动 | 0 | 待补数据 |
| [脓毒症提前预警](benchmarks/medical_decision_v1/tasks/deterioration_prediction)（`deterioration_prediction`） | 风险与升级 | 100 | [PhysioNet Challenge 2019](https://physionet.org/content/challenge-2019/1.0.0/)（100） |
| [术后转归去向选择](benchmarks/medical_decision_v1/tasks/postoperative_disposition)（`postoperative_disposition`） | 流程与下一步行动 | 68 | [Post-Operative Patient](https://archive.ics.uci.edu/dataset/82/post+operative+patient)（68） |
| [子操作与所属操作关联](benchmarks/medical_decision_v1/tasks/procedure_component_link)（`procedure_component_link`） | 关联与匹配 | 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)（100） |
| [临床事件持续性](benchmarks/medical_decision_v1/tasks/event_permanence)（`event_permanence`） | 事实与状态 | 100 | [E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus)†（100） |
| [病例并发症判断](benchmarks/medical_decision_v1/tasks/case_complication)（`case_complication`） | 风险与升级 | 100 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（64）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（36） |
| [护理措施选择](benchmarks/medical_decision_v1/tasks/nursing_priority)（`nursing_priority`） | 流程与下一步行动 | 42 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（42） |
| [病例营养方案选择](benchmarks/medical_decision_v1/tasks/nutrition_plan)（`nutrition_plan`） | 分类与标准化 | 11 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（10）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（1） |
| [护理体位选择](benchmarks/medical_decision_v1/tasks/positioning_choice)（`positioning_choice`） | 分类与标准化 | 10 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（8）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（2） |
| [病情监测指标选择](benchmarks/medical_decision_v1/tasks/monitoring_target)（`monitoring_target`） | 临床候选方案、流程与下一步行动 | 5 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（5） |
| [感染防控措施选择](benchmarks/medical_decision_v1/tasks/infection_precaution)（`infection_precaution`） | 临床候选方案、流程与下一步行动 | 5 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（4）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（1） |

### 出院与随访

识别后续行动、完成状态和出院后的风险。

| 任务（ID） | 能力维度 | 题数 | 数据集来源（题数） |
| --- | --- | ---: | --- |
| [随访行动与完成状态](benchmarks/medical_decision_v1/tasks/followup_action)（`followup_action`） | 流程与下一步行动 | 0 | 待补数据 |
| [出院后 30 天内再入院预测](benchmarks/medical_decision_v1/tasks/readmission_30d)（`readmission_30d`） | 风险与升级 | 100 | [Diabetes 130-US Hospitals for Years 1999-2008](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)（100） |
| [出院待办行动类别](benchmarks/medical_decision_v1/tasks/followup_item_type)（`followup_item_type`） | 分类与标准化 | 0 | 待补数据 |
| [90 日死亡结局预测](benchmarks/medical_decision_v1/tasks/mortality_90d)（`mortality_90d`） | 风险与升级 | 100 | [Heart Failure Clinical Records](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records)（100） |
| [随访方案选择](benchmarks/medical_decision_v1/tasks/followup_plan)（`followup_plan`） | 临床候选方案、流程与下一步行动 | 6 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（3）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（2）；[MedMCQA](https://huggingface.co/datasets/openlifescienceai/medmcqa)（1） |
| [康复训练方案选择](benchmarks/medical_decision_v1/tasks/rehabilitation_choice)（`rehabilitation_choice`） | 临床候选方案、流程与下一步行动 | 4 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（4） |
| [个体预防方案选择](benchmarks/medical_decision_v1/tasks/prevention_choice)（`prevention_choice`） | 临床候选方案、流程与下一步行动 | 13 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（10）；[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)（2）；[MedMCQA](https://huggingface.co/datasets/openlifescienceai/medmcqa)（1） |
| [患者教育与沟通选择](benchmarks/medical_decision_v1/tasks/patient_counseling)（`patient_counseling`） | 临床候选方案、流程与下一步行动 | 11 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（11） |

### 临床试验筛选

解释入排条件并判断患者转介资格。

| 任务（ID） | 能力维度 | 题数 | 数据集来源（题数） |
| --- | --- | ---: | --- |
| [患者与试验匹配](benchmarks/medical_decision_v1/tasks/trial_referral)（`trial_referral`） | 资格与适宜性、证据与一致性 | 100 | [TrialGPT SIGIR](https://github.com/ncbi-nlp/TrialGPT)（100） |
| [入排条件要素分类](benchmarks/medical_decision_v1/tasks/criterion_entity_type)（`criterion_entity_type`） | 资格与适宜性 | 100 | [Chia](https://doi.org/10.6084/m9.figshare.11855817)（100） |
| [入排条件限定关系](benchmarks/medical_decision_v1/tasks/criterion_relation)（`criterion_relation`） | 资格与适宜性 | 100 | [Chia](https://doi.org/10.6084/m9.figshare.11855817)（100） |
| [入排条件与或关系](benchmarks/medical_decision_v1/tasks/criterion_boolean)（`criterion_boolean`） | 资格与适宜性、规则与数值 | 100 | [Chia](https://doi.org/10.6084/m9.figshare.11855817)（100） |
| [条件上界与下界](benchmarks/medical_decision_v1/tasks/criterion_bound)（`criterion_bound`） | 资格与适宜性 | 100 | [Clinical Trial Parser annotated test data](https://github.com/facebookresearch/Clinical-Trial-Parser)（100） |
| [病程与疗程时长关联](benchmarks/medical_decision_v1/tasks/duration_link)（`duration_link`） | 关联与匹配 | 100 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)†（100） |
| [联合干预对象关联](benchmarks/medical_decision_v1/tasks/combination_link)（`combination_link`） | 关联与匹配 | 100 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)†（100） |
| [干预用途关联](benchmarks/medical_decision_v1/tasks/indication_link)（`indication_link`） | 关联与匹配 | 100 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)†（100） |

### 病历与医疗质量控制

识别文书类别、错误、隐私与证据不一致。

| 任务（ID） | 能力维度 | 题数 | 数据集来源（题数） |
| --- | --- | ---: | --- |
| [病历章节类别](benchmarks/medical_decision_v1/tasks/note_section)（`note_section`） | 分类与标准化 | 100 | [ACI-Bench](https://github.com/microsoft/clinical_visit_note_summarization_corpus)（100） |
| [医学术语归一化](benchmarks/medical_decision_v1/tasks/terminology)（`terminology`） | 分类与标准化 | 0 | 待补数据 |
| [医疗叙述错误检出](benchmarks/medical_decision_v1/tasks/clinical_error_detection)（`clinical_error_detection`） | 证据与一致性、临床候选方案 | 100 | [MEDEC-MS](https://github.com/abachaa/MEDEC)（50）；[MedErrBench CN](https://github.com/congboma/MedErrBench)（50） |
| [医疗叙述错误定位](benchmarks/medical_decision_v1/tasks/clinical_error_location)（`clinical_error_location`） | 证据与一致性 | 100 | [MEDEC-MS](https://github.com/abachaa/MEDEC)（50）；[MedErrBench CN](https://github.com/congboma/MedErrBench)（50） |
| [研究论断证据关系](benchmarks/medical_decision_v1/tasks/claim_support)（`claim_support`） | 证据与一致性 | 100 | [SciFact](https://github.com/allenai/scifact)（100） |
| [医疗材料隐私候选](benchmarks/medical_decision_v1/tasks/privacy_candidate)（`privacy_candidate`） | 风险与升级 | 100 | [MEDDOCAN / SPACCC](https://github.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN)（100） |
| [病历论断支持关系](benchmarks/medical_decision_v1/tasks/clinical_statement_support)（`clinical_statement_support`） | 证据与一致性 | 0 | 待补数据 |
| [同一临床事件指代关联](benchmarks/medical_decision_v1/tasks/event_coreference)（`event_coreference`） | 关联与匹配 | 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)（100） |
| [文本因果结果关联](benchmarks/medical_decision_v1/tasks/cause_effect_link)（`cause_effect_link`） | 关联与匹配 | 100 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)†（100） |
| [否定或推测线索作用对象](benchmarks/medical_decision_v1/tasks/assertion_cue_target)（`assertion_cue_target`） | 关联与匹配 | 100 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)†（100） |
| [临床时间表达类别](benchmarks/medical_decision_v1/tasks/clinical_time_type)（`clinical_time_type`） | 分类与标准化 | 100 | [E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus)†（100） |
| [知情与隐私处置选择](benchmarks/medical_decision_v1/tasks/consent_action)（`consent_action`） | 临床候选方案、流程与下一步行动 | 3 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)（1）；[PrinciplismQA](https://github.com/FreedomIntelligence/PrinciplismQA)（2） |

## 数据来源与追溯

任务表展示实际使用的数据集。各来源的论文引用、发布方、材料性质、许可和答案映射见 [来源登记](benchmarks/medical_decision_v1/SOURCES.md)；任务定义、选项标签和实际题量见 [任务说明](benchmarks/medical_decision_v1/README.md)。

每道题保留 **题目 ID → 上游固定版本与文件哈希 → 原记录或标注位置 → 答案映射** 的溯源链。下载包内的 `provenance.jsonl` 可逐题查询，`sources.lock.json` 记录原始资源版本与 SHA-256。原始答案与适配元数据不作为模型输入。

材料包括考试题、模拟病例、病例报告、临床记录和指南规则，具体性质逐来源标明。答案沿用上游标注或声明的机械映射，尚未经过本项目独立医生逐题审核。待补任务及未收录来源的原因见 [数据调研](benchmarks/medical_decision_v1/SCENARIO_RESEARCH.md) 和 [最新空缺核验](benchmarks/medical_decision_v1/expansion_audit_v080.json)。

## 模型得分与耗时对比

比较以 **模型版本 × 任务 × 固定评测子集** 为单位。JEV 与其他模型使用同一批题、同一候选项和一致的评分规则；训练前后模型使用不同版本标识。先查看逐任务结果，再按场景与能力维度汇总。

| 比较项 | 记录方式 |
| --- | --- |
| 评测范围 | 数据版本、任务 ID、子集、实际题数和完成题数 |
| 决策得分 | 准确率、宏 F1、逐类召回；缺失及无效回答按错计 |
| 单题耗时 | 完整决策的平均耗时、P50、P95，单位为秒 |
| 任务总耗时 | 本任务从第一题启动到最后一题结束的墙钟时间，同时报告并发数 |
| 运行失败 | 超时率、请求失败率、无效回答率及重试次数 |
| 运行条件 | 模型/检查点、推理配置、部署环境、缓存与重试策略 |

单题计时从开始执行该题的决策流程、发出首次请求之前开始，到最终决策返回或该题失败结束。若 JEV 或其他系统涉及多阶段处理、多次模型调用及重试，计入完整流程耗时。数据下载、离线评分等准备工作不计入推理耗时。详细计时边界和失败处理见 [评测方法](docs/EVALUATION.md#耗时测量与结果记录)。

现有评分工具输出逐任务质量指标，以及场景、能力维度等汇总。**耗时需要由模型运行端采集，当前评分工具尚未自动汇总耗时，也未包含模型调用器。** 本仓库目前提供固定评测数据和离线评分工具；模型对比结果待实际运行后发布。

默认评测开放核心集，非商业附加集单独报告。场景分数为场景内任务准确率的等权平均，总分再对有题场景等权平均。空任务不计零分，小样本任务必须同时展示题数；不同数据范围和运行条件下的得分、耗时不直接混排。

## 下载与使用

以下为当前整理的数据包。

| 数据包 | 题数 | 使用范围 |
| --- | ---: | --- |
| [开放许可核心集](releases/jev-medical-decision-v0.8.0-open.zip) | 4,334 | 遵守各来源的署名、相同方式共享等许可条件 |
| [非商业研究附加集](releases/jev-medical-decision-v0.8.0-research-noncommercial.zip) | 1,573 | 任务表中带 † 的来源；保留各自非商业等限制 |

[下载说明与校验和](releases/README.md)。两个包互不重复，均包含整理题目、无答案请求、独立答案、逐题溯源和离线校验/评分工具。解压后进入包目录执行（Python 3.10+，仅标准库）：

```bash
python3 tools/medical_decision_release.py verify --dataset .
python3 tools/medical_decision_release.py score --dataset . --predictions predictions.jsonl --output scores.json
```

运行模型时读取 `requests.jsonl`，只发送其中的 `request`。把返回的选项键保存为预测文件，每行一条：

```json
{"id":"bounded_score:medcalc:489","choice":"选项键"}
```

示例题号属于开放核心集，`choice` 应替换为该题实际返回的选项键。`scores.json` 的 `tasks` 字段按任务 ID 保存质量指标；运行端的耗时记录通过相同题目 ID 关联。原始来源查询及从仓库复建的方法见 [使用与复建说明](docs/REPRODUCING.md)。

## 结果解释

每任务约 100 题用于固定对照，少量题目的任务仅提供探索性覆盖。共享病例中的多道题不等于多个独立患者；例如 LongHealth 的两个任务共用 20 个虚构患者。完整分组与任务边界见 [评测方法](docs/EVALUATION.md)。

当前有 406 题来自上游公开训练划分（CMB 306、PhysioNet 100），677 题材料或片段命中过往评测指纹；PMR-Synth 的收件箱与论文训练/测试划分对应尚未确认。比较模型训练效果时，应按已使用的训练材料剔除或分层报告，并冻结相同评测子集。这些数据不能作为完全未暴露的盲测或临床有效性证明。

## 许可

代码采用 [MIT](LICENSE)。第三方题目和材料分别遵守原数据许可，代码许可不覆盖数据；参见 [第三方声明](THIRD_PARTY_NOTICES.md) 和包内 `LICENSE-DATA.md`。
