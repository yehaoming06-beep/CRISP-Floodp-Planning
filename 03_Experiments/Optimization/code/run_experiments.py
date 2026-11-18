"""Rerun legacy capacity grid and all priority experiments with explicit mobile stock."""
from pathlib import Path
from dataclasses import replace
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse,csv,hashlib,importlib.util,json,sys,time,platform,shutil

HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
MODEL=ROOT/'02_Model'
sys.path.insert(0,str(MODEL))
from crisp_parameters import load_inputs,_parameters_to_json
from crisp_model import Runner,PumpFleet

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec)
    sys.modules[name]=m;spec.loader.exec_module(m);return m
import experiment_design as design
from crisp_model import load_case_settings

def dump(path,x):path.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def table(path,rows):
    if not rows:return
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run-id',default='replication');ap.add_argument('--output',type=Path);args=ap.parse_args()
    if Path(args.run_id).name!=args.run_id:raise ValueError('Single directory name required')
    out=args.output.resolve() if args.output else ROOT/'04_Results/Reproductions'/args.run_id;out.mkdir(parents=True,exist_ok=False)
    settings=load_case_settings(ROOT/'01_Data/CRISP_Master_Data.xlsx',ROOT/'03_Experiments/Experiment_Protocol.json')
    source_paths=[ROOT/'01_Data/CRISP_Master_Data.xlsx',MODEL/'crisp_parameters.py',MODEL/'crisp_model.py',
        Path(__file__),Path(__file__).with_name('experiment_design.py'),ROOT/'03_Experiments/Experiment_Protocol.json']
    source_hashes={str(p.relative_to(ROOT)):sha(p) for p in source_paths}
    dump(out/'manifest_start.json',{'started':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
        'python':sys.version,'platform':platform.platform(),'source_sha256':source_hashes,'settings':settings})
    dump(out/'experiment_settings.json',settings)
    p=load_inputs(ROOT/'01_Data/CRISP_Master_Data.xlsx')
    assert p.upper_bound==p.with_recomputed_bounds().upper_bound
    dump(out/'baseline_inputs.json',_parameters_to_json(p))
    fleet=PumpFleet(**{**settings['primary_case'],'accessible_locations':tuple(settings['primary_case']['accessible_locations'])})
    runner=Runner(out);payloads=[];start=time.monotonic()
    def evaluate(q,c,fleet_arg=fleet,policy=None,allowed=None):
        if time.monotonic()-start>settings['hard_timeout_seconds']:raise TimeoutError('Experiment hard timeout')
        r=runner.evaluate(q,c,policy,fleet_arg,allowed);payloads.append(r);return r
    try:
        legacy=evaluate(p,{'id':'legacy_baseline','experiment':'legacy_baseline'},None)
        assert abs(legacy['summary']['rp']-686.0078260869565)<1e-6
        primary=evaluate(p,{'id':'mobile_baseline','experiment':'baseline'})
        policy=Runner.policy(primary['rp']);legacy_policy=Runner.policy(legacy['rp'])
        for factor,levels in [('Setup Budget',design.SETUP_LEVELS),*((k,design.RESOURCE_LEVELS) for k in design.RESOURCE_FIELDS)]:
            for level in levels:
                q=design.scaled_parameters(p,factor,level)
                c={'id':f'legacy_{factor.replace(" ","_")}_{level:.2f}','experiment':'legacy_capacity','factor':factor,'level':level}
                evaluate(q,c,None,legacy_policy)
                evaluate(q,{**c,'id':c['id'].replace('legacy_','mobile_',1),'experiment':'mobile_capacity'},fleet,policy)
        print('Legacy and mobile capacity grids complete',flush=True)
        for q,c in design.spatial(p):evaluate(q,c,policy=policy)
        for mask in range(8):
            allowed=[i for k,i in enumerate(p.interventions) if mask&2**k]
            evaluate(p,{'id':f'ablation_{mask}','experiment':'ablation','allowed':allowed},policy=policy,allowed=allowed)
        for f,factor in enumerate(design.FACTORS):
            for k,level in enumerate((.8,.9,1.1,1.2)):
                evaluate(design.oat(p,factor,level),{'id':f'oat_{f:02}_{k}','experiment':'oat','factor':factor,'level':level,
                    'u_mode':'fixed_old' if factor=='deploy_cost_fixed_U' else 'availability' if factor=='availability_U' else 'derived'},policy=policy)
        print('Spatial, ablation and one-at-a-time cases complete',flush=True)
        for q,c in design.joint(p,n=settings['joint_draws']):
            evaluate(q,c,policy=policy)
            if c['u_mode']=='availability' and (c['draw']+1)%25==0:print(f'Paired draws {c["draw"]+1}/200',flush=True)
        for n in settings['fleet_capacity_grid_new_purchase_limits']:
            f=replace(fleet,capital_budget_hkd=n*fleet.purchase_price_hkd)
            evaluate(p,{'id':f'fleet_{n:02}','experiment':'fleet','factor':'new_purchase_limit','level':n},f,policy)
        for n in settings['existing_stock_grid']:
            f=replace(fleet,existing_stock=n,capital_budget_hkd=0)
            evaluate(p,{'id':f'existing_{n:02}','experiment':'existing_stock','factor':'existing_stock','level':n},f,policy)
        for mult in settings['purchase_price_multipliers']:
            f=replace(fleet,purchase_price_hkd=fleet.purchase_price_hkd*mult)
            evaluate(p,{'id':f'price_{mult:.2f}','experiment':'purchase_price','factor':'purchase_price_multiplier','level':mult},f,policy)
        for name,locations in [('mainland_only',(p.locations[1],)),('no_access',())]:
            evaluate(p,{'id':f'access_{name}','experiment':'access','factor':'accessible_locations','level':name},replace(fleet,accessible_locations=locations),policy)
        table(out/'summary.csv',[r['summary'] for r in payloads]);table(out/'solver_audit.csv',runner.audit)
        old_rows=json.loads((ROOT/'01_Data/Controls/capacity_bound_reference.json').read_text())
        comparison=[]
        for oldrow in old_rows:
            row=next(r['summary'] for r in payloads if r['summary']['experiment']=='legacy_capacity' and r['summary']['factor']==oldrow['factor'] and r['summary']['level']==oldrow['level'])
            comparison.append({'factor':oldrow['factor'],'level':oldrow['level'],
                **{f'old_{m}':oldrow[f'frozen_{m}'] for m in ['rp','ws','ev','eev','vss','evpi']},
                **{f'corrected_{m}':row[m] for m in ['rp','ws','ev','eev','vss','evpi']},
                'max_metric_change':max(abs(row[m]-oldrow[f'frozen_{m}']) for m in ['rp','ws','ev','eev','vss','evpi'])})
            assert all(abs(row[m]-oldrow[f'derived_{m}'])<1e-6 for m in ['rp','ws','ev','eev','vss','evpi'])
        table(out/'legacy_correction_comparison.csv',comparison)
        assert len(payloads)==555,len(payloads)
        assert source_hashes=={str(path.relative_to(ROOT)):sha(path) for path in source_paths}
        result={'status':'COMPLETED','configurations':len(payloads),'solver_runs':len(runner.audit),
            'all_optimal':all(r['status']=='OPTIMAL' for r in runner.audit),'all_feasibility_and_information_value_checks_passed':True,
            'capacity_points_affected_by_U_fix':sum(r['max_metric_change']>1e-6 for r in comparison),
            'baseline_legacy':legacy['summary'],'baseline_mobile':primary['summary'],
            'all_first_stage_variables_fixed_in_EEV':True,'input_code_hashes_stable_during_execution':True,
            'elapsed_seconds':time.monotonic()-start,'empirical_validation':False}
        dump(out/'validation.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)
    finally:runner.close()

if __name__=='__main__':main()
