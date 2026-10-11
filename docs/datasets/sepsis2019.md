# PhysioNet Challenge 2019

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

真实 ICU 小时记录；只使用公开训练医院 A 中按固定哈希预选的 1,000 个来源记录，非官方隐藏测试。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `sepsis2019` |
| 上游入口 | [发布方页面](https://physionet.org/content/challenge-2019/1.0.0/) |
| 收录情况 | 100 题 / 1 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 100 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 英语 100 题 |

## 来源与引用

Reyna et al. (2019), Early Prediction of Sepsis From Clinical Data: The PhysioNet/Computing in Cardiology Challenge 2019; PhysioNet v1.0.0, doi:10.13026/v64v-d857.

[论文或项目引用](https://doi.org/10.1097/CCM.0000000000004145) · [数据许可](https://physionet.org/content/challenge-2019/view-license/1.0.0/) · [补充核验依据](https://physionet.org/content/challenge-2019/1.0.0/)

许可与说明快照：[LICENSE.txt](../../benchmarks/medical_decision_v1/sources/sepsis2019/LICENSE.txt) · [source-page.html](../../benchmarks/medical_decision_v1/sources/sepsis2019/source-page.html) · [preselection.json](../../benchmarks/medical_decision_v1/sources/sepsis2019/preselection.json) · [selection_frame.json](../../benchmarks/medical_decision_v1/sources/sepsis2019/selection_frame.json)

### 使用限制

本子集仅有 11 个阳性、89 个阴性；恒答阴性准确率为 89%，应同时报告两类召回。来源是公开训练医院 A，不能对训练过该库的模型声称盲测。选择框为 1,000 例，合格 528 例（11 阳性/517 阴性）；分层抽样改变了类别比例，不用于风险校准、临床患病率或 PPV 估计。推算起病和原挑战逐小时 utility 不等价。

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [脓毒症发生风险预测](../tasks/deterioration_prediction.md) | 辅助评测（不计临床主分数） | 100 | 仅使用 ICU 前 12 小时的记录，判断按挑战定义的脓毒症起病是否发生在第 12 小时之后至第 24 小时（含）。 |

## 答案与格式转换

原 SepsisLabel 提前 6 小时。首次 1 所在小时加 6 得到挑战定义起病小时。要求完整 ICU 第 1–12 小时，随访至起病或第 24 小时；排除起始即阳性、12 小时内起病、非法序列及随访不足。只给前 12 小时，预测 (12,24] 小时起病。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

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

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[脓毒症发生风险预测](../tasks/deterioration_prediction.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
