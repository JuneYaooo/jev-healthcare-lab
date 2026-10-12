"""Reader-facing sustained throughput tables, grouped by medical task."""
from __future__ import annotations
import build_sustained_throughput_report as report


def modes(result,family):
    return sorted([m for m in result['modes'] if m['family']==family],key=lambda m:(m['concurrency'],report.runner.MODELS.index(m['model'])))


def compact_table(result,family):
    rows=[]
    family_modes=modes(result,family)
    for original in family_modes:
        m=original
        peer=next((p for p in family_modes if p['concurrency']==m['concurrency'] and p['model']!=m['model']),None)
        if peer:
            common={r['repeat'] for r in m['repeat_metrics']} & {r['repeat'] for r in peer['repeat_metrics']}
            if len(common)==1:
                chosen=next(r for r in m['repeat_metrics'] if r['repeat'] in common)
                m={**m,**chosen,'full_repeats':1}
        if not m['full_repeats']:
            rows.append([m['concurrency'],report.LABELS[m['model']]]+['未纳入']*4+[f"0/{m['attempted_repeats']}"])
        else:
            rows.append([m['concurrency'],report.LABELS[m['model']],report.number(m['valid_per_s']),report.percent(m['accuracy']),
                         report.number(m['end_to_end_p95_s'],3),report.cost_text(m),f"{m['full_repeats']}/{m['attempted_repeats']}"])
    return report.table(['配置并发','模型','判断／秒 ↑','准确率 ↑','含排队 P95 秒 ↓','美元／千次正确 ↓','纳入轮次'],rows)


def finding(result,family):
    by={(m['concurrency'],m['model']):m for m in modes(result,family) if m['full_repeats']}
    pairs=[]
    for c in [8,32,64]:
        if all((c,m) in by for m in report.runner.MODELS):
            common=set.intersection(*[{r['repeat'] for r in by[(c,m)]['repeat_metrics']} for m in report.runner.MODELS])
            if common: pairs.append((c,common))
    if not pairs:
        return '两模型尚无同档、同轮均完整完成的结果，暂不判断谁在本任务更快或更省。未完成与跳过记录保留在原始结果中。'
    c,common=max(pairs,key=lambda p:p[0])
    j,f=[by[(c,m)] for m in report.runner.MODELS]
    if len(common)==1:
        repeat=next(iter(common))
        j,f=[next(r for r in m['repeat_metrics'] if r['repeat']==repeat) for m in [j,f]]
        prefix=f'双方最高可比档为 {c} 并发，但仅第 {repeat+1} 轮均完整完成，以下为该轮观察，尚不能确认稳定优势。'
    else:
        prefix=f'在双方两轮均完成的最高档（{c} 并发），'
    text=prefix+f"JEV 每秒返回 {j['valid_per_s']:.1f} 个合法判断，Flash 为 {f['valid_per_s']:.1f}；准确率分别为 {j['accuracy']:.2%}、{f['accuracy']:.2%}。"
    jc,fc=j['cost'],f['cost']
    if jc['unpriced_requests'] or fc['unpriced_requests']:
        text+='该档有请求缺少用量，完整成本暂不能比较。'
    elif jc['usd_per_1000_correct_upper'] is not None and fc['usd_per_1000_correct_lower'] is not None:
        jlo,jhi=jc['usd_per_1000_correct_lower'],jc['usd_per_1000_correct_upper']
        flo,fhi=fc['usd_per_1000_correct_lower'],fc['usd_per_1000_correct_upper']
        if jhi<flo: text+='JEV 每千次正确判断的估算成本更低。'
        elif jlo>fhi: text+='Flash 每千次正确判断的估算成本更低。'
        else: text+='成本高低取决于 Flash 的闲时／高峰计价。'
    return text


def task_intro(result,family):
    parts=['### 持续多题并发',
        '本轮每请求 8 题，同时配置 8／32／64 个工作器；每个工作器收到完整响应后立即补入下一包。每档预热 5 秒，再统计 30 秒，重复两轮。固定 32 道原题循环施压，重放不增加独立医学样本数。',
        finding(result,family),compact_table(result,family),
        '判断／秒只计合法选项，不代表全部答对。准确率按原题等权，失败和非法选项计错；P95 包含发出前的配额排队及收到完整结果的时间。单位成本包含答错消耗，缺少用量标为待核算。配置并发包含配额排队，实际在途并发见详细结果。',
        '[持续负载协议](../SUSTAINED_THROUGHPUT.md) · [逐档实际并发、完整包率和失败](../../results/sustained-throughput-v1/README.md) · [原始响应与配置](../../results/sustained-throughput-v1/archive_manifest.json)',
        '### 历史有限批次测试',
        '以下记录把多题与并发分别测试，只处理有限的一组题，不能用作持续高吞吐证据。']
    return parts


def render(result):
    high=[m['mean_http_concurrency'] for m in result['modes'] if m['model']=='jev-1.13.0' and m['family']!='routing_200' and m['concurrency']==64 and m['full_repeats']]
    parts=['# Jev Healthcare Lab',
        '**JEV 在哪些医疗判断任务上更准、处理得更多、成本更低？** 本轮比较 JEV 1.13 与 DeepSeek V4.1 Flash 的持续批量处理表现。',
        '**每请求 8 题，多个请求同时处理，完成后立即补入下一包。** 并发依次设为 8、32、64；每档预热 5 秒后连续统计 30 秒，重复两轮。这里的吞吐是每秒收到的合法判断数量，不是首字速度。',
        f"本轮选择病例并发症、用药方案、病例诊断、中医证型四个任务，各 32 道原题；另有 200 题规则分流工程测试。共发出 {result['measured_requests']:,} 次正式负载请求，{result['full_cells']} / {len(result['config']['cells'])} 个计划窗口纳入汇总。",
        '固定题组循环施压，费用包含供应商缓存命中。本轮测量当前配额保护设置下的服务吞吐，不代表冷缓存新病例流量或模型计算上限。',
        f'**JEV 配置 64 并发时，各医疗任务实际平均在途请求仅 {min(high):.1f}–{max(high):.1f} 个。** 客户端配额保护先限制了发出速度，因此本轮没有验证 JEV 持续承载 64 个实际并发请求的能力。' if high else '本轮尚无 JEV 64 并发设置的可用记录。',
        '[医疗任务结果](#医疗任务结果) · [200-题工程压力测试](#200-题工程压力测试) · [测试边界](#测试边界) · [完整记录](results/sustained-throughput-v1/README.md)',
        '## 医疗任务结果',
        '同任务两模型使用相同原题与金标；双方有结果的档位仅比较相同轮次，额外完成的轮次见完整记录。**判断／秒越高，表示持续处理能力越强；准确率越高，表示可直接交付的正确判断比例越高；每千次正确判断成本越低，表示完成有效工作的费用越低。** 答错及无效返回均计入准确率分母。',
        'P95 表示约 95% 的已发出请求，从排队到收到完整结果所需的时间，包含客户端配额等待。配置并发是工作器数，实际在途请求可能因配额更少。“未纳入”表示触发中止条件或被跳过；即使在收尾时触发也不纳入汇总；“待核算”表示有请求缺少用量，不代表免费。纳入轮次须结合结果一起阅读。']
    for family in result['config']['families']:
        fid=family['id']
        parts.extend(['### '+family['title'],finding(result,fid),compact_table(result,fid),
                      f"[本任务数据、样例与历史测试](docs/tasks/{fid}.md#多问题与并发性能)。32 道独立原题，重复请求仅用于施加负载。"])
    parts.extend(['## 200 题工程压力测试',
        '每请求 200 道规则判断，配置 8／32 并发，持续补入请求。用于观察大批量 JSON 输出与原生多问题接口的处理表现。三块固定规则分流板循环发送，**不属于医学准确率证据**。',
        compact_table(result,'routing_200'),
        '## 测试边界',
        '- 这是两轮 30 秒的闭环持续负载测试，测得的是当前服务、网络和配额下的处理能力，不是全天稳定性、开放流量 SLA 或模型最大吞吐。实际并发、配额等待、每 5 秒吞吐与错误保留在详细结果中。',
        '- JEV 客户端按已公布的请求／输入 token 配额平滑发出请求。吞吐平台可能来自客户端配额保护，本轮没有通过突破该设置寻找服务端上限；不能把平台或连接超时解释为模型计算上限。Flash 关闭思考并输出精简 JSON，完整接收后再计分。',
        '- 医疗材料是同任务的多病例拼包，尚未验证“同一份病历一次读取、多项临床判断”的收益。验证这项能力需要另补带专家金标的多字段病历数据。',
        '- 32 道原题循环重放，可能命中供应商缓存；不能把请求次数当作新增医学样本。成本按实际 usage 和冻结价目估算，Flash 区间对应闲时／高峰，不是账单金额。',
        '- 目前仅这四项医疗任务完成了持续负载尝试。其他 22 个有题任务只有历史有限批次结果，不能据此声称已验证高并发高吞吐。公开考试或模拟题成绩也不等同于临床有效性验证。',
        '## 数据与复核',
        '[持续负载协议](docs/SUSTAINED_THROUGHPUT.md) · [逐档结果与原始响应](results/sustained-throughput-v1/README.md) · [全部任务](docs/tasks/README.md) · [数据来源](docs/datasets/README.md)',
        '[历史有限批次测试：26 任务](results/task-performance-v1/README.md) · [历史五模型测试](docs/MODEL_RESULTS.md)',
        '```bash\npython -m pip install -r requirements-throughput.txt\npython scripts/build_sustained_throughput_report.py --check\npython scripts/generate_catalog_docs.py --check\n```',
        '## 许可',
        '第三方数据保留原始许可，包括非商业研究限制；见 [第三方声明](THIRD_PARTY_NOTICES.md) 和各任务来源页。'])
    return '\n\n'.join(parts)+'\n'
