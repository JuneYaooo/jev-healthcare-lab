"""Standalone throughput figures for individual healthcare tasks."""
from textwrap import wrap

TITLES = {
    'triage_urgency': '患者分诊与就医紧急程度判断',
    'message_urgency_pair': '患者消息的处理优先级判断',
    'examination_choice': '患者下一步检查方案选择',
    'clinical_grade': '疾病分期与病情严重程度判断',
    'diagnosis': '根据病例选择诊断',
    'tcm_syndrome': '中医病例的证型判断',
    'case_etiology': '根据病例判断病因',
    'tcm_pathogenesis_candidate': '中医病例的候选病机判断',
    'patient_contraindication': '患者治疗方案的禁忌判断',
    'treatment_choice': '患者治疗方案选择',
    'medication_choice': '患者用药方案选择',
    'fluid_plan': '患者补液方案选择',
    'pgx_guideline_recommendation': '根据药物基因结果选择指南建议',
    'administration_route_choice': '药物给药途径与实施方法选择',
    'case_complication': '根据病例判断并发症',
    'nursing_priority': '患者护理措施选择',
    'nutrition_plan': '患者营养与饮食方案选择',
    'positioning_choice': '护理与医疗操作中的患者体位选择',
    'monitoring_target': '病情监测与治疗效果判断',
    'infection_precaution': '患者感染防控措施选择',
    'followup_plan': '患者复查项目与随访时间选择',
    'rehabilitation_choice': '患者康复训练方案选择',
    'prevention_choice': '患者疾病预防措施选择',
    'patient_counseling': '患者健康教育与沟通方式选择',
    'trial_referral': '患者临床试验初筛与转介判断',
    'trial_shared_patient': '同一患者的多项临床试验转介筛选',
    'consent_action': '医疗知情同意与患者隐私处置',
}


def figure(report, fid, colors, *, english=False):
    import matplotlib.pyplot as plt
    from medical_load_english import TASK_TITLES

    family = report['families'][fid]
    fig = plt.figure(figsize=(11.5, 8), facecolor='white')
    ax = fig.add_axes([.095, .365, .55, .355])
    title = TASK_TITLES[fid] if english else TITLES[fid]
    if english:
        title = title.replace('TCM', 'Traditional Chinese medicine')
        title = '\n'.join(wrap(title, width=62))
    fig.text(.065, .963, title, fontsize=18, weight='bold', va='top', color='#17212b')
    fig.text(.065, .856,
             'JEV and comparison models: throughput at concurrency 8 and 32' if english else
             'JEV 与对照模型：8 与 32 并发下的判断吞吐量',
             fontsize=13, color='#364152', va='top')
    if english:
        scope = f"Task set: {family['decisions']} unique decisions · Repeated load subset: {family['load_decisions']} decisions"
        setup = f"Up to {family['batch']} decisions per request · Two sustained-load rounds per concurrency setting"
    else:
        scope = f"任务题集 {family['decisions']} 项判断 · 循环负载子集 {family['load_decisions']} 项判断"
        setup = f"每请求上限 {family['batch']} 项判断 · 每个并发档持续测试两轮"
    fig.text(.065, .803, scope, fontsize=10.5, color='#475467')
    fig.text(.065, .770, setup, fontsize=10.5, color='#475467')

    fig.text(.705, .714, 'Throughput (decisions/s)' if english else '吞吐数值（项/秒）',
             fontsize=11, weight='bold', color='#17212b')
    for x, c in ((.705, '8'), (.86, '32')):
        fig.text(x, .684, f'Concurrency {c}' if english else f'{c} 并发',
                 fontsize=9, color='#667085')
    styles = [('o', '-'), ('s', '--'), ('^', '-.'), ('D', ':')]
    for mi, model in enumerate(report['config']['models']):
        result = family['models'][model]
        xs, ys, lo, hi = [], [], [], []
        for c in ('8', '32'):
            v = result['load'][c]
            if v['throughput'] is None:
                continue
            xs.append(int(c)); ys.append(v['throughput'])
            lo.append(max(0, v['throughput'] - v['throughput_range'][0]))
            hi.append(max(0, v['throughput_range'][1] - v['throughput']))
        marker, linestyle = styles[mi % len(styles)]
        label = report['models'][model]['label']
        if xs:
            ax.errorbar(xs, ys, yerr=[lo, hi], marker=marker, linestyle=linestyle,
                        markersize=6, capsize=4, linewidth=1.8, color=colors[model], label=label)
        y = .634 - mi * .072
        fig.text(.705, y, label, fontsize=10, weight='bold', color=colors[model])
        for x, c in ((.705, '8'), (.86, '32')):
            value = result['load'][c]['throughput']
            fig.text(x, y-.027, '—' if value is None else f'{value:.2f}', fontsize=11, color='#17212b')
    ax.set(xticks=[8, 32], xlim=(5, 35), ylim=(0, None))
    ax.set_xlabel('Concurrent request limit' if english else '同时请求数上限（并发）', fontsize=10, labelpad=10)
    ax.set_ylabel('Valid decisions / second ↑' if english else '有效判断吞吐（项/秒）↑', fontsize=10, labelpad=10)
    ax.tick_params(labelsize=10)
    ax.grid(axis='y', alpha=.16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    notes = [
        'Metric: valid-format decisions received per second; this is not the number of correct decisions per second.',
        'Points pool two rounds; vertical bars show the range between rounds, not confidence intervals.',
        'Test account quotas, rate limits, network conditions, and caching affect results; these are not model capacity limits.',
        'Repeated requests do not add unique samples. This chart measures throughput, not clinical reliability.',
    ] if english else [
        '指标：每秒收到的格式有效判断数，不等于每秒正确判断数；数值越高表示处理吞吐越高。',
        '读图：数据点为两轮合并吞吐；竖线为两轮观测范围，不是置信区间。',
        '条件：账户额度、请求限流、网络与缓存都会影响结果，不代表模型的性能上限。',
        '样本：固定题组反复请求不增加独立题量；本图衡量处理吞吐，不验证临床可靠性。',
    ]
    if family['small_sample']:
        notes[3] = ('Limited sample coverage: exploratory results only. Repeated requests do not add unique samples.' if english else
                    '样本覆盖有限，仅作探索性比较；重复请求不增加独立题量，不能据此推断临床可靠性。')
    if fid == 'trial_shared_patient':
        notes[3] = ('Eight simulated patients, eight trials each; each request shares one patient’s context. Exploratory results.' if english else
                    '8 位模拟患者各对应 8 项试验，每个请求共享一份患者材料；样本有限，仅作探索性比较。')
    if any(family['models'][m]['load'][c]['throughput'] is None for m in report['config']['models'] for c in ('8','32')):
        notes.append('— = no complete measurement; missing points are omitted.' if english else '— 表示未获得完整测量结果，相应数据点不绘制。')
    for i, note in enumerate(notes):
        fig.text(.065, .235-i*.032, note, fontsize=9, color='#475467')
    fig.text(.065, .047, f"JEV Healthcare Lab · github.com/JuneYaooo/jev-healthcare-lab · Task: {fid}",
             fontsize=8.5, color='#667085', url=f'https://github.com/JuneYaooo/jev-healthcare-lab/blob/main/docs/tasks/{fid}.md')
    return fig
