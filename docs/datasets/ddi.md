# DDI Corpus 2013

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

DrugBank / MEDLINE 文本，不是患者处方。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `ddi` |
| 上游入口 | [发布方页面](https://github.com/isegura/DDICorpus) |
| 收录情况 | 100 题 / 1 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 100 题 |
| 使用范围 | 非商业研究附加集 |
| 登记的数据许可 | CC-BY-NC-4.0 |
| 收录语种 | 英语 100 题 |

## 来源与引用

Herrero-Zazo, Segura-Bedmar, Martinez and Declerck (2013)

[论文或项目引用](https://doi.org/10.1016/j.jbi.2013.07.011) · [数据许可](https://creativecommons.org/licenses/by-nc/4.0/)

许可与说明快照：[ddi__README](../../benchmarks/medical_decision_v1/sources/ddi/ddi__README)

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [文本药物相互作用关系识别](../tasks/drug_interaction.md) | 辅助评测（不计临床主分数） | 100 | 给定药物对，判断无关系或原文标注的相互作用类型。 |

## 答案与格式转换

沿用公开测试集药物实体对及 ddi/type 标签。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`drug_interaction:ddi:DDI-DrugBank.d619.s2.p0`；语种：英语；来源组：`ddi:DDI-DrugBank.d619`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "advise": "Advice or recommendation about joint use",
        "effect": "Pharmacodynamic effect",
        "int": "Interaction without specified mechanism or effect",
        "mechanism": "Pharmacokinetic mechanism",
        "none": "No annotated interaction"
      },
      "instructions": "给定药物对，判断无关系或原文标注的相互作用类型。",
      "type": "choice"
    }
  },
  "state": {
    "drug_1": "meperidine",
    "drug_2": "MAOIs",
    "sentence": "This is typical of the interaction of meperidine and MAOIs. "
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `int`，对应选项：

```json
"Interaction without specified mechanism or effect"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "drug_interaction:ddi:DDI-DrugBank.d619.s2.p0", "choice": "int"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/isegura/DDICorpus/819b0fa538ed83ab2a8b4f5417bba3c03249b7f3/DDICorpus-2013.zip) · [数据集说明](../datasets/ddi.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-NC-4.0",
  "distribution": "research_noncommercial",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "pair_id": "DDI-DrugBank.d619.s2.p0",
    "zip_member": "DDICorpus/Test/Test for DDI Extraction task/DrugBank/Selegiline.xml"
  },
  "material_kind": "drug_reference_and_literature",
  "resource": "ddi__DDICorpus-2013.zip",
  "resource_sha256": "87fc63e32ebce20d9841c372e0c594ec72d60882ab5621550ca73c3eaf80ab60",
  "resource_url": "https://raw.githubusercontent.com/isegura/DDICorpus/819b0fa538ed83ab2a8b4f5417bba3c03249b7f3/DDICorpus-2013.zip",
  "source_id": "ddi",
  "source_url": "https://github.com/isegura/DDICorpus",
  "split": "official_test",
  "upstream_group": "DDI-DrugBank.d619",
  "upstream_id": "DDI-DrugBank.d619.s2.p0",
  "version": "819b0fa538ed83ab2a8b4f5417bba3c03249b7f3"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[文本药物相互作用关系识别](../tasks/drug_interaction.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
