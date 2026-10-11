# 医疗操作记录状态核对

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 判断记录显示计划、完成或取消，未决定下一步操作；当前为空。

## 任务是什么

区分计划、进行、完成、取消及目标未达成。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `procedure_progress` |
| 医疗场景 | 住院与护理 |
| 能力维度 | 流程与下一步行动 |
| 评测类别 | 流程与记录核对 |
| 当前题数 / 目标题数 | 0 / 100 |
| 来源组数 | 0 |
| 语种 | 待补 |
| 数据范围 | 待补 |

## 数据集来源

当前没有收录题目，不参与评分。

## 样例与缺口

**样例待补。** 尚无符合此任务定义的可用题目，不提供虚构输入、选项或答案。

操作状态标准与 E3C 事件时态不同；未找到完整覆盖计划、进行、完成、取消、目标未达成的开放金标。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [E3C English Layer 1](../datasets/e3c.md) | 本任务暂无收录，是否适用需按任务定义核验。 |
| [FHIR R4 clinical workflow definitions](../datasets/fhir_workflow.md) | 可定义诊断核实、标本链、操作及报告状态；标准示例不等于独立临床金标数据集。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/procedure_progress/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/procedure_progress/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
