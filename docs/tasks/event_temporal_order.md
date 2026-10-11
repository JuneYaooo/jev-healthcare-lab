# 临床事件先后关系

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

给定病例和两个事件，选择第一个相对第二个的原始先于、晚于或重叠关系。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `event_temporal_order` |
| 医疗场景 | 诊断与鉴别 |
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

题目 ID：`event_temporal_order:maccrobat:28292056.ann:T26:T27`；语种：英语；来源组：`maccrobat:28292056`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "AFTER": "After",
        "BEFORE": "Before",
        "OVERLAP": "Overlaps"
      },
      "instructions": "给定病例和两个事件，选择第一个相对第二个的原始先于、晚于或重叠关系。",
      "type": "choice"
    }
  },
  "state": {
    "case_report": "We report the case of a 68-year-old female with no past medical history, presented with an upper gastrointestinal bleeding and pain in left upper abdomen.\nPhysical examination found a splenomegaly and signs of portosystemic collateral formation including abdominal wall dilated veins and rectal haemorrhoids.\nNo biological abnormalities were noted besides those due to hypersplenism (anaemia and thrombocytopenia).\nThe patient underwent upper gastrointestinal endoscopy that showed stage III oesophageal varices with portal hypertensive gastropathy and red signs.\nUltrasonography revealed a fusiform dilatation of the portal bifurcation measuring 40 mm in diameter with dilated branches; no signs of portal thrombosis were detected (Figure 1).\nThe portal Doppler study showed a normal hepatopetal flow.\nOther signs of portal hypertension were found, including splenomegaly, repermeation of the umbilical vein and a splenorenal collateral circulation.\nA complementary angio-CT allowed a better assessment of the portal system that contained some thin calcifications in the aneurysmal wall and the main portal trunk (Figure 2, Figure 3, Figure 4).\nOther signs of portal hypertension were noted such as oesophageal and gastric varices, parietal collateral circulation associated to ultrasonography findings.\nLiver cirrhosis was confirmed by transcient elastometry and biopsy.\n",
    "event_1": {
      "end": 579,
      "start": 564,
      "text": "Ultrasonography"
    },
    "event_2": {
      "end": 610,
      "start": 591,
      "text": "fusiform dilatation"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `OVERLAP`，对应选项：

```json
"Overlaps"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "event_temporal_order:maccrobat:28292056.ann:T26:T27", "choice": "OVERLAP"}
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
    "annotation_kind": "BEFORE/AFTER relation or explicit OVERLAP set",
    "event_1": "T26",
    "event_2": "T27",
    "zip_member": "28292056.ann"
  },
  "material_kind": "published_clinical_case_reports",
  "resource": "maccrobat__MACCROBAT2020.zip",
  "resource_sha256": "a2d34ccd1a605d9147fc7368293e61dcf2090357b26f7bce6c2b3d257204acc6",
  "resource_url": "https://ndownloader.figshare.com/files/21489405",
  "source_id": "maccrobat",
  "source_url": "https://doi.org/10.6084/m9.figshare.9764942.v2",
  "split": "published_corpus_no_official_split",
  "upstream_group": "28292056",
  "upstream_id": "28292056.ann:T26:T27",
  "version": "figshare.9764942.v2/MACCROBAT2020"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：AFTER 34 题、BEFORE 33 题、OVERLAP 33 题。

**[MACCROBAT2020](../datasets/maccrobat.md)**：公开发表的临床病例报告；原病例被编辑整理，不等同医院原始 EHR。 答案依据：原始 BRAT MODIFY 关系；把事件引用解析为文本实体，只保留目标检查/药物唯一的关联。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/event_temporal_order/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/event_temporal_order/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
