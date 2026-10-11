# 孕产风险等级识别

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

根据孕产记录的年龄与生命体征，选择发布数据标注的低、中、高风险；不等同经过验证的母婴结局预测。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `maternal_risk` |
| 医疗场景 | 接诊与分诊 |
| 能力维度 | 风险与升级 |
| 决策类型 | 风险分类 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可核心集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [Maternal Health Risk](../datasets/uci_maternal.md) | 100 | [原始来源](https://archive.ics.uci.edu/dataset/863/maternal+health+risk) |

## 如何作答与评分

根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`maternal_risk:uci_maternal:654`；语种：英语；来源组：`uci_maternal:01bf8b7531e1af7107642c1b821b0a79e4467e4b580223a2145227f17fa2d246`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "high risk": "High risk",
        "low risk": "Low risk",
        "mid risk": "Intermediate risk"
      },
      "instructions": "根据孕产记录的年龄与生命体征，选择发布数据标注的低、中、高风险；不等同经过验证的母婴结局预测。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_features": {
      "Age": "15",
      "BS": "7",
      "BodyTemp": "98",
      "DiastolicBP": "68",
      "HeartRate": "77",
      "SystolicBP": "76"
    },
    "feature_definitions": {
      "Age": {
        "description": "Any ages in years when a women during pregnant.",
        "units": null
      },
      "BS": {
        "description": "Blood glucose levels is in terms of a molar concentration",
        "units": "mmol/L"
      },
      "BodyTemp": {
        "description": null,
        "units": "F"
      },
      "DiastolicBP": {
        "description": "Lower value of Blood Pressure in mmHg, another significant attribute during pregnancy.",
        "units": null
      },
      "HeartRate": {
        "description": "A normal resting heart rate",
        "units": "bpm"
      },
      "SystolicBP": {
        "description": "Upper value of Blood Pressure in mmHg, another significant attribute during pregnancy.",
        "units": null
      }
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `low risk`，对应选项：

```json
"Low risk"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "maternal_risk:uci_maternal:654", "choice": "low risk"}
```

### 样例溯源

[上游资源](https://archive.ics.uci.edu/static/public/863/maternal+health+risk.zip) · [数据集说明](../datasets/uci_maternal.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "csv_row": 655,
    "supporting_resources": [
      "uci_maternal__metadata.json"
    ],
    "zip_member": "Maternal Health Risk Data Set.csv"
  },
  "material_kind": "structured_clinical_observations",
  "resource": "uci_maternal__data.zip",
  "resource_sha256": "84f0de0d647bb217ff7224ff265afadf27eb65c5483baaf1cfcc59abadeb75b1",
  "resource_url": "https://archive.ics.uci.edu/static/public/863/maternal+health+risk.zip",
  "source_id": "uci_maternal",
  "source_url": "https://archive.ics.uci.edu/dataset/863/maternal+health+risk",
  "split": "published_corpus_no_official_split",
  "upstream_group": "01bf8b7531e1af7107642c1b821b0a79e4467e4b580223a2145227f17fa2d246",
  "upstream_id": "654",
  "version": "UCI snapshot 2026-10-10; SHA-256 locked"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：high risk 31 题、low risk 49 题、mid risk 20 题。

**[Maternal Health Risk](../datasets/uci_maternal.md)**：Data has been collected from different hospitals, community clinics, maternal health cares from the rural areas of Bangladesh through the IoT based risk monitoring system. 答案依据：沿用原 RiskLevel，不能当成独立结局随访；完全相同特征冲突全部排除，无患者 ID。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/maternal_risk/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/maternal_risk/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
