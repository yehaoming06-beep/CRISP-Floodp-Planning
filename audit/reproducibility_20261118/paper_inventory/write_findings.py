from pathlib import Path
import csv,json,hashlib
OUT=Path(__file__).resolve().parent;R=OUT.parents[2]
x=json.loads((OUT/'manuscript_extract.json').read_text());ps={p['paragraph']:p['text'] for p in x['paragraphs']}
checks=[
('conditional_method_validation',[9,14,33,197,210,212,215],'PASS_TEXT_SCOPE','摘要、研究问题、方法、讨论与结论均限定为条件性方法验证；未发现将其表述为实地政策效果验证的自有研究断言。'),
('uncalibrated_cost_resource_benefit',[33,51,56,130,133,134,135,209],'PASS_TEXT_SCOPE','成本/资源/收益、可调用库存、通行、泵性能和经济换算均明确未校准。泵的约百万HKD购置参考仅有文献支持，不等于所有成本校准。'),
('frequency_only_sensitivity',[16,51,99,138,191,193,206,213],'PASS_TEXT_SCOPE','60事件前端重新拟合；后端只替换条件频率，沿用原假设响应表。正文承认完整观测至决策的不确定性传播未完成。'),
('three_pending_unresolved',[9,14,117,118,181,204,208,213,215],'PASS_TEXT_SCOPE','63身份=60可分析+3pending；2017数值冲突与2021双气旋归属未解决；Yagi日期冲突另行保留。'),
('scores_not_losses_or_population',[9,14,51,56,59,76,104,111,168,193,201,209,213],'PASS_TEXT_SCOPE','模型分数不是实际经济损失、受保护居民或等同服务量；CU与HKD不合并，人口仅提供地理背景。')]
result=[]
for key,ids,status,assessment in checks:
 result.append({'check':key,'status':status,'assessment_zh':assessment,'paragraphs':[{'paragraph':i,'text':ps[i]} for i in ids]})
(OUT/'claim_boundaries.json').write_text(json.dumps({'document_sha256':x['sha256'],'locator':'direct-body paragraph index, including empty paragraphs; not pages','limits':'Text-scope audit only; numerical reproduction and empirical validity require independent evidence.','checks':result},ensure_ascii=False,indent=2))
links=list(csv.DictReader((OUT/'supplement_local_links.csv').open()))
sections=list(csv.DictReader((OUT/'supplement_sections.csv').open()))
maps={
'S1':('范围/证据版本及冻结设计','03_Experiments/Experiment_Protocol.json;03_Experiments/Optimization/code/experiment_design.py;manuscript_revision/peer_review_validation_20261105_v2/assessment/Scenario_Chain_Audit.json','条件频率替换边界；此处不以旧PASS代替重算'),
'S2':('EV A/B和完整基线策略枚举','01_Data/CRISP_Master_Data.xlsx;02_Model/crisp_parameters.py;02_Model/crisp_model.py;manuscript_revision/peer_review_validation_20261105_v2/code/run_validation.py;manuscript_revision/peer_review_validation_20261105_v2/code/verify_independent.py','表S1–S4；8个EV规格/416固定策略历史记录存在'),
'S3':('受控组件/可达性/整数性','manuscript_revision/peer_review_validation_20261105_v2/code/run_validation.py;manuscript_revision/peer_review_validation_20261105_v2/runs/primary/component_summary.csv;manuscript_revision/peer_review_validation_20261105_v2/runs/primary/shared_inventory_feasible_set_witness.json','表S5–S7；24规格；6.5百万HKD为假想检验'),
'S4':('假想地理覆盖规则','manuscript_revision/peer_review_validation_20261105_v2/runs/primary/coverage_summary.csv;manuscript_revision/peer_review_validation_20261105_v2/runs/primary/coverage_deployment.csv;manuscript_revision/peer_review_validation_20261105_v2/code/run_validation.py','表S8–S9；只报告RP，WS/EV/EEV/VSS未计算'),
'S5':('空间网格及交叉情景','03_Experiments/Optimization/code/experiment_design.py;04_Results/Optimization/summary.csv;manuscript_revision/figures/Figure_3_Spatial.png','图S1；25网格+1交叉规格'),
'S6':('措施子集和逐因素敏感性','03_Experiments/Optimization/code/experiment_design.py;04_Results/Optimization/ablation_contributions.csv;04_Results/Optimization/summary.csv','图S2–S3；8子集与56 OAT规格'),
'S7':('联合假想扰动','03_Experiments/Optimization/code/experiment_design.py;04_Results/Optimization/uncertainty_intervals.csv;04_Results/Optimization/summary.csv','表S10/图S4；PCG64 seed20261103，200配对=400规格'),
'S8':('旧上界修正/容量网格','03_Experiments/Optimization/code/experiment_design.py;04_Results/Optimization/legacy_correction_comparison.csv;04_Results/Optimization/summary.csv','表S11/图S5；两组21规格'),
'S9':('采购和EV策略范围','03_Experiments/Optimization/code/audit_ev_ties.py;04_Results/Optimization/ev_policy_tie_ranges.csv;manuscript_revision/audit/ci01_independent_20261104/code/audit_backend_ev_ties.py;manuscript_revision/audit/ci01_independent_20261104/backend_probability60/ev_policy_tie_ranges.csv','表S12–S13；10 case范围审计不代表555全部最优策略枚举'),
'S10':('原23事件向量及源登记','01_Data/Events/model_input.csv;01_Data/Events/event_metadata.csv;01_Data/Sources/source_registry.json;manuscript_revision/audit/ci01_independent_20261104/Official_Source_Manifest.csv','表S14；与背景source_registry的S01等来源编号不是同一编号体系'),
'S11':('示例性场景响应系数','01_Data/CRISP_Master_Data.xlsx;01_Data/Evidence/current_parameters.json;02_Model/crisp_parameters.py;04_Results/Optimization/baseline_inputs.json','表S15；不是现场测得的成本/资源/效益系数'),
'S12':('重建警告框架/候选流','manuscript_revision/audit/ci01_independent_20261104/Candidate_Event_Inventory.csv;manuscript_revision/audit/ci01_independent_20261104/Inclusion_Exclusion_Audit.csv;manuscript_revision/audit/ci01_independent_20261104/analysis/reconstructed_model_input.csv;manuscript_revision/audit/ci01_independent_20261104/code/reconstruct.py','表S16；final60与superseded61分开，3pending未补全'),
'S13':('验证边界与剩余证据','manuscript_revision/peer_review_validation_20261105_v2/code/verify_independent.py;manuscript_revision/peer_review_validation_20261105_v2/independent_validation/verification.json;manuscript_revision/Remaining_Research_Risks.md','历史500/936运行记录不是本次运行证明；校准和历史筛选证据仍开放')}
rows=[]
for section in sections:
 s=section['section'];topic,paths,note=maps[s]
 rr=[R/p for p in paths.split(';')]
 rows.append({**section,'topic_zh':topic,'principal_files':paths,'all_principal_files_present':all(p.is_file() for p in rr),'explicit_local_links_in_source':sum(l['document'].startswith('manuscript_revision') and l['section']==s for l in links),'explicit_local_links_all_present':all(l['exists']=='True' for l in links if l['section']==s),'assessment_zh':note,'execution_status_this_subtask':'NOT_RUN_FILE_AND_TEXT_AUDIT_ONLY'})
with (OUT/'supplement_evidence_map.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
missing=[
 {'item':'原23事件同时期候选/排除清单','status':'UNRECOVERED_ORIGINAL_EVIDENCE','specified_filename':None,'basis':'两目录文件盘点未定位；Final Paper P124/P208与Remaining_Research_Risks R01明确未恢复；现有2026 retrospective Screening_Protocol不是原始登记。','impact':'不阻止以冻结23向量计算；阻止证明原历史样本完整性/无偏性'},
 {'item':'原23事件历史anchor规则版本','status':'UNRECOVERED_ORIGINAL_EVIDENCE','specified_filename':None,'basis':'现有metadata提供日期但无同时期规则；新规则使五anchor变动而向量不变不能倒推原规则。','impact':'不阻止冻结向量复算；来源选择可重复性未闭合'},
 {'item':'四个非R11站选择的同时期说明','status':'UNRECOVERED_ORIGINAL_EVIDENCE','specified_filename':None,'basis':'Original_Four_Station_Choices.csv四行historical_reason均为UNRECOVERED；回溯QC相容不是原始原因。','impact':'不阻止冻结23复算；不能认证历史选择原因'},
 {'item':'实地成本/资源/效益响应校准数据和关系','status':'NOT_SUPPLIED_EMPIRICAL_EVIDENCE','specified_filename':None,'basis':'有01_Data/Sources/Calibration背景文献和参数审计，但parameter_families.json标为待校准；P209明确无经验映射。','impact':'不阻止示例模型复算；阻止实际损失/人口/操作政策收益结论'},
 {'item':'完整63身份可归属无冲突的R/W/S输入','status':'UNRESOLVED_OBSERVATIONS_NOT_MISSING_ARCHIVES','specified_filename':None,'basis':'TC2017_06官方数值矛盾；TC2021_02_E/W共享不可拆分摘要，model_eligible=False；原始档案存在。','impact':'不能生成完整63模型；不得把三条补成现有频率分布'},
 {'item':'Node导出工具package.json/lock','status':'NOT_FOUND_IN_ACCESSIBLE_WORKSPACES','specified_filename':'package.json / package-lock.json / pnpm-lock.yaml / yarn.lock','basis':'已枚举全部27,543原始工作区文件；无这些名称；存在.mjs导出代码。','impact':'精确重装样式化Excel导出依赖未闭合，不属于核心数值输入缺失'}]
(OUT/'missing_evidence.json').write_text(json.dumps(missing,ensure_ascii=False,indent=2))
