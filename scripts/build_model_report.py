"""Verify archived runs and render the clinical model comparison."""
import argparse
import collections
import json
from pathlib import Path
import tempfile

import medical_decision_dataset as data
import run_model_evaluation as runner

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / 'results/clinical-20261012'


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |']
                     + ['| ' + ' | '.join(str(x) for x in row) + ' |' for row in rows])


def pct(value):
    return '—' if value is None else f'{value * 100:.2f}%'


def seconds(value):
    return '—' if value is None else f'{value:.3f}'


def render():
    models = [m for m in runner.MODELS if (RUNS / m / 'config.json').exists()]
    if len(models) < 2:
        raise ValueError('A comparison requires at least two completed model archives')
    configs, summaries, scores, slices = {}, {}, {}, {}
    for model in models:
        folder = RUNS / model
        configs[model] = json.loads((folder / 'config.json').read_text())
        # Re-derive answers and verify every response against the exact frozen request.
        summaries[model] = runner.summarize(folder, data.DEFAULT, archived_dataset=RUNS / 'dataset_at_run')
        if not summaries[model]['complete']:
            raise ValueError('Do not publish an incomplete model comparison')
        snapshot = folder / 'tools/run_model_evaluation.py'
        if not snapshot.exists():
            snapshot = RUNS / 'tools/run_model_evaluation.py'
        if configs[model]['runner_sha256'] != data.file_sha(snapshot):
            raise ValueError('Archived runner does not match run configuration')
        scores[model] = json.loads((folder / 'scores.json').read_text())
        predictions = list(data.read_jsonl(folder / 'predictions.jsonl'))
        open_ids = {r['id'] for r in data.evaluation_rows(data.DEFAULT)}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'predictions.jsonl'
            data.write_jsonl(path, [r for r in predictions if r['id'] in open_ids])
            open_score = data.score(data.DEFAULT, path)
        slices[model] = {'open': {'records': open_score['records'],
                                 'primary_clinical_score': open_score['primary_clinical_score'],
                                 'task_macro_accuracy': open_score['task_macro_accuracy']},
                        'by_distribution': {distribution: data.metrics(
                            [r for r in data.evaluation_rows(data.DEFAULT, True)
                             if r['provenance']['distribution'] == distribution],
                            {r['id']: r['choice'] for r in predictions})
                            for distribution in ['open', 'research_noncommercial']}}
    for field in ['inputs_sha256', 'scope_policy_sha256', 'dataset_manifest_sha256', 'workers', 'timeout_s', 'max_attempts', 'scope', 'include_research']:
        if len({json.dumps(c[field], sort_keys=True) for c in configs.values()}) != 1:
            raise ValueError('Incomparable model configurations: ' + field)
    common = json.loads((data.DEFAULT / 'evaluation-summary.json').read_text())['clinical']
    labels = {m: runner.MODELS[m]['label'] for m in models}
    model_names = '、'.join(labels[m] for m in models[:-1]) + ' 和 ' + labels[models[-1]]
    overall = []
    for model in models:
        q, summary = scores[model], summaries[model]
        t = summary['overall_timing']
        overall.append([labels[model], pct(q['primary_clinical_score']), pct(q['task_macro_accuracy']),
                        f"{t['success']}/{t['total']}", seconds(t['mean_elapsed_s']),
                        seconds(t['p50_elapsed_s']), seconds(t['p95_elapsed_s']),
                        t['status_counts'].get('invalid_answer', 0),
                        t['status_counts'].get('request_error', 0), t['status_counts'].get('timeout', 0), t['retries']])
    parts = ['# 医疗决策模型评测',
             '[返回首页](../README.md) · [评测方法](EVALUATION.md) · [原始结果与运行配置](../results/clinical-20261012/README.md)',
             f'本轮比较 {model_names}。{len(models)} 个模型各测试相同的 1,514 道临床决策题，覆盖 26 个有题任务；3 个空任务不调用 API。开放许可部分为 1,284 题，非商业附加部分为 230 题。辅助任务与暂停任务不在本轮范围。',
             '## 总体结果',
             '主分数先对场景内所有有题任务等权，再对有成绩的场景等权；任务均分对全部 26 个有题任务等权。11 个不足 20 题的任务标记为小样本，仍计入总分；其成绩更易受个别题目影响。有效回答数表示返回了合法选项，不代表回答正确。',
             table(['模型', '临床主分数', '任务均分', '有效回答', '平均耗时（秒）', 'P50（秒）', 'P95（秒）', '无效回答', '请求失败', '超时', '重试次数'], overall),
             '## 逐任务结果',
             '每格为 **准确率 / 平均完整决策耗时（秒）**。所有有题任务计入总分，不足 20 题标记“小样本”；待补任务不填零分。',
             table(['任务', '题数', '状态'] + [labels[m] for m in models], [
                 [f"[{f['title']}](tasks/{f['id']}.md)", f['records'],
                  '待补' if not f['records'] else '计入总分（小样本）' if f['small_sample'] else '计入总分']
                 + [f"{pct(scores[m]['task_families'][f['id']]['accuracy'])} / {seconds(summaries[m]['task_timing'][f['id']]['mean_elapsed_s'])}" if f['records'] else '—' for m in models]
                 for f in common['families']]),
             '## 按许可范围查看',
             '这里按数据使用许可拆分，与题目难度和计分权重无关。**允许商业使用的数据**共 1,284 题，仍需遵循各来源的署名、许可保留或相同方式共享等条件；**仅限非商业使用的数据**共 230 题，来自 CARE-Bench（100）、TCM-SD（100）和 PMR-Synth（30），同样可以依许可公开分享，但许可不授权商业用途。具体条款见 [数据许可说明](EVALUATION.md#数据许可分组)。两部分都计入上方完整临床主分数。下表另对允许商业使用的子集独立计算场景主分数，所有有题任务都纳入；逐题准确率按题数加权，与场景等权主分数不同。',
             table(['模型', '允许商业使用子集 · 主分数', '允许商业使用子集 · 逐题准确率（1,284 题）', '仅限非商业子集 · 逐题准确率（230 题）'], [
                 [labels[m], pct(slices[m]['open']['primary_clinical_score']),
                  pct(slices[m]['by_distribution']['open']['accuracy']),
                  pct(slices[m]['by_distribution']['research_noncommercial']['accuracy'])] for m in models]),
             '## 运行条件',
             'JEV 使用官方 TypeSafe 接口，固定请求模型为 jev-1.13.0。DeepSeek 使用官方接口，分别请求 deepseek-flash 和 deepseek-v4-pro；两者关闭思考，temperature=0，输出上限 256 token。DeepSeek 返回模型别名，其实际底层检查点由服务商维护，原始响应保留 model 与 system_fingerprint。',
             '模型读取相同的 state、问题说明和候选项。JEV 使用原生 choice 接口；其他模型外加同一份 JSON 格式提示。金标、来源和适配元数据均不发送。字符串选项键必须与候选完全一致；解释文本、选项内容替代选项键、数字类型与截断输出都判为无效，不作事后修复。',
             '每个模型并发 8，HTTP 连接与读取超时 120 秒，最多 3 次尝试；只重试网络、超时、限流和暂时服务错误，不重试错误答案或格式错误。JEV 与两个 DeepSeek 模型的三组运行同期启动；两个 DeepSeek 模型共享同一服务商账户。三组正式运行前分别使用一条非评测颜色选择题检查接口，耗时不纳入结果。',
             '单题时间包含客户端序列化、HTTP 请求、响应验证及重试等待。模型服务、网络和服务商缓存条件并不相同，不能把全部时间差归因于模型推理速度；服务器计算时间未单独测量。没有跨模型复用本地答案，服务商自动缓存不可控，token 用量与命中记录保存在原始响应中。',
             '逐任务总耗时为该任务从首题开始到最后一题结束的墙钟时间，包含并发调度。原始日志采用 UTC，展示日期以 Asia/Shanghai 为准；各模型的实际起止时间保存在运行配置与任务日志中。',
             '## 完整耗时与失败明细']
    qwen_models = [m for m in models if runner.MODELS[m]['provider'] == 'siliconflow']
    if qwen_models:
        qwen_note = ('Qwen 通过 SiliconFlow 官方接口调用：' + '、'.join(configs[m]['remote_model'] for m in qwen_models)
                     + '。均设置 enable_thinking=false、temperature=0、输出上限 256 token，使用与 DeepSeek 相同的提示及严格答案校验。'
                     'Qwen 两组在前三组完成后同期补跑，共享一个 SiliconFlow 账户，使用同一份冻结题目；与前三组的服务商账户及运行时段不同。每组先用非评测颜色选择题检查接口，检查响应另存 interface-check.json，不计入成绩或耗时。'
                     '接口参数见 [SiliconFlow 官方文档](https://docs.siliconflow.cn/docs/api/chat-completions-post)。')
        for m in qwen_models:
            records = list(data.read_jsonl(RUNS / m / 'responses.jsonl'))
            failed = [r for r in records if r['status'] == 'request_error']
            limited = sum(r['attempt_history'][-1].get('http_status') == 429 for r in failed)
            if failed:
                qwen_note += (f" {labels[m]} 有 {len(failed)} 道题在重试后仍请求失败"
                              f"（其中 {limited} 道最终返回 HTTP 429 限流），这些题计错并保留全部尝试；"
                              '因此本轮得分同时受到服务可用性的影响。')
        parts.insert(parts.index('## 完整耗时与失败明细'), qwen_note)
    for model in models:
        parts.extend([f"### {labels[model]}", table(['任务', '题数', '有效回答', '平均秒', 'P50 秒', 'P95 秒', '任务总秒', '超时', '请求失败', '无效回答'], [
            [f['title'], f['records'], summaries[model]['task_timing'][f['id']]['success'],
             *[seconds(summaries[model]['task_timing'][f['id']][key]) for key in ['mean_elapsed_s', 'p50_elapsed_s', 'p95_elapsed_s', 'task_wall_s']],
             *[summaries[model]['task_timing'][f['id']]['status_counts'].get(key, 0) for key in ['timeout', 'request_error', 'invalid_answer']]]
            for f in common['families'] if f['records']])])
    parts.extend(['## 解释范围',
                  '这是公开数据上的单轮 API 决策测试。部分材料来自上游训练划分或公开考试题，不能证明模型从未见过；没有独立医生逐题复核，也不是临床有效性验证。小样本任务、题型和来源差异会影响成绩。本轮没有训练或微调模型。',
                  '模型接口与设置参考 [TypeSafe 模型文档](https://docs.typesafe.ai/models) 和 [DeepSeek 官方模型说明](https://api-docs.deepseek.com/quick_start/pricing/)。'])
    comparison = {'models': {m: {'label': labels[m], 'primary_clinical_score': scores[m]['primary_clinical_score'],
                        'task_macro_accuracy': scores[m]['task_macro_accuracy'], 'timing': summaries[m]['overall_timing'],
                        'tasks': {f: {**q, 'timing': summaries[m]['task_timing'][f]} for f, q in scores[m]['task_families'].items()},
                        'license_slices': slices[m]} for m in models},
                  'records': common['records'], 'scope': 'clinical', 'include_research': True,
                  'inputs_sha256': configs[models[0]]['inputs_sha256'],
                  'scope_policy_sha256': scores[models[0]]['scope_policy_sha256'],
                  'run_scope_policy_sha256': configs[models[0]]['scope_policy_sha256'],
                  'scorer_sha256': data.file_sha(Path(data.__file__))}
    readme = ['# 临床模型评测原始结果',
              '[返回首页](../../README.md) · [逐任务得分与耗时](../../docs/MODEL_RESULTS.md)',
              f'{len(models)} 组各 1,514 道题。每组保存冻结输入、配置、逐次原始响应、最终预测、质量评分、耗时汇总和任务墙钟记录。inputs.jsonl 包含开放及非商业材料，继承 [各来源许可](../../THIRD_PARTY_NOTICES.md)，不能将整组输入当作无限制开放数据。',
              table(['模型', '配置', '输入', '原始响应', '评分', '耗时'], [[labels[m], f'[{m}/config.json]({m}/config.json)',
                  f'[输入]({m}/inputs.jsonl)', f'[响应]({m}/responses.jsonl)', f'[评分]({m}/scores.json)', f'[耗时]({m}/summary.json)'] for m in models]),
              'tools/ 保存调用时的运行和评分代码快照，dataset_at_run/ 保存调用时的数据清单与范围策略。config.json 保留调用时的哈希；当前 scores.json、summary.json 和 comparison.json 按所有有题任务计入总分的现行规则离线重算，并记录当前评分策略哈希。原始输入、配置、响应及计时记录不变。archive_manifest.json 对档案文件记录 SHA-256；当前仓库可执行下列命令复核响应、重新计分并检查报告：',
              '```bash\npython3 scripts/build_model_report.py --check\n```',
              '逐题选择、错误和耗时均来自实际调用。失败保留在分母；没有按答案正确与否筛选或重跑。']
    return {ROOT / 'docs/MODEL_RESULTS.md': '\n\n'.join(parts) + '\n',
            RUNS / 'README.md': '\n\n'.join(readme) + '\n',
            RUNS / 'comparison.json': json.dumps(comparison, ensure_ascii=False, indent=2) + '\n'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    manifest_path = RUNS / 'archive_manifest.json'
    if args.check:
        manifest = json.loads(manifest_path.read_text())
        for name, expected in manifest['files'].items():
            if data.file_sha(RUNS / name) != expected:
                raise ValueError('Archive hash mismatch: ' + name)
    rendered = render()
    for path, value in rendered.items():
        if args.check:
            if not path.exists() or path.read_text() != value:
                raise ValueError('Stale report: ' + str(path))
        else:
            path.write_text(value)
    if not args.check:
        paths = [p for p in RUNS.rglob('*') if p.is_file() and p != manifest_path
                 and '__pycache__' not in p.parts and not p.name.startswith('.')]
        data.write_json(manifest_path, {'algorithm': 'SHA-256', 'files': {
            str(p.relative_to(RUNS)): data.file_sha(p) for p in sorted(paths)}})
    print('Verified clinical comparison.' if args.check else 'Wrote clinical comparison.')


if __name__ == '__main__':
    main()
