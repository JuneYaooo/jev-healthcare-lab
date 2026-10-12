"""Verify every frozen request/response and render the performance report offline."""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
import statistics

import medical_decision_dataset as data
import run_performance_evaluation as perf

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'results/performance-v1'
REPORT = ROOT / 'docs/PERFORMANCE_RESULTS.md'


def verify(run):
    archive = json.loads((run / 'archive_manifest.json').read_text())
    for name, sha in archive['files'].items():
        if data.file_sha(run / name) != sha:
            raise ValueError('Archive hash mismatch: ' + name)
    config = json.loads((run / 'config.json').read_text())
    expected_cells = {(suite, level, repeat, model) for suite, levels in [('concurrency', perf.CONCURRENCY), ('fanout', perf.COUNTS)] for level in levels for repeat in range(3) for model in perf.MODELS}
    actual_cells = [(c['suite'], c['level'], c['repeat'], c['model']) for c in config['cells']]
    if len(actual_cells) != len(expected_cells) or set(actual_cells) != expected_cells:
        raise ValueError('Incomplete or duplicate experiment matrix')
    if config['pricing'] != perf.PRICING:
        raise ValueError('Price snapshot differs from scorer')
    if config['smoke']:
        raise ValueError('Smoke runs cannot be published as full comparisons')
    if config['dataset_manifest_sha256'] != data.file_sha(perf.DATASET / 'manifest.json'):
        raise ValueError('Archived workload differs from published workload')
    if config['dataset_manifest_sha256'] != data.file_sha(run / 'dataset/manifest.json'):
        raise ValueError('Workload manifest mismatch')
    if config['runner_sha256'] != data.file_sha(run / 'tools/run_performance_evaluation.py'):
        raise ValueError('Runner snapshot mismatch')
    if config['runner_sha256'] != data.file_sha(Path(perf.__file__)):
        raise ValueError('Use matching performance runner to rescore this archive')
    if data.file_sha(run / 'tools/run_model_evaluation.py') != data.file_sha(Path(perf.clinical.__file__)):
        raise ValueError('Clinical payload helper differs from archived helper')
    perf.verify_dataset(run / 'dataset')
    inputs = {r['id']: r for filename in ['clinical.jsonl', 'fanout.jsonl']
              for r in data.read_jsonl(run / 'dataset' / filename)}
    summaries = json.loads((run / 'summary.json').read_text())
    if len(summaries) != len(config['cells']):
        raise ValueError('Incomplete performance run')
    verified = []
    for index, (cell, saved) in enumerate(zip(config['cells'], summaries)):
        if saved['cell'] != index or any(saved[k] != v for k, v in cell.items()):
            raise ValueError('Cell identity mismatch')
        if cell['suite'] == 'concurrency':
            expected = {r['id'] for r in inputs.values() if 'task' in r}
        else:
            expected = {r['id'] for r in inputs.values() if r.get('repeat') == cell['repeat'] and r.get('questions') == cell['level']}
        records = list(data.read_jsonl(run / saved['records_file']))
        seen = set()
        for record in records:
            uid = record['id']
            if uid not in expected or uid in seen or record['model'] != cell['model']:
                raise ValueError('Unknown, duplicate or mismatched response')
            seen.add(uid)
            item = inputs[uid]
            if record['request_sha256'] != data.digest(item['request']) or record['provider_request_sha256'] != data.digest(perf.payload(item['request'], cell['model'])):
                raise ValueError('Provider payload mismatch')
            if record['elapsed_s'] < 0 or record['queue_s'] < 0 or abs(record['completion_s'] - record['elapsed_s'] - record['queue_s']) > 1e-8:
                raise ValueError('Invalid timing')
            if record['completion_s'] > saved['wall_s'] + .001:
                raise ValueError('Request completes outside batch window')
            if record['decisions'] != len(item['gold']):
                raise ValueError('Decision count mismatch')
            if 'response' in record:
                recalculated = perf.evaluate(item, record['response'], cell['model'])
                if any(record[k] != v for k, v in recalculated.items()):
                    raise ValueError('Response score mismatch')
                if record['status'] != ('success' if recalculated['complete_valid'] else 'invalid_answer'):
                    raise ValueError('Response status mismatch')
            elif record['valid_decisions'] or record['correct_decisions'] or record['complete_valid'] or record['all_correct']:
                raise ValueError('Missing response has positive score')
        if seen != expected:
            raise ValueError('Missing requests in completed cell')
        computed = perf.summary(records, saved['wall_s'], cell['model'], len(expected), sum(len(inputs[k]['gold']) for k in expected))
        if any(saved[k] != v for k, v in computed.items()):
            raise ValueError('Summary mismatch')
        verified.append((saved, records))
    return config, verified


def aggregate(verified):
    groups = collections.defaultdict(list)
    for cell, records in verified:
        groups[(cell['suite'], cell['level'], cell['model'])].append((cell, records))
    result = []
    for (suite, level, model), parts in sorted(groups.items()):
        records = [r for _, rows in parts for r in rows]
        wall = sum(c['wall_s'] for c, _ in parts)
        summary = perf.summary(records, wall, model, sum(c['expected_requests'] for c, _ in parts), sum(c['decisions'] for c, _ in parts))
        result.append({'suite': suite, 'level': level, 'model': model, 'repeats': len(parts), **summary,
                       'wall_per_repeat_s': [c['wall_s'] for c, _ in parts],
                       'throughput_per_repeat': [c['valid_decisions_per_s'] for c, _ in parts]})
    return result


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] +
                     ['| ' + ' | '.join(map(str, row)) + ' |' for row in rows])


def pct(x):
    return f'{x * 100:.2f}%'


def span(values):
    return f'{min(values):.2f}–{max(values):.2f}'


def price(cost, metric):
    low, high = cost[f'{metric}_lower'], cost[f'{metric}_upper']
    if low is None:
        return '—（用量缺失）'
    return f'{low:.4f}' if low == high else f'{low:.4f}–{high:.4f}'


def render(config, verified, grouped):
    label = lambda r: perf.clinical.MODELS[r['model']]['label']
    concurrency = sorted([r for r in grouped if r['suite'] == 'concurrency'], key=lambda r: (r['level'], perf.MODELS.index(r['model'])))
    fanout = sorted([r for r in grouped if r['suite'] == 'fanout'], key=lambda r: (r['level'], perf.MODELS.index(r['model'])))
    total = sum(r['requests'] for r in grouped)
    failures = [(c, r) for c, records in verified for r in records if r['status'] != 'success']
    parts = ['# 决策 API 性能补充测试',
        '[首页](../README.md) · [测试协议与数据](PERFORMANCE.md) · [完整原始记录](../results/performance-v1/README.md)',
        f'测试日期：2026-10-12（Asia/Shanghai）。JEV 1.13 与 DeepSeek V4.1 Flash 共 {total:,} 次请求，60 个测试单元。每档 3 轮，各单元顺序预先随机化，模型不同时运行。下表全部由原始响应离线复核生成。',
        '![并发吞吐与多问题完整响应时间](../assets/performance/performance-v1.svg)',
        '## 临床单题并发扩展',
        '复用开放许可临床子集的 128 道题，每档、每轮均相同。单题提示词与原临床测试一致。HTTP 连接在每个工作线程内复用，每单元新建连接池；首个连接计时。无自动重试。吞吐为三轮有效决策总数除以三轮墙钟总和，失败保留在准确率分母。此为有限批次测试，64 路时仅约两波请求，不能据此认定持续服务容量。',
        table(['并发', '模型', '有效决策/秒', '正确决策/秒', '准确率', '有效率', 'P50 秒', 'P95 秒', 'P99 秒', '429'],
              [[r['level'], label(r), f"{r['valid_decisions_per_s']:.2f}", f"{r['correct_decisions_per_s']:.2f}", pct(r['accuracy']), pct(r['valid_rate']), f"{r['p50_s']:.3f}", f"{r['p95_s']:.3f}", f"{r['p99_s']:.3f}", r['http_429']] for r in concurrency]),
        'P50/P95/P99 是排除客户端任务队列的完整请求耗时，包含序列化、网络、服务端处理、读取及校验。384 次请求合并统计；重复题不构成 384 道独立样本。以下整批时间包含排队与调度：',
        table(['并发', '模型', '每轮批次秒（最小–最大）', '每轮有效决策/秒（最小–最大）', '请求失败 / 超时 / 无效输出'],
              [[r['level'], label(r), span(r['wall_per_repeat_s']), span(r['throughput_per_repeat']), ' / '.join(str(r['status_counts'].get(k, 0)) for k in ['request_error', 'timeout', 'invalid_answer'])] for r in concurrency]),
        '### 失败与长尾记录',
        table(['模型', '组别/档位/轮次', '状态', '完整请求秒', 'HTTP / 错误类型', '原始记录'],
              [[label(c), f"{c['suite']}/{c['level']}/{c['repeat'] + 1}", r['status'], f"{r['elapsed_s']:.3f}", r.get('http_status', r.get('error_type', r.get('validation_error', '—'))), f"[cell-{c['cell']:03d}](../results/performance-v1/{c['records_file']})"] for c, r in failures]) if failures else '所有请求均返回完整合法结果。',
        '单次长尾即使没有进入合并 P99，也会拖慢整批完成；上方吞吐保留这种影响。网络错误只报告客户端观测，不能据此定位供应商内部故障。',
        '## 单请求多问题扩展',
        '3 份原创合成文档受理看板，各含 200 条不同记录及四条路由规则。每份看板在 1、10、50、100、200 问时材料完全相同，仅增加问题；答案由规则机械计算。任务是多记录路由，不是“一份真实病历的 200 项临床判断”。这组测量输出规模与处理效率，不能作为临床能力证据。',
        table(['问题数', '模型', '完整请求秒中位数', '完整请求秒范围', '有效决策/秒', '逐项准确率', '完整返回', '全项正确'],
              [[r['level'], label(r), f"{r['p50_s']:.3f}", span([rec['elapsed_s'] for c, rows in verified if c['suite']=='fanout' and c['level']==r['level'] and c['model']==r['model'] for rec in rows]), f"{r['valid_decisions_per_s']:.2f}", pct(r['accuracy']), f"{r['complete_requests']}/3", f"{r['all_correct_requests']}/3"] for r in fanout]),
        '每档只有 3 个请求，因此不展示多问题组的 P95/P99，也不作显著性判断。LLM 关闭思考，输出上限 max(256, 32 × 问题数)，200 问为 6,400 token；计时等到整个 JSON 接收并校验完成，不使用首 token 时间。',
        '## 用量与成本',
        '按 2026-10-12 官方价目估算美元成本，非账单。JEV 输入 $0.042/M、输出免费；Flash 用量区分缓存命中、未命中及输出，表中为闲时至高峰价格上下界，不按客户端请求时间猜测服务端计费时段。失败响应缺用量时不填完整单位成本；“已报告用量费用”仍列出，并标明缺失数。价格来源：[TypeSafe](https://docs.typesafe.ai/models)、[DeepSeek](https://api-docs.deepseek.com/quick_start/pricing/)。',
        table(['组别/档位', '模型', '每千有效决策 USD', '每千正确决策 USD', '已报告用量费用 USD', '缺用量请求'],
              [[f"{r['suite']}/{r['level']}", label(r), price(r['cost'], 'usd_per_1000_valid'), price(r['cost'], 'usd_per_1000_correct'), f"{r['cost']['usd_lower']:.6f}–{r['cost']['usd_upper']:.6f}", r['cost']['unpriced_requests']] for r in concurrency + fanout]),
        '## 解释边界',
        '原临床榜单的准确率与耗时仍有效，但仅覆盖单题 Choice、8 路并发与原运行环境。本轮改变了连接复用方式和样本规模，不把两轮绝对时间差解释为模型版本进步。',
        '结果包含客户端、跨服务商网络路径、连接建立与缓存影响，不等同于 GPU 推理时间。模型与档位随机交错可缓解时段偏差，不能消除网络和服务端负载差异。没有测开放到达流量、持续饱和、长时间稳定性、真实病历多字段判断、Score/Noul 或概率校准。',
        '重复使用题目与规则会触发服务商自动缓存；原始 usage 保留缓存命中。没有关闭缓存或把重复题称为冷缓存测试。失败不会自动重试，也不按是否答对筛选重跑。',
        '预检曾将临床单题改成统一多问题 JSON 提示，发现选项键遵守率下降；在冻结正式协议前停止该试跑，恢复原临床提示与输出形状。预检不计入以上结果，其记录与当时代码保留在 [预检档案](../results/performance-pilot-v1/README.md)。']
    return '\n\n'.join(parts) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    config, verified = verify(RUN)
    grouped = aggregate(verified)
    outputs = {REPORT: render(config, verified, grouped), RUN / 'comparison.json': json.dumps(grouped, ensure_ascii=False, indent=2) + '\n'}
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                raise ValueError('Stale generated file: ' + str(path))
        else:
            path.write_text(content)
    print(f'Verified {len(verified)} cells and {sum(len(r) for _, r in verified)} requests.')


if __name__ == '__main__':
    main()
