# openFDA drug labels

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

可作规则材料，尚无对应患者判断题与金标

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `openfda` |
| 上游入口 | [发布方页面](https://open.fda.gov/apis/drug/label/) |
| 收录情况 | 0 题；仅作参考 |
| 评测用途 | 仅作参考 |
| 使用范围 | 仅作参考，未收录题目 |
| 登记的数据许可 | 未确认；不据此再分发数据 |
| 收录语种 | 无收录题目 |

## 来源与引用

已登记入口：[上游页面](https://open.fda.gov/apis/drug/label/)。独立论文引用与数据许可未完整登记。

### 登记边界

可作规则材料，尚无对应患者判断题与金标

## 用于哪些任务

当前没有使用该来源的评测任务。

## 样例数据

**样例留空。** 当前未收录可用于本评测集的题目，仅保留来源与调研信息；不复制许可未闭合或需受控访问的原文。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [患者方案禁忌判断](../tasks/patient_contraindication.md) | 根据病例从原选项中选择不宜使用或禁忌的药物、检查或治疗方案。 |
| [患者剂量适宜性判断](../tasks/dose_appropriateness.md) | 给定药品规则及患者肝肾功能等，判断剂量是否适宜。 |
| [危急检验结果处置选择](../tasks/critical_result_escalation.md) | 根据明确规则选择无需升级、复核或立即升级。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
