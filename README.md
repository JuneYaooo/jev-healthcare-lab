# Jev Healthcare Lab

用于逐任务比较 **JEV 与其他模型的医疗决策准确率和完整运行耗时**。主评测围绕病例诊断、检查、治疗、用药、分诊、护理、随访与试验转介，要求从给定候选中作出选择；不包含自由生成任务。

**8 个医疗场景、7 个能力标签、29 个任务定义。** 其中 26 个任务有题，共 1,514 题（中文 1,080 题），采用 11 个数据来源。3 个任务待补；11 个不足 20 题的任务作为探索项，暂不进入汇总。已完成 5 个模型的同题评测。

[场景与任务](#场景与任务) · [任务说明与样例](docs/tasks/README.md) · [数据集说明与样例](docs/datasets/README.md) · [辅助任务](docs/tasks/AUXILIARY.md)

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

任务名称链接到说明页，包含任务定义、输入样例、选项与原答案；数据集名称链接到来源、引用与许可。来源后的数字为实际题数，† 表示非商业附加来源。“可参与汇总”只代表达到最低题量门槛，不表示已通过临床验证。 各模型列为 **任务准确率 / 平均完整决策耗时（秒）**，失败计错；空任务显示 —。点击任务名称查看分位耗时、任务总耗时、失败情况与原始记录。

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

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） | JEV 1.13 | DeepSeek V4.1 Flash | DeepSeek V4 Pro | Qwen3.5-9B | Qwen3.8-27B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [分诊与就医紧急程度判断](docs/tasks/triage_urgency.md) | 风险与升级 | 100 | 可参与汇总 | [CARE-Bench](docs/datasets/care_bench.md)†（100） | 63.00% / 0.971s | 61.00% / 0.511s | 57.00% / 1.003s | 50.00% / 1.075s | 65.00% / 2.201s |
| [首诊科室选择](docs/tasks/department_routing.md) | 临床候选方案 | 0 | 待补 | 待补数据 | — | — | — | — | — |
| [患者消息处理优先级](docs/tasks/message_urgency_pair.md) | 风险与升级 | 30 | 可参与汇总 | [PMR-Synth annotated pairs](docs/datasets/pmr_synth.md)†（30） | 63.33% / 0.906s | 50.00% / 0.496s | 63.33% / 1.306s | 63.33% / 1.020s | 50.00% / 2.728s |

### 检查与检验

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） | JEV 1.13 | DeepSeek V4.1 Flash | DeepSeek V4 Pro | Qwen3.5-9B | Qwen3.8-27B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [危急检验结果处置选择](docs/tasks/critical_result_escalation.md) | 风险与升级 | 0 | 待补 | 待补数据 | — | — | — | — | — |
| [检查方案选择](docs/tasks/examination_choice.md) | 临床候选方案 | 100 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（19）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（81） | 88.00% / 0.954s | 81.00% / 0.479s | 74.00% / 0.954s | 60.00% / 1.188s | 74.00% / 2.366s |

### 诊断与鉴别

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） | JEV 1.13 | DeepSeek V4.1 Flash | DeepSeek V4 Pro | Qwen3.5-9B | Qwen3.8-27B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [疾病分期与严重程度判断](docs/tasks/clinical_grade.md) | 规则与数值 | 100 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（70）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（30） | 62.00% / 1.336s | 50.00% / 0.470s | 53.00% / 0.949s | 34.00% / 1.469s | 43.00% / 2.685s |
| [病例诊断选择](docs/tasks/diagnosis.md) | 临床候选方案 | 200 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（50）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（50）；[DDXPlus](docs/datasets/ddxplus.md)（100） | 79.50% / 1.047s | 84.00% / 0.586s | 81.00% / 0.994s | 66.00% / 1.283s | 77.00% / 3.025s |
| [中医证型判断](docs/tasks/tcm_syndrome.md) | 临床候选方案 | 100 | 可参与汇总 | [TCM-SD](docs/datasets/tcm_sd.md)†（100） | 38.00% / 3.838s | 37.00% / 0.546s | 30.00% / 1.162s | 29.00% / 1.143s | 31.00% / 4.763s |
| [病例病因判断](docs/tasks/case_etiology.md) | 临床候选方案 | 100 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（50）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（50） | 84.00% / 3.744s | 84.00% / 0.478s | 84.00% / 1.012s | 66.00% / 1.585s | 81.00% / 1.808s |
| [中医候选病机判断](docs/tasks/tcm_pathogenesis_candidate.md) | 分类与标准化 | 100 | 可参与汇总 | [TCMEval-SDT](docs/datasets/tcmeval_sdt.md)（100） | 67.00% / 1.666s | 76.00% / 0.430s | 79.00% / 1.101s | 70.00% / 1.012s | 75.00% / 3.760s |

### 治疗与用药

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） | JEV 1.13 | DeepSeek V4.1 Flash | DeepSeek V4 Pro | Qwen3.5-9B | Qwen3.8-27B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [患者方案禁忌判断](docs/tasks/patient_contraindication.md) | 资格与适宜性 | 54 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（33）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（21） | 79.63% / 1.009s | 74.07% / 0.487s | 66.67% / 0.951s | 46.30% / 0.729s | 64.81% / 1.701s |
| [患者剂量适宜性判断](docs/tasks/dose_appropriateness.md) | 资格与适宜性 | 0 | 待补 | 待补数据 | — | — | — | — | — |
| [治疗方案选择](docs/tasks/treatment_choice.md) | 临床候选方案 | 100 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（46）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（54） | 78.00% / 0.923s | 82.00% / 0.454s | 74.00% / 0.946s | 51.00% / 0.861s | 72.00% / 2.486s |
| [用药方案选择](docs/tasks/medication_choice.md) | 临床候选方案 | 100 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（12）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（88） | 83.00% / 0.960s | 80.00% / 0.519s | 72.00% / 0.978s | 47.00% / 1.217s | 73.00% / 1.595s |
| [补液方案选择](docs/tasks/fluid_plan.md) | 规则与数值 | 16 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（9）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（7） | 50.00% / 0.980s | 56.25% / 0.589s | 50.00% / 0.910s | 18.75% / 2.595s | 31.25% / 1.992s |
| [药物基因结果对应的指南建议选择](docs/tasks/pgx_guideline_recommendation.md) | 资格与适宜性 | 100 | 可参与汇总 | [CPIC curated pharmacogenomic tables](docs/datasets/cpic.md)（100） | 55.00% / 0.993s | 54.00% / 0.492s | 51.00% / 1.084s | 39.00% / 0.865s | 54.00% / 3.176s |
| [给药途径与实施方法选择](docs/tasks/administration_route_choice.md) | 临床候选方案、流程与下一步行动 | 4 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（3）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（1） | 75.00% / 0.946s | 75.00% / 0.576s | 75.00% / 0.883s | 50.00% / 1.762s | 50.00% / 1.334s |

### 住院与护理

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） | JEV 1.13 | DeepSeek V4.1 Flash | DeepSeek V4 Pro | Qwen3.5-9B | Qwen3.8-27B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [病例并发症判断](docs/tasks/case_complication.md) | 风险与升级 | 100 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（64）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（36） | 93.00% / 1.018s | 89.00% / 0.439s | 89.00% / 0.960s | 70.00% / 1.173s | 84.00% / 2.439s |
| [护理措施选择](docs/tasks/nursing_priority.md) | 流程与下一步行动 | 42 | 可参与汇总 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（42） | 85.71% / 0.918s | 73.81% / 0.452s | 80.95% / 0.966s | 71.43% / 0.869s | 83.33% / 7.995s |
| [营养与饮食方案选择](docs/tasks/nutrition_plan.md) | 分类与标准化 | 11 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（10）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（1） | 72.73% / 0.848s | 72.73% / 0.445s | 72.73% / 1.165s | 45.45% / 1.335s | 45.45% / 1.470s |
| [护理与操作体位选择](docs/tasks/positioning_choice.md) | 分类与标准化 | 10 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（8）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（2） | 90.00% / 0.985s | 80.00% / 0.474s | 90.00% / 0.740s | 60.00% / 0.967s | 70.00% / 1.409s |
| [病情监测与疗效判断](docs/tasks/monitoring_target.md) | 临床候选方案、流程与下一步行动 | 5 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（5） | 80.00% / 0.843s | 100.00% / 0.433s | 80.00% / 1.363s | 60.00% / 0.716s | 60.00% / 4.005s |
| [感染防控措施选择](docs/tasks/infection_precaution.md) | 临床候选方案、流程与下一步行动 | 5 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（4）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（1） | 100.00% / 0.990s | 100.00% / 0.465s | 100.00% / 0.945s | 100.00% / 1.124s | 100.00% / 1.498s |

### 出院与随访

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） | JEV 1.13 | DeepSeek V4.1 Flash | DeepSeek V4 Pro | Qwen3.5-9B | Qwen3.8-27B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [复查项目与随访时机选择](docs/tasks/followup_plan.md) | 临床候选方案、流程与下一步行动 | 6 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（3）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（2）；[MedMCQA](docs/datasets/medmcqa.md)（1） | 83.33% / 0.989s | 66.67% / 0.468s | 83.33% / 0.983s | 50.00% / 0.709s | 83.33% / 5.576s |
| [康复训练方案选择](docs/tasks/rehabilitation_choice.md) | 临床候选方案、流程与下一步行动 | 4 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（4） | 100.00% / 0.860s | 50.00% / 0.503s | 75.00% / 0.963s | 75.00% / 0.630s | 50.00% / 1.835s |
| [预防措施选择](docs/tasks/prevention_choice.md) | 临床候选方案、流程与下一步行动 | 13 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（10）；[CNMLEQA-10k（中文案例分析子集）](docs/datasets/cnmleqa.md)（2）；[MedMCQA](docs/datasets/medmcqa.md)（1） | 84.62% / 0.898s | 84.62% / 0.432s | 84.62% / 0.881s | 76.92% / 0.720s | 92.31% / 1.407s |
| [健康教育与沟通行动选择](docs/tasks/patient_counseling.md) | 临床候选方案、流程与下一步行动 | 11 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（11） | 100.00% / 1.140s | 90.91% / 0.423s | 90.91% / 3.157s | 100.00% / 1.043s | 90.91% / 1.674s |

### 临床试验筛选

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） | JEV 1.13 | DeepSeek V4.1 Flash | DeepSeek V4 Pro | Qwen3.5-9B | Qwen3.8-27B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [患者临床试验初筛与转介判断](docs/tasks/trial_referral.md) | 资格与适宜性、证据与一致性 | 100 | 可参与汇总 | [TrialGPT SIGIR](docs/datasets/trialgpt.md)（100） | 53.00% / 1.046s | 60.00% / 0.698s | 58.00% / 1.282s | 50.00% / 3.040s | 58.00% / 2.092s |

### 病历与医疗质量控制

| 任务 | 能力维度 | 题数 | 状态 | 数据集来源（题数） | JEV 1.13 | DeepSeek V4.1 Flash | DeepSeek V4 Pro | Qwen3.5-9B | Qwen3.8-27B |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [知情同意与隐私处置选择](docs/tasks/consent_action.md) | 临床候选方案、流程与下一步行动 | 3 | 探索性 | [CMB-Exam（中文病例单选子集）](docs/datasets/cmb.md)（1）；[PrinciplismQA](docs/datasets/principlismqa.md)（2） | 100.00% / 0.906s | 100.00% / 0.350s | 100.00% / 0.967s | 100.00% / 0.606s | 100.00% / 5.022s |

## 模型得分与耗时对比

每个模型使用相同题目、候选项和许可范围，分别报告逐任务准确率、完整决策耗时（均值、P50、P95）、任务总耗时及失败率。多阶段调用、工具与重试计入完整决策耗时，运行配置随结果保存。

病例诊断的两个来源子集合并为一个任务。汇总先对场景内达到 20 题的任务等权，再对有分数场景等权；不足 20 题仅给探索结果，空任务不计零分。题量门槛按本次所选许可范围计算。固定语义分类额外报告 F1、召回、混淆矩阵与多数类基线；A/B/C 等随题变化的选项不报告临床类别 F1。

详细口径见 [评测方法](docs/EVALUATION.md)。

| 模型 | 临床主分数 | 平均完整耗时（秒） | P95（秒） | 有效回答 / 题数 |
| --- | --- | --- | --- | --- |
| JEV 1.13 | 72.26% | 1.426 | 4.092 | 1514 / 1514 |
| DeepSeek V4.1 Flash | 69.44% | 0.509 | 0.759 | 1505 / 1514 |
| DeepSeek V4 Pro | 68.08% | 1.045 | 1.522 | 1514 / 1514 |
| Qwen3.5-9B | 56.03% | 1.280 | 4.098 | 1493 / 1514 |
| Qwen3.8-27B | 66.75% | 2.800 | 6.496 | 1513 / 1514 |

生成式对照模型均关闭思考；每模型并发 8。主分数为场景等权汇总，不是全部题目的简单准确率。耗时为实际 API 调用的客户端时间，包含网络和重试；不同服务商和运行时段分别记录。

[全部逐任务得分与耗时](docs/MODEL_RESULTS.md) · [原始响应与运行配置](results/clinical-20261012/README.md)

## 许可

代码采用 [MIT](LICENSE)。第三方数据保留原许可，代码许可不覆盖题目材料；见 [第三方声明](THIRD_PARTY_NOTICES.md) 和包内 LICENSE-DATA.md。
