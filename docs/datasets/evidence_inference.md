# Evidence Inference 2.0 — CC-BY article subset

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

已发表临床试验报告及医生判断；不是患者级原始病历。只纳入官方测试文章中 XML 明确标注 CC-BY 的文章。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `evidence_inference` |
| 上游入口 | [发布方页面](https://github.com/jayded/evidence-inference) |
| 收录情况 | 100 题 / 1 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | MIT (annotations); CC-BY (articles, per-record version) |
| 收录语种 | 英语 100 题 |

## 来源与引用

DeYoung et al. (2020), Evidence Inference 2.0: More Data, Better Models. Article title, authors, DOI, PMCID and exact CC-BY license are retained per record.

[论文或项目引用](https://aclanthology.org/2020.bionlp-1.13/) · [数据许可](https://raw.githubusercontent.com/jayded/evidence-inference/a661e8c14f973398380c8865cf2f27a535aaaf6d/LICENSE)

许可与说明快照：[LICENSE](../../benchmarks/medical_decision_v1/sources/evidence_inference/LICENSE) · [annotation-guide.md](../../benchmarks/medical_decision_v1/sources/evidence_inference/annotation-guide.md) · [article-attribution.md](../../benchmarks/medical_decision_v1/sources/evidence_inference/article-attribution.md)

### 使用限制

判断指定干预相对对照对指定结局的报告方向，不把降低某结局直接当作治疗更优，也不把无显著差异当作等效证明。输入完整原始文章文本；统计和人群外推不在该任务的评测范围。

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [试验干预效果方向判定](../tasks/trial_effect_direction.md) | 100 | 根据完整试验报告，判断指定干预相对对照对指定结局的报告结果：显著降低、无显著差异或显著升高。方向不等同临床优劣。 |

## 答案与格式转换

PromptID 连接原 ICO 提示和医生标注；仅保留验证通过、全部有效标注的方向一致且至少有一条有效理由的条目。复制 Label Code (-1/0/1)。排除作者列出的 incorrect/questionable/malformed 提示。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`trial_effect_direction:evidence_inference:209`；语种：英语；来源组：`evidence_inference:PMC2206488`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "-1": "Significantly decreased",
        "0": "No significant difference",
        "1": "Significantly increased"
      },
      "instructions": "根据完整试验报告，判断指定干预相对对照对指定结局的报告结果：显著降低、无显著差异或显著升高。方向不等同临床优劣。",
      "type": "choice"
    }
  },
  "state": {
    "comparator": "identical amounts of gelatin infusion",
    "intervention": "dextran-70 infusion was administered at a dose of 7.5 ml/kg before the initiation of cardiopulmonary bypass and at a dose of 12.5 ml/kg after the cessation of cardiopulmonary bypass",
    "outcome": "Cardiac index ",
    "trial_report": ""
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `1`，对应选项：

```json
"Significantly increased"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "trial_effect_direction:evidence_inference:209", "choice": "1"}
```

### 样例溯源

[上游资源](https://codeload.github.com/jayded/evidence-inference/zip/a661e8c14f973398380c8865cf2f27a535aaaf6d) · [数据集说明](../datasets/evidence_inference.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "MIT (annotations); CC-BY (articles, per-record version)",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "annotation_csv_rows": [
      287,
      288,
      289,
      290,
      291
    ],
    "annotation_member": "evidence-inference-a661e8c14f973398380c8865cf2f27a535aaaf6d/annotations/annotations_merged.csv",
    "csv_row": 89,
    "license_member": "evidence-inference-a661e8c14f973398380c8865cf2f27a535aaaf6d/annotations/xml_files/PMC2206488.nxml",
    "prompt_id": "209",
    "split_member": "evidence-inference-a661e8c14f973398380c8865cf2f27a535aaaf6d/annotations/splits/test_article_ids.txt",
    "text_member": "evidence-inference-a661e8c14f973398380c8865cf2f27a535aaaf6d/annotations/txt_files/PMC2206488.txt",
    "zip_member": "evidence-inference-a661e8c14f973398380c8865cf2f27a535aaaf6d/annotations/prompts_merged.csv"
  },
  "material_kind": "published_clinical_trial_reports",
  "resource": "evidence_inference__corpus.zip",
  "resource_sha256": "cfccb8f35a7ae825eea920a8ecfd2b59573907b7cdf3fb9902d3aabee591f8e7",
  "resource_url": "https://codeload.github.com/jayded/evidence-inference/zip/a661e8c14f973398380c8865cf2f27a535aaaf6d",
  "source_id": "evidence_inference",
  "source_url": "https://github.com/jayded/evidence-inference",
  "split": "official_test_articles",
  "upstream_group": "PMC2206488",
  "upstream_id": "209",
  "version": "a661e8c14f973398380c8865cf2f27a535aaaf6d"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[试验干预效果方向判定](../tasks/trial_effect_direction.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
