# PromptCBLUE

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

CBLUE 等任务的指令化衍生集合。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `promptcblue` |
| 上游入口 | [发布方页面](https://github.com/michael-wzhu/PromptCBLUE) |
| 收录情况 | 0 题；仅作参考 |
| 使用范围 | 仅作参考，未收录题目 |
| 登记的数据许可 | 未核验到覆盖全部上游数据的独立分发许可 |
| 收录语种 | 无收录题目 |

## 来源与引用

[补充核验依据](https://github.com/michael-wzhu/PromptCBLUE)

### 登记边界

优先回到 CBLUE 原任务核验许可和划分；不把模板改写当独立来源或独立病例，不纳入生成子任务。

## 用于哪些任务

当前没有使用该来源的评测任务。

## 样例数据

**样例留空。** 当前未收录可用于本评测集的题目，仅保留来源与调研信息；不复制许可未闭合或需受控访问的原文。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [医疗问题意图](../tasks/query_intent.md) | 给定医疗问题，判断其信息需求类别。 |
| [入排条件要素分类](../tasks/criterion_entity_type.md) | 给定条件原文与目标实体，判断原标注的要素类别。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
