# CLIP 出院行动标注

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

MIMIC-III 出院记录，部分脱敏占位替换为合成信息。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `clip` |
| 上游入口 | [发布方页面](https://physionet.org/content/mimic-iii-clinical-action/1.0.0/) |
| 收录情况 | 0 题；仅作参考 |
| 评测用途 | 仅作参考 |
| 使用范围 | 仅作参考，未收录题目 |
| 登记的数据许可 | PhysioNet Credentialed Health Data License 1.5.0 |
| 收录语种 | 无收录题目 |

## 来源与引用

[补充核验依据](https://doi.org/10.13026/kw00-z903)

### 登记边界

需凭证、培训及 DUA；只能在获准环境适配，不公开转发原文。

## 用于哪些任务

当前没有使用该来源的评测任务。

## 样例数据

**样例留空。** 当前未收录可用于本评测集的题目，仅保留来源与调研信息；不复制许可未闭合或需受控访问的原文。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [随访待办与完成状态核对](../tasks/followup_action.md) | 从固定候选中选择待办行动并判断是否完成或逾期。 |
| [出院文书待办类别识别](../tasks/followup_item_type.md) | 给定出院文书片段，判断是否有待办及所属复诊、检验、影像、用药等类别。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
