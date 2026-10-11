# 参考区间适用性

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

给定区间及人群、方法条件，选择适用区间或不确定。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `reference_range` |
| 医疗场景 | 检查与检验 |
| 能力维度 | 规则与数值 |
| 决策类型 | 临床候选方案选择 |
| 当前题数 / 目标题数 | 72 / 100 |
| 来源组数 | 25 |
| 语种 | 英语 72 题 |
| 数据范围 | 开放许可核心集 72 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [LabQAR](../datasets/labqar.md) | 72 | [原始来源](https://doi.org/10.6084/m9.figshare.29189894) |

## 如何作答与评分

根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`reference_range:labqar:200`；语种：英语；来源组：`labqar:6f4bce051fd84e952510`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "range_0": "15.3-53.3 μmol/L",
        "range_1": "22.9-68.6 μmol/L"
      },
      "instructions": "给定区间及人群、方法条件，选择适用区间或不确定。",
      "type": "choice"
    }
  },
  "state": {
    "reference_entries": [
      {
        "age_group": "any age group",
        "category": null,
        "condition": null,
        "range": "15.3-53.3",
        "sex": "Male",
        "specimen": "Serum",
        "test": "Creatine",
        "unit": "μmol/L"
      },
      {
        "age_group": "any age group",
        "category": null,
        "condition": null,
        "range": "22.9-68.6",
        "sex": "Female",
        "specimen": "Serum",
        "test": "Creatine",
        "unit": "μmol/L"
      }
    ],
    "rule": "Select the interval matching the target context in these source reference entries; do not infer a diagnosis or apply it as a universal laboratory standard.",
    "target_context": {
      "age_group": "any age group",
      "category": null,
      "condition": null,
      "sex": "Male",
      "specimen": "Serum",
      "test": "Creatine",
      "unit": "μmol/L"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `range_0`，对应选项：

```json
"15.3-53.3 μmol/L"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "reference_range:labqar:200", "choice": "range_0"}
```

### 样例溯源

[上游资源](https://ndownloader.figshare.com/files/61820641) · [数据集说明](../datasets/labqar.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "json_index": 199,
    "reference_json_indices": [
      199,
      200
    ],
    "upstream_id": 200
  },
  "material_kind": "curated_reference_rules",
  "resource": "labqar__Set_1.json",
  "resource_sha256": "4841ffdf57066852c34f0df4fdc8dea9cc383ce694a1d3939d9cd049f785abcb",
  "resource_url": "https://ndownloader.figshare.com/files/61820641",
  "source_id": "labqar",
  "source_url": "https://doi.org/10.6084/m9.figshare.29189894",
  "split": "published_corpus_reserved_for_evaluation",
  "upstream_group": "6f4bce051fd84e952510",
  "upstream_id": "200",
  "version": "figshare:29189894.v1"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：range_0 26 题、range_1 27 题、range_2 9 题、range_3 6 题、range_4 3 题、range_5 1 题。

当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。

**[LabQAR](../datasets/labqar.md)**：根据专家医学参考资料整理的区间与条件；Set 2 数值由作者构造，不是真实患者检验结果。 答案依据：原 Set 1 范围答案机械映射为同检验、单位、类别的固定候选；输入附上同组原参考条目，考查条件匹配。排除同条件答案冲突、裸数值及无替代范围条目；不生成范围或不确定答案。 Set 2 保留原 High/Normal/Low 选项与答案；仅收两端有限且有序的区间，排除边界相等、数值无法解析及原答案与给定区间不一致的题。

仅评估给定参考条目的人群、标本和条件匹配；不是独立诊疗知识或所有实验室范围的正确性。本版 72 题，未覆盖不确定和检验方法差异。 新增 Set 2 任务只测给定区间的数值判读，不推断诊断、危急值或处置优先级。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/reference_range/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/reference_range/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
