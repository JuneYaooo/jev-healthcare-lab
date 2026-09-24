# 实验归档与核验

当前仓库已从原实验目录恢复全部 **6,886 条计分记录**的真实输入、金标、提示词和响应。归档前逐条核对请求哈希与原响应文件哈希，与原发布的 `results/evaluation_index.jsonl` 完全一致。该过程未新增模型调用或替换失败结果。

## 归档内容

实验按 `scenarios/<场景>/<任务>/` 保存。每个主任务包含 `samples.jsonl`、`responses.jsonl`、`prompts.json`、`example.json`、`results.json`、`index.jsonl`、`provenance.json` 和方法说明 `README.md`。5 个任务的额外扰动分别放在自身的 `robustness/repeat`、`rotate`、`irrelevant` 下。

`samples.jsonl` 是实际参与评测的 prepared 记录，包含完整 `request`、本地评分用的 `gold` 和元数据，不是仅有 ID 的索引。`responses.jsonl` 每行保留原缓存文件的完整字节；去除新增的换行分隔符后计算 SHA256，应等于索引中的 `response_sha256`。通过 `(task, id)` 关联文件，不依赖文件顺序。

所有任务的真实输入已包含在请求中，但不包含上游全量数据集及训练语料。语音实验另保留实际使用的患者扮演音频和两份转写；OCR 实验另保留六张原图、参考文本与识别文本，位于对应任务的 `upstream/`。模型权重和凭据不随仓库分发。

## 离线核验

```sh
python3 scripts/verify_experiments.py
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
