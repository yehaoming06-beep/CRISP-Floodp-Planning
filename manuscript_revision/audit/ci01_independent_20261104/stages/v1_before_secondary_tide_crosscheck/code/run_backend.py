"""Full 555-case probability-only sensitivity, using immutable code snapshots.

The reconstructed scenario coefficients cannot be empirically recalibrated from
R/W/S with the available model. This runner explicitly holds them fixed.
"""
from pathlib import Path
from dataclasses import replace
from datetime import datetime, timezone
import hashlib,json,platform,sys,time
import numpy as np
import pandas as pd
from reconstruct import OUT,SNAP,dump,csvout

sys.path[:0]=[str(SNAP/'02_Model'),str(SNAP/'03_Experiments/Optimization/code')]
from crisp_parameters import load_inputs,_parameters_to_json
from crisp_model import Runner,PumpFleet,load_case_settings
import experiment_design as design

def main():
    out=OUT/'backend_probability61';out.mkdir(exist_ok=False)
    started=time.monotonic()
    update=json.loads((OUT/'analysis/backend_probability_update.json').read_text())
    settings=load_case_settings(SNAP/'01_Data/CRISP_Master_Data.xlsx',SNAP/'03_Experiments/Experiment_Protocol.json')
    old=load_inputs(SNAP/'01_Data/CRISP_Master_Data.xlsx')
    p=replace(old,probabilities=update['probabilities'])
    assert old.upper_bound==p.with_recomputed_bounds().upper_bound
    source_paths=[SNAP/'01_Data/CRISP_Master_Data.xlsx',SNAP/'02_Model/crisp_parameters.py',SNAP/'02_Model/crisp_model.py',SNAP/'03_Experiments/Optimization/code/experiment_design.py',SNAP/'03_Experiments/Experiment_Protocol.json',OUT/'analysis/backend_probability_update.json']
    hashes={str(path.relative_to(OUT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths}
    manifest=dict(started_utc=datetime.now(timezone.utc).isoformat(),scope='All existing 555 configurations; only baseline conditional scenario frequencies updated. Scenario coefficients and empirical calibration held fixed.',update=update,settings=settings,python=sys.version,platform=platform.platform(),source_sha256=hashes)
    dump('backend_probability61/manifest_start.json',manifest)
    dump('backend_probability61/inputs.json',_parameters_to_json(p))
    fleet=PumpFleet(**{**settings['primary_case'],'accessible_locations':tuple(settings['primary_case']['accessible_locations'])})
    runner=Runner(out);payloads=[]
    def evaluate(q,c,fleet_arg=fleet,policy=None,allowed=None):
        if time.monotonic()-started>settings['hard_timeout_seconds']:raise TimeoutError('1800s experiment hard timeout')
        value=runner.evaluate(q,c,policy,fleet_arg,allowed);payloads.append(value);return value
    try:
        # Verify frozen baselines through the same current solver before changing p.
        old_mobile=runner.evaluate(old,{'id':'old23_verification_mobile','experiment':'verification'},fleet=fleet)
        old_legacy=runner.evaluate(old,{'id':'old23_verification_legacy','experiment':'verification'})
        reference=pd.read_csv(SNAP/'04_Results/Optimization/summary.csv').set_index('id')
        old_diffs={}
        for rec,target in [(old_mobile,'mobile_baseline'),(old_legacy,'legacy_baseline')]:
            diffs={k:rec['summary'][k]-float(reference.loc[target,k]) for k in ['rp','ws','ev','eev','vss','evpi']}
            assert max(abs(v) for v in diffs.values())<1e-6,diffs;old_diffs[target]=diffs
        legacy=evaluate(p,{'id':'legacy_baseline','experiment':'legacy_baseline'},None)
        primary=evaluate(p,{'id':'mobile_baseline','experiment':'baseline'})
        policy=Runner.policy(primary['rp']);legacy_policy=Runner.policy(legacy['rp'])
        original_policy=Runner.policy(old_mobile['rp'])
        old_policy_new=runner.solve(p,'original23_policy_under_new61',fleet=fleet,fixed=original_policy)
        dump('backend_probability61/original23_policy_under_new61.json',old_policy_new)
        for factor,levels in [('Setup Budget',design.SETUP_LEVELS),*((k,design.RESOURCE_LEVELS) for k in design.RESOURCE_FIELDS)]:
            for level in levels:
                q=design.scaled_parameters(p,factor,level)
                c={'id':f'legacy_{factor.replace(" ","_")}_{level:.2f}','experiment':'legacy_capacity','factor':factor,'level':level}
                evaluate(q,c,None,legacy_policy)
                evaluate(q,{**c,'id':c['id'].replace('legacy_','mobile_',1),'experiment':'mobile_capacity'},fleet,policy)
        print('555-case run: baseline and capacity cases complete',flush=True)
        for q,c in design.spatial(p):evaluate(q,c,policy=policy)
        for mask in range(8):
            allowed=[i for k,i in enumerate(p.interventions) if mask&2**k]
            evaluate(p,{'id':f'ablation_{mask}','experiment':'ablation','allowed':allowed},policy=policy,allowed=allowed)
        for f,factor in enumerate(design.FACTORS):
            for k,level in enumerate((.8,.9,1.1,1.2)):
                evaluate(design.oat(p,factor,level),{'id':f'oat_{f:02}_{k}','experiment':'oat','factor':factor,'level':level,'u_mode':'fixed_old' if factor=='deploy_cost_fixed_U' else 'availability' if factor=='availability_U' else 'derived'},policy=policy)
        print('555-case run: spatial, ablation, OAT cases complete',flush=True)
        for q,c in design.joint(p,n=settings['joint_draws']):
            evaluate(q,c,policy=policy)
            if c['u_mode']=='availability' and (c['draw']+1)%25==0:print(f'555-case run: paired draws {c["draw"]+1}/200',flush=True)
        for n in settings['fleet_capacity_grid_new_purchase_limits']:
            f=replace(fleet,capital_budget_hkd=n*fleet.purchase_price_hkd)
            evaluate(p,{'id':f'fleet_{n:02}','experiment':'fleet','factor':'new_purchase_limit','level':n},f,policy)
        for n in settings['existing_stock_grid']:
            evaluate(p,{'id':f'existing_{n:02}','experiment':'existing_stock','factor':'existing_stock','level':n},replace(fleet,existing_stock=n,capital_budget_hkd=0),policy)
        for mult in settings['purchase_price_multipliers']:
            evaluate(p,{'id':f'price_{mult:.2f}','experiment':'purchase_price','factor':'purchase_price_multiplier','level':mult},replace(fleet,purchase_price_hkd=fleet.purchase_price_hkd*mult),policy)
        for name,locations in [('mainland_only',(p.locations[1],)),('no_access',())]:
            evaluate(p,{'id':f'access_{name}','experiment':'access','factor':'accessible_locations','level':name},replace(fleet,accessible_locations=locations),policy)
        assert len(payloads)==555
        summary=[r['summary'] for r in payloads];csvout('backend_probability61/summary.csv',summary);csvout('backend_probability61/solver_audit.csv',runner.audit)
        comparisons=[]
        for row in summary:
            before=reference.loc[row['id']]
            comparisons.append(dict(id=row['id'],experiment=row['experiment'],old_plan=before['plan'],new_plan=row['plan'],old_new_pumps=float(before['new_pumps']),new_new_pumps=row['new_pumps'],**{f'old_{k}':float(before[k]) for k in ['rp','ws','ev','eev','vss','evpi']},**{f'new_{k}':row[k] for k in ['rp','ws','ev','eev','vss','evpi']},**{f'delta_{k}':row[k]-float(before[k]) for k in ['rp','ws','ev','eev','vss','evpi']}))
        csvout('backend_probability61/Original555_vs_Probability61.csv',comparisons)
        assert hashes=={str(path.relative_to(OUT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths}
        joint=[r for r in summary if r['experiment']=='joint']
        validation=dict(status='COMPLETED',configurations=555,verification_configurations=2,solver_audit_rows=len(runner.audit),all_recorded_solver_statuses_optimal=all(r['status']=='OPTIMAL' for r in runner.audit),all_existing_feasibility_and_information_value_checks_passed=all(r['checks_passed'] for r in summary),frozen_baseline_max_errors=old_diffs,baseline_legacy=legacy['summary'],baseline_mobile=primary['summary'],original23_policy_new61_feasible=old_policy_new['feasible'],original23_policy_new61_value=old_policy_new['objective'],original23_policy_new61_regret=primary['summary']['rp']-old_policy_new['objective'] if old_policy_new['feasible'] else None,plan_changes=sum(r['old_plan']!=r['new_plan'] for r in comparisons),new_pump_changes=sum(r['old_new_pumps']!=r['new_new_pumps'] for r in comparisons),max_abs_RP_change=max(abs(r['delta_rp']) for r in comparisons),paired_joint_cases=len(joint),elapsed_seconds=time.monotonic()-started,input_code_hashes_stable=True,empirical_recalibration=False,full_observation_to_decision_propagation=False,remaining='No evidence-based mapping from revised scenario representative R/W/S to costs, capacities and benefits; pending two individual attributions; no annual probability model.')
        dump('backend_probability61/validation.json',validation)
        print(json.dumps(validation,ensure_ascii=False,indent=2),flush=True)
    finally:runner.close()

if __name__=='__main__':main()
