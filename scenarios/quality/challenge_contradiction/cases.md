# 边界挑战：病历矛盾：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| contradiction:1 | {"note": "段A：今日体温38.6℃。段B：同次测量体温36.6℃。"}… | 1 | 100.0% | 100.0% |
| contradiction:2 | {"note": "段A：昨日发热。段B：今日已退热。"}… | 1 | 100.0% | 100.0% |
| contradiction:3 | {"note": "段A：否认药物过敏。段B：同一时点确认青霉素过敏。"}… | 1 | 100.0% | 100.0% |
| contradiction:4 | {"note": "段A：体温未测。段B：患者感到不适。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:1 | {"note": "A：本时点有头痛。B：同一患者同一时点明确没有头痛。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:2 | {"note": "A：昨日有头痛。B：今天已经没有头痛。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:3 | {"note": "A：患者没有头痛。B：母亲有头痛。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:4 | {"note": "A：本次头痛未询问。B：只记录其他症状。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:5 | {"note": "A：本时点有腹痛。B：同一患者同一时点明确没有腹痛。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:6 | {"note": "A：昨日有腹痛。B：今天已经没有腹痛。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:7 | {"note": "A：患者没有腹痛。B：母亲有腹痛。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:8 | {"note": "A：本次腹痛未询问。B：只记录其他症状。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:9 | {"note": "A：本时点有咳嗽。B：同一患者同一时点明确没有咳嗽。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:10 | {"note": "A：昨日有咳嗽。B：今天已经没有咳嗽。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:11 | {"note": "A：患者没有咳嗽。B：母亲有咳嗽。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:12 | {"note": "A：本次咳嗽未询问。B：只记录其他症状。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:13 | {"note": "A：本时点有乏力。B：同一患者同一时点明确没有乏力。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:14 | {"note": "A：昨日有乏力。B：今天已经没有乏力。"}… | 1 | 100.0% | 0.0% |
| expansion:contradiction:15 | {"note": "A：患者没有乏力。B：母亲有乏力。"}… | 1 | 100.0% | 100.0% |
| expansion:contradiction:16 | {"note": "A：本次乏力未询问。B：只记录其他症状。"}… | 1 | 100.0% | 100.0% |
