from paper_plot_style import *
labels={'benefit_Drainage':'Drainage benefit','benefit_Barrier':'Barrier benefit','benefit_Warning':'Warning benefit',
    'weight_w_L':'Life weight','weight_w_P':'Property weight','weight_w_R':'Recovery weight','setup_cost':'Readiness cost',
    'deploy_cost':'Deployment cost','probability_Extreme':'Extreme probability','beta_location2':'Tai O2 modifier',
    'availability_U':'Additional availability bound','both_costs':'Both CU costs','deploy_cost_fixed_U':'Deployment cost (frozen U)','alpha_all':'Scenario multipliers'}
base=DATA['primary']['summary']['rp'];pairs=[]
for factor in labels:
    r=[x for x in DATA['oat'] if x['factor']==factor]
    a=next(x['rp'] for x in r if x['level']==.8)-base;b=next(x['rp'] for x in r if x['level']==1.2)-base
    pairs.append((factor,a,b))
pairs.sort(key=lambda x:max(abs(x[1]),abs(x[2])))
fig,ax=plt.subplots(figsize=(7,4.6),layout='constrained')
for y,(name,a,b) in enumerate(pairs):
    ax.plot([a,b],[y,y],color='#B8C2CC',lw=6,solid_capstyle='butt')
    ax.plot(a,y,'o',color=COLORS[0],ms=5,label='0.8×' if y==0 else None)
    ax.plot(b,y,'s',color=COLORS[1],ms=5,label='1.2×' if y==0 else None)
ax.set_yticks(range(len(pairs)),[labels[x[0]] for x in pairs]);ax.axvline(0,color='#444444',lw=.8)
ax.set_xlabel('Change in reoptimized RP (model score)');ax.legend(frameon=False,loc='lower right')
save(fig,'fig04_oat')
