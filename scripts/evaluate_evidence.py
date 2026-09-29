"""Offline evidence audit of archived paired predictions (standard library only)."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import random

import benchmark as b
from build_case_inventory import case_key
from verify_experiments import prediction

ROOT = Path(__file__).resolve().parents[1]
REPEATS = 2000
SEED = 20260930


def read(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def index(rows):
    result = {}
    for row in rows:
        key = (row['task'], row['id'])
        if key in result:
            raise ValueError(f'Duplicate response: {key}')
        result[key] = row
    return result


def wilson(errors, n):
    """Two-sided 95% Wilson interval; null when there are no observations."""
    if not n:
        return None
    z = 1.959963984540054
    p = errors / n
    center = (p + z*z/(2*n)) / (1 + z*z/n)
    half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return {'lower': max(0, center-half), 'upper': min(1, center+half)}


def stats(gold, pred):
    if isinstance(gold, set):
        return (len(gold & pred), len(pred-gold), len(gold-pred))
    return (int(gold == pred), 1)


def metric(total):
    if len(total) == 2:
        return total[0] / total[1] if total[1] else None
    denominator = 2*total[0] + total[1] + total[2]
    return 2*total[0]/denominator if denominator else 0.0


def paired_interval(items, repeats=REPEATS):
    """Resample source cases once per draw, sharing draws between providers."""
    groups = defaultdict(list)
    for group, j, d in items:
        groups[group].append((j, d))
    if not groups:
        raise ValueError('No cases')
    width = len(items[0][1])
    totals = []
    for key in sorted(groups):
        totals.append(tuple(tuple(sum(pair[p][i] for pair in groups[key])
                                  for i in range(width)) for p in (0, 1)))
    point = [metric([sum(t[p][i] for t in totals) for i in range(width)]) for p in (0, 1)]
    result = {'groups': len(groups), 'jev': point[0], 'deepseek': point[1],
              'difference': point[0]-point[1], 'ci95': None}
    if len(groups) < 2:
        return result
    rng = random.Random(SEED)
    draws = [[], [], []]
    for _ in range(repeats):
        sums = [[0]*width for _ in (0, 1)]
        for _ in totals:
            t = rng.choice(totals)
            for p in (0, 1):
                for i in range(width):
                    sums[p][i] += t[p][i]
        j, d = map(metric, sums)
        for bucket, value in zip(draws, (j, d, j-d)):
            bucket.append(value)
    result['ci95'] = {}
    for name, values in zip(('jev', 'deepseek', 'difference'), draws):
        values.sort()
        result['ci95'][name] = {'lower': values[int((repeats-1)*.025)],
                                'upper': values[int((repeats-1)*.975)]}
    return result


def resolve(row, response, provider):
    if response is None:
        return None, False
    if (response['task'], response['id'], response['request_sha256']) != (
            row['task'], row['id'], row['request_sha256']):
        raise ValueError('Response identity / request hash mismatch')
    if response.get('status') != 'ok':
        return None, False
    if provider == 'jev':
        b.validate_response(row['request'], response['response'])
        return prediction(row, response)[1], True
    answers = response['normalized_answers']
    if set(answers) != set(row['request']['questions']):
        raise ValueError('Comparison question mismatch')
    for key, q in row['request']['questions'].items():
        if q['type'] == 'choice' and answers[key]['choice'] not in q['criteria']:
            raise ValueError('Comparison label mismatch')
        if q['type'] == 'noul' and (type(answers[key]['noul']) not in (int, float)
                or not math.isfinite(answers[key]['noul']) or not 0 <= answers[key]['noul'] <= 1):
            raise ValueError('Comparison Noul invalid')
    return prediction(row, {'response': {'answers': answers}})[1], True


def gold_value(row):
    if row['metadata'].get('scoring') in ('multi_label_vocabulary', 'multi_question_keys') or row['task'] in ('nli4ct_evidence', 'medjourney_departments'):
        return set(row['gold'])
    if row['task'] == 'imcs_ner_dictionary_pipeline':
        return {tuple(x) for x in row['gold']}
    return row['gold']


def selection(observations, threshold, field):
    accepted = [o for o in observations if o.get(field) is not None and o[field] >= threshold and o['valid']]
    errors = sum(not o['correct'] for o in accepted)
    groups = defaultdict(list)
    for o in accepted:
        groups[o['case']].append(o['correct'])
    error_groups = sum(not all(values) for values in groups.values())
    return {'threshold': threshold, 'accepted': len(accepted), 'errors': errors,
            'coverage': len(accepted)/len(observations), 'review_required': len(observations)-len(accepted),
            'error_rate': errors/len(accepted) if accepted else None,
            'accepted_cases': len(groups), 'cases_with_errors': error_groups,
            'case_error_wilson95': wilson(error_groups, len(groups))}


def audit_task(rows, jev, deepseek, safety_rules):
    paired = []
    observations = []
    outcomes = {p: defaultdict(list) for p in ('jev', 'deepseek')}
    failures = Counter()
    slices = defaultdict(list)
    confusion = {p: Counter() for p in outcomes}
    events = {rule['id']: {p: {'eligible': 0, 'events': 0, 'unresolved': 0} for p in outcomes} for rule in safety_rules}
    for row in rows:
        if b.sha(row['request']) != row['request_sha256']:
            raise ValueError('Input hash mismatch')
        key = (row['task'], row['id'])
        g = gold_value(row)
        predictions, valid = {}, {}
        for p, source in (('jev', jev), ('deepseek', deepseek)):
            predictions[p], valid[p] = resolve(row, source.get(key), p)
            failures[p] += not valid[p]
            # Keep transport failure separate from valid empty prediction.
            if not valid[p]:
                predictions[p] = set() if isinstance(g, set) else '__FAILED__'
            outcomes[p][case_key(row)].append(valid[p] and predictions[p] == g)
            if not isinstance(g, set):
                confusion[p][(g, predictions[p])] += 1
            for rule in safety_rules:
                if g in rule['gold']:
                    event = events[rule['id']][p]
                    event['eligible'] += 1
                    event['events'] += valid[p] and predictions[p] in rule['prediction']
                    event['unresolved'] += not valid[p]
        paired.append((case_key(row), stats(g, predictions['jev']), stats(g, predictions['deepseek'])))
        cohort = row['metadata'].get('cohort', 'original_archive')
        slices[cohort].append((g, predictions, valid))
        if not isinstance(g, set):
            answer = jev.get(key, {}).get('response', {}).get('answers', {}).get('decision', {})
            probabilities = answer.get('probabilities', {})
            confidence = answer.get('confidence')
            if confidence is not None and (type(confidence) not in (int, float) or not math.isfinite(confidence) or not 0 <= confidence <= 1):
                raise ValueError('Invalid confidence')
            observations.append({'id': row['id'], 'case': case_key(row), 'valid': valid['jev'],
                                 'correct': valid['jev'] and g == predictions['jev'],
                                 'probability': probabilities.get(predictions['jev']), 'confidence': confidence,
                                 'brier': sum((v-int(k == g))**2 for k, v in probabilities.items()) if g in probabilities else None})
    result = {'records': len(rows), 'cases': len(outcomes['jev']),
              'metric': 'micro_f1' if isinstance(gold_value(rows[0]), set) else 'accuracy',
              'paired': paired_interval(paired), 'failures': dict(failures),
              'case_all_correct': {p: {'correct': sum(all(v) for v in groups.values()), 'total': len(groups),
                                          'rate': sum(all(v) for v in groups.values())/len(groups)} for p, groups in outcomes.items()},
              'safety_events': events, 'cohorts': {}}
    for name, values in sorted(slices.items()):
        result['cohorts'][name] = {'records': len(values), **{p: metric([sum(stats(g, pred[p])[i] for g, pred, _ in values) for i in range(len(paired[0][1]))]) for p in outcomes}}
    if observations:
        result['confusion'] = {p: [{'gold': g, 'prediction': pred, 'n': n} for (g, pred), n in sorted(c.items())] for p, c in confusion.items()}
        counts = Counter(row['gold'] for row in rows)
        result['majority_label_reference'] = {'accuracy': max(counts.values())/len(rows), 'scope': 'test-label descriptive reference; not a trained baseline'}
        result['selective_risk'] = {field: [selection(observations, cutoff, field) for cutoff in (0, .8, .9, .95, .99)] for field in ('probability', 'confidence')}
        briers = [o['brier'] for o in observations if o['brier'] is not None]
        bins = []
        for i in range(10):
            subset = [o for o in observations if o['probability'] is not None and min(9, int(o['probability']*10)) == i]
            if subset:
                bins.append({'lower': i/10, 'n': len(subset), 'mean_probability': sum(o['probability'] for o in subset)/len(subset), 'accuracy': sum(o['correct'] for o in subset)/len(subset)})
        result['calibration'] = {'brier_n': len(briers), 'brier_sum_mean': sum(briers)/len(briers) if briers else None,
                                 'bins': bins, 'ece10': sum(x['n']*abs(x['mean_probability']-x['accuracy']) for x in bins)/sum(x['n'] for x in bins) if bins else None}
        result['high_probability_errors'] = [o['id'] for o in observations if not o['correct'] and o['probability'] is not None and o['probability'] >= .95]
    return result


def build():
    config_path = ROOT/'evaluation/evidence_policy.json'
    config = json.loads(config_path.read_text())
    methods = json.loads((ROOT/'results/task_methods.json').read_text())
    scenes = json.loads((ROOT/'results/scenario_manifest.json').read_text())['scenes']
    tasks, inputs = {}, {}
    for scene in scenes:
        for task in scene['task_ids']:
            folder = ROOT/'scenarios'/scene['id']/task
            paths = [folder/'samples.jsonl', folder/'responses.jsonl', folder/'comparison/deepseek_responses.jsonl']
            for p in paths:
                inputs[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
            rows = read(paths[0])
            j, d = index(read(paths[1])), index(read(paths[2]))
            keys = {(r['task'], r['id']) for r in rows}
            if len(keys) != len(rows) or any(r['task'] != task for r in rows) or set(j)-keys or set(d)-keys:
                raise ValueError('Archive identity mismatch')
            result = audit_task(rows, j, d, config['safety_events'].get(task, []))
            result.update(title=methods[task]['title'], scene=scene['id'], synthetic=task.startswith('challenge_'),
                          provided_gold_span=any('given_gold_span' in str(r['metadata'].get('oracle', '')) for r in rows) or 'oracle_span' in task or 'oracle_entities' in task or 'oracle_pairs' in task)
            tasks[task] = result
    return {'schema_version': 1, 'analysis': 'retrospective_exploratory', 'seed': SEED, 'bootstrap_repeats': REPEATS,
            'interval_scope': 'pointwise, paired source-case percentile bootstrap; no multiplicity correction; no deployment certification',
            'policy_sha256': hashlib.sha256(config_path.read_bytes()).hexdigest(),
            'input_sha256': inputs, 'tasks': tasks}


def percent(v):
    return '—' if v is None else f'{v:.1%}'


def render(report):
    lines = ['# 医疗适用性证据审计', '', '这是对已有真实响应的回顾性再分析，没有新增模型调用。所有差异区间按来源案例成组、两模型配对重采样 2,000 次；同一病例的多条问题不会被当成独立病例。', '',
             '区间为逐任务探索性 95% 区间，未校正多重比较，不能据此给 96 个任务排显著性榜单。零错误时 bootstrap 区间可能退化；来源分组仍可能遗漏模板或机构相关性。', '',
             '## 错误方向', '', '事件由标签定义，尚未经医生逐例判定严重程度；分母是符合条件的金标记录。接口失败单列为未解决，不能算安全通过。', '',
             '| 任务 / 错误事件 | Jev 事件 / 分母 | DeepSeek 事件 / 分母 | 未解决 Jev / DeepSeek |', '| --- | ---: | ---: | ---: |']
    config = json.loads((ROOT/'evaluation/evidence_policy.json').read_text())
    for task, rules in config['safety_events'].items():
        for rule in rules:
            e = report['tasks'][task]['safety_events'][rule['id']]
            lines.append(f'| {report["tasks"][task]["title"]}：{rule["label"]} | {e["jev"]["events"]} / {e["jev"]["eligible"]} | {e["deepseek"]["events"]} / {e["deepseek"]["eligible"]} | {e["jev"]["unresolved"]} / {e["deepseek"]["unresolved"]} |')
    lines += ['', '## 高概率筛选与人工复核', '', '固定阈值 0.95，仅检查 Choice 所选标签的 probability；API confidence 在 JSON 中另列，两者不互相替代。阈值是回顾性诊断，未在独立开发集选择或前瞻验证。复核数量包含低概率和无有效响应记录。', '',
              '病例错误上界是已接受案例中“至少一条错”的 Wilson 95% 区间上界，假设来源案例独立；不是逐字段风险上界或临床可接受阈值。零错误不等于零风险。', '',
              '| 任务 | 接受 / 总记录 | 接受后错误 | 需复核 | 接受案例错误上界 |', '| --- | ---: | ---: | ---: | ---: |']
    for task in config['focus_tasks']:
        r = report['tasks'][task]
        g = next(x for x in r['selective_risk']['probability'] if x['threshold'] == .95)
        interval = g['case_error_wilson95']
        lines.append(f'| {r["title"]} | {g["accepted"]} / {r["records"]} | {g["errors"]} | {g["review_required"]} | {percent(interval["upper"] if interval else None)} |')
    lines += ['', '## 全任务配对比较', '', 'Jev 与 DeepSeek 的数值对应 Accuracy 或 micro-F1；差值与区间单位为百分点。病例全对要求该案例的全部字段／集合完全匹配，且没有接口失败。集合任务仍保留原 micro-F1 口径，并用病例全对和失败数区分有效空集与失败。', '',
              '| 任务 | 类型 | 案例 / 记录 | Jev / DeepSeek | 差值 [95% 区间] | Jev 病例全对 |', '| --- | --- | ---: | ---: | ---: | ---: |']
    for task, r in report['tasks'].items():
        paired = r['paired']; ci = paired['ci95']['difference'] if paired['ci95'] else None
        interval = f'[{100*ci["lower"]:.1f}, {100*ci["upper"]:.1f}]' if ci else '不可估计'
        kind = '自编挑战' if r['synthetic'] else ('给定标准实体' if r['provided_gold_span'] else '公开数据适配')
        lines.append(f'| [{r["title"]}](../scenarios/{r["scene"]}/{task}/README.md) | {kind} | {r["cases"]} / {r["records"]} | {percent(paired["jev"])} / {percent(paired["deepseek"])} | {100*paired["difference"]:.1f} {interval} | {percent(r["case_all_correct"]["jev"]["rate"])} |')
    lines += ['', '## 如何复核', '', '`python3 scripts/evaluate_evidence.py --check` 重算全部指标并检查报告；[机器可读结果](../results/evidence_audit.json)保存来源文件哈希、混淆矩阵、分来源结果、Brier/ECE、两种置信度筛选及高概率错误 ID。', '',
              '测试集多数类比例仅用于判断类别不平衡，不是独立训练的基线。已有规则基线及候选召回上限见各任务原报告。结果只适用于归档版本和抽样；任务间可能复用病例，不能把各任务案例数相加当患者总数。', '',
              '[评测设计与权威参考](EVALUATION.md) · [复现步骤](REPRODUCING.md)', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    report = build()
    outputs = {ROOT/'results/evidence_audit.json': json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+'\n',
               ROOT/'docs/医疗适用性审计.md': render(report)}
    for path, content in outputs.items():
        if args.check:
            if path.read_text() != content:
                raise SystemExit(f'Stale audit: {path}')
        else:
            path.write_text(content)
    print(f'Verified evidence for {len(report["tasks"])} tasks; {sum(r["records"] for r in report["tasks"].values())} records')


if __name__ == '__main__':
    main()
