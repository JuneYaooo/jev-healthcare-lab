# MACCROBAT2020

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

公开发表的临床病例报告；原病例被编辑整理，不等同医院原始 EHR。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `maccrobat` |
| 上游入口 | [发布方页面](https://doi.org/10.6084/m9.figshare.9764942.v2) |
| 收录情况 | 815 题 / 9 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 815 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 英语 815 题 |

## 来源与引用

Caufield et al., MACCROBAT (2019/2020)

[论文或项目引用](https://doi.org/10.6084/m9.figshare.c.4652765.v1) · [数据许可](https://creativecommons.org/licenses/by/4.0/)

许可与说明快照：[figshare-metadata.json](../../benchmarks/medical_decision_v1/sources/maccrobat/figshare-metadata.json)

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [文本事件与解剖部位关联](../tasks/anatomical_site_link.md) | 辅助评测（不计临床主分数） | 100 | 给定病例和临床事件，从原文解剖部位候选中选择原 MODIFY 关系唯一关联的部位。 |
| [剂量片段与药物文本关联](../tasks/dose_link.md) | 辅助评测（不计临床主分数） | 100 | 给定病例全文和剂量片段，从候选药物中选择原始标注关联的药物；不评价剂量是否适宜，也不覆盖频次和途径。 |
| [文本同一事件指代识别](../tasks/event_coreference.md) | 辅助评测（不计临床主分数） | 100 | 给定病例中的目标事件，从原文事件候选中选择原 IDENTICAL 标注唯一关联的同一事件提及。 |
| [文本事件与时间表达关联](../tasks/event_date_link.md) | 辅助评测（不计临床主分数） | 15 | 给定病例和时间表达，从原文事件候选中选择原时间关联标注的唯一目标；若提供关系类型，按该方向解释。 |
| [文本临床事件先后关系](../tasks/event_temporal_order.md) | 辅助评测（不计临床主分数） | 100 | 给定病例和两个事件，选择第一个相对第二个的原始先于、晚于或重叠关系。 |
| [检验结果与项目文本关联](../tasks/lab_link.md) | 辅助评测（不计临床主分数） | 100 | 给定病例全文和已标注的数值结果片段，从候选检查/评估中选择原始标注关联的项目；包含量表，不判断结果是否异常。 |
| [文本操作包含关系识别](../tasks/procedure_component_link.md) | 辅助评测（不计临床主分数） | 100 | 给定病例和子操作片段，从原文操作候选中选择原 SUB_PROCEDURE 唯一关联的所属操作。 |
| [文本事件变化描述识别](../tasks/result_trend.md) | 辅助评测（不计临床主分数） | 100 | 给定病例及事件片段，选择原 TREND 标注的增加、减少或改变；只判断原文描述，不预测未来。 |
| [文本严重程度修饰关联](../tasks/severity_link.md) | 辅助评测（不计临床主分数） | 100 | 给定病例和严重程度片段，从原文事件候选中选择其唯一修饰的事件。 |

## 答案与格式转换

原始 BRAT MODIFY 关系；把事件引用解析为文本实体，只保留目标检查/药物唯一的关联。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`dose_link:maccrobat:21067996.ann:T22`；语种：英语；来源组：`maccrobat:21067996`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "T17": "barium sulfate suspension [characters 317:342]",
        "T20": "iopromide [characters 394:403]"
      },
      "instructions": "给定病例全文和剂量片段，从候选药物中选择原始标注关联的药物；不评价剂量是否适宜，也不覆盖频次和途径。",
      "type": "choice"
    }
  },
  "state": {
    "case_report": "A 41-year-old man with weight loss, nausea, vomiting, and abdominal pain was referred for an abdominal CT scan to rule out intraabdominal pathology.\nA dedicated CT of the abdomen was performed at our institution according to our standard venous phase protocol.\nFollowing ingestion of positive oral contrast material (barium sulfate suspension 2.1% w/v, Mallinckrodt) and injection of 125 ml of iopromide, 300 mg I/mL (Ultravist, Bayer HealthCare), helical CT was obtained with a 65-s delays using a 64-slice GE Lightspeed VCT scanner (GE Medical Systems; Milwaukee, WI).\nAxial sections of the abdomen showed a large (18×22×22 cm) heterogeneous retroperitoneal mass probably arising from the left adrenal gland containing multiple areas of macroscopic fat (Fig.1).\nThe patient had no documented clinical or laboratory evidence of adrenal hormonal excess.\nOn the basis of the clinical history and CT findings, the patient underwent surgical resection of the left adrenal mass, which was found on pathologic examination to represent a low-grade adrenocortical carcinoma.\n",
    "target": {
      "end": 416,
      "start": 405,
      "text": "300 mg I/mL"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `T20`，对应选项：

```json
"iopromide [characters 394:403]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "dose_link:maccrobat:21067996.ann:T22", "choice": "T20"}
```

### 样例溯源

[上游资源](https://ndownloader.figshare.com/files/21489405) · [数据集说明](../datasets/maccrobat.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "linked_entity_id": "T20",
    "modifier_id": "T22",
    "relation_ids": [
      "R13"
    ],
    "zip_member": "21067996.ann"
  },
  "material_kind": "published_clinical_case_reports",
  "resource": "maccrobat__MACCROBAT2020.zip",
  "resource_sha256": "a2d34ccd1a605d9147fc7368293e61dcf2090357b26f7bce6c2b3d257204acc6",
  "resource_url": "https://ndownloader.figshare.com/files/21489405",
  "source_id": "maccrobat",
  "source_url": "https://doi.org/10.6084/m9.figshare.9764942.v2",
  "split": "published_corpus_no_official_split",
  "upstream_group": "21067996",
  "upstream_id": "21067996.ann:T22",
  "version": "figshare.9764942.v2/MACCROBAT2020"
}
```

该题的格式转换说明：

Resolve event IDs to text anchors; unique original MODIFY link; all valid same-type entities are options.

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[剂量片段与药物文本关联](../tasks/dose_link.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
