# Data and upstream projects

The `scenarios/` archive contains the exact evaluated subsets: input text, gold labels, adapted Jev questions, cached responses, and experiment metadata. The ASR task also includes its original acted-patient audio and transcripts; the OCR task includes the selected scans and texts. These are experiment subsets, not complete upstream datasets.

Source links and adaptation scope are recorded in each task's README and provenance.json, and in results/medical_catalog.json. Dataset texts, annotations, media, upstream code and provider outputs remain subject to their original rights and access conditions; the repository's MIT code license does not relicense them. In particular, research-only/noncommercial source restrictions remain applicable, including TCM-SD's CC BY-NC-SA 4.0 conditions noted in the original adapter.

Credentials, model weights, unrelated media-domain experiments and unselected source corpora are not included. Public benchmark and acted/synthetic records are not newly collected patient data. Adapted task metrics are not official leaderboard submissions; closed-model training exposure is unknown.

### TCM-QA 补充题目

中医基础知识多选与治法单选补充题目来自 [yizhen-buaa/TCM-QA-datasets](https://github.com/yizhen-buaa/TCM-QA-datasets)，采用原始问题、选项和答案，许可为 [Apache License 2.0](third_party/tcm-qa/LICENSE)。题号与源文件位置保存在各条样本的 metadata 中；仅作评测适配，未改写题目答案。
