"""Independent finite enumeration of all feasible first-stage/recourse decisions.
Uses input workbook parser only; neither the Gurobi builder nor saved solutions
are imported. Every feasible readiness mask, pump count and deployment vector
is considered, including all EV-optimal first-stage policies.
"""
from itertools import product
from functools import lru_cache
from dataclasses import replace
import math

CAPS=(('deploy_cost','operating_budget'),('labour','labour_capacity'),('equipment','equipment_capacity'),('supply','supply_capacity'))

def expected(p):
    updates={'scenarios':('EV',),'probabilities':{'EV':1.0}}
    for k in ('deploy_cost','labour','equipment','supply','upper_bound','benefit'):
        updates[k]={('EV',j,i):sum(p.probabilities[s]*getattr(p,k)[s,j,i] for s in p.scenarios) for j in p.locations for i in p.interventions}
    for _,k in CAPS:
        updates[k]={'EV':sum(p.probabilities[s]*getattr(p,k)[s] for s in p.scenarios)}
    return replace(p,**updates)

def enumerate_case(p,fleet=None):
    pairs=[(j,i) for j in p.locations for i in p.interventions]
    feasible_masks=[mask for mask in range(1<<len(pairs)) if sum(p.setup_cost[j,i] for k,(j,i) in enumerate(pairs) if mask&(1<<k))<=p.setup_budget+1e-8]
    ns=range(math.floor(fleet.capital_budget_hkd/fleet.purchase_price_hkd+1e-10)+1) if fleet else [0]
    counters={'first_stage_policies':len(feasible_masks)*len(ns),'recourse_vectors_considered':0,'recourse_vectors_feasible':0}
    def values(q):
        result={}
        for n in ns:
            for mask in feasible_masks:
                active=[pair for k,pair in enumerate(pairs) if mask&(1<<k)]
                for s in q.scenarios:
                    ranges=[]
                    for j,i in active:
                        bound=math.floor(q.upper_bound[s,j,i]+1e-10)
                        if fleet and i=='Drainage':
                            bound=min(bound,fleet.existing_stock+n) if j in fleet.accessible_locations else 0
                        ranges.append(range(bound+1))
                    best=-math.inf;best_x=None
                    for vector in product(*ranges):
                        counters['recourse_vectors_considered']+=1
                        if fleet and sum(v for (j,i),v in zip(active,vector) if i=='Drainage')>fleet.existing_stock+n:continue
                        if any(sum(getattr(q,c)[s,j,i]*v for (j,i),v in zip(active,vector))>getattr(q,cap)[s]+1e-8 for c,cap in CAPS):continue
                        counters['recourse_vectors_feasible']+=1
                        objective=sum(q.benefit[s,j,i]*v for (j,i),v in zip(active,vector))
                        if objective>best+1e-8:best=objective;best_x=vector
                    result[n,mask,s]=best
        return result
    v=values(p);e=expected(p);evv=values(e)
    def choose(objectives):
        optimum=max(objectives.values())
        policies=[key for key,value in objectives.items() if abs(value-optimum)<=1e-8]
        def tie(key):
            n,mask=key
            setup=sum(p.setup_cost[j,i] for k,(j,i) in enumerate(pairs) if mask&(1<<k))
            return n,setup,mask
        return optimum,min(policies,key=tie),policies
    rp_obj={(n,mask):sum(p.probabilities[s]*v[n,mask,s] for s in p.scenarios) for n in ns for mask in feasible_masks}
    ev_obj={(n,mask):evv[n,mask,'EV'] for n in ns for mask in feasible_masks}
    rp,rp_policy,_=choose(rp_obj);ev,ev_policy,ev_policies=choose(ev_obj)
    ws=sum(p.probabilities[s]*max(v[n,mask,s] for n in ns for mask in feasible_masks) for s in p.scenarios)
    n,mask=ev_policy;eev=rp_obj[n,mask]
    return {'rp':rp,'ws':ws,'ev':ev,'eev':eev,'vss':rp-eev,'evpi':ws-rp,
            'rp_policy':list(rp_policy),'ev_policy':list(ev_policy),
            'rp_plan':';'.join(f'{j}/{i}' for k,(j,i) in enumerate(pairs) if rp_policy[1]&(1<<k)),
            'ev_optimal_first_stage_policies':[{'n':key[0],'mask':key[1],'eev':rp_obj[key]} for key in ev_policies],
            'eev_optimal_policy_range':[min(rp_obj[key] for key in ev_policies),max(rp_obj[key] for key in ev_policies)],
            'counters':counters,'method':'exhaustive finite enumeration; original model builder and saved outputs not imported'}
