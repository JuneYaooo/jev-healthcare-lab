# 患者消息处理优先级

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 有病历背景和优先处理动作，方向适合；只有 30 对、两个收件箱且消息为合成，需单列探索性结果。

## 任务是什么

给定两条患者消息及各自病历背景，选择应优先处理的消息；当前子集为人工合成消息及上游临床人员比较标注。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `message_urgency_pair` |
| 医疗场景 | 接诊与分诊 |
| 能力维度 | 风险与升级 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 30 / 100 |
| 来源组数 | 30 |
| 语种 | 英语 30 题 |
| 数据范围 | 非商业研究附加集 30 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [PMR-Synth annotated pairs](../datasets/pmr_synth.md) | 30 | [原始来源](https://huggingface.co/datasets/PortalPal-AI/PMP-Synth-AllPairs-Annotated) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。固定语义标签计算准确率、宏 F1、召回与混淆矩阵。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下成绩使用本页全部已收录题目；耗时包括请求、响应处理及重试等待。

有效回答表示返回合法选项，不代表正确；平均值和分位数包含已启动题目的失败耗时。任务总秒为含并发调度的墙钟时间，不是单题耗时之和。响应链接包含该模型全部题目，可按本页任务的题目 ID 查找。

加粗表示本任务的最高准确率或最短用时；按显示精度并列时同时加粗，全部相同则不标记。

| 模型 | 准确率 ↑ | 有效回答 / 题数 | 平均秒 ↓ | P50 秒 ↓ | P95 秒 ↓ | 任务总秒 ↓ | 超时 / 请求失败 / 无效回答 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | **63.33%** | 30 / 30 | 0.906 | 0.854 | 1.096 | 3.632 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 50.00% | 30 / 30 | **0.496** | **0.452** | **0.926** | **2.392** | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | **63.33%** | 30 / 30 | 1.306 | 1.296 | 1.776 | 5.257 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | **63.33%** | 30 / 30 | 1.020 | 0.822 | 2.135 | 4.541 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 50.00% | 30 / 30 | 2.728 | 2.778 | 3.349 | 10.878 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

本轮多题结果（固定最大打包档，对比 Flash）：JEV 65.56%，Flash 62.22%；JEV 耗时少 50.4%；JEV 成本低 18.4%–59.2%。具体准确率与费用仅对应下述性能子集，不代表全量成绩或其他调用方式。

固定本任务 30 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 62.22% | 19.635 | 1.53 / 0.95 | 90 / 90 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 56.67% | 19.430 | 1.54 / 0.87 | 90 / 90 | 0 |
| 逐题 | 8 | 1 | JEV 1.13 | 62.22% | 1.769 | 16.96 / 10.55 | 90 / 90 | 0 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 55.56% | 3.127 | 9.49 / 5.33 | 89 / 90 | 1 |
| 逐题 | 30 | 1 | JEV 1.13 | 64.44% | 1.196 | 25.08 / 16.16 | 90 / 90 | 0 |
| 逐题 | 30 | 1 | DeepSeek V4.1 Flash | 55.56% | 2.812 | 10.55 / 5.93 | 89 / 90 | 1 |
| 多题打包 | 1 | 6–8 | JEV 1.13 | 66.67% | 1.208 | 24.83 / 16.55 | 12 / 12 | 0 |
| 多题打包 | 1 | 6–8 | DeepSeek V4.1 Flash | 62.22% | 3.705 | 7.56 / 5.04 | 11 / 12 | 1 |
| 多题打包 | 1 | 3–9 | JEV 1.13 | 65.56% | 1.688 | 17.77 / 11.65 | 12 / 12 | 0 |
| 多题打包 | 1 | 3–9 | DeepSeek V4.1 Flash | 62.22% | 3.401 | 8.82 / 5.49 | 12 / 12 | 0 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 8.414–39.331 | 0.280 | 0.519 | 30.738 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-113.jsonl) · [轮2](../../results/task-performance-v1/cell-380.jsonl) · [轮3](../../results/task-performance-v1/cell-499.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 18.359–21.302 | 0.623 | 0.872 | 1.195 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-104.jsonl) · [轮2](../../results/task-performance-v1/cell-260.jsonl) · [轮3](../../results/task-performance-v1/cell-502.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 1.577–1.960 | 0.294 | 0.955 | 1.270 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-143.jsonl) · [轮2](../../results/task-performance-v1/cell-440.jsonl) · [轮3](../../results/task-performance-v1/cell-627.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 2.710–3.563 | 0.675 | 1.457 | 1.553 | 0 | 1 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-206.jsonl) · [轮2](../../results/task-performance-v1/cell-456.jsonl) · [轮3](../../results/task-performance-v1/cell-518.jsonl) |
| 逐题 B≤1 / C30 | JEV 1.13 | 0.831–1.505 | 0.567 | 1.160 | 1.495 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-158.jsonl) · [轮2](../../results/task-performance-v1/cell-352.jsonl) · [轮3](../../results/task-performance-v1/cell-609.jsonl) |
| 逐题 B≤1 / C30 | DeepSeek V4.1 Flash | 1.985–3.267 | 1.788 | 2.708 | 3.252 | 0 | 1 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-014.jsonl) · [轮2](../../results/task-performance-v1/cell-307.jsonl) · [轮3](../../results/task-performance-v1/cell-599.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 1.049–1.330 | 0.277 | 样本不足 | 0.437 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-147.jsonl) · [轮2](../../results/task-performance-v1/cell-340.jsonl) · [轮3](../../results/task-performance-v1/cell-623.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 3.282–4.295 | 0.905 | 样本不足 | 1.482 | 0 | 1 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-050.jsonl) · [轮2](../../results/task-performance-v1/cell-316.jsonl) · [轮3](../../results/task-performance-v1/cell-606.jsonl) |
| 多题打包 B≤30 / C1 | JEV 1.13 | 1.272–1.952 | 0.300 | 样本不足 | 0.950 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-184.jsonl) · [轮2](../../results/task-performance-v1/cell-323.jsonl) · [轮3](../../results/task-performance-v1/cell-542.jsonl) |
| 多题打包 B≤30 / C1 | DeepSeek V4.1 Flash | 3.283–3.610 | 0.782 | 样本不足 | 1.068 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-213.jsonl) · [轮2](../../results/task-performance-v1/cell-376.jsonl) · [轮3](../../results/task-performance-v1/cell-612.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0907 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0626–0.1251 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.0907 | 0 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | — | 1 |
| 逐题 B≤1 / C30 | JEV 1.13 | 0.0876 | 0 |
| 逐题 B≤1 / C30 | DeepSeek V4.1 Flash | — | 1 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0727 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | — | 1 |
| 多题打包 B≤30 / C1 | JEV 1.13 | 0.0739 | 0 |
| 多题打包 B≤30 / C1 | DeepSeek V4.1 Flash | 0.0906–0.1812 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

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

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：Patient #1 20 题、Patient #2 10 题。

当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。

**[PMR-Synth annotated pairs](../datasets/pmr_synth.md)**：人工合成患者消息，配对去标识病历背景；不能称为真实患者发出的消息。 答案依据：沿用 Label 字段的 Patient #1 / Patient #2；每条消息与病历最多出现一次。

公开 INBOX_A/B 与论文 train/test 的对应未确认；不得视为未暴露官方测试集。保留原始 inbox 标记；60 条消息至多组成 30 个不重复材料的比较，仍只来自两个收件箱。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [PMR-Bench Reddit Test Pairs](../datasets/pmr_bench.md) | 论文 §3.2.1 明确：Reddit 等级由 GPT-5 根据医生回复推导，再配对；并非逐对医生直接标注。本轮保留研究引用，不作为人工金标补入。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/message_urgency_pair/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/message_urgency_pair/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
