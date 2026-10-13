"""Standalone accuracy, cost, and throughput figures for individual healthcare tasks."""
from textwrap import wrap
import math

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


def _place_labels(fig, ax, points):
    """Try label orders and nearby positions to keep four callouts readable."""
    from itertools import permutations
    from matplotlib.transforms import Bbox

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bounds = ax.get_window_extent(renderer).padded(-4)
    candidates = []
    bubble_boxes = []
    for point in points:
        px, py = ax.transData.transform(point['xy'])
        radius = point['size'] ** .5 / 2 * fig.dpi / 72
        bubble_boxes.append(Bbox.from_bounds(px-radius, py-radius, radius*2, radius*2))
    for point, bubble in zip(points, bubble_boxes):
        probe = fig.text(0, 0, point['label'], fontsize=9, linespacing=1.4)
        extent = probe.get_window_extent(renderer)
        width, height = extent.width, extent.height
        probe.remove()
        px, py = ax.transData.transform(point['xy'])
        gap = max(12, bubble.width/2 + 7)
        options = []
        for dx, dy in [(gap, gap), (gap, -gap), (-gap, gap), (-gap, -gap),
                       (0, gap), (0, -gap), (gap, 0), (-gap, 0),
                       (0, gap+35), (0, -gap-35), (gap, gap+35),
                       (gap, -gap-35), (-gap, gap+35), (-gap, -gap-35)]:
            ha = 'left' if dx > 0 else 'right' if dx < 0 else 'center'
            va = 'bottom' if dy > 0 else 'top' if dy < 0 else 'center'
            x = px+dx-(0 if ha == 'left' else width if ha == 'right' else width/2)
            y = py+dy-(0 if va == 'bottom' else height if va == 'top' else height/2)
            box = Bbox.from_bounds(x, y, width, height)
            if not bounds.contains(x, y) or not bounds.contains(x+width, y+height):
                continue
            bubble_overlap = sum(_overlap(box.padded(3), b) for b in bubble_boxes)
            options.append((dx, dy, ha, va, box, (dx*dx+dy*dy)**.5 + bubble_overlap*100))
        if not options:
            raise ValueError('No in-bounds label position for ' + point['label'])
        candidates.append(options)
    best = None
    for order in permutations(range(len(points))):
        chosen = {}; score = 0
        for index in order:
            def cost(option):
                return option[5] + sum(_overlap(option[4].padded(4), other[4]) * 1000 for other in chosen.values())
            selected = min(candidates[index], key=cost)
            score += cost(selected)
            chosen[index] = selected
        if best is None or score < best[0]:
            best = score, chosen
    for index, point in enumerate(points):
        dx, dy, ha, va, _, _ = best[1][index]
        ax.annotate(point['label'], point['xy'], xytext=(dx*72/fig.dpi, dy*72/fig.dpi),
                    textcoords='offset points', ha=ha, va=va, fontsize=9, linespacing=1.4,
                    color=point['color'], zorder=4,
                    arrowprops={'arrowstyle': '-', 'color': point['color'], 'alpha': .4, 'lw': .7},
                    bbox={'boxstyle': 'round,pad=0.18', 'fc': 'white', 'ec': 'none', 'alpha': .90})


def _overlap(a, b):
    return max(0, min(a.x1, b.x1)-max(a.x0, b.x0)) * max(0, min(a.y1, b.y1)-max(a.y0, b.y0))


def figure(report, fid, colors, *, english=False):
    import matplotlib.pyplot as plt
    from medical_load_english import TASK_TITLES

    family = report['families'][fid]
    fig = plt.figure(figsize=(11, 6), facecolor='white')
    ax = fig.add_axes([.085, .21, .88, .57])
    title = TASK_TITLES[fid] if english else TITLES[fid]
    if english:
        title = title.replace('TCM', 'Traditional Chinese medicine')
        title = '\n'.join(wrap(title, width=73))
    fig.text(.085, .965, title, fontsize=16, va='top', color='#17212b')
    if english:
        scope = (f"Accuracy & cost: {family['decisions']} decisions · Throughput: {family['load_decisions']} repeated decisions at concurrency 32")
    else:
        scope = (f"准确率与成本：{family['decisions']} 项判断 · 吞吐：{family['load_decisions']} 项循环负载，32 并发")
    if family['small_sample']:
        scope += ' · Exploratory' if english else ' · 探索性结果'
    fig.text(.085, .845, scope, fontsize=10, color='#475467')
    points = []
    max_cost = 0
    for model in report['config']['models']:
        result = family['models'][model]
        quality, load = result['quality'], result['load']['32']
        costs, accuracy, throughput = quality['cost_cny_per_1000'], quality['accuracy'], load['throughput']
        if costs is None or accuracy is None or throughput is None:
            continue
        x, y = sum(costs)/2, accuracy*100
        max_cost = max(max_cost, costs[1])
        size = max(12, throughput*4)
        ax.plot(costs, [y,y], color=colors[model], linewidth=2, alpha=.6, zorder=1)
        ax.scatter([x], [y], s=size, color=colors[model], alpha=.70,
                   edgecolor='white', linewidth=1.1, zorder=3)
        price = f'{costs[0]:.3f}' if costs[0] == costs[1] else f'{costs[0]:.3f}–{costs[1]:.3f}'
        rate = f'{throughput:.2f}/s' if english else f'{throughput:.2f}项/秒'
        points.append({'xy': (x,y), 'size': size, 'color': colors[model],
                       'label': f"{report['models'][model]['label']}\n{y:.2f}% · ¥{price} · {rate}"})
    xmax = max(max_cost, .01)
    accuracies = [point['xy'][1] for point in points] or [0, 100]
    ymin = max(-5, math.floor((min(accuracies)-15)/10)*10)
    ymax = min(112, math.ceil((max(accuracies)+15)/10)*10)
    ax.set(xlim=(-xmax*.035, xmax*1.08), ylim=(ymin, ymax))
    ax.set_yticks([value for value in range(0, 101, 10) if ymin <= value <= ymax])
    ax.set_xlabel('Cost (CNY / 1,000 decisions) ↓' if english else '成本（元 / 千项判断）↓', fontsize=11, labelpad=7)
    ax.set_ylabel('Accuracy (%) ↑' if english else '准确率（%）↑', fontsize=11, labelpad=7)
    ax.tick_params(labelsize=10)
    ax.grid(alpha=.14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if points:
        _place_labels(fig, ax, points)
    notes = [
        'Bubble area = valid decisions/s (tiny values use a minimum dot); Flash line = price range; its bubble is at the midpoint.',
        'Throughput counts valid outputs, not correct answers. Account and network limits apply; these are not model capacity limits.',
    ] if english else [
        '气泡面积表示吞吐量（低值保留最小可见点）；Flash 横线为价格区间，气泡位于区间中点。',
        '吞吐计格式有效输出，不等于正确答案数；受账户与网络限制，不代表模型性能上限。',
    ]
    for y, note in zip((.08, .045), notes):
        fig.text(.085, y, note, fontsize=9, color='#475467')
    fig.text(.965, .010, 'JEV Healthcare Lab', ha='right', fontsize=8, color='#667085',
             url=f'https://github.com/JuneYaooo/jev-healthcare-lab/blob/main/docs/tasks/{fid}.md')
    return fig
