# v0.5.0 空缺任务核验与新增数据

2026-10-10 核验 v0.4.0 中的 21 个空任务。本版采用 3 项、增加 272 题；18 项继续为空。现有 73 个任务定义中，55 个有题，共 5,210 题，其中 48 个任务各 100 题、7 个任务不足 100 题。中文仍为 1,012 题。此前 4,938 条完整记录保持不变。

检索范围包括原发布仓库、论文、数据托管页、许可和样本结构。下列“留空”表示本轮没有确认可直接采用的来源，不表示世界上不存在相关数据；找到相邻题材也不代表已有当前任务的金标。

## 逐项结果

| 任务 | 本轮结果 | 核验来源与原因 |
| --- | --- | --- |
| 诊断核实状态 | 留空 | [fhir_workflow](https://hl7.org/fhir/R4/)、[e3c](https://github.com/hltfbk/E3C-Corpus)。FHIR 有核实状态定义；E3C 的实际/假设/不确定是事件属性，不能等同疑似/确诊/排除四分类。未找到匹配且可开放分发的原金标。 |
| 用药状态与变更 | 留空 | [cmed](https://n2c2.dbmi.hms.harvard.edu/2022-track-1)、[n2c2](https://n2c2.dbmi.hms.harvard.edu/data-sets)。CMED/n2c2 原标注相关，但临床文本受协议限制；未取得可公开再分发的替代语料。 |
| 患者与记录身份匹配 | 留空 | [febrl](https://recordlinkage.readthedocs.io/en/latest/ref-datasets.html)、[mimic_iv_demo](https://physionet.org/content/mimic-iv-demo/2.2/)。FEBRL 是合成人口学匹配，MIMIC 演示 ID 连接不是身份可确定性评测；缺医疗证据、冲突及不确定金标。 |
| 标本身份与来源链 | 留空 | [fhir_workflow](https://hl7.org/fhir/R4/)。FHIR Specimen.parent 提供字段和示例；未找到同物、派生、无关、未知四类的开放标注病例。 |
| 医学术语归一化 | 留空 | [medal](https://github.com/McGill-NLP/medal)、[imcs21](https://github.com/lemuria-wchen/imcs21)、[cblue](https://github.com/CBLUEbenchmark/CBLUE)。MeDAL 原摘要版权尚未闭合；IMCS21 未明确数据许可；CBLUE 的术语材料及授权需按任务核验，不用代码许可证代替。 |
| 决策资料充分性 | 留空 | [cmedcalc](https://github.com/Zhihong-Zhu/CMedCalc-Bench)、[care_bench](https://github.com/ningkko/CARE-bench)。CMedCalc 数据再分发许可未明确；CARE-Bench 的 need_info 是分诊行动标签，不能代表计算要素齐全及冲突消解。 |
| 数值与单位等价 | 留空 | [ucum](https://ucum.org/ucum)。UCUM 提供换算依据，本轮未找到独立标注的医疗数值等价题集；不自行改数值生成金标。 |
| 参考区间适用性 | 72 题 | [labqar](https://doi.org/10.6084/m9.figshare.29189894)。采用 LabQAR Set 1 原范围答案，给定同检验/单位/类别的原参考条目后判断人群、标本与条件匹配；排除条件冲突、非区间及无候选项，不补造干扰项。 |
| 剂量适宜性 | 留空 | [openfda](https://open.fda.gov/apis/drug/label/)、[cmedcalc](https://github.com/Zhihong-Zhu/CMedCalc-Bench)。openFDA 是药品说明书规则；尚缺患者肝肾功能、具体处方及独立剂量适宜性金标。 |
| 危急结果与人工升级 | 留空 | [openfda](https://open.fda.gov/apis/drug/label/)、[care_bench](https://github.com/ningkko/CARE-bench)。现有规则/分诊数据不提供机构危急值阈值版本、复核条件及升级等级的匹配金标。 |
| 医疗材料隐私候选 | 100 题 | [meddocan](https://github.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN)。采用 MEDDOCAN 官方测试标注；词级 PHI/非 PHI 二选一，每文档至多选一题，正负各 50。 |
| 医疗操作进度 | 留空 | [fhir_workflow](https://hl7.org/fhir/R4/)、[e3c](https://github.com/hltfbk/E3C-Corpus)。操作状态标准与 E3C 事件时态不同；未找到完整覆盖计划、进行、完成、取消、目标未达成的开放金标。 |
| 单次给药执行状态 | 留空 | [mimic_iv_demo](https://physionet.org/content/mimic-iv-demo/2.2/)、[fhir_workflow](https://hl7.org/fhir/R4/)。MIMIC 演示为真实结构化事件；尚缺跨医嘱、配药、给入的可判定证据与统一答案协议，留空。 |
| 随访行动与完成状态 | 留空 | [clip](https://physionet.org/content/mimic-iii-clinical-action/1.0.0/)。CLIP 标注行动片段与类别，不标注是否已完成或逾期；原文另受 MIMIC 协议限制。 |
| 报告阶段与效力 | 留空 | [fhir_workflow](https://hl7.org/fhir/R4/)。FHIR DiagnosticReport.status 是状态标准，未找到具有独立状态答案的开放临床报告集。 |
| 候选科室分流 | 留空 | [rd_triage](https://github.com/zhelishisongjie/RD-Triage)、[clinicalmc](https://github.com/hzyuezh/ClinicalMPD)、[medjourney](https://github.com/Medical-AI-Learning/MedJourney)、[chinese_medical_dialogue](https://github.com/Toyhom/Chinese-medical-dialogue-data)。RD-Triage 有多答案及多上游来源需分别核权；ClinicalMC/MedJourney 数据许可未闭合；中文问诊科室字段不等于最佳首诊科室。 |
| 患者消息紧急性比较 | 留空 | [pmr_bench](https://arxiv.org/abs/2601.13178)。PMR-Reddit 的原等级经 GPT-5 推导，并非逐对人工金标；本轮不纳入主评测。 |
| 脓毒症提前预警 | 100 题 | [sepsis2019](https://physionet.org/content/challenge-2019/1.0.0/)。采用 PhysioNet 2019 公开训练 A 的固定自留评测；还原 6 小时提前标签，固定 ICU 第 12 小时预测未来至第 24 小时的起病。 |
| 出院待办行动类别 | 留空 | [clip](https://physionet.org/content/mimic-iii-clinical-action/1.0.0/)。CLIP 任务匹配，但基于 MIMIC 文本，需要凭证和 DUA，不能公开复制原文。 |
| 治疗相关不良事件预测 | 留空 | [ct_ade](https://github.com/ds4dh/CT-ADE)。CT-ADE 的数据许可声明未解决 MedDRA SOC/PT 术语及底层材料全部再分发边界；本轮保留引用。 |
| 病历论断支持关系 | 留空 | [mednli](https://physionet.org/content/mednli/1.0.0/)、[nli4ct](https://github.com/ai-systems/nli4ct)。MedNLI 原病历受控；NLI4CT 是试验报告二分类且原仓库数据许可不明确，不能替代病历三分类。 |

## MEDDOCAN：隐私候选判断，100 题

[发布方仓库](https://github.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN) 与 [原论文](https://ceur-ws.org/Vol-2421/MEDDOCAN_overview.pdf) 说明语料基于公开病例报告构建，并补入隐私表达。许可为 CC-BY-4.0；材料属于经过加工的合成增强病例，不是原始患者身份数据。固定提交 `783a6df385c975b328c99bcffb54196a9ba4078a`，只使用 250 份官方测试文档的原 BRAT 标注。

目标单位统一为词，避免正例使用完整姓名、负例使用单词造成长度捷径。完全位于 PHI 标注内为 yes；与全部标注不重叠为 no，这是完整标注语料的闭世界 O 标签映射，不能证明原标注无漏标。跨标注边界或存在定位错误的候选排除。每份文档按固定哈希预选正负候选，再按来源组抽样；最终 100 份不同文档，正负各 50。此任务只覆盖给定词的隐私判断，不代表整份文档脱敏召回率。

## PhysioNet 2019：固定时点脓毒症预测，100 题

[发布页](https://physionet.org/content/challenge-2019/1.0.0/) 明确给出 CC-BY-4.0 和提前 6 小时的 `SepsisLabel` 定义。只采用公开训练医院 A，自留作本地评测，逐题标为 `upstream_train_reserved_for_local_evaluation`；不是官方隐藏测试，也不能视为训练过该库模型的盲测。

候选记录在读取结果之前确定：对医院 A 的 20,336 个文件名，计算 `SHA256("20261010:sepsis2019:setA:" + filename)`，取最小的 1,000 个。完整文件名框、选择清单及逐文件 SHA-256 已保存。下载使用发布页提供的公开 PhysioNet S3 桶；无需凭证。

固定协议：

1. 预测时点为 ICU 第 12 小时，只输入第 1–12 小时的 18 个生命体征、检验和人口学字段；缺失记为 null，不填补、不读取未来测量。
2. 仅保留从第 1 小时起连续记录的病例。原标签首次变为 1 的小时加 6，得到挑战定义推算的起病小时；首行已为 1 的起病时间左删失病例排除。
3. 排除第 12 小时及以前已起病者；目标为起病落在 `(12,24]` 小时。阳性须观察到推算起病时点，阴性须观察到第 24 小时。随访不足不能记作阴性。
4. 候选框中 528 例符合条件，含 11 个阳性、517 个阴性。按既有分层抽样规则得到 100 例：11 个阳性、89 个阴性；每个原记录最多一题。

该目标是由挑战定义推算的事件，不是独立医生重新审定的诊断，也不是是否应转 ICU 的行动标签。分数与原挑战的逐小时 utility 不可直接比较。样本经过随访与时间完整性筛选，且抽样改变了类别比例，不能估计临床患病率、风险校准或真实部署 PPV。恒答阴性即可得到 89% 准确率；应同时报告阳性召回和阴性召回。只有 11 个阳性时，对敏感度变化的解释尤其有限。

## LabQAR：参考区间条件匹配，72 题

数据取自作者论文链接的 [Figshare v1](https://doi.org/10.6084/m9.figshare.29189894)，明确为 CC-BY-4.0。采用 `Set_1.json` 的 550 条原始范围答案；原始 README、Figshare 许可元数据、文件 MD5 和 SHA-256 均保留。代码仓库的 MIT 与数据许可分别记录。

同一检验、单位、类别的原区间组成固定候选表；输入同时提供原参考条目的标本、人群与条件，要求选择适用于目标条件的区间。答案是原范围字符串的机械映射，没有生成新范围。任务衡量给定参考资料的条件匹配，不是医疗知识记忆，也不证明该范围适用于任意实验室。未覆盖原语料没有提供的方法差异和“不确定”金标。

26 条因问题条件无法可靠解析或答案不是明确区间/阈值而排除，21 条同条件答案冲突全部排除，418 条缺少不同的可用候选区间。剩余 85 条，经重复 CBC/独立检验条目归并、请求去重及每来源组最多 5 题限制，保留 72 题。未使用 `Set_2.json` 中构造检验数值的高/正常/低题来替代本任务。

## 原有不足 100 题的任务

| 任务 | 本轮后题数 | 补充情况 |
| --- | ---: | --- |
| 患者特异性禁忌判断 | 54 | 现有病例筛选保留；openFDA 只有规则，不能补成患者金标。MedMCQA 仍需逐题审核任务归属。 |
| 术后去向判断 | 68 | 原 UCI 小语料去重后有限；未核实可直接合并的新临床去向来源。 |
| 用药频次关联 | 81 | 现有 CT-EBM-SP 测试/开发标注保留；未纳入未经核验的新关系来源。 |
| 药物剂型关联 | 77 | 同上；未为补足数量扩大到上游训练标注。 |
| 护理优先行动 | 42 | 原病例题保留；尚未从其他考试数据完成可追溯的对应任务筛选。 |
| 补液方案选择 | 16 | 原病例题保留；不能用一般补液知识题代替病例方案选择。 |

上述是本轮未补齐的状态，不是“没有任何开源候选”的结论。[MedMCQA 原项目](https://github.com/medmcqa/medmcqa) 可作为后续病例审核候选，但科目字段本身不是这几项决策任务标签。

## 文件与验证

[机器可读核验记录](../benchmarks/medical_decision_v1/gap_audit.json) 保存 21 项任务的来源及结论；[来源登记](../benchmarks/medical_decision_v1/SOURCES.md) 保存采用与仅引用状态；[原版本身份索引](../benchmarks/medical_decision_v1/history/v0.4.0_sample_identity.json) 用于检查已发布题目没有被替换。

新增数据经逐题原文件/标注回查，以及时间边界、删失处理、词边界、条件冲突、答案隔离、旧版本完整记录保留等本地检查。尚未运行模型评测，也未进行本项目独立医生逐题复核。
