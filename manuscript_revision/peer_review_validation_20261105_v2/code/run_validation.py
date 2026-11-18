"""Minimal separately versioned peer-review validation. Never mutates frozen inputs."""
from __future__ import annotations
import argparse, csv, hashlib, itertools, json, math, platform, shutil, sys, time
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(BASE / 'snapshots' / '02_Model' if (BASE / 'snapshots' / '02_Model').exists() else ROOT / '02_Model'))
import gurobipy as gp
from gurobipy import GRB
from crisp_parameters import load_inputs, _parameters_to_json
from crisp_model import Runner, load_case_settings

PAIRS = [('deploy_cost', 'operating_budget'), ('labour', 'labour_capacity'),
         ('equipment', 'equipment_capacity'), ('supply', 'supply_capacity')]
TOL = 1e-6

def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False))

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''): h.update(block)
    return h.hexdigest()

def table(path, rows):
    if not rows: return
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def frozen_manifest():
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(ROOT.rglob('*'))
            if p.is_file() and BASE not in p.parents
            and ROOT/'manuscript_revision/peer_review_validation_20261105_v1' not in p.parents
            and not any(x in p.parts for x in ('.venv', '__pycache__', '.git'))
            and p.name != '.DS_Store'}

def initialize():
    guard = BASE / 'frozen_manifest_before.json'
    if guard.exists(): raise RuntimeError('Initialization already exists; refuse overwrite')
    dump(guard, frozen_manifest())
    for rel in ('02_Model/crisp_parameters.py', '02_Model/crisp_model.py',
                '01_Data/CRISP_Master_Data.xlsx', '03_Experiments/Experiment_Protocol.json', 'requirements-lock.txt',
                'manuscript_revision/Revised_Manuscript_EN_v2.md',
                '04_Results/Optimization/baseline_inputs.json',
                '04_Results/Optimization/solutions/legacy_baseline.json',
                '04_Results/Optimization/solutions/mobile_baseline.json',
                '04_Results/Scenario_Stability/tables/baseline_scenarios.csv',
                'manuscript_revision/audit/ci01_independent_20261104/analysis/scenario_impact.json',
                'manuscript_revision/audit/ci01_independent_20261104/analysis/Scenario_Comparisons.csv',
                'manuscript_revision/audit/ci01_independent_20261104/analysis/Original23_Label_Migration.csv',
                'manuscript_revision/audit/ci01_independent_20261104/analysis/scenarios/reconstructed60_adjudicated/scenario_summary.csv',
                'manuscript_revision/audit/ci01_independent_20261104/code/run_backend.py',
                'manuscript_revision/audit/ci01_independent_20261104/backend_probability60/inputs.json',
                'manuscript_revision/audit/ci01_independent_20261104/backend_probability60/solutions/legacy_baseline.json',
                'manuscript_revision/audit/ci01_independent_20261104/backend_probability60/solutions/mobile_baseline.json'):
        dest = BASE / 'snapshots' / rel
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(ROOT / rel, dest)
    print('Frozen guard initialized:', len(json.loads(guard.read_text())), 'files', flush=True)

def config(stock='shared', integer_n=True, budget=2000000, access=('Tai O1','Tai O2'), coverage=0):
    return {'stock':stock, 'integer_n':integer_n, 'existing_stock':0,
            'capital_budget_hkd':budget, 'purchase_price_hkd':1000000,
            'accessible_locations':list(access), 'coverage_each_location_each_scenario':coverage}

class AuditSolver:
    def __init__(self, out):
        self.out = out; out.mkdir(parents=True, exist_ok=False)
        for part in ('logs', 'models', 'sol', 'solutions', 'parameters'): (out/part).mkdir()
        self.env = gp.Env(empty=True); self.env.setParam('OutputFlag',0); self.env.start()
        self.rows=[]; self.started=time.monotonic()

    def close(self): self.env.dispose()

    def solve(self, p, c, tag, fixed=None):
        if time.monotonic()-self.started > 1200: raise TimeoutError('1200s run hard limit')
        raw = _parameters_to_json(p)
        pid = hashlib.sha256(json.dumps(raw, sort_keys=True).encode()).hexdigest()[:20]
        if not (self.out/'parameters'/f'{pid}.json').exists(): dump(self.out/'parameters'/f'{pid}.json',raw)
        pairs=list(p.setup_cost); triples=[(s,j,i) for s in p.scenarios for j,i in pairs]
        m=gp.Model(tag, env=self.env)
        for key,val in {'OutputFlag':1, 'LogToConsole':0,'Seed':0,'Threads':1,'MIPGap':0,'MIPGapAbs':0,
                        'FeasibilityTol':1e-8,'IntFeasTol':1e-8,'TimeLimit':60,
                        'LogFile':str(self.out/'logs'/f'{tag}.log')}.items(): m.setParam(key,val)
        y={k:m.addVar(vtype=GRB.BINARY,name=f'ready_{z}') for z,k in enumerate(pairs)}
        x={k:m.addVar(vtype=GRB.INTEGER,lb=0,name=f'deploy_{z}') for z,k in enumerate(triples)}
        n=m.addVar(lb=0,ub=c['capital_budget_hkd']/c['purchase_price_hkd'],
                   vtype=GRB.INTEGER if c['integer_n'] else GRB.CONTINUOUS,name='new_pumps')
        setup=gp.quicksum(p.setup_cost[k]*y[k] for k in pairs)
        obj=gp.quicksum(p.probabilities[s]*p.benefit[s,j,i]*x[s,j,i] for s,j,i in triples)
        m.addConstr(setup<=p.setup_budget,name='readiness_budget_CU')
        m.addConstr(c['purchase_price_hkd']*n<=c['capital_budget_hkd'],name='capital_HKD')
        if fixed:
            for k in pairs: m.addConstr(y[k]==fixed['y'][pairs.index(k)],name=f'fix_y_{pairs.index(k)}')
            m.addConstr(n==fixed['n'],name='fix_n')
        for s in p.scenarios:
            for a,b in PAIRS:
                m.addConstr(gp.quicksum(getattr(p,a)[s,j,i]*x[s,j,i] for j,i in pairs)
                            <=getattr(p,b)[s],name=f'{b}_{s}')
            for j,i in pairs: m.addConstr(x[s,j,i]<=p.upper_bound[s,j,i]*y[j,i],name=f'link_{s}_{j}_{i}'.replace(' ','_'))
            if c['stock']=='shared':
                m.addConstr(gp.quicksum(x[s,j,'Drainage'] for j in p.locations)<=c['existing_stock']+n,name=f'shared_{s}')
            elif c['stock']=='replicated':
                for j in p.locations: m.addConstr(x[s,j,'Drainage']<=c['existing_stock']+n,name=f'replicated_{s}_{j}'.replace(' ','_'))
            elif c['stock']!='none': raise ValueError(c['stock'])
            for j in p.locations:
                if j not in c['accessible_locations']: m.addConstr(x[s,j,'Drainage']==0,name=f'access_{s}_{j}'.replace(' ','_'))
                if c['coverage_each_location_each_scenario']:
                    m.addConstr(gp.quicksum(x[s,j,i] for i in p.interventions)>=c['coverage_each_location_each_scenario'],name=f'coverage_{s}_{j}'.replace(' ','_'))
        m.ModelSense=GRB.MAXIMIZE
        for idx,(expr,priority,name) in enumerate(((obj,4,'benefit'),(-n,3,'minimum_procurement'),
                (-setup,2,'minimum_readiness'),(-gp.quicksum(2**k*y[z] for k,z in enumerate(pairs)),1,'minimum_mask'))):
            m.setObjectiveN(expr,idx,priority=priority,abstol=1e-8,reltol=0,name=name)
        m.write(str(self.out/'models'/f'{tag}.lp')); m.optimize()
        result={'tag':tag,'parameter_id':pid,'config':c,'fixed_policy':fixed,
                'status_code':m.Status,'status':{2:'OPTIMAL',3:'INFEASIBLE'}.get(m.Status,str(m.Status)),
                'runtime_seconds':m.Runtime,'node_count':m.NodeCount,'solution_count':m.SolCount,
                'objective':None,'primary_value_from_solver':None}
        if m.Status==GRB.OPTIMAL:
            yy=[int(round(y[k].X)) for k in pairs]; nn=n.X
            xx={z:int(round(x[z].X)) for z in triples}
            objective=sum(p.probabilities[s]*p.benefit[s,j,i]*xx[s,j,i] for s,j,i in triples)
            residuals=[{'constraint':'readiness','lhs':sum(p.setup_cost[k]*yy[i] for i,k in enumerate(pairs)),'rhs':p.setup_budget},
                {'constraint':'capital','lhs':c['purchase_price_hkd']*nn,'rhs':c['capital_budget_hkd']}]
            for s in p.scenarios:
                for a,b in PAIRS: residuals.append({'constraint':f'{s}/{b}','lhs':sum(getattr(p,a)[s,j,i]*xx[s,j,i] for j,i in pairs),'rhs':getattr(p,b)[s]})
                for z,(j,i) in enumerate(pairs): residuals.append({'constraint':f'link/{s}/{j}/{i}','lhs':xx[s,j,i],'rhs':p.upper_bound[s,j,i]*yy[z]})
                if c['stock']=='shared': residuals.append({'constraint':f'shared/{s}','lhs':sum(xx[s,j,'Drainage'] for j in p.locations),'rhs':c['existing_stock']+nn})
                if c['stock']=='replicated':
                    for j in p.locations: residuals.append({'constraint':f'replicated/{s}/{j}','lhs':xx[s,j,'Drainage'],'rhs':c['existing_stock']+nn})
                for j in p.locations:
                    if j not in c['accessible_locations']: residuals.append({'constraint':f'access/{s}/{j}','lhs':xx[s,j,'Drainage'],'rhs':0})
                    if c['coverage_each_location_each_scenario']: residuals.append({'constraint':f'coverage/{s}/{j}','lhs':c['coverage_each_location_each_scenario'],'rhs':sum(xx[s,j,i] for i in p.interventions)})
            for r in residuals: r['slack']=r['rhs']-r['lhs']
            violation=max(0,max(-r['slack'] for r in residuals))
            integrality=max([abs(y[k].X-round(y[k].X)) for k in pairs]+[abs(x[z].X-round(x[z].X)) for z in triples]+([abs(nn-round(nn))] if c['integer_n'] else [0]))
            assert violation<TOL and integrality<TOL and abs(objective-m.ObjVal)<TOL
            if fixed: assert yy==fixed['y'] and abs(nn-fixed['n'])<TOL
            result.update(objective=objective,policy={'y':yy,'n':nn},
                plan=';'.join(f'{j}/{i}' for z,(j,i) in enumerate(pairs) if yy[z]),
                x=[{'scenario':s,'location':j,'intervention':i,'x':xx[s,j,i]} for s,j,i in triples],
                residuals=residuals,validation={'max_constraint_violation':violation,'max_integrality_error':integrality,
                'objective_reconstruction_error':abs(objective-m.ObjVal),'fixed_stage_preserved':True},
                primary_value_from_solver=m.ObjNVal)
            # Primary proof of optimality is in each multiobjective solver log; m.ObjBound after final tie objective is not a primary bound.
            m.write(str(self.out/'sol'/f'{tag}.sol'))
        elif m.Status==GRB.INFEASIBLE:
            m.computeIIS(); m.write(str(self.out/'models'/f'{tag}.ilp'))
        else: raise RuntimeError(f'{tag}: {m.Status}')
        dump(self.out/'solutions'/f'{tag}.json',result)
        self.rows.append({k:result[k] for k in ('tag','parameter_id','status','status_code','objective','runtime_seconds','node_count','solution_count')})
        m.dispose(); return result

def run(out):
    manifest=json.loads((BASE/'frozen_manifest_before.json').read_text())
    p=load_inputs(BASE/'snapshots/01_Data/CRISP_Master_Data.xlsx')
    assert p.upper_bound==p.with_recomputed_bounds().upper_bound
    old=json.loads((BASE/'snapshots/04_Results/Optimization/baseline_inputs.json').read_text())
    assert _parameters_to_json(p)==old
    new_path='manuscript_revision/audit/ci01_independent_20261104/backend_probability60/inputs.json'
    new=json.loads((BASE/'snapshots'/new_path).read_text())
    assert {k:v for k,v in new.items() if k!='probabilities'}=={k:v for k,v in old.items() if k!='probabilities'}
    qs={'23':p,'60':replace(p,probabilities=new['probabilities'])}
    settings=load_case_settings(BASE/'snapshots/01_Data/CRISP_Master_Data.xlsx',BASE/'snapshots/03_Experiments/Experiment_Protocol.json')
    assert settings['primary_case']=={'existing_stock':0,'capital_budget_hkd':2000000,
        'purchase_price_hkd':1000000,'accessible_locations':['Tai O1','Tai O2']}
    assert all(abs(qs['60'].probabilities[s]-v)<1e-12 for s,v in zip(p.scenarios,(35/60,19/60,6/60)))
    solver=AuditSolver(out); evrows=[]; allpolicies=[]; alltrials=[]; boundrows=[]; component=[]; coverage=[]; compatibility=[]
    dump(out/'run_manifest.json',{'started_at':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
        'python':sys.version,'platform':platform.platform(),'gurobi_version':gp.gurobi.version(),
        'code_sha256':sha(Path(__file__)),'assessment_sha256':sha(BASE/'assessment/Decision_Before_Execution.md'),
        'independent_pre_execution_review_sha256':sha(BASE/'assessment/Independent_Pre_Execution_Review.md'),
        'primary_workbook_settings':settings['primary_case'],
        'solver_settings':{'Seed':0,'Threads':1,'MIPGap':0,'MIPGapAbs':0,'FeasibilityTol':1e-8,'IntFeasTol':1e-8,'solve_timeout_s':60,'run_timeout_s':1200},
        'experiment_scope':'8 EV specifications; 24 component cases; 8 coverage cases; full EV policy enumeration',
        'empirical_calibration':False,'old_files_protected':len(manifest)})
    try:
        for freq,q in qs.items():
            for model in ('legacy','mobile'):
                c=config(stock='none' if model=='legacy' else 'shared',budget=0 if model=='legacy' else 2000000)
                rp=solver.solve(q,c,f'f{freq}_{model}_rp')
                ws=[solver.solve(replace(q,scenarios=(s,),probabilities={s:1.0}),c,f'f{freq}_{model}_ws_{s}') for s in q.scenarios]
                wsv=sum(q.probabilities[s]*z['objective'] for s,z in zip(q.scenarios,ws))
                ea=Runner.expected(q); eb=ea.with_recomputed_bounds()
                for j,i in q.setup_cost:
                    boundrows.append({'frequency':freq,'model':model,'location':j,'intervention':i,
                        'U_A':ea.upper_bound['EV',j,i],'effective_integer_U_A':math.floor(ea.upper_bound['EV',j,i]+1e-10),
                        'U_B':eb.upper_bound['EV',j,i]})
                byconv={}
                for conv,evp in (('A',ea),('B',eb)):
                    tag=f'f{freq}_{model}_{conv}'
                    ev=solver.solve(evp,c,tag+'_ev'); eev=solver.solve(q,c,tag+'_eev',ev['policy'])
                    policies=[]; tried=0
                    for mask in range(64):
                        yy=[int(bool(mask&2**z)) for z in range(6)]
                        if sum(q.setup_cost[k]*yy[z] for z,k in enumerate(q.setup_cost))>q.setup_budget+TOL: continue
                        for n in range(1 if model=='legacy' else 3):
                            fixed={'y':yy,'n':n}; er=solver.solve(evp,c,f'{tag}_enum_{mask}_{n}_ev',fixed); tried+=1
                            optimal=abs(er['objective']-ev['objective'])<=TOL
                            alltrials.append({'frequency':freq,'model':model,'convention':conv,'mask':mask,'n':n,'ev':er['objective'],'is_primary_ev_optimum':optimal,'tag':er['tag']})
                            if not optimal: continue
                            sr=solver.solve(q,c,f'{tag}_enum_{mask}_{n}_eev',fixed)
                            row={'frequency':freq,'model':model,'convention':conv,'mask':mask,'n':n,'plan':sr['plan'],
                                 'ev':er['objective'],'eev':sr['objective'],'vss':rp['objective']-sr['objective']}
                            policies.append(row); allpolicies.append(row)
                    assert policies and all(wsv+TOL>=rp['objective']>=z['eev']-TOL for z in policies)
                    selected=min(policies,key=lambda z:(z['n'],sum(q.setup_cost[k]*int(bool(z['mask']&2**j)) for j,k in enumerate(q.setup_cost)),z['mask']))
                    assert ev['policy']['y']==[int(bool(selected['mask']&2**j)) for j in range(6)] and abs(ev['policy']['n']-selected['n'])<TOL
                    r={'frequency':freq,'model':model,'convention':conv,'rp':rp['objective'],'ws':wsv,'ev':ev['objective'],
                       'selected_ev_plan':ev['plan'],'selected_ev_n':ev['policy']['n'],'selected_eev':eev['objective'],
                       'selected_vss':rp['objective']-eev['objective'],'evpi':wsv-rp['objective'],
                       'feasible_policies_enumerated':tried,'ev_optimal_policy_count':len(policies),
                       'eev_min':min(z['eev'] for z in policies),'eev_max':max(z['eev'] for z in policies),
                       'vss_min':min(z['vss'] for z in policies),'vss_max':max(z['vss'] for z in policies)}
                    evrows.append(r); byconv[conv]=r; print(json.dumps(r),flush=True)
                    if conv=='A':
                        rel=f'04_Results/Optimization/solutions/{model}_baseline.json' if freq=='23' else f'manuscript_revision/audit/ci01_independent_20261104/backend_probability60/solutions/{model}_baseline.json'
                        frozen=json.loads((BASE/'snapshots'/rel).read_text())['summary']
                        for key,newkey in [('rp','rp'),('ws','ws'),('ev','ev'),('eev','selected_eev'),('vss','selected_vss'),('evpi','evpi')]:
                            err=abs(frozen[key]-r[newkey]); assert err<TOL
                            compatibility.append({'frequency':freq,'model':model,'metric':key,'frozen':frozen[key],'rerun':r[newkey],'absolute_error':err})
                assert byconv['B']['ev']+TOL>=byconv['A']['ev']
            # Ordered structural counterfactuals; all other parameters identical inside each panel.
            for budget in (2000000,6500000):
                specs=[('F0_no_stock',config(stock='none',integer_n=False,budget=budget)),
                       ('F1_replicated_continuous',config(stock='replicated',integer_n=False,budget=budget)),
                       ('F2_shared_continuous',config(integer_n=False,budget=budget)),
                       ('F3_shared_integer',config(budget=budget)),
                       ('A1_access_O1_only',config(budget=budget,access=('Tai O1',))),
                       ('A2_access_O2_only',config(budget=budget,access=('Tai O2',)))]
                prev=None; shared_integer_value=None
                for name,c in specs:
                    z=solver.solve(q,c,f'f{freq}_budget{budget}_{name}')
                    reference=shared_integer_value if name.startswith('A') else prev
                    if reference is not None: assert reference+TOL>=z['objective']
                    row={'frequency':freq,'capital_budget_hkd':budget,'case':name,'status':z['status'],'rp':z['objective'],
                         'comparison_reference':'F3_shared_integer' if name.startswith('A') else 'previous_chain_case',
                         'delta_vs_reference':None if reference is None else z['objective']-reference,
                         'n':z['policy']['n'],'plan':z['plan'],'tag':z['tag']}
                    if name=='F2_shared_continuous': continuous=z['objective']
                    if name=='F3_shared_integer':
                        assert abs(continuous-z['objective'])<TOL
                        shared_integer_value=z['objective']
                    component.append(row); prev=z['objective']
                print('Component panel complete',freq,budget,flush=True)
            basevalue=None
            for k in (0,1,2,6):
                z=solver.solve(q,config(coverage=k),f'f{freq}_coverage_{k}')
                if k==0: basevalue=z['objective']
                if k==6: assert z['status']=='INFEASIBLE'
                else: assert z['status']=='OPTIMAL' and z['objective']<=basevalue+TOL
                coverage.append({'frequency':freq,'minimum_packages_each_location_each_scenario':k,'status':z['status'],
                    'rp':z['objective'],'delta_vs_no_coverage':None if z['objective'] is None else z['objective']-basevalue,
                    'n':None if z['objective'] is None else z['policy']['n'],'plan':z.get('plan'),'tag':z['tag']})
        for filename,rows in [('ev_summary.csv',evrows),('ev_optimal_policies.csv',allpolicies),('ev_all_policy_trials.csv',alltrials),
                              ('ev_bounds.csv',boundrows),('component_summary.csv',component),('coverage_summary.csv',coverage),
                              ('frozen_baseline_compatibility.csv',compatibility),('solver_audit.csv',solver.rows)]: table(out/filename,rows)
        current={rel:sha(ROOT/rel) if (ROOT/rel).exists() else None for rel in manifest}
        changed=[rel for rel in manifest if current[rel]!=manifest[rel]]
        dump(out/'frozen_guard.json',{'old_file_count':len(manifest),'changed_or_missing':changed,'pass':not changed})
        assert not changed
        assert sha(Path(__file__))==json.loads((out/'run_manifest.json').read_text())['code_sha256']
        dump(out/'validation.json',{'status':'PASS','solves':len(solver.rows),'optimal':sum(z['status']=='OPTIMAL' for z in solver.rows),
            'infeasible_expected':sum(z['status']=='INFEASIBLE' for z in solver.rows),'ev_specs':len(evrows),'enumerated_policies':len(alltrials),
            'all_primary_ev_optima':len(allpolicies),'component_cases':len(component),'coverage_cases':len(coverage),
            'frozen_baseline_metrics_matched':len(compatibility),'old_files_unchanged':not changed,
            'elapsed_seconds':time.monotonic()-solver.started,'empirical_validation':False})
    finally: solver.close()

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--initialize',action='store_true'); ap.add_argument('--output',type=Path); args=ap.parse_args()
    if args.initialize: initialize()
    else: run(args.output or BASE/'runs'/'primary')
