# 药物关系、用药变更与出院带药

**7 个任务条件，366 条主评测记录。** [全部场景](../../README.md)

关系任务给定实体；CDrugRed 为发布训练池按患者分离的留出样本，不是官方隐藏测试。

| 任务（点击查看完整方法与数据） | 类型 | 记录数 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [化学物致病关系判断](bc5cdr_relation_oracle_entities/README.md) | 数据适配 | 100 | Accuracy | 57.0% |
| [给定药物对相互作用分类](ddi_relation_oracle_pairs/README.md) | 数据适配 | 150 | Accuracy | 79.3% |
| [出院带药候选筛选](cdrugred_discharge_candidate_pipeline/README.md) | 数据适配 | 100 | micro-F1 | 48.6% |
| [边界挑战：过敏状态](challenge_allergy_state/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
| [边界挑战：药物剂量关联](challenge_dose_link/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
| [边界挑战：给药频次](challenge_frequency/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
| [边界挑战：用药变更](challenge_medication_change/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
