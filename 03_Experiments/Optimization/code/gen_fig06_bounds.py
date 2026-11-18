from paper_plot_style import *
fig,axs=plt.subplots(1,3,figsize=(9,3.1),layout='constrained')
for ax,factor in zip(axs,['Labour','Equipment','Supply']):
    r=sorted([x for x in DATA['corrected'] if x['factor']==factor],key=lambda x:x['level'])
    for k,label,color,marker in [('old_rp','Frozen U',COLORS[1],'s'),('corrected_rp','Recomputed U',COLORS[0],'o')]:
        ax.plot([x['level'] for x in r],[x[k] for x in r],label=label,color=color,marker=marker,ms=4,lw=1.2)
    ax.set_xlabel(f'{factor} capacity multiplier');ax.set_ylabel('RP benefit (model score)')
axs[0].legend(frameon=False,fontsize=8)
save(fig,'fig06_bounds')
