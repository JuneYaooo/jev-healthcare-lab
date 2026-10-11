# 任务说明目录

[返回首页](../../README.md) · [数据集目录](../datasets/README.md)

共 89 个任务定义，73 个有题任务。每页说明判断目标、来源、样例输入、标准答案与使用边界；空任务保留定义和缺口。

## 接诊与分诊

识别就诊诉求、资料缺口及处理优先级。

| 任务说明 | 能力维度 | 题数 |
| --- | --- | --- |
| [事实主体归属](experiencer.md) | 事实与状态 | 100 |
| [医疗问题意图](query_intent.md) | 分类与标准化 | 100 |
| [决策资料充分性](input_sufficiency.md) | 规则与数值 | 100 |
| [当前分诊与升级行动](triage_urgency.md) | 风险与升级 | 100 |
| [候选科室分流](department_routing.md) | 临床候选方案 | 0 |
| [患者消息紧急性比较](message_urgency_pair.md) | 风险与升级 | 30 |
| [孕产风险等级识别](maternal_risk.md) | 风险与升级 | 100 |

## 检查与检验

选择检查、关联结果并判断结果的适用性与处理需求。

| 任务说明 | 能力维度 | 题数 |
| --- | --- | --- |
| [检查检验数值关联](lab_link.md) | 关联与匹配、证据与一致性 | 100 |
| [标本身份与来源链](specimen_lineage.md) | 关联与匹配 | 0 |
| [数值与单位等价](unit_equivalence.md) | 规则与数值 | 0 |
| [参考区间适用性](reference_range.md) | 规则与数值 | 72 |
| [临床事件变化趋势](result_trend.md) | 事实与状态 | 100 |
| [危急结果与人工升级](critical_result_escalation.md) | 风险与升级 | 0 |
| [报告阶段与效力](report_stage.md) | 流程与下一步行动 | 0 |
| [检查方案选择](examination_choice.md) | 临床候选方案 | 100 |
| [检验数值高低判读](lab_value_classification.md) | 规则与数值 | 100 |
| [药物基因检测功能表型判定](pgx_function_phenotype.md) | 分类与标准化 | 84 |

## 诊断与鉴别

根据已有材料判断诊断、状态和临床分级。

| 任务说明 | 能力维度 | 题数 |
| --- | --- | --- |
| [否定与不确定状态](assertion_scope.md) | 事实与状态 | 100 |
| [事件与文档时间关系](temporality.md) | 事实与状态 | 100 |
| [诊断核实状态](diagnosis_verification.md) | 事实与状态 | 0 |
| [有界临床量表评分](bounded_score.md) | 规则与数值、证据与一致性 | 100 |
| [临床分级与分期选择](clinical_grade.md) | 规则与数值 | 100 |
| [模拟病例主诊断选择](synthetic_diagnosis.md) | 临床候选方案 | 100 |
| [临床病例候选诊断](diagnosis_choice.md) | 临床候选方案 | 100 |
| [中医证型选择](tcm_syndrome.md) | 临床候选方案 | 100 |
| [临床事件先后关系](event_temporal_order.md) | 关联与匹配 | 100 |
| [临床事件与解剖部位关联](anatomical_site_link.md) | 关联与匹配 | 100 |
| [严重程度与临床事件关联](severity_link.md) | 关联与匹配 | 100 |
| [事件与时间表达关联](event_date_link.md) | 关联与匹配 | 100 |
| [病例病因与原因判断](case_etiology.md) | 临床候选方案 | 100 |
| [中医病机候选核验](tcm_pathogenesis_candidate.md) | 分类与标准化 | 100 |

## 治疗与用药

判断治疗选择、用药关系及患者特异性适宜性。

| 任务说明 | 能力维度 | 题数 |
| --- | --- | --- |
| [用药状态与变更](medication_status.md) | 事实与状态 | 0 |
| [药物相互作用关系](drug_interaction.md) | 关联与匹配 | 100 |
| [药物与剂量关联](dose_link.md) | 关联与匹配、证据与一致性 | 100 |
| [患者特异性禁忌选择](patient_contraindication.md) | 资格与适宜性 | 54 |
| [剂量适宜性](dose_appropriateness.md) | 资格与适宜性 | 0 |
| [治疗方案选择](treatment_choice.md) | 临床候选方案 | 100 |
| [用药方案选择](medication_choice.md) | 临床候选方案 | 100 |
| [治疗相关不良事件预测](adverse_event_prediction.md) | 风险与升级 | 0 |
| [给药途径关联](route_link.md) | 关联与匹配 | 100 |
| [用药或操作频次关联](frequency_link.md) | 关联与匹配 | 81 |
| [药物剂型关联](drug_form_link.md) | 关联与匹配 | 77 |
| [补液方案选择](fluid_plan.md) | 规则与数值 | 16 |
| [药物基因结果用药建议匹配](pgx_guideline_recommendation.md) | 资格与适宜性 | 100 |
| [试验干预效果方向判定](trial_effect_direction.md) | 证据与一致性 | 100 |
| [处方审核处置选择](prescription_audit_action.md) | 分类与标准化 | 11 |
| [给药途径与方法选择](administration_route_choice.md) | 临床候选方案、流程与下一步行动 | 4 |

## 住院与护理

核对病情证据、操作执行和病情恶化风险。

| 任务说明 | 能力维度 | 题数 |
| --- | --- | --- |
| [患者与记录身份匹配](patient_identity.md) | 关联与匹配 | 0 |
| [长病历证据选择](long_record_evidence.md) | 证据与一致性 | 100 |
| [医疗操作进度](procedure_progress.md) | 流程与下一步行动 | 0 |
| [单次给药执行状态](administration_status.md) | 流程与下一步行动 | 0 |
| [脓毒症提前预警](deterioration_prediction.md) | 风险与升级 | 100 |
| [术后转归去向选择](postoperative_disposition.md) | 流程与下一步行动 | 68 |
| [子操作与所属操作关联](procedure_component_link.md) | 关联与匹配 | 100 |
| [临床事件持续性](event_permanence.md) | 事实与状态 | 100 |
| [病例并发症判断](case_complication.md) | 风险与升级 | 100 |
| [护理措施选择](nursing_priority.md) | 流程与下一步行动 | 42 |
| [病例营养方案选择](nutrition_plan.md) | 分类与标准化 | 11 |
| [护理体位选择](positioning_choice.md) | 分类与标准化 | 10 |
| [病情监测指标选择](monitoring_target.md) | 临床候选方案、流程与下一步行动 | 5 |
| [感染防控措施选择](infection_precaution.md) | 临床候选方案、流程与下一步行动 | 5 |

## 出院与随访

识别后续行动、完成状态和出院后的风险。

| 任务说明 | 能力维度 | 题数 |
| --- | --- | --- |
| [随访行动与完成状态](followup_action.md) | 流程与下一步行动 | 0 |
| [出院后 30 天内再入院预测](readmission_30d.md) | 风险与升级 | 100 |
| [出院待办行动类别](followup_item_type.md) | 分类与标准化 | 0 |
| [90 日死亡结局预测](mortality_90d.md) | 风险与升级 | 100 |
| [随访方案选择](followup_plan.md) | 临床候选方案、流程与下一步行动 | 6 |
| [康复训练方案选择](rehabilitation_choice.md) | 临床候选方案、流程与下一步行动 | 4 |
| [个体预防方案选择](prevention_choice.md) | 临床候选方案、流程与下一步行动 | 13 |
| [患者教育与沟通选择](patient_counseling.md) | 临床候选方案、流程与下一步行动 | 11 |

## 临床试验筛选

解释入排条件并判断患者转介资格。

| 任务说明 | 能力维度 | 题数 |
| --- | --- | --- |
| [患者与试验匹配](trial_referral.md) | 资格与适宜性、证据与一致性 | 100 |
| [入排条件要素分类](criterion_entity_type.md) | 资格与适宜性 | 100 |
| [入排条件限定关系](criterion_relation.md) | 资格与适宜性 | 100 |
| [入排条件与或关系](criterion_boolean.md) | 资格与适宜性、规则与数值 | 100 |
| [条件上界与下界](criterion_bound.md) | 资格与适宜性 | 100 |
| [病程与疗程时长关联](duration_link.md) | 关联与匹配 | 100 |
| [联合干预对象关联](combination_link.md) | 关联与匹配 | 100 |
| [干预用途关联](indication_link.md) | 关联与匹配 | 100 |

## 病历与医疗质量控制

识别文书类别、错误、隐私与证据不一致。

| 任务说明 | 能力维度 | 题数 |
| --- | --- | --- |
| [病历章节类别](note_section.md) | 分类与标准化 | 100 |
| [医学术语归一化](terminology.md) | 分类与标准化 | 0 |
| [医疗叙述错误检出](clinical_error_detection.md) | 证据与一致性、临床候选方案 | 100 |
| [医疗叙述错误定位](clinical_error_location.md) | 证据与一致性 | 100 |
| [研究论断证据关系](claim_support.md) | 证据与一致性 | 100 |
| [医疗材料隐私候选](privacy_candidate.md) | 风险与升级 | 100 |
| [病历论断支持关系](clinical_statement_support.md) | 证据与一致性 | 0 |
| [同一临床事件指代关联](event_coreference.md) | 关联与匹配 | 100 |
| [文本因果结果关联](cause_effect_link.md) | 关联与匹配 | 100 |
| [否定或推测线索作用对象](assertion_cue_target.md) | 关联与匹配 | 100 |
| [临床时间表达类别](clinical_time_type.md) | 分类与标准化 | 100 |
| [知情与隐私处置选择](consent_action.md) | 临床候选方案、流程与下一步行动 | 3 |
