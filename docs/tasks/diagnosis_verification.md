# 病历诊断记录状态核对

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 当前定义是记录状态分类，尚无题目；应区别于根据病例作出诊断。

## 任务是什么

区分疑似、确诊、排除与未明确。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `diagnosis_verification` |
| 医疗场景 | 诊断与鉴别 |
| 能力维度 | 事实与状态 |
| 评测类别 | 流程与记录核对 |
| 当前题数 / 目标题数 | 0 / 100 |
| 来源组数 | 0 |
| 语种 | 待补 |
| 数据范围 | 待补 |

## 数据集来源

当前没有收录题目，不参与评分。

## 样例与缺口

**样例待补。** 尚无符合此任务定义的可用题目，不提供虚构输入、选项或答案。

FHIR 有核实状态定义；E3C 的实际/假设/不确定是事件属性，不能等同疑似/确诊/排除四分类。未找到匹配且可开放分发的原金标。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [E3C English Layer 1](../datasets/e3c.md) | 本任务暂无收录，是否适用需按任务定义核验。 |
| [FHIR R4 clinical workflow definitions](../datasets/fhir_workflow.md) | 可定义诊断核实、标本链、操作及报告状态；标准示例不等于独立临床金标数据集。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/diagnosis_verification/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/diagnosis_verification/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
