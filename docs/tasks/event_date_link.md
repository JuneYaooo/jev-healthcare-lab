# 文本事件与时间表达关联

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 把已有事件和时间提及配对，不决定检查或治疗时点。

## 任务是什么

给定病例和时间表达，从原文事件候选中选择原时间关联标注的唯一目标；若提供关系类型，按该方向解释。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `event_date_link` |
| 医疗场景 | 诊断与鉴别 |
| 能力维度 | 关联与匹配 |
| 评测类别 | 文本理解与标注 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 47 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可部分 15 题、非商业研究附加集 85 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [E3C English Layer 1](../datasets/e3c.md) | 85 | [原始来源](https://github.com/hltfbk/E3C-Corpus) |
| [MACCROBAT2020](../datasets/maccrobat.md) | 15 | [原始来源](https://doi.org/10.6084/m9.figshare.9764942.v2) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`event_date_link:e3c:EN105094:1982`；语种：英语；来源组：`e3c:EN105094`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "1567": "present [characters 3:10]",
        "1582": "jaundice [characters 68:76]",
        "1597": "tests [characters 89:94]",
        "1612": "revealed [characters 95:103]",
        "1627": "levels [characters 153:159]",
        "1642": "scan [characters 184:188]",
        "1657": "showed [characters 189:195]",
        "1672": "mass [characters 219:223]",
        "1687": "obstructing [characters 224:235]",
        "1702": "results [characters 262:269]",
        "1717": "consistent [characters 293:303]",
        "1732": "papilloma [characters 329:338]",
        "1747": "features [characters 390:398]",
        "1762": "tumor [characters 460:465]",
        "1777": "discussion [characters 482:492]",
        "1792": "resection [characters 538:547]",
        "1807": "examination [characters 604:615]",
        "1822": "confirmed [characters 616:625]",
        "1837": "adenoma [characters 636:643]",
        "1852": "course [characters 673:679]",
        "1867": "uneventful [characters 684:694]"
      },
      "instructions": "给定病例和时间表达，从原文事件候选中选择原时间关联标注的唯一目标；若提供关系类型，按该方向解释。",
      "type": "choice"
    }
  },
  "state": {
    "annotated_relation_types": [
      "SIMULTANEOUS"
    ],
    "case_report": "We present a case of a 77-year-old Caucasian woman with obstructive jaundice. Laboratory tests revealed that she had elevated bilirubin and liver enzyme levels. A computed tomographic scan showed a homogeneous 5 × 3-cm mass obstructing the common bile duct. The results of brush cytology were consistent with a bile duct villous papilloma. However, on the basis of the tumor's radiological features, a preliminary diagnosis of extrahepatic bile duct malignant tumor was made. After discussion among the multidisciplinary team, a surgical resection of the bile duct tumor was performed. Histopathological examination confirmed a villous adenoma. The patient's postoperative course was uneventful.\r\n",
    "target": {
      "end": 672,
      "start": 659,
      "text": "postoperative"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `1852`，对应选项：

```json
"course [characters 673:679]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "event_date_link:e3c:EN105094:1982", "choice": "1852"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/hltfbk/E3C-Corpus/8196181eacd5d65828d324dcc63970c503aff5e9/data_annotation/English/layer1/EN105094.xml) · [数据集说明](../datasets/e3c.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-NC (publisher does not specify version)",
  "distribution": "research_noncommercial",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "relation_attribute": "timexLink",
    "supporting_resources": [
      "e3c__train_test_split.txt"
    ],
    "target_xmi_id": "1852",
    "xmi_id": "1982"
  },
  "material_kind": "published_clinical_case_reports",
  "resource": "e3c__EN105094.xml",
  "resource_sha256": "f2bffebfc3e91f05125afe34a29760eb647fd2f371ceac31977d840c9afc6e9f",
  "resource_url": "https://raw.githubusercontent.com/hltfbk/E3C-Corpus/8196181eacd5d65828d324dcc63970c503aff5e9/data_annotation/English/layer1/EN105094.xml",
  "source_id": "e3c",
  "source_url": "https://github.com/hltfbk/E3C-Corpus",
  "split": "official_test",
  "upstream_group": "EN105094",
  "upstream_id": "EN105094:1982",
  "version": "8196181eacd5d65828d324dcc63970c503aff5e9"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：10344 1 题、10374 1 题、10603 1 题、10734 1 题、1644 1 题、1659 1 题、1777 1 题、1852 1 题、1888 1 题、1889 1 题、1914 1 题、1934 1 题、1979 1 题、2039 1 题、2068 1 题、2309 1 题、2472 1 题、2652 1 题、2680 1 题、2757 1 题、2830 1 题、3219 1 题、3294 2 题、3553 1 题、3920 1 题、3980 1 题、4205 1 题、4310 1 题、4325 1 题、4340 1 题、4445 1 题、4639 1 题、4984 1 题、5041 1 题、5074 1 题、5250 1 题、5267 1 题、5277 1 题、5292 1 题、5337 1 题、5493 1 题、5656 1 题、5796 1 题、5941 1 题、5956 1 题、6781 1 题、6826 2 题、6841 1 题、6920 1 题、7419 1 题、7546 1 题、7569 1 题、7644 1 题、7687 1 题、7807 1 题、7849 1 题、8014 1 题、8021 1 题、8059 1 题、8081 1 题、8389 1 题、8505 1 题、8535 1 题、8550 1 题、8600 1 题、8713 1 题、8719 1 题、8758 1 题、8779 1 题、8925 1 题、8926 1 题、8941 1 题、8945 1 题、8959 1 题、9064 1 题、9133 1 题、9253 1 题、9259 1 题、9523 1 题、9529 1 题、9538 1 题、9556 1 题、9990 1 题、T10 1 题、T115 1 题、T122 2 题、T14 1 题、T19 1 题、T35 1 题、T41 1 题、T5 1 题、T50 2 题、T51 1 题、T60 1 题、T63 1 题、T68 1 题。

**[E3C English Layer 1](../datasets/e3c.md)**：公开病例报道；Layer 1 人工事件与时间标注。保留各文献原作者、DOI、原文许可。 答案依据：仅官方英文测试文档；原 docTimeRel、permanence、TIMEX3 类型及 timexLink 唯一目标机械适配，不使用自动标注层。

**[MACCROBAT2020](../datasets/maccrobat.md)**：公开发表的临床病例报告；原病例被编辑整理，不等同医院原始 EHR。 答案依据：原始 BRAT MODIFY 关系；把事件引用解析为文本实体，只保留目标检查/药物唯一的关联。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/event_date_link/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/event_date_link/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
