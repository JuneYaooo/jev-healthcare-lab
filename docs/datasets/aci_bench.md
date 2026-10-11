# ACI-Bench

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

合成就诊会话与人工文书；不是自然发生的医院记录。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `aci_bench` |
| 上游入口 | [发布方页面](https://github.com/microsoft/clinical_visit_note_summarization_corpus) |
| 收录情况 | 100 题 / 1 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 英语 100 题 |

## 来源与引用

Microsoft / Yim et al. (2023)

[论文或项目引用](https://www.nature.com/articles/s41597-023-02487-3) · [数据许可](https://creativecommons.org/licenses/by/4.0/)

许可与说明快照：[aci_bench__LICENSE](../../benchmarks/medical_decision_v1/sources/aci_bench/aci_bench__LICENSE) · [LICENSE](../../benchmarks/medical_decision_v1/sources/aci_bench/LICENSE) · [aci_bench__README.md](../../benchmarks/medical_decision_v1/sources/aci_bench/aci_bench__README.md) · [README.md](../../benchmarks/medical_decision_v1/sources/aci_bench/README.md)

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [病历章节类别](../tasks/note_section.md) | 100 | 给定去除章节标题的原文片段，选择原始章节类别。 |

## 答案与格式转换

沿用人工文书的章节标题；去除标题后作分类。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`note_section:aci_bench:D2N144:0`；语种：英语；来源组：`aci_bench:D2N144`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "assessment_plan": "Assessment or plan",
        "exam": "Physical examination or vital signs",
        "history": "History, symptoms, medications or allergies",
        "results": "Laboratory, imaging or diagnostic results"
      },
      "instructions": "给定去除章节标题的原文片段，选择原始章节类别。",
      "type": "choice"
    }
  },
  "state": {
    "section_text": "Rheumatoid arthritis management."
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `history`，对应选项：

```json
"History, symptoms, medications or allergies"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "note_section:aci_bench:D2N144:0", "choice": "history"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/microsoft/clinical_visit_note_summarization_corpus/293e454917c562361409232f65e9d870a45af026/data/aci-bench/challenge_data/clinicalnlp_taskC_test2.csv) · [数据集说明](../datasets/aci_bench.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "csv_row": 18,
    "encounter_id": "D2N144",
    "heading": "CHIEF COMPLAINT"
  },
  "material_kind": "expert_simulated",
  "resource": "aci_bench__data_aci-bench_challenge_data_clinicalnlp_taskC_test2.csv",
  "resource_sha256": "599e3330a14e25a0e056aee1365ffac7ebe50058f15821eae42a5513c2bb5a4f",
  "resource_url": "https://raw.githubusercontent.com/microsoft/clinical_visit_note_summarization_corpus/293e454917c562361409232f65e9d870a45af026/data/aci-bench/challenge_data/clinicalnlp_taskC_test2.csv",
  "source_id": "aci_bench",
  "source_url": "https://github.com/microsoft/clinical_visit_note_summarization_corpus",
  "split": "official_test_1_2_3",
  "upstream_group": "D2N144",
  "upstream_id": "D2N144:0",
  "version": "293e454917c562361409232f65e9d870a45af026"
}
```

该题的格式转换说明：

Removed original heading; mapped section titles into four fixed categories.

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[病历章节类别](../tasks/note_section.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
