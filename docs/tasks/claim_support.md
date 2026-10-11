# 研究论断与摘要一致性判断

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 是文献证据判断，不评价指定患者治疗获益；单列证据评估。

## 任务是什么

给定论断与被引摘要，判断支持、反驳或证据不足。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `claim_support` |
| 医疗场景 | 病历与医疗质量控制 |
| 能力维度 | 证据与一致性 |
| 评测类别 | 临床计算、解读与证据 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [SciFact](../datasets/scifact.md) | 100 | [原始来源](https://github.com/allenai/scifact) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。固定语义标签计算准确率、宏 F1、召回与混淆矩阵。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`claim_support:scifact:232:10536636`；语种：英语；来源组：`scifact:10536636`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "CONTRADICT": "Contradicts the claim",
        "NOT_ENOUGH_INFO": "No annotated support or contradiction in this abstract",
        "SUPPORT": "Supports the claim"
      },
      "instructions": "给定论断与被引摘要，判断支持、反驳或证据不足。",
      "type": "choice"
    }
  },
  "state": {
    "abstract": "Background Blindness and low vision are thought to be common in southern Sudan. However, the magnitude and geographical distribution are largely unknown. We aimed to estimate the prevalence of blindness and low vision, identify the main causes of blindness and low vision, and estimate targets for blindness prevention programs in Mankien payam (district), southern Sudan.",
    "claim": "Cataract and trachoma are the primary cause of blindness in Southern Sudan.",
    "title": "Prevalence and Causes of Blindness and Low Vision in Southern Sudan "
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `NOT_ENOUGH_INFO`，对应选项：

```json
"No annotated support or contradiction in this abstract"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "claim_support:scifact:232:10536636", "choice": "NOT_ENOUGH_INFO"}
```

### 样例溯源

[上游资源](https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz) · [数据集说明](../datasets/scifact.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0 AND ODC-By-1.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "claim_id": 232,
    "doc_id": "10536636"
  },
  "material_kind": "scientific_literature",
  "resource": "scifact__data.tar.gz",
  "resource_sha256": "11c621288d41ac144d29b13b0f8503b3820b7d6e8b1f6ff24dff335c196d76be",
  "resource_url": "https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz",
  "source_id": "scifact",
  "source_url": "https://github.com/allenai/scifact",
  "split": "official_dev_document_disjoint_from_upstream_train",
  "upstream_group": "10536636",
  "upstream_id": "232:10536636",
  "version": "sha256:11c621288d41ac144d29b13b0f8503b3820b7d6e8b1f6ff24dff335c196d76be"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：CONTRADICT 20 题、NOT_ENOUGH_INFO 39 题、SUPPORT 41 题。

**[SciFact](../datasets/scifact.md)**：科学论文摘要，不全是临床医学。 答案依据：原始 claim evidence 标签；无该文证据标注记为未标注支持或反驳。

其中 31 题材料或片段命中过往评测指纹；训练效果对比应核查材料暴露，并对各模型冻结相同子集。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/claim_support/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/claim_support/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
