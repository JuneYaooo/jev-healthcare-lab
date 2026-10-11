# 病历论断一致性判断

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 判断材料是否支持论断，可作可靠性辅助评测；没有直接诊疗动作，当前为空。

## 任务是什么

给定临床记录和论断，判断支持、矛盾或无法确定。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `clinical_statement_support` |
| 医疗场景 | 病历与医疗质量控制 |
| 能力维度 | 证据与一致性 |
| 评测类别 | 临床计算、解读与证据 |
| 当前题数 / 目标题数 | 0 / 100 |
| 来源组数 | 0 |
| 语种 | 待补 |
| 数据范围 | 待补 |

## 数据集来源

当前没有收录题目，不参与评分。

## 样例与缺口

**样例待补。** 尚无符合此任务定义的可用题目，不提供虚构输入、选项或答案。

MedNLI 原病历受控；NLI4CT 是试验报告二分类且原仓库数据许可不明确，不能替代病历三分类。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [MedNLI](../datasets/mednli.md) | 需凭证及 DUA；不从公开镜像绕过原始访问条件。 |
| [NLI4CT](../datasets/nli4ct.md) | 数据为试验报告论断的支持/矛盾二分类，缺少患者病历的无法确定类别；不替代当前病历三分类任务。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/clinical_statement_support/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/clinical_statement_support/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
