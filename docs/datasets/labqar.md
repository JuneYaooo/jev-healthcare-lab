# LabQAR

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

根据专家医学参考资料整理的区间与条件；Set 2 数值由作者构造，不是真实患者检验结果。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `labqar` |
| 上游入口 | [发布方页面](https://doi.org/10.6084/m9.figshare.29189894) |
| 收录情况 | 172 题 / 2 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 172 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 英语 172 题 |

## 来源与引用

Bhasuran, Jin, Deville et al., A Curated Dataset for Question Answering on Laboratory Test Reference Ranges and Interpretation. Scientific Data (2026); Figshare 29189894 v1.

[论文或项目引用](https://doi.org/10.1038/s41597-026-07554-z) · [数据许可](https://creativecommons.org/licenses/by/4.0/) · [补充核验依据](https://doi.org/10.6084/m9.figshare.29189894)

许可与说明快照：[LabQAR_README.md](../../benchmarks/medical_decision_v1/sources/labqar/LabQAR_README.md) · [figshare-metadata.json](../../benchmarks/medical_decision_v1/sources/labqar/figshare-metadata.json)

### 使用限制

仅评估给定参考条目的人群、标本和条件匹配；不是独立诊疗知识或所有实验室范围的正确性。本版 72 题，未覆盖不确定和检验方法差异。 新增 Set 2 任务只测给定区间的数值判读，不推断诊断、危急值或处置优先级。

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [按给定区间判读检验值高低](../tasks/lab_value_classification.md) | 辅助评测（不计临床主分数） | 100 | 根据题目给出的检验值和参考区间，选择原始选项中的 High、Normal 或 Low；仅按给定区间判读，不推断诊断或危急程度。 |
| [给定参考表的区间匹配](../tasks/reference_range.md) | 辅助评测（不计临床主分数） | 72 | 给定区间及人群、方法条件，选择适用区间或不确定。 |

## 答案与格式转换

原 Set 1 范围答案机械映射为同检验、单位、类别的固定候选；输入附上同组原参考条目，考查条件匹配。排除同条件答案冲突、裸数值及无替代范围条目；不生成范围或不确定答案。 Set 2 保留原 High/Normal/Low 选项与答案；仅收两端有限且有序的区间，排除边界相等、数值无法解析及原答案与给定区间不一致的题。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`lab_value_classification:labqar:103`；语种：英语；来源组：`labqar:set2:C3 complement`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "Low",
        "B": "Normal",
        "C": "High"
      },
      "instructions": "根据题目给出的检验值和参考区间，选择原始选项中的 High、Normal 或 Low；仅按给定区间判读，不推断诊断或危急程度。",
      "type": "choice"
    }
  },
  "state": {
    "provided_reference_interval": {
      "lower_bound": 1.2,
      "unit": "g/L",
      "upper_bound": 1.5
    },
    "question": "For the lab test 'C3 complement' measuring in 'g/L' in Specimen 'Serum' for 'any gender' and 'any age group', a value in 'SI reference range' is 1.87. Is the lab test result?"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `C`，对应选项：

```json
"High"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "lab_value_classification:labqar:103", "choice": "C"}
```

### 样例溯源

[上游资源](https://ndownloader.figshare.com/files/61820644) · [数据集说明](../datasets/labqar.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "json_index": 102,
    "upstream_id": 103
  },
  "material_kind": "curated_reference_rules",
  "resource": "labqar__Set_2.json",
  "resource_sha256": "970f18f45679db9e39ec2df7f231566acaaf8b8e1a0d11accbf8d6e6058a2158",
  "resource_url": "https://ndownloader.figshare.com/files/61820644",
  "source_id": "labqar",
  "source_url": "https://doi.org/10.6084/m9.figshare.29189894",
  "split": "published_corpus_reserved_for_evaluation",
  "upstream_group": "set2:C3 complement",
  "upstream_id": "103",
  "version": "Figshare 29189894 v1"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[按给定区间判读检验值高低](../tasks/lab_value_classification.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
