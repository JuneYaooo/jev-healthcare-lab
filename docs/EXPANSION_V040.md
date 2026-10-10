# v0.4.0：来源扩展与评测协议

本版本共 52 个有题任务、4,938 题：46 个任务达到 100 题，6 个任务不足 100 题；另 21 个任务保留为空。中文 1,012 题。原 v0.3.0 的 2,200 条完整记录保持不变。

新增 2,738 题、30 个有题任务。任务按决策目标区分，不按语种、疾病科别或来源副本重复计数。材料判断、临床方案选择、分诊行动与观察结局预测分别标记 decision_stage。

## 本次采用的来源

| 来源 | 本次用途 | 材料与许可 |
| --- | --- | --- |
| [CT-EBM-SP v3](https://github.com/lcampillos/ct-ebm-sp-v3) | 主体角色、给药途径/频次/剂型、时长、因果、联合干预、用途和线索作用对象 | 试验注册文本与摘要的人工标注；CC-BY-NC-SA-4.0 |
| [E3C](https://github.com/hltfbk/E3C-Corpus) | 事件时间属性、时间表达类别、持续性、时间与事件关联 | 英文 Layer 1 人工测试标注；发布方声明 CC-BY-NC，未指定版本；保留逐文献署名和原许可 |
| [CARE-Bench](https://github.com/ningkko/CARE-bench) | 当前轮次分诊与升级行动 | 来源约束的重构对话，模型辅助后人工审核；CC-BY-NC-4.0 |
| [UCI Diabetes 130-US Hospitals](https://doi.org/10.24432/C5230J) | 30 日内再入院 | 1999—2008 年糖尿病住院记录；CC-BY-4.0 |
| [UCI Heart Failure](https://doi.org/10.24432/C5Z89R) | 90 日死亡 | 心衰随访结构化记录；CC-BY-4.0 |
| [UCI Post-Operative Patient](https://doi.org/10.24432/C5DG6Q) | 术后去向 | 90 条历史记录，重复及冲突筛查后保留实际数量；CC-BY-4.0 |
| [UCI Maternal Health Risk](https://doi.org/10.24432/C5DP5D) | 孕产风险等级 | 沿用发布风险分级，不冒称真实母婴结局；CC-BY-4.0 |
| [MACCROBAT](https://doi.org/10.6084/m9.figshare.9764942) | 趋势、事件顺序、同一事件指代、解剖部位、严重程度、子操作等关联 | 使用已锁定原病例与人工标注，扩展原有来源 |
| [CMB](https://github.com/FreedomIntelligence/CMB)、[CNMLEQA](https://doi.org/10.5281/zenodo.18951465) | 病例分期、禁忌、原因、并发症、护理、补液 | 病例式考试单选；分别沿用 Apache-2.0 与 CC-BY-4.0 |

另外核验了 [MTCMB](https://github.com/Wayyuanyuan/MTCMB)：其开放生成、处方生成和文书抽取部分不纳入本集；考试题与既有任务同型，仍需核对上游材料条件。没有把其 12 个子集直接计作 12 个新决策任务。

## 新增任务与实际题数

| 场景 | 任务 | 题数 | 逐题来源统计 |
| --- | --- | ---: | --- |
| intake | [事实主体归属](../benchmarks/medical_decision_v1/tasks/experiencer/task.json) | 100 | ct_ebm_sp: 100 |
| diagnosis | [事件与文档时间关系](../benchmarks/medical_decision_v1/tasks/temporality/task.json) | 100 | e3c: 100 |
| diagnosis | [临床分级与分期选择](../benchmarks/medical_decision_v1/tasks/clinical_grade/task.json) | 100 | cmb: 70, cnmleqa: 30 |
| testing | [临床事件变化趋势](../benchmarks/medical_decision_v1/tasks/result_trend/task.json) | 100 | maccrobat: 100 |
| treatment | [患者特异性禁忌选择](../benchmarks/medical_decision_v1/tasks/patient_contraindication/task.json) | 54 | cnmleqa: 21, cmb: 33 |
| intake | [当前分诊与升级行动](../benchmarks/medical_decision_v1/tasks/triage_urgency/task.json) | 100 | care_bench: 100 |
| followup | [出院后 30 天内再入院预测](../benchmarks/medical_decision_v1/tasks/readmission_30d/task.json) | 100 | uci_diabetes: 100 |
| followup | [90 日死亡结局预测](../benchmarks/medical_decision_v1/tasks/mortality_90d/task.json) | 100 | uci_heart_failure: 100 |
| inpatient | [术后转归去向选择](../benchmarks/medical_decision_v1/tasks/postoperative_disposition/task.json) | 68 | uci_postoperative: 68 |
| intake | [孕产风险等级识别](../benchmarks/medical_decision_v1/tasks/maternal_risk/task.json) | 100 | uci_maternal: 100 |
| diagnosis | [临床事件先后关系](../benchmarks/medical_decision_v1/tasks/event_temporal_order/task.json) | 100 | maccrobat: 100 |
| quality | [同一临床事件指代关联](../benchmarks/medical_decision_v1/tasks/event_coreference/task.json) | 100 | maccrobat: 100 |
| diagnosis | [临床事件与解剖部位关联](../benchmarks/medical_decision_v1/tasks/anatomical_site_link/task.json) | 100 | maccrobat: 100 |
| diagnosis | [严重程度与临床事件关联](../benchmarks/medical_decision_v1/tasks/severity_link/task.json) | 100 | maccrobat: 100 |
| treatment | [给药途径关联](../benchmarks/medical_decision_v1/tasks/route_link/task.json) | 100 | ct_ebm_sp: 100 |
| treatment | [用药或操作频次关联](../benchmarks/medical_decision_v1/tasks/frequency_link/task.json) | 81 | ct_ebm_sp: 81 |
| trials | [病程与疗程时长关联](../benchmarks/medical_decision_v1/tasks/duration_link/task.json) | 100 | ct_ebm_sp: 100 |
| treatment | [药物剂型关联](../benchmarks/medical_decision_v1/tasks/drug_form_link/task.json) | 77 | ct_ebm_sp: 77 |
| quality | [文本因果结果关联](../benchmarks/medical_decision_v1/tasks/cause_effect_link/task.json) | 100 | ct_ebm_sp: 100 |
| trials | [联合干预对象关联](../benchmarks/medical_decision_v1/tasks/combination_link/task.json) | 100 | ct_ebm_sp: 100 |
| trials | [干预用途关联](../benchmarks/medical_decision_v1/tasks/indication_link/task.json) | 100 | ct_ebm_sp: 100 |
| quality | [否定或推测线索作用对象](../benchmarks/medical_decision_v1/tasks/assertion_cue_target/task.json) | 100 | ct_ebm_sp: 100 |
| diagnosis | [事件与时间表达关联](../benchmarks/medical_decision_v1/tasks/event_date_link/task.json) | 100 | e3c: 85, maccrobat: 15 |
| inpatient | [子操作与所属操作关联](../benchmarks/medical_decision_v1/tasks/procedure_component_link/task.json) | 100 | maccrobat: 100 |
| inpatient | [临床事件持续性](../benchmarks/medical_decision_v1/tasks/event_permanence/task.json) | 100 | e3c: 100 |
| quality | [临床时间表达类别](../benchmarks/medical_decision_v1/tasks/clinical_time_type/task.json) | 100 | e3c: 100 |
| diagnosis | [病例病因与原因判断](../benchmarks/medical_decision_v1/tasks/case_etiology/task.json) | 100 | cnmleqa: 50, cmb: 50 |
| inpatient | [病例并发症判断](../benchmarks/medical_decision_v1/tasks/case_complication/task.json) | 100 | cnmleqa: 36, cmb: 64 |
| inpatient | [护理措施选择](../benchmarks/medical_decision_v1/tasks/nursing_priority/task.json) | 42 | cmb: 42 |
| treatment | [补液方案选择](../benchmarks/medical_decision_v1/tasks/fluid_plan/task.json) | 16 | cmb: 9, cnmleqa: 7 |

不足 100 题的任务作为探索性覆盖；目标数和实际数均公开，不通过重复、改写或扩大标签含义补齐。评分输出的 sample_completeness 分层区分完整与不足量任务。

## 适配协议

### 中文病例题

只收带病例信息且明确询问对应决策的原单选题，保留原题和 4/5 个选项。排除缺图、明显截断、题意不符及不适用的反向提问；病因题不会仅因题干提到病因就收录。仅禁忌任务允许其定义所需的否定问法。新题按去空白/标点后的题干及全部选项去重，答案文本冲突则全部排除。相似题改写仍可能残留，group_id 是近似病例前缀分组。

CMB 使用原测试答案 ID 连接，并核对考试元数据；另使用验证和训练文件，253 道选中题来自上游训练划分，明确标记 upstream_train_reserved_for_local_evaluation。CNMLEQA 没有官方测试划分。它们是本项目冻结自留题，不是对已接触题库的模型提供全新盲测。评分按 upstream_split 分层。

### 文本属性与关联

CT-EBM-SP 主要使用 brat/test；频次与剂型关联另补 brat/dev，逐题保留划分。只把明确标注且可唯一解析的目标作答案，候选取原文中所有预先规定类型的有效实体，不把未标注关系当负例，不依据正确答案生成干扰项。未发布 UMLS 词表。

E3C 仅使用官方英文 Layer 1 测试文档，排除训练名单；UIMA 的 UTF-16 偏移转为 Python 字符位置，原 XML ID 和偏移均保留。FINITE/PERMANENT 是原语料事件属性，不能解释为新的临床慢病诊断。MACCROBAT 使用原关系及属性，不把“增加/减少”当成未来预测。

### 分诊与未来结局

CARE-Bench 只用 public_test_1；输入为截至该轮的患者披露消息。原参考答复、后续轮次、信息充分性标签及构造元数据均不作为输入。同病例多轮共享 group_id。四类输出包括询问澄清、自护监测、非紧急就医和紧急就医；不是 ESI 五级急诊分诊。

UCI 再入院只收原出院去向为回家（代码 1）的记录，并按 patient_nbr 仅取原文件中首个合格住院；输入删除 ID 和 readmitted，编码按原字典解释。标签 <30 为阳性，其他为未观察到 30 日内再入院；不能据此断言患者没有在库外医院再次入院。

UCI 心衰以基线为预测时点：time≤90 且 DEATH_EVENT=1 为阳性；观察至少 90 天且此前未死亡为阴性；90 天前删失的未死亡者排除。time 不作为输入。两个结局任务采用自然分布哈希抽样，不做正负平衡；100 题的患病率波动和阳性样本数须同时报告。

术后去向和孕产风险沿用原分类标签；完全相同输入的冲突标签全部排除。这两个来源没有患者 ID，不能宣称患者级独立划分。孕产 RiskLevel 是发布方风险等级，不是可替代临床终点的实际结局。结构化输入附原字段解释和单位，原数据的年代、字段与单位质量限制仍保留。

## 使用与边界

开放核心包 3,395 题、37 个有题任务，非商业附加包 1,543 题、16 个有题任务。两包题目不重叠，但事件与时间表达关联任务在两包都有题，因此去重后共 52 个任务。两个包均提供逐题定位、固定版本和 SHA-256，保留来源声明。临床方案、材料判断和结局预测应分别报告；不同版本或不同许可范围的总分不直接比较。

关系选择任务中的 T/E/XML ID 只是该文档内的候选键，跨病例不代表同一个医学类别，因此优先看准确率和分组全对率，不能把这类候选 ID 的宏 F1 解读为临床类别宏 F1。

答案沿用原始标注，本项目未进行独立医生逐题复核。原语料标注、考试版本、重构对话和风险标签都可能存在错误或适用性限制。任务数量表示已构建的可计分目标数量，不代表独立病例数量，也不代表已经覆盖完整临床工作流。

[全部来源](../benchmarks/medical_decision_v1/SOURCES.md) · [任务目录](../benchmarks/medical_decision_v1/README.md) · [评分方法](EVALUATION.md) · [数据包](../releases/README.md)
