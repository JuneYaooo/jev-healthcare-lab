# 术后转归去向选择

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

给定术后恢复指标，选择原记录的 ICU、普通病房或回家去向。历史记录选择不等于临床最优决策。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `postoperative_disposition` |
| 医疗场景 | 住院与护理 |
| 能力维度 | 流程与下一步行动 |
| 决策类型 | 临床行动选择 |
| 当前题数 / 目标题数 | 68 / 100 |
| 来源组数 | 68 |
| 语种 | 英语 68 题 |
| 数据范围 | 开放许可核心集 68 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [Post-Operative Patient](../datasets/uci_postoperative.md) | 68 | [原始来源](https://archive.ics.uci.edu/dataset/82/post+operative+patient) |

## 如何作答与评分

根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`postoperative_disposition:uci_postoperative:11`；语种：英语；来源组：`uci_postoperative:b8e707039081876ef71e8383e3797f08a2dda217a6a687e571393c954edbe509`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "General hospital floor",
        "I": "Intensive care unit",
        "S": "Prepared to go home"
      },
      "instructions": "给定术后恢复指标，选择原记录的 ICU、普通病房或回家去向。历史记录选择不等于临床最优决策。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_features": {
      "BP-STBL": "stable",
      "COMFORT": "15",
      "CORE-STBL": "stable",
      "L-BP": "mid",
      "L-CORE": "mid",
      "L-O2": "good",
      "L-SURF": "mid",
      "SURF-STBL": "stable"
    },
    "feature_definitions": {
      "BP-STBL": {
        "description": "stability of patient's blood pressure",
        "units": null
      },
      "COMFORT": {
        "description": "patient's perceived comfort at discharge, measured between 0 and 20",
        "units": null
      },
      "CORE-STBL": {
        "description": "stability of patient's core temperature",
        "units": null
      },
      "L-BP": {
        "description": "last measurement of blood pressure",
        "units": null
      },
      "L-CORE": {
        "description": "patient's internal temperature",
        "units": "C"
      },
      "L-O2": {
        "description": "oxygen saturation",
        "units": "%"
      },
      "L-SURF": {
        "description": "patient's surface temperature",
        "units": "C"
      },
      "SURF-STBL": {
        "description": "stability of patient's surface temperature",
        "units": null
      }
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `A`，对应选项：

```json
"General hospital floor"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "postoperative_disposition:uci_postoperative:11", "choice": "A"}
```

### 样例溯源

[上游资源](https://archive.ics.uci.edu/static/public/82/post+operative+patient.zip) · [数据集说明](../datasets/uci_postoperative.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "csv_row": 11,
    "supporting_resources": [
      "uci_postoperative__metadata.json"
    ],
    "zip_member": "post-operative.data"
  },
  "material_kind": "structured_clinical_observations",
  "resource": "uci_postoperative__data.zip",
  "resource_sha256": "eed2652e7d4b2c2653b94e383d991dd1806631a1566ea07ea2cdfb0c1cc16f25",
  "resource_url": "https://archive.ics.uci.edu/static/public/82/post+operative+patient.zip",
  "source_id": "uci_postoperative",
  "source_url": "https://archive.ics.uci.edu/dataset/82/post+operative+patient",
  "split": "published_corpus_no_official_split",
  "upstream_group": "b8e707039081876ef71e8383e3797f08a2dda217a6a687e571393c954edbe509",
  "upstream_id": "11",
  "version": "UCI snapshot 2026-10-10; SHA-256 locked"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：A 48 题、I 2 题、S 18 题。

当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。

**[Post-Operative Patient](../datasets/uci_postoperative.md)**：Dataset of patient features 答案依据：ADM-DECS 原术后去向标签；相同输入冲突全部排除，无患者 ID，不冒称患者独立。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/postoperative_disposition/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/postoperative_disposition/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
