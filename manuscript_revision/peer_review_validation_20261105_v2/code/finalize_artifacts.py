"""Derived comparison tables, set witness and model parser check; no optimization."""
import csv, hashlib, importlib.metadata, json, sys
from pathlib import Path
import gurobipy as gp

BASE=Path(__file__).resolve().parents[1]; RUN=BASE/'runs/primary'
def read(name): return list(csv.DictReader((RUN/name).open(encoding='utf-8-sig')))
def dump(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def table(name,rows):
    with (RUN/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

trials=read('ev_all_policy_trials.csv'); rows=[]
for freq in ('23','60'):
    for model in ('legacy','mobile'):
        a={(z['mask'],z['n']):float(z['ev']) for z in trials if z['frequency']==freq and z['model']==model and z['convention']=='A'}
        b={(z['mask'],z['n']):float(z['ev']) for z in trials if z['frequency']==freq and z['model']==model and z['convention']=='B'}
        ds={k:b[k]-v for k,v in a.items()}; witness=max(ds,key=ds.get)
        rows.append({'frequency':freq,'model':model,'paired_policy_count':len(a),
                     'policies_with_changed_ev_value':sum(abs(x)>1e-6 for x in ds.values()),
                     'minimum_EV_B_minus_A':min(ds.values()),'maximum_EV_B_minus_A':max(ds.values()),
                     'max_difference_mask':witness[0],'max_difference_n':witness[1]})
table('ev_fixed_policy_convention_comparison.csv',rows)

deployment=[]
for freq in (23,60):
    for k in (0,1,2):
        z=json.loads((RUN/'solutions'/f'f{freq}_coverage_{k}.json').read_text())
        for s in ('Moderate','Severe','Extreme'):
            for j in ('Tai O1','Tai O2'):
                xs={x['intervention']:x['x'] for x in z['x'] if x['scenario']==s and x['location']==j}
                deployment.append({'frequency':freq,'minimum_k':k,'scenario':s,'location':j,
                    'Drainage':xs['Drainage'],'Barrier':xs['Barrier'],'Warning':xs['Warning'],'total_packages':sum(xs.values())})
table('coverage_deployment.csv',deployment)
dump(BASE/'environment_versions.json',{'python':sys.version,'packages':{k:importlib.metadata.version(k) for k in ('gurobipy','numpy','scipy','openpyxl')}})

# Re-read every original model export. Numeric variable names avoid location whitespace.
log=[]
env=gp.Env(empty=True);env.setParam('OutputFlag',0);env.start()
try:
    for path in sorted((RUN/'models').glob('*.lp')):
        m=gp.read(str(path),env=env)
        log.append({'filename':path.name,'variables':m.NumVars,'constraints':m.NumConstrs,'objectives':m.NumObj,
                    'parse_status':'PASS','sha256':hashlib.sha256(path.read_bytes()).hexdigest()});m.dispose()
finally: env.dispose()
dump(RUN/'model_readback_verification.json',{'status':'PASS','models_read_successfully':len(log),
    'optimization_performed':False,'models':log})

p=json.loads((BASE/'snapshots/04_Results/Optimization/baseline_inputs.json').read_text())
setup_used=sum(z['value'] for z in p['setup_cost'] if z['intervention']=='Drainage')
assert setup_used==17000 and setup_used<=p['setup_budget']
params={name:{tuple(z[k] for k in ('scenario','location','intervention')):z['value'] for z in p[name]}
        for name in ('deploy_cost','labour','equipment','supply','upper_bound')}
witness=[]
for s in p['probabilities']:
    checks=[]
    for coeff,cap in [('deploy_cost','operating_budget'),('labour','labour_capacity'),('equipment','equipment_capacity'),('supply','supply_capacity')]:
        used=sum(2*params[coeff][s,j,'Drainage'] for j in ('Tai O1','Tai O2'))
        assert used<=p[cap][s]
        checks.append({'row':cap,'used':used,'capacity':p[cap][s]})
    assert all(2<=params['upper_bound'][s,j,'Drainage'] for j in ('Tai O1','Tai O2'))
    witness.append({'scenario':s,'ready_sites':['Tai O1/Drainage','Tai O2/Drainage'],'setup_used_CU':setup_used,
        'n':2,'capital_used_HKD':2000000,'deploy_each_location':2,'resource_checks':checks,
        'replicated_stock_each_site_rhs':2,'replicated_feasible':True,'shared_total_used':4,'shared_rhs':2,'shared_feasible':False})
dump(RUN/'shared_inventory_feasible_set_witness.json',{'status':'PASS','hypothetical_policy_under_frozen_inputs':True,
    'not_an_optimal_policy_claim':True,'scenarios':witness})
print(json.dumps({'fixed_policy_comparison':rows,'models_checked':len(log)}))
