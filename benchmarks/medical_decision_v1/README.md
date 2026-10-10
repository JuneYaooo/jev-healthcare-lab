# Jev 医疗决策评测集 v0.2.0

给定医疗材料、规则或候选项，评估可明确计分的分类、状态、关系、证据和方案选择。每题只有一个决策输出，使用 Jev `choice` 请求格式；不要求生成病历、建议或解释。

**8 个医疗场景 · 50 个任务定义 · 18 个任务各 100 题 · 0 个不足 100 题 · 32 个留空 · 共 1,800 题。**

开放许可核心部分 1,600 题；非商业研究附加部分 200 题。当前 7 个场景有题目，不代表场景工作流完整覆盖；语言分布为 en 1,500 题、es 100 题、zh 200 题。

[全部题目](samples.jsonl) · [无答案请求](requests.jsonl) · [答案](answers.jsonl) · [来源与许可](SOURCES.md) · [场景任务定义](taxonomy.json) · [按场景寻找数据](SCENARIO_RESEARCH.md) · [构建统计](summary.json)

**[下载独立数据包](../../releases/README.md)**：开放核心包和非商业研究附加包分别交付，内含题目、答案、逐题溯源索引、原许可、格式说明及校验/评分工具。每道题可通过 `id → 原始资源版本与哈希 → 标注位置 → 转换代码` 回查。

主目录按医疗场景 → 决策任务组织。每个任务只有一个 `primary_scenario`；原九个能力维度作为 `ability_tags`，允许多标签但不重复计算题目。`dimension` 保留为主要能力，兼容旧分析。材料判断、临床候选选择和结局预测分别报告；当前预测任务尚未收题。

## 场景覆盖

| 场景 | 有题任务 / 定义任务 | 题数 |
| --- | ---: | ---: |
| 接诊与分诊 | 1 / 6 | 100 |
| 检查与检验 | 1 / 8 | 100 |
| 诊断与鉴别 | 4 / 8 | 400 |
| 治疗与用药 | 2 / 8 | 200 |
| 住院与护理 | 1 / 5 | 100 |
| 出院与随访 | 0 / 3 | 0 |
| 临床试验筛选 | 5 / 5 | 500 |
| 病历与医疗质量控制 | 4 / 7 | 400 |

## 任务目录

题数是决策问题数，来源组可能是文档、句子、模拟病例或患者，不能一律解读为患者数。语种和输入条件不另计为任务。

### 接诊与分诊

识别就诊诉求、资料缺口及处理优先级。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [事实主体归属](tasks/experiencer/task.json) | 0 / 0 | [n2c2/i2b2](https://n2c2.dbmi.hms.harvard.edu/data-sets) | 未找到同时满足公开分发与原始主体金标的已核验来源。 |
| [医疗问题意图](tasks/query_intent/task.json) | 100 / 100 | [MedQuAD](https://github.com/abachaa/MedQuAD) | 给定医疗问题，判断其信息需求类别。 |
| [决策资料充分性](tasks/input_sufficiency/task.json) | 0 / 0 | [CMedCalc-Bench](https://github.com/Zhihong-Zhu/CMedCalc-Bench) | CMedCalc 数据可下载，但发布仓库未找到明确数据再分发许可。 |
| [分诊紧急程度](tasks/triage_urgency/task.json) | 0 / 0 | [TRIAGE](https://github.com/NLie2/Triage)、[MIMIC-IV-ED](https://physionet.org/content/mimic-iv-ed/2.2/)、[TriageBench（Wong，一致性探针）](https://github.com/wongqihan/triagebench) | TRIAGE 发布数据未见明确许可证；不将提示变体当独立病例凑数。 |
| [候选科室分流](tasks/department_routing/task.json) | 0 / 0 | [MedJourney](https://github.com/Medical-AI-Learning/MedJourney) | 已有候选来源缺明确数据许可，科室分流金标亦需核对。 |
| [患者消息紧急性比较](tasks/message_urgency_pair/task.json) | 0 / 0 | [PMR-Bench Reddit Test Pairs](https://arxiv.org/abs/2601.13178) | 已找到官方测试对与非商业许可；尚需核验消息复用、标注方案及配对抽样。 |

### 检查与检验

选择检查、关联结果并判断结果的适用性与处理需求。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [检查检验数值关联](tasks/lab_link/task.json) | 100 / 100 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2) | 给定病例全文和已标注的数值结果片段，从候选检查/评估中选择原始标注关联的项目；包含量表，不判断结果是否异常。 |
| [标本身份与来源链](tasks/specimen_lineage/task.json) | 0 / 0 | 待补 | FHIR 是标准参考，不能代替有答案的数据集。 |
| [数值与单位等价](tasks/unit_equivalence/task.json) | 0 / 0 | 待补 | 现有独立金标均为自编题，暂不填充。 |
| [参考区间适用性](tasks/reference_range/task.json) | 0 / 0 | 待补 | 尚无已核验的开放题目与金标。 |
| [检验结果趋势](tasks/result_trend/task.json) | 0 / 0 | 待补 | 不能将带时序数值的开放材料直接当作有审核金标的测试题。 |
| [危急结果与人工升级](tasks/critical_result_escalation/task.json) | 0 / 0 | 待补 | 未找到具有机构阈值版本与审核标签的开放来源。 |
| [报告阶段与效力](tasks/report_stage/task.json) | 0 / 0 | 待补 | 标准字段不代替独立真实材料与标签。 |
| [检查方案选择](tasks/examination_choice/task.json) | 0 / 0 | [MedJourney](https://github.com/Medical-AI-Learning/MedJourney)、[MedMCQA](https://github.com/medmcqa/medmcqa) | MedJourney 缺明确数据许可。 |

### 诊断与鉴别

根据已有材料判断诊断、状态和临床分级。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [否定与不确定状态](tasks/assertion_scope/task.json) | 100 / 100 | [NUBes SAMPLE-001](https://github.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus) | 给定临床句子与标注目标，区分否定和不确定；本任务不覆盖肯定类。 |
| [事实时间属性](tasks/temporality/task.json) | 0 / 0 | [THYME](https://github.com/stylerw/thymedata) | 现有自编题不纳入；THYME 临床原文需访问协议。 |
| [诊断核实状态](tasks/diagnosis_verification/task.json) | 0 / 0 | 待补 | 尚无核验完成的开放独立金标。 |
| [有界临床量表评分](tasks/bounded_score/task.json) | 100 / 100 | [MedCalc-Bench GitHub test release](https://github.com/ncbi-nlp/MedCalc-Bench) | 根据病例选择 GCS、CURB-65、SIRS、CHA2DS2-VASc 或 FeverPAIN 的数值。 |
| [临床语义分级](tasks/clinical_grade/task.json) | 0 / 0 | [CMedCalc-Bench](https://github.com/Zhihong-Zhu/CMedCalc-Bench) | CMedCalc 数据许可待明确。 |
| [模拟病例主诊断选择](tasks/synthetic_diagnosis/task.json) | 100 / 100 | [DDXPlus](https://doi.org/10.6084/m9.figshare.20043374) | 给定 DDXPlus 观察到的症状与背景，从完整病种表选择模拟主诊断。 |
| [临床病例候选诊断](tasks/diagnosis_choice/task.json) | 0 / 0 | [MedJourney](https://github.com/Medical-AI-Learning/MedJourney)、[MedMCQA](https://github.com/medmcqa/medmcqa) | MedJourney/CMExam 许可或研究使用限制需进一步澄清。 |
| [中医证型选择](tasks/tcm_syndrome/task.json) | 100 / 100 | [TCM-SD](https://github.com/borororo/zy-bert) | 根据主诉、病情和检查选择原始标准证型。 |

### 治疗与用药

判断治疗选择、用药关系及患者特异性适宜性。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [用药状态与变更](tasks/medication_status/task.json) | 0 / 0 | [n2c2/i2b2](https://n2c2.dbmi.hms.harvard.edu/data-sets) | 未找到可直接公开分发的临床用药状态金标。 |
| [药物相互作用关系](tasks/drug_interaction/task.json) | 100 / 100 | [DDI Corpus 2013](https://github.com/isegura/DDICorpus) | 给定药物对，判断无关系或原文标注的相互作用类型。 |
| [药物与剂量关联](tasks/dose_link/task.json) | 100 / 95 | [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2) | 给定病例全文和剂量片段，从候选药物中选择原始标注关联的药物；不评价剂量是否适宜，也不覆盖频次和途径。 |
| [患者特异性禁忌](tasks/patient_contraindication/task.json) | 0 / 0 | [openFDA drug labels](https://open.fda.gov/apis/drug/label/) | 说明书是材料来源，尚无配套患者及审核金标。 |
| [剂量适宜性](tasks/dose_appropriateness/task.json) | 0 / 0 | 待补 | 未找到已核验、可分发的患者特异性剂量适宜性金标。 |
| [治疗方案选择](tasks/treatment_choice/task.json) | 0 / 0 | [MedJourney](https://github.com/Medical-AI-Learning/MedJourney)、[MedMCQA](https://github.com/medmcqa/medmcqa) | MedJourney 缺明确数据许可；不生成替代金标。 |
| [用药方案选择](tasks/medication_choice/task.json) | 0 / 0 | [MedJourney](https://github.com/Medical-AI-Learning/MedJourney)、[CDrugRed](https://arxiv.org/abs/2511.06230)、[MedMCQA](https://github.com/medmcqa/medmcqa) | MedJourney 缺明确数据许可；CDrugRed 下载源与许可链未完成核验。 |
| [治疗相关不良事件预测](tasks/adverse_event_prediction/task.json) | 0 / 0 | [CT-ADE-SOC / CT-ADE-PT](https://github.com/ds4dh/CT-ADE) | 已找到发布方数据；需核验版本与术语许可，并固定试验组划分。群体结局不能直接解释为个体禁忌。 |

### 住院与护理

核对病情证据、操作执行和病情恶化风险。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [患者与记录身份匹配](tasks/patient_identity/task.json) | 0 / 0 | 待补 | 未取得合适的可分发配对金标。 |
| [长病历证据选择](tasks/long_record_evidence/task.json) | 100 / 20 | [LongHealth](https://github.com/kbressem/LongHealth) | 根据完整病例文书，在原始选项中选择有依据的答案。 |
| [医疗操作进度](tasks/procedure_progress/task.json) | 0 / 0 | 待补 | 现有训练题为自编，未核验外部测试来源。 |
| [单次给药执行状态](tasks/administration_status/task.json) | 0 / 0 | 待补 | 未取得可分发的执行记录及金标。 |
| [脓毒症提前预警](tasks/deterioration_prediction/task.json) | 0 / 0 | [PhysioNet Challenge 2019](https://physionet.org/content/challenge-2019/1.0.0/) | 开放数据已核验；预测窗口、患者划分及类别先验尚未固定，不直接将整段住院结果转成题目。 |

### 出院与随访

识别后续行动、完成状态和出院后的风险。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [随访行动与完成状态](tasks/followup_action/task.json) | 0 / 0 | 待补 | 现有评测为自编题，暂留空。 |
| [出院后 30 天内再入院预测](tasks/readmission_30d/task.json) | 0 / 0 | [UCI Diabetes 130-US Hospitals](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008) | 开放结局数据已核验；需按患者划分，排除死亡等不适用出院并固定特征和基线。 |
| [出院待办行动类别](tasks/followup_item_type/task.json) | 0 / 0 | [CLIP 出院行动标注](https://physionet.org/content/mimic-iii-clinical-action/1.0.0/) | CLIP 有医生标注，但原文受 PhysioNet 凭证与协议限制，不打包进开放主集。 |

### 临床试验筛选

解释入排条件并判断患者转介资格。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [患者与试验匹配](tasks/trial_referral/task.json) | 100 / 58 | [TrialGPT SIGIR](https://github.com/ncbi-nlp/TrialGPT) | 根据患者和试验材料，判断不相关、可能适合或很可能适合转介。 |
| [入排条件要素分类](tasks/criterion_entity_type/task.json) | 100 / 100 | [Chia](https://doi.org/10.6084/m9.figshare.11855817) | 给定条件原文与目标实体，判断原标注的要素类别。 |
| [入排条件限定关系](tasks/criterion_relation/task.json) | 100 / 100 | [Chia](https://doi.org/10.6084/m9.figshare.11855817) | 给定已标注关联的两个要素，判断数值、时间、限定等关系类型。 |
| [入排条件与或关系](tasks/criterion_boolean/task.json) | 100 / 100 | [Chia](https://doi.org/10.6084/m9.figshare.11855817) | 给定条件中的两个标注要素，判断原文要求 AND 还是 OR。 |
| [条件上界与下界](tasks/criterion_bound/task.json) | 100 / 100 | [Clinical Trial Parser annotated test data](https://github.com/facebookresearch/Clinical-Trial-Parser) | 给定条件与数值限制片段，判断该限制是上界还是下界。 |

### 病历与医疗质量控制

识别文书类别、错误、隐私与证据不一致。

| 任务 | 题数 / 来源组 | 来源 | 状态与边界 |
| --- | ---: | --- | --- |
| [病历章节类别](tasks/note_section/task.json) | 100 / 100 | [ACI-Bench](https://github.com/microsoft/clinical_visit_note_summarization_corpus) | 给定去除章节标题的原文片段，选择原始章节类别。 |
| [医学术语归一化](tasks/terminology/task.json) | 0 / 0 | [IMCS-21](https://github.com/lemuria-wchen/imcs21)、[MeDAL](https://github.com/McGill-NLP/medal) | IMCS 数据许可未明确；MeDAL 旧样本为演示数据。 |
| [医疗叙述错误检出](tasks/clinical_error_detection/task.json) | 100 / 100 | [MEDEC-MS](https://github.com/abachaa/MEDEC)、[MedErrBench CN](https://github.com/congboma/MedErrBench) | 判断给定病例文本是否含原数据标注的医学错误。 |
| [医疗叙述错误定位](tasks/clinical_error_location/task.json) | 100 / 100 | [MEDEC-MS](https://github.com/abachaa/MEDEC)、[MedErrBench CN](https://github.com/congboma/MedErrBench) | 在明确含错误的病例中，选择原始标注的错误句。 |
| [研究论断证据关系](tasks/claim_support/task.json) | 100 / 100 | [SciFact](https://github.com/allenai/scifact) | 给定论断与被引摘要，判断支持、反驳或证据不足。 |
| [医疗材料隐私候选](tasks/privacy_candidate/task.json) | 0 / 0 | [n2c2/i2b2](https://n2c2.dbmi.hms.harvard.edu/data-sets) | 现有自编题不进入；临床脱敏语料多需协议。 |
| [病历论断支持关系](tasks/clinical_statement_support/task.json) | 0 / 0 | [MedNLI](https://physionet.org/content/mednli/1.0.0/) | MedNLI 有临床医生标注，但材料来自受控 MIMIC-III，需访问协议。 |

## 版本、抽样和答案

固定种子 20261010；从锁定版本的原文件解析，以标签/量表/来源等已声明分层轮流取样。先尽量每来源组一题，必要时逐步放宽至每组最多五题。去掉重复请求、冲突答案、不能解析的标注和本地训练指纹命中；不复制或改写题目补足数量。DDXPlus 先从完整官方测试 CSV 按哈希取 1,000 条候选。

LongHealth 对 20 个虚构患者各取五题；这些问题共享整份病历。TCM-SD 按原测试分布哈希抽样，不将 148 个证型强行压成每类一题。CHIA 关系题只分类原始已标注关系，不包含自动构造的负例。NUBes 只测否定/不确定。FRD 的数值已由上游替换为 @NUMBER，仅测上下界方向。MedCalc 使用固定 GitHub 测试版本，不能报告为 HF Verified 版本。

答案来自原始发布标注及可重现的机械映射。记录经过格式、定位、映射与去重检查，尚未做本项目独立医生逐题审核。本版本属于可审计初版，不是临床验证金标准。原始训练/开发/测试划分逐题保留；没有官方测试划分的来源不冒称官方测试集。

v0.2.0 新增 MACCROBAT 的检查数值关联、药物剂量关联；检查题仅保留含数字的原始结果片段。候选项为病例中所有有效的对应类型实体，带原文位置以区分重复名称。只收原始 MODIFY 关系可唯一定位目标的题，不构造负关系、不判断处方适宜性。旧版 1,600 题的 ID、请求及金标保留，迁移基线见 [历史身份索引](history/v0.1.0_sample_identity.json)。

## 训练隔离与历史使用

[筛查索引](exposure_index.json) 固定列出本地训练文件及哈希。选中题目没有命中该索引的精确/窗口指纹；543 道题的材料或片段命中过往主评测指纹（通用片段可能误报）。新抽样不等于从未见过的新病例，不能把这部分称为全新盲测。SciFact 额外排除与官方训练声明共用的文档。

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

默认导出及计分只包含 `open` 部分。研究用途需要显式加 `--include-research`，才纳入 DDI 和 TCM-SD；相应题目仍受非商业及相同方式共享等原许可约束。

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
