# Chinese-medical-dialogue-data

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

中文在线医疗问答汇编，原平台逐条溯源不足。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `chinese_medical_dialogue` |
| 上游入口 | [发布方页面](https://github.com/Toyhom/Chinese-medical-dialogue-data) |
| 收录情况 | 0 题；仅作参考 |
| 使用范围 | 仅作参考，未收录题目 |
| 登记的数据许可 | 仓库 MIT；原问诊内容授权链未核实 |
| 收录语种 | 无收录题目 |

## 来源与引用

[补充核验依据](https://github.com/Toyhom/Chinese-medical-dialogue-data)

### 登记边界

科室字段是采集来源的分类，未证明为临床审核的最佳首诊科室；不能直接作分流金标。

## 用于哪些任务

当前没有使用该来源的评测任务。

## 样例数据

**样例留空。** 当前未收录可用于本评测集的题目，仅保留来源与调研信息；不复制许可未闭合或需受控访问的原文。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [候选科室分流](../tasks/department_routing.md) | 根据就诊主诉从固定科室表选择适合的首诊科室。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
