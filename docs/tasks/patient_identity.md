# 患者记录身份核对

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 属于医疗安全和数据身份核对；当前为空，不能将合成身份连接等同临床身份判定。

## 任务是什么

判断两条材料是否属于同一患者及身份是否可确定。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `patient_identity` |
| 医疗场景 | 住院与护理 |
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

FEBRL 是合成人口学匹配，MIMIC 演示 ID 连接不是身份可确定性评测；缺医疗证据、冲突及不确定金标。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [FEBRL record linkage datasets](../datasets/febrl.md) | 公开合成身份匹配基准，不是医疗材料的患者身份核实；缺信息时的不确定标签也未覆盖。 |
| [MIMIC-IV Clinical Database Demo v2.2](../datasets/mimic_iv_demo.md) | 开放结构化演示数据可作开发材料；本轮未建立覆盖开单、配药、给入、未执行的独立证据与金标协议。不能把已有状态字段原样放进输入再要求选择同一字段。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/patient_identity/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/patient_identity/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
