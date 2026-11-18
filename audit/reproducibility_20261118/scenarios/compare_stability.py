"""Compare a fresh full scenario-stability run with frozen numerical tables."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent/'stability'
OLD=ROOT/'04_Results/Scenario_Stability'

rows=[]
for path in sorted((OUT/'tables').glob('*.csv')):
    saved=OLD/'tables'/path.name
    if not saved.exists():
        rows.append(dict(table=path.name,status='NO_HISTORICAL_TARGET',rows=0,max_absolute_error=None))
        continue
    new=pd.read_csv(path)
    old=pd.read_csv(saved)
    assert new.columns.equals(old.columns),path.name
    assert new.shape==old.shape,path.name
    numeric=new.select_dtypes('number').columns
    max_error=0.0
    numeric_pass=True
    for col in numeric:
        assert np.array_equal(new[col].isna(),old[col].isna()),(path.name,col)
        diff=(new[col]-old[col]).abs().dropna()
        error=float(diff.max()) if len(diff) else 0.0
        max_error=max(max_error,error)
        numeric_pass=numeric_pass and error<=1e-10
    other=[col for col in new if col not in numeric]
    nonnumeric_pass=all(new[col].fillna('<NA>').equals(old[col].fillna('<NA>')) for col in other)
    rows.append(dict(table=path.name,status='PASS' if numeric_pass and nonnumeric_pass else 'FAIL',rows=len(new),max_absolute_error=max_error,tolerance=1e-10,nonnumeric_equal=nonnumeric_pass))
pd.DataFrame(rows).to_csv(OUT/'historical_comparison.csv',index=False)
indices_equal=json.loads((OUT/'resample_indices.json').read_text())==json.loads((OLD/'resample_indices.json').read_text())
result=dict(status='PASS' if all(r['status']=='PASS' for r in rows) and indices_equal else 'FAIL',compared_tables=len(rows),max_absolute_error=max(r['max_absolute_error'] or 0 for r in rows),fresh_indices_equal_historical=indices_equal,numerical_tolerance=1e-10)
(OUT/'historical_comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
