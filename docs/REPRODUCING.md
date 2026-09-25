# 实验归档与核验

仓库保留原始 6,886 条计分记录，并追加 446 条两模型真实调用记录；当前共 7,032 条主任务记录及 300 条配对扰动记录。每条输入、金标、提示词和响应均有身份与哈希关联，原有记录没有被新样本替换。补充来源与数量见 [补充实验统计](../results/expansion_summary.json)。

## 归档内容

实验按 `scenarios/<场景>/<任务>/` 保存。每个主任务包含 `samples.jsonl`、`responses.jsonl`、`prompts.json`、`example.json`、`results.json`、`index.jsonl`、`provenance.json` 和方法说明 `README.md`。5 个任务的额外扰动分别放在自身的 `robustness/repeat`、`rotate`、`irrelevant` 下。

`samples.jsonl` 是实际参与评测的 prepared 记录，包含完整 `request`、本地评分用的 `gold` 和元数据，不是仅有 ID 的索引。`responses.jsonl` 每行保留原缓存文件的完整字节；去除新增的换行分隔符后计算 SHA256，应等于索引中的 `response_sha256`。通过 `(task, id)` 关联文件，不依赖文件顺序。

所有任务的真实输入已包含在请求中，但不包含上游全量数据集及训练语料。语音实验另保留实际使用的患者扮演音频和两份转写；OCR 实验另保留全部实际使用的原图、参考文本与识别文本，位于对应任务的 `upstream/`。

## 离线核验

```sh
python3 scripts/verify_experiments.py
python3 scripts/verify_comparison.py
python3 scripts/verify_batch_time.py
python3 scripts/build_scenario_report.py --check
python3 -m unittest discover -s tests -v
```

核验器检查 96 个主任务无遗漏，逐条校验请求／响应／文件哈希、模型、token、空预测标记和完整提示词覆盖，再从实际响应与金标重算全部主任务质量指标及 15 组扰动结果。该检查不连接 API。历史置信区间和延迟保留原统计，核验器不将本次本地运行时间写成模型延迟。

## 实际调用方式

原批量调用逻辑见 `scripts/live_batch.py`：向 `https://api.typesafe.ai/v1/systemone` 发送 `request` 加 `model`；`gold` 和 `metadata` 不发送。默认模型为 `jev-1.13.0`。空候选直接生成空预测，成功响应缓存跳过，失败记录保留，不以模拟响应替代。

重新调用使用任务目录中的 `samples.jsonl` 作为 `--input`，需在本地设置 `TYPESAFE_API_KEY`。`.env.example` 仅展示格式，不会自动加载；也可通过 `--env-file` 指定私有配置。重新调用会产生费用，新的服务响应不保证与历史缓存相同。

默认运行缓存目录为根目录下被 Git 忽略的 `data/`；也可通过 `JEV_DATA_DIR` 指定。请求重放不需要重新下载上游全量语料；重新构造候选、重做抽样或运行原数据适配器仍需要相应上游文件。可选依赖见 `requirements-optional.txt`。

## 维护归档

- `results/scenario_manifest.json`：12 个场景和 96 个主任务的一对一归属。
- `results/task_methods.json`：每个任务的中文名称、实际适配器与实验方法。
- `scripts/archive_experiments.py --source <原 medical-bench 目录>`：仅抽取已发布索引中的医疗／扰动记录，验证原哈希后归档；不会递归复制凭据或自媒体任务。
- `scripts/build_scenario_report.py`：从归档生成统计 README、场景页和任务方法页；`--check` 检查页面是否与结果同步。

已归档的每个 prepared 分片原始文件哈希记录在任务的 provenance.json。EvidenceBench 的 37 条历史请求哈希格式修正记录保留在任务的 hash_audit.json；它们是原实验序列化排序修正，不是此次重新生成响应。

## DeepSeek 同题对比

主任务的 `comparison/` 保留同一批输入的 DeepSeek 原始回答、适配结果和费用；失败重试记录单独保留。完整方法见 [对比实验说明](../comparisons/deepseek-flash/README.md)。`verify_comparison.py` 离线检查全部主任务的输入绑定、原始回答适配、文件哈希，并重算分数和费用，不需要 API key。

如需自行重跑，`compare_deepseek.py --key-file <私有配置路径>` 读取包含 `DEEPSEEK_API_KEY` 的私有文件；默认 8 个并发，缓存位于被 Git 忽略的 `comparisons/deepseek-flash/runs/`。`--max-usd` 限制已报告用量的估算支出，在途请求可能使最终金额略超限。`--retry-errors` 只重试失败记录并保留旧尝试，不重试有效但答错的回答。中国法定节假日重跑时，应按官方规则加 `--off-peak-holiday` 使用全天空闲价；其他时间按官方 UTC 时段计算。重新调用会产生费用和新的响应。

## 补充实验

`prepare_expansion.py --source <原数据目录>` 从公开答案和明确规则生成补充文本，`prepare_media_expansion.py` 读取公开音频的参考／ASR 文本及 ClinOCR-Bench 的 normal、tables 测试分片。`prepare_audio_excerpts.py` 从 PriMock57 的音频与 TextGrid 提取补充片段，取两个患者声道的前 90 秒，Whisper tiny.en-q5_1、英语、4 线程配置（本次使用 Metal 后端），保留实际片段和输出；OCR 使用 Tesseract English `--psm 3`。补充输入、证据短语和来源均已合入各任务目录，`upstream/expansion/` 保留使用的媒体与识别文本。

`append_experiments.py --input <补充输入 JSONL>` 只在所有新增 Jev 响应通过验证后追加记录，保留旧输入与响应，更新索引、完整提示词、质量指标及分组置信区间。`finalize_comparison.py` 重算并归档对应 DeepSeek 结果。

两家凭据分别使用 `TYPESAFE_API_KEY` 与 `DEEPSEEK_API_KEY`。调用脚本从 `--env-file` 或 `--key-file` 指定的本地配置读取。

## 全量响应时间

[整批测速](../comparisons/batch-time/README.md) 保存独立重新调用的全部响应、尝试次数与相对计时。`measure_batch_time.py` 接收完整输入 JSONL，使用 `--provider jev` 或 `--provider deepseek` 分别计时；本次配置为 `--workers 8 --timeout 45`，每条最多两次请求。DeepSeek 空闲时段使用 `--off-peak`。`--output` 必须是新目录，避免混入既有结果。

计时文件由 `finalize_batch_time.py` 发布，`verify_batch_time.py` 核验输入一致性、计时边界、失败计数和费用。新运行会产生新的响应与成本，不能覆盖原始效果评测以择优提高分数。

## 新材料的配对实验

`scenarios/evidence/pubmed_rct_section/paired-new/` 单独保存 20 篇新摘要、200 个原始标注判断及两轮单项／合并调用。它们不混入原 7,032 条主评测统计。`inputs.jsonl` 包含完整材料、问题和金标，`protocol.json` 固定抽样、分组及顺序，`responses.jsonl` 和 `blocks.jsonl` 保留请求与整批时间。

运行 `python3 scripts/analyze_paired_new.py --check` 可离线核验全部 240 次文档处理、原始模型回答、问题配对、费用与总耗时。调用程序为 `run_paired_new.py`，依赖可选的 httpx，使用连接池；重新调用时须使用新的输出目录。`prepare_paired_new.py --source <PubMed_20k_RCT/test.txt>` 使用前 300 篇完整摘要构建候选池，排除主评测重合内容；已有实验方案不会被覆盖。
