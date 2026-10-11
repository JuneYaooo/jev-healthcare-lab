# Jev Healthcare Lab

用于逐任务比较 **JEV 与其他模型的医疗决策准确率和完整运行耗时**。主评测围绕病例诊断、检查、治疗、用药、分诊、护理、随访与试验转介，要求从给定候选中作出选择；不包含自由生成任务。

**8 个医疗场景、7 个能力标签、29 个任务定义。** 其中 26 个任务有题，共 1,514 题（中文 1,080 题），采用 11 个数据来源。3 个任务待补；11 个不足 20 题的任务作为探索项，暂不进入汇总。当前尚无模型对比成绩。

[场景与任务](#场景与任务) · [任务说明与样例](docs/tasks/README.md) · [数据集说明与样例](docs/datasets/README.md) · [辅助任务](docs/tasks/AUXILIARY.md) · [下载与使用](#下载与使用)

## 能力维度

场景表示医疗流程环节；能力标签描述判断方式，可以重叠。任务是逐项比较的单位，数据来源或语言子集不重复算作独立任务。

| 能力维度 | 关联任务数（含待补） |
| --- | --- |
| 分类与标准化 | 3 |
| 临床候选方案 | 15 |
| 资格与适宜性 | 4 |
| 证据与一致性 | 1 |
| 风险与升级 | 4 |
| 规则与数值 | 2 |
| 流程与下一步行动 | 9 |

## 场景与任务

任务名称链接到说明页，包含任务定义、输入样例、选项与原答案；数据集名称链接到来源、引用与许可。来源后的数字为实际题数，† 表示非商业附加来源。“可参与汇总”只代表达到最低题量门槛，不表示已通过临床验证。

| 医疗场景 | 有题任务 / 定义任务 | 题数 |
| --- | --- | --- |
| 接诊与分诊 | 2 / 3 | 130 |
| 检查与检验 | 1 / 2 | 100 |
| 诊断与鉴别 | 5 / 5 | 600 |
| 治疗与用药 | 6 / 7 | 374 |
| 住院与护理 | 6 / 6 | 173 |
| 出院与随访 | 4 / 4 | 34 |
| 临床试验筛选 | 1 / 1 | 100 |
| 病历与医疗质量控制 | 1 / 1 | 3 |

### 接诊与分诊

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） |
| --- | --- | --- | --- | --- |
| [分诊与就医紧急程度判断](docs/tasks/triage_urgency.md) | 风险与升级 | 100 | 可参与汇总 | [CARE-Bench](docs/datasets/care_bench.md)†（100） |
| [首诊科室选择](docs/tasks/department_routing.md) | 临床候选方案 | 0 | 待补 | 待补数据 |
| [患者消息处理优先级](docs/tasks/message_urgency_pair.md) | 风险与升级 | 30 | 可参与汇总 | [PMR-Synth annotated pairs](docs/datasets/pmr_synth.md)†（30） |

### 检查与检验

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） |
| --- | --- | --- | --- | --- |
| [危急检验结果处置选择](docs/tasks/critical_result_escalation.md) | 风险与升级 | 0 | 待补 | 待补数据 |
| [检查方案选择](docs/tasks/examination_choice.md) | 临床候选方案 | 100 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（19）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（81） |

### 诊断与鉴别

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） |
| --- | --- | --- | --- | --- |
| [疾病分期与严重程度判断](docs/tasks/clinical_grade.md) | 规则与数值 | 100 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（70）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（30） |
| [病例诊断选择](docs/tasks/diagnosis.md) | 临床候选方案 | 200 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（50）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（50）；[DDXPlus](docs/datasets/ddxplus.md)（100） |
| [中医证型判断](docs/tasks/tcm_syndrome.md) | 临床候选方案 | 100 | 可参与汇总 | [TCM-SD](docs/datasets/tcm_sd.md)†（100） |
| [病例病因判断](docs/tasks/case_etiology.md) | 临床候选方案 | 100 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（50）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（50） |
| [中医候选病机判断](docs/tasks/tcm_pathogenesis_candidate.md) | 分类与标准化 | 100 | 可参与汇总 | [TCMEval-SDT](docs/datasets/tcmeval_sdt.md)（100） |

### 治疗与用药

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） |
| --- | --- | --- | --- | --- |
| [患者方案禁忌判断](docs/tasks/patient_contraindication.md) | 资格与适宜性 | 54 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（33）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（21） |
| [患者剂量适宜性判断](docs/tasks/dose_appropriateness.md) | 资格与适宜性 | 0 | 待补 | 待补数据 |
| [治疗方案选择](docs/tasks/treatment_choice.md) | 临床候选方案 | 100 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（46）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（54） |
| [用药方案选择](docs/tasks/medication_choice.md) | 临床候选方案 | 100 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（12）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（88） |
| [补液方案选择](docs/tasks/fluid_plan.md) | 规则与数值 | 16 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（9）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（7） |
| [药物基因结果对应的指南建议选择](docs/tasks/pgx_guideline_recommendation.md) | 资格与适宜性 | 100 | 可参与汇总 | [CPIC curated pharmacogenomic tables](docs/datasets/cpic.md)（100） |
| [给药途径与实施方法选择](docs/tasks/administration_route_choice.md) | 临床候选方案、流程与下一步行动 | 4 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（3）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（1） |

### 住院与护理

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） |
| --- | --- | --- | --- | --- |
| [病例并发症判断](docs/tasks/case_complication.md) | 风险与升级 | 100 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（64）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（36） |
| [护理措施选择](docs/tasks/nursing_priority.md) | 流程与下一步行动 | 42 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（42） |
| [营养与饮食方案选择](docs/tasks/nutrition_plan.md) | 分类与标准化 | 11 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（10）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（1） |
| [护理与操作体位选择](docs/tasks/positioning_choice.md) | 分类与标准化 | 10 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（8）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（2） |
| [病情监测与疗效判断](docs/tasks/monitoring_target.md) | 临床候选方案、流程与下一步行动 | 5 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（5） |
| [感染防控措施选择](docs/tasks/infection_precaution.md) | 临床候选方案、流程与下一步行动 | 5 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（4）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（1） |

### 出院与随访

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） |
| --- | --- | --- | --- | --- |
| [复查项目与随访时机选择](docs/tasks/followup_plan.md) | 临床候选方案、流程与下一步行动 | 6 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（3）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（2）；[MedMCQA](docs/datasets/medmcqa.md)（1） |
| [康复训练方案选择](docs/tasks/rehabilitation_choice.md) | 临床候选方案、流程与下一步行动 | 4 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（4） |
| [预防措施选择](docs/tasks/prevention_choice.md) | 临床候选方案、流程与下一步行动 | 13 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（10）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（2）；[MedMCQA](docs/datasets/medmcqa.md)（1） |
| [健康教育与沟通行动选择](docs/tasks/patient_counseling.md) | 临床候选方案、流程与下一步行动 | 11 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（11） |

### 临床试验筛选

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） |
| --- | --- | --- | --- | --- |
| [患者临床试验初筛与转介判断](docs/tasks/trial_referral.md) | 资格与适宜性、证据与一致性 | 100 | 可参与汇总 | [TrialGPT SIGIR](docs/datasets/trialgpt.md)（100） |

### 病历与医疗质量控制

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） |
| --- | --- | --- | --- | --- |
| [知情同意与隐私处置选择](docs/tasks/consent_action.md) | 临床候选方案、流程与下一步行动 | 3 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（1）；[PrinciplismQA](docs/datasets/principlismqa.md)（2） |

## 模型得分与耗时对比

每个模型使用相同题目、候选项和许可范围，分别报告逐任务准确率、完整决策耗时（均值、P50、P95）、任务总耗时及失败率。多阶段调用、工具与重试计入完整决策耗时，运行配置随结果保存。

病例诊断的两个来源子集合并为一个任务。汇总先对场景内达到 20 题的任务等权，再对有分数场景等权；不足 20 题仅给探索结果，空任务不计零分。题量门槛按本次所选许可范围计算。固定语义分类额外报告 F1、召回、混淆矩阵与多数类基线；A/B/C 等随题变化的选项不报告临床类别 F1。

**现有工具支持离线质量评分，尚未实现模型调用和耗时采集。** 详细口径见 [评测方法](docs/EVALUATION.md)。

## 下载与使用

| 数据包 | 题数 | 使用范围 |
| --- | --- | --- |
| [临床主评测 · 开放许可](releases/jev-medical-decision-clinical-open.zip) | 1284 | 遵守各来源署名、相同方式共享等条款 |
| [临床主评测 · 非商业附加](releases/jev-medical-decision-clinical-research-noncommercial.zip) | 230 | 保留非商业等限制；与开放部分分开报告 |

[辅助数据包与全部校验和](releases/README.md)。解压后进入包目录执行（Python 3.10+，仅标准库）：

```bash
python3 tools/medical_decision_release.py verify --dataset .
python3 tools/medical_decision_release.py score --dataset . --predictions predictions.jsonl --output scores.json
```

读取包内 requests.jsonl，只把 request 发给模型。预测文件每行一条，以下使用一个实际题号演示，choice 应填模型返回的选项键：

```json
{"id": "medication_choice:cmb:484", "choice": "模型返回的选项键"}
```

scores.json 的 task_families 保存合并后的逐任务结果，tasks 保留来源子集结果。逐题耗时记录通过题目编号关联。仓库内导出默认同样只选择临床主评测的开放许可部分：

```bash
python3 scripts/medical_decision_dataset.py export --output work/clinical-requests.jsonl
python3 scripts/medical_decision_dataset.py score --predictions work/predictions.jsonl --output work/clinical-scores.json
```

## 数据来源与评测边界

每题保留原始资源地址、固定快照、文件哈希、原记录位置及答案映射。材料包含考试病例、模拟病例、重构咨询和指南规则，各来源说明页标明性质与许可；尚未经过本项目独立医生逐题审核。

辅助计算、风险预测、流程核对和文本标注放在 [辅助目录](docs/tasks/AUXILIARY.md)，须显式指定 --scope auxiliary，不能混入临床主分数。“目标患者回答证据是否出现”因姓名捷径暂停使用，不导出、不评分、不打包。

[任务范围调整依据](docs/TASK_SCOPE_REVIEW.md) · [来源登记](docs/datasets/README.md) · [使用与复建](docs/REPRODUCING.md)

训练对比需要检查上游训练划分、模型暴露和共享病例，并冻结相同子集。公开试题和小样本结果不能作为未暴露盲测或临床有效性证明。

## 许可

代码采用 [MIT](LICENSE)。第三方数据保留原许可，代码许可不覆盖题目材料；见 [第三方声明](THIRD_PARTY_NOTICES.md) 和包内 LICENSE-DATA.md。
