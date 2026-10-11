# E3C English Layer 1

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

公开病例报道；Layer 1 人工事件与时间标注。保留各文献原作者、DOI、原文许可。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `e3c` |
| 上游入口 | [发布方页面](https://github.com/hltfbk/E3C-Corpus) |
| 收录情况 | 385 题 / 4 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 385 题 |
| 使用范围 | 非商业研究附加集 |
| 登记的数据许可 | CC-BY-NC (publisher does not specify version) |
| 收录语种 | 英语 385 题 |

## 来源与引用

Magnini et al.; Fondazione Bruno Kessler

[论文或项目引用](https://e3c.fbk.eu/home) · [数据许可](https://github.com/hltfbk/E3C-Corpus/blob/8196181eacd5d65828d324dcc63970c503aff5e9/README.md)

许可与说明快照：[README.md](../../benchmarks/medical_decision_v1/sources/e3c/README.md) · [train_test_split.txt](../../benchmarks/medical_decision_v1/sources/e3c/train_test_split.txt)

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [临床文本时间表达分类](../tasks/clinical_time_type.md) | 辅助评测（不计临床主分数） | 100 | 给定病例及时间片段，选择原 E3C TIMEX3 类别：时长、周期集合、日期、数量时间或前后表达。 |
| [文本事件与时间表达关联](../tasks/event_date_link.md) | 辅助评测（不计临床主分数） | 85 | 给定病例和时间表达，从原文事件候选中选择原时间关联标注的唯一目标；若提供关系类型，按该方向解释。 |
| [文本事件持续性分类](../tasks/event_permanence.md) | 辅助评测（不计临床主分数） | 100 | 给定病例及事件片段，选择原 E3C 持续性标注 FINITE 或 PERMANENT；不把它解释为新的慢病诊断。 |
| [临床事件相对记录时间标注](../tasks/temporality.md) | 辅助评测（不计临床主分数） | 100 | 给定病例原文、文档时间和事件片段，选择原 E3C docTimeRel 时间关系。 |

## 答案与格式转换

仅官方英文测试文档；原 docTimeRel、permanence、TIMEX3 类型及 timexLink 唯一目标机械适配，不使用自动标注层。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

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

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[文本事件持续性分类](../tasks/event_permanence.md)。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [病历诊断记录状态核对](../tasks/diagnosis_verification.md) | 区分疑似、确诊、排除与未明确。 |
| [医疗操作记录状态核对](../tasks/procedure_progress.md) | 区分计划、进行、完成、取消及目标未达成。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
