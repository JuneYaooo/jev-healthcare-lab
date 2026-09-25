# 边界挑战：影像报告断言：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| radiology_assertion:1 | {"note": "右肺上叶见一枚结节。"}… | 1 | 100.0% | 100.0% |
| radiology_assertion:2 | {"note": "双肺未见结节。"}… | 1 | 100.0% | 100.0% |
| radiology_assertion:3 | {"note": "右上肺结节不能排除。"}… | 1 | 100.0% | 100.0% |
| radiology_assertion:4 | {"note": "心影大小正常，其他结构未描述。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:1 | {"note": "本次文字报告明确可见胸腔积液。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:2 | {"note": "本次未见胸腔积液，其他发现另述。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:3 | {"note": "影像表现不能排除胸腔积液，建议结合临床。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:4 | {"note": "本次仅描述心影大小正常，其余内容未记录。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:5 | {"note": "本次文字报告明确可见气胸。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:6 | {"note": "本次未见气胸，其他发现另述。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:7 | {"note": "影像表现不能排除气胸，建议结合临床。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:8 | {"note": "本次仅描述心影大小正常，其余内容未记录。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:9 | {"note": "本次文字报告明确可见肺部实变。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:10 | {"note": "本次未见肺部实变，其他发现另述。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:11 | {"note": "影像表现不能排除肺部实变，建议结合临床。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:12 | {"note": "本次仅描述心影大小正常，其余内容未记录。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:13 | {"note": "本次文字报告明确可见纵隔肿块。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:14 | {"note": "本次未见纵隔肿块，其他发现另述。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:15 | {"note": "影像表现不能排除纵隔肿块，建议结合临床。"}… | 1 | 100.0% | 100.0% |
| expansion:radiology_assertion:16 | {"note": "本次仅描述心影大小正常，其余内容未记录。"}… | 1 | 100.0% | 100.0% |
