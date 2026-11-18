from paper_plot_style import *
r=sorted([x for x in DATA['summary'] if x['experiment']=='ablation'],key=lambda x:x['id'])
labels=['None','D','B','D+B','W','D+W','B+W','D+B+W']
fig,ax=plt.subplots(figsize=(6.5,3.2),layout='constrained')
bars=ax.bar(labels,[x['rp'] for x in r],color=COLORS[0],width=.65)
for bar,v in zip(bars,r):ax.text(bar.get_x()+bar.get_width()/2,v['rp']+10,f'{v["rp"]:.1f}',ha='center',va='bottom',fontsize=8)
ax.set_ylim(0,max(x['rp'] for x in r)*1.14);ax.set_ylabel('RP benefit (model score)');ax.set_xlabel('Available measures: D=Drainage, B=Barrier, W=Warning')
save(fig,'fig03_ablation')
