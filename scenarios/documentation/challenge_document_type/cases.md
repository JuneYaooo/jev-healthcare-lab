# 边界挑战：文档类型：逐案例结果

20 个案例，共 20 条测试记录。案例口径：自编测试案例（含相关模板变体）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| document_type:1 | {"note": "检验项目：血红蛋白；结果：120g/L；参考区间见表。"}… | 1 | 100.0% | 100.0% |
| document_type:2 | {"note": "入院日期、出院日期、住院经过、出院医嘱如下。"}… | 1 | 100.0% | 100.0% |
| document_type:3 | {"note": "药品名称、规格、每次剂量、每日频次，医师签名。"}… | 1 | 100.0% | 100.0% |
| document_type:4 | {"note": "因系统维护，明日暂停线上预约服务。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:1 | {"note": "白细胞计数、数值、参考范围、检验者签名。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:2 | {"note": "尿液检验结果与正常参考区间。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:3 | {"note": "电解质检验项目、浓度及异常标记。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:4 | {"note": "肝功能各检验项目结果及采样时间。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:5 | {"note": "出院小结列有入院诊断、住院经过和出院医嘱。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:6 | {"note": "住院结束记录，含出院诊断及后续安排。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:7 | {"note": "出院时病情、住院治疗过程及复诊计划。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:8 | {"note": "病案结尾汇总入院原因、住院经过、离院安排。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:9 | {"note": "处方单列药名、数量、用法及处方医师。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:10 | {"note": "Rp：药品规格、每次用量、发药数量。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:11 | {"note": "门诊处方列三种药及各自服法。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:12 | {"note": "电子处方含药名、剂量、频次和药师审核。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:13 | {"note": "通知：周末窗口调整开放时间。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:14 | {"note": "公告：院内停车区域临时关闭。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:15 | {"note": "通知：线上挂号系统停机维护。"}… | 1 | 100.0% | 100.0% |
| expansion:document_type:16 | {"note": "工作人员培训安排与会议室分配。"}… | 1 | 100.0% | 100.0% |
