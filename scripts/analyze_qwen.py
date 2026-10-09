"""Archive and independently verify the same-input Qwen comparison, without API calls."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import statistics

import benchmark as b
from compare_qwen import ROOT, OUT, CACHE, MODEL, config, request_payload
from compare_deepseek import dumps, load_rows, normalize, sha
from verify_experiments import prediction, same_metrics


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def load_records(archived=False):
    if archived:
        return [r for p in sorted((ROOT/'scenarios').glob('*/*/comparison/qwen_responses.jsonl')) for r in read_jsonl(p)]
    return [json.loads(p.read_text()) for p in sorted((CACHE/'runs').glob('*.json'))]


def estimate_cost(record, pricing):
    usage = record.get('response', {}).get('usage', {})
    return (usage.get('prompt_tokens', 0)*pricing['input_per_million'] +
            usage.get('completion_tokens', 0)*pricing['output_per_million']) / 1e6


def summarize(records):
    source = load_rows()
    indexed = {(r['task'], r['id']): r for r in records}
    if len(indexed) != len(records):
        raise ValueError('Duplicate Qwen identity')
    expected = {(r['task'], r['id']) for r in source}
    if not set(indexed) <= expected:
        raise ValueError('Unexpected Qwen identity')
    methods = json.loads((ROOT/'results/task_methods.json').read_text())
    pricing = json.loads((OUT/'pricing_source.json').read_text())
    if pricing['model_requested'] != MODEL or pricing['currency'] != 'CNY':
        raise ValueError('Pricing snapshot model or currency differs')
    if any(pricing[k] != config()['pricing'][k] for k in ('input_per_million', 'output_per_million')):
        raise ValueError('Pricing snapshot differs from configuration')
    tasks = {}
    groups = defaultdict(list)
    for row in source:
        groups[row['task']].append(row)
    counts, returned = Counter(), Counter()
    all_times, all_attempts = [], []
    for task, rows in groups.items():
        pairs, latencies, attempts, failures = [], [], [], []
        empty = 0
        for row in rows:
            record = indexed.get((task, row['id']))
            if record is None:
                continue
            if record['request_sha256'] != row['request_sha256'] or record['provider_request_sha256'] != sha(request_payload(row)):
                raise ValueError('Input/payload mismatch')
            if sha(row['request']) != row['request_sha256']:
                raise ValueError('Source request hash differs')
            prior = record['prior_attempts']
            for attempt in [*prior, record]:
                if any(attempt[k] != record[k] for k in ('task', 'id', 'request_sha256', 'provider_request_sha256')):
                    raise ValueError('Retry input differs')
                if 'response' in attempt:
                    data = attempt['response']
                    if data['model'] != MODEL:
                        raise ValueError('Returned model differs')
                    usage = data['usage']
                    if usage['prompt_tokens'] + usage['completion_tokens'] != usage['total_tokens']:
                        raise ValueError('Token total mismatch')
                    if usage.get('completion_tokens_details', {}).get('reasoning_tokens', 0):
                        raise ValueError('Unexpected thinking tokens')
                if attempt['status'] == 'ok' and not attempt.get('deterministic_empty'):
                    if normalize(row, attempt['response']) != attempt['normalized_answers']:
                        raise ValueError('Normalized output differs')
                    if attempt['response']['choices'][0]['finish_reason'] != 'stop':
                        raise ValueError('Truncated success')
            if any(a['status'] == 'ok' for a in prior):
                raise ValueError('Successful output retried')
            if record['reported_total_tokens'] != sum(a.get('response', {}).get('usage', {}).get('total_tokens', 0) for a in [*prior, record]):
                raise ValueError('Retry usage mismatch')
            if record['status'] == 'ok':
                if not row['request']['questions']:
                    if not record.get('deterministic_empty') or record['normalized_answers'] != {} or record['elapsed_s'] != 0:
                        raise ValueError('Invalid deterministic empty')
                    empty += 1
                else:
                    if record.get('deterministic_empty'):
                        raise ValueError('Nonempty request skipped')
                    latencies.append(record['elapsed_s'])
                    returned[record['response']['model']] += 1
                pairs.append(prediction(row, {'response': {'answers': record['normalized_answers']}}))
                counts['successful_rows'] += 1
            else:
                format_reason = None
                if 'response' in record and record['response']['choices'][0]['finish_reason'] == 'stop':
                    try:
                        normalize(row, record['response'])
                    except (ValueError, KeyError, TypeError) as error:
                        format_reason = str(error)
                    else:
                        raise ValueError('Valid response counted as failure')
                elif 'response' in record:
                    format_reason = 'Incomplete generation'
                # Use the same failure scoring as the archived DeepSeek comparison.
                gold, _ = prediction(row, {'response': {'answers': {k: {'choice': next(iter(q['criteria']))} if q['type']=='choice' else {'noul': 0} for k,q in row['request']['questions'].items()}}})
                pairs.append((gold, set() if isinstance(gold, set) else '__API_OR_FORMAT_FAILURE__'))
                failures.append({'id': row['id'], 'status': record['status'], 'error_type': record.get('error_type'), 'http_status': record.get('http_status'), 'format_reason': format_reason})
                counts['failed_rows'] += 1
            attempts.extend([*prior, record])
        quality = None if not pairs else (b.sets_metric(pairs) if isinstance(pairs[0][0], set) else b.classification([g for g,p in pairs], [p for g,p in pairs]))
        cost = sum(estimate_cost(a, pricing) for a in attempts)
        tasks[task] = {'title': methods[task]['title'], 'planned': len(rows), 'compared': len(pairs), 'quality': quality,
                       'latency_median_s': statistics.median(latencies) if latencies else None,
                       'cost_cny': cost, 'cost_per_1000_cny': cost / len(pairs)*1000 if pairs else None,
                       'prompt_tokens': sum(a.get('response',{}).get('usage',{}).get('prompt_tokens',0) for a in attempts),
                       'completion_tokens': sum(a.get('response',{}).get('usage',{}).get('completion_tokens',0) for a in attempts),
                       'prior_attempts': len(attempts)-len(pairs), 'deterministic_empty': empty, 'failures': failures}
        all_times.extend(latencies)
        all_attempts.extend(attempts)
    total_cost = sum(t['cost_cny'] for t in tasks.values())
    summary = {'model_requested': MODEL, 'returned_models': dict(returned), 'enable_thinking': False,
               'planned_rows': len(source), 'compared_rows': len(indexed), 'complete': set(indexed)==expected,
               'successful_rows': counts['successful_rows'], 'failed_rows': counts['failed_rows'],
               'deterministic_empty': sum(t['deterministic_empty'] for t in tasks.values()),
               'latency_median_s': statistics.median(all_times) if all_times else None,
               'cost_cny': total_cost, 'cost_per_1000_cny': total_cost/len(indexed)*1000 if indexed else None,
               'prompt_tokens': sum(t['prompt_tokens'] for t in tasks.values()),
               'completion_tokens': sum(t['completion_tokens'] for t in tasks.values()),
               'prior_attempts': len(all_attempts)-len(indexed),
               'cost_scope': 'CNY public list-price estimate including retained retry token usage. Excludes unreported usage, setup smoke request and upstream OCR/ASR; not an invoice.',
               'latency_scope': 'Successful final full-response HTTP requests only; excludes zero-call empties and prior retries. Historical Jev/DeepSeek versus newly run Qwen, not simultaneous.'}
    return {'summary': summary, 'tasks': tasks}


def archive(records, result):
    if not result['summary']['complete']:
        raise ValueError('Incomplete cohort cannot be published')
    owners = {t:s['id'] for s in json.loads((ROOT/'results/scenario_manifest.json').read_text())['scenes'] for t in s['task_ids']}
    groups = defaultdict(list)
    for record in records:
        groups[record['task']].append(record)
    manifest = []
    for task, rows in groups.items():
        path = ROOT/'scenarios'/owners[task]/task/'comparison/qwen_responses.jsonl'
        path.write_text(''.join(dumps(r)+'\n' for r in sorted(rows,key=lambda r:r['id'])))
        manifest.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    (OUT/'archive_manifest.json').write_text(json.dumps(sorted(manifest,key=lambda r:r['path']),ensure_ascii=False,indent=2)+'\n')
    (OUT/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (OUT/'config.json').write_text(json.dumps(config(),ensure_ascii=False,indent=2)+'\n')
    (OUT/'README.md').write_text(render_report(result))


def render_report(result):
    summary = result['summary']
    pricing = json.loads((OUT/'pricing_source.json').read_text())
    references = json.loads((ROOT/'comparisons/deepseek-flash/summary.json').read_text())['tasks']
    owners = {t:s['id'] for s in json.loads((ROOT/'results/scenario_manifest.json').read_text())['scenes'] for t in s['task_ids']}
    lines = [
        '# Qwen3.5-9B：同题医疗任务对照', '',
        '[返回三模型对比](../../README.md#全部领域与任务的详细测试数据)', '',
        f'通过硅基流动中国站调用 `{MODEL}`，覆盖 **96 项任务、{summary["compared_rows"]:,} 条输入**。Jev 和 DeepSeek 使用已归档的同题结果；Qwen 为本次新增调用。', '',
        '| 项目 | 结果 |', '| --- | ---: |',
        f'| 可评分记录（含规则空集） | {summary["successful_rows"]:,} |',
        f'| 最终调用或格式失败 | {summary["failed_rows"]:,} |',
        f'| 无候选、无需 API 的规则空集 | {summary["deterministic_empty"]} |',
        f'| 保留的早期尝试 | {summary["prior_attempts"]:,} |',
        f'| 成功请求中位响应 | {summary["latency_median_s"]:.2f} 秒 |',
        f'| 输入／输出 tokens（含重试） | {summary["prompt_tokens"]:,}／{summary["completion_tokens"]:,} |',
        f'| 全部评测调用的估算费用 | ¥{summary["cost_cny"]:.4f} |',
        f'| 每千条输入的估算费用 | ¥{summary["cost_per_1000_cny"]:.3f} |', '',
        '## 比较方法', '',
        '- **题目不变**：读取已冻结的 `samples.jsonl`，仅向模型发送 `request`，不发送金标或评分元数据。每条记录保留原始请求与供应商请求的 SHA-256。',
        '- **输出接口一致**：沿用 DeepSeek 的系统提示词、JSON 输出格式与 choice／布尔值适配器。设置 `temperature=0`、`enable_thinking=false`；输出上限沿用相同的按问题数计算规则。',
        '- **评分一致**：单标签任务报告准确率，集合任务报告 micro-F1；保留调用和格式失败在分母中，失败分类计错、失败集合按空集评分。',
        '- **格式要求**：choice 必须返回给定选项的键，不能用选项说明或提取出的数值代替。只允许与既有 DeepSeek 适配器相同的无歧义整数键转字符串，不针对某个模型追加答案修复。格式失败原因和原始内容均保留。',
        '- **分数含义**：这里衡量既定输入与输出约定下的端到端任务表现；医学判断与结构化输出能力都会影响得分，不能把格式失败全部解释为医学知识错误。',
        '- **重试透明**：单次执行最多尝试三次；首轮遇到限流后增加共享 60 秒等待，并对传输失败补跑。成功答案不重跑，格式失败不在恢复阶段额外重跑，所有早期尝试嵌入最终记录的 `prior_attempts`。不按答案正误决定重跑。',
        '- **时间口径**：8 并发；表内耗时为成功最终请求从发出到完整响应的中位时间，排除规则空集和早期重试。三家调用日期、服务端负载与接口不同，不能据此认定为同期速度排名。分阶段运行未合成为整批总时间。', '',
        '## 费用口径', '',
        f'按[硅基流动中国站公开模型目录]({pricing["source"]})在 `{pricing["retrieved_utc"]}` 的费率快照估算：每百万输入 tokens **¥{pricing["input_per_million"]:g}**，每百万输出 tokens **¥{pricing["output_per_million"]:g}**。保留[原始费率字段](pricing_source.json)。', '',
        '计入所有有用量记录的最终调用和早期重试；不假设缓存折扣，不包含未返回用量的调用、接口连通性试跑、上游 OCR／ASR 或人工成本。该数值是公开标价估算，不是账单实付金额。Jev／DeepSeek 原表为美元，未做汇率换算。', '',
        '## 各任务结果', '',
        '| 任务 | 输入数 | 指标 | Jev | DeepSeek | Qwen | Qwen 中位耗时（秒） | Qwen 每千条（人民币） | 失败数 | 原始回答 |',
        '| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |',
    ]
    for task, row in result['tasks'].items():
        q = row['quality']
        metric = '准确率（%）' if 'accuracy' in q else 'micro-F1（分）'
        def value(quality):
            return quality.get('accuracy', quality.get('micro_f1'))*100
        ref = references[task]
        folder = f'../../scenarios/{owners[task]}/{task}'
        latency = '—' if row['latency_median_s'] is None else f'{row["latency_median_s"]:.2f}'
        lines.append(f'| [{row["title"]}]({folder}/README.md) | {row["planned"]} | {metric} | {value(ref["jev"]["quality"]):.1f} | {value(ref["deepseek"]["quality"]):.1f} | {value(q):.1f} | {latency} | ¥{row["cost_per_1000_cny"]:.3f} | {len(row["failures"])} | [Qwen]({folder}/comparison/qwen_responses.jsonl) |')
    lines += ['', '## 归档与核验', '',
              '[配置](config.json) · [汇总](summary.json) · [运行阶段](sessions.jsonl) · [归档校验清单](archive_manifest.json) · [接口文档](https://docs.siliconflow.cn/docs/api/chat-completions-post)', '',
              '无需密钥即可在仓库根目录核验原始回答、请求指纹、重试用量与重算得分：', '',
              '```sh', 'python3 scripts/analyze_qwen.py --verify', '```', '',
              '重新运行会产生 API 费用；脚本从环境变量 `SILICONFLOW_API_KEY` 或仓库外的私有密钥文件读取凭据：', '',
              '```sh', 'python3 scripts/compare_qwen.py', 'python3 scripts/analyze_qwen.py', '```', '',
              '本地缓存位于被 Git 忽略的 `work/qwen3.5-9b/`；脚本会跳过已有最终记录。仅恢复限流、服务器或网络失败时使用 `--retry-transport`，保留先前尝试。', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--progress', action='store_true')
    args = parser.parse_args()
    records = load_records(args.verify)
    result = summarize(records)
    if args.verify:
        if not result['summary']['complete']:
            raise ValueError('Archive is incomplete')
        if not same_metrics(result,json.loads((OUT/'summary.json').read_text())):
            raise ValueError('Published Qwen summary differs')
        manifest = json.loads((OUT/'archive_manifest.json').read_text())
        paths = {p.relative_to(ROOT).as_posix() for p in (ROOT/'scenarios').glob('*/*/comparison/qwen_responses.jsonl')}
        if len(manifest) != len(paths) or {item['path'] for item in manifest} != paths:
            raise ValueError('Archive manifest coverage differs')
        for item in manifest:
            if hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()!=item['sha256']:
                raise ValueError('Archive hash differs')
        if json.loads((OUT/'config.json').read_text()) != config():
            raise ValueError('Configuration differs')
        if (OUT/'README.md').read_text() != render_report(result):
            raise ValueError('Qwen report differs from summary')
        print('Verified 7,133 Qwen rows: prompts, adapter, retries, metrics, token usage and archive hashes match.')
    elif args.progress:
        print(json.dumps(result['summary'],ensure_ascii=False,indent=2))
    else:
        archive(records,result)
        print(json.dumps(result['summary'],ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
