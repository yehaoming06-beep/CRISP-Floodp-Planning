"""Build final Chinese reports and source ledgers from saved audit outputs."""
from pathlib import Path
from datetime import datetime
from collections import Counter
import csv,hashlib,json,re
import pandas as pd
from reconstruct import OUT,SNAP,readcsv,csvout,dump,rain_window

def j(name):return json.loads((OUT/name).read_text())
def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(str(v).replace('|','/') for v in row)+' |' for row in rows])
def nums(values,n=6):return ' / '.join(f'{v:.{n}f}' for v in values)
def percent(values):return ' / '.join(f'{100*v:.2f}%' for v in values)
def passport(label,status='ANALYZED'):
    return f'## Material Passport\n\n- Origin Skill: academic-research-suite / experiment-agent\n- Origin Mode: validate\n- Origin Date: 2026-11-04（Asia/Shanghai）\n- Verification Status: {status}（限定范围见正文）\n- Version Label: {label}\n'
def write(name,text):(OUT/name).write_text(text.strip().replace('-0.000000','0.000000')+'\n')

def ledgers():
    retrieval=[json.loads(s) for s in (OUT/'logs/retrieval.jsonl').read_text().splitlines() if s.strip()]
    # The very first successful network probe preceded the batch collector.
    path=OUT/'sources/web/HKO_2024_table43.html'
    probe=dict(name=path.name,url='https://www.hko.gov.hk/en/publica/tc/tc2024/table43.html',path=str(path.relative_to(OUT)),http_status='200',status='COMPLETE_INITIAL_PROBE',bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),headers='logs/network_probe_headers.txt',retrieved_utc='not separately timestamped; response Date retained in headers')
    retrieval=[probe]+retrieval
    for n,r in enumerate(retrieval,1):r['attempt_record_id']=f'HTTP{n:04}'
    csvout('Official_Source_Manifest.csv',retrieval)
    pdfs=[]
    for name in ['logs/pdf_download.json','logs/pdf_download_201709_202409.json']:
        d=j(name)
        for row in d['snapshots']:pdfs.append({**row,'download_log':name})
    for m in [7,9]:
        path=OUT/f'sources/prior_fix/sources/HKO_MWS2025{m:02}.pdf'
        pdfs.append(dict(name=path.stem,url=f'https://www.hko.gov.hk/en/publica/mws/files/mws2025{m:02}.pdf',complete=True,path=str(path.relative_to(OUT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),download_log='sources/prior_fix/range_download_log.json',retrieval_scope='reused complete earlier official snapshot; not downloaded again in this run'))
    csvout('PDF_Source_Manifest.csv',pdfs)
    pages=[]
    for rec in j('sources/pdf_table_pages.json'):
        if rec['month']==10 and rec['pdf_page']==19:continue
        pages.append(dict(pdf=rec['pdf'],sha256=rec['sha256'],pdf_page=rec['pdf_page'],printed_page=rec['pdf_page']-3,image=rec['image'],status='VISUALLY_CHECKED',scope='full target page; title, Shek Pik row, W/S values and times, units/datums and table-specific notes; preceding rain-table bracket notes not transferred'))
    for period,page in [('201709',28),('202409',29)]:
        path=OUT/f'sources/pdf/HKO_MWS{period}.pdf'
        pages.append(dict(pdf=str(path.relative_to(OUT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),pdf_page=page,printed_page=26,image=f'sources/conflict_pages/HKO_MWS{period}_p{page:03}.png',status='VISUALLY_CHECKED_SOURCE_CONFLICT_RETAINED',scope='full page and target tide table; agreement with annual report does not resolve disagreement with official database'))
    csvout('PDF_Visual_Check_Ledger.csv',pages)
    originals=readcsv(SNAP/'01_Data/Events/event_metadata.csv')
    rain_choices=[]
    for old in originals:
        if '(R11)' in old['rainfall_station']:continue
        day=datetime.fromisoformat(old['event_date'])
        rain_choices.append(dict(event_id=old['event_id'],original_anchor=old['event_date'],selected_station=old['rainfall_station'],**{s+'_five_raw_cells':rain_window(day,s)['raw_values'] for s in ['R11','HKA','R12']},historical_reason='UNRECOVERED; current v1 QC compatibility is not historical evidence'))
    csvout('evidence/Original_Four_Station_Choices.csv',rain_choices)
    csvout('evidence/Observed_Original23.csv',originals)

def main():
    ledgers()
    screen=j('analysis/screening_summary.json');impact=j('analysis/scenario_impact.json');spatial=j('analysis/spatial_impact.json');verification=j('logs/Final_Verification.json');stability=j('analysis/stability_summary.json')
    fits=impact['fits'];mainfit=fits[impact['main_fit']];old=fits['original23_frozen']
    audit=pd.read_csv(OUT/'Inclusion_Exclusion_Audit.csv');compare=pd.read_csv(OUT/'Original23_vs_Reconstructed.csv');originals=pd.read_csv(SNAP/'01_Data/Events/event_metadata.csv')
    backend=j('backend_probability60/validation.json');ties=pd.read_csv(OUT/'backend_probability60/ev_policy_tie_ranges.csv').set_index('case');bc=pd.read_csv(OUT/'backend_probability60/Original555_vs_Reconstructed.csv').set_index('id')
    comparison_rows=[[name,rec['N'],nums(rec['weights']),'/'.join(map(str,rec['counts'])),percent(rec['conditional_frequencies'])] for name,rec in fits.items()]
    reps=pd.read_csv(OUT/'analysis/scenarios/reconstructed60_adjudicated/scenario_summary.csv')
    rep_table=table(['类别','H中心','R均值 mm/day','W均值 mCD','S均值 m'],[[r.scenario,f'{r.cluster_center_mu:.6f}',f'{r.representative_rainfall:.6f}',f'{r.representative_sea_level:.6f}',f'{r.representative_storm_surge:.6f}'] for r in reps.itertuples()])
    stability_rows=[]
    for rec in stability:
        a=rec['ARI_projection_to_main_p025_median_p975'];w=rec['w_R_p025_median_p975']
        stability_rows.append([rec['method'],rec['valid'],nums(w),nums(a)])
    spatial_rows=[[name,rec['N'],nums(rec['weights']),'/'.join(map(str,rec['counts'])),percent(rec['conditional_frequencies'])] for name,rec in spatial['fits'].items()]
    metrics=[]
    for label,cid in [('旧式基准','legacy_baseline'),('移动泵基准','mobile_baseline')]:
        row=bc.loc[cid]
        for metric in ['rp','ws','ev','eev','vss','evpi']:
            metrics.append([label,metric.upper(),f'{row["old_"+metric]:.6f}',f'{row["new_"+metric]:.6f}',f'{row["delta_"+metric]:+.6f}'])
    bounds=pd.read_csv(OUT/'analysis/Fixed_Class_Missingness_Bounds.csv')
    fallacies=[
        ['Simpson悖论','CAUTION','不同年份/站点混合可能改变关联；留一年和年份块敏感性已报告；未作总体方向推断'],
        ['生态谬误','CAUTION','区域雨站/测潮站不能推出单户受淹、洪深或个体避免损失'],
        ['Berkson选择偏差','CAUTION','旧23非完整抽样框；新60也条件于资料与归属可核，不能由CRITIC相关断言总体相关'],
        ['碰撞偏差','CAUTION','完整案例与可观测性可能受气象/站点条件共同影响；未以调整某变量消除该风险'],
        ['忽视基率','已控制解释','所有n_s/N写为条件相对频率；未估计年度洪灾概率或重现期'],
        ['均值回归','N/A','没有极端组前后干预效果比较；不作因果改善结论'],
        ['幸存者偏差','CAUTION','三条待核保留在63候选台账；大澳缺站不判非事件'],
        ['多重寻找效应','N/A/NOTE','未进行p值显著性筛选；保留所有披露的敏感性与不利来源冲突'],
        ['分析路径自由度','CAUTION','已看旧23；v1.0、发现冲突后的v1.1及空间补充均留版本/哈希；不是盲法预注册'],
        ['相关即因果','已限定','CRITIC是离散规划预处理；示例优化收益没有实证因果校准'],
        ['反向因果','N/A','未以横截面关联识别干预效果方向，现模型没有此因果识别设计'],
    ]
    report=f'''# 情景与后端影响评估

{passport('CI01-final-impact-v1.1','VERIFIED')}
## 结论与范围

最终主链是**63候选、60条可分析、3条待核、0条实体排除**。60条包含旧23全部身份，另加37条；Yagi数值可用但S峰值日期仍冲突。主规程为[冻结v1.0](Screening_Protocol.md)，结合[公开QC解释v1.1](Source_Conflict_Adjudication.md)执行。60条不是63候选全部已验证，也不是全部“大澳洪灾”。

原23在新锚点/雨站规程下三元输入完全不变。扩展并重拟合后，CRITIC权重(R/W/S)由{nums(old['weights'])}变为{nums(mainfit['weights'])}；三类计数由9/9/5变为35/19/6。Extreme条件相对频率由21.74%变为10.00%，相差-11.74个百分点。此变化不是长期年发生概率下降，也不代表气候趋势。

## 1. 可复现的分解比较

{table(['数据/处理','N','CRITIC R / W / S','三类计数 M/S/E','条件相对频率 M/S/E'],comparison_rows)}

original23_new_rules与冻结23的数值完全相同，故差异不来自为了改模型而调节原事件的R值。35/19/6同时受到新增身份、Min-Max范围、相关结构、权重和重新分群影响，不能只把分母从23改成60。

旧Min-Max最小值为{nums(old['minima'])}，最终为{nums(mainfit['minima'])}；旧阈值为{nums(old['thresholds'])}，最终为{nums(mainfit['thresholds'])}。K=3为保持规划离散化可比性的固定选择，未证明存在三个自然灾害类别。独立动态规划和穷举三段SSE校验与K-means结果一致；60点非空三段切分有C(59,2)=1711种。

把新60投影到旧预处理和旧阈值时，类别计数为{'/'.join(map(str,impact['main_old_projection_counts']))}；全重拟合则为35/19/6。{impact['extrapolates_below_old_min_count']}条至少一指标低于旧Min-Max下界，投影保留外推值，没有裁剪到0。两种新样本分类的ARI={impact['main_ARI_fixed_old_projection_vs_refitted']:.6f}。

旧23中{impact['original23_class_changes']}条在全重拟合后改变类别，ARI={impact['original23_ARI_old_vs_refitted']:.6f}；明细见[标签迁移](analysis/Original23_Label_Migration.csv)。这反映分类对母体和预处理的依赖，不证明原观测错误。

## 2. 最终代表值

{rep_table}

R为日累计量的五日窗口最大值；W/S为官方事件摘要极值。三个代表值是同一类内各变量分别求均值，不是实测同步过程。W、S通常不同时，官方汇总的起止时刻多数未在表内明示。Son-Tinh有两次经过，按同一气旋汇总W/S，但一个锚点五日雨窗不能覆盖两次过程，限制已保留。

## 3. 待核与来源冲突敏感性

第一次按主报告得到的61条结果保存在[第一阶段快照](stages/v1_before_secondary_tide_crosscheck/STAGE_STATUS.md)和backend_probability61，不是最终QC通过样本。该试算权重约0.486526/0.286673/0.226802，计数36/19/6。交叉核对后2017低压数值冲突待核，最终使用60条。另将Yagi的日期冲突也完全避开时，数值样本为59条，计数34/19/6；这是严格敏感性，不是实体排除。

2017低压的[年报](https://www.hko.gov.hk/en/publica/tc/tc2017/table363.html)和[月报p.28](https://www.hko.gov.hk/en/publica/mws/files/mws201709.pdf#page=28)为2.23/0.26，而官方增水数据库记录354为2.48/0.29。Yagi的[年报](https://www.hko.gov.hk/en/publica/tc/tc2024/table334.html)和[月报p.29](https://www.hko.gov.hk/en/publica/mws/files/mws202409.pdf#page=29)把S峰值记在5/9，数据库记录393记在6/9，数值均为0.57。没有推定哪个版本是真值，也未改冻结输入。原始两套字段见[交叉核对表](evidence/Tide_Database_Crosscheck.csv)。

三个未决身份使全63候选的最终Min-Max、CRITIC、阈值和频率仍不可识别。只有**固定最终60的类别定义及已知标签**时，才有以下算术缺失界：

{table(['类别','已知计数','固定类别的下界','固定类别的上界'],[[r.scenario,r.known_count,f'{r.lower:.6f}',f'{r.upper:.6f}'] for r in bounds.itertuples()])}

这些是n_s/63至(n_s+3)/63的逻辑界，不是重拟合模型区间或统计置信区间；各类上界不能同时实现。不能把共同摘要复制给2021两个低压来补足分母。

## 4. 重叠和年份敏感性

保留了候选雨窗的{screen['overlap_pairs']}对相交关系，含两个共同摘要身份的重合。重采样只使用最终可分析数据，按相交窗连通块和年份成块，另逐次留出一年。seed=20261104；每种bootstrap1000次，共2009次留出/重采样拟合；保存全部抽样索引和运行行。

{table(['方法','有效次数','w_R的2.5%/中位/97.5%','投影ARI的2.5%/中位/97.5%'],stability_rows)}

这些百分位只描述给定事件库和分块方案下的经验敏感性，不能填补候选外影响、测量误差或三条未决。只有9个年份，未宣称这些范围具有长期风险的置信覆盖率。

## 5. 大澳测潮站空间敏感性

[HKO增水数据库](https://www.hko.gov.hk/en/wservice/tsheet/pms/stormsurgedb.htm?t=STORM&v=31)还包含Tai O站。它明确采用香港标准时间；站点JSON识别Tai O=10、Shek Pik=2。该来源在主规程冻结后发现，因此以[补充规程](TaiO_Spatial_Sensitivity_Addendum.md)单独处理，不把两站混拼。2018 Bebinca的大澳记录不可得，保留PENDING_TAIO_DATA。源文件未给出足以证明大澳站仪器校准、长期基准同质性或岸上洪深的材料。

{table(['样本/站点','N','CRITIC R / W / S','M/S/E计数','条件相对频率'],spatial_rows)}

在完全相同的59个身份上，换站后{spatial['common_sample_class_changes']}条类别改变，ARI={spatial['common_sample_ARI']:.6f}。W最大站差={spatial['max_abs_W_difference_m']:.2f} m，S最大站差={spatial['max_abs_S_difference_m']:.2f} m。原23全部有可读大澳记录，换站后的计数为10/11/2。因此石壁数据不能无条件称“大澳原位观测”；大澳站海面高度也不能称“大澳洪深”。完整数值、缺测及限定见[大澳补充台账](Supplemental_TaiO_Observations.csv)。

## 6. 后端隔离重算

已执行最终60条件频率下的**全部555配置**，再在backend_probability60_replay完整重复一次，555行summary.csv逐字节相同。每次记录{backend['solver_audit_rows']}条求解审计行，均为OPTIMAL；既有可行性、全第一阶段固定的EEV、WS≥RP≥EEV等检查通过（容差1e-6）。原冻结两个基准的六指标复算误差均为0。结果见[555组逐项比较](backend_probability60/Original555_vs_Reconstructed.csv)和[验证记录](backend_probability60/validation.json)。

覆盖：旧式/移动基准2、容量42、空间26、消融8、OAT56、配对扰动400、购置容量9、现有库存5、价格5、可达性2，共555。主60与旧23的比较仅更新条件情景频率，其他情景资源、成本、效益、库存及可达性系数固定。

{table(['基准','指标','原23','新60','变化'],metrics)}

这些数值是既有示例效益分数，不能称为观测避免损失、年收益或港元总福利。移动基准旧策略在新输入下仍可行，策略价值={backend['original23_policy_reconstructed_value']:.6f}，对新RP的regret={backend['original23_policy_reconstructed_regret']:.6f}。555组中返回的准备方案字符串有{backend['plan_changes']}组变化，返回的购置数有{backend['new_pump_changes']}组变化；这不证明最优策略唯一。

已对10个基准/购置容量案例穷举1716个可行第一阶段政策并求解1808次，检查EV同值政策。新移动基准有{int(ties.loc['mobile_baseline','EV_optimal_policies'])}个EV最优政策，EEV范围{ties.loc['mobile_baseline','worst_EEV_among_EV_optima']:.6f}—{ties.loc['mobile_baseline','best_EEV_among_EV_optima']:.6f}，对应VSS为{ties.loc['mobile_baseline','minimum_VSS_over_EV_optima']:.6f}—{ties.loc['mobile_baseline','maximum_VSS_over_EV_optima']:.6f}。表中的VSS是求解器所返回EV政策的结果，不能说成唯一值。详见[EV同值政策范围](backend_probability60/ev_policy_tie_ranges.csv)。

## 7. 尚不能完成的实证传播与完整重算方案

现有load_inputs只从Scenario表读取三类频率；更新后的R/W/S均值没有通往资源需求、效益、alpha/beta或CU成本的已验证映射。代码和求解依赖足以完成555组频率敏感性，但不足以创造缺失的实证关系。**full_observation_to_decision_propagation=false**。

完整替代主结果需依次完成：

1. 取得2017低压官方更正/连续测潮及同期天文潮记录，确定2021共同过程的分析单位；解决Yagi日期。保留未解决版本，不能自动补值。
2. 确认研究目标是本地警告气旋、气旋影响过程，还是大澳洪灾；若扩大到无信号/残余环流事件，另以官方轨迹、警告与降雨资料建立可追踪的新抽样框。九年本地警告名录不自动覆盖后两种总体。
3. 明确采用大澳原位潮站还是石壁代理；收集测站基准/迁站/维护、降雨站质量、时序与地面高程资料，在独立版本拟合R/W/S、CRITIC及聚类，重做年份/过程稳健性。
4. 用可核的库存、可达性、暴露、有效流量、班组、运输/运行成本及损失关系，建立情景观测→资源/效益系数的映射和不确定性模型；资本HKD与示例CU不能混成同一实证货币口径。
5. 保存独立参数包，重算RP、各情景WS、EV、固定全部第一阶段政策的EEV、VSS/EVPI和EV同值政策范围；重新执行上述全部555配置及配对扰动，同时评估旧策略在新输入下的可行性、价值和regret。
6. 通过来源/QC、输入哈希、精确聚类、可行性和同值解审计后，才形成可供作者审阅的主结果替代稿。本次不覆盖论文或冻结主链。

## 8. 统计谬误检查（11/11）

{table(['检查','结论','适用限制/证据'],fallacies)}

## 9. 复现状态

离线重建、情景和空间分析重跑的{verification['offline_deterministic_replay']['files_compared']}个数据/证据输出逐字节相同；独立NumPy CRITIC和动态规划SSE通过。现有{verification['frozen_input_guard']['files']}个冻结文件及快照哈希均未改变。以上只证明指定文件和计算链的可重复性；CI-01历史初筛、来源冲突和实证代表性仍未全部关闭。
'''
    write('Scenario_Impact_Assessment.md',report)
    years=[]
    for y in range(2017,2026):
        g=audit[audit.year.eq(y)];o=originals[originals.event_date.str.startswith(str(y))]
        years.append([y,g.hko_warning_group_id.nunique(),len(g),len(o),int(g.model_eligible.sum()),int((~g.model_eligible).sum())])
    oldlist=table(['ID','旧台账锚点','实际事件名','实际雨站'],[[r.event_id,r.event_date,r.event_name,re.search(r'\((\w+)\)',r.rainfall_station)[1]] for r in originals.itertuples()])
    shifts=compare[(compare.comparison_type=='ORIGINAL_EVENT')&compare.anchor_shift_days.ne(0)]
    resolution=f'''# CI-01 独立历史事件筛选验证报告

{passport('CI01-resolution-v1.1','VERIFIED')}
## 结论

**CI-01：PARTIALLY RESOLVED，不能完全关闭。** 已从官方记录独立重建一个明确受限、可逐年核对的候选母体，提出并执行新规程，完成逐事件对账、情景复算与隔离后端敏感性。原作者的最初候选/排除记录、当时锚点和选站决策仍未恢复；新建规则不等于历史规则。

最终是**62组本地警告涉及63个独立气旋身份，60条可作事件R/W/S数值分析，3条待核，0条实体排除**。60条保留旧23全部事件，另加37条。Yagi在60条内，但增水峰值日期仍有限定。未决和缺测不能从台账消失，也不能作为“没有事件”的证据。

## 六项交付

{table(['文件','内容/行数'],[['[Candidate_Event_Inventory.csv](Candidate_Event_Inventory.csv)','63个候选；非由旧23反推'],['[Screening_Protocol.md](Screening_Protocol.md)','冻结的新规程v1.0；执行时结合下述QC解释v1.1'],['[Inclusion_Exclusion_Audit.csv](Inclusion_Exclusion_Audit.csv)','63行；60 INCLUDE、3 PENDING_DATA、0实体排除'],['[Original23_vs_Reconstructed.csv](Original23_vs_Reconstructed.csv)','63行完整外联对账：23原事件+40额外候选'],['[Scenario_Impact_Assessment.md](Scenario_Impact_Assessment.md)','CRITIC/分类/条件频率、大澳空间敏感性与完整后端重算边界'],['[CI01_Resolution_Report.md](CI01_Resolution_Report.md)','本报告；已完成与未关闭范围']])}

执行版本是主规程v1.0加[来源冲突QC解释v1.1](Source_Conflict_Adjudication.md)，空间补充另见[TaiO规程](TaiO_Spatial_Sensitivity_Addendum.md)。v1.1是在首轮试算后发现新的正面证据冲突时公开形成，未伪装为事前盲法注册；此前61条数据、代码和555组结果全部保留。

## 1. 当前实际使用的23条与可确认操作

读取并快照保存event_metadata.csv、model_input.csv、27个年度雨量归档、现有HKO来源恢复档、Event_Validation_Audit.md、实际fallback配置、分析代码、工作簿和结果。没有找到新的同时期历史初筛登记，也未把旧审计意见当作已验证的候选规则。

{oldlist}

{table(['操作项目','可确认事实','仍不能推定'],[['样本和输入','23个唯一非空ID；R/W/S有限；与metadata一致；23入23留','这只是既选23条的清洗，不能推出历史候选或排除数'],['降雨','旧日期±2日；日RF五日最大、当日和累计均可复算','旧锚点统一取最近接近/最高信号/登陆日的历史规则未恢复'],['站点','19 R11、3 HKA(E004/E007/E017)、1 R12(E013)','四次替代的原始优先级和触发记录未恢复'],['潮位/增水','均用Shek Pik/SPW事件摘要；23对数值复算相符；Man-yi共同驱动限定保留','不是大澳洪深、仪器校准或纯台风因果增水'],['清洗配置','missing_strategy=drop、duplicate_event_id=error、CRITIC ddof0、K3/seed42/n_init50','不证明原始初筛按同一缺测规则；本次待核候选没有交给drop静默删除'],['旧样本构成','包含官方母体中全部22个最高信号≥8的气旋，另加一号Man-yi','这是事后描述，不能认定恢复了“8号阈值+例外”的历史规则']])}

四次非R11选择的新规程兼容性见[逐站五格](evidence/Original_Four_Station_Choices.csv)。本次官方页面解释#为不完整、***为不可得，但“一天有#即整窗转下一站”仍是本次保守QC选择，未声称HKO或原作者采用过该门槛。

## 2. 独立候选母体及完整性边界

定义：2017-01-01至2025-12-31香港时间，任何时刻曾被HKO发出本地热带气旋警告信号的独立气旋。含1号、3号、8/9/10号与未命名低压。同一气旋多次经过合为同一身份，2021年共同警告下的两个低压分列身份但不复制观测。

候选从[官方本地警告数据库](https://www.hko.gov.hk/en/wxinfo/climat/warndb/warndb1.shtml)实际加载的[tc.dat](https://www.hko.gov.hk/dps/wxinfo/climat/warndb/tc.dat)构造；与2017—2024逐年Table4.3及2025年1—12月完整官方月报网页逐信号段交叉核对。九年203段完全一致。2017—2024的航运警告表、盆地清单、章节与原始索引亦保留，未把航运警告直接当本地警告。2025年度常见URL返回404，不据此漏掉全年事件；其37段信号由全年月报补齐核对。

{table(['年','本地警告组','气旋身份','旧23条数','最终数值分析','待核'],years)}

这一完整性只适用于**本地警告气旋框**。香港行政警告不证明每条均导致大澳水浸；没有本地警告的远距离气旋、残余环流或季风关联降雨，以及无气旋洪灾未形成完整母体。不能宣称已穷尽所有“大澳相关气旋影响/洪灾”。HKO对2021两个低压共用警告的说明保留在[官方报告§3.2](https://www.hko.gov.hk/en/publica/tc/tc2021/section3_2rpt.html)快照；Son-Tinh二次经过按[2018报告§3.2](https://www.hko.gov.hk/en/publica/tc/tc2018/section3_2rpt.html)确认，不把数据库No name第二次经过误加为另一气旋。

## 3. 新规程执行、对账和未决

新锚点是最高本地信号首次发出的香港日期；雨窗±2日；雨站固定R11→HKA→R12，每站五日全部未标记才可用，整窗选站，不逐日拼接或按大小选站。没有为得到23而设置风球、雨量、潮位或灾损阈值。

{table(['原ID','旧锚点','新锚点','R/W/S变化'],[[r.original_event_id,r.original_anchor,r.reconstructed_anchor,'全为0'] for r in shifts.itertuples()])}

其余18条锚点相同。全部23条的已选站和R/W/S数值均不变，未据此宣布找回历史规则。27份官方RF响应本次重新下载，与原归档**27/27逐字节相同**。最终60条雨站为54 R11、4 HKA、2 R12。

{table(['待核身份/限定','证据','处置'],[['TC2017_06 未命名低压','年报/月报W=2.23,S=0.26；官方数据库W=2.48,S=0.29','候选保留；PENDING_SOURCE_CONFLICT，不作实体排除'],['TC2021_02_E、TC2021_02_W','两个独立低压共用警告及R/W/S摘要，不能逐气旋分离','候选各一行；PENDING_COMPOUND_ATTRIBUTION，不复制为两个样本'],['TC2024_03 / E018 Yagi','W/S数值一致，S日期5Sep与6Sep冲突','允许事件极值数值分析，峰值时间UNRESOLVED；另做避开全部冲突的59条敏感性']])}

2017—2024共有48张完整官方潮表、2025有14个完整月报目标原表。8份相关完整月报PDF通过页数与SHA预检，14个2025目标页和2个冲突目标页均核看。官方增水数据库是额外官方证据，不是独立仪器复测；62个警告组中60组的W/S及两项峰值时刻相符，另有上述两组冲突。未用来源多数表决、同值或质量标记N推断仪器准确。

Man-yi、Fengshen、Fung-wong的天文潮以上水位上升均保留与东北季风共同驱动的限定。W/S各自取事件极值，不要求同时，S不由W减去另一时刻天文潮峰值，更不是地面洪深。

## 4. 对分析及优化的影响

完整结果在[影响评估](Scenario_Impact_Assessment.md)。旧23重建后输入不变；扩展到最终60条后权重为{nums(mainfit['weights'])}，计数35/19/6，条件频率58.33%/31.67%/10.00%。旧23中的6条标签因全重拟合而变化。大澳与石壁同一59身份比较，有10条标签变化，说明站点空间选择也是实质影响源。

已完成最终60频率下的555组既有配置及一次完整重复，555行摘要逐字节一致；另完成10案例EV同值政策穷举。只更新条件频率，其他示例资源/效益系数固定。没有已验证的R/W/S→资源/效益映射，因此未宣称完成实证全链不确定性传播。未决全63候选的最终类别与频率仍不可识别，不能用60条结果冒充全母体最终模型。

## 5. CI-01处理判定

{table(['事项','判定','关闭范围/剩余条件'],[['现有23条实际输入及可见操作','VERIFIED_LOCAL','数值/窗口/站点构成可复现；非原始初筛证明'],['限定本地警告候选框','RECONSTRUCTED_COMPLETE_WITHIN_DEFINED_FRAME','九年203段双清单核对；63身份含共同警告的两组件'],['更广义大澳相关气旋/洪灾母体','UNRESOLVED','无本地信号、残余环流与复合影响范围未闭合'],['本次新规程与逐候选判定','EXECUTED_WITH_PENDING_ITEMS','60数值分析、3待核、Yagi峰值日期限定；0实体排除'],['原始历史筛选、锚点、四次选站决策','OPEN','仍需作者同时期候选/排除台账、规则版本及决策记录；新规程不代替'],['官方数值/日期冲突和共同摘要归属','OPEN','需官方更正或可比连续实测/天文潮，及明确分析单位'],['条件情景与后端计算复现','VERIFIED_CONDITIONAL','555组概率敏感性完整执行并重复；效益/成本实证映射与长期风险模型未完成'],['CI-01总体','PARTIALLY RESOLVED / NOT FULLY CLOSED','有可复现的独立重建，不能认证原23初筛无偏或历史程序']])}

## 6. 保留与复现

所有写入限定在本独立目录。已保存原始输入快照、官方响应（包括404/失败历史）、URL、HTTP头、UTC下载时间或明确时间未知标记、文件SHA、分段下载记录、PDF预检/原页图像、逐站五格、抽样索引及全部求解日志。{verification['frozen_input_guard']['files']}个冻结文件和对应快照复核未变，原Event_Validation_Audit.md与论文未覆盖。

离线重建/情景/空间的{verification['offline_deterministic_replay']['files_compared']}个输出逐字节重现；NumPy CRITIC和独立动态规划SSE核验通过。详见[最终验证JSON](logs/Final_Verification.json)、[官方下载台账](Official_Source_Manifest.csv)、[PDF原件台账](PDF_Source_Manifest.csv)和[复现说明](README.md)。完整性和计算通过不等于观测无误、筛选无偏或CI-01完全关闭。
'''
    write('CI01_Resolution_Report.md',resolution)
    readme='''# CI-01 独立重建：交付与复现

最终入口为[CI01_Resolution_Report.md](CI01_Resolution_Report.md)。最终状态PARTIALLY RESOLVED，63气旋身份/62警告组，60数值案例、3待核、0实体排除。Screening_Protocol.md是应用前冻结的v1.0，执行时与Source_Conflict_Adjudication.md v1.1结合；原主文不追改。TaiO_Spatial_Sensitivity_Addendum.md是发现新站点资料后的公开补充，非历史规则。

## 当前与历史阶段

- 根目录三张事件CSV：最终63候选及60/3判定；Original23_vs_Reconstructed含原23和40额外候选。
- analysis/scenario_impact.json：最终主链索引，main_fit=reconstructed60_adjudicated；当前主输入analysis/reconstructed_model_input.csv。
- analysis/scenarios/reconstructed60_adjudicated：最终60条CRITIC、聚类及代表值。
- analysis/spatial_impact.json：同一59身份的石壁/大澳比较及原23换大澳的敏感性。
- backend_probability60：最终60条件频率的555配置、3888求解审计行；另有10案例EV同值政策审计。
- backend_probability60_replay：最终555配置完整重复，summary.csv与上项逐字节一致。
- stages/v1_before_secondary_tide_crosscheck：QC新证据出现前的61条输入、分析和代码。backend_probability61为该阶段555组试算；其中manifest指向的通用概率文件后来被最终60更新，**当时实际61频率原件在stage的analysis/backend_probability_update.json、backend_probability61/inputs.json及每个solution参数中保留，哈希可对账**。不要把该目录视为最终QC通过样本。
- analysis/scenarios中名字含reconstructed61_main、warning_group62_unit_sensitivity、omit_explicit_joint_rise_sensitivity的目录是保留的首阶段输出；当前主索引不引用它们。
- snapshots：原始主数据、配置、模型、代码和结果；logs/frozen_inputs_manifest.json记录975文件的原位置/快照/SHA。
- sources/web、sources/pdf、sources/ranges、sources/prior_fix：完整官方响应、PDF、原始字节段和以前完整归档；404响应留存但不作缺失事件证据。原始响应内可能存在无关网页导航文字，只按明确证据范围使用。

## 离线重现

在项目根目录使用已有.venv，或安装snapshots目录中的requirements-lock.txt对应依赖。实际版本另见logs/exact_environment_versions.json。不会联网的主复算命令：

```sh
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/reconstruct.py
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/assess_scenarios.py
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/verify_tides_and_spatial.py
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/verify_delivery.py
```

上述命令只重写本审计目录的派生表和日志，使用已保存的原始来源，不改冻结主项目。verify_delivery会再运行三步、逐字节比较派生输出、独立检查CRITIC/SSE、冻结输入、PDF完整性和已保存的两次555结果。报告重建：

```sh
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/write_reports.py
```

如需自己重新求解完整555组，用一个尚不存在的目录名，已有结果不会被覆盖：

```sh
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/run_backend.py --run-name backend_probability60_reproduction_02
.venv/bin/python manuscript_revision/audit/ci01_independent_20261104/code/audit_backend_ev_ties.py --run-name backend_probability60_reproduction_02
```

求解需可用Gurobi许可证；本次许可证和代码实际可用。当前runner加载最终analysis/backend_probability_update.json，只更改条件频率，保留情景系数；其余555设计与快照相同。复制到其他机器时，保护原工作区的哈希核验需要原目录结构；仅在独立包中运行时，应将冻结清单核验指向对应原件或明确标记原件不可访问，不能当成已通过。

## 下载与PDF检查

collect_sources.py和logs/jobs_*.json保存下载任务，网络重取可能得到新版本，必须保留新旧快照及差异，不能与本次离线复现混为一谈。collect_pdfs.py使用核验Content-Range/长度/Last-Modified的分段下载；pdf_download*.json记录完整性。2025年7/9月重用此前完整官方快照，沿用其原下载记录和SHA，没有虚构本次重下载。

extract_pdf_evidence.py使用已保存PDF，生成文本和目标页图像。code/vendor保留ARS的pdf_read_preflight.py及其audit_snapshot.py依赖，来源为本机academic-research-suite/ars/scripts，供页树三重页数预检。PDF_Visual_Check_Ledger.csv只表示已核看的16个目标页，不是全文技术审读或仪器校准。

logs中的attempt01、crosscheck_before_adjudication等失败/中止记录刻意保留。初次解析遇到研究期外历史2400时刻，已通过先过滤研究期修复；来源冲突触发过暂停，之后公开登记v1.1并重新执行。verify_delivery的初次导入错误已修正；这些不是被隐藏的成功运行。

## 解释限制

任何n_s/N均为给定筛选、QC和可得性下的条件相对频率。不是年发生概率、洪深、同步水文事件或现场干预效果。未决候选、官方正面冲突、无警告影响总体及历史筛选证据均保留。未向外部应用上传、发布或修改论文。
'''
    write('README.md',readme)
    readme_path=OUT/'README.md'
    readme_path.write_text(readme_path.read_text().replace('975文件',str(verification['frozen_input_guard']['files'])+'文件'))
    print('Wrote final impact/resolution reports, README, source and visual ledgers')

if __name__=='__main__':main()
