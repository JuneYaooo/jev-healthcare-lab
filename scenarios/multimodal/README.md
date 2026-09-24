# 语音病历、医疗文档 OCR 与报告断言

**5 个任务条件，40 条主评测记录。** [全部场景](../../README.md)

实际执行 ASR 与 OCR；仅一段扮演患者音频、六份文档且只有两种模板。影像和 ECG 尚未运行。

| 任务（点击查看完整方法与数据） | 类型 | 记录数 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [ASR 转写病史字段判断](primock_asr_fields/README.md) | 数据适配 | 12 | Accuracy | 91.7% |
| [参考转写病史字段判断](primock_reference_fields/README.md) | 数据适配 | 12 | Accuracy | 100.0% |
| [OCR 文本医疗文档类型识别](clinocr_ocr_doctype/README.md) | 数据适配 | 6 | Accuracy | 83.3% |
| [参考文本医疗文档类型识别](clinocr_reference_doctype/README.md) | 数据适配 | 6 | Accuracy | 100.0% |
| [边界挑战：影像报告断言](challenge_radiology_assertion/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
