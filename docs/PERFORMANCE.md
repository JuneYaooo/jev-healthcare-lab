# 性能测试协议

[首页](../README.md) · [结果](PERFORMANCE_RESULTS.md) · [冻结数据](../benchmarks/performance_v1/README.md)

本组比较 JEV 1.13 与 DeepSeek V4.1 Flash 的客户端 API 性能。原有 1,514 题临床准确率榜单保持独立；单题、多问题、并发是不同测试维度。

## 数据是否需要扩充

并发扩展不需要新临床数据。本次从现有开放许可临床子集按任务轮转抽取 128 道，覆盖 24 个源任务 ID，病例诊断的两个来源任务仍属于同一个临床任务族。样本用于相同工作量下的吞吐比较，不重新定义临床主分数。小任务取尽后继续轮转其他任务，不按模型答对情况筛选。

现有开放许可临床题按完整 state 精确匹配，同一份材料最多只有两题，无法直接组成固定材料、50～200 个不同问题的工作负载。因此新增独立合成性能数据：三份文档受理看板，检查身份、文档完整性、授权状态，并按明确规则从四个受理动作中选择。金标由代码机械计算，保存在模型输入之外。合成数据简单且有显式规则，只能评估延迟扩展、有效吞吐和输出完整性。

如果要声称“真实医疗多字段决策更好”，还需单独建设同一病历的多项独立标注集，具备来源许可、逐项金标及专业审核。当前结果不作此类推断。

## 实验矩阵

| 组别 | 不变部分 | 扩展维度 | 每档样本 |
| --- | --- | --- | --- |
| 临床单题并发 | 同一组 128 道题，每请求一个 Choice | 并发 1、8、16、32、64 | 3 轮，共 384 请求 |
| 单请求多问题 | 每轮固定 200 条记录及规则 | 每请求 1、10、50、100、200 个不同 Choice | 3 份看板，各一请求 |

全部单元的执行顺序在调用前写入 config.json。每轮先用固定种子打乱模型和档位顺序，运行单元之间间隔 1 秒，所有模型顺序运行。并发组每轮的样本顺序固定，各模型、各并发档一致。采用有限批次、闭环工作线程池：一条请求完成后该线程领取下一题。它不是固定到达率压测，不能测出持续容量或完整排队服务等级。64 路仅约两波请求；需要容量规划时应增加独立样本数与持续时间。

每个工作线程持有独立 requests.Session，复用 HTTP/1.1 连接；每个单元重新建池。没有隐含热身；首个连接建立也计时。客户端连接超时 10 秒、读取空闲超时 120 秒（不是严格总时长截止）。请求超时、429、其他 HTTP 错误均保留；自动重试为 0。401/402/403 停止剩余工作。未完成的测试单元不续接成一个墙钟结果。

临床单题完全复用 `run_model_evaluation.py` 的请求体与提示；Flash 输出为 `{"choice":"选项键"}`。多问题组统一要求 `{"q000":{"choice":"A"},...}`；Jev 使用原生 questions。Flash temperature=0、关闭思考、JSON object 模式；输出上限为 max(256, 32×问题数)。双方材料、问题、选项和必须完成的业务决策相同。Jev 额外返回概率分布，不要求 Flash 生成未经验证的自报概率。

## 计量与完整性

- 完整请求耗时：从工作线程领取题目到完整响应读完、JSON 解析及答案验证结束；包含序列化、网络和服务端处理，不含客户端任务队列。
- 排队与完成时间：分别保留相对于批次起点的 queue_s 与 completion_s。批次墙钟含调度和连接清理，不含落盘；不把 128 道的单题平均耗时当成整批完成时间。
- 有效／正确决策吞吐：有效／正确业务决策总数除以整批墙钟。分别报告请求数和决策数，多问题不把一次请求当作一次决策。
- 逐项合法性与整包完整性分开：遗漏、额外键、错误类型使整包不完整；仍单列其他合法条目。截断、不可解析 JSON 或重复键无法可靠使用，整包计无效；不自动修复。
- 准确率分母包含全部预定决策，包括请求失败。多问题另报全项正确率；不能用“多数条目对了”代替整包可用。
- 并发组展示完整请求 P50/P95/P99；多问题每档只有 3 请求，展示中位数和范围，不用三个样本估计尾延迟。
- 成本按各供应商实际 usage 和冻结价目估算，Flash 包含缓存命中、未命中与输出。输出 token 上限不是实际输出量；Jev usage 即使含 output_tokens 也不收费。Flash 同时列闲时／高峰上下界，不冒充账单。无 usage 的失败单列，单位成本不当作完整费用展示。

题目、提示、配置、执行顺序、运行代码与原始响应均归档，金标不发给 API。报告脚本从原始响应重新校验每道题，验证请求哈希、决策计数、完整率、成本和时间。重复运行使用相同问题，服务端缓存自动生效且不可控；不是冷缓存实验。各来源 tokenizer 不同，不能把 token 数差异解释为模型能力差异。

价格与限制参考：[TypeSafe 模型说明](https://docs.typesafe.ai/models)、[多问题并行](https://docs.typesafe.ai/patterns/fan-out)、[DeepSeek 价格](https://api-docs.deepseek.com/quick_start/pricing/)、[限流说明](https://api-docs.deepseek.com/quick_start/rate_limit/)。并发限制与每秒请求／token 限制不是同一个量，均可能随服务商调整。

## 复现

```bash
python3 -m pip install -r requirements-performance.txt
python3 -m unittest discover -s tests -p 'test_performance_evaluation.py'
# 使用已冻结数据运行；读取环境变量或根目录 .env 中的 TYPESAFE_API_KEY / DEEPSEEK_API_KEY。
# 运行会产生 API 费用；输出目录必须不存在。
python3 scripts/run_performance_evaluation.py run --output work/performance-new-run
# 对仓库内正式档案重新验算并检查生成报告，不调用 API。
python3 scripts/build_performance_report.py --check
# 可选：从已验算结果重绘曲线。
python3 scripts/generate_performance_visuals.py
```

重新生成数据需指定新的、不存在的目录：`python3 scripts/run_performance_evaluation.py prepare --dataset work/performance-new-data`。试跑可加 `--smoke`，只检查 1 问与 200 问端点；试跑不能作为完整对比报告发布。
