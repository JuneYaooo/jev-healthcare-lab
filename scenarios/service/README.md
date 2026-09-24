# 患者咨询、服务路由与就医流程

**9 个任务条件，708 条主评测记录。** [全部场景](../../README.md)

MedQuAD 测问题类型；MedJourney 的科室多标签与四类选择题不是实际分诊效果。

| 任务（点击查看方法与费用） | 任务类型 | 记录数 | 指标 | Jev | DeepSeek |
| --- | --- | ---: | --- | ---: | ---: |
| [中文问诊对话行为分类](imcs_dialogue_act/README.md) | 意图分类 | 100 | Accuracy | 70.0% | 68.0% |
| [患者问题信息需求分类](medquad_question_type/README.md) | 意图分类 | 100 | Accuracy | 96.0% | 97.0% |
| [主诉推荐就诊科室](medjourney_departments/README.md) | 多标签科室推荐 | 100 | micro-F1 | 36.9% | 34.9% |
| [MedJourney 诊断预测选择题](medjourney_dp_mcq/README.md) | 单选问答 | 100 | Accuracy | 92.0% | 91.0% |
| [MedJourney 检查预测选择题](medjourney_ep_mcq/README.md) | 单选问答 | 100 | Accuracy | 82.0% | 79.0% |
| [MedJourney 用药预测选择题](medjourney_mp_mcq/README.md) | 单选问答 | 100 | Accuracy | 86.0% | 88.0% |
| [MedJourney 治疗预测选择题](medjourney_tp_mcq/README.md) | 单选问答 | 100 | Accuracy | 83.0% | 82.0% |
| [边界挑战：服务路由](challenge_service_route/README.md) | 服务路由分类 | 4 | Accuracy | 100.0% | 100.0% |
| [边界挑战：给定规则紧急程度](challenge_urgency_given_policy/README.md) | 规则紧急程度分类 | 4 | Accuracy | 100.0% | 100.0% |
