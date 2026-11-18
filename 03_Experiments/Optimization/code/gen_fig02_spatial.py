from paper_plot_style import *
r=[x for x in DATA['spatial'] if 'delta' in x]
delta=sorted(set(x['delta'] for x in r));cost=sorted(set(x['cost1'] for x in r))
grid=np.array([[next(x['rp'] for x in r if x['delta']==d and x['cost1']==c) for c in cost] for d in delta])
fig,ax=plt.subplots(figsize=(5.6,4.2),layout='constrained')
im=ax.imshow(grid,origin='lower',aspect='auto',cmap='Blues',vmin=grid.min(),vmax=grid.max())
ax.set_xticks(range(5),[f'{c:.1f}' for c in cost]);ax.set_yticks(range(5),[f'{d:+.1f}' for d in delta])
ax.set_xlabel('Tai O1 cost multiplier c (Tai O2: 2 − c)');ax.set_ylabel('Location-benefit contrast δ (β1=1+δ, β2=1−δ)')
for i in range(5):
    for j in range(5):ax.text(j,i,f'{grid[i,j]:.1f}',ha='center',va='center',fontsize=9,color='white' if grid[i,j]>(grid.min()+grid.max())/2 else '#222222')
fig.colorbar(im,ax=ax,label='RP benefit (model score)',shrink=.9)
save(fig,'fig02_spatial')
