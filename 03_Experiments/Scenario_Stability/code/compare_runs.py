"""Compare complete independent executions, excluding path/time metadata and graphics."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

def main(a,b):
    names=sorted(p.name for p in (a/'tables').glob('*.csv') if not p.name.startswith('T'))
    compared=[]
    for name in names:
        x=(a/'tables'/name).read_bytes(); y=(b/'tables'/name).read_bytes()
        assert x==y, 'CSV differs: '+name
        compared.append(name)
    for name in ['baseline_audit.json','resample_indices.json','run_counts.json','publication_table_cells.json']:
        assert json.loads((a/name).read_text())==json.loads((b/name).read_text()), name
    x=np.load(a/'event_projections.npz'); y=np.load(b/'event_projections.npz')
    assert set(x.files)==set(y.files)
    for key in x.files: np.testing.assert_array_equal(x[key],y[key])
    verdict=dict(status='REPRODUCIBLE',comparison='second full run, same locked environment and seeds',
        csv_files_byte_identical=len(compared),csv_names=compared,npz_arrays_exact=len(x.files),
        structured_json_files_identical=4,graphics_and_environment_metadata_excluded=True)
    (a/'reproducibility.json').write_text(json.dumps(verdict,ensure_ascii=False,indent=2))
    print(json.dumps(verdict,ensure_ascii=False,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('first',type=Path);p.add_argument('second',type=Path);a=p.parse_args();main(a.first,a.second)
