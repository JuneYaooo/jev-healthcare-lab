# Jev 医疗决策评测集 v0.6.0

给定医疗材料、规则或候选项，评估可明确计分的分类、状态、关系、证据和方案选择。每题只有一个决策输出，使用 Jev `choice` 请求格式；不要求生成病历、建议或解释。

**8 个医疗场景 · 77 个任务定义 · 51 个任务各 100 题 · 8 个不足 100 题 · 18 个留空 · 共 5,594 题。**

开放许可核心部分 4,051 题；非商业研究附加部分 1,543 题。当前 8 个场景有题目，不代表场景工作流完整覆盖；语言分布为 en 3,524 题、es 1,058 题、zh 1,012 题。

[全部题目](samples.jsonl) · [无答案请求](requests.jsonl) · [答案](answers.jsonl) · [来源与许可](SOURCES.md) · [场景任务定义](taxonomy.json) · [按场景寻找数据](SCENARIO_RESEARCH.md) · [构建统计](summary.json)

**[下载独立数据包](../../releases/README.md)**：开放核心包和非商业研究附加包分别交付，内含题目、答案、逐题溯源索引、原许可、格式说明及校验/评分工具。每道题可通过 `id → 原始资源版本与哈希 → 标注位置 → 转换代码` 回查。

主目录按医疗场景 → 决策任务组织。每个任务只有一个 `primary_scenario`；原九个能力维度作为 `ability_tags`，允许多标签但不重复计算题目。`dimension` 保留为主要能力，兼容旧分析。材料判断、临床候选选择和结局预测分别报告。

## 场景覆盖

| 场景 | 有题任务 / 定义任务 | 题数 |
| --- | ---: | ---: |
| 接诊与分诊 | 4 / 7 | 400 |
| 检查与检验 | 6 / 10 | 556 |
| 诊断与鉴别 | 12 / 13 | 1200 |
| 治疗与用药 | 11 / 14 | 928 |
| 住院与护理 | 7 / 10 | 610 |
| 出院与随访 | 2 / 4 | 200 |
| 临床试验筛选 | 8 / 8 | 800 |
| 病历与医疗质量控制 | 9 / 11 | 900 |

## 任务目录

题数是决策问题数，来源组可能是文档、句子、模拟病例或患者，不能一律解读为患者数。语种和输入条件不另计为任务。

### 接诊与分诊

识别就诊诉求、资料缺口及处理优先级。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [事实主体归属](tasks/experiencer/task.json) | 100 / 100 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3) | 给定试验文本及主体片段，选择原标注角色：患者、家属或其他人。只评价文本角色。 |
| [医疗问题意图](tasks/query_intent/task.json) | 100 / 100 | [MedQuAD](https://github.com/abachaa/MedQuAD) | 给定医疗问题，判断其信息需求类别。 |
| [决策资料充分性](tasks/input_sufficiency/task.json) | 0 / 0 | [CMedCalc-Bench](https://github.com/Zhihong-Zhu/CMedCalc-Bench)、[CARE-Bench](https://github.com/ningkko/CARE-bench) | CMedCalc 数据再分发许可未明确；CARE-Bench 的 need_info 是分诊行动标签，不能代表计算要素齐全及冲突消解。 |
| [当前分诊与升级行动](tasks/triage_urgency/task.json) | 100 / 62 | [CARE-Bench](https://github.com/ningkko/CARE-bench) | 仅根据当前已披露消息，选择澄清信息、自护监测、非紧急就医或紧急就医；不生成建议文本。 |
| [候选科室分流](tasks/department_routing/task.json) | 0 / 0 | [MedJourney](https://github.com/Medical-AI-Learning/MedJourney)、[RD-Triage](https://github.com/zhelishisongjie/RD-Triage)、[ClinicalMC / ClinicalMPD](https://github.com/hzyuezh/ClinicalMPD)、[Chinese-medical-dialogue-data](https://github.com/Toyhom/Chinese-medical-dialogue-data) | RD-Triage 有多答案及多上游来源需分别核权；ClinicalMC/MedJourney 数据许可未闭合；中文问诊科室字段不等于最佳首诊科室。 |
| [患者消息紧急性比较](tasks/message_urgency_pair/task.json) | 0 / 0 | [PMR-Bench Reddit Test Pairs](https://arxiv.org/abs/2601.13178) | PMR-Reddit 的原等级经 GPT-5 推导，并非逐对人工金标；本轮不纳入主评测。 |
| [孕产风险等级识别](tasks/maternal_risk/task.json) | 100 / 100 | [Maternal Health Risk](https://archive.ics.uci.edu/dataset/863/maternal+health+risk) | 根据孕产记录的年龄与生命体征，选择发布数据标注的低、中、高风险；不等同经过验证的母婴结局预测。 |

### 检查与检验

选择检查、关联结果并判断结果的适用性与处理需求。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [检查检验数值关联](tasks/lab_link/task.json) | 100 / 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2) | 给定病例全文和已标注的数值结果片段，从候选检查/评估中选择原始标注关联的项目；包含量表，不判断结果是否异常。 |
| [标本身份与来源链](tasks/specimen_lineage/task.json) | 0 / 0 | [FHIR R4 clinical workflow definitions](https://hl7.org/fhir/R4/) | FHIR Specimen.parent 提供字段和示例；未找到同物、派生、无关、未知四类的开放标注病例。 |
| [数值与单位等价](tasks/unit_equivalence/task.json) | 0 / 0 | [UCUM unit specification](https://ucum.org/ucum) | UCUM 提供换算依据，本轮未找到独立标注的医疗数值等价题集；不自行改数值生成金标。 |
| [参考区间适用性](tasks/reference_range/task.json) | 72 / 25 | [LabQAR](https://doi.org/10.6084/m9.figshare.29189894) | 去重、训练重合筛查和来源分组限制后不足目标数量；保留实际数量。 |
| [临床事件变化趋势](tasks/result_trend/task.json) | 100 / 71 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2) | 给定病例及事件片段，选择原 TREND 标注的增加、减少或改变；只判断原文描述，不预测未来。 |
| [危急结果与人工升级](tasks/critical_result_escalation/task.json) | 0 / 0 | [openFDA drug labels](https://open.fda.gov/apis/drug/label/)、[CARE-Bench](https://github.com/ningkko/CARE-bench) | 现有规则/分诊数据不提供机构危急值阈值版本、复核条件及升级等级的匹配金标。 |
| [报告阶段与效力](tasks/report_stage/task.json) | 0 / 0 | [FHIR R4 clinical workflow definitions](https://hl7.org/fhir/R4/) | FHIR DiagnosticReport.status 是状态标准，未找到具有独立状态答案的开放临床报告集。 |
| [检查方案选择](tasks/examination_choice/task.json) | 100 / 100 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465) | 根据病例从给定候选中选择检查。 |
| [检验数值高低判读](tasks/lab_value_classification/task.json) | 100 / 100 | [LabQAR](https://doi.org/10.6084/m9.figshare.29189894) | 根据题目给出的检验值和参考区间，选择原始选项中的 High、Normal 或 Low；仅按给定区间判读，不推断诊断或危急程度。 |
| [药物基因检测功能表型判定](tasks/pgx_function_phenotype/task.json) | 84 / 19 | [CPIC curated pharmacogenomic tables](https://www.clinpgx.org/cpic) | 去重、训练重合筛查和来源分组限制后不足目标数量；保留实际数量。 |

### 诊断与鉴别

根据已有材料判断诊断、状态和临床分级。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [否定与不确定状态](tasks/assertion_scope/task.json) | 100 / 100 | [NUBes SAMPLE-001](https://github.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus) | 给定临床句子与标注目标，区分否定和不确定；本任务不覆盖肯定类。 |
| [事件与文档时间关系](tasks/temporality/task.json) | 100 / 48 | [E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus) | 给定病例原文、文档时间和事件片段，选择原 E3C docTimeRel 时间关系。 |
| [诊断核实状态](tasks/diagnosis_verification/task.json) | 0 / 0 | [FHIR R4 clinical workflow definitions](https://hl7.org/fhir/R4/)、[E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus) | FHIR 有核实状态定义；E3C 的实际/假设/不确定是事件属性，不能等同疑似/确诊/排除四分类。未找到匹配且可开放分发的原金标。 |
| [有界临床量表评分](tasks/bounded_score/task.json) | 100 / 100 | [MedCalc-Bench GitHub test release](https://github.com/ncbi-nlp/MedCalc-Bench) | 根据病例选择 GCS、CURB-65、SIRS、CHA2DS2-VASc 或 FeverPAIN 的数值。 |
| [临床分级与分期选择](tasks/clinical_grade/task.json) | 100 / 99 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465) | 根据病例从原选项中选择疾病分期、严重程度分度或功能分级。 |
| [模拟病例主诊断选择](tasks/synthetic_diagnosis/task.json) | 100 / 100 | [DDXPlus](https://doi.org/10.6084/m9.figshare.20043374) | 给定 DDXPlus 观察到的症状与背景，从完整病种表选择模拟主诊断。 |
| [临床病例候选诊断](tasks/diagnosis_choice/task.json) | 100 / 100 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465) | 从给定诊断候选中选择最符合病例者。 |
| [中医证型选择](tasks/tcm_syndrome/task.json) | 100 / 100 | [TCM-SD](https://github.com/borororo/zy-bert) | 根据主诉、病情和检查选择原始标准证型。 |
| [临床事件先后关系](tasks/event_temporal_order/task.json) | 100 / 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2) | 给定病例和两个事件，选择第一个相对第二个的原始先于、晚于或重叠关系。 |
| [临床事件与解剖部位关联](tasks/anatomical_site_link/task.json) | 100 / 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2) | 给定病例和临床事件，从原文解剖部位候选中选择原 MODIFY 关系唯一关联的部位。 |
| [严重程度与临床事件关联](tasks/severity_link/task.json) | 100 / 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2) | 给定病例和严重程度片段，从原文事件候选中选择其唯一修饰的事件。 |
| [事件与时间表达关联](tasks/event_date_link/task.json) | 100 / 47 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)、[E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus) | 给定病例和时间表达，从原文事件候选中选择原时间关联标注的唯一目标；若提供关系类型，按该方向解释。 |
| [病例病因与原因判断](tasks/case_etiology/task.json) | 100 / 100 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465) | 根据病例从原选项中选择导致所述疾病、症状或事件的最可能原因。 |

### 治疗与用药

判断治疗选择、用药关系及患者特异性适宜性。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [用药状态与变更](tasks/medication_status/task.json) | 0 / 0 | [n2c2/i2b2](https://n2c2.dbmi.hms.harvard.edu/data-sets)、[CMED / n2c2 2022 Track 1](https://n2c2.dbmi.hms.harvard.edu/2022-track-1) | CMED/n2c2 原标注相关，但临床文本受协议限制；未取得可公开再分发的替代语料。 |
| [药物相互作用关系](tasks/drug_interaction/task.json) | 100 / 100 | [DDI Corpus 2013](https://github.com/isegura/DDICorpus) | 给定药物对，判断无关系或原文标注的相互作用类型。 |
| [药物与剂量关联](tasks/dose_link/task.json) | 100 / 95 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2) | 给定病例全文和剂量片段，从候选药物中选择原始标注关联的药物；不评价剂量是否适宜，也不覆盖频次和途径。 |
| [患者特异性禁忌选择](tasks/patient_contraindication/task.json) | 54 / 53 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465) | 去重、训练重合筛查和来源分组限制后不足目标数量；保留实际数量。 |
| [剂量适宜性](tasks/dose_appropriateness/task.json) | 0 / 0 | [openFDA drug labels](https://open.fda.gov/apis/drug/label/)、[CMedCalc-Bench](https://github.com/Zhihong-Zhu/CMedCalc-Bench) | openFDA 是药品说明书规则；尚缺患者肝肾功能、具体处方及独立剂量适宜性金标。 |
| [治疗方案选择](tasks/treatment_choice/task.json) | 100 / 100 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465) | 根据病例从给定候选中选择治疗。 |
| [用药方案选择](tasks/medication_choice/task.json) | 100 / 100 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465) | 根据病例从给定候选中选择用药。 |
| [治疗相关不良事件预测](tasks/adverse_event_prediction/task.json) | 0 / 0 | [CT-ADE-SOC / CT-ADE-PT](https://github.com/ds4dh/CT-ADE) | CT-ADE 的数据许可声明未解决 MedDRA SOC/PT 术语及底层材料全部再分发边界；本轮保留引用。 |
| [给药途径关联](tasks/route_link/task.json) | 100 / 74 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3) | 给定试验文本和给药途径片段，从原文药物或操作候选中选择原关系唯一关联的目标。 |
| [用药或操作频次关联](tasks/frequency_link/task.json) | 81 / 55 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3) | 去重、训练重合筛查和来源分组限制后不足目标数量；保留实际数量。 |
| [药物剂型关联](tasks/drug_form_link/task.json) | 77 / 39 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3) | 去重、训练重合筛查和来源分组限制后不足目标数量；保留实际数量。 |
| [补液方案选择](tasks/fluid_plan/task.json) | 16 / 15 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465) | 去重、训练重合筛查和来源分组限制后不足目标数量；保留实际数量。 |
| [药物基因结果用药建议匹配](tasks/pgx_guideline_recommendation/task.json) | 100 / 25 | [CPIC curated pharmacogenomic tables](https://www.clinpgx.org/cpic) | 给定药物、人群及基因结果，选择 CPIC 固定快照中对应的原始用药建议；不外推为完整个体处方。 |
| [试验干预效果方向判定](tasks/trial_effect_direction/task.json) | 100 / 100 | [Evidence Inference 2.0 — CC-BY article subset](https://github.com/jayded/evidence-inference) | 根据完整试验报告，判断指定干预相对对照对指定结局的报告结果：显著降低、无显著差异或显著升高。方向不等同临床优劣。 |

### 住院与护理

核对病情证据、操作执行和病情恶化风险。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [患者与记录身份匹配](tasks/patient_identity/task.json) | 0 / 0 | [FEBRL record linkage datasets](https://recordlinkage.readthedocs.io/en/latest/ref-datasets.html)、[MIMIC-IV Clinical Database Demo v2.2](https://physionet.org/content/mimic-iv-demo/2.2/) | FEBRL 是合成人口学匹配，MIMIC 演示 ID 连接不是身份可确定性评测；缺医疗证据、冲突及不确定金标。 |
| [长病历证据选择](tasks/long_record_evidence/task.json) | 100 / 20 | [LongHealth](https://github.com/kbressem/LongHealth) | 根据完整病例文书，在原始选项中选择有依据的答案。 |
| [医疗操作进度](tasks/procedure_progress/task.json) | 0 / 0 | [FHIR R4 clinical workflow definitions](https://hl7.org/fhir/R4/)、[E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus) | 操作状态标准与 E3C 事件时态不同；未找到完整覆盖计划、进行、完成、取消、目标未达成的开放金标。 |
| [单次给药执行状态](tasks/administration_status/task.json) | 0 / 0 | [MIMIC-IV Clinical Database Demo v2.2](https://physionet.org/content/mimic-iv-demo/2.2/)、[FHIR R4 clinical workflow definitions](https://hl7.org/fhir/R4/) | MIMIC 演示为真实结构化事件；尚缺跨医嘱、配药、给入的可判定证据与统一答案协议，留空。 |
| [脓毒症提前预警](tasks/deterioration_prediction/task.json) | 100 / 100 | [PhysioNet Challenge 2019](https://physionet.org/content/challenge-2019/1.0.0/) | 仅使用 ICU 前 12 小时的记录，判断按挑战定义的脓毒症起病是否发生在第 12 小时之后至第 24 小时（含）。 |
| [术后转归去向选择](tasks/postoperative_disposition/task.json) | 68 / 68 | [Post-Operative Patient](https://archive.ics.uci.edu/dataset/82/post+operative+patient) | 去重、训练重合筛查和来源分组限制后不足目标数量；保留实际数量。 |
| [子操作与所属操作关联](tasks/procedure_component_link/task.json) | 100 / 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2) | 给定病例和子操作片段，从原文操作候选中选择原 SUB_PROCEDURE 唯一关联的所属操作。 |
| [临床事件持续性](tasks/event_permanence/task.json) | 100 / 48 | [E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus) | 给定病例及事件片段，选择原 E3C 持续性标注 FINITE 或 PERMANENT；不把它解释为新的慢病诊断。 |
| [病例并发症判断](tasks/case_complication/task.json) | 100 / 96 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465) | 根据病例从原选项中选择最可能的并发症；不是主诊断任务。 |
| [护理措施选择](tasks/nursing_priority/task.json) | 42 / 42 | [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465) | 去重、训练重合筛查和来源分组限制后不足目标数量；保留实际数量。 |

### 出院与随访

识别后续行动、完成状态和出院后的风险。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [随访行动与完成状态](tasks/followup_action/task.json) | 0 / 0 | [CLIP 出院行动标注](https://physionet.org/content/mimic-iii-clinical-action/1.0.0/) | CLIP 标注行动片段与类别，不标注是否已完成或逾期；原文另受 MIMIC 协议限制。 |
| [出院后 30 天内再入院预测](tasks/readmission_30d/task.json) | 100 / 100 | [Diabetes 130-US Hospitals for Years 1999-2008](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008) | 根据出院时结构化资料，预测是否被记录为 30 天内再入院。限糖尿病住院后回家人群，预测观察结局而非最优行动。 |
| [出院待办行动类别](tasks/followup_item_type/task.json) | 0 / 0 | [CLIP 出院行动标注](https://physionet.org/content/mimic-iii-clinical-action/1.0.0/) | CLIP 任务匹配，但基于 MIMIC 文本，需要凭证和 DUA，不能公开复制原文。 |
| [90 日死亡结局预测](tasks/mortality_90d/task.json) | 100 / 100 | [Heart Failure Clinical Records](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records) | 根据基线心衰记录预测 90 日内死亡；不提供随访长度；90 日前无死亡但失访者已排除。 |

### 临床试验筛选

解释入排条件并判断患者转介资格。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [患者与试验匹配](tasks/trial_referral/task.json) | 100 / 58 | [TrialGPT SIGIR](https://github.com/ncbi-nlp/TrialGPT) | 根据患者和试验材料，判断不相关、可能适合或很可能适合转介。 |
| [入排条件要素分类](tasks/criterion_entity_type/task.json) | 100 / 100 | [Chia](https://doi.org/10.6084/m9.figshare.11855817) | 给定条件原文与目标实体，判断原标注的要素类别。 |
| [入排条件限定关系](tasks/criterion_relation/task.json) | 100 / 100 | [Chia](https://doi.org/10.6084/m9.figshare.11855817) | 给定已标注关联的两个要素，判断数值、时间、限定等关系类型。 |
| [入排条件与或关系](tasks/criterion_boolean/task.json) | 100 / 100 | [Chia](https://doi.org/10.6084/m9.figshare.11855817) | 给定条件中的两个标注要素，判断原文要求 AND 还是 OR。 |
| [条件上界与下界](tasks/criterion_bound/task.json) | 100 / 100 | [Clinical Trial Parser annotated test data](https://github.com/facebookresearch/Clinical-Trial-Parser) | 给定条件与数值限制片段，判断该限制是上界还是下界。 |
| [病程与疗程时长关联](tasks/duration_link/task.json) | 100 / 100 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3) | 给定试验文本和持续时长片段，从原文候选中选择原 Has_Duration_or_Interval 唯一关联的临床对象。 |
| [联合干预对象关联](tasks/combination_link/task.json) | 100 / 61 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3) | 给定试验文本和干预片段，从原文候选中选择原 Combined_with 唯一关联的联合对象。 |
| [干预用途关联](tasks/indication_link/task.json) | 100 / 100 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3) | 给定试验文本及干预片段，从原文候选中选择原 Used_for 唯一关联的用途；不评价个体适宜性。 |

### 病历与医疗质量控制

识别文书类别、错误、隐私与证据不一致。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [病历章节类别](tasks/note_section/task.json) | 100 / 100 | [ACI-Bench](https://github.com/microsoft/clinical_visit_note_summarization_corpus) | 给定去除章节标题的原文片段，选择原始章节类别。 |
| [医学术语归一化](tasks/terminology/task.json) | 0 / 0 | [IMCS-21](https://github.com/lemuria-wchen/imcs21)、[MeDAL](https://github.com/McGill-NLP/medal)、[CBLUE（KUAKE-QIC / CHIP-CTC / CHIP-CDN）](https://github.com/CBLUEbenchmark/CBLUE) | MeDAL 原摘要版权尚未闭合；IMCS21 未明确数据许可；CBLUE 的术语材料及授权需按任务核验，不用代码许可证代替。 |
| [医疗叙述错误检出](tasks/clinical_error_detection/task.json) | 100 / 100 | [MEDEC-MS](https://github.com/abachaa/MEDEC)、[MedErrBench CN](https://github.com/congboma/MedErrBench) | 判断给定病例文本是否含原数据标注的医学错误。 |
| [医疗叙述错误定位](tasks/clinical_error_location/task.json) | 100 / 100 | [MEDEC-MS](https://github.com/abachaa/MEDEC)、[MedErrBench CN](https://github.com/congboma/MedErrBench) | 在明确含错误的病例中，选择原始标注的错误句。 |
| [研究论断证据关系](tasks/claim_support/task.json) | 100 / 100 | [SciFact](https://github.com/allenai/scifact) | 给定论断与被引摘要，判断支持、反驳或证据不足。 |
| [医疗材料隐私候选](tasks/privacy_candidate/task.json) | 100 / 100 | [MEDDOCAN / SPACCC](https://github.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN) | 给定目标片段，判断是否属于需处理的个人标识。 |
| [病历论断支持关系](tasks/clinical_statement_support/task.json) | 0 / 0 | [MedNLI](https://physionet.org/content/mednli/1.0.0/)、[NLI4CT](https://github.com/ai-systems/nli4ct) | MedNLI 原病历受控；NLI4CT 是试验报告二分类且原仓库数据许可不明确，不能替代病历三分类。 |
| [同一临床事件指代关联](tasks/event_coreference/task.json) | 100 / 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2) | 给定病例中的目标事件，从原文事件候选中选择原 IDENTICAL 标注唯一关联的同一事件提及。 |
| [文本因果结果关联](tasks/cause_effect_link/task.json) | 100 / 100 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3) | 给定试验文本及原因片段，从原文候选中选择原 Causes 唯一关联的结果；不推断未标注因果，也不认定患者级药物因果。 |
| [否定或推测线索作用对象](tasks/assertion_cue_target/task.json) | 100 / 100 | [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3) | 给定试验文本及否定或推测线索，从原文候选中选择原 Negation/Speculation 唯一关联的对象。 |
| [临床时间表达类别](tasks/clinical_time_type/task.json) | 100 / 41 | [E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus) | 给定病例及时间片段，选择原 E3C TIMEX3 类别：时长、周期集合、日期、数量时间或前后表达。 |

## 版本、抽样和答案

固定种子 20261010；从锁定版本的原文件解析，以标签/量表/来源等已声明分层轮流取样。先尽量每来源组一题，必要时逐步放宽至每组最多五题。去掉重复请求、冲突答案、不能解析的标注和本地训练指纹命中；不复制或改写题目补足数量。DDXPlus 先从完整官方测试 CSV 按哈希取 1,000 条候选。

LongHealth 对 20 个虚构患者各取五题；这些问题共享整份病历。TCM-SD 按原测试分布哈希抽样，不将 148 个证型强行压成每类一题。CHIA 关系题只分类原始已标注关系，不包含自动构造的负例。NUBes 只测否定/不确定。FRD 的数值已由上游替换为 @NUMBER，仅测上下界方向。MedCalc 使用固定 GitHub 测试版本，不能报告为 HF Verified 版本。

答案来自原始发布标注及可重现的机械映射。记录经过格式、定位、映射与去重检查，尚未做本项目独立医生逐题审核。本版本属于可审计初版，不是临床验证金标准。原始训练/开发/测试划分逐题保留；没有官方测试划分的来源不冒称官方测试集。

v0.2.0 新增 MACCROBAT 的检查数值关联、药物剂量关联；检查题仅保留含数字的原始结果片段。候选项为病例中所有有效的对应类型实体，带原文位置以区分重复名称。只收原始 MODIFY 关系可唯一定位目标的题，不构造负关系、不判断处方适宜性。旧版 1,600 题的 ID、请求及金标保留，迁移基线见 [历史身份索引](history/v0.1.0_sample_identity.json)。

v0.3.0 从 CMB-Exam 和 CNMLEQA-10k 补入中文病例的诊断、检查、治疗、用药四类选择题，原有 1,800 题的 ID、请求与答案保持不变，见 [v0.2.0 身份索引](history/v0.2.0_sample_identity.json)。按病例特征和问题意图规则筛选，排除纯知识题、缺图题、反向提问及不符合任务定义的题；保留原选项与金标，不生成新答案。CMB 原题与独立答案按 ID 连接，原 C 型及多选题不纳入。CNMLEQA 没有官方测试划分，使用发布语料的固定自留子集。

两套中文题库按标准化题干与完整选项集合去重，答案文本冲突时全部排除；来源组由去标点后题干前 60 字的指纹近似确定，可能合并相似病例，也不能排除所有改写重复。题目中的旧术语或原始拼写按原文保留。中文新增题经过程序化适配与抽查，未独立复核其临床金标。[本轮新增来源核验](../../docs/DATASET_EXPANSION.md) 记录其他中文及英文候选。

v0.4.0 增加 E3C、CT-EBM-SP、CARE-Bench 及 UCI 结构化来源，并扩展原 MACCROBAT 和中文病例题。每任务目标 100 题；不足部分保留实际数量，不填充。E3C/CT-EBM-SP 为材料属性或关系判断，CARE-Bench 为来源约束的重构分诊任务，UCI 结局预测与行动标签分别报告，不能将它们全部解释为诊疗方案能力。

新中文任务从 CMB 官方测试、验证及训练文件和 CNMLEQA 固定版本选题；上游训练文件逐题标为 upstream_train_reserved_for_local_evaluation，不能作为已训练过该题库模型的盲测证据。原有 2,200 条完整记录保持不变，见 [v0.3.0 身份索引](history/v0.3.0_sample_identity.json)。

[v0.4.0 来源与适配协议](../../docs/EXPANSION_V040.md) 说明小样本任务、数据许可、结局预测时点、删失处理及模型比较范围。

v0.5.0 对此前 21 个空任务逐项复核：MEDDOCAN 补入 100 道词级隐私判断，PhysioNet 2019 补入 100 道固定时点脓毒症预测，LabQAR 补入 72 道参考区间条件匹配。其他 18 项仍为空；详见 [逐项核验](../../docs/GAP_AUDIT_V050.md) 和 [机器可读记录](gap_audit.json)。原有 4,938 条完整记录保持不变。

v0.6.0 新增检验数值判读、药物基因检测功能表型、基因结果用药建议匹配、试验干预效果方向 4 类任务。分别采用 LabQAR Set 2、CPIC CC0 规则快照和 Evidence Inference 官方测试中的 CC-BY 文章。前版 5,210 条完整记录保持不变；见 [适配协议](../../docs/EXPANSION_V060.md)。

## 训练隔离与历史使用

[筛查索引](exposure_index.json) 固定列出本地训练文件及哈希。选中题目没有命中该索引的精确/窗口指纹；577 道题的材料或片段命中过往主评测指纹（通用片段可能误报）。新抽样不等于从未见过的新病例，不能把这部分称为全新盲测。SciFact 额外排除与官方训练声明共用的文档。

该筛查不证明不存在改写、翻译、患者级关联或基础模型预训练暴露。`summary.json` 记录任务间共享来源组；跨任务统计应按组处理，不把共享文档的不同题当作独立患者。后续训练材料应反向检查本评测集，版本冻结后不根据成绩挑换题。

## 运行

在仓库根目录执行（Python 标准库，无自动模型调用）：

```bash
python3 scripts/medical_decision_dataset.py validate
python3 scripts/medical_decision_dataset.py fetch
python3 scripts/medical_decision_dataset.py build
python3 scripts/medical_decision_dataset.py export --output work/decision-requests.jsonl
python3 scripts/medical_decision_dataset.py score --predictions work/predictions.jsonl --output work/decision-scores.json
```

`fetch` 按 sources.lock.json 下载并核验源文件，`build` 使用已冻结的训练筛查索引复建；不重新生成答案。刷新本地筛查使用 `index` 子命令，刷新后重建将形成不同内容的版本，需复核并更新版本号。

默认导出及计分只包含 `open` 部分。研究用途需要显式加 `--include-research`，才纳入 DDI、TCM-SD、E3C、CT-EBM-SP、CARE-Bench；相应题目仍受非商业及相同方式共享等原许可约束。

模型只接收 `request`（按 API 需要另加 model）；不要发送 gold、provenance、metadata 或来源定位。预测文件每行格式：

```json
{"id":"样本完整 ID","choice":"选项键"}
```

也接受 `{"id":"样本完整 ID","response":{"answers":{"decision":{"choice":"选项键"}}}}`。缺失、格式错误和不在选项内的回答按错计；重复或未知 ID 会使计分失败。

计分先报告逐任务结果，再对同一场景内任务准确率等权平均；`scenario_macro_accuracy` 对有题场景等权，避免试验筛选任务较多而主导总分。场景表同时显示已计分任务数和定义任务数；空场景分数为 null，不计零分也不算已覆盖。旧 `task_macro_accuracy` 仍保留。能力标签统计可重叠，不累加成主分母。不同版本和不同题目覆盖的总分不可直接作训练前后比较。

逐任务输出准确率、宏 F1、逐类召回和来源组全对率；另按决策模式、来源性质、语种及历史匹配状态分层。宏 F1 使用实际有金标的类别，未出现的候选类别单列。公开论文、考试改编、模拟病例和真实临床材料分别报告。

每任务 100 题适合固定的小规模模型与训练对照，不能据此确认细小提升或临床效果。比较训练前后应使用相同题目、候选项、提示和计分范围，并按来源组做配对分析；LongHealth 的有效来源组只有 20 个。这里的汇总分数仅为描述性统计。

## 评测状态

本版本尚未运行模型评测。逐题历史材料重合标记及冻结筛查索引属于数据来源记录，不能解释为本版本模型成绩。
