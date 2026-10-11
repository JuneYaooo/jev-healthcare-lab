# CBLUE（KUAKE-QIC / CHIP-CTC / CHIP-CDN）

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

医疗搜索问题、试验标准及诊断术语，材料性质分任务。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `cblue` |
| 上游入口 | [发布方页面](https://github.com/CBLUEbenchmark/CBLUE) |
| 收录情况 | 0 题；仅作参考 |
| 使用范围 | 仅作参考，未收录题目 |
| 登记的数据许可 | Apache-2.0（代码）；天池数据包协议待核验 |
| 收录语种 | 无收录题目 |

## 来源与引用

[补充核验依据](https://github.com/CBLUEbenchmark/CBLUE)

### 登记边界

不能用代码许可替代数据许可；需取得官方数据包及其协议，核验开发集答案，CDN 候选术语表还需核对许可。

## 用于哪些任务

当前没有使用该来源的评测任务。

## 样例数据

**样例留空。** 当前未收录可用于本评测集的题目，仅保留来源与调研信息；不复制许可未闭合或需受控访问的原文。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [医疗问题意图](../tasks/query_intent.md) | 给定医疗问题，判断其信息需求类别。 |
| [医学术语归一化](../tasks/terminology.md) | 从固定术语表选择对应标准术语或不确定。 |
| [入排条件要素分类](../tasks/criterion_entity_type.md) | 给定条件原文与目标实体，判断原标注的要素类别。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
