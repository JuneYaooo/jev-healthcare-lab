# 边界挑战：事件时态：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| temporality:1 | {"note": "去年曾胸痛，此后未再发作。"}… | 1 | 100.0% | 100.0% |
| temporality:2 | {"note": "胸痛至今未缓解。"}… | 1 | 100.0% | 100.0% |
| temporality:3 | {"note": "如出现胸痛，请及时就诊。当前未报告胸痛。"}… | 1 | 100.0% | 0.0% |
| temporality:4 | {"note": "胸痛情况：未采集。"}… | 1 | 100.0% | 100.0% |
| expansion:temporality:1 | {"note": "昨日头痛，今天完全消失。"}… | 1 | 100.0% | 100.0% |
| expansion:temporality:2 | {"note": "头痛从昨日持续至本次就诊。"}… | 1 | 100.0% | 100.0% |
| expansion:temporality:3 | {"note": "告知患者以后若有头痛再联系，当前没有此症状。"}… | 1 | 100.0% | 0.0% |
| expansion:temporality:4 | {"note": "只记录了乏力，未采集头痛情况。"}… | 1 | 100.0% | 100.0% |
| expansion:temporality:5 | {"note": "昨日恶心，今天完全消失。"}… | 1 | 100.0% | 100.0% |
| expansion:temporality:6 | {"note": "恶心从昨日持续至本次就诊。"}… | 1 | 100.0% | 100.0% |
| expansion:temporality:7 | {"note": "告知患者以后若有恶心再联系，当前没有此症状。"}… | 1 | 100.0% | 0.0% |
| expansion:temporality:8 | {"note": "只记录了乏力，未采集恶心情况。"}… | 1 | 100.0% | 100.0% |
| expansion:temporality:9 | {"note": "昨日咳嗽，今天完全消失。"}… | 1 | 100.0% | 100.0% |
| expansion:temporality:10 | {"note": "咳嗽从昨日持续至本次就诊。"}… | 1 | 100.0% | 100.0% |
| expansion:temporality:11 | {"note": "告知患者以后若有咳嗽再联系，当前没有此症状。"}… | 1 | 100.0% | 0.0% |
| expansion:temporality:12 | {"note": "只记录了乏力，未采集咳嗽情况。"}… | 1 | 100.0% | 100.0% |
| expansion:temporality:13 | {"note": "昨日皮疹，今天完全消失。"}… | 1 | 100.0% | 100.0% |
| expansion:temporality:14 | {"note": "皮疹从昨日持续至本次就诊。"}… | 1 | 100.0% | 100.0% |
| expansion:temporality:15 | {"note": "告知患者以后若有皮疹再联系，当前没有此症状。"}… | 1 | 100.0% | 0.0% |
| expansion:temporality:16 | {"note": "只记录了乏力，未采集皮疹情况。"}… | 1 | 100.0% | 100.0% |
