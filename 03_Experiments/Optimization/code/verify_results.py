"""Independent matrix/HiGHS verification; does not import either Gurobi builder."""
from pathlib import Path
import argparse,csv,hashlib,json,math,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
import scipy

HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
CAPS={'deploy_cost':'operating_budget','labour':'labour_capacity','equipment':'equipment_capacity','supply':'supply_capacity'}
def read(path):return json.loads(path.read_text())
def unpack(raw):
    p={}
    for k,v in raw.items():
        p[k]={tuple(row[x] for x in row if x!='value'):row['value'] for row in v} if isinstance(v,list) else v
    return p
def expected(p):
    q=dict(p);prob=p['probabilities'];q['probabilities']={'EV':1.0}
    for k in ['deploy_cost','labour','equipment','supply','upper_bound','benefit']:
        q[k]={('EV',j,i):sum(prob[s]*p[k][s,j,i] for s in prob) for j,i in p['setup_cost']}
    for k in CAPS.values():q[k]={'EV':sum(prob[s]*p[k][s] for s in prob)}
    return q
def check_solution(p,fleet,sol,allowed):
    if not sol['feasible']:return
    y={(r['location'],r['intervention']):r['y'] for r in sol['y']}
    x={(r['scenario'],r['location'],r['intervention']):r['x'] for r in sol['x']}
    assert set(y)==set(p['setup_cost'])
    assert set(x)==set(p['benefit'])
    assert all(v in (0,1) for v in y.values()) and all(v>=0 and v==round(v) for v in x.values())
    assert all(not y[j,i] for j,i in y if i not in allowed)
    assert sum(p['setup_cost'][k]*y[k] for k in y)<=p['setup_budget']+1e-6
    for (s,j,i),v in x.items():assert v<=p['upper_bound'][s,j,i]*y[j,i]+1e-6
    for s in p['probabilities']:
        for coef,cap in CAPS.items():assert sum(p[coef][s,j,i]*x[s,j,i] for j,i in y)<=p[cap][s]+1e-6
    if fleet:
        n=sol['new_pumps'];assert isinstance(n,int) and n>=0
        assert n*fleet['purchase_price_hkd']<=fleet['capital_budget_hkd']+1e-6
        for s in p['probabilities']:
            assert sum(x[s,j,'Drainage'] for j in p['beta'])<=n+fleet['existing_stock']
            assert all(x[s,j,'Drainage']==0 for j in p['beta'] if j not in fleet['accessible_locations'])
    obj=sum(p['probabilities'][s]*p['benefit'][s,j,i]*v for (s,j,i),v in x.items())
    assert abs(obj-sol['objective'])<1e-6

def highs(p,fleet,allowed):
    pairs=list(p['setup_cost']);triples=list(p['benefit']);S=list(p['probabilities']);J=list(p['beta'])
    yi={k:n for n,k in enumerate(pairs)};xi={k:len(pairs)+n for n,k in enumerate(triples)}
    ni=len(pairs)+len(triples);size=ni+(fleet is not None)
    lo=np.zeros(size);hi=np.full(size,np.inf);hi[:len(pairs)]=1
    for (j,i),idx in yi.items():
        if i not in allowed:hi[idx]=0
    if fleet:
        hi[ni]=math.floor(fleet['capital_budget_hkd']/fleet['purchase_price_hkd']+1e-10)
        for (s,j,i),idx in xi.items():
            if i=='Drainage' and j not in fleet['accessible_locations']:hi[idx]=0
    objective=np.zeros(size)
    for (s,j,i),idx in xi.items():objective[idx]=-p['probabilities'][s]*p['benefit'][s,j,i]
    rows=[];rhs=[]
    def row(terms,b):
        a=np.zeros(size)
        for idx,v in terms:a[idx]+=v
        rows.append(a);rhs.append(b)
    row([(yi[k],p['setup_cost'][k]) for k in pairs],p['setup_budget'])
    for s in S:
        for coef,cap in CAPS.items():row([(xi[s,j,i],p[coef][s,j,i]) for j,i in pairs],p[cap][s])
        if fleet:row([(xi[s,j,'Drainage'],1) for j in J]+[(ni,-1)],fleet['existing_stock'])
    for s,j,i in triples:row([(xi[s,j,i],1),(yi[j,i],-p['upper_bound'][s,j,i])],0)
    result=milp(objective,integrality=np.ones(size),bounds=Bounds(lo,hi),
        constraints=LinearConstraint(np.array(rows),-np.inf,np.array(rhs)),
        options={'mip_rel_gap':0.0,'time_limit':60.0})
    assert result.status==0,result.message
    return -float(result.fun)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('results',type=Path);args=ap.parse_args();out=args.results
    start=time.monotonic();deltas=[];checked=0
    for path in sorted((out/'solutions').glob('*.json')):
        r=read(path);p=unpack(r['parameters']);f=r['fleet'];allowed=set(r['config'].get('allowed',p['life_score']))
        check_solution(p,f,r['rp'],allowed);check_solution(p,f,r['eev'],allowed)
        check_solution(p,f,r['fixed_baseline'],allowed)
        e=expected(p);check_solution(e,f,r['ev'],allowed)
        assert r['eev']['y']==r['ev']['y'] and r['eev']['new_pumps']==r['ev']['new_pumps']
        for s,sol in r['ws'].items():
            q=dict(p);q['probabilities']={s:1.0}
            for key in ['deploy_cost','labour','equipment','supply','benefit','upper_bound']:
                q[key]={k:v for k,v in p[key].items() if k[0]==s}
            check_solution(q,f,sol,allowed)
        ws=sum(p['probabilities'][s]*sol['objective'] for s,sol in r['ws'].items())
        assert abs(ws-r['summary']['ws'])<1e-6
        value=highs(p,f,allowed);delta=abs(value-r['summary']['rp']);assert delta<1e-5,(path.name,value,r['summary']['rp'])
        deltas.append(delta);checked+=1
        if checked%100==0:print(f'HiGHS verified {checked}/555 RP optima',flush=True)
    assert checked==555
    # The deterministic repeated run should reproduce every primary metric and first-stage choice.
    reference=read(ROOT/'01_Data/Controls/pre_cleanup_metrics.json')['cases'];replicated=0
    for path in (out/'solutions').glob('*.json'):
        a=read(path)['summary'];b=reference[a['id']]
        for k in ['rp','ws','ev','eev','vss','evpi','new_pumps','setup_used']:
            assert abs(a[k]-b[k])<1e-9,(path.name,k)
        assert a['plan']==b['plan'];replicated+=1
    changes=[]
    current=read(out/'manifest_start.json')['source_sha256']
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in current.items())
    result={'status':'PASS','scipy_version':scipy.__version__,'independent_solver':'HiGHS via scipy.optimize.milp',
        'independent_RP_optima_verified':checked,'max_objective_difference':max(deltas),
        'all_saved_models_feasibility_and_objectives_reconstructed':True,
        'EEV_readiness_and_procurement_fixed':True,'repeated_run_configurations_matched':replicated,
        'input_and_source_hashes_checked':len(current),
        'unexpected_original_file_changes':changes,'current_source_hashes_match':True,
        'elapsed_seconds':time.monotonic()-start}
    (out/'independent_verification.json').write_text(json.dumps(result,indent=2,ensure_ascii=False));print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
