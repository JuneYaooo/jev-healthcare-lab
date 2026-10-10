# 新增数据来源核验：中文决策任务

核验日期：2026-10-10。新增登记 13 个来源，其中 10 个为中文或含中文，2 个为英文，RD-Triage 的正文语种尚待逐文件核验。PromptCBLUE 等衍生集不视为独立病例来源。

本轮采用 CMB-Exam 与 CNMLEQA-10k，增加 400 道中文病例决策题。v0.3.0 共 2,200 题：开放核心集 2,000，非商业附加集 200；中文共 600 题。旧版 1,800 题的题号、请求和答案未改变。

## 已纳入的任务

| 任务 | 新增题数 | CMB | CNMLEQA |
| --- | ---: | ---: | ---: |
| 临床病例候选诊断 | 100 | 50 | 50 |
| 检查方案选择 | 100 | 19 | 81 |
| 治疗方案选择 | 100 | 46 | 54 |
| 用药方案选择 | 100 | 12 | 88 |

CMB 使用官方测试题和独立答案文件，按 ID 连接并核对元数据。CNMLEQA 使用 Zenodo 固定版本，保留其每题原始来源标识；该来源没有官方测试划分。本次子集经过程序筛选与抽查，答案直接沿用发布标注，并未独立重新审核临床正确性。

## 来源与采用状态

| 来源 | 语种 | 对应场景 | 许可与当前结论 |
| --- | --- | --- | --- |
| [CMB-Exam（中文病例单选子集）](https://github.com/FreedomIntelligence/CMB) | 中文 | 诊断与鉴别、检查与检验、治疗与用药 | Apache-2.0；已收 127 题 |
| [CNMLEQA-10k（中文案例分析子集）](https://doi.org/10.5281/zenodo.18951465) | 中文 | 诊断与鉴别、检查与检验、治疗与用药 | CC-BY-4.0；已收 273 题 |
| [CMExam](https://github.com/williamliujl/CMExam) | 中文 | 诊断与鉴别、检查与检验、治疗与用药 | Apache-2.0（仓库）；README 另限学术/研究使用；许可范围待澄清 |
| [CBLUE（KUAKE-QIC / CHIP-CTC / CHIP-CDN）](https://github.com/CBLUEbenchmark/CBLUE) | 中文 | 接诊与分诊、临床试验筛选、病历与医疗质量控制 | Apache-2.0（代码）；天池数据包协议待核验；需官方数据条款 |
| [PromptCBLUE](https://github.com/michael-wzhu/PromptCBLUE) | 中文 | 接诊与分诊、临床试验筛选、病历与医疗质量控制 | 未核验到覆盖全部上游数据的独立分发许可；衍生来源待核验 |
| [MLEC-QA](https://github.com/Judenpech/MLEC-QA) | 中文 | 诊断与鉴别、检查与检验、治疗与用药 | MIT（代码）；下载包数据许可待核验；下载包待核验 |
| [RJUA-MedDQA](https://github.com/AQ-MedAI/medDQA_benchmark) | 中文 | 检查与检验、诊断与鉴别 | CC-BY-NC-SA-4.0（数据）；AGPL（代码）；完整数据入口待核验 |
| [MedXpertQA](https://github.com/TsinghuaC3I/MedXpertQA) | 英文 | 诊断与鉴别、检查与检验、治疗与用药 | MIT（数据卡）；论文另要求不在线分享题例；发布条件待澄清 |
| [MedHallu](https://github.com/MedHallu/MedHallu) | 英文 | 病历与医疗质量控制 | MIT（项目）；PubMedQA 等上游材料需核验；数据与标签质量待核验 |
| [MedEthicEval](https://github.com/X-LANCE/MedEthicEval) | 中文 | 病历与医疗质量控制 | 公开仓库未见明确数据许可证；数据许可待明确 |
| [RD-Triage](https://github.com/zhelishisongjie/RD-Triage) | 待核验 | 接诊与分诊 | MIT（仓库）；RareBench 等上游条款待核验；优先核验分诊候选 |
| [ClinicalMC / ClinicalMPD](https://github.com/hzyuezh/ClinicalMPD) | 中文、英文 | 接诊与分诊、检查与检验、诊断与鉴别、治疗与用药、住院与护理、出院与随访 | 仓库未见明确数据许可证；上游 MedEureka / PMC-Patients 需核验；工作流候选待核验 |
| [CARE-MI](https://github.com/Meetyou-AI-Lab/CARE-MI) | 中文 | 病历与医疗质量控制 | Apache-2.0（代码）；完整数据及上游许可待核验；完整数据及许可待核验 |

## 未收录原因与下一步

下面的任务映射是本项目对适配方向的判断，不代表来源已具有当前任务所需的全部字段或金标。

### CMExam

中文医考题，不是病历。 测试 CSV 有原答案及疾病、科室、能力等标注。

Apache 标识与 README 学术/研究限制并存，先澄清数据授权范围；病例题也需筛选。 [核验依据](https://github.com/williamliujl/CMExam)。

### CBLUE（KUAKE-QIC / CHIP-CTC / CHIP-CDN）

医疗搜索问题、试验标准及诊断术语，材料性质分任务。 QIC 为意图分类，CTC 为 44 类标准；CDN 为诊断归一化。公开测试通常不带答案，可研究开发集。

不能用代码许可替代数据许可；需取得官方数据包及其协议，核验开发集答案，CDN 候选术语表还需核对许可。 [核验依据](https://github.com/CBLUEbenchmark/CBLUE)。

### PromptCBLUE

CBLUE 等任务的指令化衍生集合。 部分分类任务可恢复有限标签；其余为抽取/生成。

优先回到 CBLUE 原任务核验许可和划分；不把模板改写当独立来源或独立病例，不纳入生成子任务。 [核验依据](https://github.com/michael-wzhu/PromptCBLUE)。

### MLEC-QA

中文执业医师考试题，包含共享病例题干。 公开说明含题型、选项和答案；官方入口为 Google Drive。

需下载官方包核对独立数据许可、测试划分和共享题干；仅收病例决策单选。 [核验依据](https://github.com/Judenpech/MLEC-QA)。

### RJUA-MedDQA

泌尿科真实报告影像及专家标注，发布方声明。 含报告数值推理及临床推理单选，也有自由回答。

仓库目前给示例、README 仍称完整集将发布；需核验完整下载、OCR 对齐和单选金标，若采用只入非商业附加集。 [核验依据](https://github.com/AQ-MedAI/medDQA_benchmark)。

### MedXpertQA

专家复核的医学考试改写题；分 Text 与 MM。 原选项、label、medical_task、question_type 可用；Diagnosis 标签也含检查选择，需再细分。

论文附录提出不在线分享题例；在与 MIT 数据卡的适用范围澄清前仅引用，不在本仓库再分发题目。 [核验依据](https://proceedings.mlr.press/v267/zuo25a.html)。

### MedHallu

论文问答上自动构造的正确/幻觉答案；不是真实临床错误。 二分类适配可能可行，但生成标签不等于逐条医生审核。

官方代码与论文已定位；完整数据下载及上游摘要许可待核验，只考虑错误判别，不收生成任务。 [核验依据](https://github.com/MedHallu/MedHallu)。

### MedEthicEval

中文医疗伦理知识、违规场景与伦理两难。 违规识别可作分类；平衡两难不应强行产生唯一答案。

需明确数据再分发许可和违规类别答案，只考虑有明确标签的违规识别；不收开放伦理解释。 [核验依据](https://github.com/X-LANCE/MedEthicEval)。

### RD-Triage

罕见病病例报告/表型改编的初诊科室分流。 629 条、固定 30 科室；部分题有多个可接受科室，不能只保留其中一个。

优先核对上游来源许可与 PMID、单标签数量和诊断泄露；论文尚在审稿，适用范围为罕见病。 [核验依据](https://github.com/zhelishisongjie/RD-Triage)。

### ClinicalMC / ClinicalMPD

发布论文称 1,275 中文、5,804 英文多病程样本。 科室分流可作有限选择；检查、诊断、治疗等多为开放生成和评判。

只研究可封闭计分的子任务，需核验发布数据、许可及逐时点信息边界，不能把完整住院信息泄漏给早期决策。 [核验依据](https://arxiv.org/abs/2606.03157)。

### CARE-MI

母婴领域知识与题库衍生，包含自动生成的真假陈述。 论文有专家审核与真假题，但主要评价长回答；README 仍称完整集后续发布。

仅研究真假判别子集及人工标签；代码样例不足以认定完整可用，不收自由生成部分。 [核验依据](https://github.com/Meetyou-AI-Lab/CARE-MI)。

## 后续优先级

1. CBLUE：先核验官方数据包协议，再尝试意图识别、试验条件分类与诊断术语归一化。分类适配能增加中文覆盖，但不能冒称新的患者级临床决策能力。
2. RD-Triage：有明确科室候选与标签，优先核验上游许可和完整题目。多答案需保留可接受答案集合，不能任意改成唯一正确科室。
3. RJUA-MedDQA：可补报告结果解释，先核验完整数据入口与图文对齐；适配时保留原 OCR 和所需影像条件。
4. ClinicalMC：场景覆盖好，但许可、逐病程输入边界与封闭答案均需进一步核验；只考虑可明确计分的子任务。

出院与随访、危急结果升级、患者特异性禁忌等仍有缺口。现有候选不足以直接生成这些任务的可靠金标，因此未以自由回答或自造答案补齐。

[完整来源登记](../benchmarks/medical_decision_v1/SOURCES.md) · [任务目录](../benchmarks/medical_decision_v1/README.md) · [最新数据包](../releases/README.md)
