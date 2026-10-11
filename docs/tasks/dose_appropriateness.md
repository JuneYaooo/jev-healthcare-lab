# 患者剂量适宜性判断

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 方向适合主评测，但当前无题目；需患者状态、具体处方和有来源的适宜性金标。

## 任务是什么

给定药品规则及患者肝肾功能等，判断剂量是否适宜。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `dose_appropriateness` |
| 医疗场景 | 治疗与用药 |
| 能力维度 | 资格与适宜性 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 0 / 100 |
| 来源组数 | 0 |
| 语种 | 待补 |
| 数据范围 | 待补 |

## 数据集来源

当前没有收录题目，不参与评分。

## 样例与缺口

**样例待补。** 尚无符合此任务定义的可用题目，不提供虚构输入、选项或答案。

openFDA 是药品说明书规则；尚缺患者肝肾功能、具体处方及独立剂量适宜性金标。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [CMedCalc-Bench](../datasets/cmedcalc.md) | 公开仓库未见明确数据许可；原文与合成混合 |
| [openFDA drug labels](../datasets/openfda.md) | 可作规则材料，尚无对应患者判断题与金标 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/dose_appropriateness/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/dose_appropriateness/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
