# Heart Failure Clinical Records

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

This dataset contains the medical records of 299 patients who had heart failure, collected during their follow-up period, where each patient profile has 13 clinical features.

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `uci_heart_failure` |
| 上游入口 | [发布方页面](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records) |
| 收录情况 | 100 题 / 1 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 英语 100 题 |

## 来源与引用

Ahmad et al.; Chicco and Jurman; UCI

[论文或项目引用](https://doi.org/10.24432/C5Z89R) · [数据许可](https://creativecommons.org/licenses/by/4.0/)

许可与说明快照：[metadata.json](../../benchmarks/medical_decision_v1/sources/uci_heart_failure/metadata.json) · [source-page.html](../../benchmarks/medical_decision_v1/sources/uci_heart_failure/source-page.html)

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [90 日死亡结局预测](../tasks/mortality_90d.md) | 100 | 根据基线心衰记录预测 90 日内死亡；不提供随访长度；90 日前无死亡但失访者已排除。 |

## 答案与格式转换

90 日死亡：time<=90 且 DEATH_EVENT=1 为阳性；time>=90 且无此前死亡为阴性；90 日前删失排除。time 与死亡标签不输入。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

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

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[90 日死亡结局预测](../tasks/mortality_90d.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
