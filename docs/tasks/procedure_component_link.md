# 子操作与所属操作关联

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

给定病例和子操作片段，从原文操作候选中选择原 SUB_PROCEDURE 唯一关联的所属操作。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `procedure_component_link` |
| 医疗场景 | 住院与护理 |
| 能力维度 | 关联与匹配 |
| 决策类型 | 材料判断 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可核心集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [MACCROBAT2020](../datasets/maccrobat.md) | 100 | [原始来源](https://doi.org/10.6084/m9.figshare.9764942.v2) |

## 如何作答与评分

根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`procedure_component_link:maccrobat:23077697.ann:T56`；语种：英语；来源组：`maccrobat:23077697`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "T14": "Physical examination [characters 110:130]",
        "T26": "resection [characters 440:449]",
        "T27": "histological examinations [characters 455:480]",
        "T33": "Lumpectomy [characters 636:646]",
        "T35": "Histopathological examinatio [characters 659:687]",
        "T51": "immunohistochemical analysis [characters 1138:1166]",
        "T53": "anti-CK7 [characters 1189:1197]",
        "T54": "AE1/AE3 [characters 1210:1217]",
        "T55": "anti CEA [characters 1237:1245]",
        "T9": "Radiotherapy [characters 1393:1405]"
      },
      "instructions": "给定病例和子操作片段，从原文操作候选中选择原 SUB_PROCEDURE 唯一关联的所属操作。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_text": "A 76-year old woman presented with a 24-month history of enlarging mass involving the back history of trauma.\nPhysical examination showed a mass of an 3x4 cm in diameter, localized in the right inter-scapular region.\nThe mass was ulcerative helophytic, grayish in colour, hard in consistency and easily bleeding on manipulation.\nThe remainder of the examination was unremarkable; no lymphadenopathy and no abdominal masses were felt.\nAfter resection, the histological examinations of the specimens have concluded for basal cell carcinoma.\nA local recurrence was observed 18 months later; the patient was admitted to our institution for Lumpectomy (Figure 1).\nHistopathological examination revealed a syringomatous pattern infiltrating the dermis (Figure 2, Figure 3), subcutis and skeletal muscle.\nThe neoplastic epithelial cells were arranged in interconnecting cords with microcystic areas.\nNests, cords, and tubules of the tumour extended into the dermis and into the adjacent muscle.\nMany lobules showed squamous differentiation.\nSclerosis of stroma around the cords was present.\nTumour cells were not connected to the epidermis.\nThe immunohistochemical analysis showed positivity for anti-CK7 (Figure 4), AE1/AE3 and negativity for anti CEA and anti CK20.\nBased upon her histological and immunohistochemical presentation, the diagnosis of syringomatous eccrine carcinoma was established.\nRadiotherapy of the involved area was performed (70 Gy, 35 sessions)\n",
    "target": {
      "end": 1259,
      "start": 1250,
      "text": "anti CK20"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `T51`，对应选项：

```json
"immunohistochemical analysis [characters 1138:1166]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "procedure_component_link:maccrobat:23077697.ann:T56", "choice": "T51"}
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
    "answer_entity_id": "T51",
    "direction_reversed": false,
    "query_entity_id": "T56",
    "relation_ids": [
      "R30"
    ],
    "zip_member": "23077697.ann"
  },
  "material_kind": "published_clinical_case_reports",
  "resource": "maccrobat__MACCROBAT2020.zip",
  "resource_sha256": "a2d34ccd1a605d9147fc7368293e61dcf2090357b26f7bce6c2b3d257204acc6",
  "resource_url": "https://ndownloader.figshare.com/files/21489405",
  "source_id": "maccrobat",
  "source_url": "https://doi.org/10.6084/m9.figshare.9764942.v2",
  "split": "published_corpus_no_official_split",
  "upstream_group": "23077697",
  "upstream_id": "23077697.ann:T56",
  "version": "figshare.9764942.v2/MACCROBAT2020"
}
```

该题的格式转换说明：

All valid entities of prespecified candidate types; unique explicit relation; no invented negatives.

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：T105 1 题、T107 1 题、T110 1 题、T111 1 题、T113 1 题、T114 1 题、T115 1 题、T116 1 题、T118 1 题、T126 1 题、T142 1 题、T15 1 题、T150 1 题、T152 1 题、T153 1 题、T166 1 题、T188 1 题、T20 2 题、T21 1 题、T22 2 题、T26 3 题、T27 1 题、T28 1 题、T30 2 题、T31 1 题、T33 2 题、T35 1 题、T36 1 题、T37 2 题、T42 2 题、T43 2 题、T44 1 题、T45 1 题、T48 1 题、T49 1 题、T5 1 题、T51 3 题、T52 1 题、T53 3 题、T57 3 题、T58 1 题、T61 2 题、T63 2 题、T64 1 题、T65 1 题、T66 2 题、T68 1 题、T70 1 题、T71 1 题、T72 1 题、T73 1 题、T74 3 题、T76 1 题、T77 1 题、T78 1 题、T79 1 题、T80 1 题、T81 1 题、T82 1 题、T84 2 题、T85 1 题、T87 1 题、T88 1 题、T90 1 题、T91 1 题、T92 2 题、T93 4 题、T94 1 题、T97 3 题、T98 2 题、T99 2 题。

**[MACCROBAT2020](../datasets/maccrobat.md)**：公开发表的临床病例报告；原病例被编辑整理，不等同医院原始 EHR。 答案依据：原始 BRAT MODIFY 关系；把事件引用解析为文本实体，只保留目标检查/药物唯一的关联。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/procedure_component_link/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/procedure_component_link/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
