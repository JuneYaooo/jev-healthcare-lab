# 按医疗场景寻找任务与数据

核验日期：2026-10-10。仅有数据可下载，不表示已满足当前任务的题目、答案、许可与隔离要求。以下为新增来源的采用状态和剩余步骤；已采用来源也可只覆盖某个场景的局部任务。

## 接诊与分诊

识别就诊诉求、资料缺口及处理优先级。

任务：事实主体归属、医疗问题意图、决策资料充分性、分诊紧急程度、候选科室分流、患者消息紧急性比较。

已有题目来源：[MedQuAD](https://github.com/abachaa/MedQuAD)。

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

## 检查与检验

选择检查、关联结果并判断结果的适用性与处理需求。

任务：检查检验数值关联、标本身份与来源链、数值与单位等价、参考区间适用性、检验结果趋势、危急结果与人工升级、报告阶段与效力、检查方案选择。

已有题目来源：[MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)。

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

## 诊断与鉴别

根据已有材料判断诊断、状态和临床分级。

任务：否定与不确定状态、事实时间属性、诊断核实状态、有界临床量表评分、临床语义分级、模拟病例主诊断选择、临床病例候选诊断、中医证型选择。

已有题目来源：[DDXPlus](https://doi.org/10.6084/m9.figshare.20043374)、[MedCalc-Bench GitHub test release](https://github.com/ncbi-nlp/MedCalc-Bench)、[NUBes SAMPLE-001](https://github.com/Vicomtech/NUBes-negation-uncertainty-biomedical-corpus)、[TCM-SD](https://github.com/borororo/zy-bert)。

### [MedMCQA](https://github.com/medmcqa/medmcqa)

材料：考试题与原选项答案；不是真实临床结局。

金标：已有单选金标，但按科目划分，不直接提供诊断/检查/治疗决策标签。

许可：Apache-2.0（发布数据卡）；GitHub 代码 MIT。

状态：需任务筛选。需要逐题筛选临床情境与任务类型，核对数据卡与仓库划分数量差异；不混入纯知识记忆题。

[核验依据](https://huggingface.co/datasets/openlifescienceai/medmcqa)。

## 治疗与用药

判断治疗选择、用药关系及患者特异性适宜性。

任务：用药状态与变更、药物相互作用关系、药物与剂量关联、患者特异性禁忌、剂量适宜性、治疗方案选择、用药方案选择、治疗相关不良事件预测。

已有题目来源：[DDI Corpus 2013](https://github.com/isegura/DDICorpus)、[MACCROBAT2020](https://doi.org/10.6084/m9.figshare.9764942.v2)。

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

## 住院与护理

核对病情证据、操作执行和病情恶化风险。

任务：患者与记录身份匹配、长病历证据选择、医疗操作进度、单次给药执行状态、脓毒症提前预警。

已有题目来源：[LongHealth](https://github.com/kbressem/LongHealth)。

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

## 出院与随访

识别后续行动、完成状态和出院后的风险。

任务：随访行动与完成状态、出院后 30 天内再入院预测、出院待办行动类别。

已有题目来源：暂无。

### [UCI Diabetes 130-US Hospitals](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)

材料：1999—2008 年美国医院糖尿病住院结构化记录。

金标：readmitted 表示实际再入院结果，不是最优随访行动标签。

许可：CC-BY-4.0。

状态：需预测协议。按 patient_nbr 隔离；排除不适用出院情况；仅使用出院时已知特征，报告人群和年代限制。

[核验依据](https://doi.org/10.24432/C5230J)。

### [CLIP 出院行动标注](https://physionet.org/content/mimic-iii-clinical-action/1.0.0/)

材料：MIMIC-III 出院记录，部分脱敏占位替换为合成信息。

金标：医生标注的行动片段与类别；Patient Instructions 部分依章节规则标注。

许可：PhysioNet Credentialed Health Data License 1.5.0。

状态：受控访问。需凭证、培训及 DUA；只能在获准环境适配，不公开转发原文。

[核验依据](https://doi.org/10.13026/kw00-z903)。

## 临床试验筛选

解释入排条件并判断患者转介资格。

任务：患者与试验匹配、入排条件要素分类、入排条件限定关系、入排条件与或关系、条件上界与下界。

已有题目来源：[Chia](https://doi.org/10.6084/m9.figshare.11855817)、[Clinical Trial Parser annotated test data](https://github.com/facebookresearch/Clinical-Trial-Parser)、[TrialGPT SIGIR](https://github.com/ncbi-nlp/TrialGPT)。

## 病历与医疗质量控制

识别文书类别、错误、隐私与证据不一致。

任务：病历章节类别、医学术语归一化、医疗叙述错误检出、医疗叙述错误定位、研究论断证据关系、医疗材料隐私候选、病历论断支持关系。

已有题目来源：[ACI-Bench](https://github.com/microsoft/clinical_visit_note_summarization_corpus)、[MEDEC-MS](https://github.com/abachaa/MEDEC)、[MedErrBench CN](https://github.com/congboma/MedErrBench)、[SciFact](https://github.com/allenai/scifact)。

### [MedNLI](https://physionet.org/content/mednli/1.0.0/)

材料：MIMIC-III 病历前提配临床医生撰写的推论。

金标：entailment/contradiction/neutral 三分类医生标签。

许可：PhysioNet Credentialed Health Data License 1.5.0。

状态：受控访问。需凭证及 DUA；不从公开镜像绕过原始访问条件。

[核验依据](https://doi.org/10.13026/C2RS98)。
