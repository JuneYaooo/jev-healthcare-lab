# PMR-Synth annotated pairs

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

人工合成患者消息，配对去标识病历背景；不能称为真实患者发出的消息。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `pmr_synth` |
| 上游入口 | [发布方页面](https://huggingface.co/datasets/PortalPal-AI/PMP-Synth-AllPairs-Annotated) |
| 收录情况 | 30 题 / 1 个任务 |
| 评测用途 | 临床主评测 30 题 |
| 使用范围 | 非商业研究附加集 |
| 登记的数据许可 | CC-BY-NC-4.0 |
| 收录语种 | 英语 30 题 |

## 来源与引用

Gatto et al. (2026)

[论文或项目引用](https://arxiv.org/abs/2601.13178) · [数据许可](https://creativecommons.org/licenses/by-nc/4.0/)

许可与说明快照：[README.md](../../benchmarks/medical_decision_v1/sources/pmr_synth/README.md)

### 使用限制

公开 INBOX_A/B 与论文 train/test 的对应未确认；不得视为未暴露官方测试集。保留原始 inbox 标记；60 条消息至多组成 30 个不重复材料的比较，仍只来自两个收件箱。

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [患者消息处理优先级](../tasks/message_urgency_pair.md) | 临床主评测 | 30 | 给定两条患者消息及各自病历背景，选择应优先处理的消息；当前子集为人工合成消息及上游临床人员比较标注。 |

## 答案与格式转换

沿用 Label 字段的 Patient #1 / Patient #2；每条消息与病历最多出现一次。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`message_urgency_pair:pmr_synth:A:175`；语种：英语；来源组：`pmr_synth:fc8f0c897ec65af988dece01`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "Patient #1": "Prioritize patient 1",
        "Patient #2": "Prioritize patient 2"
      },
      "instructions": "给定两条患者消息及各自病历背景，选择应优先处理的消息；当前子集为人工合成消息及上游临床人员比较标注。",
      "type": "choice"
    }
  },
  "state": {
    "patient_1": {
      "ehr": "###Demographics###\nAge: Between 35 - 40    \nGender: Female\n    \n###Full Active Problem List###:\nLeft tubal pregnancy without intrauterine pregnancy\n\n###Recent Encounters (Max 10)###\n\nDiagnoses (Past Year): Reactive depression (situational)\nDiagnoses (Older): Multiple benign nevi - IUD (intrauterine device) in place - Onychocryptosis - Intrauterine contraceptive device threads lost, initial encounter - Cherry angioma - Abnormal ultrasound - Encounter for postpartum care of lactating mother\n\n###Medications (Outpatient)###\n\nActive (Start Date Before Message, Not Yet Ended):\n    \n-BUPROPION HCL XL 150 MG 24 HR TABLET, EXTENDED RELEASE\n-FLUOXETINE 20 MG CAPSULE\n-LEVONORGESTREL 0.15 MG-ETHINYL ESTRADIOL 30 MCG TABLETS,3 MOS PACK(91)",
      "message": "I just had my first period after giving birth and I've been having pretty heavy bleeding for 4 days now. I am soaking through many more pads per day than normal. I feel like everytime I go to the bathroom there is just so much blood and I dont know what to do. My flow has not slowed down at all. is this normal??"
    },
    "patient_2": {
      "ehr": "###Demographics###\nAge: Between 30 - 35    \nGender: Female\n    \n###Full Active Problem List###:\nHealth care maintenance - Subclinical hypothyroidism - Acanthosis nigricans - BMI 38.0-38.9,adult - Left knee pain - Mixed hyperlipidemia - Infertility management - Rh negative, antepartum - Prenatal care\n\n###Recent Encounters (Max 10)###\n\nDiagnoses (Past Year): Prenatal care in second trimester - History of infertility - History of miscarriage - Pregnancy of unknown anatomic location - Male factor infertility - Pregnancy, unspecified gestational age - Prenatal care in first trimester - BMI 40.0-44.9, adult\nDiagnoses (Older): \n\n###Medications (Outpatient)###\n\nActive (Start Date Before Message, Not Yet Ended):\n    \n*No Active Medications*",
      "message": "Hi Doctor, \n\nSo I am having some unexpected bleeding I need to chat with you about. I had sex with my girlfriend last night and I'm not sure if this is normal but I was just wondering if I should go to the doctor because I'm bleeding like I have my period. It doesn't seem heavy but it started right after we finished having sex. Is this cause for concern? \n\nAlso, I need to update my physical address in the system. Can I do this over the portal? \n\nThanks."
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `Patient #1`，对应选项：

```json
"Prioritize patient 1"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "message_urgency_pair:pmr_synth:A:175", "choice": "Patient #1"}
```

### 样例溯源

[上游资源](https://huggingface.co/datasets/PortalPal-AI/PMP-Synth-AllPairs-Annotated/resolve/0a0347fdc9cd0639348ffa54fe3988a7b45b2a18/data/INBOX_A-00000-of-00001.parquet) · [数据集说明](../datasets/pmr_synth.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-NC-4.0",
  "distribution": "research_noncommercial",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_field": "Label",
    "inbox": "INBOX_A",
    "row_index_zero_based": 175
  },
  "material_kind": "synthetic_messages_with_ehr_context",
  "resource": "pmr_synth__INBOX_A-00000-of-00001.parquet",
  "resource_sha256": "f381a6f2ec8e55214086282e7ffe7f7bd94ec737535ccb91dae86db50cdd8dc2",
  "resource_url": "https://huggingface.co/datasets/PortalPal-AI/PMP-Synth-AllPairs-Annotated/resolve/0a0347fdc9cd0639348ffa54fe3988a7b45b2a18/data/INBOX_A-00000-of-00001.parquet",
  "source_id": "pmr_synth",
  "source_url": "https://huggingface.co/datasets/PortalPal-AI/PMP-Synth-AllPairs-Annotated",
  "split": "published_inboxes_train_test_mapping_unresolved",
  "upstream_group": "fc8f0c897ec65af988dece01",
  "upstream_id": "A:175",
  "version": "0a0347fdc9cd0639348ffa54fe3988a7b45b2a18"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[患者消息处理优先级](../tasks/message_urgency_pair.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
