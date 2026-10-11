# MIMIC-IV Clinical Database Demo v2.2

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

真实去标识临床数据库演示子集。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `mimic_iv_demo` |
| 上游入口 | [发布方页面](https://physionet.org/content/mimic-iv-demo/2.2/) |
| 收录情况 | 0 题；仅作参考 |
| 评测用途 | 仅作参考 |
| 使用范围 | 仅作参考，未收录题目 |
| 登记的数据许可 | Open Data Commons Open Database License v1.0（以发布页为准） |
| 收录语种 | 无收录题目 |

## 来源与引用

[补充核验依据](https://physionet.org/content/mimic-iv-demo/2.2/)

### 登记边界

开放结构化演示数据可作开发材料；本轮未建立覆盖开单、配药、给入、未执行的独立证据与金标协议。不能把已有状态字段原样放进输入再要求选择同一字段。

## 用于哪些任务

当前没有使用该来源的评测任务。

## 样例数据

**样例留空。** 当前未收录可用于本评测集的题目，仅保留来源与调研信息；不复制许可未闭合或需受控访问的原文。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [患者记录身份核对](../tasks/patient_identity.md) | 判断两条材料是否属于同一患者及身份是否可确定。 |
| [给药执行记录状态核对](../tasks/administration_status.md) | 判断已开医嘱、已配药、已给入或未执行。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
