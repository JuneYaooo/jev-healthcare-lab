# SciFact

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

科学论文摘要，不全是临床医学。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `scifact` |
| 上游入口 | [发布方页面](https://github.com/allenai/scifact) |
| 收录情况 | 100 题 / 1 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | CC-BY-4.0 AND ODC-By-1.0 |
| 收录语种 | 英语 100 题 |

## 来源与引用

Wadden et al. (2020)

[论文或项目引用](https://aclanthology.org/2020.emnlp-main.609/) · [数据许可](https://github.com/allenai/scifact/blob/master/LICENSE.md)

许可与说明快照：[LICENSE.md](../../benchmarks/medical_decision_v1/sources/scifact/LICENSE.md) · [README.md](../../benchmarks/medical_decision_v1/sources/scifact/README.md)

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [研究论断证据关系](../tasks/claim_support.md) | 100 | 给定论断与被引摘要，判断支持、反驳或证据不足。 |

## 答案与格式转换

原始 claim evidence 标签；无该文证据标注记为未标注支持或反驳。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`claim_support:scifact:232:10536636`；语种：英语；来源组：`scifact:10536636`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "CONTRADICT": "Contradicts the claim",
        "NOT_ENOUGH_INFO": "No annotated support or contradiction in this abstract",
        "SUPPORT": "Supports the claim"
      },
      "instructions": "给定论断与被引摘要，判断支持、反驳或证据不足。",
      "type": "choice"
    }
  },
  "state": {
    "abstract": "Background Blindness and low vision are thought to be common in southern Sudan. However, the magnitude and geographical distribution are largely unknown. We aimed to estimate the prevalence of blindness and low vision, identify the main causes of blindness and low vision, and estimate targets for blindness prevention programs in Mankien payam (district), southern Sudan.",
    "claim": "Cataract and trachoma are the primary cause of blindness in Southern Sudan.",
    "title": "Prevalence and Causes of Blindness and Low Vision in Southern Sudan "
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `NOT_ENOUGH_INFO`，对应选项：

```json
"No annotated support or contradiction in this abstract"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "claim_support:scifact:232:10536636", "choice": "NOT_ENOUGH_INFO"}
```

### 样例溯源

[上游资源](https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz) · [数据集说明](../datasets/scifact.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0 AND ODC-By-1.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "claim_id": 232,
    "doc_id": "10536636"
  },
  "material_kind": "scientific_literature",
  "resource": "scifact__data.tar.gz",
  "resource_sha256": "11c621288d41ac144d29b13b0f8503b3820b7d6e8b1f6ff24dff335c196d76be",
  "resource_url": "https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz",
  "source_id": "scifact",
  "source_url": "https://github.com/allenai/scifact",
  "split": "official_dev_document_disjoint_from_upstream_train",
  "upstream_group": "10536636",
  "upstream_id": "232:10536636",
  "version": "sha256:11c621288d41ac144d29b13b0f8503b3820b7d6e8b1f6ff24dff335c196d76be"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[研究论断证据关系](../tasks/claim_support.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
