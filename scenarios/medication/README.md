# 药物关系、用药变更与出院带药

**7 个任务条件，430 条主评测记录。** [全部场景](../../README.md)

关系任务给定实体；CDrugRed 为发布训练池按患者分离的留出样本，不是官方隐藏测试。

| 任务（点击查看方法与费用） | 任务类型 | 记录数 | 指标 | Jev | DeepSeek |
| --- | --- | ---: | --- | ---: | ---: |
| [化学物致病关系判断](bc5cdr_relation_oracle_entities/README.md) | 关系分类 | 100 | Accuracy | 57.0% | 66.0% |
| [给定药物对相互作用分类](ddi_relation_oracle_pairs/README.md) | 关系分类 | 150 | Accuracy | 79.3% | 74.7% |
| [出院带药候选筛选](cdrugred_discharge_candidate_pipeline/README.md) | 多标签候选筛选 | 100 | micro-F1 | 48.6% | 47.9% |
| [边界挑战：过敏状态](challenge_allergy_state/README.md) | 过敏状态判断 | 20 | Accuracy | 100.0% | 100.0% |
| [边界挑战：药物剂量关联](challenge_dose_link/README.md) | 剂量关联判断 | 20 | Accuracy | 100.0% | 100.0% |
| [边界挑战：给药频次](challenge_frequency/README.md) | 频次解析 | 20 | Accuracy | 100.0% | 100.0% |
| [边界挑战：用药变更](challenge_medication_change/README.md) | 用药变更判断 | 20 | Accuracy | 100.0% | 100.0% |
