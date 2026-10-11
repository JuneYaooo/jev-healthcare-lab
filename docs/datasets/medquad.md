# MedQuAD

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

NIH 旗下网站信息形成的问题；不属于真实患者问诊。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `medquad` |
| 上游入口 | [发布方页面](https://github.com/abachaa/MedQuAD) |
| 收录情况 | 100 题 / 1 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 100 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 英语 100 题 |

## 来源与引用

Abacha and Demner-Fushman (2019)

[论文或项目引用](https://doi.org/10.1016/j.jbi.2019.103217) · [数据许可](https://creativecommons.org/licenses/by/4.0/)

许可与说明快照：[LICENSE.txt](../../benchmarks/medical_decision_v1/sources/medquad/LICENSE.txt) · [readme.txt](../../benchmarks/medical_decision_v1/sources/medquad/readme.txt)

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [医疗问句意图分类](../tasks/query_intent.md) | 辅助评测（不计临床主分数） | 100 | 给定医疗问题，判断其信息需求类别。 |

## 答案与格式转换

原 XML 的 question qtype 元数据；不评价原答案临床正确性。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`query_intent:medquad:MedQuAD-577bd37b96c02d1833b2c9eed2de9f96964e96cb/10_MPlus_ADAM_QA/0001440.xml:2`；语种：英语；来源组：`medquad:https://www.nlm.nih.gov/medlineplus/ency/article/000618.htm`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "causes": "causes",
        "complications": "complications",
        "exams and tests": "exams and tests",
        "frequency": "frequency",
        "information": "information",
        "inheritance": "inheritance",
        "outlook": "outlook",
        "prevention": "prevention",
        "research": "research",
        "susceptibility": "susceptibility",
        "symptoms": "symptoms",
        "treatment": "treatment"
      },
      "instructions": "给定医疗问题，判断其信息需求类别。",
      "type": "choice"
    }
  },
  "state": {
    "question": "What causes Erysipelas ?"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `causes`，对应选项：

```json
"causes"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "query_intent:medquad:MedQuAD-577bd37b96c02d1833b2c9eed2de9f96964e96cb/10_MPlus_ADAM_QA/0001440.xml:2", "choice": "causes"}
```

### 样例溯源

[上游资源](https://codeload.github.com/abachaa/MedQuAD/zip/577bd37b96c02d1833b2c9eed2de9f96964e96cb) · [数据集说明](../datasets/medquad.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "original_page": "https://www.nlm.nih.gov/medlineplus/ency/article/000618.htm",
    "qa_pid": "2",
    "zip_member": "MedQuAD-577bd37b96c02d1833b2c9eed2de9f96964e96cb/10_MPlus_ADAM_QA/0001440.xml"
  },
  "material_kind": "authoritative_health_information",
  "resource": "medquad.zip",
  "resource_sha256": "161d948f8ce8f82accca1f5769a512dff2a01af2b3004d48f2b3da2758a38a09",
  "resource_url": "https://codeload.github.com/abachaa/MedQuAD/zip/577bd37b96c02d1833b2c9eed2de9f96964e96cb",
  "source_id": "medquad",
  "source_url": "https://github.com/abachaa/MedQuAD",
  "split": "published_corpus_no_official_split",
  "upstream_group": "https://www.nlm.nih.gov/medlineplus/ency/article/000618.htm",
  "upstream_id": "MedQuAD-577bd37b96c02d1833b2c9eed2de9f96964e96cb/10_MPlus_ADAM_QA/0001440.xml:2",
  "version": "sha256:161d948f8ce8f82accca1f5769a512dff2a01af2b3004d48f2b3da2758a38a09"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[医疗问句意图分类](../tasks/query_intent.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
