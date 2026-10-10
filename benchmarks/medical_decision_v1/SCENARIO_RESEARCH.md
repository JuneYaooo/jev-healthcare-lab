# 按医疗场景寻找任务与数据

核验日期：2026-10-10。仅有数据可下载，不表示已满足当前任务的题目、答案、许可与隔离要求。以下为新增来源的采用状态和剩余步骤；已采用来源也可只覆盖某个场景的局部任务。

## 接诊与分诊

识别就诊诉求、资料缺口及处理优先级。

任务：事实主体归属、医疗问题意图、决策资料充分性、当前分诊与升级行动、候选科室分流、患者消息紧急性比较、孕产风险等级识别。

已有题目来源：[CARE-Bench](https://github.com/ningkko/CARE-bench)、[CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)、[MedQuAD](https://github.com/abachaa/MedQuAD)、[Maternal Health Risk](https://archive.ics.uci.edu/dataset/863/maternal+health+risk)。

### [PMR-Bench Reddit Test Pairs](https://arxiv.org/abs/2601.13178)

材料：患者自述消息的比较；不能称为医院急诊真实分诊记录。

金标：官方测试文件含 1,502 对 chosen/rejected 及等级字段；不采用合成训练对作测试。

许可：CC-BY-NC-4.0。

状态：需抽样协议。固定消息级隔离和配对位置平衡，核对判定者及意见分歧后抽样；只进非商业附加部分。

[核验依据](https://huggingface.co/datasets/PortalPal-AI/PMR-Reddit-Test-Pairs)。

### [TriageBench（Wong，一致性探针）](https://github.com/wongqihan/triagebench)

材料：同一神经症状题设的属性/语言变体。

金标：发布方明确只测一致性、不声称临床正确；不能当正确性金标。

许可：MIT。

状态：不纳入主集。仅作另行设计的一致性附加实验，不填分诊正确性主任务。

[核验依据](https://huggingface.co/datasets/wongqihan/triagebench)。

### [MIMIC-IV-ED](https://physionet.org/content/mimic-iv-ed/2.2/)

材料：真实急诊就诊资料，含分诊、生命体征及出院诊断等表。

金标：分诊 acuity 可作为原记录标签；出院诊断是后验信息。

许可：PhysioNet Credentialed Health Data License。

状态：受控访问。需凭证与 DUA；构建入院分诊任务时必须排除出院诊断、去向等未来信息。

[核验依据](https://physionet.org/content/mimic-iv-ed/2.2/)。

### [CBLUE（KUAKE-QIC / CHIP-CTC / CHIP-CDN）](https://github.com/CBLUEbenchmark/CBLUE)

材料：医疗搜索问题、试验标准及诊断术语，材料性质分任务。

金标：QIC 为意图分类，CTC 为 44 类标准；CDN 为诊断归一化。公开测试通常不带答案，可研究开发集。

许可：Apache-2.0（代码）；天池数据包协议待核验。

状态：需官方数据条款。不能用代码许可替代数据许可；需取得官方数据包及其协议，核验开发集答案，CDN 候选术语表还需核对许可。

[核验依据](https://github.com/CBLUEbenchmark/CBLUE)。

### [PromptCBLUE](https://github.com/michael-wzhu/PromptCBLUE)

材料：CBLUE 等任务的指令化衍生集合。

金标：部分分类任务可恢复有限标签；其余为抽取/生成。

许可：未核验到覆盖全部上游数据的独立分发许可。

状态：衍生来源待核验。优先回到 CBLUE 原任务核验许可和划分；不把模板改写当独立来源或独立病例，不纳入生成子任务。

[核验依据](https://github.com/michael-wzhu/PromptCBLUE)。

### [RD-Triage](https://github.com/zhelishisongjie/RD-Triage)

材料：罕见病病例报告/表型改编的初诊科室分流。

金标：629 条、固定 30 科室；部分题有多个可接受科室，不能只保留其中一个。

许可：MIT（仓库）；RareBench 等上游条款待核验。

状态：优先核验分诊候选。优先核对上游来源许可与 PMID、单标签数量和诊断泄露；论文尚在审稿，适用范围为罕见病。

[核验依据](https://github.com/zhelishisongjie/RD-Triage)。

### [ClinicalMC / ClinicalMPD](https://github.com/hzyuezh/ClinicalMPD)

材料：发布论文称 1,275 中文、5,804 英文多病程样本。

金标：科室分流可作有限选择；检查、诊断、治疗等多为开放生成和评判。

许可：仓库未见明确数据许可证；上游 MedEureka / PMC-Patients 需核验。

状态：工作流候选待核验。只研究可封闭计分的子任务，需核验发布数据、许可及逐时点信息边界，不能把完整住院信息泄漏给早期决策。

[核验依据](https://arxiv.org/abs/2606.03157)。

### [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)

材料：西班牙语试验注册文本与期刊摘要；不是患者就诊记录。

金标：使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

许可：CC-BY-NC-SA-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [CARE-Bench](https://github.com/ningkko/CARE-bench)

材料：来源约束的重构咨询轨迹；GPT-5.5 辅助构建后人工审核（发布方说明），不是原始真实分诊记录。

金标：只用 public_test_1 的四类 gold_label；只给当前已披露患者消息，不给后续轮次、参考回复、信息充分性和构造标签。

许可：CC-BY-NC-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [Maternal Health Risk](https://archive.ics.uci.edu/dataset/863/maternal+health+risk)

材料：Data has been collected from different hospitals, community clinics, maternal health cares from the rural areas of Bangladesh through the IoT based risk monitoring system.

金标：沿用原 RiskLevel，不能当成独立结局随访；完全相同特征冲突全部排除，无患者 ID。

许可：CC-BY-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

## 检查与检验

选择检查、关联结果并判断结果的适用性与处理需求。

任务：检查检验数值关联、标本身份与来源链、数值与单位等价、参考区间适用性、临床事件变化趋势、危急结果与人工升级、报告阶段与效力、检查方案选择。

已有题目来源：[CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)、[MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)。

### [MedMCQA](https://github.com/medmcqa/medmcqa)

材料：考试题与原选项答案；不是真实临床结局。

金标：已有单选金标，但按科目划分，不直接提供诊断/检查/治疗决策标签。

许可：Apache-2.0（发布数据卡）；GitHub 代码 MIT。

状态：需任务筛选。需要逐题筛选临床情境与任务类型，核对数据卡与仓库划分数量差异；不混入纯知识记忆题。

[核验依据](https://huggingface.co/datasets/openlifescienceai/medmcqa)。

### [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)

材料：公开发表的临床病例报告；原病例被编辑整理，不等同医院原始 EHR。

金标：原始 BRAT MODIFY 关系；把事件引用解析为文本实体，只保留目标检查/药物唯一的关联。

许可：CC-BY-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)

材料：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。

金标：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 v0.4.0 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

许可：Apache-2.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)

材料：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。

金标：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 v0.4.0 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

许可：CC-BY-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [CMExam](https://github.com/williamliujl/CMExam)

材料：中文医考题，不是病历。

金标：测试 CSV 有原答案及疾病、科室、能力等标注。

许可：Apache-2.0（仓库）；README 另限学术/研究使用。

状态：许可范围待澄清。Apache 标识与 README 学术/研究限制并存，先澄清数据授权范围；病例题也需筛选。

[核验依据](https://github.com/williamliujl/CMExam)。

### [MLEC-QA](https://github.com/Judenpech/MLEC-QA)

材料：中文执业医师考试题，包含共享病例题干。

金标：公开说明含题型、选项和答案；官方入口为 Google Drive。

许可：MIT（代码）；下载包数据许可待核验。

状态：下载包待核验。需下载官方包核对独立数据许可、测试划分和共享题干；仅收病例决策单选。

[核验依据](https://github.com/Judenpech/MLEC-QA)。

### [RJUA-MedDQA](https://github.com/AQ-MedAI/medDQA_benchmark)

材料：泌尿科真实报告影像及专家标注，发布方声明。

金标：含报告数值推理及临床推理单选，也有自由回答。

许可：CC-BY-NC-SA-4.0（数据）；AGPL（代码）。

状态：完整数据入口待核验。仓库目前给示例、README 仍称完整集将发布；需核验完整下载、OCR 对齐和单选金标，若采用只入非商业附加集。

[核验依据](https://github.com/AQ-MedAI/medDQA_benchmark)。

### [MedXpertQA](https://github.com/TsinghuaC3I/MedXpertQA)

材料：专家复核的医学考试改写题；分 Text 与 MM。

金标：原选项、label、medical_task、question_type 可用；Diagnosis 标签也含检查选择，需再细分。

许可：MIT（数据卡）；论文另要求不在线分享题例。

状态：发布条件待澄清。论文附录提出不在线分享题例；在与 MIT 数据卡的适用范围澄清前仅引用，不在本仓库再分发题目。

[核验依据](https://proceedings.mlr.press/v267/zuo25a.html)。

### [ClinicalMC / ClinicalMPD](https://github.com/hzyuezh/ClinicalMPD)

材料：发布论文称 1,275 中文、5,804 英文多病程样本。

金标：科室分流可作有限选择；检查、诊断、治疗等多为开放生成和评判。

许可：仓库未见明确数据许可证；上游 MedEureka / PMC-Patients 需核验。

状态：工作流候选待核验。只研究可封闭计分的子任务，需核验发布数据、许可及逐时点信息边界，不能把完整住院信息泄漏给早期决策。

[核验依据](https://arxiv.org/abs/2606.03157)。

## 诊断与鉴别

根据已有材料判断诊断、状态和临床分级。

任务：否定与不确定状态、事件与文档时间关系、诊断核实状态、有界临床量表评分、临床分级与分期选择、模拟病例主诊断选择、临床病例候选诊断、中医证型选择、临床事件先后关系、临床事件与解剖部位关联、严重程度与临床事件关联、事件与时间表达关联、病例病因与原因判断。

已有题目来源：[CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)、[DDXPlus](https://doi.org/10.6084/m9.figshare.20043374)、[E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus)、[MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)、[MedCalc-Bench GitHub test release](https://github.com/ncbi-nlp/MedCalc-Bench)、[NUBes SAMPLE-001](https://github.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus)、[TCM-SD](https://github.com/borororo/zy-bert)。

### [MedMCQA](https://github.com/medmcqa/medmcqa)

材料：考试题与原选项答案；不是真实临床结局。

金标：已有单选金标，但按科目划分，不直接提供诊断/检查/治疗决策标签。

许可：Apache-2.0（发布数据卡）；GitHub 代码 MIT。

状态：需任务筛选。需要逐题筛选临床情境与任务类型，核对数据卡与仓库划分数量差异；不混入纯知识记忆题。

[核验依据](https://huggingface.co/datasets/openlifescienceai/medmcqa)。

### [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)

材料：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。

金标：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 v0.4.0 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

许可：Apache-2.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)

材料：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。

金标：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 v0.4.0 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

许可：CC-BY-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [CMExam](https://github.com/williamliujl/CMExam)

材料：中文医考题，不是病历。

金标：测试 CSV 有原答案及疾病、科室、能力等标注。

许可：Apache-2.0（仓库）；README 另限学术/研究使用。

状态：许可范围待澄清。Apache 标识与 README 学术/研究限制并存，先澄清数据授权范围；病例题也需筛选。

[核验依据](https://github.com/williamliujl/CMExam)。

### [MLEC-QA](https://github.com/Judenpech/MLEC-QA)

材料：中文执业医师考试题，包含共享病例题干。

金标：公开说明含题型、选项和答案；官方入口为 Google Drive。

许可：MIT（代码）；下载包数据许可待核验。

状态：下载包待核验。需下载官方包核对独立数据许可、测试划分和共享题干；仅收病例决策单选。

[核验依据](https://github.com/Judenpech/MLEC-QA)。

### [RJUA-MedDQA](https://github.com/AQ-MedAI/medDQA_benchmark)

材料：泌尿科真实报告影像及专家标注，发布方声明。

金标：含报告数值推理及临床推理单选，也有自由回答。

许可：CC-BY-NC-SA-4.0（数据）；AGPL（代码）。

状态：完整数据入口待核验。仓库目前给示例、README 仍称完整集将发布；需核验完整下载、OCR 对齐和单选金标，若采用只入非商业附加集。

[核验依据](https://github.com/AQ-MedAI/medDQA_benchmark)。

### [MedXpertQA](https://github.com/TsinghuaC3I/MedXpertQA)

材料：专家复核的医学考试改写题；分 Text 与 MM。

金标：原选项、label、medical_task、question_type 可用；Diagnosis 标签也含检查选择，需再细分。

许可：MIT（数据卡）；论文另要求不在线分享题例。

状态：发布条件待澄清。论文附录提出不在线分享题例；在与 MIT 数据卡的适用范围澄清前仅引用，不在本仓库再分发题目。

[核验依据](https://proceedings.mlr.press/v267/zuo25a.html)。

### [ClinicalMC / ClinicalMPD](https://github.com/hzyuezh/ClinicalMPD)

材料：发布论文称 1,275 中文、5,804 英文多病程样本。

金标：科室分流可作有限选择；检查、诊断、治疗等多为开放生成和评判。

许可：仓库未见明确数据许可证；上游 MedEureka / PMC-Patients 需核验。

状态：工作流候选待核验。只研究可封闭计分的子任务，需核验发布数据、许可及逐时点信息边界，不能把完整住院信息泄漏给早期决策。

[核验依据](https://arxiv.org/abs/2606.03157)。

### [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)

材料：西班牙语试验注册文本与期刊摘要；不是患者就诊记录。

金标：使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

许可：CC-BY-NC-SA-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus)

材料：公开病例报道；Layer 1 人工事件与时间标注。保留各文献原作者、DOI、原文许可。

金标：仅官方英文测试文档；原 docTimeRel、permanence、TIMEX3 类型及 timexLink 唯一目标机械适配，不使用自动标注层。

许可：CC-BY-NC (publisher does not specify version)。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [MTCMB](https://github.com/Wayyuanyuan/MTCMB)

材料：教材、医考题库、古籍、专家医案及 CCL/Tianchi 衍生；不能统称自然发生的临床记录。

金标：部分为选择题、部分为自由文本或多字段答案；未转换为本次评测题。

许可：CC-BY-4.0（发布方 Zenodo 数据声明）；各上游来源仍需核对。

状态：scope_and_upstream_terms_pending。主体包含病历/处方/解释生成和实体抽取；不把这些任务计入决策任务数。考试选择题与已有任务同型；病例来源和原始分发条款待进一步核对。

[核验依据](https://github.com/Wayyuanyuan/MTCMB/blob/faffd813c67fe012cef74277a23270d5dd6db9b8/ReadMe_cn.md)。

## 治疗与用药

判断治疗选择、用药关系及患者特异性适宜性。

任务：用药状态与变更、药物相互作用关系、药物与剂量关联、患者特异性禁忌选择、剂量适宜性、治疗方案选择、用药方案选择、治疗相关不良事件预测、给药途径关联、用药或操作频次关联、药物剂型关联、补液方案选择。

已有题目来源：[CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)、[CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)、[DDI Corpus 2013](https://github.com/isegura/DDICorpus)、[MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)。

### [MedMCQA](https://github.com/medmcqa/medmcqa)

材料：考试题与原选项答案；不是真实临床结局。

金标：已有单选金标，但按科目划分，不直接提供诊断/检查/治疗决策标签。

许可：Apache-2.0（发布数据卡）；GitHub 代码 MIT。

状态：需任务筛选。需要逐题筛选临床情境与任务类型，核对数据卡与仓库划分数量差异；不混入纯知识记忆题。

[核验依据](https://huggingface.co/datasets/openlifescienceai/medmcqa)。

### [CT-ADE-SOC / CT-ADE-PT](https://github.com/ds4dh/CT-ADE)

材料：临床试验组层面的单药与不良事件数据。

金标：ClinicalTrials.gov 结果派生的多标签结局；不是个体药物因果或禁忌标签。

许可：MIT（SOC 数据卡）；第三方术语与补充源需单独核验。

状态：需预测协议。核对数据版本和外部术语条件，按 NCT/试验组隔离；不良事件频率与标签不能作为输入。

[核验依据](https://huggingface.co/datasets/anthonyyazdaniml/CT-ADE-SOC)。

### [MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)

材料：公开发表的临床病例报告；原病例被编辑整理，不等同医院原始 EHR。

金标：原始 BRAT MODIFY 关系；把事件引用解析为文本实体，只保留目标检查/药物唯一的关联。

许可：CC-BY-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)

材料：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。

金标：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 v0.4.0 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

许可：Apache-2.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)

材料：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。

金标：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 v0.4.0 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

许可：CC-BY-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [CMExam](https://github.com/williamliujl/CMExam)

材料：中文医考题，不是病历。

金标：测试 CSV 有原答案及疾病、科室、能力等标注。

许可：Apache-2.0（仓库）；README 另限学术/研究使用。

状态：许可范围待澄清。Apache 标识与 README 学术/研究限制并存，先澄清数据授权范围；病例题也需筛选。

[核验依据](https://github.com/williamliujl/CMExam)。

### [MLEC-QA](https://github.com/Judenpech/MLEC-QA)

材料：中文执业医师考试题，包含共享病例题干。

金标：公开说明含题型、选项和答案；官方入口为 Google Drive。

许可：MIT（代码）；下载包数据许可待核验。

状态：下载包待核验。需下载官方包核对独立数据许可、测试划分和共享题干；仅收病例决策单选。

[核验依据](https://github.com/Judenpech/MLEC-QA)。

### [MedXpertQA](https://github.com/TsinghuaC3I/MedXpertQA)

材料：专家复核的医学考试改写题；分 Text 与 MM。

金标：原选项、label、medical_task、question_type 可用；Diagnosis 标签也含检查选择，需再细分。

许可：MIT（数据卡）；论文另要求不在线分享题例。

状态：发布条件待澄清。论文附录提出不在线分享题例；在与 MIT 数据卡的适用范围澄清前仅引用，不在本仓库再分发题目。

[核验依据](https://proceedings.mlr.press/v267/zuo25a.html)。

### [ClinicalMC / ClinicalMPD](https://github.com/hzyuezh/ClinicalMPD)

材料：发布论文称 1,275 中文、5,804 英文多病程样本。

金标：科室分流可作有限选择；检查、诊断、治疗等多为开放生成和评判。

许可：仓库未见明确数据许可证；上游 MedEureka / PMC-Patients 需核验。

状态：工作流候选待核验。只研究可封闭计分的子任务，需核验发布数据、许可及逐时点信息边界，不能把完整住院信息泄漏给早期决策。

[核验依据](https://arxiv.org/abs/2606.03157)。

### [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)

材料：西班牙语试验注册文本与期刊摘要；不是患者就诊记录。

金标：使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

许可：CC-BY-NC-SA-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [MTCMB](https://github.com/Wayyuanyuan/MTCMB)

材料：教材、医考题库、古籍、专家医案及 CCL/Tianchi 衍生；不能统称自然发生的临床记录。

金标：部分为选择题、部分为自由文本或多字段答案；未转换为本次评测题。

许可：CC-BY-4.0（发布方 Zenodo 数据声明）；各上游来源仍需核对。

状态：scope_and_upstream_terms_pending。主体包含病历/处方/解释生成和实体抽取；不把这些任务计入决策任务数。考试选择题与已有任务同型；病例来源和原始分发条款待进一步核对。

[核验依据](https://github.com/Wayyuanyuan/MTCMB/blob/faffd813c67fe012cef74277a23270d5dd6db9b8/ReadMe_cn.md)。

## 住院与护理

核对病情证据、操作执行和病情恶化风险。

任务：患者与记录身份匹配、长病历证据选择、医疗操作进度、单次给药执行状态、脓毒症提前预警、术后转归去向选择、子操作与所属操作关联、临床事件持续性、病例并发症判断、护理措施选择。

已有题目来源：[CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465)、[E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus)、[LongHealth](https://github.com/kbressem/LongHealth)、[MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)、[Post-Operative Patient](https://archive.ics.uci.edu/dataset/82/post+operative+patient)。

### [PhysioNet Challenge 2019](https://physionet.org/content/challenge-2019/1.0.0/)

材料：真实 ICU 的生命体征与检验时序，公开训练部分。

金标：基于挑战定义的 SepsisLabel；官方隐藏测试不能假称已取得。

许可：CC-BY-4.0。

状态：需预测协议。先固定预测时点/提前窗口、患者划分与基线；公开训练材料构建的自留评测应明确标注，不能直接代表是否应转 ICU。

[核验依据](https://physionet.org/content/challenge-2019/1.0.0/)。

### [MIMIC-IV-ED](https://physionet.org/content/mimic-iv-ed/2.2/)

材料：真实急诊就诊资料，含分诊、生命体征及出院诊断等表。

金标：分诊 acuity 可作为原记录标签；出院诊断是后验信息。

许可：PhysioNet Credentialed Health Data License。

状态：受控访问。需凭证与 DUA；构建入院分诊任务时必须排除出院诊断、去向等未来信息。

[核验依据](https://physionet.org/content/mimic-iv-ed/2.2/)。

### [ClinicalMC / ClinicalMPD](https://github.com/hzyuezh/ClinicalMPD)

材料：发布论文称 1,275 中文、5,804 英文多病程样本。

金标：科室分流可作有限选择；检查、诊断、治疗等多为开放生成和评判。

许可：仓库未见明确数据许可证；上游 MedEureka / PMC-Patients 需核验。

状态：工作流候选待核验。只研究可封闭计分的子任务，需核验发布数据、许可及逐时点信息边界，不能把完整住院信息泄漏给早期决策。

[核验依据](https://arxiv.org/abs/2606.03157)。

### [E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus)

材料：公开病例报道；Layer 1 人工事件与时间标注。保留各文献原作者、DOI、原文许可。

金标：仅官方英文测试文档；原 docTimeRel、permanence、TIMEX3 类型及 timexLink 唯一目标机械适配，不使用自动标注层。

许可：CC-BY-NC (publisher does not specify version)。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [Post-Operative Patient](https://archive.ics.uci.edu/dataset/82/post+operative+patient)

材料：Dataset of patient features

金标：ADM-DECS 原术后去向标签；相同输入冲突全部排除，无患者 ID，不冒称患者独立。

许可：CC-BY-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

## 出院与随访

识别后续行动、完成状态和出院后的风险。

任务：随访行动与完成状态、出院后 30 天内再入院预测、出院待办行动类别、90 日死亡结局预测。

已有题目来源：[Diabetes 130-US Hospitals for Years 1999-2008](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)、[Heart Failure Clinical Records](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records)。

### [CLIP 出院行动标注](https://physionet.org/content/mimic-iii-clinical-action/1.0.0/)

材料：MIMIC-III 出院记录，部分脱敏占位替换为合成信息。

金标：医生标注的行动片段与类别；Patient Instructions 部分依章节规则标注。

许可：PhysioNet Credentialed Health Data License 1.5.0。

状态：受控访问。需凭证、培训及 DUA；只能在获准环境适配，不公开转发原文。

[核验依据](https://doi.org/10.13026/kw00-z903)。

### [ClinicalMC / ClinicalMPD](https://github.com/hzyuezh/ClinicalMPD)

材料：发布论文称 1,275 中文、5,804 英文多病程样本。

金标：科室分流可作有限选择；检查、诊断、治疗等多为开放生成和评判。

许可：仓库未见明确数据许可证；上游 MedEureka / PMC-Patients 需核验。

状态：工作流候选待核验。只研究可封闭计分的子任务，需核验发布数据、许可及逐时点信息边界，不能把完整住院信息泄漏给早期决策。

[核验依据](https://arxiv.org/abs/2606.03157)。

### [Diabetes 130-US Hospitals for Years 1999-2008](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)

材料：The dataset represents ten years (1999-2008) of clinical care at 130 US hospitals and integrated delivery networks. Each row concerns hospital records of patients diagnosed with diabetes, who underwent laboratory, medications, and stayed up to 14 days. The goal is to determine the early readmission of the patient within 30 days of discharge.
The problem is important for the following reasons. Despite high-quality evidence showing improved clinical outcomes for diabetic patients who receive various preventive and therapeutic interventions, many patients do not receive them. This can be partially attributed to arbitrary diabetes management in hospital environments, which fail to attend to glycemic control. Failure to provide proper diabetes care not only increases the managing costs for the hospitals (as the patients are readmitted) but also impacts the morbidity and mortality of the patients, who may face complications associated with diabetes.


金标：按患者取首个合格住院；出院去向只保留回家 (1)；readmitted <30 为阳性，其他为未观察到 30 日内再入院。输入移除患者 ID、住院 ID 和再入院标签。

许可：CC-BY-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [Heart Failure Clinical Records](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records)

材料：This dataset contains the medical records of 299 patients who had heart failure, collected during their follow-up period, where each patient profile has 13 clinical features.

金标：90 日死亡：time<=90 且 DEATH_EVENT=1 为阳性；time>=90 且无此前死亡为阴性；90 日前删失排除。time 与死亡标签不输入。

许可：CC-BY-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

## 临床试验筛选

解释入排条件并判断患者转介资格。

任务：患者与试验匹配、入排条件要素分类、入排条件限定关系、入排条件与或关系、条件上界与下界、病程与疗程时长关联、联合干预对象关联、干预用途关联。

已有题目来源：[Chia](https://doi.org/10.6084/m9.figshare.11855817)、[CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)、[Clinical Trial Parser annotated test data](https://github.com/facebookresearch/Clinical-Trial-Parser)、[TrialGPT SIGIR](https://github.com/ncbi-nlp/TrialGPT)。

### [CBLUE（KUAKE-QIC / CHIP-CTC / CHIP-CDN）](https://github.com/CBLUEbenchmark/CBLUE)

材料：医疗搜索问题、试验标准及诊断术语，材料性质分任务。

金标：QIC 为意图分类，CTC 为 44 类标准；CDN 为诊断归一化。公开测试通常不带答案，可研究开发集。

许可：Apache-2.0（代码）；天池数据包协议待核验。

状态：需官方数据条款。不能用代码许可替代数据许可；需取得官方数据包及其协议，核验开发集答案，CDN 候选术语表还需核对许可。

[核验依据](https://github.com/CBLUEbenchmark/CBLUE)。

### [PromptCBLUE](https://github.com/michael-wzhu/PromptCBLUE)

材料：CBLUE 等任务的指令化衍生集合。

金标：部分分类任务可恢复有限标签；其余为抽取/生成。

许可：未核验到覆盖全部上游数据的独立分发许可。

状态：衍生来源待核验。优先回到 CBLUE 原任务核验许可和划分；不把模板改写当独立来源或独立病例，不纳入生成子任务。

[核验依据](https://github.com/michael-wzhu/PromptCBLUE)。

### [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)

材料：西班牙语试验注册文本与期刊摘要；不是患者就诊记录。

金标：使用 brat/test 原始人工属性和关系；频次与剂型关联另外使用 brat/dev，逐题保留划分。实体片段或关联目标有限选择；不导出 UMLS 术语库，不构造未标注负例。

许可：CC-BY-NC-SA-4.0。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

## 病历与医疗质量控制

识别文书类别、错误、隐私与证据不一致。

任务：病历章节类别、医学术语归一化、医疗叙述错误检出、医疗叙述错误定位、研究论断证据关系、医疗材料隐私候选、病历论断支持关系、同一临床事件指代关联、文本因果结果关联、否定或推测线索作用对象、临床时间表达类别。

已有题目来源：[ACI-Bench](https://github.com/microsoft/clinical_visit_note_summarization_corpus)、[CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3)、[E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus)、[MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)、[MEDEC-MS](https://github.com/abachaa/MEDEC)、[MedErrBench CN](https://github.com/congboma/MedErrBench)、[SciFact](https://github.com/allenai/scifact)。

### [MedNLI](https://physionet.org/content/mednli/1.0.0/)

材料：MIMIC-III 病历前提配临床医生撰写的推论。

金标：entailment/contradiction/neutral 三分类医生标签。

许可：PhysioNet Credentialed Health Data License 1.5.0。

状态：受控访问。需凭证及 DUA；不从公开镜像绕过原始访问条件。

[核验依据](https://doi.org/10.13026/C2RS98)。

### [CBLUE（KUAKE-QIC / CHIP-CTC / CHIP-CDN）](https://github.com/CBLUEbenchmark/CBLUE)

材料：医疗搜索问题、试验标准及诊断术语，材料性质分任务。

金标：QIC 为意图分类，CTC 为 44 类标准；CDN 为诊断归一化。公开测试通常不带答案，可研究开发集。

许可：Apache-2.0（代码）；天池数据包协议待核验。

状态：需官方数据条款。不能用代码许可替代数据许可；需取得官方数据包及其协议，核验开发集答案，CDN 候选术语表还需核对许可。

[核验依据](https://github.com/CBLUEbenchmark/CBLUE)。

### [PromptCBLUE](https://github.com/michael-wzhu/PromptCBLUE)

材料：CBLUE 等任务的指令化衍生集合。

金标：部分分类任务可恢复有限标签；其余为抽取/生成。

许可：未核验到覆盖全部上游数据的独立分发许可。

状态：衍生来源待核验。优先回到 CBLUE 原任务核验许可和划分；不把模板改写当独立来源或独立病例，不纳入生成子任务。

[核验依据](https://github.com/michael-wzhu/PromptCBLUE)。

### [MedHallu](https://github.com/MedHallu/MedHallu)

材料：论文问答上自动构造的正确/幻觉答案；不是真实临床错误。

金标：二分类适配可能可行，但生成标签不等于逐条医生审核。

许可：MIT（项目）；PubMedQA 等上游材料需核验。

状态：数据与标签质量待核验。官方代码与论文已定位；完整数据下载及上游摘要许可待核验，只考虑错误判别，不收生成任务。

[核验依据](https://github.com/MedHallu/MedHallu)。

### [MedEthicEval](https://github.com/X-LANCE/MedEthicEval)

材料：中文医疗伦理知识、违规场景与伦理两难。

金标：违规识别可作分类；平衡两难不应强行产生唯一答案。

许可：公开仓库未见明确数据许可证。

状态：数据许可待明确。需明确数据再分发许可和违规类别答案，只考虑有明确标签的违规识别；不收开放伦理解释。

[核验依据](https://github.com/X-LANCE/MedEthicEval)。

### [CARE-MI](https://github.com/Meetyou-AI-Lab/CARE-MI)

材料：母婴领域知识与题库衍生，包含自动生成的真假陈述。

金标：论文有专家审核与真假题，但主要评价长回答；README 仍称完整集后续发布。

许可：Apache-2.0（代码）；完整数据及上游许可待核验。

状态：完整数据及许可待核验。仅研究真假判别子集及人工标签；代码样例不足以认定完整可用，不收自由生成部分。

[核验依据](https://github.com/Meetyou-AI-Lab/CARE-MI)。

### [E3C English Layer 1](https://github.com/hltfbk/E3C-Corpus)

材料：公开病例报道；Layer 1 人工事件与时间标注。保留各文献原作者、DOI、原文许可。

金标：仅官方英文测试文档；原 docTimeRel、permanence、TIMEX3 类型及 timexLink 唯一目标机械适配，不使用自动标注层。

许可：CC-BY-NC (publisher does not specify version)。

状态：已采用。抽样和转换见任务目录及逐题来源定位。

### [MTCMB](https://github.com/Wayyuanyuan/MTCMB)

材料：教材、医考题库、古籍、专家医案及 CCL/Tianchi 衍生；不能统称自然发生的临床记录。

金标：部分为选择题、部分为自由文本或多字段答案；未转换为本次评测题。

许可：CC-BY-4.0（发布方 Zenodo 数据声明）；各上游来源仍需核对。

状态：scope_and_upstream_terms_pending。主体包含病历/处方/解释生成和实体抽取；不把这些任务计入决策任务数。考试选择题与已有任务同型；病例来源和原始分发条款待进一步核对。

[核验依据](https://github.com/Wayyuanyuan/MTCMB/blob/faffd813c67fe012cef74277a23270d5dd6db9b8/ReadMe_cn.md)。
