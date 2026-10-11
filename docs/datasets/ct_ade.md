# CT-ADE-SOC / CT-ADE-PT

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

临床试验组层面的单药与不良事件数据。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `ct_ade` |
| 上游入口 | [发布方页面](https://github.com/ds4dh/CT-ADE) |
| 收录情况 | 0 题；仅作参考 |
| 使用范围 | 仅作参考，未收录题目 |
| 登记的数据许可 | MIT（SOC 数据卡）；第三方术语与补充源需单独核验 |
| 收录语种 | 无收录题目 |

## 来源与引用

[补充核验依据](https://huggingface.co/datasets/anthonyyazdaniml/CT-ADE-SOC)

### 登记边界

核对数据版本和外部术语条件，按 NCT/试验组隔离；不良事件频率与标签不能作为输入。

## 用于哪些任务

当前没有使用该来源的评测任务。

## 样例数据

**样例留空。** 当前未收录可用于本评测集的题目，仅保留来源与调研信息；不复制许可未闭合或需受控访问的原文。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [治疗相关不良事件预测](../tasks/adverse_event_prediction.md) | 给定试验人群和单药方案，判断指定不良事件类别是否会在该组出现。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
