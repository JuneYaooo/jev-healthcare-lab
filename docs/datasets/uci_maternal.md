# Maternal Health Risk

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

Data has been collected from different hospitals, community clinics, maternal health cares from the rural areas of Bangladesh through the IoT based risk monitoring system.

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `uci_maternal` |
| 上游入口 | [发布方页面](https://archive.ics.uci.edu/dataset/863/maternal+health+risk) |
| 收录情况 | 100 题 / 1 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 100 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 英语 100 题 |

## 来源与引用

Marzia Ahmed

[论文或项目引用](https://doi.org/10.24432/C5DP5D) · [数据许可](https://creativecommons.org/licenses/by/4.0/)

许可与说明快照：[metadata.json](../../benchmarks/medical_decision_v1/sources/uci_maternal/metadata.json) · [source-page.html](../../benchmarks/medical_decision_v1/sources/uci_maternal/source-page.html)

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [孕产记录风险标签分类](../tasks/maternal_risk.md) | 辅助评测（不计临床主分数） | 100 | 根据孕产记录的年龄与生命体征，选择发布数据标注的低、中、高风险；不等同经过验证的母婴结局预测。 |

## 答案与格式转换

沿用原 RiskLevel，不能当成独立结局随访；完全相同特征冲突全部排除，无患者 ID。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

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

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[孕产记录风险标签分类](../tasks/maternal_risk.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
