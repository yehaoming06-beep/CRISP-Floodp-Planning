from paper_plot_style import *
r=DATA['fleet'];x=[a['level'] for a in r]
fig,ax=plt.subplots(1,2,figsize=(9,3.3),layout='constrained')
for k,label,color,marker in [('rp','RP',COLORS[0],'o'),('ws','WS',COLORS[2],'^'),('eev','EEV (minimum-purchase EV policy)',COLORS[1],'s')]:
    ax[0].plot(x,[a[k] for a in r],label=label,color=color,marker=marker,ms=4,lw=1.3)
ax[0].set_xlabel('Maximum new pumps allowed');ax[0].set_ylabel('Expected benefit (model score)');ax[0].legend(frameon=False,loc='lower right',fontsize=8)
ties={a['case']:a for a in DATA['ties']}
lo=[];hi=[]
for n in x:
    t=ties['mobile_baseline' if n==2 else f'fleet_{n:02}']
    lo.append(t['minimum_VSS_over_EV_optima']);hi.append(t['maximum_VSS_over_EV_optima'])
ax[1].fill_between(x,lo,hi,color=COLORS[0],alpha=.16,label='Range over EV-optimal policies')
ax[1].plot(x,[a['vss'] for a in r],color=COLORS[1],marker='s',ms=4,label='Selected minimum-purchase policy')
ax[1].plot(x,lo,color=COLORS[0],ls=':',lw=1)
ax[1].set_xlabel('Maximum new pumps allowed');ax[1].set_ylabel('VSS (model score)');ax[1].set_ylim(bottom=0);ax[1].legend(frameon=False,fontsize=8,loc='upper right')
for i,a in enumerate(ax):
    a.text(-.12,1.03,f'({chr(97+i)})',transform=a.transAxes)
    a.set_xticks([0,2,4,6,8,12,20])
save(fig,'fig01_inventory')
