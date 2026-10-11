# FHIR R4 clinical workflow definitions

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

互操作标准及示例。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `fhir_workflow` |
| 上游入口 | [发布方页面](https://hl7.org/fhir/R4/) |
| 收录情况 | 0 题；仅作参考 |
| 评测用途 | 仅作参考 |
| 使用范围 | 仅作参考，未收录题目 |
| 登记的数据许可 | 标准文档许可；不是病例标注集 |
| 收录语种 | 无收录题目 |

## 来源与引用

[补充核验依据](https://hl7.org/fhir/R4/)

### 登记边界

可定义诊断核实、标本链、操作及报告状态；标准示例不等于独立临床金标数据集。

## 用于哪些任务

当前没有使用该来源的评测任务。

## 样例数据

**样例留空。** 当前未收录可用于本评测集的题目，仅保留来源与调研信息；不复制许可未闭合或需受控访问的原文。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [病历诊断记录状态核对](../tasks/diagnosis_verification.md) | 区分疑似、确诊、排除与未明确。 |
| [标本来源关系核对](../tasks/specimen_lineage.md) | 区分同一实物、派生关系、无关系和信息不足。 |
| [医疗操作记录状态核对](../tasks/procedure_progress.md) | 区分计划、进行、完成、取消及目标未达成。 |
| [给药执行记录状态核对](../tasks/administration_status.md) | 判断已开医嘱、已配药、已给入或未执行。 |
| [报告状态核对](../tasks/report_stage.md) | 区分初步、最终、补充、更正及作废报告。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
