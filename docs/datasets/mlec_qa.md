# MLEC-QA

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

中文执业医师考试题，包含共享病例题干。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `mlec_qa` |
| 上游入口 | [发布方页面](https://github.com/Judenpech/MLEC-QA) |
| 收录情况 | 0 题；仅作参考 |
| 使用范围 | 仅作参考，未收录题目 |
| 登记的数据许可 | MIT（代码）；下载包数据许可待核验 |
| 收录语种 | 无收录题目 |

## 来源与引用

[补充核验依据](https://github.com/Judenpech/MLEC-QA)

### 登记边界

需下载官方包核对独立数据许可、测试划分和共享题干；仅收病例决策单选。

## 用于哪些任务

当前没有使用该来源的评测任务。

## 样例数据

**样例留空。** 当前未收录可用于本评测集的题目，仅保留来源与调研信息；不复制许可未闭合或需受控访问的原文。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [临床病例候选诊断](../tasks/diagnosis_choice.md) | 从给定诊断候选中选择最符合病例者。 |
| [检查方案选择](../tasks/examination_choice.md) | 根据病例从给定候选中选择检查。 |
| [治疗方案选择](../tasks/treatment_choice.md) | 根据病例从给定候选中选择治疗。 |
| [用药方案选择](../tasks/medication_choice.md) | 根据病例从给定候选中选择用药。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
