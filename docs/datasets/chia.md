# Chia

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

真实 Phase IV 试验入排标准；无患者临床记录。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `chia` |
| 上游入口 | [发布方页面](https://doi.org/10.6084/m9.figshare.11855817) |
| 收录情况 | 300 题 / 3 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 英语 300 题 |

## 来源与引用

Kury et al. (2020)

[论文或项目引用](https://doi.org/10.1038/s41597-020-00620-0) · [数据许可](https://creativecommons.org/licenses/by/4.0/)

许可与说明快照：[figshare-metadata.json](../../benchmarks/medical_decision_v1/sources/chia/figshare-metadata.json)

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [入排条件与或关系](../tasks/criterion_boolean.md) | 100 | 给定条件中的两个标注要素，判断原文要求 AND 还是 OR。 |
| [入排条件要素分类](../tasks/criterion_entity_type.md) | 100 | 给定条件原文与目标实体，判断原标注的要素类别。 |
| [入排条件限定关系](../tasks/criterion_relation.md) | 100 | 给定已标注关联的两个要素，判断数值、时间、限定等关系类型。 |

## 答案与格式转换

医学专业人员的 BRAT 实体与关系；只转换已有标签，不合成患者。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`criterion_boolean:chia:NCT00440245_exc.ann:OR-0-T1-T2`；语种：英语；来源组：`chia:NCT00440245`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "AND": "AND",
        "OR": "OR"
      },
      "instructions": "给定条件中的两个标注要素，判断原文要求 AND 还是 OR。",
      "type": "choice"
    }
  },
  "state": {
    "criteria_text": "asthma and COPD\r\n",
    "entity_1": {
      "end": 6,
      "start": 0,
      "text": "asthma"
    },
    "entity_2": {
      "end": 15,
      "start": 11,
      "text": "COPD"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `OR`，对应选项：

```json
"OR"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "criterion_boolean:chia:NCT00440245_exc.ann:OR-0-T1-T2", "choice": "OR"}
```

### 样例溯源

[上游资源](https://ndownloader.figshare.com/files/21728853) · [数据集说明](../datasets/chia.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "entity_ids": [
      "T1",
      "T2"
    ],
    "relation_id": "OR-0-T1-T2",
    "zip_member": "NCT00440245_exc.ann"
  },
  "material_kind": "clinical_trial_registry",
  "resource": "chia_without_scope.zip",
  "resource_sha256": "723457a4eb0ad57ac352b4976d1cdfc81b96e36233906474dc9c845cdc759c7c",
  "resource_url": "https://ndownloader.figshare.com/files/21728853",
  "source_id": "chia",
  "source_url": "https://doi.org/10.6084/m9.figshare.11855817",
  "split": "published_corpus_no_official_split",
  "upstream_group": "NCT00440245",
  "upstream_id": "NCT00440245_exc.ann:OR-0-T1-T2",
  "version": "figshare:11855817.v2"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[入排条件与或关系](../tasks/criterion_boolean.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
