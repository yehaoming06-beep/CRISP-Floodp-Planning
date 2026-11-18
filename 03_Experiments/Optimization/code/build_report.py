"""Create user-facing analysis and plotting/workbook data from completed runs."""
from pathlib import Path
import collections,csv,difflib,itertools,json,math,sys
import numpy as np
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
RUN=ROOT/'04_Results/Optimization';OUT=RUN
def read(p):return json.loads(p.read_text())
def csvrows(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def writecsv(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def fmt(v):return f'{0 if abs(v)<1e-6 else v:,.6f}'

def main():
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'figures').mkdir(exist_ok=True)
    payloads=[read(p) for p in sorted((RUN/'solutions').glob('*.json'))]
    byid={r['summary']['id']:r for r in payloads};rows=[r['summary'] for r in payloads]
    validation=read(RUN/'validation.json');independent=read(RUN/'independent_verification.json');ties=csvrows(RUN/'ev_policy_tie_ranges.csv')
    for row in ties:
        for k in list(row):
            if k not in ['case','best_EEV_plan']:row[k]=float(row[k])
    corrected=csvrows(RUN/'legacy_correction_comparison.csv')
    for r in corrected:
        for k in r:
            if k!='factor':r[k]=float(r[k])
    production_crosscheck=json.loads((ROOT/'01_Data/Controls/pre_cleanup_report_verification.json').read_text())
    assert production_crosscheck['legacy_production_grid_matched']==21
    uncertain=[];frequencies=[]
    for mode in ['derived','availability']:
        subset=[r for r in rows if r['experiment']=='joint' and r['u_mode']==mode];assert len(subset)==200
        for k in ['rp','vss','evpi','regret','new_pumps']:
            a=np.array([r[k] for r in subset if r[k] is not None]);lo,med,hi=np.quantile(a,[.025,.5,.975])
            uncertain.append({'u_mode':mode,'metric':k,'n':len(a),'p2.5':float(lo),'median':float(med),'p97.5':float(hi),'minimum':float(a.min()),'maximum':float(a.max())})
        frequencies.extend({'u_mode':mode,'plan':k[0],'new_pumps':k[1],'count':v,'frequency':v/len(subset)}
            for k,v in collections.Counter((r['plan'],r['new_pumps']) for r in subset).most_common())
    writecsv(RUN/'uncertainty_intervals.csv',uncertain);writecsv(RUN/'plan_frequencies.csv',frequencies)
    abl={frozenset(r['config']['allowed']):r['summary']['rp'] for r in payloads if r['summary']['experiment']=='ablation'}
    shapley=[];I=['Drainage','Barrier','Warning']
    for i in I:
        v=0
        for subset,value in abl.items():
            if i not in subset:
                assert abl[subset|{i}]>=value-1e-6
                v+=math.factorial(len(subset))*math.factorial(2-len(subset))/6*(abl[subset|{i}]-value)
        shapley.append({'intervention':i,'shapley_score':v,'leave_one_out_loss':abl[frozenset(I)]-abl[frozenset(I)-{i}]})
    assert abs(sum(x['shapley_score'] for x in shapley)-abl[frozenset(I)])<1e-6
    writecsv(RUN/'ablation_contributions.csv',shapley)
    primary=byid['mobile_baseline'];legacy=byid['legacy_baseline'];deployment=[]
    for name in ['rp','ev','eev']:
        sol=primary[name];y={(r['location'],r['intervention']):r['y'] for r in sol['y']}
        deployment.extend({'model':name.upper(),**r,'prepared':y[r['location'],r['intervention']]} for r in sol['x'])
    writecsv(RUN/'baseline_deployment.csv',deployment)
    data={'summary':rows,'primary':primary,'legacy':legacy,'corrected':corrected,'ties':ties,
        'fleet':sorted([r for r in rows if r['experiment']=='fleet'],key=lambda x:x['level']),
        'uncertainty':uncertain,'frequencies':frequencies,'shapley':shapley,'deployment':deployment,
        'spatial':[r['config']|r['summary'] for r in payloads if r['summary']['experiment']=='spatial'],
        'oat':[r for r in rows if r['experiment']=='oat'],'settings':read(RUN/'experiment_settings.json'),
        'validation':validation,'independent':independent,'tie_verification':read(RUN/'ev_tie_verification.json')}
    (RUN/'report_data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    a=legacy['summary'];b=primary['summary'];tie=next(r for r in ties if r['case']=='mobile_baseline')
    report=['## Material Passport','', '- Origin Skill: academic-research-suite / experiment-agent',
        '- Origin Mode: run and computational validation','- Origin Date: 2026-11-04',
        '- Verification Status: VERIFIED (computational only; not field validation)','- Version Label: mobile_inventory_v2','',
        '# 模型修改与实验重跑结果','',
        '已完成移动泵共享库存模型、资源上界修复和完整重跑。正式结果目录为 `04_Results/Optimization`。共555个配置、3,875次主求解，全部最优；完整重复运行得到相同主指标及第一阶段选择。另以HiGHS独立复核全部555个RP目标，最大绝对差'+f"{independent['max_objective_difference']:.3g}分。原23事件和原CU系数保留；当前参数表合并了移动泵与普查信息，旧版本已归档。",'',
        '## 修改内容与单位','',
        '第一阶段新增整数购泵变量n，并满足单价×n≤港元采购预算。每个互斥情景内，两区同时部署泵数合计不超过已有库存+n。两区共用设备只计一次，不同情景可以重复使用同一库存。场地不可达时，该区抽水部署为0。未建模一个情景内部的多时段转运。',
        '原二元y保留为地点措施准备状态。原Drainage准备费用在这一过渡版本中解释为假设的地点准备费用；它不是泵采购价。运行费用、其他资源及效益仍使用原抽象CU/分数。一次抽水部署量按“一台同时分配的泵”解释，是单位建模假设；原系数尚未通过现场数据证明适用于单台设备。采购港元预算与CU预算分别约束，未假定兑换比例。',
        'EEV现在同时固定平均情景得到的y和n，避免在事件发生后重新采购设备而高估平均情景策略。主目标最大化原期望效益分数；并列时依次最小化购泵数、准备费用和二元选择编码。该顺序是公开的计算规则，不能解释为生命周期净收益最优。',
        '资源敏感性分析中，U重新按当前运行预算、人员、设备及物资容量与单位消耗的最小比值向下取整。U是推导出的链接上界，额外设备库存单独建约束。保留的“固定旧U”和“额外可用容量”实验是显式对照，不是默认修复结果。','',
        '## 基准假设与实际结果','',
        '为了比较库存约束，基准设已有库存0、采购预算200万港元、单价约100万港元，故最多可购2台，并暂假定两区都可到达。只有单价有官方设备报道支持；库存0、预算200万和两区可达是实验条件，尚不是大澳现场测量。',
        '| 模型 | RP | WS | EEV | VSS | EVPI |','|---|---:|---:|---:|---:|---:|',
        '| 原抽象模型 | '+' | '.join(fmt(a[k]) for k in ['rp','ws','eev','vss','evpi'])+' |',
        '| 加入库存的基准条件 | '+' | '.join(fmt(b[k]) for k in ['rp','ws','eev','vss','evpi'])+' |','',
        '指标单位均为模型效益分数，不能解释为避免损失的港元金额。新约束改变了可行集合，两行差值不表示新方法提高或降低了真实防灾效果。',
        f"在基准假设下，RP选择{b['plan']}，购泵{b['new_pumps']}台。平均情景EV选择{primary['ev']['plan']}并购泵{primary['ev']['new_pumps']}台；把这项完整准备/采购决策固定后，EEV为{fmt(b['eev'])}。新RP的三种情景部署（Barrier/Warning）依次为6/4、3/5、1/5个假设包，均在Tai O1。",'',
        '## 并列EV解检查','',
        f"对10个基准及库存条件，枚举了{data['tie_verification']['policies_enumerated']}项可行第一阶段策略，检查其中所有EV最优策略的EEV。库存2台的基准有{int(tie['EV_optimal_policies'])}项EV最优策略，VSS均为{fmt(b['vss'])}，因此该基准的正VSS不是当前择优规则造成的。该结论仍以假设系数为条件。",
        '较大采购上限下，EV可对未在平均情景使用的备用泵保持无差异。上限3、4、6、8、12和20台的VSS下界均为0；报告中这些点的正VSS必须附带“最少采购”等并列选择规则，不能声称所有EV最优策略都较差。范围是对最优策略集合的枚举，不是统计置信区间。','',
        '## 库存敏感性','',
        '| 最多可购泵数 | RP实际购泵 | RP | 所选EV策略的EEV | VSS |','|---:|---:|---:|---:|---:|']
    report.extend('| '+ ' | '.join([str(r['level']),str(r['new_pumps']),fmt(r['rp']),fmt(r['eev']),fmt(r['vss'])])+' |' for r in data['fleet'])
    report.extend(['','在测试网格中，最多可购3台时，RP转为抽水加预警；最多可购6台及以上时，RP实际购6台并达到原抽象模型的RP值。这是给定CU/效益假设、预算和可达性下的模型阈值，不能作为大澳应采购6台设备的建议。仅本土侧可达或两区都不可达的压力条件下，抽水方案未被基准RP选择。','',
        '## 旧资源敏感性结果的修正','',
        '旧21点网格中有5点的至少一个主要指标发生变化，6个准备预算点不受U修复影响。独立的旧版Step 5–7入口也已重跑21点，与本版无库存对照一致。','',
        '| 参数 | 倍数 | 旧RP | 修正RP | 旧EVPI | 修正EVPI |','|---|---:|---:|---:|---:|---:|'])
    report.extend('| '+' | '.join([r['factor'],str(r['level']),fmt(r['old_rp']),fmt(r['corrected_rp']),fmt(r['old_evpi']),fmt(r['corrected_evpi'])])+' |' for r in corrected if r['max_metric_change']>1e-6)
    report.extend(['','## 其他重跑实验','',
        '重跑了26个空间配置、8个干预子集、56个单因素条件和200组配对联合扰动（两种U规则共400个配置），沿用上一轮扰动幅度及随机种子20261103。另增加两种模型各21个资源/预算配置，以及采购上限、已有库存、价格和可达性条件。',
        '联合扰动的分位数描述假设参数网格中的结果变化，不是抽样置信区间。200组分别重新优化，不等于得到一项统一稳健策略。固定基准策略在准备费用变化后可能不再满足预算，此时后悔值留空，而不以0替代。干预消融和Shapley值是模型贡献分解，不是现实因果效应。','',
        '| U规则 | 指标 | 2.5%分位 | 中位数 | 97.5%分位 |','|---|---|---:|---:|---:|'])
    report.extend('| '+' | '.join([r['u_mode'],r['metric'],fmt(r['p2.5']),fmt(r['median']),fmt(r['p97.5'])])+' |' for r in uncertain if r['metric'] in ['rp','vss','evpi'])
    report.extend(['','## 校准与投稿边界','',
        '825与2,853人的2021普查记录作为研究区人口背景，未进入原地点效益系数；额定最高800立方米/小时和8小时加油间隔没有转换成效益分数或洪水时长。有效抽水流量、燃油、班组、运输、实际库存、设备通达性、响应时窗和避免损失关系仍缺实测依据。',
        '本轮完成了可运行的库存结构修正与计算复核。英文稿应把结果定位为部分现实数据支持的方法验证案例。若要声称大澳实证政策优化，仍需补齐运行和减损数据、统一全部经济口径，再校准及重跑。情景聚类的数据与算法未因本次优化模型修改而改变，先前聚类稳定性分析继续保留。','',
        '## 复现与文件','',
        '结果快照见随附Excel；完整参数、RP/WS/EV/EEV/固定基准解和日志保存在04_Results/Optimization。独立核验记录为independent_verification.json，EV并列解记录为ev_policy_tie_ranges.csv。当前工作目录只保留有效版本；历史文件及修改前状态在目录外的完整备份中。模型与实验入口均已更新到当前目录。',
        '设备单价来源：[香港政府2025年8月12日报道](https://www.news.gov.hk/chi/2025/08/20250812/20250812_155549_205.html)，原始存档在前一轮参数证据包。本轮未进行外部模型审稿或实地性能验证。'])
    (OUT/'模型修改与重跑报告.md').write_text('\n'.join(report))
    english=f'''# Mobile-pump inventory extension and computational results

## Model extension

Let n be the nonnegative integer number of newly procured pumps, N0 the available pre-existing stock, Ccap the procurement price in HKD per pump, and Kcap a separate capital envelope. The first-stage procurement constraint is Ccap n ≤ Kcap. For each mutually exclusive scenario s, the shared-stock constraint is Σ_z x[s,z,Drainage] ≤ N0 + n. Each Drainage deployment unit is assumed to represent one simultaneous pump assignment. Original binary readiness decisions and resource constraints remain; a site-inaccessible pump deployment is fixed to zero. Within-event sequential transfers are not modelled.

The earlier readiness and operation coefficients remain illustrative CU inputs. The Drainage readiness amount is interpreted as a hypothetical local preparation expense, distinct from pump acquisition. Original benefit scores are not calibrated per-pump hydraulic or avoided-loss effects. HKD and CU budgets are constrained separately, with no exchange factor. EEV fixes both readiness and procurement from the EV solution. After maximizing expected benefit, the numerical tie rules minimize pump purchases, then readiness expenditure, then the readiness encoding. Capital expenditure is constrained, not deducted from the benefit-score objective; this is not a lifecycle net-benefit model.

Linking bounds are recalculated as the floor of the minimum current capacity-to-unit-requirement ratio across operation, labour, equipment and supply constraints. Explicit stock limits are separate from these resource-derived bounds. The EV comparison retains the previous probability-weighted-coefficient convention, including weighted linking bounds.

## Conditional computational instance

The reference experiment assumes N0=0, Kcap=HK$2 million, an approximate 2025 purchase reference Ccap=HK$1 million, and access to both sectors. N0, the capital envelope and access are design assumptions rather than observations of Tai O operations. The procurement price comes from the government equipment report of 12 August 2025: https://www.news.gov.hk/chi/2025/08/20250812/20250812_155549_205.html. Reported maximum discharge and refuelling intervals are not treated as effective flow, response duration or intervention benefit.

Under these conditions, RP={fmt(b['rp'])}, WS={fmt(b['ws'])}, and EEV={fmt(b['eev'])}, yielding VSS={fmt(b['vss'])} and EVPI={fmt(b['evpi'])} in model-score units. RP prepares Barrier and Warning in Tai O1 and purchases no pumps. EV prepares Drainage and Warning in Tai O1 and purchases two pumps. Enumerating all EV-optimal first-stage policies for this reference condition gives the same EEV, so its positive VSS is invariant to the EV tie choice. At several larger procurement limits, the VSS range includes zero because additional reserve pumps can be EV-indifferent; the selected-policy VSS there depends on the stated minimum-procurement rule.

The inventory sweep reaches the unconstrained reference RP score with six purchased pumps when at least six may be procured. This is a threshold of the hypothetical instance, not an empirical recommendation to purchase six pumps. The census counts of 825 and 2,853 residents are contextual and do not calibrate exposure or the original location modifiers.

## Verification and limitations

The revised experiment contains 555 configurations and 3,875 main Gurobi solves. All main solves were optimal and passed numerical feasibility, objective reconstruction and WS≥RP≥EEV checks. A complete deterministic repeat matched all primary metrics and first-stage choices. Independent matrix formulations solved with HiGHS matched all 555 RP optima within {independent['max_objective_difference']:.3g} score units. The corrected legacy 21-point grid was also rerun using the existing Step 5–7 implementation; five points differ from the frozen-bound results. These checks establish computational consistency, not field validity. Parameter stress-test quantiles are not confidence intervals, ablation contributions are not causal effects, and separately optimized perturbations do not define a common robust policy.
'''
    (ROOT/'06_Manuscript/Sections/Model_and_Results_EN.md').write_text(english)
    plan='''# Figure plan

| ID | Data and content | Source | Fixed conditions |
|---|---|---|---|
| 01 | Procurement limit: RP/WS/EEV and EV-policy VSS range | report_data.json fleet/ties | N0=0; HKD1m/pump; baseline CU/score assumptions |
| 02 | Spatial heterogeneity heatmap | report_data.json spatial | Capital HKD2m; beta/cost factors hypothetical |
| 03 | Eight intervention subsets | report_data.json summary | Same conditional inventory model |
| 04 | One-at-a-time endpoint effects | report_data.json oat | Four levels per factor; endpoints 0.8/1.2 |
| 05 | Paired joint perturbation distributions | report_data.json summary | 200 draws/mode, fixed seed; not confidence intervals |
| 06 | Frozen vs recomputed resource upper bounds | report_data.json corrected | Legacy model; 5 levels/resource |

Figures use vector PDF plus PNG previews. Captions are in latex_includes.tex. No external or cross-model figure review is claimed.
'''
    (OUT/'FIGURE_PLAN.md').write_text(plan)
    (RUN/'report_verification.json').write_text(json.dumps({'status':'PASS','legacy_production_grid_matched':21,'ablation_monotonicity_and_Shapley_sum':True,'joint_draws_per_mode':200,'all_555_records_in_report_data':len(rows)},indent=2))
    print('Report, English methods/results insert and workbook/figure data saved')

if __name__=='__main__':main()
