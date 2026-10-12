# 治疗方案选择

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 根据病例选择治疗，方向适合；与用药、补液等细分任务按层级组织，避免任务拆分影响权重。

## 任务是什么

根据病例从给定候选中选择治疗。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `treatment_choice` |
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
| [CMB-Exam（中文病例单选子集）](../datasets/cmb.md) | 46 | [原始来源](https://github.com/FreedomIntelligence/CMB) |
| [CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md) | 54 | [原始来源](https://doi.org/10.5281/zenodo.18951465) |

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
| JEV 1.13 | 78.00% | 100 / 100 | 0.923 | 0.885 | 1.122 | 12.639 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | **82.00%** | 100 / 100 | **0.454** | **0.439** | **0.640** | **6.052** | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 74.00% | 100 / 100 | 0.946 | 0.923 | 1.279 | 12.260 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 51.00% | 100 / 100 | 0.861 | 0.627 | 2.070 | 12.156 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 72.00% | 100 / 100 | 2.486 | 1.781 | 7.001 | 31.418 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

持续多题并发尚未测试。以下为历史有限批次结果，不作为高并发高吞吐证据。

### 历史有限批次测试

固定本任务 32 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

历史多题结果（固定最大打包档，对比 Flash）：JEV 84.38%，Flash 75.00%；JEV 耗时多 1.2%；JEV 成本低 8.3%–54.2%。具体准确率与费用仅对应下述性能子集，不代表全量成绩或其他调用方式。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 84.38% | 8.397 | 3.81 / 3.22 | 96 / 96 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 75.00% | 20.481 | 1.56 / 1.17 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | JEV 1.13 | 84.38% | 1.689 | 18.95 / 15.99 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 75.00% | 3.076 | 10.40 / 7.80 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | JEV 1.13 | 84.38% | 0.603 | 53.09 / 44.79 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | DeepSeek V4.1 Flash | 78.12% | 1.014 | 31.57 / 24.66 | 96 / 96 | 0 |
| 多题打包 | 1 | 8 | JEV 1.13 | 90.62% | 0.997 | 32.11 / 29.10 | 12 / 12 | 0 |
| 多题打包 | 1 | 8 | DeepSeek V4.1 Flash | 72.92% | 3.158 | 9.71 / 7.39 | 8 / 12 | 4 |
| 多题打包 | 1 | 32 | JEV 1.13 | 84.38% | 1.079 | 29.65 / 25.02 | 3 / 3 | 0 |
| 多题打包 | 1 | 32 | DeepSeek V4.1 Flash | 75.00% | 1.066 | 30.02 / 22.51 | 3 / 3 | 0 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 7.896–9.310 | 0.254 | 0.308 | 0.641 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-150.jsonl) · [轮2](../../results/task-performance-v1/cell-259.jsonl) · [轮3](../../results/task-performance-v1/cell-532.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 18.324–21.914 | 0.599 | 1.049 | 1.394 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-055.jsonl) · [轮2](../../results/task-performance-v1/cell-251.jsonl) · [轮3](../../results/task-performance-v1/cell-698.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 1.180–2.106 | 0.274 | 0.986 | 1.582 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-061.jsonl) · [轮2](../../results/task-performance-v1/cell-254.jsonl) · [轮3](../../results/task-performance-v1/cell-617.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 2.977–3.177 | 0.629 | 0.905 | 1.220 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-084.jsonl) · [轮2](../../results/task-performance-v1/cell-362.jsonl) · [轮3](../../results/task-performance-v1/cell-687.jsonl) |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.332–1.131 | 0.261 | 0.584 | 1.123 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-191.jsonl) · [轮2](../../results/task-performance-v1/cell-334.jsonl) · [轮3](../../results/task-performance-v1/cell-579.jsonl) |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.874–1.178 | 0.645 | 0.959 | 1.173 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-149.jsonl) · [轮2](../../results/task-performance-v1/cell-265.jsonl) · [轮3](../../results/task-performance-v1/cell-552.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.933–1.055 | 0.240 | 样本不足 | 0.286 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-169.jsonl) · [轮2](../../results/task-performance-v1/cell-419.jsonl) · [轮3](../../results/task-performance-v1/cell-520.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 2.876–3.399 | 0.796 | 样本不足 | 0.998 | 0 | 0 / 0 / 4 | [轮1](../../results/task-performance-v1/cell-041.jsonl) · [轮2](../../results/task-performance-v1/cell-462.jsonl) · [轮3](../../results/task-performance-v1/cell-628.jsonl) |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.281–1.976 | 0.981 | 样本不足 | 1.976 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-180.jsonl) · [轮2](../../results/task-performance-v1/cell-395.jsonl) · [轮3](../../results/task-performance-v1/cell-485.jsonl) |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.913–1.198 | 1.087 | 样本不足 | 1.198 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-210.jsonl) · [轮2](../../results/task-performance-v1/cell-311.jsonl) · [轮3](../../results/task-performance-v1/cell-539.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0247 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0464–0.0928 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.0247 | 0 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 0.0464–0.0928 | 0 |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.0247 | 0 |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.0446–0.0892 | 0 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0142 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 0.0213–0.0426 | 0 |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.0140 | 0 |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.0153–0.0305 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`treatment_choice:cmb:478`；语种：中文；来源组：`zh_exam_case:e8306f4273b636a7d483603d`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "阳明经穴",
        "B": "太阳经穴",
        "C": "少阳经穴",
        "D": "督脉经穴",
        "E": "厥阴经穴"
      },
      "instructions": "根据病例从给定候选中选择治疗。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "患者，男，47岁。下肢弛缓无力1年余，肌肉明显萎缩，功能严重受限，并感麻木，发凉，腰酸，头晕，舌红少苔，脉细数。治疗应首选"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `A`，对应选项：

```json
"阳明经穴"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "treatment_choice:cmb:478", "choice": "A"}
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
    "answer_json_index": 477,
    "json_index": 477,
    "question_id": 478,
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
  "upstream_group": "478",
  "upstream_id": "478",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：A 8 题、B 10 题、C 10 题、D 10 题、E 8 题、opa 11 题、opb 11 题、opc 10 题、opd 11 题、ope 11 题。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

**[CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md)**：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。 答案依据：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

其中 3 题材料或片段命中过往评测指纹；训练效果对比应核查材料暴露，并对各模型冻结相同子集。

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

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/treatment_choice/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/treatment_choice/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
