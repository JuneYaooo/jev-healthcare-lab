# 心衰患者 90 日死亡结局预测

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 仅限心衰基线记录及声明的删失规则；不是普适死亡风险，100 题阳性 22，需报告风险指标与基线。

## 任务是什么

根据基线心衰记录预测 90 日内死亡；不提供随访长度；90 日前无死亡但失访者已排除。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `mortality_90d` |
| 医疗场景 | 出院与随访 |
| 能力维度 | 风险与升级 |
| 评测类别 | 风险、结局与历史去向预测 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [Heart Failure Clinical Records](../datasets/uci_heart_failure.md) | 100 | [原始来源](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。固定语义标签计算准确率、宏 F1、召回与混淆矩阵。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`mortality_90d:uci_heart_failure:11`；语种：英语；来源组：`uci_heart_failure:298504e9d7b8fb7dba4215b0306686f889f70ffd7e6a5da2bb74dc3311cb452a`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "no": "Observed alive through day 90",
        "yes": "Death by day 90"
      },
      "instructions": "根据基线心衰记录预测 90 日内死亡；不提供随访长度；90 日前无死亡但失访者已排除。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_features": {
      "age": "75",
      "anaemia": "1",
      "creatinine_phosphokinase": "81",
      "diabetes": "0",
      "ejection_fraction": "38",
      "high_blood_pressure": "1",
      "platelets": "368000",
      "serum_creatinine": "4",
      "serum_sodium": "131",
      "sex": "1",
      "smoking": "1"
    },
    "feature_definitions": {
      "age": {
        "description": "age of the patient",
        "units": "years"
      },
      "anaemia": {
        "description": "decrease of red blood cells or hemoglobin",
        "units": null
      },
      "creatinine_phosphokinase": {
        "description": "level of the CPK enzyme in the blood",
        "units": "mcg/L"
      },
      "diabetes": {
        "description": "if the patient has diabetes",
        "units": null
      },
      "ejection_fraction": {
        "description": "percentage of blood leaving the heart at each contraction",
        "units": "%"
      },
      "high_blood_pressure": {
        "description": "if the patient has hypertension",
        "units": null
      },
      "platelets": {
        "description": "platelets in the blood",
        "units": "kiloplatelets/mL"
      },
      "serum_creatinine": {
        "description": "level of serum creatinine in the blood",
        "units": "mg/dL"
      },
      "serum_sodium": {
        "description": "level of serum sodium in the blood",
        "units": "mEq/L"
      },
      "sex": {
        "description": "woman or man",
        "units": null
      },
      "smoking": {
        "description": "if the patient smokes or not",
        "units": null
      }
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `yes`，对应选项：

```json
"Death by day 90"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "mortality_90d:uci_heart_failure:11", "choice": "yes"}
```

### 样例溯源

[上游资源](https://archive.ics.uci.edu/static/public/519/heart+failure+clinical+records.zip) · [数据集说明](../datasets/uci_heart_failure.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "csv_row": 12,
    "supporting_resources": [
      "uci_heart_failure__metadata.json"
    ],
    "zip_member": "heart_failure_clinical_records_dataset.csv"
  },
  "material_kind": "structured_clinical_observations",
  "resource": "uci_heart_failure__data.zip",
  "resource_sha256": "f0739603e2f9573ffc7d509573cbf9bcb4cc889e4eea0f35a75bec68fc9163d7",
  "resource_url": "https://archive.ics.uci.edu/static/public/519/heart+failure+clinical+records.zip",
  "source_id": "uci_heart_failure",
  "source_url": "https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records",
  "split": "published_corpus_no_official_split",
  "upstream_group": "298504e9d7b8fb7dba4215b0306686f889f70ffd7e6a5da2bb74dc3311cb452a",
  "upstream_id": "11",
  "version": "UCI snapshot 2026-10-10; SHA-256 locked"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：no 78 题、yes 22 题。

**[Heart Failure Clinical Records](../datasets/uci_heart_failure.md)**：This dataset contains the medical records of 299 patients who had heart failure, collected during their follow-up period, where each patient profile has 13 clinical features. 答案依据：90 日死亡：time<=90 且 DEATH_EVENT=1 为阳性；time>=90 且无此前死亡为阴性；90 日前删失排除。time 与死亡标签不输入。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/mortality_90d/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/mortality_90d/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
