# 文本事件持续性分类

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 复制 FINITE/PERMANENT 属性，不判断慢病诊断或长期预后。

## 任务是什么

给定病例及事件片段，选择原 E3C 持续性标注 FINITE 或 PERMANENT；不把它解释为新的慢病诊断。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `event_permanence` |
| 医疗场景 | 住院与护理 |
| 能力维度 | 事实与状态 |
| 评测类别 | 文本理解与标注 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 48 |
| 语种 | 英语 100 题 |
| 数据范围 | 非商业研究附加集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [E3C English Layer 1](../datasets/e3c.md) | 100 | [原始来源](https://github.com/hltfbk/E3C-Corpus) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。固定语义标签计算准确率、宏 F1、召回与混淆矩阵。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`event_permanence:e3c:EN107423:1670`；语种：英语；来源组：`e3c:EN107423`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "FINITE": "Finite",
        "PERMANENT": "Permanent"
      },
      "instructions": "给定病例及事件片段，选择原 E3C 持续性标注 FINITE 或 PERMANENT；不把它解释为新的慢病诊断。",
      "type": "choice"
    }
  },
  "state": {
    "case_report": "A 16-year-old Indian boy presented to our hospital with a history of a lump in the lower back region since birth. Initially, it was small, but its size increased gradually over time to a size of 15 cm × 15 cm at presentation. There were no other associated abnormalities. Investigations revealed the lump to be a benign cystic teratoma. The patient underwent surgery, and the whole tumor, from its base to the vertebrae, was excised. Bisection of the tumor revealed that it contained hair and pultaceous material consistent with a teratoma, which was later confirmed by histopathologic examination.\n",
    "target": {
      "end": 443,
      "start": 434,
      "text": "Bisection"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `FINITE`，对应选项：

```json
"Finite"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "event_permanence:e3c:EN107423:1670", "choice": "FINITE"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/hltfbk/E3C-Corpus/8196181eacd5d65828d324dcc63970c503aff5e9/data_annotation/English/layer1/EN107423.xml) · [数据集说明](../datasets/e3c.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-NC (publisher does not specify version)",
  "distribution": "research_noncommercial",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "attribute": "permanence",
    "supporting_resources": [
      "e3c__train_test_split.txt"
    ],
    "utf16_begin": 434,
    "utf16_end": 443,
    "xmi_id": "1670"
  },
  "material_kind": "published_clinical_case_reports",
  "resource": "e3c__EN107423.xml",
  "resource_sha256": "52358b98869a9386d5bd896eeae7c721f5f3a7e2216c4070297a5c2cf7482eda",
  "resource_url": "https://raw.githubusercontent.com/hltfbk/E3C-Corpus/8196181eacd5d65828d324dcc63970c503aff5e9/data_annotation/English/layer1/EN107423.xml",
  "source_id": "e3c",
  "source_url": "https://github.com/hltfbk/E3C-Corpus",
  "split": "official_test",
  "upstream_group": "EN107423",
  "upstream_id": "EN107423:1670",
  "version": "8196181eacd5d65828d324dcc63970c503aff5e9"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：FINITE 76 题、PERMANENT 24 题。

**[E3C English Layer 1](../datasets/e3c.md)**：公开病例报道；Layer 1 人工事件与时间标注。保留各文献原作者、DOI、原文许可。 答案依据：仅官方英文测试文档；原 docTimeRel、permanence、TIMEX3 类型及 timexLink 唯一目标机械适配，不使用自动标注层。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/event_permanence/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/event_permanence/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
