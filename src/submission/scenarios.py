"""Recompute manuscript scenario values from source inputs into a new directory.

No saved result is used to construct an input or estimate a parameter. The
independent implementation fits CRITIC directly, enumerates all nonempty
contiguous three-cluster partitions, and cross-checks the existing seeded
KMeans pipeline only after the independent fit has finished.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import itertools
import json
import math
from pathlib import Path
import platform
import re
import subprocess
import sys
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
CI = ROOT / 'manuscript_revision/audit/ci01_independent_20261104'
COLS = ['event_window_max_daily_rainfall_mm', 'maximum_sea_level_mCD', 'maximum_storm_surge_m']
NAMES = ['Moderate', 'Severe', 'Extreme']
INDICATORS = ['rainfall', 'sea_level', 'storm_surge']


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_status(path):
    if not (ROOT / '.git').exists():
        return 'prospective_git_tree_export'
    rel = str(path.relative_to(ROOT))
    tracked = subprocess.run(['git', 'ls-files', '--error-unmatch', '--', rel], cwd=ROOT, capture_output=True).returncode == 0
    ignored = subprocess.run(['git', 'check-ignore', '-q', '--', rel], cwd=ROOT, capture_output=True).returncode == 0
    return 'tracked' if tracked else ('ignored_local' if ignored else 'untracked_local')


def raw_input(path):
    frame = pd.read_csv(path)
    assert frame.event_id.is_unique and not frame.event_id.isna().any()
    assert not frame[COLS].isna().any().any()
    assert np.isfinite(frame[COLS].to_numpy(dtype=float)).all()
    return frame


def independent_fit(frame, name):
    x = frame[COLS].to_numpy(dtype=float)
    minima, maxima = x.min(axis=0), x.max(axis=0)
    z = (x - minima) / (maxima - minima)
    # Scalar Pearson correlation with fsum avoids calling the production
    # pandas correlation/std implementation.
    means = np.array([math.fsum(z[:, j]) / len(z) for j in range(3)])
    centered = z - means
    sumsquares = np.array([math.fsum(centered[:, j] ** 2) for j in range(3)])
    std = np.sqrt(sumsquares / len(z))
    corr = np.array([[math.fsum(centered[:, i] * centered[:, j]) / math.sqrt(sumsquares[i] * sumsquares[j]) for j in range(3)] for i in range(3)])
    conflict = np.array([math.fsum(1.0 - corr[i]) for i in range(3)])
    information = std * conflict
    weights = information / math.fsum(information)
    h = z @ weights
    ordered = np.sort(h)
    best = None
    trials = []
    for first, second in itertools.combinations(range(1, len(h)), 2):
        groups = (ordered[:first], ordered[first:second], ordered[second:])
        centers = np.array([math.fsum(g) / len(g) for g in groups])
        sse = math.fsum(math.fsum((g - c) ** 2) for g, c in zip(groups, centers))
        trials.append((first, second, sse))
        if best is None or sse < best[0]:
            best = sse, centers, (first, second)
    sse, centers, split = best
    thresholds = (centers[:-1] + centers[1:]) / 2
    labels = np.searchsorted(thresholds, h, side='right')
    assert tuple(np.bincount(labels, minlength=3).cumsum()[:2]) == split
    events = frame.copy()
    for j, ind in enumerate(INDICATORS):
        events['z_' + ind] = z[:, j]
    events['H_t'] = h
    events['scenario'] = [NAMES[int(i)] for i in labels]
    events.to_csv(OUT / f'{name}_events.csv', index=False)
    summary = []
    for i, scenario in enumerate(NAMES):
        group = x[labels == i]
        summary.append(dict(scenario=scenario, event_count=len(group), probability=len(group) / len(x), cluster_center_mu=float(centers[i]), representative_rainfall=float(group[:, 0].mean()), representative_sea_level=float(group[:, 1].mean()), representative_storm_surge=float(group[:, 2].mean())))
    pd.DataFrame(summary).to_csv(OUT / f'{name}_summary.csv', index=False)
    pd.DataFrame(dict(indicator=INDICATORS, minimum=minima, maximum=maxima, normalized_std=std, conflict=conflict, information_content=information, weight=weights)).to_csv(OUT / f'{name}_critic.csv', index=False)
    pd.DataFrame(trials, columns=['split_1', 'split_2', 'sse']).to_csv(OUT / f'{name}_all_partitions.csv', index=False)
    return dict(name=name, N=len(frame), minima=minima.tolist(), ranges=(maxima-minima).tolist(), weights=weights.tolist(), centers=centers.tolist(), thresholds=thresholds.tolist(), counts=np.bincount(labels, minlength=3).tolist(), frequencies=(np.bincount(labels, minlength=3)/len(frame)).tolist(), global_sse=float(sse), evaluated_partitions=len(trials), summary=summary), events


def manuscript_tables():
    # Read-only table transcription from the audited, SHA-identified manuscript.
    # It is a comparison reference, never an input to scenario fitting.
    path = ROOT / 'audit/reproducibility_20261118/scenarios/paper_tables_4_11_12.json'
    return {int(k): v for k, v in json.loads(path.read_text()).items()}


def main():
    global OUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=OUT)
    arguments = parser.parse_args()
    OUT=arguments.output.resolve()
    OUT.mkdir(parents=True,exist_ok=False)
    source_paths = [ROOT/'01_Data/Events/model_input.csv', CI/'analysis/reconstructed_model_input.csv', ROOT/'05_Code/Scenario_Pipeline/config/fallback.yaml', CI/'Inclusion_Exclusion_Audit.csv', ROOT/'05_Code/Scenario_Pipeline/src/crisp_data_layer/pipeline.py', ROOT/'audit/reproducibility_20261118/scenarios/paper_tables_4_11_12.json']
    inventory = []
    for path in source_paths:
        rel = path.relative_to(ROOT)
        inventory.append(dict(path=str(rel), sha256=sha(path), bytes=path.stat().st_size, git_status=git_status(path)))
    dump('input_inventory.json', inventory)
    frozen, reconstructed = (raw_input(path) for path in source_paths[:2])
    assert len(frozen) == 23 and len(reconstructed) == 60
    audit = pd.read_csv(CI/'Inclusion_Exclusion_Audit.csv')
    eligible = audit[audit.model_eligible.eq(True)]
    supplied = reconstructed.set_index('event_id')[COLS]
    derived = eligible.set_index('candidate_id')[['model_R_mm_day','model_W_mCD','model_S_m']].rename(columns=dict(zip(['model_R_mm_day','model_W_mCD','model_S_m'], COLS)))
    assert set(supplied.index) == set(derived.index)
    differences = supplied - derived.loc[supplied.index]
    differences.to_csv(OUT/'reconstructed_input_vs_inclusion_ledger.csv')
    assert np.array_equal(supplied.values, derived.loc[supplied.index].values)
    same = eligible[eligible.original_event_id.notna()].sort_values('original_event_id')
    common = pd.DataFrame({'event_id': same.original_event_id.to_numpy(), **{column: same[key].to_numpy() for column, key in zip(COLS, ['model_R_mm_day','model_W_mCD','model_S_m'])}})
    assert np.array_equal(frozen.event_id, common.event_id)
    assert np.array_equal(frozen[COLS].values, common[COLS].values)
    # Save no copied hazard inputs: generated event outputs retain the independently computed fields.
    fits, event_sets = {}, {}
    for name, frame in [('original23', frozen), ('original23_new_rules', common), ('reconstructed60', reconstructed)]:
        fits[name], event_sets[name] = independent_fit(frame, name)
    old = fits['original23']
    projected_h = ((reconstructed[COLS].values - old['minima']) / old['ranges']) @ old['weights']
    projected_labels = np.searchsorted(old['thresholds'], projected_h, side='right')
    projected_counts = np.bincount(projected_labels, minlength=3)
    pd.DataFrame(dict(event_id=reconstructed.event_id, H_frozen23_preprocessing=projected_h, scenario=[NAMES[i] for i in projected_labels])).to_csv(OUT/'reconstructed60_fixed_preprocessing_events.csv', index=False)
    fits['reconstructed60_fixed_preprocessing'] = dict(N=60, weights=old['weights'], counts=projected_counts.tolist(), frequencies=(projected_counts/60).tolist())

    # Cross-check the unmodified production implementation after all independent fits.
    sys.path.insert(0, str(ROOT/'05_Code/Scenario_Pipeline/src'))
    from crisp_data_layer.config import load_config
    from crisp_data_layer.pipeline import run_data_layer
    config = load_config(source_paths[2])
    assert (config.critic.standard_deviation_ddof,config.kmeans.k,config.kmeans.random_state,config.kmeans.n_init,config.kmeans.max_iter,config.scenarios.representative_statistic) == (0,3,42,50,300,'mean')
    pipeline_comparison=[]
    for name, frame in [('original23', frozen), ('original23_new_rules', common), ('reconstructed60', reconstructed)]:
        with threadpool_limits(limits=1):
            actual = run_data_layer(frame, config)
        actual.event_results.to_csv(OUT/f'{name}_production_events.csv', index=False)
        max_weight = float(np.max(np.abs(actual.indicator_diagnostics.weight.to_numpy()-fits[name]['weights'])))
        max_score = float(np.max(np.abs(actual.event_results.H_t-event_sets[name].H_t)))
        disagreements = int((actual.event_results.scenario != event_sets[name].scenario).sum())
        pipeline_sse=float(sum(((group.H_t-group.H_t.mean())**2).sum() for _,group in actual.event_results.groupby('scenario')))
        row=dict(dataset=name,max_weight_abs_error=max_weight,max_score_abs_error=max_score,label_disagreements=disagreements,kmeans_sse=pipeline_sse,independent_global_sse=fits[name]['global_sse'],global_sse_abs_error=abs(pipeline_sse-fits[name]['global_sse']),status='PASS' if max_weight<1e-12 and max_score<1e-12 and disagreements==0 and abs(pipeline_sse-fits[name]['global_sse'])<1e-12 else 'FAIL')
        pipeline_comparison.append(row)
    pd.DataFrame(pipeline_comparison).to_csv(OUT/'production_crosscheck.csv',index=False)

    tables=manuscript_tables()
    dump('paper_tables_4_11_12.json',tables)
    comparisons=[]
    def compare(table,dataset,row,field,printed,value,tolerance):
        expected=float(printed)
        error=float(value)-expected
        comparisons.append(dict(table=table,dataset=dataset,row=row,field=field,paper_printed=printed,recomputed=float(value),signed_error=error,absolute_error=abs(error),rounding_tolerance=tolerance,status='PASS' if abs(error)<=tolerance+1e-12 else 'FAIL'))
    for table,name in [(4,'original23'),(12,'reconstructed60')]:
        for printed,computed in zip(tables[table][1:],fits[name]['summary']):
            assert printed[0]==computed['scenario']
            for col,field,tol in [(1,'event_count',0),(3,'cluster_center_mu',.5e-6),(4,'representative_rainfall',.5e-6),(5,'representative_sea_level',.5e-6),(6,'representative_storm_surge',.5e-6)]:
                compare(table,name,printed[0],field,printed[col],computed[field],tol)
            rational,decimal=printed[2].split('=')
            numerator,denominator=[int(i.strip()) for i in rational.split('/')]
            compare(table,name,printed[0],'probability_exact_fraction',str(numerator/denominator),computed['probability'],1e-15)
            compare(table,name,printed[0],'probability_printed',decimal.strip(),computed['probability'],.5e-6)
    for printed,name in zip(tables[11][1:],['original23','original23_new_rules','reconstructed60','reconstructed60_fixed_preprocessing']):
        fit=fits[name]
        compare(11,name,printed[0],'N',printed[1],fit['N'],0)
        for ind,weight,num in zip(INDICATORS,fit['weights'],re.findall(r'\d+\.\d+',printed[2])):
            compare(11,name,printed[0],'weight_'+ind,num,weight,.5e-6)
        for scenario,count,num in zip(NAMES,fit['counts'],printed[3].split('/')):
            compare(11,name,scenario,'count',num,count,0)
        for scenario,freq,num in zip(NAMES,fit['frequencies'],re.findall(r'\d+\.\d+',printed[4])):
            compare(11,name,scenario,'frequency_percent',num,freq*100,.005)
    pd.DataFrame(comparisons).to_csv(OUT/'paper_comparison.csv',index=False)
    old_ids = audit[audit.original_event_id.notna()].sort_values('original_event_id')
    refitted=event_sets['reconstructed60'].set_index('event_id').loc[old_ids.candidate_id]
    migration=pd.DataFrame(dict(original_event_id=frozen.event_id,candidate_id=old_ids.candidate_id.to_numpy(),old_class=event_sets['original23'].scenario.to_numpy(),new_class=refitted.scenario.to_numpy()))
    migration['class_changed']=migration.old_class!=migration.new_class
    migration.to_csv(OUT/'original23_label_migration.csv',index=False)
    pending=audit[audit.model_eligible.ne(True)]
    pending.to_csv(OUT/'pending_identities_unchanged.csv',index=False)
    venv_config_path=Path(sys.prefix)/'pyvenv.cfg'
    venv_config=venv_config_path.read_text() if venv_config_path.exists() else ''
    isolated='include-system-site-packages = false' in venv_config.lower()
    environment_type='Fresh isolated audit environment; no inherited system-site-packages' if isolated else 'Existing original research environment reused, not a clean installation'
    dump('environment.json',dict(python=sys.version,executable=sys.executable,platform=platform.platform(),packages={p:importlib.metadata.version(p) for p in ['numpy','pandas','scikit-learn','threadpoolctl','PyYAML']},environment_type=environment_type,virtual_environment_prefix=sys.prefix,base_prefix=sys.base_prefix,include_system_site_packages=not isolated,runner_sha256=sha(Path(__file__)),command=f'{sys.executable} {Path(__file__).relative_to(ROOT)} --output {OUT.relative_to(ROOT)}',configuration=dict(critic_ddof=0,k=3,random_state=42,n_init=50,max_iter=300,algorithm='lloyd',representative_statistic='mean',independent_algorithm='scalar CRITIC and exhaustive global one-dimensional three-segment SSE minimization')))
    result=dict(status='PASS' if all(r['status']=='PASS' for r in comparisons+pipeline_comparison) else 'FAIL',paper_comparisons=len(comparisons),paper_failures=sum(r['status']!='PASS' for r in comparisons),pipeline_crosschecks=pipeline_comparison,fits=fits,original23_label_changes=int(migration.class_changed.sum()),pending_identities=pending.candidate_id.tolist(),input60_matches_inclusion_ledger_exactly=True,original23_new_screening_input_identical=True,environment_type=environment_type,limits=['Source reconstruction from archived HKO records was not rerun in this scenario calculation.','Three pending identities are retained unresolved.'])
    dump('scenario_reproduction_summary.json',result)
    print(json.dumps({key:result[key] for key in ['status','paper_comparisons','paper_failures','original23_label_changes','pending_identities']},ensure_ascii=False,indent=2))
    if result['status'] != 'PASS':
        raise RuntimeError('Scenario numerical cross-check failed; see generated records')


if __name__=='__main__':
    main()
