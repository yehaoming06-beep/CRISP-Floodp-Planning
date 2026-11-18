"""Recompute scenario chains in isolation; never update frozen outputs."""
from pathlib import Path
from itertools import combinations
import csv,hashlib,json,platform,sys
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score
from threadpoolctl import threadpool_limits
from reconstruct import OUT,SNAP,COLS,csvout,dump

sys.path.insert(0,str(SNAP/'05_Code/Scenario_Pipeline/src'))
from crisp_data_layer.config import load_config
from crisp_data_layer.pipeline import run_data_layer

NAMES=['Moderate','Severe','Extreme']

def exact3(h):
    h=np.sort(h);n=len(h);pairs=np.array(list(combinations(range(1,n),2)));i,j=pairs.T
    a=np.r_[0,np.cumsum(h)];b=np.r_[0,np.cumsum(h*h)]
    sse=b[i]-a[i]**2/i+b[j]-b[i]-(a[j]-a[i])**2/(j-i)+b[n]-b[j]-(a[n]-a[j])**2/(n-j)
    ix=int(np.argmin(sse));ii,jj=pairs[ix]
    return float(sse[ix]),np.array([a[ii]/ii,(a[jj]-a[ii])/(jj-ii),(a[n]-a[jj])/(n-jj)])

def preprocessing(x):
    lo=x.min(0);span=np.ptp(x,axis=0)
    if (span==0).any():raise ValueError('Constant column')
    z=(x-lo)/span;corr=np.corrcoef(z,rowvar=False)
    c=z.std(0,ddof=0)*np.sum(1-corr,axis=1);w=c/c.sum()
    if not np.isfinite(w).all():raise ValueError('Undefined CRITIC')
    return lo,span,w

def fit(name,data,config):
    directory=OUT/'analysis/scenarios'/name;directory.mkdir(parents=True,exist_ok=True)
    with threadpool_limits(limits=1):r=run_data_layer(data,config)
    for key in ['event_results','scenario_summary','indicator_diagnostics','model_parameters','cleaning_log']:
        getattr(r,key).to_csv(directory/f'{key}.csv',index=False)
    x=data[COLS].to_numpy(float);lo,span,w=preprocessing(x);h=(x-lo)/span@w
    exact,centers=exact3(h);params=r.model_parameters.set_index('parameter').value
    tau=np.array([float(params['tau_1']),float(params['tau_2'])]);sse=float(sum((v-g.H_t.mean())**2 for _,g in r.event_results.groupby('scenario') for v in g.H_t))
    assert abs(sse-exact)<1e-10,(name,sse,exact)
    record=dict(name=name,N=len(data),minima=lo.tolist(),ranges=span.tolist(),weights=w.tolist(),centroids=[float(params[f'mu_{i}']) for i in [1,2,3]],thresholds=tau.tolist(),kmeans_sse=sse,exact_global_sse=exact,exact_sse_match=abs(sse-exact)<1e-10,counts=r.scenario_summary.event_count.tolist(),conditional_frequencies=r.scenario_summary.probability.tolist(),representatives=r.scenario_summary[['representative_rainfall','representative_sea_level','representative_storm_surge']].values.tolist())
    dump(f'analysis/scenarios/{name}/fit_summary.json',record)
    return r,record

def stability(data,audit,baseline_record,baseline_labels):
    x=data[COLS].to_numpy(float);ids=list(data.event_id)
    indexed=audit.set_index('candidate_id').loc[ids]
    rng=np.random.Generator(np.random.PCG64(20261104));rows=[];indices={}
    definitions={
        'leave_one_year_out':[[i for i,v in enumerate(indexed.year) if v!=year] for year in sorted(indexed.year.unique())],
    }
    for method,column in [('overlap_episode_bootstrap','overlap_episode_id'),('year_block_bootstrap','year')]:
        blocks=[np.where(indexed[column].to_numpy()==v)[0] for v in indexed[column].unique()]
        definitions[method]=[np.concatenate([blocks[k] for k in rng.integers(0,len(blocks),size=len(blocks))]).tolist() for _ in range(1000)]
    for method,replicates in definitions.items():
        indices[method]=replicates
        for replicate,ix in enumerate(replicates):
            ix=np.array(ix);train=x[ix]
            try:
                lo,span,w=preprocessing(train);ht=(train-lo)/span@w;sse,centers=exact3(ht);tau=(centers[:-1]+centers[1:])/2
                projected=np.searchsorted(tau,(x-lo)/span@w,side='right');train_labels=np.searchsorted(tau,ht,side='right')
                rows.append(dict(method=method,replicate=replicate,N=len(ix),status='OK',w_R=w[0],w_W=w[1],w_S=w[2],tau1=tau[0],tau2=tau[1],ARI_projection_to_main=adjusted_rand_score(baseline_labels,projected),freq_Moderate=float(np.mean(train_labels==0)),freq_Severe=float(np.mean(train_labels==1)),freq_Extreme=float(np.mean(train_labels==2))))
            except ValueError as exc:rows.append(dict(method=method,replicate=replicate,N=len(ix),status=str(exc)))
    csvout('analysis/stability_runs.csv',rows);dump('analysis/stability_resample_indices.json',indices)
    summary=[]
    frame=pd.DataFrame(rows)
    for method,g in frame.groupby('method',sort=False):
        d=dict(method=method,total=len(g),valid=int(g.status.eq('OK').sum()),interpretation='conditional empirical sensitivity; percentile ranges are not confidence intervals or annual-risk estimates')
        for col in ['w_R','w_W','w_S','ARI_projection_to_main','freq_Moderate','freq_Severe','freq_Extreme']:
            d[col+'_p025_median_p975']=np.quantile(g.loc[g.status.eq('OK'),col],[.025,.5,.975]).tolist()
        summary.append(d)
    dump('analysis/stability_summary.json',summary)

def main():
    config=load_config(SNAP/'05_Code/Scenario_Pipeline/config/fallback.yaml')
    audit=pd.read_csv(OUT/'Inclusion_Exclusion_Audit.csv');data=pd.read_csv(OUT/'analysis/reconstructed_model_input.csv')
    original=pd.read_csv(SNAP/'01_Data/Events/model_input.csv');results={};records={}
    r,b=fit('original23_frozen',original,config);results[b['name']]=r;records[b['name']]=b
    ref=pd.read_csv(SNAP/'01_Data/Events/reference_scenarios.csv');ind=pd.read_csv(SNAP/'01_Data/Events/reference_indicators.csv')
    assert np.array_equal(r.scenario_summary.event_count.to_numpy(),ref.event_count.to_numpy())
    assert np.allclose(r.indicator_diagnostics.weight,ind.weight,rtol=0,atol=1e-14)
    # Original identities with v1 anchors/priority; preserve the old ID for comparison.
    common=audit[audit.original_event_id.notna() & audit.model_eligible.eq(True)].sort_values('original_event_id')
    same=pd.DataFrame({'event_id':common.original_event_id.to_numpy(),**{k:common[v].to_numpy() for k,v in zip(COLS,['model_R_mm_day','model_W_mCD','model_S_m'])}})
    for name,matrix in [('original23_new_rules',same),('reconstructed61_main',data)]:
        rr,record=fit(name,matrix,config);results[name]=rr;records[name]=record
    assert np.array_equal(original[COLS].values,same[COLS].values)
    # Sensitivity to a different unit of analysis, not two independent copies.
    joint=audit[audit.hko_warning_group_id.eq(202102)].iloc[0]
    extra=pd.DataFrame([dict(event_id='TC2021_02_JOINT_WARNING_UNIT',**{k:joint[v] for k,v in zip(COLS,['R_mm_day','W_mCD','S_m'])})])
    for name,matrix in [('warning_group62_unit_sensitivity',pd.concat([data,extra],ignore_index=True)),('omit_explicit_joint_rise_sensitivity',data[data.event_id.isin(audit.loc[audit.joint_driver_note.isna(),'candidate_id'])])]:
        rr,record=fit(name,matrix,config);results[name]=rr;records[name]=record
    mainr=results['reconstructed61_main'];mainb=records['reconstructed61_main']
    # Fixed old preprocessing/thresholds: no clipping, since extrapolation is evidence.
    x=data[COLS].values;h=(x-np.array(b['minima']))/np.array(b['ranges'])@np.array(b['weights']);old_projection=np.searchsorted(b['thresholds'],h,side='right')
    projected=pd.DataFrame(dict(event_id=data.event_id,H_using_frozen23_preprocess=h,frozen23_class=[NAMES[k] for k in old_projection],reconstructed61_class=mainr.event_results.scenario,extrapolates_below_old_min=(x<np.array(b['minima'])).any(1),extrapolates_above_old_max=(x>np.array(b['minima'])+np.array(b['ranges'])).any(1)))
    projected.to_csv(OUT/'analysis/fixed_old_preprocess_projection.csv',index=False)
    common_new=mainr.event_results.set_index('event_id').loc[common.candidate_id].copy();old_labels=r.event_results.scenario.to_numpy();new_labels=common_new.scenario.to_numpy()
    migration=pd.DataFrame(dict(original_event_id=original.event_id,candidate_id=common.candidate_id.to_numpy(),old_class=old_labels,new_class=new_labels,old_H=r.event_results.H_t.to_numpy(),new_H=common_new.H_t.to_numpy(),class_changed=old_labels!=new_labels))
    migration.to_csv(OUT/'analysis/Original23_Label_Migration.csv',index=False)
    frequencies=[]
    for name,record in records.items():
        for s,n,p in zip(NAMES,record['counts'],record['conditional_frequencies']):frequencies.append(dict(dataset=name,scenario=s,N=record['N'],count=n,conditional_frequency=p))
    csvout('analysis/Scenario_Comparisons.csv',frequencies)
    # Unknown individual attribution cannot identify final refitted categories.
    # Arithmetic bounds below keep the main61 definition and labels fixed.
    bounds=[dict(scenario=s,known_count=n,pending_identities=2,total_candidate_identities=63,lower=n/63,upper=(n+2)/63,scope='fixed main61 class definitions only; component attribution unresolved; not refitted-model confidence intervals') for s,n in zip(NAMES,mainb['counts'])]
    csvout('analysis/Fixed_Class_Missingness_Bounds.csv',bounds)
    impact=dict(fits=records,original23_baseline_max_weight_error=float(np.max(np.abs(r.indicator_diagnostics.weight.to_numpy()-ind.weight.to_numpy()))),original23_baseline_max_summary_error=float(np.max(np.abs(r.scenario_summary.select_dtypes('number').fillna(0).to_numpy()-ref.select_dtypes('number').fillna(0).to_numpy()))),original23_values_equal_under_v1=True,original23_class_changes=int((old_labels!=new_labels).sum()),original23_ARI_old_vs_refitted61=float(adjusted_rand_score(old_labels,new_labels)),main61_ARI_fixed_old_projection_vs_refitted=float(adjusted_rand_score(projected.frozen23_class,projected.reconstructed61_class)),main61_old_projection_counts=np.bincount(old_projection,minlength=3).tolist(),extrapolates_below_old_min_count=int(projected.extrapolates_below_old_min.sum()),extrapolates_above_old_max_count=int(projected.extrapolates_above_old_max.sum()),pending_identities=2,all_candidate_final_refit_identified=False)
    dump('analysis/scenario_impact.json',impact)
    dump('analysis/backend_probability_update.json',dict(probabilities=dict(zip(NAMES,mainb['conditional_frequencies'])),dataset='reconstructed61_main',N=61,interpretation='conditional frequencies of v1 eligible, attributable, complete cases; scenario-specific resource/benefit coefficients held fixed; hypothetical optimization sensitivity only'))
    dump('logs/analysis_environment.json',dict(python=sys.version,platform=platform.platform(),numpy=np.__version__,pandas=pd.__version__,executable=sys.executable,seed=20261104,bootstrap_counts={'overlap_episode':1000,'year_block':1000,'leave_one_year_out':9},main_pipeline='snapshot of existing implementation',exact_audit='one-dimensional global nonempty contiguous three segments'))
    stability(data,audit,mainb,np.searchsorted(mainb['thresholds'],mainr.event_results.H_t,side='right'))
    print(json.dumps(impact,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
