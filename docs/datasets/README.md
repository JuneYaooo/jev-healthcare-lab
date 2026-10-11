# 数据集与参考来源目录

[返回首页](../../README.md) · [任务目录](../tasks/README.md)

登记 80 个来源，其中 34 个实际提供题目。其余仅作调研参考，包括受控数据、许可待核验数据及标准规范，不能按已收录数据集统计。页面中的题数均为本评测集实际采用的数量，不是上游数据总量。

## 开放许可核心集

| 数据集 / 来源说明 | 题数 | 采用任务数 | 材料性质或未采用原因 |
| --- | --- | --- | --- |
| [ACI-Bench](aci_bench.md) | 100 | 1 | 合成就诊会话与人工文书；不是自然发生的医院记录。 |
| [MedQuAD](medquad.md) | 100 | 1 | NIH 旗下网站信息形成的问题；不属于真实患者问诊。 |
| [MEDEC-MS](medec.md) | 100 | 2 | MedQA 考试病例改编与专家错误注入；未使用 UW 受控病历。 |
| [MedErrBench CN](mederr.md) | 100 | 2 | 考试病例改编及专家补充，不声称全部是原始病历。 |
| [NUBes SAMPLE-001](nubes.md) | 100 | 1 | 西班牙语脱敏临床句子；句子打乱，不能据文件恢复患者。 |
| [LongHealth](longhealth.md) | 200 | 2 | 20 个虚构患者；100 道题不是 100 个患者。 |
| [MedCalc-Bench GitHub test release](medcalc.md) | 100 | 1 | 文献提取、生成后人工编辑、模板混合；逐题保留 Note Type。 |
| [SciFact](scifact.md) | 100 | 1 | 科学论文摘要，不全是临床医学。 |
| [Chia](chia.md) | 300 | 3 | 真实 Phase IV 试验入排标准；无患者临床记录。 |
| [Clinical Trial Parser annotated test data](frd.md) | 100 | 1 | 真实试验条件，公开测试文本经过规范化，数字替换为 @NUMBER。 |
| [TrialGPT SIGIR](trialgpt.md) | 100 | 1 | 患者题设配真实试验文件；不是实际入组结局。 |
| [DDXPlus](ddxplus.md) | 100 | 1 | 模拟器生成症状与诊断，不是实际病历。 |
| [PhysioNet Challenge 2019](sepsis2019.md) | 100 | 1 | 真实 ICU 小时记录；只使用公开训练医院 A 中按固定哈希预选的 1,000 个来源记录，非官方隐藏测试。 |
| [MACCROBAT2020](maccrobat.md) | 815 | 9 | 公开发表的临床病例报告；原病例被编辑整理，不等同医院原始 EHR。 |
| [CMB-Exam（中文病例单选子集）](cmb.md) | 454 | 20 | 中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 |
| [CNMLEQA-10k（中文案例分析子集）](cnmleqa.md) | 426 | 15 | 中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。 |
| [Diabetes 130-US Hospitals for Years 1999-2008](uci_diabetes.md) | 100 | 1 | The dataset represents ten years (1999-2008) of clinical care at 130 US hospitals and integrated delivery networks. Each row concerns hospital records of patients diagnosed with diabetes, who underwent laboratory, medications, and stayed up to 14 days. The goal is to determine the early readmission of the patient within 30 days of discharge. The problem is important for the following reasons. Despite high-quality evidence showing improved clinical outcomes for diabetic patients who receive various preventive and therapeutic interventions, many patients do not receive them. This can be partially attributed to arbitrary diabetes management in hospital environments, which fail to attend to glycemic control. Failure to provide proper diabetes care not only increases the managing costs for the hospitals (as the patients are readmitted) but also impacts the morbidity and mortality of the patients, who may face complications associated with diabetes. |
| [Post-Operative Patient](uci_postoperative.md) | 68 | 1 | Dataset of patient features |
| [Heart Failure Clinical Records](uci_heart_failure.md) | 100 | 1 | This dataset contains the medical records of 299 patients who had heart failure, collected during their follow-up period, where each patient profile has 13 clinical features. |
| [Maternal Health Risk](uci_maternal.md) | 100 | 1 | Data has been collected from different hospitals, community clinics, maternal health cares from the rural areas of Bangladesh through the IoT based risk monitoring system. |
| [MEDDOCAN / SPACCC](meddocan.md) | 100 | 1 | 西班牙语公开病例报告经筛选、补入合成个人信息；不能视为原始患者身份记录。 |
| [LabQAR](labqar.md) | 172 | 2 | 根据专家医学参考资料整理的区间与条件；Set 2 数值由作者构造，不是真实患者检验结果。 |
| [CPIC curated pharmacogenomic tables](cpic.md) | 184 | 2 | CPIC 专家整理的功能到表型映射和基因结果用药建议表，不是患者病例。API 的原始响应随数据包冻结，访问日期不冒充数据库发布版本。 |
| [Evidence Inference 2.0 — CC-BY article subset](evidence_inference.md) | 100 | 1 | 已发表临床试验报告及医生判断；不是患者级原始病历。只纳入官方测试文章中 XML 明确标注 CC-BY 的文章。 |
| [TCMEval-SDT](tcmeval_sdt.md) | 100 | 1 | 整理的经典医案、网络及医院病例材料；不是统一采集的前瞻性患者队列。 |
| [TCMEval-PA](tcmeval_pa.md) | 11 | 1 | 考试题与规则情境题，经上游中医执业医师核验；不是实际处方审核日志。 |
| [MedMCQA](medmcqa.md) | 2 | 2 | 印度医学考试题；不是患者观察队列。 |
| [PrinciplismQA](principlismqa.md) | 2 | 1 | 上游模型根据医学伦理教材构造题目，经医学专家审核；不是实际临床记录。 |

## 非商业研究附加集

| 数据集 / 来源说明 | 题数 | 采用任务数 | 材料性质或未采用原因 |
| --- | --- | --- | --- |
| [DDI Corpus 2013](ddi.md) | 100 | 1 | DrugBank / MEDLINE 文本，不是患者处方。 |
| [TCM-SD](tcm_sd.md) | 100 | 1 | 发布论文称真实临床记录；不评价疗效。 |
| [CT-EBM-SP v3](ct_ebm_sp.md) | 858 | 9 | 西班牙语试验注册文本与期刊摘要；不是患者就诊记录。 |
| [E3C English Layer 1](e3c.md) | 385 | 4 | 公开病例报道；Layer 1 人工事件与时间标注。保留各文献原作者、DOI、原文许可。 |
| [CARE-Bench](care_bench.md) | 100 | 1 | 来源约束的重构咨询轨迹；GPT-5.5 辅助构建后人工审核（发布方说明），不是原始真实分诊记录。 |
| [PMR-Synth annotated pairs](pmr_synth.md) | 30 | 1 | 人工合成患者消息，配对去标识病历背景；不能称为真实患者发出的消息。 |

## 仅作参考，未收录题目

| 数据集 / 来源说明 | 题数 | 采用任务数 | 材料性质或未采用原因 |
| --- | --- | --- | --- |
| [IMCS-21](imcs21.md) | 0 | 0 | 未发现明确数据许可 |
| [MeDAL](medal.md) | 0 | 0 | Zenodo v4 与原 README 明确指向 NLM 条款，部分 PubMed 摘要仍可能受第三方版权保护。不能将模型/代码 MIT 或 Apache 许可当作全部摘要数据开放许可；本轮留空。 |
| [CMedCalc-Bench](cmedcalc.md) | 0 | 0 | 公开仓库未见明确数据许可；原文与合成混合 |
| [MedJourney](medjourney.md) | 0 | 0 | 未见明确数据许可；部分任务共用 CMB/CMExam 上游 |
| [CDrugRed](cdrugred.md) | 0 | 0 | 下载入口与官方数据包许可链待核验 |
| [TRIAGE](triage.md) | 0 | 0 | 公开数据未见明确许可，87病例的提示变体不当作独立病例 |
| [THYME](thyme.md) | 0 | 0 | 标注公开不等于临床原文开放，原文需数据协议 |
| [n2c2/i2b2](n2c2.md) | 0 | 0 | 需要相应数据使用协议，不纳入公开题目 |
| [openFDA drug labels](openfda.md) | 0 | 0 | 可作规则材料，尚无对应患者判断题与金标 |
| [PMR-Bench Reddit Test Pairs](pmr_bench.md) | 0 | 0 | 论文 §3.2.1 明确：Reddit 等级由 GPT-5 根据医生回复推导，再配对；并非逐对医生直接标注。本轮保留研究引用，不作为人工金标补入。 |
| [TriageBench（Wong，一致性探针）](triagebench_wong.md) | 0 | 0 | 仅作另行设计的一致性附加实验，不填分诊正确性主任务。 |
| [CLIP 出院行动标注](clip.md) | 0 | 0 | 需凭证、培训及 DUA；只能在获准环境适配，不公开转发原文。 |
| [MIMIC-IV-ED](mimic_iv_ed.md) | 0 | 0 | 需凭证与 DUA；构建入院分诊任务时必须排除出院诊断、去向等未来信息。 |
| [MedNLI](mednli.md) | 0 | 0 | 需凭证及 DUA；不从公开镜像绕过原始访问条件。 |
| [CT-ADE-SOC / CT-ADE-PT](ct_ade.md) | 0 | 0 | 核对数据版本和外部术语条件，按 NCT/试验组隔离；不良事件频率与标签不能作为输入。 |
| [CMExam](cmexam.md) | 0 | 0 | Apache 标识与 README 学术/研究限制并存，先澄清数据授权范围；病例题也需筛选。 |
| [CBLUE（KUAKE-QIC / CHIP-CTC / CHIP-CDN）](cblue.md) | 0 | 0 | 不能用代码许可替代数据许可；需取得官方数据包及其协议，核验开发集答案，CDN 候选术语表还需核对许可。 |
| [PromptCBLUE](promptcblue.md) | 0 | 0 | 优先回到 CBLUE 原任务核验许可和划分；不把模板改写当独立来源或独立病例，不纳入生成子任务。 |
| [MLEC-QA](mlec_qa.md) | 0 | 0 | 需下载官方包核对独立数据许可、测试划分和共享题干；仅收病例决策单选。 |
| [RJUA-MedDQA](rjua_meddqa.md) | 0 | 0 | 仓库目前给示例、README 仍称完整集将发布；需核验完整下载、OCR 对齐和单选金标，若采用只入非商业附加集。 |
| [MedXpertQA](medxpertqa.md) | 0 | 0 | 论文附录提出不在线分享题例；在与 MIT 数据卡的适用范围澄清前仅引用，不在本仓库再分发题目。 |
| [MedHallu](medhallu.md) | 0 | 0 | 官方代码与论文已定位；完整数据下载及上游摘要许可待核验，只考虑错误判别，不收生成任务。 |
| [MedEthicEval](medethiceval.md) | 0 | 0 | 需明确数据再分发许可和违规类别答案，只考虑有明确标签的违规识别；不收开放伦理解释。 |
| [RD-Triage](rd_triage.md) | 0 | 0 | 优先核对上游来源许可与 PMID、单标签数量和诊断泄露；论文尚在审稿，适用范围为罕见病。 |
| [ClinicalMC / ClinicalMPD](clinicalmc.md) | 0 | 0 | 只研究可封闭计分的子任务，需核验发布数据、许可及逐时点信息边界，不能把完整住院信息泄漏给早期决策。 |
| [CARE-MI](care_mi.md) | 0 | 0 | 仅研究真假判别子集及人工标签；代码样例不足以认定完整可用，不收自由生成部分。 |
| [MTCMB](mtcmb.md) | 0 | 0 | 主体包含病历/处方/解释生成和实体抽取；不把这些任务计入决策任务数。考试选择题与已有任务同型；病例来源和原始分发条款待进一步核对。 |
| [CMED / n2c2 2022 Track 1](cmed.md) | 0 | 0 | 具有启停、变更、时态等原标注，但不具备公开转发临床原文的授权。 |
| [FEBRL record linkage datasets](febrl.md) | 0 | 0 | 公开合成身份匹配基准，不是医疗材料的患者身份核实；缺信息时的不确定标签也未覆盖。 |
| [NLI4CT](nli4ct.md) | 0 | 0 | 数据为试验报告论断的支持/矛盾二分类，缺少患者病历的无法确定类别；不替代当前病历三分类任务。 |
| [Chinese-medical-dialogue-data](chinese_medical_dialogue.md) | 0 | 0 | 科室字段是采集来源的分类，未证明为临床审核的最佳首诊科室；不能直接作分流金标。 |
| [FHIR R4 clinical workflow definitions](fhir_workflow.md) | 0 | 0 | 可定义诊断核实、标本链、操作及报告状态；标准示例不等于独立临床金标数据集。 |
| [UCUM unit specification](ucum.md) | 0 | 0 | 提供单位语义与换算标准；本轮未找到符合医疗数值等价判断的独立标注题集。 |
| [MIMIC-IV Clinical Database Demo v2.2](mimic_iv_demo.md) | 0 | 0 | 开放结构化演示数据可作开发材料；本轮未建立覆盖开单、配药、给入、未执行的独立证据与金标协议。不能把已有状态字段原样放进输入再要求选择同一字段。 |
| [TRIAGE-Bench guideline conflicts (DarrenLoong)](triage_bench_conflicts.md) | 0 | 0 | 核验子集引用 DXY/AMBOSS 本地资料路径；未找到完整可公开复核的原始资料及摘录再分发授权。临床行动为开放文本，未强行改造成单选金标。 |
| [UCI Cryotherapy](uci_cryotherapy.md) | 0 | 0 | 官网 CC-BY-4.0 与原 XLSX 内嵌用户协议研究用途限制冲突；未导入。证据位置 Cryotherapy.xlsx!xl/embeddings/Microsoft_Word_Document1.docx。 |
| [UCI Immunotherapy](uci_immunotherapy.md) | 0 | 0 | 原作者使用条件含研究用途限制；不依据外层 CC-BY 标签假定可任意再分发。 |
| [CICTD](cictd.md) | 0 | 0 | 基于 MIMIC-IV 构建；仓库代码 MIT 不解除原始临床数据访问与再分发限制。 |
| [medLLMbenchmark](medllmbenchmark.md) | 0 | 0 | 分诊构建流程依赖 MIMIC-IV/ED/Note；不能公开打包基础病例。 |
| [MedDec](meddec.md) | 0 | 0 | 医学决策抽取标注来自 MIMIC-III 出院记录；代码许可不授权重分发基础记录。 |
| [MedEthicsQA](medethicsqa.md) | 0 | 0 | 5,623 MCQ 大部分源于 Quizlet、Lecturio 等第三方题库；发布方 NC 声明未解决这些底层题目的许可链。小部分来自现有开放题库，不另当新增任务。 |
| [BedsideBench](bedsidebench.md) | 0 | 0 | 公开部分为自由作答和评分 rubric；不自行构造闭集候选及新答案。 |
| [PediaBench](pediabench.md) | 0 | 0 | 未确认可用于本次公开再分发的数据许可，暂不收录。 |
| [MedHALT](medhalt.md) | 0 | 0 | NOTA 的统一缺项标签及虚构问题不能替代真实信息充分性任务；回答核验与已覆盖错误核验有重合，不据此扩增任务数。 |
| [LCMDC](lcmdc.md) | 0 | 0 | 对话科室标签不能直接认定为临床审核的首诊推荐金标；未确认与 department_routing 定义一致的授权标注子集。 |
| [MedTriage](medtriage.md) | 0 | 0 | 论文说明专科分诊评测，但本轮未获取可锁定且明确允许再分发的完整病例与金标文件，不凭论文规模计入题数。 |
