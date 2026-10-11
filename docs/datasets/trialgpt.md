# TrialGPT SIGIR

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

患者题设配真实试验文件；不是实际入组结局。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `trialgpt` |
| 上游入口 | [发布方页面](https://github.com/ncbi-nlp/TrialGPT) |
| 收录情况 | 100 题 / 1 个任务 |
| 评测用途 | 临床主评测 100 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | LicenseRef-NCBI-Public-Domain |
| 收录语种 | 英语 100 题 |

## 来源与引用

Jin et al., Matching Patients to Clinical Trials with Large Language Models

[论文或项目引用](https://github.com/ncbi-nlp/TrialGPT) · [数据许可](https://github.com/ncbi-nlp/TrialGPT/blob/main/LICENSE)

许可与说明快照：[trialgpt__LICENSE](../../benchmarks/medical_decision_v1/sources/trialgpt/trialgpt__LICENSE) · [trialgpt__README.md](../../benchmarks/medical_decision_v1/sources/trialgpt/trialgpt__README.md)

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [患者临床试验初筛与转介判断](../tasks/trial_referral.md) | 临床主评测 | 100 | 根据患者和试验材料，判断不相关、可能适合或很可能适合转介。 |

## 答案与格式转换

SIGIR 公开 relevance 0/1/2；0 不相关、1 可能转介、2 高度适合转介。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`trial_referral:trialgpt:sigir-201512:NCT02418169`；语种：英语；来源组：`trialgpt:sigir-201512`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "0": "Irrelevant: would not refer",
        "1": "Potential: consider referral after further investigation",
        "2": "Eligible: highly likely to refer"
      },
      "instructions": "根据患者和试验材料，判断不相关、可能适合或很可能适合转介。",
      "type": "choice"
    }
  },
  "state": {
    "patient": "A 44-year-old man was recently in an automobile accident where he sustained a skull fracture. In the emergency room, he noted clear fluid dripping from his nose. The following day he started complaining of severe headache and fever. Nuchal rigidity was found on physical examination.",
    "trial": {
      "brief_summary": "This study evaluates the association between traumatic brain injuries and craniofacial or/and skull fractures. Purpose is to find out the amount of missed diagnoses and improve primary diagnostics of trauma patients.",
      "brief_title": "Association Between Craniofacial Fractures and Brain Injuries: Diagnostic and Therapeutic Considerations",
      "exclusion_criteria": ": \n\n Died before admitted to hospital",
      "inclusion_criteria": "inclusion criteria: \n\n Severe traumatic brain injury, GCS 8 or less and/or Craniofacial fracture \n\n "
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `1`，对应选项：

```json
"Potential: consider referral after further investigation"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "trial_referral:trialgpt:sigir-201512:NCT02418169", "choice": "1"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/ncbi-nlp/TrialGPT/1b3242cd50c153a9c324661d4a0bd94fc68a4226/dataset/sigir/retrieved_trials.json) · [数据集说明](../datasets/trialgpt.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "LicenseRef-NCBI-Public-Domain",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "nct_id": "NCT02418169",
    "patient_id": "sigir-201512",
    "relevance": "1"
  },
  "material_kind": "synthetic_patient_real_trial",
  "resource": "trialgpt__dataset_sigir_retrieved_trials.json",
  "resource_sha256": "8516049da9f4663b1288086532cc885da232532bd2e081a2b70f54fb035ddb81",
  "resource_url": "https://raw.githubusercontent.com/ncbi-nlp/TrialGPT/1b3242cd50c153a9c324661d4a0bd94fc68a4226/dataset/sigir/retrieved_trials.json",
  "source_id": "trialgpt",
  "source_url": "https://github.com/ncbi-nlp/TrialGPT",
  "split": "sigir_judged_pool",
  "upstream_group": "sigir-201512",
  "upstream_id": "sigir-201512:NCT02418169",
  "version": "1b3242cd50c153a9c324661d4a0bd94fc68a4226"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[患者临床试验初筛与转介判断](../tasks/trial_referral.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
