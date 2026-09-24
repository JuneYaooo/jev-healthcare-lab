# 临床计算、参数选择与评分量表

**8 个任务条件，514 条主评测记录。** [全部场景](../../README.md)

参数选择与公式执行分开记录；Verified 只适配 5 种评分各 20 条，不是全部计算器。

| 任务（点击查看方法与费用） | 任务类型 | 记录数 | 指标 | Jev | DeepSeek |
| --- | --- | ---: | --- | ---: | ---: |
| [BMI 当前身高参数选择](bmi_height_selection/README.md) | 数值参数选择 | 20 | Accuracy | 95.0% | 95.0% |
| [BMI 当前体重参数选择](bmi_weight_selection/README.md) | 数值参数选择 | 20 | Accuracy | 95.0% | 90.0% |
| [临床计算输入充分性](cmedcalc_input_sufficiency/README.md) | 输入充分性判断 | 200 | Accuracy | 81.5% | 84.0% |
| [临床量表语义分级](cmedcalc_semantic_grade/README.md) | 量表分级 | 162 | Accuracy | 60.5% | 39.5% |
| [五种临床量表闭集数值评分](medcalc_verified_bounded_score/README.md) | 闭集数值评分 | 100 | Accuracy | 25.0% | 31.0% |
| [边界挑战：检验数值关联](challenge_lab_link/README.md) | 检验数值关联 | 4 | Accuracy | 100.0% | 100.0% |
| [边界挑战：缺失计算参数](challenge_missing_parameter/README.md) | 输入充分性判断 | 4 | Accuracy | 100.0% | 100.0% |
| [边界挑战：单位等价](challenge_unit_equivalence/README.md) | 单位等价判断 | 4 | Accuracy | 100.0% | 100.0% |
