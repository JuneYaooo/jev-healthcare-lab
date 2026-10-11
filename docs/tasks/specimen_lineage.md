# 标本来源关系核对

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 属于检验流程追溯，当前为空；标准字段示例不能充当独立病例金标。

## 任务是什么

区分同一实物、派生关系、无关系和信息不足。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `specimen_lineage` |
| 医疗场景 | 检查与检验 |
| 能力维度 | 关联与匹配 |
| 评测类别 | 流程与记录核对 |
| 当前题数 / 目标题数 | 0 / 100 |
| 来源组数 | 0 |
| 语种 | 待补 |
| 数据范围 | 待补 |

## 数据集来源

当前没有收录题目，不参与评分。

## 样例与缺口

**样例待补。** 尚无符合此任务定义的可用题目，不提供虚构输入、选项或答案。

FHIR Specimen.parent 提供字段和示例；未找到同物、派生、无关、未知四类的开放标注病例。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [FHIR R4 clinical workflow definitions](../datasets/fhir_workflow.md) | 可定义诊断核实、标本链、操作及报告状态；标准示例不等于独立临床金标数据集。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/specimen_lineage/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/specimen_lineage/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
