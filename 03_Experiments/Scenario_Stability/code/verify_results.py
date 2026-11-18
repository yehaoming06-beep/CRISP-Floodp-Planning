"""Independent numerical checks; uses archived production code for spot reruns."""
import argparse
import itertools
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]
INPUTS=ROOT/"01_Data/Events"

def ari(a,b):
    _,a=np.unique(a,return_inverse=True); _,b=np.unique(b,return_inverse=True)
    tab=np.zeros((a.max()+1,b.max()+1),int); np.add.at(tab,(a,b),1)
    pair=lambda v: np.sum(v*(v-1)//2)
    count=pair(tab); rows=pair(tab.sum(1)); cols=pair(tab.sum(0)); total=len(a)*(len(a)-1)//2
    expected=rows*cols/total; maximum=(rows+cols)/2
    return 1. if maximum==expected else (count-expected)/(maximum-expected)

def main(out):
    t=out/'tables'
    raw=pd.read_csv(INPUTS/'model_input.csv'); x=raw.iloc[:,1:].to_numpy(float)
    e=pd.read_csv(t/'baseline_events.csv'); bw=pd.read_csv(t/'baseline_weights.csv')
    basey=e.label.to_numpy(int); n=len(x)
    # Compute Pearson correlations directly from centered raw data, independently of normalized corrcoef.
    centered=x-x.mean(0); cov=centered.T@centered
    corr=cov/np.sqrt(np.outer(np.diag(cov),np.diag(cov)))
    span=x.max(0)-x.min(0); std=np.sqrt(np.mean(centered**2,axis=0))/span
    info=std*np.sum(1-corr,axis=1); w=info/info.sum()
    np.testing.assert_allclose(w,bw.weight,rtol=0,atol=1e-12)
    h=((x-x.min(0))/span)@w
    np.testing.assert_allclose(h,e.H,rtol=0,atol=1e-12)
    s=np.sort(h); ss=[]
    for i,j in itertools.combinations(range(1,n),2):
        groups=[s[:i],s[i:j],s[j:]]
        ss.append(sum(np.sum((g-g.mean())**2) for g in groups))
    audit=json.loads((out/'baseline_audit.json').read_text())
    assert abs(min(ss)-audit['kmeans_sse'])<1e-12
    runs=pd.read_csv(t/'resample_runs.csv')
    saved=np.load(out/'event_projections.npz')
    indices=json.loads((out/'resample_indices.json').read_text())['groups']
    counts=json.loads((out/'run_counts.json').read_text())
    cfg=json.loads((out/'manifest.json').read_text())['configuration']
    rngs=[np.random.default_rng(s) for s in np.random.SeedSequence(cfg['seed']).spawn(3)]
    expected=[rngs[0].integers(n,size=n).tolist() for _ in range(cfg['bootstrap'])]
    assert expected==indices['event_bootstrap']==indices['fixed_preprocess']
    years=pd.to_datetime(pd.read_csv(INPUTS/'event_metadata.csv').event_date).dt.year.to_numpy()
    unique=np.unique(years)
    for ix in indices['year_bootstrap']:
        draw=rngs[1].choice(unique,size=len(unique),replace=True)
        assert np.array_equal(ix,np.concatenate([np.flatnonzero(years==v) for v in draw]))
    for ix in indices['subsample80']:
        assert ix==np.sort(rngs[2].choice(n,size=18,replace=False)).tolist()
    checked=0
    for method,g in runs.groupby('method',sort=False):
        assert counts[method]['successful']==len(g)
        assert counts[method]['attempted']==len(indices[method])
        assert np.all(np.diff(g[['center_Moderate','center_Severe','center_Extreme']],axis=1)>0)
        np.testing.assert_allclose(g[['w_rainfall','w_sea_level','w_storm_surge']].sum(1),1,atol=1e-12)
        np.testing.assert_allclose(g[['p_train_Moderate','p_train_Severe','p_train_Extreme']].sum(1),1,atol=1e-12)
        np.testing.assert_allclose(g[['p_project_Moderate','p_project_Severe','p_project_Extreme']].sum(1),1,atol=1e-12)
        for pos,(_,r) in enumerate(g.iterrows()):
            ix=np.array(indices[method][int(r.replicate)])
            pred=saved[method][pos]; hp=saved[method+'_H'][pos]
            c=r[['center_Moderate','center_Severe','center_Extreme']].to_numpy(float)
            yp=np.searchsorted((c[:-1]+c[1:])/2,hp,side='right')
            np.testing.assert_array_equal(pred,yp)
            assert abs(ari(basey,pred)-r.ARI)<1e-12
            assert abs(np.mean(pred==basey)-r.agreement)<1e-12
            assert len(np.setdiff1d(np.arange(n),ix))==r.n_oob
            for j,sname in enumerate(['Moderate','Severe','Extreme']):
                assert abs(np.mean(pred[ix]==j)-r['p_train_'+sname])<1e-12
                assert abs(np.mean(pred==j)-r['p_project_'+sname])<1e-12
                for c,q in enumerate(['rainfall','sea_level','storm_surge']):
                    assert abs(x[ix][pred[ix]==j,c].mean()-r['rep_'+sname+'_'+q])<1e-10
            checked+=1
        co=np.mean(saved[method][:,:,None]==saved[method][:,None,:],axis=0)
        np.testing.assert_allclose(co,pd.read_csv(t/(method+'_coassignment.csv'),index_col=0),atol=1e-12)
    summary=pd.read_csv(t/'resample_summary.csv')
    for _,r in summary.iterrows():
        v=runs.loc[runs.method==r.method,r.metric].dropna()
        np.testing.assert_allclose(np.quantile(v,[.025,.5,.975]),r[['q025','median','q975']].to_numpy(float),atol=1e-12)
    assert runs.lloyd_sse_gap.min()>-1e-10
    # Original implementation with fresh IDs: resampling multiplicities are intentionally retained.
    sys.path.insert(0,str(ROOT/'05_Code/Scenario_Pipeline/src'))
    from crisp_data_layer.config import load_config
    from crisp_data_layer.pipeline import run_data_layer
    config=load_config(ROOT/'05_Code/Scenario_Pipeline/config/fallback.yaml')
    original_spots=0
    for method,g in runs.groupby('method',sort=False):
        if method=='fixed_preprocess': continue
        for _,r in g.head(10).iterrows():
            ix=indices[method][int(r.replicate)]
            sampled=raw.iloc[ix].reset_index(drop=True).copy()
            sampled.event_id=['replica_'+str(i) for i in range(len(sampled))]
            result=run_data_layer(sampled,config)
            np.testing.assert_allclose(result.indicator_diagnostics.weight,
                r[['w_rainfall','w_sea_level','w_storm_surge']].to_numpy(float),atol=1e-12)
            np.testing.assert_allclose(result.scenario_summary.cluster_center_mu,
                r[['center_Moderate','center_Severe','center_Extreme']].to_numpy(float),atol=1e-12)
            original_spots+=1
    verdict=dict(status='PASS',independent_formula_check=True,all_resample_rows_checked=checked,
        all_quantile_rows_checked=len(summary),resample_indices_regenerated=True,
        production_spot_reruns=original_spots,exact_global_baseline_verified=True,
        failed_fits=sum(v['failed'] for v in counts.values()),
        nonoptimal_lloyd_fits=int((runs.lloyd_sse_gap>1e-10).sum()),
        tolerance_numeric=1e-12,representatives_tolerance=1e-10)
    (out/'verification.json').write_text(json.dumps(verdict,indent=2))
    print(json.dumps(verdict,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,default=ROOT/'04_Results/Scenario_Stability'); a=p.parse_args()
    with threadpool_limits(limits=1): main(a.output.resolve())
