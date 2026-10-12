# 首诊科室选择

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 方向适合主评测，但无合适题目；采集平台科室标签不等于首诊推荐金标。

## 任务是什么

根据就诊主诉从固定科室表选择适合的首诊科室。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `department_routing` |
| 医疗场景 | 接诊与分诊 |
| 能力维度 | 临床候选方案 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 0 / 100 |
| 来源组数 | 0 |
| 语种 | 待补 |
| 数据范围 | 待补 |

## 数据集来源

当前没有收录题目，不参与评分。

## 样例与缺口

**样例待补。** 尚无符合此任务定义的可用题目，不提供虚构输入、选项或答案。

RD-Triage 有多答案及多上游来源需分别核权；ClinicalMC/MedJourney 数据许可未闭合；中文问诊科室字段不等于最佳首诊科室。

## 多问题与并发性能

持续多题并发尚未测试。以下为历史有限批次结果，不作为高并发高吞吐证据。

### 历史有限批次测试

本任务尚无可用原题，多问题与并发测试均待补；不以其他任务或合成规则结果代填。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [Chinese-medical-dialogue-data](../datasets/chinese_medical_dialogue.md) | 科室字段是采集来源的分类，未证明为临床审核的最佳首诊科室；不能直接作分流金标。 |
| [ClinicalMC / ClinicalMPD](../datasets/clinicalmc.md) | 只研究可封闭计分的子任务，需核验发布数据、许可及逐时点信息边界，不能把完整住院信息泄漏给早期决策。 |
| [MedJourney](../datasets/medjourney.md) | 未见明确数据许可；部分任务共用 CMB/CMExam 上游 |
| [RD-Triage](../datasets/rd_triage.md) | 优先核对上游来源许可与 PMID、单标签数量和诊断泄露；论文尚在审稿，适用范围为罕见病。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/department_routing/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/department_routing/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
