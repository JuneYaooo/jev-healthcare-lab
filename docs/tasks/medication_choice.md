# 用药方案选择

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 根据病例选药，方向适合；不是药物实体匹配，需与后者严格区分。

## 任务是什么

根据病例从给定候选中选择用药。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `medication_choice` |
| 医疗场景 | 治疗与用药 |
| 能力维度 | 临床候选方案 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 中文 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CMB-Exam（中文病例单选子集）](../datasets/cmb.md) | 12 | [原始来源](https://github.com/FreedomIntelligence/CMB) |
| [CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md) | 88 | [原始来源](https://doi.org/10.5281/zenodo.18951465) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下成绩使用本页全部已收录题目；耗时包括请求、响应处理及重试等待。

有效回答表示返回合法选项，不代表正确；平均值和分位数包含已启动题目的失败耗时。任务总秒为含并发调度的墙钟时间，不是单题耗时之和。响应链接包含该模型全部题目，可按本页任务的题目 ID 查找。

加粗表示本任务的最高准确率或最短用时；按显示精度并列时同时加粗，全部相同则不标记。

| 模型 | 准确率 ↑ | 有效回答 / 题数 | 平均秒 ↓ | P50 秒 ↓ | P95 秒 ↓ | 任务总秒 ↓ | 超时 / 请求失败 / 无效回答 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | **83.00%** | 100 / 100 | 0.960 | 0.937 | 1.152 | 12.514 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 80.00% | 100 / 100 | **0.519** | **0.486** | **0.946** | **7.049** | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 72.00% | 100 / 100 | 0.978 | 0.935 | 1.329 | 12.794 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 47.00% | 100 / 100 | 1.217 | 0.637 | 4.687 | 15.627 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 73.00% | 100 / 100 | 1.595 | 1.583 | 1.964 | 20.732 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

固定本任务 32 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 84.38% | 8.040 | 3.98 / 3.36 | 96 / 96 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 83.33% | 19.127 | 1.67 / 1.39 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | JEV 1.13 | 82.29% | 1.276 | 25.08 / 20.64 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 84.38% | 2.997 | 10.68 / 9.01 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | JEV 1.13 | 84.38% | 0.584 | 54.77 / 46.22 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | DeepSeek V4.1 Flash | 82.29% | 5.737 | 5.52 / 4.59 | 95 / 96 | 1 |
| 多题打包 | 1 | 8 | JEV 1.13 | 76.04% | 1.600 | 20.00 / 15.20 | 12 / 12 | 0 |
| 多题打包 | 1 | 8 | DeepSeek V4.1 Flash | 67.71% | 3.019 | 9.39 / 7.18 | 8 / 12 | 4 |
| 多题打包 | 1 | 32 | JEV 1.13 | 77.08% | 0.497 | 64.37 / 49.62 | 3 / 3 | 0 |
| 多题打包 | 1 | 32 | DeepSeek V4.1 Flash | 67.71% | 1.253 | 25.02 / 17.30 | 2 / 3 | 1 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 7.678–8.527 | 0.241 | 0.287 | 0.739 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-033.jsonl) · [轮2](../../results/task-performance-v1/cell-465.jsonl) · [轮3](../../results/task-performance-v1/cell-525.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 18.472–19.880 | 0.589 | 0.860 | 1.136 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-078.jsonl) · [轮2](../../results/task-performance-v1/cell-353.jsonl) · [轮3](../../results/task-performance-v1/cell-616.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 1.027–1.759 | 0.250 | 0.907 | 0.949 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-036.jsonl) · [轮2](../../results/task-performance-v1/cell-373.jsonl) · [轮3](../../results/task-performance-v1/cell-701.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 2.797–3.243 | 0.648 | 0.963 | 1.275 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-058.jsonl) · [轮2](../../results/task-performance-v1/cell-312.jsonl) · [轮3](../../results/task-performance-v1/cell-635.jsonl) |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.338–0.806 | 0.275 | 0.353 | 0.799 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-209.jsonl) · [轮2](../../results/task-performance-v1/cell-266.jsonl) · [轮3](../../results/task-performance-v1/cell-586.jsonl) |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.807–15.365 | 0.662 | 1.153 | 15.363 | 0 | 1 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-101.jsonl) · [轮2](../../results/task-performance-v1/cell-329.jsonl) · [轮3](../../results/task-performance-v1/cell-682.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 1.321–1.889 | 0.309 | 样本不足 | 0.998 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-043.jsonl) · [轮2](../../results/task-performance-v1/cell-425.jsonl) · [轮3](../../results/task-performance-v1/cell-657.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 2.732–3.358 | 0.669 | 样本不足 | 1.153 | 0 | 1 / 0 / 3 | [轮1](../../results/task-performance-v1/cell-174.jsonl) · [轮2](../../results/task-performance-v1/cell-390.jsonl) · [轮3](../../results/task-performance-v1/cell-497.jsonl) |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.285–0.608 | 0.598 | 样本不足 | 0.608 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-076.jsonl) · [轮2](../../results/task-performance-v1/cell-384.jsonl) · [轮3](../../results/task-performance-v1/cell-565.jsonl) |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 1.121–1.344 | 1.293 | 样本不足 | 1.344 | 0 | 0 / 0 / 1 | [轮1](../../results/task-performance-v1/cell-185.jsonl) · [轮2](../../results/task-performance-v1/cell-469.jsonl) · [轮3](../../results/task-performance-v1/cell-536.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0246 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0418–0.0836 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.0253 | 0 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 0.0413–0.0825 | 0 |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.0246 | 0 |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | — | 1 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0168 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | — | 1 |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.0152 | 0 |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.0180–0.0360 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`medication_choice:cmb:484`；语种：中文；来源组：`zh_exam_case:8a058cac7751eb24e2eaf744`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "止带方",
        "B": "知柏地黄丸",
        "C": "完带汤",
        "D": "六味地黄丸",
        "E": "内补丸"
      },
      "instructions": "根据病例从给定候选中选择用药。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "患者，女，30岁，已婚。近感带下量增多，伴阴道灼热、干涩，腰膝酸软，头晕耳鸣，五心烦热，舌红苔黄，脉细数。治疗首选方剂为"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `B`，对应选项：

```json
"知柏地黄丸"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "medication_choice:cmb:484", "choice": "B"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip) · [数据集说明](../datasets/cmb.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "Apache-2.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_field": "answer",
    "answer_json_index": 483,
    "json_index": 483,
    "question_id": 484,
    "supporting_resources": [
      "cmb__CMB-test-choice-answer.json"
    ],
    "zip_member": "CMB/CMB-Exam/CMB-test/CMB-test-choice-question-merge.json"
  },
  "material_kind": "medical_examination_vignettes",
  "resource": "cmb__CMB.zip",
  "resource_sha256": "c2e4288127fa5e6c03cc3659d893b0bbb19e699f74fdadce8e7fa10ac5bfdd94",
  "resource_url": "https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip",
  "source_id": "cmb",
  "source_url": "https://github.com/FreedomIntelligence/CMB",
  "split": "official_test",
  "upstream_group": "484",
  "upstream_id": "484",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：A 1 题、B 4 题、C 6 题、D 1 题、opa 20 题、opb 18 题、opc 16 题、opd 21 题、ope 13 题。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

**[CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md)**：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。 答案依据：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [CDrugRed](../datasets/cdrugred.md) | 下载入口与官方数据包许可链待核验 |
| [CMExam](../datasets/cmexam.md) | Apache 标识与 README 学术/研究限制并存，先澄清数据授权范围；病例题也需筛选。 |
| [MedJourney](../datasets/medjourney.md) | 未见明确数据许可；部分任务共用 CMB/CMExam 上游 |
| [MedMCQA](../datasets/medmcqa.md) | 本任务暂无收录，是否适用需按任务定义核验。 |
| [MedXpertQA](../datasets/medxpertqa.md) | 论文附录提出不在线分享题例；在与 MIT 数据卡的适用范围澄清前仅引用，不在本仓库再分发题目。 |
| [MLEC-QA](../datasets/mlec_qa.md) | 需下载官方包核对独立数据许可、测试划分和共享题干；仅收病例决策单选。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/medication_choice/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/medication_choice/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
