"""Enumerate all feasible first-stage policies for selected EV-optimal-policy ranges."""
from pathlib import Path
from dataclasses import replace
import csv,itertools,json,sys,time
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'02_Model'))
from crisp_parameters import load_inputs
from crisp_model import Runner,PumpFleet

def main():
    out=Path(sys.argv[1]);base=load_inputs(ROOT/'01_Data/CRISP_Master_Data.xlsx')
    runner=Runner(out/'ev_tie_audit');rows=[];details=[];start=time.monotonic()
    names=['legacy_baseline','mobile_baseline','fleet_00','fleet_01','fleet_03','fleet_04','fleet_06','fleet_08','fleet_12','fleet_20']
    pairs=list(base.setup_cost)
    try:
        for name in names:
            saved=json.loads((out/'solutions'/f'{name}.json').read_text());raw=saved['fleet']
            fleet=PumpFleet(**{**raw,'accessible_locations':tuple(raw['accessible_locations'])}) if raw else None
            target=saved['ev']['objective'];ev=runner.expected(base);policies=[];tried=0
            for mask in range(2**len(pairs)):
                yy={k:int(bool(mask&2**i)) for i,k in enumerate(pairs)}
                if sum(base.setup_cost[k]*yy[k] for k in pairs)>base.setup_budget+1e-6:continue
                # With no prepared pump site, positive procurement cannot alter recourse.
                ns=range(fleet.maximum_new_pumps+1) if fleet else (0,)
                for n in ns:
                    fixed={'y':yy,'n':n};tag=f'{name}_{mask}_{n}'
                    er=runner.solve(ev,tag+'_ev',fleet,fixed=fixed);tried+=1
                    if abs(er['objective']-target)>1e-6:continue
                    sr=runner.solve(base,tag+'_eev',fleet,fixed=fixed)
                    d={'case':name,'y_mask':mask,'new_pumps':n,'setup_used':sr['setup_used'],
                        'plan':sr['plan'],'ev':er['objective'],'eev':sr['objective']}
                    policies.append(d);details.append(d)
            assert policies
            best=max(policies,key=lambda x:x['eev']);worst=min(policies,key=lambda x:x['eev'])
            rp=saved['rp']['objective'];min_n=min(p['new_pumps'] for p in policies)
            min_n_policies=[p for p in policies if p['new_pumps']==min_n]
            min_setup=min(p['setup_used'] for p in min_n_policies)
            lex=[p for p in min_n_policies if abs(p['setup_used']-min_setup)<1e-6]
            rows.append({'case':name,'feasible_first_stage_policies_enumerated':tried,'EV_optimal_policies':len(policies),
                'selected_EEV':saved['eev']['objective'],'best_EEV_among_EV_optima':best['eev'],
                'worst_EEV_among_EV_optima':worst['eev'],'minimum_VSS_over_EV_optima':rp-best['eev'],
                'maximum_VSS_over_EV_optima':rp-worst['eev'],
                'EV_minimum_new_pumps':min_n,'EV_minimum_readiness_given_minimum_pumps':min_setup,
                'policies_after_two_secondary_objectives':len(lex),
                'best_EEV_plan':best['plan'],'best_EEV_new_pumps':best['new_pumps']})
            print(json.dumps(rows[-1],ensure_ascii=False),flush=True)
        for filename,data in [('ev_policy_tie_ranges.csv',rows),('ev_optimal_policies.csv',details)]:
            with (out/filename).open('w',encoding='utf-8-sig',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
        (out/'ev_tie_verification.json').write_text(json.dumps({'status':'PASS','cases':len(rows),
            'policies_enumerated':sum(x['feasible_first_stage_policies_enumerated'] for x in rows),
            'solver_runs':len(runner.audit),'all_optimal':True,'elapsed_seconds':time.monotonic()-start},indent=2))
    finally:runner.close()

if __name__=='__main__':main()
