# 条件上界与下界

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

给定条件与数值限制片段，判断该限制是上界还是下界。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `criterion_bound` |
| 医疗场景 | 临床试验筛选 |
| 能力维度 | 资格与适宜性 |
| 决策类型 | 材料判断 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可核心集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [Clinical Trial Parser annotated test data](../datasets/frd.md) | 100 | [原始来源](https://github.com/facebookresearch/Clinical-Trial-Parser) |

## 如何作答与评分

根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`criterion_bound:frd:2301:1`；语种：英语；来源组：`frd:e97bc0b10c78cbbc9243b50e276b43da6c59024488dd2bc9edc4fe20b5960762`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "lower_bound": "Lower bound / minimum",
        "upper_bound": "Upper bound / maximum"
      },
      "instructions": "给定条件与数值限制片段，判断该限制是上界还是下界。",
      "type": "choice"
    }
  },
  "state": {
    "criterion": "anc > @NUMBER",
    "end_exclusive": 13,
    "start": 6,
    "target": "@NUMBER"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `lower_bound`，对应选项：

```json
"Lower bound / minimum"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "criterion_bound:frd:2301:1", "choice": "lower_bound"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/facebookresearch/Clinical-Trial-Parser/03ea0d3f5efe7d1bee713d05bb026201230d9409/data/ner/test_processed_medical_ner.tsv) · [数据集说明](../datasets/frd.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "Apache-2.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "annotation_index": 1,
    "line": 2301,
    "original_annotation": "7:14:lower_bound"
  },
  "material_kind": "clinical_trial_registry_normalized",
  "resource": "frd__data_ner_test_processed_medical_ner.tsv",
  "resource_sha256": "0a2f14cd8045e15327657962b999fddb651b01c132b092addb12b12b67d74b9e",
  "resource_url": "https://raw.githubusercontent.com/facebookresearch/Clinical-Trial-Parser/03ea0d3f5efe7d1bee713d05bb026201230d9409/data/ner/test_processed_medical_ner.tsv",
  "source_id": "frd",
  "source_url": "https://github.com/facebookresearch/Clinical-Trial-Parser",
  "split": "official_test",
  "upstream_group": "e97bc0b10c78cbbc9243b50e276b43da6c59024488dd2bc9edc4fe20b5960762",
  "upstream_id": "2301:1",
  "version": "03ea0d3f5efe7d1bee713d05bb026201230d9409"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：lower_bound 50 题、upper_bound 50 题。

**[Clinical Trial Parser annotated test data](../datasets/frd.md)**：真实试验条件，公开测试文本经过规范化，数字替换为 @NUMBER。 答案依据：专业标注员 upper_bound/lower_bound；这里只判断方向，不做数值推理。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/criterion_bound/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/criterion_bound/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
