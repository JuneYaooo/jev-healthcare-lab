"""Task-first tables and figures for the four-model medical decision benchmark."""
from __future__ import annotations
import json
from pathlib import Path
import statistics
from html import escape
from itertools import groupby

import run_medical_load as run

ROOT = run.ROOT


def current_report_path():
    gateway = ROOT / 'results/medical-load-jev-gateway-v1/comparison.json'
    return gateway if gateway.exists() else ROOT / 'results/medical-load-v2/comparison.json'


def archive_path(report):
    return report.get('gateway', {}).get('archive', 'results/medical-load-v2')


def asset_path(report):
    return 'docs/assets/' + archive_path(report).split('/')[-1]


def number(value, digits=2, percent=False):
    return '—' if value is None else f'{value * (100 if percent else 1):.{digits}f}'


def price(values):
    if values is None:
        return '—'
    return number(values[0], 3) if values[0] == values[1] else f'{values[0]:.3f}–{values[1]:.3f}'


def table(headers, rows, text_columns=1, numeric_columns=None):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join('---:' if (i in numeric_columns if numeric_columns is not None else i >= text_columns)
                                       else '---' for i in range(len(headers))) + ' |',
                      *['| ' + ' | '.join(str(x).replace('|', '\\|') for x in row) + ' |' for row in rows]])


BEST_NOTE = '粗体表示同一任务、同一并发档内已测模型的最优观测值，并列最优均加粗；不表示统计显著性。成本区间重叠、无法确定最低者时不加粗。'


def best_models(family, concurrency='32'):
    metrics = {key: {} for key in ('accuracy', 'macro_f1', 'throughput', 'p95_http_s', 'cost')}
    for model, result in family['models'].items():
        for key in ('accuracy', 'macro_f1'):
            metrics[key][model] = result['quality'][key]
        for key in ('throughput', 'p95_http_s'):
            metrics[key][model] = result['load'][concurrency][key]
        metrics['cost'][model] = result['quality']['cost_cny_per_1000']
    winners = {}
    for key, values in metrics.items():
        known = {m: v for m, v in values.items() if v is not None}
        if key == 'cost':
            winners[key] = {m for m, v in known.items()
                            if all(v == other or v[1] <= other[0] for other in known.values())}
        else:
            best = (min if key == 'p95_http_s' else max)(known.values()) if known else None
            winners[key] = {m for m, v in known.items() if v == best}
    return winners


def emphasized(value, model, metric, winners, *, html=False):
    text = escape(value) if html else value
    if model not in winners[metric]:
        return text
    return f'<strong>{text}</strong>' if html else f'**{text}**'


def task_sections(report, fid, index, *, root=False):
    family = report['families'][fid]
    has_f1 = fid in {'trial_referral', 'triage_urgency', 'tcm_syndrome',
                     'tcm_pathogenesis_candidate', 'trial_shared_patient'}
    title = family['title']
    prefix = '' if root else '../../'
    rows = []
    winners = best_models(family)
    for model in report['config']['models']:
        result = family['models'][model]
        q, load = result['quality'], result['load']['32']
        def mark(value, metric):
            return emphasized(value, model, metric, winners)
        rows.append([report['models'][model]['label'], mark(number(q['accuracy'], percent=True), 'accuracy'),
                     *([mark(number(q['macro_f1'], percent=True), 'macro_f1')] if has_f1 else []),
                     mark(number(load['throughput']), 'throughput'), mark(number(load['p95_http_s'], 3), 'p95_http_s'),
                     mark(price(q['cost_cny_per_1000']), 'cost')])
    parts = [f'<a id="{fid}"></a>', f'## {title}' if root else '### 当前多题评测',
             f"**表 {index}｜{title}：{family['decisions']} 项独立判断，{family['cases']} 个来源组；每请求最多 {family['batch']} 项。准确率测试配置 8 并发，负载测试配置 32 并发。**",
             table(['模型', '准确率 (%) ↑', *(['Macro-F1 (%) ↑'] if has_f1 else []),
                    '吞吐量 (判断/秒) ↑', '完整响应 P95 (秒) ↓', '成本 (元/千项判断) ↓'], rows),
             f"准确率和成本来自完整的 {family['decisions']} 项固定题集；吞吐与 P95 来自其中预先选定的 {family['load_decisions']} 项判断，持续循环施压两轮。重复调用不增加独立题量。P95 从实际发出计时，不含额度排队；不足 20 个响应时留空。"]
    if family['small_sample']:
        parts.append('样本覆盖有限，只作探索性比较，尤其不能据此稳定估计临床可靠性。')
    if fid == 'trial_shared_patient':
        parts.append('8 位模拟患者各对应 8 项真实注册试验。患者材料放在共享 state 中，只传一次；每个问题对应一项候选试验。金标为上游的“不相关／可能适合／很可能适合转介”，不是逐条入排标准的专家判定。与原试验转介题集可能重合，不另计入总体图。')
        parts.append('三类金标分别为 49、9、6 项；全部回答“不相关”的多数类基线为准确率 76.56%、Macro-F1 28.91%。因此需结合 Macro-F1 判断模型是否识别了较少见的适合转介案例，不能仅看准确率。')
    if has_f1:
        parts.append('Macro-F1 对本任务金标中出现的类别等权平均；没有金标样本的候选类别不另加零分项，各模型使用相同类别集合。')
    if fid == 'tcm_pathogenesis_candidate':
        parts.append('这是候选病机的判断任务，按既有标注计分；不能由此推导自由生成辨证与处方的能力。')
    if fid == 'message_urgency_pair':
        parts.append('本任务严格区分原始选项键，例如 `Patient #1` 不能改写成 `Patient_1`。这类输出合约错误也按错计，因此成绩同时反映判断和接口可直接使用的程度，不能全部归因于医学推理差异。')
    parts.append(f'![{title}的并发吞吐对比]({prefix}{asset_path(report)}/{fid}.svg)')
    detail = []
    for c in ('8', '32'):
        winners = best_models(family, c)
        for model in report['config']['models']:
            v = family['models'][model]['load'][c]
            detail.append([report['models'][model]['label'], c,
                           emphasized(number(v['throughput']), model, 'throughput', winners),
                           emphasized(number(v['p95_http_s'], 3), model, 'p95_http_s', winners),
                           number(v['mean_http_concurrency'])])
    parts.append('<details>\n<summary>查看本任务的两个并发档</summary>\n\n'
                 + f'**表 {index}a｜{title}：每请求最多 {family["batch"]} 项，负载题集 {family["load_decisions"]} 项，各档两轮。**\n\n'
                 + table(['模型', '配置并发', '吞吐量 (判断/秒) ↑', '完整响应 P95 (秒) ↓', '实际平均同时请求数'], detail)
                 + '\n\n配置并发是工作器上限；实际在途请求可能因账户额度更少。P95 不含客户端额度等待；不足 20 个完整响应时不报告 P95。\n\n</details>')
    parts.append((f'[任务定义与数据]({prefix}docs/tasks/{fid}.md) · ' if root else '')
                 + f'[评估方法]({prefix}docs/MEDICAL_LOAD.md) · [原始记录与计价依据]({prefix}{archive_path(report)}/README.md)')
    if report.get('gateway') and not root:
        parts.append('JEV 返回版本为 `jev-1.13.0`；成本按官方标价估算，非实际账单。渠道与测试日期差异见评估方法。')
    if not root:
        parts.append(BEST_NOTE)
    return parts


def overview_table(report):
    scenes = {s['id']: s['title'] for s in json.loads((run.data.DEFAULT / 'taxonomy.json').read_text())['scenarios']}
    models = report['config']['models']
    headers = ['医疗场景', '具体任务', '独立题量', '模型', '准确率 (%) ↑', '吞吐量 (判断/秒) ↑', '成本 (元/千项判断) ↓']
    rows = ['<table>', '<thead><tr>' + ''.join(f'<th>{escape(h)}</th>' for h in headers) + '</tr></thead>', '<tbody>']
    for scene, group in groupby(report['families'].values(), key=lambda f: f['scenario']):
        families = list(group)
        for index, family in enumerate(families):
            winners = best_models(family)
            for mi, model in enumerate(models):
                cells = []
                if index == 0 and mi == 0:
                    cells.append(f'<td rowspan="{len(families) * len(models)}">{escape(scenes[scene])}</td>')
                if mi == 0:
                    cells.extend([
                        f'<td rowspan="{len(models)}"><a href="#{escape(family["id"], quote=True)}">{escape(family["title"])}</a></td>',
                        f'<td rowspan="{len(models)}" align="right">{family["decisions"]}</td>'])
                result = family['models'][model]
                cells.append(f'<td>{escape(report["models"][model]["label"])}</td>')
                for metric, value in [('accuracy', number(result['quality']['accuracy'], percent=True)),
                                      ('throughput', number(result['load']['32']['throughput'])),
                                      ('cost', price(result['quality']['cost_cny_per_1000']))]:
                    cells.append('<td align="right">' + emphasized(value, model, metric, winners, html=True) + '</td>')
                rows.append('<tr>' + ''.join(cells) + '</tr>')
    return '\n'.join([*rows, '</tbody>', '</table>'])


def gateway_findings(report):
    if not report.get('gateway'):
        return []
    statements = []
    for fid in ('patient_contraindication', 'medication_choice', 'tcm_syndrome'):
        family = report['families'][fid]
        j, f = (family['models'][m] for m in ('jev-1.13.0', 'deepseek-flash'))
        if any(v['quality']['accuracy'] is None or v['load']['32']['throughput'] is None for v in (j, f)):
            return []
        jt, ft = j['load']['32']['throughput'], f['load']['32']['throughput']
        speed = '更高' if jt > ft else '更低' if jt < ft else '相同'
        statements.append(
            f"- [{family['title']}](#{fid})：JEV 准确率 {number(j['quality']['accuracy'], percent=True)}%，"
            f"Flash 为 {number(f['quality']['accuracy'], percent=True)}%；本次 JEV 的 32 并发吞吐{speed}。")
    return ['三项任务体现出不同取舍（完整速度、成本及 Qwen 对比见表 1）：', '\n'.join(statements)]


def render(report):
    complete = [report['models'][m]['label'] for m in report['config']['models']
                if all(f['models'][m]['quality']['complete'] for f in report['families'].values())]
    parts = ['# JEV Healthcare Lab',
             '**简体中文** | [English](README.en.md)',
             '**评估 JEV 在医疗场景中的表现**：围绕分诊、诊断、用药、护理与临床试验筛选等具体任务，考察它的判断准确率、持续吞吐和使用成本，并与 DeepSeek Flash、Qwen 对照。',
             '## 项目背景与目的',
             'JEV 是 TypeSafe 推出的旗舰模型，官方将其定位为面向软件决策的 System One 模型：输入上下文（state）和类型化问题，直接返回程序可使用的结构化结果。其接口提供 Choice、Score、Noul 三类问题，并支持围绕同一份上下文并行处理多个独立判断。[官方介绍](https://docs.typesafe.ai/introduction)',
             '医疗工作流包含许多范围明确的判断，例如识别就医紧急程度、判断方案禁忌、选择下一步检查，以及筛选患者可能适合的临床试验。这些任务为检验 JEV 的结构化决策能力提供了具体场景：输出能否直接被程序读取，以及判断本身是否正确，都需要通过医疗题目验证。',
             '从接口设计和本次任务表现看，JEV 很适合高频、结构化、边界明确的决策场景：将上下文转为明确选项上的判断，再由程序组合成筛选、分流或审核流程。它在具体医疗任务上的适用程度，仍需结合各任务的准确率与错误类型判断。',
             '本项目希望回答三个问题：JEV 在哪些医疗任务上表现较好，在哪些任务上仍有短板；多题处理与持续并发时，准确率、吞吐和成本如何取舍；同一患者材料供多个问题共享的处理方式，在医疗筛选任务中表现如何。为此，项目公开固定题集、数据来源、评分方法与原始结果，便于复算和比较。',
             '当前评测聚焦有明确选项与标准答案的 Choice 任务；Score、Noul 和置信度校准尚未纳入验证。结果用于研究与原型选型，不构成临床有效性验证。',
             '## 评测结果',
             f'![医疗决策准确率、成本与吞吐对比]({asset_path(report)}/overview.png)',
             '本轮覆盖 26 个既有医疗任务的 1,514 项判断，另加 8 位模拟患者的 64 项试验转介判断。数据包含考试病例、模拟患者与公开标注，尚非临床部署验证。',
             '完整题集已完成的模型：' + '、'.join(complete) + '。']
    if report.get('gateway'):
        parts.extend(gateway_findings(report))
    missing = [report['models'][m]['label'] for m in report['config']['models'] if m not in [k for k in report['config']['models']
               if all(f['models'][k]['quality']['complete'] for f in report['families'].values())]]
    if missing:
        parts.append('**本轮尚未完成：' + '、'.join(missing) + '。** 相应成绩留空，当前尚不能完成四模型对比。[既有 JEV／Flash 阶段性测试](results/sustained-throughput-v1/README.md)另行保留。')
    parts += ['准确率按模型原样输出计分，非法选项也算错；它同时反映判断与输出可用性。吞吐表示每秒收到的合法判断数，**不等于每秒正确判断数**。成本按新病例、无缓存折扣的输入与输出用量折算，单位为人民币；Flash 区间对应闲时与高峰标价。',
              '**测试账户限制：本次测试受账户额度、请求限流及共享服务条件影响，部分性能指标可能无法充分反映模型能力，尤其是响应速度和吞吐量。** 表中数值是当前测试条件下的观测结果，不代表模型的性能上限，模型间的速度差距也不能直接外推到其他部署条件。Qwen 本次账户上限分别为 8 万／4 万 token 每分钟；网络与供应商缓存也会影响结果。',
              '**表 1｜医疗任务总览。准确率与成本来自完整题集的 8 并发多题测试；吞吐取预先指定的 32 并发档、两轮持续负载结果。点击任务进入详细结果。**',
              overview_table(report),
              BEST_NOTE,
              '“—”表示本轮未获得完整数据或样本不足。独立题量指不重复的判断项，不表示统计独立，也不等于独立患者数；患者／来源组数见每个任务表题。少于 20 题仅作探索性比较。三个空任务（剂量适宜性、危急值升级、就诊科室分流）暂不计分。',
              f'[评估方法与适用边界](docs/MEDICAL_LOAD.md) · [数据集与许可](docs/datasets/README.md) · [原始响应与复算]({archive_path(report)}/README.md)']
    for index, fid in enumerate(report['families'], 2):
        parts += task_sections(report, fid, index, root=True)
    return '\n\n'.join(parts) + '\n'


def protocol(report):
    content = '''# 医疗多问题与持续并发评估

[返回结果](../README.md) · [冻结配置](../results/medical-load-v2/config.json)

评估对象是有明确选项和标准答案的医疗判断。JEV 使用原生 Choice 接口；Flash 与两款 Qwen 关闭思考，返回题号到选项键的精简 JSON。所有模型使用相同材料、问题和金标，答案与溯源信息不进入请求。结构正确不代表判断正确。

本轮仅评估 Choice 类判断，不据此验证 Score、Noul 输出或概率校准质量。模型架构提供的接口性质与医疗任务的实际准确率是不同证据。

## 两种医疗负载

既有 26 个任务共 1,514 项判断：同一任务的独立病例按最多 8 项打包，各病例放在各自记录中，要求模型逐题独立判断。尾包不填充，不截断材料；字节级上下文保护与原始题目哈希均有记录。

新增“同一患者的多项试验转介筛选”：从 TrialGPT SIGIR 公开子集的 58 位模拟患者中，按固定种子哈希选 8 位；每位再按患者 ID 和试验 ID 的哈希选 8 项试验。选择不依赖答案。state 只放一份患者材料，候选试验分别放入问题中。64 项上游相关性标注原样使用，不自行生成临床金标。原始文件版本与许可沿用[TrialGPT 来源登记](datasets/trialgpt.md)。

这种共享患者材料的形式更接近 JEV 所强调的一份 state、多问题决策；跨病例打包则测批量处理。二者分别展示。当前没有 200 项同患者判断的独立医疗金标；[历史 200 项规则压力测试](SUSTAINED_THROUGHPUT.md)属于工程负载，不计入医疗准确率。

## 固定题集准确率和成本

先对全部独立题目做一次多题测试，配置并发 8。仅传输问题可重试，最多三次；格式错误、缺失选项、非法选项和截断输出不修补，按错计。每个题包取首次 HTTP 200 的完整原始响应。若仍有未收到响应的题包，该任务准确率留空，避免只统计容易完成的子集。

准确率是答对项数／全部独立判断数。仅在类别语义固定的任务中计算 Macro-F1，对金标中出现的类别等权平均，所有模型使用相同类别集合。没有金标样本的候选类别不额外增加零分项；预测成这类候选仍计为真实类别的漏判。随题变化的 A/B/C 和“患者 1／患者 2”等位置选项不当作临床类别。小样本只作探索性结果，重复调用不增加有效样本数。患者相关性、数据暴露、源标注质量与许可边界沿用原始数据说明。

成本是完成固定题集一次所需的输入与输出 token 标价估算，再折算为每千项判断。使用最终响应的实际 usage，但统一按**无缓存折扣、不含重试**的条件计价；不是账单金额，也不是每千次正确判断成本。实际负载支出与缓存 usage 另保存在原始记录中。缺失用量时不填价格。

2026-10-12 价格：[JEV](https://docs.typesafe.ai/models)为输入 $0.042／百万 token、输出免费；[Flash](https://api-docs.deepseek.com/quick_start/pricing/)输入闲时 $0.15／高峰 $0.30、输出 $0.60／$1.20；[硅基流动](https://cloud.siliconflow.cn/me/models) Qwen3.5-9B 为输入 ¥0.5、输出 ¥4，Qwen3.8-27B 为输入 ¥3、输出 ¥12，均按百万 token。9B 仅适用本轮未达到 128K 的输入档。美元按[当日人民币中间价](https://www.safe.gov.cn/AppStructured/hlw/RMBQuery.do) 1 USD＝6.7313 CNY 换算；保留原始币种和价格快照以供复算。

## 持续吞吐与完整响应时间

每个任务预先取最多四个题包，在 8、32 两个并发上限下持续补充请求，完成一包立即取下一包。每档两轮，第二轮颠倒并发档顺序，任务顺序由固定种子打散。各模型同时运行各自的测试队列，同一模型各窗口顺序执行；共用同一客户端，结果仍包含网络与平台因素。

每窗先预热 3 秒，再计时至少 20 秒。为避免低额度模型一窗只能发出极少请求，窗口延长至最大题包额度间隔的四倍，最长 120 秒；实际时长逐窗归档。这里只是短时持续负载，不能外推小时级稳定容量。

前一个任务未用完的额度预留等待在新窗口开始前消化。即使本窗口已不允许再发出请求，也继续观察到预定截止时刻，将剩余空闲时间计入分母，防止限流时提前结束窗口。

吞吐＝计时窗口内完成的合法判断数量／窗口秒数。窗口开始前发出、窗口内完成的响应计入；结束后才完成的响应不倒填。两轮按总完成量／总窗口时长合并；不选最好的一轮或最好的一档。0 表示短窗内没有收到合法判断，不能解释为长期处理能力为零；若响应明显长于窗口，需更长的预热和稳态测量才能估计容量。固定题集准确率不由循环负载的命中次数加权，因此快题重复得多不会抬高准确率。

P95 统计计时窗口内发出的请求，从实际 HTTP 发出到收到完整响应的时间，等待窗口尾部请求收完后计算；**不含客户端额度排队**。合计不足 20 个完整响应不报告 P95。实际平均在途请求由所有请求占用时间与窗口交集积分计算；配置并发不等于实际并发。

JEV 客户端上限为 76 请求／秒、9 万输入 token／秒；Flash 配置并发低于公开上限；Qwen 客户端以每秒 1,200／600 token 平滑发送，并预留输出长度，低于账户 8 万／4 万 token 每分钟上限。[硅基流动限额说明](https://api-docs.siliconflow.cn/docs/userguide/faqs/rate-limit-and-upgradation)规定各模型分别设置限额。初始额度预留可用历史同题 token 用量加打包开销，收到新响应后改用新 usage 加余量；历史答案和成绩不进入本轮评分。收到限流信号后退避，不绕过额度限制。

连接使用系统 DNS，保留正常 TLS 验证。连续观察的 20 个请求中有至少 10 个服务／连接异常时停止该窗口；出现环境中断的早期窗口也按同一规则排除重测，原记录保存在 `excluded/`。只有两轮均完整完成的档位进入比较，不按吞吐高低挑选窗口。

性能测量刻意使用重复题组，供应商缓存可能加速 Flash 等服务；成本列则表示无缓存的新病例标价。二者是独立维度，不能将吞吐与成本相乘推算本轮账单或冷缓存业务容量。客户端没有复用模型答案。

## 图表汇总

首页图只使用至少 20 项判断的 15 个既有任务，不包括新增共享患者面板。准确率和单位成本按任务等权平均；左图要求这 15 个任务质量与成本完整。右图另要求每个任务都有两轮完整、非零的 32 并发吞吐，再用调和平均表示等任务量的观测速度；存在零完成窗口时不估计总体持续容量，原始观测仍列在任务表中。图不是综合评分，不能掩盖具体任务的差异；选型以各任务表为准。

并发图点为两轮合并吞吐，竖线为两轮观察范围，不是置信区间。没有做显著性检验；数据量较小、源标注未经独立临床复核的结果，不据此声称临床优越性。
'''
    if report.get('gateway'):
        content = content.replace('results/medical-load-v2/config.json', archive_path(report) + '/config.json')
        content = content.replace('各模型同时运行各自的测试队列，同一模型各窗口顺序执行；共用同一客户端，结果仍包含网络与平台因素。',
                                  'Flash 与 Qwen 沿用原测试队列；JEV 通过第三方 API 另行补测，同一模型各窗口顺序执行。题包哈希与计分方法一致，但测试日期与平台不同。')
        content = content.replace('JEV 客户端上限为 76 请求／秒、9 万输入 token／秒；',
                                  'JEV 接入平台额度未知，不套用官方直连接口限额；客户端最多 32 个在途请求，收到限流信号后退避，触发服务熔断即停止；')
    return content


def visuals(report, *, english=False):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    fontpath = Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
    if fontpath.exists():
        plt.rcParams['font.family'] = FontProperties(fname=fontpath).get_name()
    plt.rcParams.update({'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.unicode_minus': False, 'svg.fonttype': 'none'})
    directory = ROOT / asset_path(report)
    if english:
        directory /= 'en'

    def localize(fig):
        if english:
            from medical_load_english import chart_text
            from matplotlib.text import Text
            for label in fig.findobj(Text):
                label.set_text(chart_text(label.get_text(), report))

    directory.mkdir(parents=True, exist_ok=True)
    colors = dict(zip(report['config']['models'], ['#087f5b', '#3366cc', '#c07914', '#8b5fa6']))
    for fid, family in report['families'].items():
        fig, ax = plt.subplots(figsize=(8, 3.2), layout='constrained')
        ax.set_title(f"{family['title']}（负载题集 {family['load_decisions']} 项）\n"
                     '点：两轮合并吞吐；竖线：两轮范围', fontsize=10)
        for model, value in family['models'].items():
            xs, ys, lo, hi = [], [], [], []
            for c in ('8', '32'):
                v = value['load'][c]
                if v['throughput'] is None:
                    continue
                xs.append(int(c)); ys.append(v['throughput'])
                lo.append(max(0, v['throughput']-v['throughput_range'][0]))
                hi.append(max(0, v['throughput_range'][1]-v['throughput']))
            if xs:
                ax.errorbar(xs, ys, yerr=[lo, hi], marker='o', capsize=3, linewidth=1.8,
                            color=colors[model], label=report['models'][model]['label'])
        ax.set(xticks=[8, 32], xlabel='配置并发（账户额度可能限制实际并发）', ylabel='吞吐量（判断/秒）', ylim=(0, None))
        ax.grid(axis='y', alpha=.18)
        if ax.lines:
            ax.legend(fontsize=8, loc='best', frameon=False)
        localize(fig)
        fig.savefig(directory / (fid + '.svg'), metadata={'Date': None})
        plt.close(fig)
    eligible = [f for f in report['families'].values() if f['decisions'] >= 20 and f['id'] != 'trial_shared_patient']
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), layout='constrained')
    shown = []
    for model in report['config']['models']:
        entries = [f['models'][model] for f in eligible]
        if any(e['quality']['accuracy'] is None or e['quality']['cost_cny_per_1000'] is None for e in entries):
            continue
        accuracy = statistics.mean(e['quality']['accuracy'] for e in entries)*100
        costs = [statistics.mean(e['quality']['cost_cny_per_1000'][i] for e in entries) for i in (0, 1)]
        label = report['models'][model]['label']
        shown.append(label)
        axes[0].plot(costs, [accuracy, accuracy], color=colors[model], linewidth=4, alpha=.5)
        points = [(axes[0], costs[0])]
        # Zero completed work in a short window cannot establish an infinite
        # long-run processing time. Keep it in task tables, not a harmonic
        # capacity estimate. The quality/cost chart remains independently valid.
        if all(e['load']['32']['throughput'] is not None and e['load']['32']['throughput'] > 0 for e in entries):
            throughput = len(entries)/sum(1/e['load']['32']['throughput'] for e in entries)
            points.append((axes[1], throughput))
        for ax, x in points:
            ax.scatter(x, accuracy, color=colors[model], s=90, zorder=3)
            detail = f'¥{price(costs)} / 千项' if ax is axes[0] else f'{x:.2f} 判断/秒'
            below = bool(report.get('gateway')) and ax is axes[1] and model == 'deepseek-flash'
            ax.annotate(f'{label}\n{accuracy:.2f}% · {detail}', (x, accuracy),
                        xytext=(6, -12) if below else (6, 9), va='top' if below else 'bottom',
                        textcoords='offset points', fontsize=9)
    for ax in axes:
        ax.set_ylabel('任务平均准确率（%）↑')
        ax.grid(alpha=.16)
        ax.margins(x=.30, y=.35)
        ax.set_xlim(left=0)
    axes[0].set_title('准确率与成本', fontsize=12, pad=12)
    axes[1].set_title('准确率与吞吐量', fontsize=12, pad=12)
    axes[0].set_xlabel('每千项判断成本（元）↓\nFlash 横线：闲时至高峰标价')
    axes[1].set_xlabel('等任务量吞吐（判断/秒）↑\n32 配置并发，受平台与账户额度影响\n未形成完整可汇总数据的模型不绘制')
    # Leave room for markers near zero without changing their measured values.
    axes[1].set_xlim(left=-.04 * axes[1].get_xlim()[1])
    fig.suptitle(f'JEV 与对照模型的医疗任务表现\n准确率、使用成本与吞吐量对比 · 汇总 {len(eligible)} 项医疗任务', fontsize=16)
    if not shown:
        axes[0].text(.5, .5, '完整结果尚未齐备', transform=axes[0].transAxes, ha='center')
    localize(fig)
    fig.savefig(directory / 'overview.png', dpi=160)
    fig.savefig(directory / 'overview.svg', metadata={'Date': None})
    plt.close(fig)
    for path in directory.glob('*.svg'):
        path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')


def archive_readme(report):
    if report.get('gateway'):
        return f'''# JEV 医疗多问题与并发测试

[结果总览](../../README.md) · [评估方法](../../docs/MEDICAL_LOAD.md)

27 个任务、1,578 项判断，沿用[原测试归档](../medical-load-v2/README.md)完全相同的题包和金标。JEV 的原始响应在本目录；Flash 与两款 Qwen 的原始响应继续保存在原归档。汇总文件记录两个来源，不将旧响应当作重新调用。

- [配置与渠道](config.json)、[题包](packets.jsonl)、[逐题来源](lineage.jsonl)、[价格快照](pricing.json)。
- [JEV 原始响应](jev-1.13.0/)、[合并复算结果](comparison.json)、[文件哈希](archive_manifest.json)、[接口适配源码](source/)。公共运行器沿用原归档中的冻结源码。
- 固定题集用于准确率与成本；预先选定的题包用于每任务 8／32 并发、各两轮持续负载。中断或不完整窗口不进入性能比较。

```bash
.venv/bin/python scripts/run_jev_gateway.py --check
.venv/bin/python scripts/generate_catalog_docs.py --check
```

重新生成报告、图表和文档不调用模型：

```bash
.venv/bin/python scripts/run_jev_gateway.py --report
.venv/bin/python scripts/render_medical_load_docs.py
.venv/bin/python scripts/generate_catalog_docs.py
```

运行测试使用本地 `JEV_GATEWAY_API_KEY`，调用命令为 `.venv/bin/python scripts/run_jev_gateway.py`。已完成题包和窗口可续跑复用；需要重新测量时应建立独立归档。费用保护按官方标价等价用量设置，不能保证接入平台的实际账单上限。
'''
    return f'''# 医疗多问题与持续并发原始记录

[结果总览](../../README.md) · [方法](../../docs/MEDICAL_LOAD.md)

本轮冻结 27 个任务、1,578 项独立判断，比较 JEV 1.13、DeepSeek V4.1 Flash、Qwen3.5-9B、Qwen3.8-27B。各模型的未完成项标注为缺失。

- [配置与题量](config.json)、[请求题包与评分金标](packets.jsonl)、[逐题来源与许可](lineage.jsonl)、[计价依据](pricing.json)。金标保存在本地归档，只发送 payload 白名单字段。
- 各模型目录的 `quality.jsonl.gz` 是全部固定题集请求；`任务-r轮次-c并发.jsonl.gz` 是逐请求负载响应；同名 JSON 记录窗口边界。原始响应均保留供应商 usage。
- [复算结果](comparison.json)、[文件哈希](archive_manifest.json)、[源代码快照](source/)。中断窗口保留为 `interrupted-*`，不参与性能汇总。
- 总体图不混入新增共享患者面板；该面板与既有转介题集可能有重合。

当前归档可核算的用量标价上界合计约 ¥{report['known_cost_cny_upper']:.2f}，不等于最终账单；缺失 usage、在途中断可能留下未观测费用。README 成本列另按最终响应、无缓存、不含重试的统一条件估算。

本地复算，无模型调用：

```bash
.venv/bin/python scripts/build_medical_load_report.py --check
.venv/bin/python scripts/generate_catalog_docs.py --check
```

重新生成图表与页面：

```bash
.venv/bin/python scripts/build_medical_load_report.py
.venv/bin/python scripts/render_medical_load_docs.py
.venv/bin/python scripts/generate_catalog_docs.py
```

重新调用会产生费用，需有效凭据与相应账户额度。运行器默认复用已完成题包与窗口；原归档应先复制留存，避免混淆不同时期模型版本。数据的研究／非商业许可仍分别适用，见[数据来源](../../docs/datasets/README.md)。
'''


if __name__ == '__main__':
    source = current_report_path()
    report = json.loads(source.read_text())
    visuals(report)
    visuals(report, english=True)
    print('Rendered medical-load overview and task charts')
