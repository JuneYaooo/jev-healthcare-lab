# 中医候选病机判断

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 属于诊断相关判断；100 题来自 50 病例，判断是否在原答案集合内，不是 100 个独立诊断病例或原多选整题准确率。

## 任务是什么

根据病例和原始候选病机，判断目标候选是否被上游专家选中。否仅表示不属于本题原始答案集合，不表示医学上不可能。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `tcm_pathogenesis_candidate` |
| 医疗场景 | 诊断与鉴别 |
| 能力维度 | 分类与标准化 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 50 |
| 语种 | 中文 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [TCMEval-SDT](../datasets/tcmeval_sdt.md) | 100 | [原始来源](https://doi.org/10.6084/m9.figshare.27184596.v5) |

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
| JEV 1.13 | 67.00% | 100 / 100 | 1.666 | 1.028 | 5.399 | 31.244 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 76.00% | 100 / 100 | **0.430** | **0.426** | **0.601** | **5.571** | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | **79.00%** | 100 / 100 | 1.101 | 1.011 | 1.760 | 14.190 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 70.00% | 100 / 100 | 1.012 | 0.610 | 2.318 | 20.477 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 75.00% | 100 / 100 | 3.760 | 1.233 | 2.583 | 125.480 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

本轮多题结果（固定最大打包档，对比 Flash）：JEV 69.79%，Flash 83.33%；JEV 耗时少 8.4%；取决于 Flash 闲时／高峰价格。具体准确率与费用仅对应下述性能子集，不代表全量成绩或其他调用方式。

固定本任务 32 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 65.62% | 8.936 | 3.58 / 2.35 | 96 / 96 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 81.25% | 20.166 | 1.59 / 1.29 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | JEV 1.13 | 65.62% | 1.557 | 20.34 / 13.49 | 95 / 96 | 1 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 80.21% | 2.949 | 10.74 / 8.70 | 95 / 96 | 1 |
| 逐题 | 32 | 1 | JEV 1.13 | 64.58% | 1.456 | 21.98 / 14.19 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | DeepSeek V4.1 Flash | 80.21% | 1.427 | 22.19 / 17.99 | 95 / 96 | 1 |
| 多题打包 | 1 | 8 | JEV 1.13 | 69.79% | 11.348 | 2.82 / 1.97 | 12 / 12 | 0 |
| 多题打包 | 1 | 8 | DeepSeek V4.1 Flash | 87.50% | 3.035 | 10.54 / 9.23 | 12 / 12 | 0 |
| 多题打包 | 1 | 32 | JEV 1.13 | 69.79% | 1.108 | 28.89 / 20.17 | 3 / 3 | 0 |
| 多题打包 | 1 | 32 | DeepSeek V4.1 Flash | 83.33% | 1.209 | 26.47 / 22.06 | 3 / 3 | 0 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 7.674–9.657 | 0.272 | 0.330 | 0.879 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-123.jsonl) · [轮2](../../results/task-performance-v1/cell-309.jsonl) · [轮3](../../results/task-performance-v1/cell-645.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 18.796–21.987 | 0.632 | 0.884 | 1.221 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-108.jsonl) · [轮2](../../results/task-performance-v1/cell-310.jsonl) · [轮3](../../results/task-performance-v1/cell-544.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 1.275–1.838 | 0.273 | 0.937 | 1.097 | 0 | 1 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-045.jsonl) · [轮2](../../results/task-performance-v1/cell-282.jsonl) · [轮3](../../results/task-performance-v1/cell-490.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 2.675–3.436 | 0.638 | 1.153 | 1.522 | 0 | 1 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-008.jsonl) · [轮2](../../results/task-performance-v1/cell-326.jsonl) · [轮3](../../results/task-performance-v1/cell-604.jsonl) |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.717–2.649 | 0.598 | 1.286 | 2.646 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-219.jsonl) · [轮2](../../results/task-performance-v1/cell-378.jsonl) · [轮3](../../results/task-performance-v1/cell-598.jsonl) |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 1.215–1.547 | 0.850 | 1.486 | 1.544 | 0 | 1 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-222.jsonl) · [轮2](../../results/task-performance-v1/cell-466.jsonl) · [轮3](../../results/task-performance-v1/cell-572.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 1.173–31.689 | 0.268 | 样本不足 | 30.889 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-003.jsonl) · [轮2](../../results/task-performance-v1/cell-280.jsonl) · [轮3](../../results/task-performance-v1/cell-494.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 2.914–3.257 | 0.685 | 样本不足 | 1.140 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-087.jsonl) · [轮2](../../results/task-performance-v1/cell-412.jsonl) · [轮3](../../results/task-performance-v1/cell-662.jsonl) |
| 多题打包 B≤32 / C1 | JEV 1.13 | 1.001–1.288 | 1.033 | 样本不足 | 1.288 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-109.jsonl) · [轮2](../../results/task-performance-v1/cell-435.jsonl) · [轮3](../../results/task-performance-v1/cell-675.jsonl) |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 1.150–1.261 | 1.215 | 样本不足 | 1.261 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-190.jsonl) · [轮2](../../results/task-performance-v1/cell-416.jsonl) · [轮3](../../results/task-performance-v1/cell-557.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0454 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0414–0.0827 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | — | 1 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | — | 1 |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.0461 | 0 |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | — | 1 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0312 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 0.0223–0.0446 | 0 |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.0297 | 0 |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.0230–0.0460 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`tcm_pathogenesis_candidate:tcmeval_sdt:病例252:J`；语种：中文；来源组：`tcmeval_sdt:病例252`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "no": "不属于本题上游所选病机集合",
        "yes": "属于上游专家所选病机集合"
      },
      "instructions": "根据病例和原始候选病机，判断目标候选是否被上游专家选中。否仅表示不属于本题原始答案集合，不表示医学上不可能。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_case": "25岁。主诉及病史：体质素弱，骤然血崩不止，唇甲俱白，目合神昏，额汗如珠，手足逆冷。诊查：脉濡舌淡。",
    "original_candidates": {
      "A": "血海失营",
      "B": "肝肾之阴不足",
      "C": "冲任受损",
      "D": "血不归经",
      "E": "脾不统血",
      "F": "痰火互结",
      "G": "热病伤阴",
      "H": "痰浊阻膈",
      "I": "气滞血瘀",
      "J": "血虚"
    },
    "target_candidate": {
      "key": "J",
      "text": "血虚"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `no`，对应选项：

```json
"不属于本题上游所选病机集合"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "tcm_pathogenesis_candidate:tcmeval_sdt:病例252:J", "choice": "no"}
```

### 样例溯源

[上游资源](https://ndownloader.figshare.com/files/51198842) · [数据集说明](../datasets/tcmeval_sdt.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_field_zero_based": 2,
    "answer_line": 16,
    "case_id": "病例252",
    "json_index": 15,
    "supporting_resources": [
      "tcmeval_sdt__Test_data_result.txt"
    ]
  },
  "material_kind": "curated_case_and_expert_annotation",
  "resource": "tcmeval_sdt__Test_TCM_Data_v1.json",
  "resource_sha256": "4b9f69308b46125ea6d979613d4b2717b1d930d7acefd2e3c58d274975420bff",
  "resource_url": "https://ndownloader.figshare.com/files/51198842",
  "source_id": "tcmeval_sdt",
  "source_url": "https://doi.org/10.6084/m9.figshare.27184596.v5",
  "split": "official_test",
  "upstream_group": "病例252",
  "upstream_id": "病例252:J",
  "version": "Figshare 27184596.v5"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：no 50 题、yes 50 题。

**[TCMEval-SDT](../datasets/tcmeval_sdt.md)**：整理的经典医案、网络及医院病例材料；不是统一采集的前瞻性患者队列。 答案依据：v5 官方测试答案按病例 ID 连接；从病机多选答案机械映射候选是否入选。

固定发布版本的上游答案；未作本项目独立临床或现行规范核验。数据许可按 Figshare 数据记录，区别于论文或仓库其他内容许可。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/tcm_pathogenesis_candidate/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/tcm_pathogenesis_candidate/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
