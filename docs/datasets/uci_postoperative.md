# Post-Operative Patient

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

Dataset of patient features

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `uci_postoperative` |
| 上游入口 | [发布方页面](https://archive.ics.uci.edu/dataset/82/post+operative+patient) |
| 收录情况 | 68 题 / 1 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 英语 68 题 |

## 来源与引用

Sharon Summers, Linda Woolery

[论文或项目引用](https://doi.org/10.24432/C5DG6Q) · [数据许可](https://creativecommons.org/licenses/by/4.0/)

许可与说明快照：[metadata.json](../../benchmarks/medical_decision_v1/sources/uci_postoperative/metadata.json) · [source-page.html](../../benchmarks/medical_decision_v1/sources/uci_postoperative/source-page.html)

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [术后转归去向选择](../tasks/postoperative_disposition.md) | 68 | 给定术后恢复指标，选择原记录的 ICU、普通病房或回家去向。历史记录选择不等于临床最优决策。 |

## 答案与格式转换

ADM-DECS 原术后去向标签；相同输入冲突全部排除，无患者 ID，不冒称患者独立。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

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

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[术后转归去向选择](../tasks/postoperative_disposition.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
