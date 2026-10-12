"""Verify sustained load archives and render task-scoped throughput results."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict, deque
import json
import math
from pathlib import Path
import statistics

import run_sustained_throughput as runner

data = runner.data
ROOT = runner.ROOT
RUN = runner.RUN
LABELS = {'jev-1.13.0': 'JEV 1.13', 'deepseek-flash': 'Flash'}


def read(path):
    return json.loads(path.read_text())


def verify(run):
    archive = read(run / 'archive_manifest.json')
    for name, digest in archive['files'].items():
        if data.file_sha(run / name) != digest:
            raise ValueError('Archive hash mismatch: ' + name)
    config, status = read(run / 'config.json'), read(run / 'run_status.json')
    if config['smoke']:
        raise ValueError('Smoke run is not a formal throughput experiment')
    for filename in ['run_sustained_throughput.py','run_task_performance.py','run_performance_evaluation.py','run_model_evaluation.py','medical_decision_dataset.py']:
        if data.file_sha(run / 'tools' / filename) != data.file_sha(ROOT / 'scripts' / filename):
            raise ValueError('Scoring helper differs from frozen snapshot: ' + filename)
    if config['pricing'] != runner.task.metrics.PRICING or config['limits'] != runner.LIMITS:
        raise ValueError('Pricing or quota snapshot mismatch')
    if config['clinical_manifest_sha256'] != data.file_sha(runner.task.DATASET / 'manifest.json') or config['synthetic_manifest_sha256'] != data.file_sha(ROOT / 'benchmarks/performance_v1/manifest.json'):
        raise ValueError('Frozen source manifest mismatch')
    if data.file_sha(run / 'source-inputs.jsonl') != data.file_sha(runner.task.DATASET / 'inputs.jsonl'):
        raise ValueError('Source inputs changed')
    items = list(data.read_jsonl(run / 'workloads.jsonl'))
    rebuilt, inventory = runner.workload([f['id'] for f in config['families']])
    if items != rebuilt or inventory != config['families'] or data.file_sha(run / 'workloads.jsonl') != config['workloads_sha256']:
        raise ValueError('Workload or original gold changed')
    first = config['cells'][0]
    first_clinical = config['families'][0]['id']
    cs = list(dict.fromkeys(c['concurrency'] for c in config['cells'] if c['family'] == first_clinical and c['repeat'] == 0))
    repeats = max(c['repeat'] for c in config['cells']) + 1
    if config['cells'] != runner.plan([f['id'] for f in inventory], repeats, tuple(cs), first['window_s'], first['warmup_s']):
        raise ValueError('Experiment matrix changed')
    by_id = {i['id']: i for i in items}

    def validate_record(record, model):
        item = by_id[record['item_id']]
        if record['model'] != model or record['family'] != item['family']:
            raise ValueError('Record identity mismatch')
        if record['request_sha256'] != data.digest(item['request']) or record['provider_request_sha256'] != data.digest(runner.task.payload(item['request'], model)):
            raise ValueError('Payload hash mismatch')
        if record['decisions'] != len(item['gold']):
            raise ValueError('Decision count mismatch')
        timings = [record[k] for k in ['http_start_s','elapsed_s','completion_s','admission_wait_s']]
        if any(not math.isfinite(t) or t < 0 for t in timings) or abs(record['http_start_s']+record['elapsed_s']-record['completion_s']) > 1e-8:
            raise ValueError('Invalid timing')
        if 'response' in record:
            score = runner.task.evaluate(item, record['response'], model)
            if any(record[k] != v for k,v in score.items()):
                raise ValueError('Raw response score mismatch')
            if record['status'] != ('success' if score['complete_valid'] else 'invalid_answer'):
                raise ValueError('Raw response status mismatch')
        elif any(record[k] for k in ['valid_decisions','correct_decisions','complete_valid','all_correct']):
            raise ValueError('Failed response contains positive score')

    calibration = []
    for model in runner.MODELS:
        path = run / f'calibration-{model}.json'
        if not path.exists():
            continue
        records = read(path)['records']
        if not status['fatal'] and [r['item_id'] for r in records] != [i['id'] for i in items]:
            raise ValueError('Calibration coverage mismatch')
        dns = read(run / f'dns-{model}.json')
        if not dns['answers'] or dns['host'] != runner.urlsplit(runner.task.clinical.MODELS[model]['endpoint']).hostname:
            raise ValueError('DNS endpoint mismatch')
        for record in records:
            validate_record(record,model)
        calibration.extend(records)
    summaries = read(run / 'summary.json')
    if len(summaries) != status['finished_cells'] or len(config['cells']) != status['planned_cells']:
        raise ValueError('Run status mismatch')
    if not status['fatal'] and len(summaries) != len(config['cells']):
        raise ValueError('Missing cells without run failure')
    verified = []
    for index, saved in enumerate(summaries):
        cell = config['cells'][index]
        if saved['cell'] != index or any(saved[k] != v for k,v in cell.items()):
            raise ValueError('Cell identity mismatch')
        if 'skipped' in saved:
            verified.append((saved, []))
            continue
        records = list(data.read_jsonl(run / saved['records_file']))
        expected = {i['id']:len(i['gold']) for i in items if i['family']==cell['family'] and (cell['family']!='routing_200' or i['target']==200)}
        for sequence, record in enumerate(records):
            if record['item_id'] not in expected or record['sequence'] != sequence:
                raise ValueError('Unexpected workload or response sequence')
            validate_record(record,cell['model'])
            if record['http_start_s'] >= cell['warmup_s']+cell['window_s']+.01 or record['completion_s']>saved['wall_s']+.001:
                raise ValueError('Response timing outside cell')
        lags = read(run / f'lag-{index:03d}.json')
        computed = runner.summarize(records,cell,saved['wall_s'],saved['stop_reason'],lags,expected)
        if any(saved[k] != v for k,v in computed.items()):
            raise ValueError('Stored summary mismatch')
        verified.append((saved,records))
    all_records = calibration + [r for _,rows in verified for r in rows]
    cost = sum(runner.task.metrics.costs([r for r in all_records if r['model']==m],m)['usd_upper'] for m in runner.MODELS)
    if abs(status['cost_upper_usd'] - cost)>1e-8:
        raise ValueError('Run cost mismatch')
    return config,status,items,verified,calibration


def aggregate(config,status,items,verified,calibration):
    def omission(saved, records):
        result={'repeat':saved['repeat'],'reason':saved.get('skipped') or saved.get('stop_reason')}
        if saved.get('stop_reason')=='service_error_circuit':
            recent=deque(maxlen=20)
            for record in records:
                recent.append(record['status'] in {'request_error','timeout'})
                if len(recent)==20 and sum(recent)>=10:
                    result['trigger_at_s']=record['completion_s']
                    result['phase']='drain' if record['completion_s']>=saved['warmup_s']+saved['window_s'] else 'load'
                    break
        return result
    grouped = defaultdict(list)
    for saved,records in verified:
        grouped[(saved['family'],saved['concurrency'],saved['model'])].append((saved,records))
    modes = []
    for (family,concurrency,model), group in grouped.items():
        completed = [(s,rs) for s,rs in group if s.get('full_window')]
        mode = dict(family=family,concurrency=concurrency,model=model,
                    attempted_repeats=len(group),full_repeats=len(completed),
                    repeat_metrics=[{'repeat':s['repeat'],'valid_per_s':s['valid_decisions_per_s'],
                                     'accuracy':s['balanced_accuracy'],'cost':s['cost'],
                                     'end_to_end_p95_s':s['end_to_end_p95_s'],
                                     'mean_http_concurrency':s['mean_http_concurrency']} for s,_ in completed],
                    omitted=[omission(s,rs) for s,rs in group if not s.get('full_window')])
        if not completed:
            modes.append(mode)
            continue
        cohorts, done, by_packet = [], [], defaultdict(list)
        for s,rs in completed:
            start,end=s['warmup_s'],s['warmup_s']+s['window_s']
            cohort=[r for r in rs if start<=r['http_start_s']<end]
            cohorts.extend(cohort)
            done.extend(r for r in rs if start<=r['completion_s']<end)
            for r in cohort:
                by_packet[r['item_id']].append(r)
        expected={i['id']:len(i['gold']) for i in items if i['family']==family and (family!='routing_200' or i['target']==200)}
        total_s=sum(s['window_s'] for s,_ in completed)
        accuracy=sum(statistics.mean(r['correct_decisions'] for r in by_packet[uid]) for uid in expected)/sum(expected.values()) if set(by_packet)==set(expected) else None
        usage=Counter()
        for r in cohorts:
            for k,v in r.get('response',{}).get('usage',{}).items():
                if isinstance(v,int): usage[k]+=v
        mode.update(window_s=total_s,unique_decisions=sum(expected.values()),
            packet_sizes=sorted(set(expected.values())),cohort_requests=len(cohorts),
            accuracy=accuracy,valid_per_s=sum(r['valid_decisions'] for r in done)/total_s,
            correct_per_s=sum(r['correct_decisions'] for r in done)/total_s,
            cohort_valid_rate=sum(r['valid_decisions'] for r in cohorts)/sum(r['decisions'] for r in cohorts) if cohorts else None,
            cohort_accuracy_among_valid=sum(r['correct_decisions'] for r in cohorts)/sum(r['valid_decisions'] for r in cohorts) if sum(r['valid_decisions'] for r in cohorts) else None,
            complete_packets_per_s=sum(r['complete_valid'] for r in done)/total_s,
            throughput_range=[min(s['valid_decisions_per_s'] for s,_ in completed),max(s['valid_decisions_per_s'] for s,_ in completed)],
            complete_rate=sum(r['complete_valid'] for r in cohorts)/len(cohorts) if cohorts else None,
            response_p95_s=runner.task.clinical.percentile([r['elapsed_s'] for r in cohorts],.95),
            end_to_end_p95_s=runner.task.clinical.percentile([r['elapsed_s']+r['admission_wait_s'] for r in cohorts],.95),
            admission_wait_mean_s=statistics.mean(r['admission_wait_s'] for r in cohorts) if cohorts else None,
            mean_http_concurrency=sum(s['mean_http_concurrency']*s['window_s'] for s,_ in completed)/total_s,
            max_http_concurrency=max(s['max_http_concurrency'] for s,_ in completed),
            event_loop_lag_max_s=max(s['event_loop_lag_max_s'] for s,_ in completed),
            status_counts=dict(Counter(r['status'] for r in cohorts)),
            http_counts=dict(Counter(str(r.get('http_status','none')) for r in cohorts)),
            cache_hit_ratio=usage['prompt_cache_hit_tokens']/(usage['prompt_cache_hit_tokens']+usage['prompt_cache_miss_tokens']) if usage['prompt_cache_hit_tokens']+usage['prompt_cache_miss_tokens'] else None,
            usage=dict(usage),cost=runner.task.metrics.costs(cohorts,model))
        modes.append(mode)
    return {'config':config,'status':status,'modes':modes,
            'measured_requests':sum(len(rows) for _,rows in verified),
            'calibration_requests':len(calibration),'cells':len(verified),
            'full_cells':sum(bool(s.get('full_window')) for s,_ in verified)}


def number(value,precision=1):
    return '—' if value is None else f'{value:.{precision}f}'


def percent(value):
    return '—' if value is None else f'{value:.2%}'


def cost_text(mode):
    cost=mode['cost']
    lo,hi=cost['usd_per_1000_correct_lower'],cost['usd_per_1000_correct_upper']
    if cost['unpriced_requests']: return '待核算'
    if lo is None: return '—'
    return f'{lo:.4f}' if lo==hi else f'{lo:.4f}–{hi:.4f}'


def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows])


def task_section(result,family,depth=2):
    groups=sorted([m for m in result['modes'] if m['family']==family],key=lambda m:(m['concurrency'],runner.MODELS.index(m['model'])))
    rows,diagnostics=[],[]
    for m in groups:
        if not m['full_repeats']:
            rows.append([m['concurrency'],LABELS[m['model']]]+['未纳入']*5)
            continue
        rows.append([m['concurrency'],LABELS[m['model']],number(m['valid_per_s']),percent(m['accuracy']),
                     number(m['response_p95_s'],3),cost_text(m),percent(m['complete_rate'])])
        diagnostics.append([m['concurrency'],LABELS[m['model']],f"{m['full_repeats']}/{m['attempted_repeats']}",
                            '–'.join(number(x) for x in m['throughput_range']),
                            f"{m['mean_http_concurrency']:.1f} / {m['max_http_concurrency']}",
                            number(m['admission_wait_mean_s'],3),number(m['end_to_end_p95_s'],3),m['cohort_requests'],
                            ' / '.join(str(m['status_counts'].get(k,0)) for k in ['timeout','request_error','invalid_answer'])])
    return '\n\n'.join([
        table(['配置并发','模型','合法判断／秒 ↑','准确率 ↑','完整响应 P95 秒 ↓','美元／千次正确 ↓','完整包率 ↑'],rows),
        '#' * (depth+1)+' 运行边界',
        table(['配置并发','模型','纳入轮次','吞吐逐轮范围','实际并发均值／峰值','配额等待均值秒','含等待 P95 秒','计分请求数','超时／请求错误／无效包'],diagnostics),
        '准确率按固定原题等权计算；重复请求不增加医学样本。合法判断可以答错，完整包率表示所有题均返回合法选项的请求比例。吞吐只统计固定时间窗口内完成的判断；准确率、延迟和成本统计窗口内发出的请求。'])


def render(result):
    cfg=result['config']
    parts=['# 持续多题并发结果',
           f"正式负载请求 {result['measured_requests']:,} 次，校准请求 {result['calibration_requests']} 次；{result['full_cells']} / {len(cfg['cells'])} 个计划窗口纳入汇总。已知用量按高峰价累计 ${result['status']['cost_upper_usd']:.4f}；缺失用量未作零费用解释。",
           '[测试协议](../../docs/SUSTAINED_THROUGHPUT.md) · [配置](config.json) · [汇总](comparison.json) · [逐档统计](summary.json) · [完整性清单](archive_manifest.json)',
           '每请求 8 道医疗题，工作器持续补入，5 秒预热后统计 30 秒，重复两轮。200 题分流板为单独的非医疗工程测试。实际并发可能受服务配额约束；这些结果不是模型吞吐上限或全天稳定性证明。']
    parts.append('两模型在校准前完成系统 DNS 解析，整轮复用解析结果；查询耗时另存于 dns-*.json。此前因 DNS 延迟中断的环境预跑单独保留，未混入本轮统计。格式错误与选项错误均影响端到端准确率，不能把二者全部归因于医学推理能力；汇总 JSON 另列合法选项比例及合法项中的准确率。')
    for family in cfg['families']:
        parts.extend(['## '+family['title'],f"{family['selected']} 道独立原题，固定每请求最多 8 题。",task_section(result,family['id'])])
    parts.extend(['## 200 题规则分流板（非医疗）','每请求 200 题，三块固定分流板循环发送；不用于医疗能力结论。',task_section(result,'routing_200')])
    skipped=[m for m in result['modes'] if m['omitted']]
    if skipped:
        parts.extend(['## 未完成记录',table(['任务','并发','模型','记录'],[[m['family'],m['concurrency'],m['model'],json.dumps(m['omitted'],ensure_ascii=False)] for m in skipped])])
    return '\n\n'.join(parts)+'\n'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',type=Path,default=RUN)
    p.add_argument('--check',action='store_true')
    args=p.parse_args()
    result=aggregate(*verify(args.run))
    outputs={args.run/'comparison.json':json.dumps(result,ensure_ascii=False,indent=2)+'\n',args.run/'README.md':render(result)}
    for path,content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text()!=content: raise ValueError('Stale report: '+str(path))
        else: path.write_text(content)
    print(f"Verified {result['cells']} cells / {result['measured_requests']} load requests")


if __name__=='__main__':
    main()
