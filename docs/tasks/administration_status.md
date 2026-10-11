# 单次给药执行状态

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

判断已开医嘱、已配药、已给入或未执行。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `administration_status` |
| 医疗场景 | 住院与护理 |
| 能力维度 | 流程与下一步行动 |
| 决策类型 | 材料判断 |
| 当前题数 / 目标题数 | 0 / 100 |
| 来源组数 | 0 |
| 语种 | 待补 |
| 数据范围 | 待补 |

## 数据集来源

当前没有收录题目，不参与评分。

## 样例与缺口

**样例待补。** 尚无符合此任务定义的可用题目，不提供虚构输入、选项或答案。

MIMIC 演示为真实结构化事件；尚缺跨医嘱、配药、给入的可判定证据与统一答案协议，留空。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [FHIR R4 clinical workflow definitions](../datasets/fhir_workflow.md) | 可定义诊断核实、标本链、操作及报告状态；标准示例不等于独立临床金标数据集。 |
| [MIMIC-IV Clinical Database Demo v2.2](../datasets/mimic_iv_demo.md) | 开放结构化演示数据可作开发材料；本轮未建立覆盖开单、配药、给入、未执行的独立证据与金标协议。不能把已有状态字段原样放进输入再要求选择同一字段。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/administration_status/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/administration_status/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
