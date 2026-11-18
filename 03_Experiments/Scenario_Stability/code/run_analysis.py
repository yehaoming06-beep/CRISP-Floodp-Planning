"""Frozen-data stability audit. Run from any working directory; never writes source files."""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import itertools
import json
import platform
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.cluster import KMeans
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import (adjusted_rand_score, silhouette_score,
                             calinski_harabasz_score, davies_bouldin_score)
from threadpoolctl import threadpool_limits

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
INPUTS=ROOT/"01_Data/Events"
NAMES = ['rainfall', 'sea_level', 'storm_surge']
SCENARIOS = ['Moderate', 'Severe', 'Extreme']
COLS = ['event_window_max_daily_rainfall_mm', 'maximum_sea_level_mCD',
        'maximum_storm_surge_m']

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def dump(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')

def critic(x, ddof=0):
    lo, span = x.min(0), np.ptp(x, axis=0)
    if np.any(np.isclose(span, 0)):
        raise ValueError('constant_indicator')
    z = (x-lo)/span
    corr = np.corrcoef(z, rowvar=False)
    if not np.isfinite(corr).all():
        raise ValueError('undefined_correlation')
    std = z.std(0, ddof=ddof)
    conflict = (1-corr).sum(1)
    info = std*conflict
    if not np.isfinite(info).all() or np.isclose(info.sum(), 0):
        raise ValueError('zero_total_information')
    return lo, span, info/info.sum(), z, corr, std, conflict

def classify(h, centers):
    return np.searchsorted((centers[:-1]+centers[1:])/2, h, side='right')

def fit_h(h, k=3, seed=42, n_init=50):
    if len(np.unique(np.round(h, 14))) < k:
        raise ValueError('too_few_distinct_scores')
    with warnings.catch_warnings():
        warnings.simplefilter('error', ConvergenceWarning)
        m = KMeans(n_clusters=k, random_state=seed, n_init=n_init,
                   max_iter=300, algorithm='lloyd').fit(h[:, None])
    centers = np.sort(m.cluster_centers_.ravel())
    lab = classify(h, centers)
    if len(np.unique(lab)) != k:
        raise ValueError('empty_cluster')
    return centers, lab, float(np.sum((h-centers[lab])**2))

def fit(x, target, fixed=None, ddof=0):
    if fixed is None:
        lo, span, w, *_ = critic(x, ddof)
    else:
        lo, span, w = fixed
    h, he = ((x-lo)/span)@w, ((target-lo)/span)@w
    c, lab, sse = fit_h(h)
    return dict(lo=lo, span=span, w=w, h=h, he=he, centers=c, labels=lab,
                predicted=classify(he,c), sse=sse)

def exact_1d_three(h):
    """Exhaust all contiguous 3-group partitions: global 1D squared-error optimum."""
    s = np.sort(h)
    candidates = []
    for i,j in itertools.combinations(range(1,len(s)),2):
        groups = [s[:i],s[i:j],s[j:]]
        c = np.array([a.mean() for a in groups])
        candidates.append((sum(float(np.sum((a-a.mean())**2)) for a in groups),c))
    return min(candidates, key=lambda a:a[0])

def all_exact_three(h):
    """Vectorized prefix sums, independently auditing all Lloyd fits."""
    s=np.sort(h); n=len(s)
    cuts=np.array(list(itertools.combinations(range(1,n),2)))
    i,j=cuts.T
    a=np.r_[0,np.cumsum(s)]; b=np.r_[0,np.cumsum(s*s)]
    scores=(b[i]-a[i]**2/i + b[j]-b[i]-(a[j]-a[i])**2/(j-i)
            +b[n]-b[j]-(a[n]-a[j])**2/(n-j))
    centers=np.column_stack((a[i]/i,(a[j]-a[i])/(j-i),(a[n]-a[j])/(n-j)))
    return cuts, scores, centers

def wilson(n, total):
    z=1.959963984540054
    p=n/total
    mid=(p+z*z/(2*total))/(1+z*z/total)
    half=z*np.sqrt(p*(1-p)/total+z*z/(4*total*total))/(1+z*z/total)
    return mid-half,mid+half

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, default=ROOT/'04_Results/Scenario_Stability')
    ap.add_argument('--bootstrap',type=int,default=3000)
    ap.add_argument('--year-bootstrap',type=int,default=2000)
    ap.add_argument('--subsample',type=int,default=1000)
    ap.add_argument('--k-resamples',type=int,default=500)
    ap.add_argument('--seed',type=int,default=20261103)
    args=ap.parse_args()
    out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    t=out/'tables'; t.mkdir(exist_ok=True)
    raw=pd.read_csv(INPUTS/'model_input.csv')
    meta=pd.read_csv(INPUTS/'event_metadata.csv')
    assert len(raw)==23 and raw.event_id.is_unique
    meta=meta.set_index('event_id').loc[raw.event_id].reset_index()
    x=raw[COLS].to_numpy(float); n=len(x)
    assert np.isfinite(x).all()
    np.testing.assert_allclose(x,meta[COLS].to_numpy(float),rtol=0,atol=0)
    years=pd.to_datetime(meta.event_date).dt.year.to_numpy()
    unique_years=np.unique(years)
    ref=fit(x,x); y=ref['predicted']
    lo,span,w,z,corr,std,conflict=critic(x)
    weights=pd.DataFrame(dict(indicator=NAMES,minimum=lo,maximum=lo+span,
                             normalized_std=std,conflict=conflict,information=std*conflict,weight=w))
    weights.to_csv(t/'baseline_weights.csv',index=False)
    pd.DataFrame(corr,index=NAMES,columns=NAMES).to_csv(t/'correlations.csv')
    ev=meta[['event_id','event_name','event_date','rainfall_station','sea_level_station']].copy()
    ev[NAMES]=x; ev[['z_'+a for a in NAMES]]=z
    ev['H']=ref['h']; ev['scenario']=np.array(SCENARIOS)[y]; ev['label']=y
    ev['distance_to_nearest_threshold']=np.abs(ref['h'][:,None]-(ref['centers'][:-1]+ref['centers'][1:])/2).min(1)
    ev.to_csv(t/'baseline_events.csv',index=False)
    scen=[]
    for j,s in enumerate(SCENARIOS):
        count=int((y==j).sum()); a,b=wilson(count,n)
        row=dict(scenario=s,count=count,probability=count/n,center=ref['centers'][j],
                 wilson_low_fixed_labels=a,wilson_high_fixed_labels=b)
        row.update({f'mean_{q}':x[y==j,i].mean() for i,q in enumerate(NAMES)})
        scen.append(row)
    pd.DataFrame(scen).to_csv(t/'baseline_scenarios.csv',index=False)
    year_table=pd.crosstab(years,np.array(SCENARIOS)[y]).reindex(columns=SCENARIOS,fill_value=0)
    year_table.index.name='year'; year_table.to_csv(t/'year_counts.csv')
    oldw=pd.read_csv(INPUTS/'reference_indicators.csv')
    olde=pd.read_csv(INPUTS/'reference_events.csv')
    olds=pd.read_csv(INPUTS/'reference_scenarios.csv')
    exact_sse,exact_c=exact_1d_three(ref['h'])
    audit=dict(n=n,years=unique_years.tolist(),year_blocks=len(unique_years),
        max_abs_weight_error=float(np.max(np.abs(w-oldw.weight.to_numpy()))),
        max_abs_H_error=float(np.max(np.abs(ref['h']-olde.H_t.to_numpy()))),
        stored_label_matches=int(np.sum(ev.scenario.to_numpy()==olde.scenario.to_numpy())),
        max_abs_center_error=float(np.max(np.abs(ref['centers']-olds.cluster_center_mu.to_numpy()))),
        exact_global_sse=exact_sse,kmeans_sse=ref['sse'],
        global_label_ARI=float(adjusted_rand_score(y,classify(ref['h'],exact_c))),
        ddof_weight_max_abs_change=float(np.max(np.abs(critic(x,1)[2]-w))),
        ddof_std_ratio=float(critic(x,1)[5][0]/std[0]),
        thresholds=((ref['centers'][:-1]+ref['centers'][1:])/2).tolist(),
        rainfall_station_counts=meta.rainfall_station.value_counts().to_dict(),
        missing_numeric=int(np.isnan(x).sum()),
        duplicate_vectors=int(pd.DataFrame(x).duplicated().sum()))
    # Actual production implementation, evaluated without its writer/CLI.
    sys.path.insert(0,str(ROOT/'05_Code/Scenario_Pipeline/src'))
    from crisp_data_layer.config import load_config
    from crisp_data_layer.pipeline import run_data_layer
    original=run_data_layer(raw,load_config(ROOT/'05_Code/Scenario_Pipeline/config/fallback.yaml'))
    audit['production_weights_max_abs_error']=float(np.max(np.abs(w-original.indicator_diagnostics.weight.to_numpy())))
    audit['production_H_max_abs_error']=float(np.max(np.abs(ref['h']-original.event_results.H_t.to_numpy())))
    audit['production_labels_match']=bool(np.all(ev.scenario.to_numpy()==original.event_results.scenario.to_numpy()))
    assert audit['stored_label_matches']==n and audit['production_labels_match']
    assert audit['max_abs_weight_error']<1e-12 and abs(exact_sse-ref['sse'])<1e-12
    # Inspect publication tables as read-only data, preserving all cells in text.
    sheets={}
    for path in [INPUTS/'Table_X_CRITIC_Weights_of_Hazard_Indicators.xlsx',
                 INPUTS/'Table_X_Flood_Scenario_Classification.xlsx']:
        sheets[path.name]={name:frame.fillna('').astype(str).values.tolist()
                          for name,frame in pd.read_excel(path,sheet_name=None,header=None).items()}
    dump(out/'publication_table_cells.json',sheets)
    dump(out/'baseline_audit.json',audit)
    cuts,ss,cc=all_exact_three(ref['h'])
    alternatives=[]
    for rank,v in enumerate(np.argsort(ss)[:20]):
        i,j=cuts[v]
        alternatives.append(dict(rank=rank+1,count_Moderate=int(i),count_Severe=int(j-i),
            count_Extreme=int(n-j),sse=ss[v],sse_gap=ss[v]-ss.min(),
            self_consistent=bool(np.array_equal(classify(np.sort(ref['h']),cc[v]),np.r_[np.zeros(i),np.ones(j-i),np.full(n-j,2)])),
            ARI_to_baseline=adjusted_rand_score(y,classify(ref['h'],cc[v])),
            center_Moderate=cc[v,0],center_Severe=cc[v,1],center_Extreme=cc[v,2]))
    pd.DataFrame(alternatives).to_csv(t/'competing_partitions.csv',index=False)
    rows=[]
    for init in [1,50]:
        for seed in range(200):
            c,lab,sse=fit_h(ref['h'],seed=seed,n_init=init)
            rows.append(dict(n_init=init,seed=seed,ARI=adjusted_rand_score(y,lab),
                             same_label_fraction=np.mean(y==lab),sse=sse,
                             global_sse_gap=sse-exact_sse))
    pd.DataFrame(rows).to_csv(t/'initialization_runs.csv',index=False)
    kr=[]
    for k in range(1,7):
        c,lab,sse=fit_h(ref['h'],k=k)
        kr.append(dict(k=k,sse=sse,min_cluster_count=int(np.bincount(lab,minlength=k).min()),
            silhouette=silhouette_score(ref['h'][:,None],lab) if k>1 else np.nan,
            calinski_harabasz=calinski_harabasz_score(ref['h'][:,None],lab) if k>1 else np.nan,
            davies_bouldin=davies_bouldin_score(ref['h'][:,None],lab) if k>1 else np.nan))
    pd.DataFrame(kr).to_csv(t/'k_diagnostics.csv',index=False)
    rngs=[np.random.default_rng(s) for s in np.random.SeedSequence(args.seed).spawn(3)]
    event_indices=[rngs[0].integers(n,size=n) for _ in range(args.bootstrap)]
    block_indices=[]; block_year_draws=[]
    for _ in range(args.year_bootstrap):
        draw=rngs[1].choice(unique_years,size=len(unique_years),replace=True)
        block_year_draws.append(draw.tolist())
        block_indices.append(np.concatenate([np.flatnonzero(years==v) for v in draw]))
    sub_indices=[np.sort(rngs[2].choice(n,size=int(np.floor(.8*n)),replace=False)) for _ in range(args.subsample)]
    groups={'event_bootstrap':event_indices,'fixed_preprocess':event_indices,
            'year_bootstrap':block_indices,'subsample80':sub_indices,
            'leave_one_event':[np.delete(np.arange(n),i) for i in range(n)],
            'leave_one_year':[np.flatnonzero(years!=v) for v in unique_years]}
    dump(out/'resample_indices.json',dict(index_base=0,event_id_order=raw.event_id.tolist(),
          groups={k:[a.tolist() for a in v] for k,v in groups.items()},year_draws=block_year_draws))
    allrows=[]; failures=[]; success_counts={}; label_arrays={}; oob_arrays={}; h_arrays={}; kboot=[]
    for method,indices in groups.items():
        labs=[]; oobs=[]; hs=[]
        for b,ix in enumerate(indices):
            try:
                f=fit(x[ix],x,fixed=(lo,span,w) if method=='fixed_preprocess' else None)
                pred=f['predicted']; train=f['labels']
                cuts,ss,cc=all_exact_three(f['h'])
                opt=int(np.argmin(ss)); exact_pred=classify(f['he'],cc[opt])
                oob=~np.isin(np.arange(n),ix)
                row=dict(method=method,replicate=b,n_train=len(ix),n_unique=len(np.unique(ix)),
                         n_oob=int(oob.sum()),ARI=adjusted_rand_score(y,pred),
                         agreement=float(np.mean(pred==y)),
                         oob_agreement=float(np.mean(pred[oob]==y[oob])) if oob.any() else np.nan,
                         H_spearman=float(spearmanr(ref['h'],f['he']).statistic),sse=f['sse'],
                         top_weight=NAMES[int(f['w'].argmax())],
                         exact_sse=float(ss[opt]),lloyd_sse_gap=float(f['sse']-ss[opt]),
                         exact_projection_ARI=adjusted_rand_score(y,exact_pred),
                         lloyd_exact_ARI=adjusted_rand_score(pred,exact_pred),
                         omitted=';'.join(raw.event_id[oob].tolist()),
                         n_projected_outside_unit=int(np.sum(np.any(((x-f['lo'])/f['span']<0)|((x-f['lo'])/f['span']>1),axis=1))))
                for j,q in enumerate(NAMES):
                    row['w_'+q]=f['w'][j]
                for j,s in enumerate(SCENARIOS):
                    row['center_'+s]=f['centers'][j]
                    row['p_train_'+s]=float(np.mean(train==j))
                    row['p_project_'+s]=float(np.mean(pred==j))
                    row['p_fixed_label_'+s]=float(np.mean(y[ix]==j))
                    row['jaccard_'+s]=float(np.sum((pred==j)&(y==j))/np.sum((pred==j)|(y==j)))
                    for c,q in enumerate(NAMES):
                        row['rep_'+s+'_'+q]=float(x[ix][train==j,c].mean())
                row['tau1'],row['tau2']=(f['centers'][:-1]+f['centers'][1:])/2
                if method=='leave_one_event': row['deleted_event']=raw.event_id[b]
                if method=='leave_one_year': row['deleted_year']=int(unique_years[b])
                allrows.append(row); labs.append(pred); oobs.append(oob); hs.append(f['he'])
                if method=='event_bootstrap' and b<args.k_resamples:
                    for k in range(2,6):
                        c,kl,ss=fit_h(f['h'],k=k)
                        kboot.append(dict(replicate=b,k=k,sse=ss,
                            silhouette=silhouette_score(f['h'][:,None],kl),
                            min_cluster_count=int(np.bincount(kl,minlength=k).min())))
            except (ValueError,ConvergenceWarning,FloatingPointError) as exc:
                failures.append(dict(method=method,replicate=b,reason=str(exc)))
        success_counts[method]=dict(attempted=len(indices),successful=len(labs),failed=len(indices)-len(labs))
        label_arrays[method]=np.array(labs,dtype=int)
        oob_arrays[method]=np.array(oobs,dtype=bool)
        h_arrays[method]=np.array(hs)
        print(method,success_counts[method],flush=True)
    runs=pd.DataFrame(allrows); runs.to_csv(t/'resample_runs.csv',index=False)
    pd.DataFrame(failures,columns=['method','replicate','reason']).to_csv(t/'failed_runs.csv',index=False)
    pd.DataFrame(kboot).to_csv(t/'k_bootstrap_runs.csv',index=False)
    np.savez_compressed(out/'event_projections.npz',**{k:v for k,v in label_arrays.items()},
        **{k+'_oob':v for k,v in oob_arrays.items()},**{k+'_H':v for k,v in h_arrays.items()})
    summaries=[]
    metrics=[c for c in runs.select_dtypes('number').columns if c not in ['replicate','deleted_year']]
    for method,g in runs.groupby('method',sort=False):
        for metric in metrics:
            v=g[metric].dropna()
            if len(v)==0: continue
            q=np.quantile(v,[.025,.5,.975])
            summaries.append(dict(method=method,metric=metric,n_valid=len(v),mean=v.mean(),
                                  sd=v.std(ddof=1),q025=q[0],median=q[1],q975=q[2],min=v.min(),max=v.max()))
    pd.DataFrame(summaries).to_csv(t/'resample_summary.csv',index=False)
    ranks=[]; memberships=[]
    for method,labels in label_arrays.items():
        g=runs[runs.method==method]
        for q in NAMES:
            ranks.append(dict(method=method,indicator=q,top_weight_fraction=float(np.mean(g.top_weight==q)),n_valid=len(g)))
        for i in range(n):
            oob=oob_arrays[method][:,i]; cnt=int(oob.sum())
            row=dict(method=method,event_id=raw.event_id[i],baseline_scenario=SCENARIOS[y[i]],
                agreement=float(np.mean(labels[:,i]==y[i])),n_valid=len(labels),n_oob=cnt,
                oob_agreement=float(np.mean(labels[oob,i]==y[i])) if cnt else np.nan)
            row.update({'p_'+s:float(np.mean(labels[:,i]==j)) for j,s in enumerate(SCENARIOS)})
            memberships.append(row)
        co=np.mean(labels[:,:,None]==labels[:,None,:],axis=0)
        pd.DataFrame(co,index=raw.event_id,columns=raw.event_id).to_csv(t/(method+'_coassignment.csv'))
    pd.DataFrame(ranks).to_csv(t/'weight_rank_frequencies.csv',index=False)
    pd.DataFrame(memberships).to_csv(t/'event_membership_stability.csv',index=False)
    dump(out/'run_counts.json',success_counts)
    tracked=[p for p in INPUTS.rglob('*') if p.is_file()]+list((BASE/'code').glob('*.py'))+[BASE/'分析方案.md']
    manifest=dict(seed=args.seed,configuration={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},
        python=sys.version,platform=platform.platform(),
        packages={p:importlib.metadata.version(p) for p in ['numpy','pandas','scipy','scikit-learn','matplotlib','PyYAML','threadpoolctl','markdown','openpyxl']},
        input_and_code_sha256={str(p.relative_to(ROOT)):sha(p) for p in tracked},
        source_files_sha256={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'05_Code/Scenario_Pipeline/src/crisp_data_layer/pipeline.py',ROOT/'05_Code/Scenario_Pipeline/src/crisp_data_layer/config.py'] if p.exists()},
        algorithm=dict(k=3,n_init=50,max_iter=300,random_state=42,algorithm='lloyd',ddof=0,
                       projection_clipping=False,quantiles=[.025,.975]))
    dump(out/'manifest.json',manifest)
    print('Analysis saved:',out,flush=True)

if __name__=='__main__':
    with threadpool_limits(limits=1):
        main()
