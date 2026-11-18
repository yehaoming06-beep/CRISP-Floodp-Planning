from paper_plot_style import *
fig,axs=plt.subplots(1,3,figsize=(9,3.2),layout='constrained')
for ax,k,label in zip(axs,['rp','vss','evpi'],['RP','VSS','EVPI']):
    vals=[[x[k] for x in DATA['summary'] if x['experiment']=='joint' and x['u_mode']==m] for m in ['derived','availability']]
    bp=ax.boxplot(vals,tick_labels=['Derived U','Extra limit'],patch_artist=True,widths=.5,whis=(0,100),showfliers=False)
    for box,color in zip(bp['boxes'],COLORS[:2]):box.set_facecolor(color);box.set_alpha(.3)
    for line in bp['medians']:line.set_color('#222222')
    ax.set_ylabel(f'{label} (model score)');ax.tick_params(axis='x',labelrotation=15)
save(fig,'fig05_uncertainty')
