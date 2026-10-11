# 脓毒症提前预警

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

仅使用 ICU 前 12 小时的记录，判断按挑战定义的脓毒症起病是否发生在第 12 小时之后至第 24 小时（含）。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `deterioration_prediction` |
| 医疗场景 | 住院与护理 |
| 能力维度 | 风险与升级 |
| 决策类型 | 结局预测 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可核心集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [PhysioNet Challenge 2019](../datasets/sepsis2019.md) | 100 | [原始来源](https://physionet.org/content/challenge-2019/1.0.0/) |

## 如何作答与评分

根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`deterioration_prediction:sepsis2019:p014596`；语种：英语；来源组：`sepsis2019:p014596`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "no": "No challenge-defined sepsis onset in hours (12,24]",
        "yes": "Challenge-defined sepsis onset occurs in hours (12,24]"
      },
      "instructions": "仅使用 ICU 前 12 小时的记录，判断按挑战定义的脓毒症起病是否发生在第 12 小时之后至第 24 小时（含）。",
      "type": "choice"
    }
  },
  "state": {
    "feature_definitions": {
      "Age": "Age (years; source de-identification retained)",
      "BUN": "Blood urea nitrogen (mg/dL)",
      "Creatinine": "Creatinine (mg/dL)",
      "DBP": "Diastolic BP (mm Hg)",
      "EtCO2": "End-tidal CO2 (mm Hg)",
      "Gender": "Source coding: female 0, male 1",
      "Glucose": "Glucose (mg/dL)",
      "HR": "Heart rate (beats/min)",
      "Hct": "Hematocrit (%)",
      "Hgb": "Hemoglobin (g/dL)",
      "MAP": "Mean arterial pressure (mm Hg)",
      "O2Sat": "Pulse oximetry (%)",
      "Platelets": "Platelets (count*10^3/microliter)",
      "Potassium": "Potassium (mmol/L)",
      "Resp": "Respiration rate (breaths/min)",
      "SBP": "Systolic BP (mm Hg)",
      "Temp": "Temperature (degrees Celsius)",
      "WBC": "White blood cell count (count*10^3/microliter)"
    },
    "hourly_observations": [
      {
        "Age": 84.46,
        "BUN": null,
        "Creatinine": null,
        "DBP": null,
        "EtCO2": null,
        "Gender": 0.0,
        "Glucose": null,
        "HR": null,
        "Hct": null,
        "Hgb": null,
        "MAP": null,
        "O2Sat": null,
        "Platelets": null,
        "Potassium": null,
        "Resp": null,
        "SBP": null,
        "Temp": null,
        "WBC": null,
        "hour": 1
      },
      {
        "Age": 84.46,
        "BUN": null,
        "Creatinine": null,
        "DBP": null,
        "EtCO2": null,
        "Gender": 0.0,
        "Glucose": null,
        "HR": 74.0,
        "Hct": null,
        "Hgb": null,
        "MAP": 52.0,
        "O2Sat": 98.0,
        "Platelets": null,
        "Potassium": null,
        "Resp": 28.0,
        "SBP": null,
        "Temp": null,
        "WBC": null,
        "hour": 2
      },
      {
        "Age": 84.46,
        "BUN": null,
        "Creatinine": null,
        "DBP": null,
        "EtCO2": null,
        "Gender": 0.0,
        "Glucose": null,
        "HR": 68.0,
        "Hct": null,
        "Hgb": null,
        "MAP": 53.0,
        "O2Sat": 98.0,
        "Platelets": null,
        "Potassium": null,
        "Resp": 21.0,
        "SBP": null,
        "Temp": null,
        "WBC": null,
        "hour": 3
      },
      {
        "Age": 84.46,
        "BUN": null,
        "Creatinine": null,
        "DBP": null,
        "EtCO2": null,
        "Gender": 0.0,
        "Glucose": null,
        "HR": 68.0,
        "Hct": null,
        "Hgb": null,
        "MAP": null,
        "O2Sat": 99.0,
        "Platelets": null,
        "Potassium": null,
        "Resp": 23.0,
        "SBP": null,
        "Temp": null,
        "WBC": null,
        "hour": 4
      },
      {
        "Age": 84.46,
        "BUN": null,
        "Creatinine": null,
        "DBP": null,
        "EtCO2": null,
        "Gender": 0.0,
        "Glucose": null,
        "HR": 66.0,
        "Hct": null,
        "Hgb": null,
        "MAP": null,
        "O2Sat": 98.0,
        "Platelets": null,
        "Potassium": null,
        "Resp": 19.0,
        "SBP": null,
        "Temp": null,
        "WBC": null,
        "hour": 5
      },
      {
        "Age": 84.46,
        "BUN": null,
        "Creatinine": null,
        "DBP": null,
        "EtCO2": null,
        "Gender": 0.0,
        "Glucose": null,
        "HR": 71.0,
        "Hct": null,
        "Hgb": null,
        "MAP": null,
        "O2Sat": 97.0,
        "Platelets": null,
        "Potassium": null,
        "Resp": 15.0,
        "SBP": null,
        "Temp": null,
        "WBC": null,
        "hour": 6
      },
      {
        "Age": 84.46,
        "BUN": null,
        "Creatinine": null,
        "DBP": null,
        "EtCO2": null,
        "Gender": 0.0,
        "Glucose": null,
        "HR": 66.0,
        "Hct": null,
        "Hgb": null,
        "MAP": null,
        "O2Sat": 97.0,
        "Platelets": null,
        "Potassium": null,
        "Resp": 20.0,
        "SBP": null,
        "Temp": null,
        "WBC": null,
        "hour": 7
      },
      {
        "Age": 84.46,
        "BUN": 91.0,
        "Creatinine": 2.7,
        "DBP": null,
        "EtCO2": null,
        "Gender": 0.0,
        "Glucose": 127.0,
        "HR": null,
        "Hct": null,
        "Hgb": null,
        "MAP": 61.0,
        "O2Sat": 96.0,
        "Platelets": null,
        "Potassium": 4.9,
        "Resp": 21.0,
        "SBP": null,
        "Temp": null,
        "WBC": null,
        "hour": 8
      },
      {
        "Age": 84.46,
        "BUN": 91.0,
        "Creatinine": null,
        "DBP": null,
        "EtCO2": null,
        "Gender": 0.0,
        "Glucose": null,
        "HR": null,
        "Hct": null,
        "Hgb": null,
        "MAP": 80.0,
        "O2Sat": 94.0,
        "Platelets": null,
        "Potassium": 4.9,
        "Resp": 22.0,
        "SBP": null,
        "Temp": 35.33,
        "WBC": null,
        "hour": 9
      },
      {
        "Age": 84.46,
        "BUN": null,
        "Creatinine": null,
        "DBP": null,
        "EtCO2": null,
        "Gender": 0.0,
        "Glucose": null,
        "HR": 95.0,
        "Hct": null,
        "Hgb": null,
        "MAP": null,
        "O2Sat": 91.0,
        "Platelets": null,
        "Potassium": null,
        "Resp": 28.0,
        "SBP": null,
        "Temp": null,
        "WBC": null,
        "hour": 10
      },
      {
        "Age": 84.46,
        "BUN": null,
        "Creatinine": null,
        "DBP": null,
        "EtCO2": null,
        "Gender": 0.0,
        "Glucose": null,
        "HR": 97.0,
        "Hct": null,
        "Hgb": null,
        "MAP": null,
        "O2Sat": 92.0,
        "Platelets": null,
        "Potassium": null,
        "Resp": 24.0,
        "SBP": null,
        "Temp": null,
        "WBC": null,
        "hour": 11
      },
      {
        "Age": 84.46,
        "BUN": null,
        "Creatinine": null,
        "DBP": null,
        "EtCO2": null,
        "Gender": 0.0,
        "Glucose": null,
        "HR": 90.0,
        "Hct": null,
        "Hgb": null,
        "MAP": null,
        "O2Sat": 94.0,
        "Platelets": null,
        "Potassium": null,
        "Resp": 22.0,
        "SBP": null,
        "Temp": null,
        "WBC": null,
        "hour": 12
      }
    ],
    "missing_value_meaning": "null = no recorded measurement; no imputation",
    "outcome_window_hours": {
      "after": 12,
      "through": 24
    },
    "prediction_hour": 12
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `no`，对应选项：

```json
"No challenge-defined sepsis onset in hours (12,24]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "deterioration_prediction:sepsis2019:p014596", "choice": "no"}
```

### 样例溯源

[上游资源](https://physionet-open.s3.amazonaws.com/challenge-2019/1.0.0/training/training_setA/p014596.psv) · [数据集说明](../datasets/sepsis2019.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "followup_requirement": "observed through inferred onset or hour 24",
    "input_data_rows_one_based": [
      1,
      12
    ],
    "onset_mapping": "first positive row hour + 6; initial positive excluded",
    "outcome_column": "SepsisLabel"
  },
  "material_kind": "real_clinical_time_series",
  "resource": "sepsis2019__p014596.psv",
  "resource_sha256": "0e42a305baa380214f23b2b6450f212d9ef4a00dc4d8f5174bad78f1a6d26162",
  "resource_url": "https://physionet-open.s3.amazonaws.com/challenge-2019/1.0.0/training/training_setA/p014596.psv",
  "source_id": "sepsis2019",
  "source_url": "https://physionet.org/content/challenge-2019/1.0.0/",
  "split": "upstream_train_reserved_for_local_evaluation",
  "upstream_group": "p014596",
  "upstream_id": "p014596",
  "version": "1.0.0"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：no 89 题、yes 11 题。

**[PhysioNet Challenge 2019](../datasets/sepsis2019.md)**：真实 ICU 小时记录；只使用公开训练医院 A 中按固定哈希预选的 1,000 个来源记录，非官方隐藏测试。 答案依据：原 SepsisLabel 提前 6 小时。首次 1 所在小时加 6 得到挑战定义起病小时。要求完整 ICU 第 1–12 小时，随访至起病或第 24 小时；排除起始即阳性、12 小时内起病、非法序列及随访不足。只给前 12 小时，预测 (12,24] 小时起病。

本子集仅有 11 个阳性、89 个阴性；恒答阴性准确率为 89%，应同时报告两类召回。来源是公开训练医院 A，不能对训练过该库的模型声称盲测。选择框为 1,000 例，合格 528 例（11 阳性/517 阴性）；分层抽样改变了类别比例，不用于风险校准、临床患病率或 PPV 估计。推算起病和原挑战逐小时 utility 不等价。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/deterioration_prediction/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/deterioration_prediction/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
