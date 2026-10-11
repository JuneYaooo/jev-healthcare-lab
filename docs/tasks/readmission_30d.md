# 出院后 30 天内再入院预测

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

根据出院时结构化资料，预测是否被记录为 30 天内再入院。限糖尿病住院后回家人群，预测观察结局而非最优行动。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `readmission_30d` |
| 医疗场景 | 出院与随访 |
| 能力维度 | 风险与升级 |
| 决策类型 | 结局预测 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可核心集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [Diabetes 130-US Hospitals for Years 1999-2008](../datasets/uci_diabetes.md) | 100 | [原始来源](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008) |

## 如何作答与评分

根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`readmission_30d:uci_diabetes:72821`；语种：英语；来源组：`uci_diabetes:82a9d23e825365ccbb206268133c257a03f81510dc1c392ec46ef7f2a7d9142a`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "no": "No recorded readmission within 30 days",
        "yes": "Recorded readmission within 30 days"
      },
      "instructions": "根据出院时结构化资料，预测是否被记录为 30 天内再入院。限糖尿病住院后回家人群，预测观察结局而非最优行动。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_features": {
      "A1Cresult": "Norm",
      "acarbose": "No",
      "acetohexamide": "No",
      "admission_source_id": " Emergency Room",
      "admission_type_id": "Emergency",
      "age": "[50-60)",
      "change": "No",
      "chlorpropamide": "No",
      "citoglipton": "No",
      "diabetesMed": "No",
      "diag_1": "491",
      "diag_2": "303",
      "diag_3": "250",
      "discharge_disposition_id": "Discharged to home",
      "examide": "No",
      "gender": "Female",
      "glimepiride": "No",
      "glimepiride-pioglitazone": "No",
      "glipizide": "No",
      "glipizide-metformin": "No",
      "glyburide": "No",
      "glyburide-metformin": "No",
      "insulin": "No",
      "max_glu_serum": "None",
      "medical_specialty": null,
      "metformin": "No",
      "metformin-pioglitazone": "No",
      "metformin-rosiglitazone": "No",
      "miglitol": "No",
      "nateglinide": "No",
      "num_lab_procedures": "47",
      "num_medications": "10",
      "num_procedures": "0",
      "number_diagnoses": "9",
      "number_emergency": "0",
      "number_inpatient": "0",
      "number_outpatient": "0",
      "payer_code": "MC",
      "pioglitazone": "No",
      "race": null,
      "repaglinide": "No",
      "rosiglitazone": "No",
      "time_in_hospital": "1",
      "tolazamide": "No",
      "tolbutamide": "No",
      "troglitazone": "No",
      "weight": null
    },
    "feature_definitions": {
      "A1Cresult": {
        "description": "Indicates the range of the result or if the test was not taken. Values: >8 if the result was greater than 8%, >7 if the result was greater than 7% but less than 8%, normal if the result was less than 7%, and none if not measured.",
        "units": null
      },
      "acarbose": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "acetohexamide": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "admission_source_id": {
        "description": "Integer identifier corresponding to 21 distinct values, for example, physician referral, emergency room, and transfer from a hospital",
        "units": null
      },
      "admission_type_id": {
        "description": "Integer identifier corresponding to 9 distinct values, for example, emergency, urgent, elective, newborn, and not available",
        "units": null
      },
      "age": {
        "description": "Grouped in 10-year intervals: [0, 10), [10, 20),..., [90, 100)",
        "units": null
      },
      "change": {
        "description": "Indicates if there was a change in diabetic medications (either dosage or generic name). Values: change and no change",
        "units": null
      },
      "chlorpropamide": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "citoglipton": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "diabetesMed": {
        "description": "Indicates if there was any diabetic medication prescribed. Values: yes and no",
        "units": null
      },
      "diag_1": {
        "description": "The primary diagnosis (coded as first three digits of ICD9); 848 distinct values",
        "units": null
      },
      "diag_2": {
        "description": "Secondary diagnosis (coded as first three digits of ICD9); 923 distinct values",
        "units": null
      },
      "diag_3": {
        "description": "Additional secondary diagnosis (coded as first three digits of ICD9); 954 distinct values",
        "units": null
      },
      "discharge_disposition_id": {
        "description": "Integer identifier corresponding to 29 distinct values, for example, discharged to home, expired, and not available",
        "units": null
      },
      "examide": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "gender": {
        "description": "Values: male, female, and unknown/invalid",
        "units": null
      },
      "glimepiride": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "glimepiride-pioglitazone": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "glipizide": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "glipizide-metformin": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "glyburide": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "glyburide-metformin": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "insulin": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "max_glu_serum": {
        "description": "Indicates the range of the result or if the test was not taken. Values: >200, >300, normal, and none if not measured",
        "units": null
      },
      "medical_specialty": {
        "description": "Integer identifier of a specialty of the admitting physician, corresponding to 84 distinct values, for example, cardiology, internal medicine, family/general practice, and surgeon",
        "units": null
      },
      "metformin": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "metformin-pioglitazone": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "metformin-rosiglitazone": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "miglitol": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "nateglinide": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "num_lab_procedures": {
        "description": "Number of lab tests performed during the encounter",
        "units": null
      },
      "num_medications": {
        "description": "Number of distinct generic names administered during the encounter",
        "units": null
      },
      "num_procedures": {
        "description": "Number of procedures (other than lab tests) performed during the encounter",
        "units": null
      },
      "number_diagnoses": {
        "description": "Number of diagnoses entered to the system",
        "units": null
      },
      "number_emergency": {
        "description": "Number of emergency visits of the patient in the year preceding the encounter",
        "units": null
      },
      "number_inpatient": {
        "description": "Number of inpatient visits of the patient in the year preceding the encounter",
        "units": null
      },
      "number_outpatient": {
        "description": "Number of outpatient visits of the patient in the year preceding the encounter",
        "units": null
      },
      "payer_code": {
        "description": "Integer identifier corresponding to 23 distinct values, for example, Blue Cross/Blue Shield, Medicare, and self-pay",
        "units": null
      },
      "pioglitazone": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "race": {
        "description": "Values: Caucasian, Asian, African American, Hispanic, and other",
        "units": null
      },
      "repaglinide": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "rosiglitazone": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "time_in_hospital": {
        "description": "Integer number of days between admission and discharge",
        "units": null
      },
      "tolazamide": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "tolbutamide": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "troglitazone": {
        "description": "The feature indicates whether the drug was prescribed or there was a change in the dosage. Values: up if the dosage was increased during the encounter, down if the dosage was decreased, steady if the dosage did not change, and no if the drug was not prescribed",
        "units": null
      },
      "weight": {
        "description": "Weight in pounds.",
        "units": null
      }
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `no`，对应选项：

```json
"No recorded readmission within 30 days"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "readmission_30d:uci_diabetes:72821", "choice": "no"}
```

### 样例溯源

[上游资源](https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip) · [数据集说明](../datasets/uci_diabetes.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "csv_row": 72822,
    "supporting_resources": [
      "uci_diabetes__metadata.json"
    ],
    "zip_member": "diabetic_data.csv"
  },
  "material_kind": "structured_clinical_observations",
  "resource": "uci_diabetes__data.zip",
  "resource_sha256": "f82ac129da2ddd2299391ff6fbae3a6a58b3edcf59ac9d7bd480c00fe453112a",
  "resource_url": "https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip",
  "source_id": "uci_diabetes",
  "source_url": "https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008",
  "split": "published_corpus_no_official_split",
  "upstream_group": "82a9d23e825365ccbb206268133c257a03f81510dc1c392ec46ef7f2a7d9142a",
  "upstream_id": "72821",
  "version": "UCI snapshot 2026-10-10; SHA-256 locked"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：no 93 题、yes 7 题。

**[Diabetes 130-US Hospitals for Years 1999-2008](../datasets/uci_diabetes.md)**：The dataset represents ten years (1999-2008) of clinical care at 130 US hospitals and integrated delivery networks. Each row concerns hospital records of patients diagnosed with diabetes, who underwent laboratory, medications, and stayed up to 14 days. The goal is to determine the early readmission of the patient within 30 days of discharge.
The problem is important for the following reasons. Despite high-quality evidence showing improved clinical outcomes for diabetic patients who receive various preventive and therapeutic interventions, many patients do not receive them. This can be partially attributed to arbitrary diabetes management in hospital environments, which fail to attend to glycemic control. Failure to provide proper diabetes care not only increases the managing costs for the hospitals (as the patients are readmitted) but also impacts the morbidity and mortality of the patients, who may face complications associated with diabetes. 答案依据：按患者取首个合格住院；出院去向只保留回家 (1)；readmitted <30 为阳性，其他为未观察到 30 日内再入院。输入移除患者 ID、住院 ID 和再入院标签。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/readmission_30d/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/readmission_30d/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
