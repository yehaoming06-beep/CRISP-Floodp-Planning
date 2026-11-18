"""HiGHS independent RP verification of fresh frequency-only 555 sweep.
Original independent verifier's matrix builder/constraint checker are reused.
Historical metrics are compared only after solving, never used as solver inputs.
"""
from pathlib import Path
import sys,csv,json,importlib.util,time,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
path=ROOT/'03_Experiments/Optimization/code/verify_results.py'
spec=importlib.util.spec_from_file_location('independent_matrix_checker',path);checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
start=time.monotonic();deltas=[];rows=[]
reference={r['id']:r for r in csv.DictReader((ROOT/'manuscript_revision/audit/ci01_independent_20261104/backend_probability60/summary.csv').open(encoding='utf-8-sig'))}
for f in sorted((OUT/'reconstructed60_555/solutions').glob('*.json')):
    raw=json.loads(f.read_text())
    if raw['config']['id'].startswith('old23_verification_'):continue
    p=checker.unpack(raw['parameters']);fleet=raw['fleet'];allowed=set(raw['config'].get('allowed',p['life_score']))
    for key in ['rp','eev','fixed_baseline']:checker.check_solution(p,fleet,raw[key],allowed)
    checker.check_solution(checker.expected(p),fleet,raw['ev'],allowed)
    assert raw['eev']['y']==raw['ev']['y'] and raw['eev']['new_pumps']==raw['ev']['new_pumps']
    for s,sol in raw['ws'].items():
        q=dict(p);q['probabilities']={s:1.0}
        for key in ['deploy_cost','labour','equipment','supply','benefit','upper_bound']:q[key]={k:v for k,v in p[key].items() if k[0]==s}
        checker.check_solution(q,fleet,sol,allowed)
    value=checker.highs(p,fleet,allowed);delta=abs(value-raw['summary']['rp']);assert delta<1e-5
    metric_diff=max(abs(raw['summary'][k]-float(reference[raw['summary']['id']][k])) for k in ['rp','ws','ev','eev','vss','evpi','new_pumps','setup_used'])
    assert metric_diff<1e-9 and raw['summary']['plan']==reference[raw['summary']['id']]['plan']
    rows.append({'id':raw['summary']['id'],'independent_highs_rp':value,'fresh_gurobi_rp':raw['summary']['rp'],'rp_abs_difference':delta,'max_historical_metric_difference':metric_diff,'plan_matches':True,'status':'PASS'})
    deltas.append(delta)
    if len(rows)%100==0:print('Verified',len(rows),'/555',flush=True)
assert len(rows)==555,len(rows)
manifest=json.loads((OUT/'reconstructed60_555/manifest_start.json').read_text())
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in manifest['source_sha256'].items())
with (OUT/'reconstructed60_555/independent_verification_rows.csv').open('w',newline='') as stream:
    w=csv.DictWriter(stream,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
result={'status':'PASS','independent_solver':'HiGHS through scipy.optimize.milp','independent_RP_optima_verified':len(rows),'max_objective_difference':max(deltas),'all_saved_models_feasibility_and_objectives_reconstructed':True,'EEV_readiness_and_procurement_fixed':True,'repeated_run_configurations_matched':len(rows),'current_source_hashes_match':True,'independent_verifier_source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'elapsed_seconds':time.monotonic()-start}
(OUT/'reconstructed60_555/independent_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
