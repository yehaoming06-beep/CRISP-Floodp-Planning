"""CRISP v2: shared mobile-pump procurement and scenario-wise allocation.

Capital procurement is in HKD. Existing readiness/operation coefficients and
benefit scores remain illustrative CU/score inputs; they are not converted to HKD.
One Drainage deployment unit is assumed to be one simultaneous pump assignment.
No hydraulic or avoided-loss calibration is implied by that unit convention.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, replace
from pathlib import Path
import json, math
import gurobipy as gp
from gurobipy import GRB
from crisp_parameters import Parameters, _parameters_to_json
from openpyxl import load_workbook

def load_case_settings(workbook_path:Path,protocol_path:Path):
    """Read current procurement/access drivers from the single master workbook."""
    settings=json.loads(protocol_path.read_text())
    wb=load_workbook(workbook_path,data_only=True,read_only=True)
    if 'Mobile_Pump' not in wb.sheetnames or 'Study_Area' not in wb.sheetnames:
        raise ValueError('Current master workbook requires Mobile_Pump and Study_Area sheets')
    ws=wb['Mobile_Pump']
    def number(cell):
        value=ws[cell].value
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
            raise ValueError(f'Missing numeric input: Mobile_Pump!{cell}')
        return value
    stock=number('B4')
    if stock<0 or stock!=round(stock):raise ValueError('Existing pump stock must be a nonnegative integer')
    access=[('Tai O1',number('B7')),('Tai O2',number('B8'))]
    if any(v not in (0,1) for _,v in access):raise ValueError('Access flags must be 0 or 1')
    settings['primary_case']={'existing_stock':int(stock),'capital_budget_hkd':number('B5'),
        'purchase_price_hkd':number('B6'),'accessible_locations':[j for j,v in access if v==1]}
    pop=wb['Study_Area']
    settings['evidence']={'purchase_price_hkd':'Approximate 2025 equipment procurement reference',
        'source_url':ws['E6'].value,'resident_population_2021':{pop.cell(r,1).value:pop.cell(r,3).value for r in (2,3)},
        'population_use':'Context only, not exposure or calibrated beta'}
    wb.close()
    return settings

TOL=1e-6
RESOURCE_PAIRS=(("deploy_cost","operating_budget"),("labour","labour_capacity"),
                ("equipment","equipment_capacity"),("supply","supply_capacity"))

@dataclass(frozen=True)
class PumpFleet:
    existing_stock: int
    capital_budget_hkd: float
    purchase_price_hkd: float
    accessible_locations: tuple[str,...]

    def validate(self, locations):
        if isinstance(self.existing_stock,bool) or not isinstance(self.existing_stock,int) or self.existing_stock<0:
            raise ValueError("Existing stock must be an explicit nonnegative integer scenario assumption")
        if not math.isfinite(self.capital_budget_hkd) or self.capital_budget_hkd<0:
            raise ValueError("Capital budget must be finite and nonnegative")
        if not math.isfinite(self.purchase_price_hkd) or self.purchase_price_hkd<=0:
            raise ValueError("Purchase price must be finite and positive")
        if not set(self.accessible_locations)<=set(locations):
            raise ValueError("Unknown accessible location")

    @property
    def maximum_new_pumps(self):
        return math.floor(self.capital_budget_hkd/self.purchase_price_hkd+1e-10)


class Runner:
    def __init__(self, output: Path):
        self.output=Path(output)
        for part in ('logs','solutions'):(self.output/part).mkdir(parents=True,exist_ok=True)
        self.env=gp.Env(empty=True);self.env.setParam('OutputFlag',0);self.env.start()
        self.env.setParam('LogToConsole',0);self.env.setParam('OutputFlag',1)
        self.audit=[]

    def close(self):self.env.dispose()

    def solve(self,p:Parameters,tag:str,fleet:PumpFleet|None=None,allowed=None,fixed=None):
        """Fix ALL first-stage choices (readiness and procurement) in EEV/regret runs."""
        if abs(sum(p.probabilities.values())-1)>1e-10 or set(p.probabilities)!=set(p.scenarios) or any(
                not math.isfinite(v) or v<0 for v in p.probabilities.values()):
            raise ValueError('Invalid scenario probabilities')
        if fleet is not None:fleet.validate(p.locations)
        pairs=[(j,i) for j in p.locations for i in p.interventions]
        triples=[(s,j,i) for s in p.scenarios for j,i in pairs]
        allowed=set(p.interventions) if allowed is None else set(allowed)
        if fixed:
            used=sum(p.setup_cost[k]*fixed['y'][k] for k in pairs)
            if used>p.setup_budget+TOL:return self.infeasible('INFEASIBLE_READINESS_BUDGET')
            if any(v and i not in allowed for (j,i),v in fixed['y'].items()):return self.infeasible('INFEASIBLE_ABLATION')
            if fleet and (fixed['n']<0 or fixed['n']>fleet.maximum_new_pumps):return self.infeasible('INFEASIBLE_CAPITAL_BUDGET')
        m=gp.Model(tag,env=self.env)
        for key,value in {'Seed':0,'Threads':1,'MIPGap':0,'MIPGapAbs':0,'FeasibilityTol':1e-8,
                          'IntFeasTol':1e-8,'TimeLimit':60,'LogFile':str(self.output/'logs'/f'{tag}.log')}.items():m.setParam(key,value)
        y=m.addVars(pairs,vtype=GRB.BINARY,name='ready')
        x=m.addVars(triples,vtype=GRB.INTEGER,lb=0,name='deploy')
        n=m.addVar(vtype=GRB.INTEGER,lb=0,ub=fleet.maximum_new_pumps,name='new_pumps') if fleet else None
        setup=gp.quicksum(p.setup_cost[k]*y[k] for k in pairs)
        primary=gp.quicksum(p.probabilities[s]*p.benefit[s,j,i]*x[s,j,i] for s,j,i in triples)
        m.addConstr(setup<=p.setup_budget,name='readiness_budget_CU')
        if fleet:
            m.addConstr(fleet.purchase_price_hkd*n<=fleet.capital_budget_hkd,name='pump_capital_budget_HKD')
            if fixed:m.addConstr(n==fixed['n'],name='fix_first_stage_procurement')
        for j,i in pairs:
            if i not in allowed:m.addConstr(y[j,i]==0,name=f'ablation_{j}_{i}')
            if fixed:m.addConstr(y[j,i]==fixed['y'][j,i],name=f'fix_readiness_{j}_{i}')
        for s in p.scenarios:
            for coefficient,capacity in RESOURCE_PAIRS:
                m.addConstr(gp.quicksum(getattr(p,coefficient)[s,j,i]*x[s,j,i] for j,i in pairs)
                            <=getattr(p,capacity)[s],name=f'{capacity}_{s}')
            for j,i in pairs:
                m.addConstr(x[s,j,i]<=p.upper_bound[s,j,i]*y[j,i],name=f'link_{s}_{j}_{i}')
            if fleet:
                m.addConstr(gp.quicksum(x[s,j,'Drainage'] for j in p.locations)<=fleet.existing_stock+n,
                            name=f'shared_pump_stock_{s}')
                for j in p.locations:
                    if j not in fleet.accessible_locations:m.addConstr(x[s,j,'Drainage']==0,name=f'pump_access_{s}_{j}')
        m.ModelSense=GRB.MAXIMIZE
        m.setObjectiveN(primary,0,priority=4,abstol=1e-8,reltol=0,name='benefit')
        if fleet:m.setObjectiveN(-n,1,priority=3,abstol=1e-8,reltol=0,name='minimum_procurement_among_optima')
        m.setObjectiveN(-setup,2,priority=2,abstol=1e-8,reltol=0,name='minimum_readiness_among_optima')
        m.setObjectiveN(-gp.quicksum(2**k*y[pair] for k,pair in enumerate(pairs)),3,
                        priority=1,abstol=1e-8,reltol=0,name='deterministic_readiness_tie_break')
        m.optimize()
        if m.Status!=GRB.OPTIMAL:
            status=m.Status;m.dispose();raise RuntimeError(f'{tag}: solver status {status}; inspect saved log')
        yy={k:int(round(y[k].X)) for k in pairs};xx={k:int(round(x[k].X)) for k in triples}
        nn=int(round(n.X)) if fleet else 0
        assert all(abs(y[k].X-yy[k])<TOL for k in pairs)
        assert all(abs(x[k].X-xx[k])<TOL and xx[k]>=0 for k in triples)
        assert all(xx[s,j,i]<=p.upper_bound[s,j,i]*yy[j,i]+TOL for s,j,i in triples)
        assert all(yy[j,i]==0 for j,i in pairs if i not in allowed)
        if fixed:assert yy==fixed['y'] and (not fleet or nn==fixed['n'])
        resources=[{'scenario':'First Stage','resource':'readiness_CU','used':sum(p.setup_cost[k]*yy[k] for k in pairs),'capacity':p.setup_budget}]
        if fleet:
            assert abs(n.X-nn)<TOL
            resources.append({'scenario':'First Stage','resource':'capital_HKD','used':fleet.purchase_price_hkd*nn,'capacity':fleet.capital_budget_hkd})
        scene_rows=[]
        for s in p.scenarios:
            for coefficient,capacity in RESOURCE_PAIRS:
                resources.append({'scenario':s,'resource':coefficient,'used':sum(getattr(p,coefficient)[s,j,i]*xx[s,j,i] for j,i in pairs),'capacity':getattr(p,capacity)[s]})
            if fleet:
                resources.append({'scenario':s,'resource':'shared_pump_stock','used':sum(xx[s,j,'Drainage'] for j in p.locations),'capacity':fleet.existing_stock+nn})
                assert all(xx[s,j,'Drainage']==0 for j in p.locations if j not in fleet.accessible_locations)
            for j in p.locations:
                scene_rows.append({'scenario':s,'location':j,'probability':p.probabilities[s],
                    'packages':sum(xx[s,j,i] for i in p.interventions),
                    'pumps':xx[s,j,'Drainage'],'benefit':sum(p.benefit[s,j,i]*xx[s,j,i] for i in p.interventions)})
        for r in resources:
            r['slack']=r['capacity']-r['used'];assert r['slack']>=-TOL
            r['utilization']=r['used']/r['capacity'] if r['capacity'] else None
        objective=sum(p.probabilities[s]*p.benefit[s,j,i]*xx[s,j,i] for s,j,i in triples)
        assert abs(objective-m.ObjVal)<TOL
        result={'status':'OPTIMAL','feasible':True,'objective':objective,'new_pumps':nn,
            'capital_used_hkd':fleet.purchase_price_hkd*nn if fleet else None,
            'plan':';'.join(f'{j}/{i}' for j,i in pairs if yy[j,i]),'setup_used':resources[0]['used'],
            'y':[{'location':j,'intervention':i,'y':yy[j,i]} for j,i in pairs],
            'x':[{'scenario':s,'location':j,'intervention':i,'x':xx[s,j,i]} for s,j,i in triples],
            'resources':resources,'location_scenarios':scene_rows,'validation_passed':True,'runtime':m.Runtime}
        self.audit.append({'tag':tag,'status':'OPTIMAL','objective':objective,'runtime':m.Runtime,'validation_passed':True})
        m.dispose();return result

    @staticmethod
    def infeasible(status):return {'status':status,'feasible':False,'objective':None}

    @staticmethod
    def policy(solution):
        return {'y':{(r['location'],r['intervention']):r['y'] for r in solution['y']},'n':solution['new_pumps']}

    @staticmethod
    def expected(p):
        updates={'scenarios':('EV',),'probabilities':{'EV':1.0}}
        for name in ('deploy_cost','labour','equipment','supply','upper_bound','benefit'):
            updates[name]={('EV',j,i):sum(p.probabilities[s]*getattr(p,name)[s,j,i] for s in p.scenarios) for j in p.locations for i in p.interventions}
        for _,name in RESOURCE_PAIRS:updates[name]={'EV':sum(p.probabilities[s]*getattr(p,name)[s] for s in p.scenarios)}
        return replace(p,**updates)

    def evaluate(self,p,config,baseline_policy=None,fleet=None,allowed=None):
        cid=config['id'];rp=self.solve(p,cid+'_rp',fleet,allowed)
        ws={s:self.solve(replace(p,scenarios=(s,),probabilities={s:1.0}),cid+'_ws_'+s,fleet,allowed) for s in p.scenarios}
        ws_value=sum(p.probabilities[s]*ws[s]['objective'] for s in p.scenarios)
        ev=self.solve(self.expected(p),cid+'_ev',fleet,allowed)
        eev=self.solve(p,cid+'_eev',fleet,allowed,self.policy(ev))
        assert eev['feasible'] and ws_value+TOL>=rp['objective']>=eev['objective']-TOL
        fixed=self.solve(p,cid+'_fixed',fleet,allowed,baseline_policy) if baseline_policy else rp
        summary={'id':cid,'experiment':config['experiment'],'factor':config.get('factor',''),'level':config.get('level',''),
            'u_mode':config.get('u_mode','derived'),'rp':rp['objective'],'ws':ws_value,'ev':ev['objective'],
            'eev':eev['objective'],'vss':rp['objective']-eev['objective'],'evpi':ws_value-rp['objective'],
            'plan':rp['plan'],'new_pumps':rp['new_pumps'],'capital_used_hkd':rp['capital_used_hkd'],'setup_used':rp['setup_used'],
            'baseline_policy_feasible':fixed['feasible'],'baseline_policy_value':fixed['objective'],
            'regret':rp['objective']-fixed['objective'] if fixed['feasible'] else None,'checks_passed':True}
        assert summary['regret'] is None or summary['regret']>=-TOL
        payload={'config':config,'parameters':_parameters_to_json(p),'fleet':asdict(fleet) if fleet else None,
            'summary':summary,'rp':rp,'ws':ws,'ev':ev,'eev':eev,'fixed_baseline':fixed}
        (self.output/'solutions'/f'{cid}.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2,allow_nan=False))
        return payload
