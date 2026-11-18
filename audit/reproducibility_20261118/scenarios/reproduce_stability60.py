"""Independent replay of final-60 conditional resampling sensitivity.

Resampling indices are freshly regenerated from the declared PCG64 seed and
the original grouping ledger. Historical numerical outputs are read only after
the new calculations have finished, for comparison.
"""
from __future__ import annotations
import itertools
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

from reproduce_scenarios import ROOT, CI, COLS, raw_input, sha

OUT=Path(__file__).resolve().parent/'stability60'


def fit(x):
    low=x.min(0)
    span=x.max(0)-low
    if np.any(span==0):
        raise ValueError('Constant column')
    centered=x-x.mean(0)
    covariance=centered.T@centered
    corr=covariance/np.sqrt(np.outer(np.diag(covariance),np.diag(covariance)))
    sd=np.sqrt(np.mean(centered*centered,axis=0))/span
    information=sd*np.sum(1-corr,axis=1)
    weights=information/information.sum()
    if not np.isfinite(weights).all():
        raise ValueError('Undefined CRITIC')
    h=((x-low)/span)@weights
    sorted_h=np.sort(h)
    first,second=np.array(list(itertools.combinations(range(1,len(h)),2))).T
    a=np.r_[0,np.cumsum(sorted_h)]
    b=np.r_[0,np.cumsum(sorted_h**2)]
    score=b[first]-a[first]**2/first+b[second]-b[first]-(a[second]-a[first])**2/(second-first)+b[-1]-b[second]-(a[-1]-a[second])**2/(len(h)-second)
    ix=int(np.argmin(score));i,j=int(first[ix]),int(second[ix])
    centers=np.array([a[i]/i,(a[j]-a[i])/(j-i),(a[-1]-a[j])/(len(h)-j)])
    thresholds=(centers[:-1]+centers[1:])/2
    return low,span,weights,h,thresholds


def main():
    OUT.mkdir(exist_ok=True)
    frame=raw_input(CI/'analysis/reconstructed_model_input.csv')
    ledger=pd.read_csv(CI/'Inclusion_Exclusion_Audit.csv').set_index('candidate_id').loc[frame.event_id]
    x=frame[COLS].to_numpy(float)
    low,span,weights,h,thresholds=fit(x)
    baseline=np.searchsorted(thresholds,h,side='right')
    rng=np.random.Generator(np.random.PCG64(20261104))
    indices={'leave_one_year_out':[[i for i,year in enumerate(ledger.year) if year!=excluded] for excluded in sorted(ledger.year.unique())]}
    for method,column in [('overlap_episode_bootstrap','overlap_episode_id'),('year_block_bootstrap','year')]:
        blocks=[np.flatnonzero(ledger[column].to_numpy()==key) for key in ledger[column].unique()]
        indices[method]=[np.concatenate([blocks[k] for k in rng.integers(0,len(blocks),size=len(blocks))]).tolist() for _ in range(1000)]
    rows=[]
    for method,replicates in indices.items():
        for replicate,index in enumerate(replicates):
            try:
                low,span,weights,h,thresholds=fit(x[index])
                projection=np.searchsorted(thresholds,((x-low)/span)@weights,side='right')
                labels=np.searchsorted(thresholds,h,side='right')
                rows.append(dict(method=method,replicate=replicate,N=len(index),status='OK',w_R=weights[0],w_W=weights[1],w_S=weights[2],tau1=thresholds[0],tau2=thresholds[1],ARI_projection_to_main=adjusted_rand_score(baseline,projection),freq_Moderate=float(np.mean(labels==0)),freq_Severe=float(np.mean(labels==1)),freq_Extreme=float(np.mean(labels==2))))
            except ValueError as exception:
                rows.append(dict(method=method,replicate=replicate,N=len(index),status=str(exception)))
    current=pd.DataFrame(rows)
    current.to_csv(OUT/'stability_runs.csv',index=False)
    (OUT/'fresh_resample_indices.json').write_text(json.dumps(indices)+'\n')
    # Existing results become comparison targets only after fresh outputs exist.
    old=pd.read_csv(CI/'analysis/stability_runs.csv')
    keys=['method','replicate']
    assert current[keys].equals(old[keys])
    assert current.status.equals(old.status)
    assert np.array_equal(current.N,old.N)
    columns=[column for column in current.select_dtypes('number') if column not in ['replicate','N']]
    comparisons=[]
    for method,group in current.groupby('method',sort=False):
        for column in columns:
            difference=(group[column]-old.loc[group.index,column]).abs()
            comparisons.append(dict(method=method,field=column,n=len(group),max_absolute_error=float(difference.max()),tolerance=1e-12,status='PASS' if difference.max()<=1e-12 else 'FAIL'))
    pd.DataFrame(comparisons).to_csv(OUT/'historical_comparison.csv',index=False)
    original_indices=json.loads((CI/'analysis/stability_resample_indices.json').read_text())
    assert indices==original_indices
    counts=[dict(method=method,attempted=len(group),valid=int(group.status.eq('OK').sum()),failed=int(group.status.ne('OK').sum())) for method,group in current.groupby('method',sort=False)]
    result=dict(status='PASS' if all(row['status']=='PASS' for row in comparisons) else 'FAIL',counts=counts,comparisons=len(comparisons),max_absolute_error=max(row['max_absolute_error'] for row in comparisons),fresh_indices_match_historical_exactly=True,python=sys.version,executable=sys.executable,seed=20261104,bit_generator='PCG64',inputs={'analysis/reconstructed_model_input.csv':sha(CI/'analysis/reconstructed_model_input.csv'),'Inclusion_Exclusion_Audit.csv':sha(CI/'Inclusion_Exclusion_Audit.csv')},scope='Conditional sensitivity only; percentile ranges are not confidence intervals or annual-risk estimates.')
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
