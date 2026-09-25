# 边界挑战：服务路由：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| service_route:1 | {"note": "我想把下周的挂号改到周五。"}… | 1 | 100.0% | 100.0% |
| service_route:2 | {"note": "检查做完了，在哪里下载报告？"}… | 1 | 100.0% | 100.0% |
| service_route:3 | {"note": "同一次检查好像扣了两次钱。"}… | 1 | 100.0% | 100.0% |
| service_route:4 | {"note": "出院带的药应该饭前还是饭后服？"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:1 | {"note": "挂号时间能换到下周吗？"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:2 | {"note": "我想取消今天的门诊预约。"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:3 | {"note": "找不到预约入口，怎么挂号？"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:4 | {"note": "原医生停诊，可以帮我改约吗？"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:5 | {"note": "化验报告在哪里领取？"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:6 | {"note": "影像报告的下载链接失效了。"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:7 | {"note": "我想打印上次的检查结果。"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:8 | {"note": "结果已经出了，如何发给我？"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:9 | {"note": "这笔门诊费为何重复扣款？"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:10 | {"note": "能补开检查费用发票吗？"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:11 | {"note": "取消挂号后退款到哪里？"}… | 1 | 0.0% | 100.0% |
| expansion:service_route:12 | {"note": "请解释账单中这项收费。"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:13 | {"note": "处方上的药应该什么时候服？"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:14 | {"note": "出院药漏服了一次，应咨询谁？"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:15 | {"note": "药品说明的用法与处方不同，帮我核实。"}… | 1 | 100.0% | 100.0% |
| expansion:service_route:16 | {"note": "这两盒药的服用顺序需要确认。"}… | 1 | 100.0% | 100.0% |
