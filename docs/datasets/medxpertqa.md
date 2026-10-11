# MedXpertQA

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

专家复核的医学考试改写题；分 Text 与 MM。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `medxpertqa` |
| 上游入口 | [发布方页面](https://github.com/TsinghuaC3I/MedXpertQA) |
| 收录情况 | 0 题；仅作参考 |
| 评测用途 | 仅作参考 |
| 使用范围 | 仅作参考，未收录题目 |
| 登记的数据许可 | MIT（数据卡）；论文另要求不在线分享题例 |
| 收录语种 | 无收录题目 |

## 来源与引用

[补充核验依据](https://proceedings.mlr.press/v267/zuo25a.html)

### 登记边界

论文附录提出不在线分享题例；在与 MIT 数据卡的适用范围澄清前仅引用，不在本仓库再分发题目。

## 用于哪些任务

当前没有使用该来源的评测任务。

## 样例数据

**样例留空。** 当前未收录可用于本评测集的题目，仅保留来源与调研信息；不复制许可未闭合或需受控访问的原文。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [病例诊断选择：考试病例子集](../tasks/diagnosis_choice.md) | 从给定诊断候选中选择最符合病例者。 |
| [检查方案选择](../tasks/examination_choice.md) | 根据病例从给定候选中选择检查。 |
| [治疗方案选择](../tasks/treatment_choice.md) | 根据病例从给定候选中选择治疗。 |
| [用药方案选择](../tasks/medication_choice.md) | 根据病例从给定候选中选择用药。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
