# 运行与复算源码

运行器分阶段快照均保留，以对应重测记录：

- `run_medical_load.py`：首次运行。
- `run_medical_load-resume.py`：更新初始 token 额度预留估算。
- `run_medical_load-network-resume.py`：连接退避、窗口异常停止与恢复。
- `run_medical_load-timing-correction.py`：最终测量使用的计时修正；全部 Qwen 负载窗口按此版本重新测量。此前 Qwen 记录保存在 `superseded-timing/`，不参与吞吐汇总。无 token 节流的 Flash 已完成有效窗口继续保留。
- `run_medical_load-final.py`：维护版运行器，另补齐来源清单自动生成、已中止窗口的恢复检查和所选模型状态字段；请求内容和评分规则未改变。

`build_medical_load_report.py` 从原始响应复算结果；`render_medical_load_docs.py` 与 `generate_catalog_docs.py` 生成图表与文档。其余文件为运行器依赖的既有脚本快照。运行时使用仓库 `scripts/` 下的模块；快照用于审计，避免用文件名推测实际运行阶段。
