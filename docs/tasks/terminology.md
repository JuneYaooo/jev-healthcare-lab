# 医学术语标准化

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 术语表映射任务；当前为空，与临床方案判断分开。

## 任务是什么

从固定术语表选择对应标准术语或不确定。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `terminology` |
| 医疗场景 | 病历与医疗质量控制 |
| 能力维度 | 分类与标准化 |
| 评测类别 | 文本理解与标注 |
| 当前题数 / 目标题数 | 0 / 100 |
| 来源组数 | 0 |
| 语种 | 待补 |
| 数据范围 | 待补 |

## 数据集来源

当前没有收录题目，不参与评分。

## 样例与缺口

**样例待补。** 尚无符合此任务定义的可用题目，不提供虚构输入、选项或答案。

MeDAL 原摘要版权尚未闭合；IMCS21 未明确数据许可；CBLUE 的术语材料及授权需按任务核验，不用代码许可证代替。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [CBLUE（KUAKE-QIC / CHIP-CTC / CHIP-CDN）](../datasets/cblue.md) | 不能用代码许可替代数据许可；需取得官方数据包及其协议，核验开发集答案，CDN 候选术语表还需核对许可。 |
| [IMCS-21](../datasets/imcs21.md) | 未发现明确数据许可 |
| [MeDAL](../datasets/medal.md) | Zenodo v4 与原 README 明确指向 NLM 条款，部分 PubMed 摘要仍可能受第三方版权保护。不能将模型/代码 MIT 或 Apache 许可当作全部摘要数据开放许可；本轮留空。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/terminology/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/terminology/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
