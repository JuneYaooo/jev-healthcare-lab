# 检查方案选择

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 根据病例选择检查，属于诊断流程决策；应保留原题信息与原选项。

## 任务是什么

根据病例从给定候选中选择检查。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `examination_choice` |
| 医疗场景 | 检查与检验 |
| 能力维度 | 临床候选方案 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 中文 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CMB-Exam（中文病例单选子集）](../datasets/cmb.md) | 19 | [原始来源](https://github.com/FreedomIntelligence/CMB) |
| [CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md) | 81 | [原始来源](https://doi.org/10.5281/zenodo.18951465) |

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
| JEV 1.13 | **88.00%** | 100 / 100 | 0.954 | 0.946 | 1.139 | 12.449 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 81.00% | 98 / 100 | **0.479** | **0.448** | **0.768** | **6.302** | 0 / 0 / 2 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 74.00% | 100 / 100 | 0.954 | 0.932 | 1.284 | 12.363 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 60.00% | 100 / 100 | 1.188 | 0.653 | 4.383 | 16.815 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 74.00% | 100 / 100 | 2.366 | 1.906 | 8.354 | 30.966 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

固定本任务 32 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 87.50% | 8.817 | 3.63 / 3.18 | 96 / 96 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 85.42% | 20.961 | 1.49 / 1.30 | 94 / 96 | 2 |
| 逐题 | 8 | 1 | JEV 1.13 | 87.50% | 1.353 | 23.64 / 20.69 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 83.33% | 2.825 | 10.97 / 9.44 | 93 / 96 | 3 |
| 逐题 | 32 | 1 | JEV 1.13 | 87.50% | 1.136 | 28.16 / 24.64 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | DeepSeek V4.1 Flash | 84.38% | 1.023 | 30.31 / 26.40 | 93 / 96 | 3 |
| 多题打包 | 1 | 8 | JEV 1.13 | 85.42% | 1.279 | 25.01 / 21.37 | 12 / 12 | 0 |
| 多题打包 | 1 | 8 | DeepSeek V4.1 Flash | 79.17% | 2.804 | 9.63 / 9.03 | 6 / 12 | 6 |
| 多题打包 | 1 | 32 | JEV 1.13 | 80.21% | 0.404 | 79.26 / 63.57 | 3 / 3 | 0 |
| 多题打包 | 1 | 32 | DeepSeek V4.1 Flash | 38.54% | 1.164 | 11.74 / 10.59 | 0 / 3 | 3 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 8.111–9.229 | 0.266 | 0.314 | 0.793 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-095.jsonl) · [轮2](../../results/task-performance-v1/cell-348.jsonl) · [轮3](../../results/task-performance-v1/cell-560.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 20.141–21.511 | 0.636 | 1.011 | 1.126 | 0 | 0 / 0 / 2 | [轮1](../../results/task-performance-v1/cell-079.jsonl) · [轮2](../../results/task-performance-v1/cell-450.jsonl) · [轮3](../../results/task-performance-v1/cell-533.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 1.072–1.754 | 0.271 | 0.834 | 0.868 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-063.jsonl) · [轮2](../../results/task-performance-v1/cell-279.jsonl) · [轮3](../../results/task-performance-v1/cell-595.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 2.629–2.950 | 0.642 | 0.851 | 0.912 | 0 | 0 / 0 / 3 | [轮1](../../results/task-performance-v1/cell-065.jsonl) · [轮2](../../results/task-performance-v1/cell-453.jsonl) · [轮3](../../results/task-performance-v1/cell-696.jsonl) |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.402–2.041 | 0.310 | 0.952 | 2.028 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-189.jsonl) · [轮2](../../results/task-performance-v1/cell-255.jsonl) · [轮3](../../results/task-performance-v1/cell-652.jsonl) |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.852–1.215 | 0.666 | 1.092 | 1.207 | 0 | 1 / 0 / 2 | [轮1](../../results/task-performance-v1/cell-157.jsonl) · [轮2](../../results/task-performance-v1/cell-464.jsonl) · [轮3](../../results/task-performance-v1/cell-564.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 1.055–1.572 | 0.276 | 样本不足 | 0.735 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-090.jsonl) · [轮2](../../results/task-performance-v1/cell-455.jsonl) · [轮3](../../results/task-performance-v1/cell-618.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 2.663–2.930 | 0.623 | 样本不足 | 0.972 | 0 | 0 / 0 / 6 | [轮1](../../results/task-performance-v1/cell-096.jsonl) · [轮2](../../results/task-performance-v1/cell-325.jsonl) · [轮3](../../results/task-performance-v1/cell-637.jsonl) |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.320–0.488 | 0.403 | 样本不足 | 0.488 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-002.jsonl) · [轮2](../../results/task-performance-v1/cell-276.jsonl) · [轮3](../../results/task-performance-v1/cell-613.jsonl) |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 1.013–1.281 | 1.198 | 样本不足 | 1.281 | 0 | 0 / 0 / 3 | [轮1](../../results/task-performance-v1/cell-132.jsonl) · [轮2](../../results/task-performance-v1/cell-350.jsonl) · [轮3](../../results/task-performance-v1/cell-482.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0233 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0433–0.0867 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.0233 | 0 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 0.0444–0.0889 | 0 |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.0233 | 0 |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | — | 1 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0145 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 0.0196–0.0392 | 0 |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.0141 | 0 |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.0299–0.0598 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`examination_choice:cmb:2934`；语种：中文；来源组：`zh_exam_case:15de54b6c663a3209027eba5`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "化验胃酸",
        "B": "胃镜",
        "C": "CT",
        "D": "B超",
        "E": "化验血常规"
      },
      "instructions": "根据病例从给定候选中选择检查。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "患者，男性，37岁，1年来每日发生空腹痛，进食后疼痛缓解。平时伴有恶心、打嗝、反酸，査体在剑突右侧有局限压痛，无反跳痛。做何种检查可以确诊"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `B`，对应选项：

```json
"胃镜"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "examination_choice:cmb:2934", "choice": "B"}
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
    "answer_json_index": 2933,
    "json_index": 2933,
    "question_id": 2934,
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
  "upstream_group": "2934",
  "upstream_id": "2934",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：A 1 题、B 6 题、C 4 题、D 5 题、E 3 题、opa 16 题、opb 16 题、opc 16 题、opd 17 题、ope 16 题。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

**[CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md)**：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。 答案依据：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [CMExam](../datasets/cmexam.md) | Apache 标识与 README 学术/研究限制并存，先澄清数据授权范围；病例题也需筛选。 |
| [MedJourney](../datasets/medjourney.md) | 未见明确数据许可；部分任务共用 CMB/CMExam 上游 |
| [MedMCQA](../datasets/medmcqa.md) | 本任务暂无收录，是否适用需按任务定义核验。 |
| [MedXpertQA](../datasets/medxpertqa.md) | 论文附录提出不在线分享题例；在与 MIT 数据卡的适用范围澄清前仅引用，不在本仓库再分发题目。 |
| [MLEC-QA](../datasets/mlec_qa.md) | 需下载官方包核对独立数据许可、测试划分和共享题干；仅收病例决策单选。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/examination_choice/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/examination_choice/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
