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
    return {'objective':-float(result.fun),'rounded_objective':-float(objective @ np.rint(result.x)), 'max_integrality_error':float(np.max(np.abs(result.x-np.rint(result.x)))), 'max_rounded_constraint_violation':float(np.max(np.array(rows) @ np.rint(result.x)-np.array(rhs)))}
