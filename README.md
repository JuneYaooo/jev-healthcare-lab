# Jev 医疗评测研究 · Jev Healthcare Lab

研究 Jev 在医疗文本、病历结构化、患者入组预筛和循证核查中，**哪些环节有效、在哪些条件下失败、结果如何核验**。

本仓库提供数据适配与评分代码、历史评测汇总、样本身份与请求哈希，以及场景研究报告。当前为探索性离线评测；非 TypeSafe 官方项目，尚不具备自主诊疗或自动确认患者入组的验证基础。

**实验快照：2026-09-24 · 模型：`jev-1.13.0` · 代码许可：[MIT](LICENSE)**

[场景统计](#医疗场景与统计总览) · [全部数据集与实验](docs/场景数据集与实验.md) · [研究结论](docs/研究报告.md) · [全部结果](docs/结果总表.md) · [复现说明](docs/REPRODUCING.md) · [覆盖与阻塞](docs/覆盖与阻塞账本.md)

## 使用场景

| 你要做什么 | 从这里开始 | 可以获得什么 |
| --- | --- | --- |
| 判断 Jev 是否值得接入病历整理流程 | [医疗工作流全景](docs/医疗工作流全景.md) | 候选字段复核、分类与质控的场景拆解、验收指标和限制 |
| 研究患者入组预筛与科研队列 | [患者入组与科研队列](docs/患者入组与科研队列.md) | 已测任务、错误边界，以及仍需人工判断的环节 |
| 核查模型结果与实验口径 | [结果总表](docs/结果总表.md)、[评测索引](results/evaluation_index.jsonl) | 逐任务指标、样本身份与请求哈希；原始响应不随仓库分发 |
| 复用适配或评分代码开展实验 | [复现说明](docs/REPRODUCING.md) | 数据准备、API 调用与评分入口，以及各数据源的获取限制 |

## 它解决什么问题

医疗选择题成绩、给定实体的分类准确率和完整病历抽取效果，回答的是不同问题。本项目把候选构造、Jev 判断和后续程序校验分开评估，保留规则基线、证据消融与失败案例，帮助判断模型具体能改善哪一步。

例如，英文实体筛选实验中，加入 Jev 后严格 F1 从 **58.9% 提升到 69.4%**，主要收益是减少误报；召回率仍只有 **61.7%**。这支持继续研究候选筛选，但不能据此认定完整病历抽取已可靠。

## 实验流程与能力边界

```mermaid
flowchart LR
    A[取得数据并构造候选] --> B[准备请求并记录哈希]
    B --> C[Jev 有限选项判断]
    C --> D[响应校验与本地缓存]
    D --> E[逐任务评分与基线比较]
    E --> F[发布聚合结果与限制]
```

| 已提供 | 使用边界 |
| --- | --- |
| 医疗文本、实体候选、证据判断等任务适配与评分代码 | 不同任务使用不同标签、样本与指标，不能合并为一个“医疗准确率” |
| 真实 API 批量调用、响应校验、成功缓存跳过与失败记录 | 重新运行需自行取得数据和 API 凭据，并产生调用费用 |
| 历史聚合结果、样本身份与请求哈希 | 不含基准原文和真实响应缓存；克隆仓库后无法直接重算全部历史指标 |
| OCR / ASR 辅助实验代码 | 依赖额外工具、权重与输入；样本规模小，不能代表完整临床流程 |
| 无需外部服务的仓库检查 | 检查数据一致性与部分代码行为，不等于重新执行医学基准或临床验证 |

人工构造的 [请求示例](examples/request.json) 展示了“支持 / 矛盾 / 证据不足”的有限选项接口；它不是真实病历，也不是批量评测所需的完整 prepared JSONL 文件。

## 快速开始

### 1. 离线查看与检查

下载或克隆仓库后，在仓库根目录运行。建议使用 **Python 3.11**（与 CI 一致）；以下命令仅使用 Python 标准库，无需密钥、下载数据或安装第三方依赖。

```sh
python3 scripts/summary.py
python3 -m unittest discover -s tests -v
```

第一条命令读取已发布的 [快照](results/snapshot.json)，输出包括：

```json
{
  "date": "2026-09-24",
  "model": "jev-1.13.0",
  "evaluation_rows": 6886,
  "successful_api_responses": 6843,
  "deterministic_empty_rows": 43
}
```

这是历史快照的字段节选，不是本次重新调用 API 的结果。当前仓库包含 **6 项离线测试**。

### 2. 开展真实评测

按 [复现说明](docs/REPRODUCING.md) 取得相应版本的数据，并使用对应适配脚本生成 prepared JSONL。默认数据与缓存放在不进入 Git 的 `data/` 下，也可通过 `JEV_DATA_DIR` 指定路径。

设置环境变量 `TYPESAFE_API_KEY`；[.env.example](.env.example) 仅展示格式，脚本不会自动加载它。也可通过 `--env-file` 指定本地私有配置文件。

```sh
# 将路径替换为已经生成的 prepared JSONL 文件；此命令会产生真实 API 调用费用。
python3 scripts/live_batch.py --input data/EXAMPLE_prepared.jsonl --max-calls 10 --workers 4
```

默认模型固定为 `jev-1.13.0`。成功缓存会跳过，网络失败可在后续运行中重试；失败请求不会用模拟预测替代。可选的数据、实体识别与音频依赖见 [requirements-optional.txt](requirements-optional.txt)，Tesseract 需单独安装。具体安装和评分步骤请按所选任务的复现说明执行。

<!-- BEGIN GENERATED SCENARIOS -->
## 医疗场景与统计总览

快照日期 **2026-09-24**，模型 **`jev-1.13.0`**。以下覆盖仓库现有的全部医疗任务与资源清单；未测场景明确列出，不表示已经穷尽或验证所有医疗业务。

| 统计项 | 数量与口径 |
| --- | --- |
| 资源入口 | 90 项；含数据集、赛事、工具与重叠入口 |
| 有实测映射的资源 | 39 项；不等于独立数据集数量 |
| 医疗任务条件 | 96 个：72 个公开数据／材料适配 + 24 类自编挑战 |
| 主评测 | 6,586 条，其中真实 API 响应 6,543 条，程序空预测 43 条 |
| 配对鲁棒性 | 300 条额外调用，5 个任务 × 20 个原始案例 × 3 种扰动 |
| 总计 | 6,886 条记录，6,843 条真实 API 响应；不是独立患者数 |

**数据包含范围：**仓库包含数据集目录、适配与评分代码、聚合指标、样本身份／哈希和失败案例摘要。原始基准文本、prepared 请求与真实响应缓存未随仓库分发；需按数据来源自行取得，不能仅凭公开快照重新计分。

完整的 [场景数据集与实验清单](docs/场景数据集与实验.md) 收录全部 90 项资源的来源、状态、任务映射与范围说明。

| 医疗场景 | 资源入口 | 计数任务 | 评测记录 | API 响应 | 空预测 |
| --- | ---: | ---: | ---: | ---: | ---: |
| [病历实体、否定状态与术语标准化](#scene-records) | 23 | 12 | 1,200 | 1,157 | 43 |
| [临床文书、章节归类与交接班](#scene-documentation) | 5 | 2 | 200 | 200 | 0 |
| [患者咨询、服务路由与就医流程](#scene-service) | 8 | 6 | 600 | 600 | 0 |
| [医疗质控、幻觉识别与请求安全](#scene-quality) | 7 | 8 | 1,097 | 1,097 | 0 |
| [药物关系、用药变更与出院带药](#scene-medication) | 6 | 3 | 350 | 350 | 0 |
| [患者入组预筛与临床试验匹配](#scene-trials) | 3 | 3 | 350 | 350 | 0 |
| [循证研究、PICO 与公共卫生核查](#scene-evidence) | 8 | 9 | 855 | 855 | 0 |
| [临床计算、参数选择与评分量表](#scene-calculators) | 2 | 5 | 502 | 502 | 0 |
| [医学知识与考试对照](#scene-knowledge) | 3 | 5 | 400 | 400 | 0 |
| [语音病历、OCR、影像报告与信号](#scene-multimodal) | 6 | 4 | 36 | 36 | 0 |
| [合成病例、急诊、护理与 ICU](#scene-acute) | 7 | 1 | 100 | 100 | 0 |
| [中医知识、辨证与安全](#scene-tcm) | 4 | 14 | 800 | 800 | 0 |
| [肿瘤登记、脱敏与临床 NLP 工具](#scene-tools) | 8 | 0 | 0 | 0 | 0 |
| [跨场景自编边界挑战](#scene-challenge) | 0 | 24 | 96 | 96 | 0 |
| **主评测合计** | **90** | **96** | **6,586** | **6,543** | **43** |

每个任务只归入一个场景；工具关联的相同任务不重复计数。鲁棒性额外 300 条在后文单列。Accuracy 和 micro-F1 不混算，不提供跨场景“总准确率”。

## 分场景数据集与效果

<a id="scene-records"></a>

### 病历实体、否定状态与术语标准化

给定实体边界的类型分类与端到端抽取分开看；LongHealth 为 20 个虚构患者的 100 个问题。

**主要结果：**IMCS 类型 Accuracy 96%；端到端 F1 59.5%；NCBI 管线 F1 69.4%；LongHealth Accuracy 95%。

<details>
<summary>查看全部 12 个任务条件 · 1,200 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [IMCS21](docs/场景数据集与实验.md#resource-6) | `imcs_assertion_oracle_span` | 100 | Accuracy | 79.0% |
| [IMCS21](docs/场景数据集与实验.md#resource-6) | `imcs_dialogue_act` | 100 | Accuracy | 70.0% |
| [IMCS21](docs/场景数据集与实验.md#resource-6) | `imcs_entity_type_oracle_span` | 100 | Accuracy | 96.0% |
| [IMCS21](docs/场景数据集与实验.md#resource-6) | `imcs_ner_dictionary_pipeline` | 100 | micro-F1 | 59.5% |
| [IMCS21](docs/场景数据集与实验.md#resource-6) | `imcs_normalization_top20` | 100 | Accuracy | 93.0% |
| [BioScope](docs/场景数据集与实验.md#resource-38) | `bioscope_sentence_cues` | 100 | Accuracy | 83.0% |
| [NUBes](docs/场景数据集与实验.md#resource-39) | `nubes_scope_status` | 100 | Accuracy | 72.0% |
| [NCBI Disease](docs/场景数据集与实验.md#resource-40) | `ncbi_disease_category_oracle_span` | 100 | Accuracy | 58.0% |
| [NCBI Disease](docs/场景数据集与实验.md#resource-40) / [medspaCy](docs/场景数据集与实验.md#resource-84) | `ncbi_medspacy_jev_ner` | 100 | micro-F1 | 69.4% |
| [MedMentions](docs/场景数据集与实验.md#resource-44) | `medmentions_type_oracle_span` | 100 | Accuracy | 60.0% |
| [MedAL](docs/场景数据集与实验.md#resource-45) | `medal_demo_disambiguation` | 100 | Accuracy | 67.0% |
| [LongHealth](docs/场景数据集与实验.md#resource-70) | `longhealth_full_context` | 100 | Accuracy | 95.0% |

</details>

<details>
<summary>未测／待补齐：16 项资源</summary>

- [CMeEE](docs/场景数据集与实验.md#resource-1)：需数据访问/许可核实或获准原文。
- [CMeIE](docs/场景数据集与实验.md#resource-2)：需数据访问/许可核实或获准原文。
- [CHIP-CDN](docs/场景数据集与实验.md#resource-3)：需数据访问/许可核实或获准原文。
- [CHIP-CDEE](docs/场景数据集与实验.md#resource-4)：需数据访问/许可核实或获准原文。
- [CHIP-MDCFNPC](docs/场景数据集与实验.md#resource-5)：需数据访问/许可核实或获准原文。
- [CCKS医疗信息抽取系列](docs/场景数据集与实验.md#resource-7)：需锁定具体届别/授权。
- [i2b2 2006](docs/场景数据集与实验.md#resource-24)：需数据访问/许可核实或获准原文。
- [i2b2 2008](docs/场景数据集与实验.md#resource-25)：需数据访问/许可核实或获准原文。
- [i2b2 2009](docs/场景数据集与实验.md#resource-26)：需数据访问/许可核实或获准原文。
- [i2b2 2010](docs/场景数据集与实验.md#resource-27)：需数据访问/许可核实或获准原文。
- [i2b2 2011](docs/场景数据集与实验.md#resource-28)：需数据访问/许可核实或获准原文。
- [i2b2 2012](docs/场景数据集与实验.md#resource-29)：需数据访问/许可核实或获准原文。
- [i2b2 2014](docs/场景数据集与实验.md#resource-30)：需数据访问/许可核实或获准原文。
- [n2c2 2022 SHAC](docs/场景数据集与实验.md#resource-33)：需数据访问/许可核实或获准原文。
- [THYME / Clinical TempEval](docs/场景数据集与实验.md#resource-34)：需数据访问/许可核实或获准原文。
- [MedNLI](docs/场景数据集与实验.md#resource-35)：需数据访问/许可核实或获准原文。

</details>

<a id="scene-documentation"></a>

### 临床文书、章节归类与交接班

已测章节分类；尚未验证从医患对话生成完整病历或真实交接班质量。

**主要结果：**MTS Accuracy 76%；ACI 已给定章节边界 Accuracy 99%。

<details>
<summary>查看全部 2 个任务条件 · 200 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [MTS-Dialog](docs/场景数据集与实验.md#resource-14) | `mts_section_classification` | 100 | Accuracy | 76.0% |
| [ACI-Bench](docs/场景数据集与实验.md#resource-15) | `aci_note_section` | 100 | Accuracy | 99.0% |

</details>

<details>
<summary>未测／待补齐：3 项资源</summary>

- [CLIP](docs/场景数据集与实验.md#resource-36)：需数据访问/许可核实或获准原文。
- [DischargeMe](docs/场景数据集与实验.md#resource-37)：需数据访问/许可核实或获准原文。
- [DiSCQ](docs/场景数据集与实验.md#resource-74)：需数据访问/许可核实或获准原文。

</details>

<a id="scene-service"></a>

### 患者咨询、服务路由与就医流程

MedQuAD 测问题类型；MedJourney 的科室多标签与四类选择题不是实际分诊效果。

**主要结果：**MedQuAD Accuracy 96%；MedJourney 科室 micro-F1 36.9%，选择题 Accuracy 82%–92%。

<details>
<summary>查看全部 6 个任务条件 · 600 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [MedQuAD](docs/场景数据集与实验.md#resource-56) | `medquad_question_type` | 100 | Accuracy | 96.0% |
| [MedJourney](docs/场景数据集与实验.md#resource-72) | `medjourney_departments` | 100 | micro-F1 | 36.9% |
| [MedJourney](docs/场景数据集与实验.md#resource-72) | `medjourney_dp_mcq` | 100 | Accuracy | 92.0% |
| [MedJourney](docs/场景数据集与实验.md#resource-72) | `medjourney_ep_mcq` | 100 | Accuracy | 82.0% |
| [MedJourney](docs/场景数据集与实验.md#resource-72) | `medjourney_mp_mcq` | 100 | Accuracy | 86.0% |
| [MedJourney](docs/场景数据集与实验.md#resource-72) | `medjourney_tp_mcq` | 100 | Accuracy | 83.0% |

</details>

<details>
<summary>未测／待补齐：6 项资源</summary>

- [CHIP-CTC](docs/场景数据集与实验.md#resource-8)：需数据访问/许可核实或获准原文。
- [CHIP-STS](docs/场景数据集与实验.md#resource-9)：需数据访问/许可核实或获准原文。
- [KUAKE-QIC](docs/场景数据集与实验.md#resource-10)：需数据访问/许可核实或获准原文。
- [KUAKE-QTR](docs/场景数据集与实验.md#resource-11)：需数据访问/许可核实或获准原文。
- [KUAKE-QQR](docs/场景数据集与实验.md#resource-12)：需数据访问/许可核实或获准原文。
- [MedDialog](docs/场景数据集与实验.md#resource-13)：缺少目标任务独立金标。

</details>

<a id="scene-quality"></a>

### 医疗质控、幻觉识别与请求安全

错误检出、错误定位、回答幻觉和请求安全是不同任务；MedSafety 的正常／有害来源存在混杂。

**主要结果：**MEDEC 检出 Accuracy 65%；MedHallu 有证据 Accuracy 82%；请求安全 Accuracy 93.5%。

<details>
<summary>查看全部 8 个任务条件 · 1,097 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [MEDEC-MS](docs/场景数据集与实验.md#resource-17) | `medec_error_detection` | 100 | Accuracy | 65.0% |
| [MEDEC-MS](docs/场景数据集与实验.md#resource-17) | `medec_error_localization` | 100 | Accuracy | 72.0% |
| [MedErrBench](docs/场景数据集与实验.md#resource-20) | `mederrbench_ARA` | 97 | Accuracy | 69.1% |
| [MedErrBench](docs/场景数据集与实验.md#resource-20) | `mederrbench_CN` | 100 | Accuracy | 73.0% |
| [MedErrBench](docs/场景数据集与实验.md#resource-20) | `mederrbench_EN` | 100 | Accuracy | 81.0% |
| [MedHallu](docs/场景数据集与实验.md#resource-21) | `medhallu_with_evidence` | 200 | Accuracy | 82.0% |
| [MedHallu](docs/场景数据集与实验.md#resource-21) | `medhallu_without_evidence` | 200 | Accuracy | 60.0% |
| [MedSafetyBench](docs/场景数据集与实验.md#resource-22) | `medsafety_request_gate` | 200 | Accuracy | 93.5% |

</details>

<details>
<summary>未测／待补齐：3 项资源</summary>

- [MEDEC-UW](docs/场景数据集与实验.md#resource-18)：需数据访问/许可核实或获准原文。
- [MEDIQA-CORR](docs/场景数据集与实验.md#resource-19)：关联赛事入口。
- [HealthBench](docs/场景数据集与实验.md#resource-23)：缺少待审回复与独立评审金标。

</details>

<a id="scene-medication"></a>

### 药物关系、用药变更与出院带药

关系任务给定实体；CDrugRed 为发布训练池按患者分离的留出样本，不是官方隐藏测试。

**主要结果：**DDI Accuracy 79.3%；BC5CDR Accuracy 57%；出院带药 micro-F1 48.6%。

<details>
<summary>查看全部 3 个任务条件 · 350 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [BC5CDR](docs/场景数据集与实验.md#resource-41) | `bc5cdr_relation_oracle_entities` | 100 | Accuracy | 57.0% |
| [DDI Corpus](docs/场景数据集与实验.md#resource-42) | `ddi_relation_oracle_pairs` | 150 | Accuracy | 79.3% |
| [CDrugRed / CHIP2025 Task2](docs/场景数据集与实验.md#resource-73) | `cdrugred_discharge_candidate_pipeline` | 100 | micro-F1 | 48.6% |

</details>

<details>
<summary>未测／待补齐：3 项资源</summary>

- [n2c2 2018 ADE](docs/场景数据集与实验.md#resource-32)：需数据访问/许可核实或获准原文。
- [CADEC](docs/场景数据集与实验.md#resource-43)：下载入口未恢复。
- [CMED / n2c2 2022 medication](docs/场景数据集与实验.md#resource-71)：需数据访问/许可核实或获准原文。

</details>

<a id="scene-trials"></a>

### 患者入组预筛与临床试验匹配

NLI4CT 测证据材料上的判断与定位；TrialGPT 为直接三分类，不是完整检索排序和逐条纳排推理。

**主要结果：**TrialGPT 三分类 Accuracy 48%；NLI4CT 判断 Accuracy 88%，证据 micro-F1 49.9%。

<details>
<summary>查看全部 3 个任务条件 · 350 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [NLI4CT / SemEval 2023 Task 7](docs/场景数据集与实验.md#resource-46) | `nli4ct_entailment` | 100 | Accuracy | 88.0% |
| [NLI4CT / SemEval 2023 Task 7](docs/场景数据集与实验.md#resource-46) | `nli4ct_evidence` | 100 | micro-F1 | 49.9% |
| [TrialGPT / TREC CT](docs/场景数据集与实验.md#resource-47) | `trialgpt_sigir_referral` | 150 | Accuracy | 48.0% |

</details>

<details>
<summary>未测／待补齐：1 项资源</summary>

- [n2c2 2018 Cohort](docs/场景数据集与实验.md#resource-31)：需数据访问/许可核实或获准原文。

</details>

<a id="scene-evidence"></a>

### 循证研究、PICO 与公共卫生核查

提供证据的判断不能替代检索评价；固定窗口分类与原始序列抽取指标不同。

**主要结果：**PICO micro-F1 12.7%；EvidenceBench micro-F1 29.4%；PubMedQA Accuracy 74%。

<details>
<summary>查看全部 9 个任务条件 · 855 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [EBM-NLP](docs/场景数据集与实验.md#resource-48) | `ebm_pico_fixed_windows` | 100 | micro-F1 | 12.7% |
| [Evidence Inference](docs/场景数据集与实验.md#resource-49) | `evidence_inference_fulltext` | 100 | Accuracy | 89.0% |
| [EvidenceOutcomes](docs/场景数据集与实验.md#resource-50) | `evidenceoutcomes_fixed_window` | 100 | Accuracy | 88.0% |
| [EvidenceBench](docs/场景数据集与实验.md#resource-51) | `evidencebench_sentence_selection` | 37 | micro-F1 | 29.4% |
| [PubMedQA](docs/场景数据集与实验.md#resource-52) | `pubmedqa_evidence_qa` | 100 | Accuracy | 74.0% |
| [PubMed 20k RCT](docs/场景数据集与实验.md#resource-53) | `pubmed_rct_section` | 100 | Accuracy | 75.0% |
| [SciFact](docs/场景数据集与实验.md#resource-54) | `scifact_cited_abstract` | 118 | Accuracy | 85.6% |
| [PUBHEALTH](docs/场景数据集与实验.md#resource-55) | `pubhealth_claim_only` | 100 | Accuracy | 20.0% |
| [PUBHEALTH](docs/场景数据集与实验.md#resource-55) | `pubhealth_with_article` | 100 | Accuracy | 67.0% |

</details>

<a id="scene-calculators"></a>

### 临床计算、参数选择与评分量表

参数选择与公式执行分开记录；Verified 只适配 5 种评分各 20 条，不是全部计算器。

**主要结果：**输入充分性 Accuracy 81.5%；分级 Accuracy 60.5%；Verified Accuracy 25%；BMI 参数对 17/20。

<details>
<summary>查看全部 5 个任务条件 · 502 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [CMedCalc-Bench](docs/场景数据集与实验.md#resource-68) | `bmi_height_selection` | 20 | Accuracy | 95.0% |
| [CMedCalc-Bench](docs/场景数据集与实验.md#resource-68) | `bmi_weight_selection` | 20 | Accuracy | 95.0% |
| [CMedCalc-Bench](docs/场景数据集与实验.md#resource-68) | `cmedcalc_input_sufficiency` | 200 | Accuracy | 81.5% |
| [CMedCalc-Bench](docs/场景数据集与实验.md#resource-68) | `cmedcalc_semantic_grade` | 162 | Accuracy | 60.5% |
| [MedCalc-Bench / Verified](docs/场景数据集与实验.md#resource-69) | `medcalc_verified_bounded_score` | 100 | Accuracy | 25.0% |

</details>

<a id="scene-knowledge"></a>

### 医学知识与考试对照

选择题用于能力对照，不能外推诊断、处方或医院工作流可靠性。

**主要结果：**MedQA 英／中 Accuracy 83%／89%；MedMCQA Accuracy 72%；CMExam 单选 Accuracy 92.6%。

<details>
<summary>查看全部 5 个任务条件 · 400 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [MedQA](docs/场景数据集与实验.md#resource-57) | `medqa_en_test` | 100 | Accuracy | 83.0% |
| [MedQA](docs/场景数据集与实验.md#resource-57) | `medqa_zh_test` | 100 | Accuracy | 89.0% |
| [MedMCQA](docs/场景数据集与实验.md#resource-58) | `medmcqa_validation` | 100 | Accuracy | 72.0% |
| [CMExam](docs/场景数据集与实验.md#resource-59) | `cmexam_mcq` | 95 | Accuracy | 92.6% |
| [CMExam](docs/场景数据集与实验.md#resource-59) | `cmexam_mcq_multi` | 5 | micro-F1 | 75.9% |

</details>

<a id="scene-multimodal"></a>

### 语音病历、OCR、影像报告与信号

实际执行 ASR 与 OCR；仅一段扮演患者音频、六份文档且只有两种模板。影像和 ECG 尚未运行。

**主要结果：**ASR 字段 11/12；OCR 文档类型 5/6；影像／ECG 未测。

<details>
<summary>查看全部 4 个任务条件 · 36 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [PriMock57](docs/场景数据集与实验.md#resource-16) | `primock_asr_fields` | 12 | Accuracy | 91.7% |
| [PriMock57](docs/场景数据集与实验.md#resource-16) | `primock_reference_fields` | 12 | Accuracy | 100.0% |
| [ClinOCR-Bench](docs/场景数据集与实验.md#resource-65) | `clinocr_ocr_doctype` | 6 | Accuracy | 83.3% |
| [ClinOCR-Bench](docs/场景数据集与实验.md#resource-65) | `clinocr_reference_doctype` | 6 | Accuracy | 100.0% |

</details>

<details>
<summary>未测／待补齐：4 项资源</summary>

- [RadGraph](docs/场景数据集与实验.md#resource-63)：需数据访问/许可核实或获准原文。
- [CheXbert](docs/场景数据集与实验.md#resource-64)：需数据访问/许可核实或获准原文。
- [MedMNIST](docs/场景数据集与实验.md#resource-66)：非原生输入。
- [PTB-XL](docs/场景数据集与实验.md#resource-67)：非原生输入。

</details>

<a id="scene-acute"></a>

### 合成病例、急诊、护理与 ICU

当前只有 DDXPlus 合成鉴别诊断实测；使用第三方镜像有限前缀抽样，不能代表急诊或 ICU 验证。

**主要结果：**DDXPlus 合成病例 Accuracy 67%；真实急诊与 ICU 未测。

<details>
<summary>查看全部 1 个任务条件 · 100 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [DDXPlus](docs/场景数据集与实验.md#resource-62) | `ddxplus_synthetic_primary` | 100 | Accuracy | 67.0% |

</details>

<details>
<summary>未测／待补齐：6 项资源</summary>

- [Synthea](docs/场景数据集与实验.md#resource-60)：生成器/待集成。
- [MIMIC-IV / MIMIC-IV-Note](docs/场景数据集与实验.md#resource-61)：需数据访问/许可核实或获准原文。
- [MIMIC-IV-ED](docs/场景数据集与实验.md#resource-75)：需数据访问/许可核实或获准原文。
- [MIMIC-IV-Ext-CDS](docs/场景数据集与实验.md#resource-76)：需数据访问/许可核实或获准原文。
- [eICU Demo](docs/场景数据集与实验.md#resource-77)：缺少本任务独立金标。
- [AmsterdamUMCdb](docs/场景数据集与实验.md#resource-78)：需数据访问/许可核实或获准原文。

</details>

<a id="scene-tcm"></a>

### 中医知识、辨证与安全

单选 Accuracy 与多选 micro-F1 分列；TCM-BEST 安全项为标签一致率，部分标签存在过度拒绝倾向。

**主要结果：**TCM-SD Accuracy 33%；BEST 单／多选分列，安全标签一致率 27%。

<details>
<summary>查看全部 14 个任务条件 · 800 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [TCM-SD](docs/场景数据集与实验.md#resource-79) | `tcm_syndrome` | 100 | Accuracy | 33.0% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_ethics` | 97 | Accuracy | 89.7% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_ethics_multi` | 3 | micro-F1 | 81.8% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_knowledge` | 89 | Accuracy | 91.0% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_knowledge_multi` | 11 | micro-F1 | 79.3% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_location` | 21 | Accuracy | 81.0% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_location_multi` | 79 | micro-F1 | 64.8% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_nature` | 99 | Accuracy | 69.7% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_nature_multi` | 1 | micro-F1 | 80.0% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_principles` | 3 | Accuracy | 100.0% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_principles_multi` | 97 | micro-F1 | 70.3% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_syndrome` | 68 | Accuracy | 80.9% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_syndrome_multi` | 32 | micro-F1 | 52.8% |
| [TCM-BEST4SDT](docs/场景数据集与实验.md#resource-81) | `tcm_best_安全问题` | 100 | Accuracy | 27.0% |

</details>

<details>
<summary>未测／待补齐：2 项资源</summary>

- [TCMEval-SDT](docs/场景数据集与实验.md#resource-80)：无可评分标签。
- [TSD](docs/场景数据集与实验.md#resource-82)：需数据访问/许可核实或获准原文。

</details>

<a id="scene-tools"></a>

### 肿瘤登记、脱敏与临床 NLP 工具

medspaCy 是已运行的候选构造基线，关联的 NCBI 任务只在病历场景计数一次；其余框架未运行。

**主要结果：**medspaCy 基线严格 F1 58.9%；对应 Jev 结果已计入病历场景。

本场景没有额外计入的 Jev 评测记录。

<details>
<summary>未测／待补齐：7 项资源</summary>

- [DeepPhe / DeepPhe-CR](docs/场景数据集与实验.md#resource-83)：替代框架，未运行。
- [EDS-NLP](docs/场景数据集与实验.md#resource-85)：替代框架，未运行。
- [EDS-Pseudo](docs/场景数据集与实验.md#resource-86)：替代框架，未运行。
- [medkit](docs/场景数据集与实验.md#resource-87)：替代框架，未运行。
- [LangExtract](docs/场景数据集与实验.md#resource-88)：替代框架，未运行。
- [MedEvalKit](docs/场景数据集与实验.md#resource-89)：评测框架，未运行。
- [Medmarks](docs/场景数据集与实验.md#resource-90)：评测框架，未运行。

</details>

<a id="scene-challenge"></a>

### 跨场景自编边界挑战

24 类各 4 条，共 96 条；自编且未经独立医生金标验证，不作为真实临床数据集。

**主要结果：**23 类 Accuracy 100%；隐私候选识别 75%；每类仅 4 条。

<details>
<summary>查看全部 24 个任务条件 · 96 条记录</summary>

| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| 自编挑战 | `challenge_allergy_state` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_coding_evidence` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_contradiction` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_document_type` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_documentation` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_dose_link` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_evidence_support` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_experiencer` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_followup_action` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_frequency` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_lab_link` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_medication_change` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_missing_parameter` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_mixed_language` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_negation` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_phi_candidate` | 4 | Accuracy | 75.0% |
| 自编挑战 | `challenge_prompt_injection` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_radiology_assertion` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_relative_date` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_service_route` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_social_context` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_temporality` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_unit_equivalence` | 4 | Accuracy | 100.0% |
| 自编挑战 | `challenge_urgency_given_policy` | 4 | Accuracy | 100.0% |

</details>

## 基线、消融与上下游实验

以下实验复用主评测样本，除鲁棒性的 300 条额外请求外，不再累加记录数。

| 实验 | 对照与结果 | 范围／证据 |
| --- | --- | --- |
| 中文实体抽取 | 词典 F1 42.6% → Jev 候选筛选 F1 59.5% | 100 条；[规则基线](results/offline_baselines.json) |
| 术语归一化 | 简单别名规则 98% → Jev 93% | 100 条；此设置下规则更好；[规则基线](results/offline_baselines.json) |
| 英文实体抽取 | medspaCy F1 58.9% → Jev 筛选 F1 69.4%；FP 467 → 155，FN 364 → 368 | 100 篇；[medspaCy 基线](results/medspacy_results.json)、[Jev 指标](results/all_results.json) |
| 出院带药 | top-5 基线 F1 25.4% → Jev F1 48.6%；候选召回 67.4% | 100 条；[用药基线](results/ablations.json) |
| BMI 参数 + 公式 | 首个候选正确参数对 14/20 → Jev 17/20；候选覆盖 18/20 | 20 病例，对应主表 40 个参数判断；[混合实验](results/ablations.json) |
| MedHallu 证据消融 | 无证据 60% → 有证据 82% | 同 100 问题 × 真／幻觉回答 × 两条件，共 400 条；[结果](results/all_results.json) |
| PUBHEALTH 证据消融 | 仅论断 20% → 提供核查文章 67% | 同 100 论断 × 两条件，共 200 条；文章可能直接包含结论；[结果](results/all_results.json) |
| ASR 误差传播 | Whisper WER 32.2%；参考转写字段 12/12 → ASR 字段 11/12 | 457.92 秒扮演患者音频；[ASR 实验](results/asr_results.json) |
| OCR 误差传播 | 参考文本类型 6/6 → OCR 文本类型 5/6 | Tesseract、六类失真、两种模板；[逐文档 OCR 指标](results/ocr_results.json) |

### 配对鲁棒性：全部 15 组实验

重复调用、轮换选项标签、加入无关说明各 100 条；预测分别改变 **1 / 8 / 3** 条。改变预测不必然意味着变差，所以下表同时报告正确数。

| 原任务 | 扰动 | 记录数 | 预测改变 | 原条件正确数 | 扰动后正确数 |
| --- | --- | ---: | ---: | ---: | ---: |
| `imcs_assertion_oracle_span` | 重复调用 | 20 | 0 | 16 | 16 |
| `imcs_assertion_oracle_span` | 选项标签轮换 | 20 | 0 | 16 | 16 |
| `imcs_assertion_oracle_span` | 加入无关说明 | 20 | 0 | 16 | 16 |
| `medec_error_detection` | 重复调用 | 20 | 0 | 13 | 13 |
| `medec_error_detection` | 选项标签轮换 | 20 | 1 | 13 | 14 |
| `medec_error_detection` | 加入无关说明 | 20 | 0 | 13 | 13 |
| `ddi_relation_oracle_pairs` | 重复调用 | 20 | 1 | 16 | 17 |
| `ddi_relation_oracle_pairs` | 选项标签轮换 | 20 | 1 | 16 | 17 |
| `ddi_relation_oracle_pairs` | 加入无关说明 | 20 | 1 | 16 | 17 |
| `cmedcalc_semantic_grade` | 重复调用 | 20 | 0 | 16 | 16 |
| `cmedcalc_semantic_grade` | 选项标签轮换 | 20 | 6 | 16 | 10 |
| `cmedcalc_semantic_grade` | 加入无关说明 | 20 | 0 | 16 | 16 |
| `cmexam_mcq` | 重复调用 | 20 | 0 | 19 | 19 |
| `cmexam_mcq` | 选项标签轮换 | 20 | 0 | 19 | 19 |
| `cmexam_mcq` | 加入无关说明 | 20 | 2 | 19 | 17 |

数据见 [ablations.json](results/ablations.json)；生成与评分见 [prepare_robustness.py](scripts/prepare_robustness.py)、[analyze_ablations.py](scripts/analyze_ablations.py)。

### 延迟、用量与核验

主评测成功 API 响应的网络延迟 P50 **0.755 秒**、P95 **1.646 秒**；输入 token **8,941,999**。鲁棒性另记录输入 token **285,114**。这些只覆盖留存成功响应，不是完整账单或纯模型推理时间。

全部任务的置信区间与逐类指标见 [结果总表](docs/结果总表.md) 和 [all_results.json](results/all_results.json)；错误示例见 [error_cases.json](results/error_cases.json)。EvidenceBench 的 37 条请求哈希格式修正见 [审计记录](results/hash_normalization_audit.json)，响应未改变。

这些是有限样本、适配任务的探索性结果，不是官方排行榜成绩。闭源模型训练暴露情况未知；多个条件或字段可能来自同一病例。单组和少组 bootstrap 区间不能代表人群泛化，也未证明医院工时节约或临床收益。
<!-- END GENERATED SCENARIOS -->

## 对标与定位

本项目的重点是医疗任务中的候选筛选、分类与证据判断实验。与上游工具的关系、公开社区信号及可复用项目见 [开源项目与社区证据](docs/开源项目与社区.md)。

同系列 **Jev Media Lab** 研究评论审核、情绪／立场、赞助字幕与创作者工作流。原联合研究中医疗与自媒体分开评分，本仓库不包含自媒体任务代码。

## 目录与阅读路径

```text
docs/       调研、方法、患者入组专题与复现说明
scripts/    数据适配、真实 API 调用与评分代码
results/    2026-09-24 聚合结果与样本身份／哈希
examples/   人工构造的接口示例
tests/      无外部服务依赖的仓库与指标检查
```

先读 [医疗研究报告](docs/研究报告.md) 了解结论，再用 [结果总表](docs/结果总表.md) 核对任务指标；准备开展实验时阅读 [复现说明](docs/REPRODUCING.md)。

## 贡献与问题反馈

欢迎通过仓库的 Issue 或 Pull Request 提交数据适配修正、指标问题和复现反馈。请附上任务名称、数据来源与版本、模型版本、运行命令及去除敏感内容的错误信息；新增实验应说明样本选择、金标来源、基线、指标和限制。

提交代码变更前运行上面的离线测试。不要提交原始病历、受限基准全文、音视频、模型权重、凭据或运行缓存。

## 许可与数据说明

仓库代码采用 [MIT License](LICENSE)。数据集、上游项目与服务商输出遵循各自的授权条件，本仓库代码许可不覆盖这些第三方材料，详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

使用数据前需自行确认获取和处理权限；取得数据访问许可，并不自动意味着可以将患者信息发送给第三方云服务。
