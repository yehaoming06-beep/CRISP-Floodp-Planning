"""All figures read saved tables; pass --figure 01 to regenerate a single figure."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]
INPUTS=ROOT/"01_Data/Events"
COLORS=['#0072B2','#D55E00','#009E73']
NAMES=['rainfall','sea_level','storm_surge']
LABELS=['Rainfall','Sea level','Storm surge']
SCENARIOS=['Moderate','Severe','Extreme']
plt.rcParams.update({'font.family':'serif','font.serif':['DejaVu Serif'],
 'font.size':10,'axes.labelsize':10,'xtick.labelsize':8,'ytick.labelsize':8,
 'legend.fontsize':8,'axes.spines.top':False,'axes.spines.right':False,
 'savefig.dpi':300,'pdf.fonttype':42,'ps.fonttype':42})

def interval(ax,frame,cols,base,labels,methods=('event_bootstrap','year_bootstrap')):
    offsets=np.linspace(-.13,.13,len(methods))
    for m,off,col,lab in zip(methods,offsets,COLORS,['Event bootstrap','Year bootstrap']):
        vals=frame[frame.method==m]
        q=np.quantile(vals[cols].to_numpy(),[.025,.5,.975],axis=0)
        # Endpoints are drawn directly; the original point need not be inside the interval.
        yy=np.arange(len(cols))+off
        ax.hlines(yy,q[0],q[2],color=col,lw=2)
        ax.scatter(q[1],yy,color=col,s=24,label=lab,zorder=3)
    ax.scatter(base,np.arange(len(cols)),marker='D',facecolor='white',edgecolor='black',s=30,label='Baseline',zorder=4)
    ax.set_yticks(np.arange(len(cols)),labels); ax.set_ylim(len(cols)-.5,-.5)

def draw(which,out):
    t=out/'tables'; fdir=out/'figures'; fdir.mkdir(exist_ok=True)
    events=pd.read_csv(t/'baseline_events.csv').sort_values('H')
    weights=pd.read_csv(t/'baseline_weights.csv'); scenarios=pd.read_csv(t/'baseline_scenarios.csv')
    runs=pd.read_csv(t/'resample_runs.csv'); captions={}
    def save(fig,name,caption):
        fig.savefig(fdir/(name+'.pdf'),bbox_inches='tight',pad_inches=.08)
        fig.savefig(fdir/(name+'.png'),bbox_inches='tight',pad_inches=.08)
        plt.close(fig); captions[name]=caption
    if which in ('all','01'):
        fig,ax=plt.subplots(figsize=(7.2,3.8),layout='constrained')
        for j,s in enumerate(SCENARIOS):
            ix=np.flatnonzero(events.scenario.to_numpy()==s)
            ax.scatter(ix,events.H.iloc[ix],color=COLORS[j],marker=['o','s','^'][j],label=s,s=38)
        c=scenarios.center.to_numpy()
        for tau in (c[:-1]+c[1:])/2: ax.axhline(tau,color='.4',ls='--',lw=1)
        ax.set_xticks(np.arange(len(events)),events.event_id,rotation=90)
        ax.set_xlabel('Event ordered by baseline score'); ax.set_ylabel('Composite severity score H')
        ax.legend(loc='upper left',frameon=False)
        save(fig,'01_baseline_scores','23條原始事件，依基線H排序。虛線為原K=3中心中點閾值；固定全樣本Min-Max與CRITIC。Moderate/Severe/Extreme是相對等級，不是物理洪水閾值。')
    if which in ('all','02'):
        fig,ax=plt.subplots(figsize=(7.2,3.3),layout='constrained')
        interval(ax,runs,['w_'+q for q in NAMES],weights.weight.to_numpy(),LABELS)
        ax.set_xlabel('CRITIC weight: median and 2.5–97.5% resampling range'); ax.set_xlim(.15,.57)
        ax.legend(loc='lower right',frameon=False)
        save(fig,'02_weight_ranges','事件bootstrap B=3000與年份bootstrap B=2000，抽樣單位分別為事件與整個年份；每次重估歸一化、權重及K=3。點為中位數，線為逐項95%經驗分位範圍，空心菱形為23事件基線；不是同時信賴區間。')
    if which in ('all','03'):
        fig,ax=plt.subplots(figsize=(7.2,3.8),layout='constrained')
        methods=['event_bootstrap','year_bootstrap','subsample80','fixed_preprocess']
        data=[runs.loc[runs.method==m,'ARI'].to_numpy() for m in methods]
        vp=ax.violinplot(data,positions=range(4),showextrema=False)
        for body in vp['bodies']: body.set_facecolor(COLORS[0]); body.set_alpha(.2)
        ax.boxplot(data,positions=range(4),widths=.2,showfliers=False,whis=(2.5,97.5),patch_artist=False)
        ax.set_xticks(range(4),['Event\nB=3000','Year\nB=2000','18/23 subsample\nB=1000','Fixed preprocessing\nB=3000'])
        ax.set_ylim(0,1.04); ax.set_ylabel('Adjusted Rand index on all 23 original events')
        save(fig,'03_partition_stability','共同23行投射分類與全樣本基線比較的ARI。箱線鬚為2.5%及97.5%分位數，箱為四分位距；小提琴僅平滑顯示分布。前三組重估完整流程；最後一組凍結Min-Max與權重，只重抽事件並重擬合K=3。同一事件抽樣索引用於第一與第四組。ARI不是預測準確率。')
    if which in ('all','04'):
        fig,axs=plt.subplots(1,2,figsize=(7.2,3.7),layout='constrained',sharex=True,sharey=True)
        for ax,prefix in zip(axs,['p_train_','p_fixed_label_']):
            interval(ax,runs,[prefix+s for s in SCENARIOS],scenarios.probability.to_numpy(),SCENARIOS)
            ax.set_xlabel('Scenario frequency')
        axs[0].set_xlabel('Refit scenario frequency')
        axs[1].set_xlabel('Fixed-label scenario frequency')
        handles,labels=axs[1].get_legend_handles_labels()
        fig.legend(handles,labels,loc='outside lower center',ncol=3,frameon=False)
        axs[0].set_xlim(0,.85)
        save(fig,'04_scenario_frequencies','左圖：每次完整流程在重抽樣訓練資料內的場景頻率，包含標籤及樣本組成變化；右圖：沿用原分類，只改抽樣組成。事件B=3000、年份B=2000；點為中位數，線為95%經驗分位範圍，菱形為原頻率。兩面板估計對象不同，均非年發生概率。')
    if which in ('all','05'):
        memberships=pd.read_csv(t/'event_membership_stability.csv')
        fig,axs=plt.subplots(1,2,figsize=(7.2,7.8),layout='constrained',sharey=True)
        for ax,m in zip(axs,['event_bootstrap','year_bootstrap']):
            a=memberships[memberships.method==m].set_index('event_id').loc[events.event_id]
            mat=a[['p_'+s for s in SCENARIOS]].to_numpy()
            im=ax.imshow(mat,vmin=0,vmax=1,cmap='Blues',aspect='auto')
            for i in range(23):
                for j in range(3): ax.text(j,i,f'{mat[i,j]:.2f}',ha='center',va='center',fontsize=8,color='white' if mat[i,j]>.6 else 'black')
            ax.set_xticks(range(3),SCENARIOS,rotation=25,ha='right'); ax.set_yticks(range(23),events.event_id)
            ax.set_xlabel('Refitted severity class'); ax.spines[['left','bottom']].set_visible(False)
        axs[0].set_ylabel('Event ordered by baseline score')
        fig.colorbar(im,ax=axs,shrink=.6,label='Classification frequency')
        save(fig,'05_event_membership','左：3000次事件bootstrap；右：2000次年份bootstrap。每格為原事件在各次重新訓練流程下被投射至該等級的比例，每行合計1，分母為成功擬合數；包括入袋與OOB情況。逐事件OOB分母及一致率另存CSV。顏色表示分類穩定性，不是災害發生概率。')
    if which in ('all','06'):
        fig,axs=plt.subplots(1,2,figsize=(7.2,4.5),layout='constrained')
        for ax,m in zip(axs,['event_bootstrap','year_bootstrap']):
            a=pd.read_csv(t/(m+'_coassignment.csv'),index_col=0).loc[events.event_id,events.event_id]
            im=ax.imshow(a,vmin=0,vmax=1,cmap='viridis')
            ax.set_xticks(range(23),events.event_id,rotation=90,fontsize=6)
            ax.set_yticks(range(23),events.event_id,fontsize=6)
            ax.set_xlabel('Event ordered by baseline score')
        fig.colorbar(im,ax=axs,shrink=.6,label='Co-clustering frequency')
        save(fig,'06_coassignment','左為事件B=3000，右為年份B=2000。每格表示兩條原始事件在重估完整流程後投射至同一群的比例。使用共同23行，並非只比較重抽樣中出現的事件；不依賴標籤名稱。對角線固定為1。')
    if which in ('all','07'):
        k=pd.read_csv(t/'k_diagnostics.csv'); kb=pd.read_csv(t/'k_bootstrap_runs.csv')
        winner=kb.loc[kb.groupby('replicate').silhouette.idxmax(),'k'].value_counts().reindex(range(2,6),fill_value=0)
        fig,axs=plt.subplots(1,3,figsize=(7.2,3.2),layout='constrained')
        axs[0].plot(k.k,k.sse,'o-',color=COLORS[0]); axs[0].set_ylabel('Within-cluster SSE')
        axs[1].plot(k.k,k.silhouette,'s-',color=COLORS[1]); axs[1].set_ylabel('Silhouette coefficient')
        axs[2].bar(winner.index,winner.to_numpy()/len(kb.replicate.unique()),color=COLORS[2]); axs[2].set_ylabel('Bootstrap selection fraction')
        for ax in axs: ax.set_xlabel('Number of clusters K'); ax.set_xticks(range(2,7))
        axs[0].set_xticks(range(1,7)); axs[2].set_xticks(range(2,6)); axs[2].set_ylim(0,.55)
        save(fig,'07_k_diagnostics','左及中：固定23事件基線分數，K=1—6的SSE、K=2—6的輪廓系數。右：前500次事件bootstrap完整重估分數，在K=2—5中選輪廓系數最高者的比例；n_init=50、seed=42。抽樣含重複行會改變輪廓系數，不可視為外部驗證或真實類別數檢定。')
    if which in ('all','08'):
        fig,axs=plt.subplots(2,1,figsize=(7.2,5.3),layout='constrained',sharey=True)
        for ax,m,key in zip(axs,['leave_one_event','leave_one_year'],['deleted_event','deleted_year']):
            g=runs[runs.method==m]
            labs=g[key].astype(str) if key=='deleted_event' else g[key].astype(int).astype(str)
            ax.scatter(range(len(g)),g.ARI,color=COLORS[0]); ax.vlines(range(len(g)),0,g.ARI,color=COLORS[0],lw=1)
            ax.set_xticks(range(len(g)),labs,rotation=90 if key=='deleted_event' else 0)
            ax.set_ylabel('ARI on all 23 events'); ax.set_ylim(0,1.05)
            ax.set_xlabel('Deleted event' if key=='deleted_event' else 'Deleted year')
        save(fig,'08_deletion_influence','上：23次逐事件刪除，訓練n=22；下：9次逐年刪除，訓練樣本量依年份不同。每次重估完整流程，再投射共同23條記錄並與全樣本基線比較ARI。這是影響診斷，沒有隨機抽樣信賴區間；被刪資料的投射也計入ARI。')
    if which in ('all','09'):
        init=pd.read_csv(t/'initialization_runs.csv'); alt=pd.read_csv(t/'competing_partitions.csv')
        alt=alt[alt.self_consistent].head(8)
        fig,axs=plt.subplots(1,2,figsize=(7.2,3.6),layout='constrained')
        for j,ni in enumerate([1,50]):
            vals=init.loc[init.n_init==ni,'ARI']
            axs[0].hist(vals,bins=np.linspace(0,1.0001,11),histtype='step',lw=2,color=COLORS[j],label=f'n_init={ni}')
        axs[0].set_xlabel('ARI to baseline'); axs[0].set_ylabel('Seed count (200 per setting)'); axs[0].legend(frameon=False)
        labels=['/'.join(str(int(r[c])) for c in ['count_Moderate','count_Severe','count_Extreme']) for _,r in alt.iterrows()]
        axs[1].bar(range(len(alt)),alt.sse_gap,color=COLORS[0]); axs[1].set_xticks(range(len(alt)),labels,rotation=45,ha='right')
        axs[1].set_ylabel('SSE minus global minimum'); axs[1].set_xlabel('Competing partition sizes (ordered classes)')
        save(fig,'09_initialization_and_competitors','左：固定原23事件H，以種子0—199比較單次與50次初始化，n_init=50為原流程。右：對排序H枚舉所有231組連續三分切點（C(22,2)），列SSE最低的8種切分與全局最低值的差；切分大小不代表相同事件集合。近似等價切分提示離散分類可能對樣本擾動敏感。')
    if which in ('all','10'):
        fig,axs=plt.subplots(1,3,figsize=(7.2,3.6),layout='constrained',sharey=True)
        for ax,q,label,unit in zip(axs,NAMES,LABELS,['mm/day','mCD','m']):
            interval(ax,runs,['rep_'+s+'_'+q for s in SCENARIOS],scenarios['mean_'+q].to_numpy(),SCENARIOS)
            ax.set_xlabel(label+' ('+unit+')')
        handles,labels=axs[2].get_legend_handles_labels()
        fig.legend(handles,labels,loc='outside lower center',ncol=3,frameon=False)
        save(fig,'10_representative_hazards','每次完整重擬合後，按中心順序對齊的三類訓練資料原量綱平均值。事件B=3000與年份B=2000；點為中位數，線為95%經驗分位範圍，菱形為基線。降雨是±2日窗口最大日總雨量（mm/day），不是一小時雨強；三項最大值未必同步發生，不能當作物理聯合事件。')
    capfile=fdir/'captions.json'
    previous=json.loads(capfile.read_text()) if capfile.exists() else {}
    previous.update(captions); capfile.write_text(json.dumps(previous,ensure_ascii=False,indent=2))
    tex=[]
    for name,caption in sorted(previous.items()):
        tex.append('\\begin{figure}[htbp]\n\\centering\n\\includegraphics[width=\\linewidth]{figures/'+name+'.pdf}\n\\caption{'+caption+'}\n\\end{figure}\n')
    (fdir/'latex_includes.tex').write_text('\n'.join(tex),encoding='utf-8')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--figure',default='all'); ap.add_argument('--output',type=Path,default=ROOT/'04_Results/Scenario_Stability')
    args=ap.parse_args(); draw(args.figure,args.output.resolve())
