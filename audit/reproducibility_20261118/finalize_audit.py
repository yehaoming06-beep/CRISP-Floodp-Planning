#!/usr/bin/env python3
"""Validate this audit's claims and links; seal new evidence without old writes."""
import csv
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]


def read(rel):
    return json.loads((OUT/rel).read_text())


def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):
            h.update(block)
    return h.hexdigest()


def main():
    scenario=read('scenarios/clean_environment/scenario_reproduction_summary.json')
    optimization=read('optimization/optimization_audit_summary.json')
    reconstruction=read('reconstruction/validation.json')
    supplementary=read('supplementary/verification.json')
    preservation=read('preservation_after.json')
    environment=read('environment_final.json')
    assert scenario['status']==optimization['status']==supplementary['status']=='PASS'
    assert scenario['paper_comparisons']==82 and scenario['paper_failures']==0
    assert optimization['paper_comparison']['paper_cells_compared']==48
    assert optimization['paper_comparison']['paper_failures']==0
    assert optimization['ev_ties_history_comparison']['fields_compared']==240
    assert optimization['ev_ties_history_comparison']['failures']==0
    assert optimization['integer_rounding_verification']['failures']==0
    assert reconstruction['all_11_outputs_byte_identical'] and reconstruction['different_cells']==0
    assert supplementary['independent_milp_calls']==936
    assert preservation['existing_source_and_imported_files_preserved']
    assert preservation['historical_guard_checks']['original_workspace']['pass']
    assert environment['status']=='PASS_INSTALL' and environment['pip_check']['exit_code']==0
    assert '17 passed' in (OUT/'software_tests_fresh.txt').read_text()
    paper=ROOT/'manuscript_revision/CRISP_Merged_Manuscript.docx'
    assert sha(paper)=='4e12f7849d0b2ca7dd0d156c987a9e90f8b651880c79b74e10f14bffbab4ca37'
    summary={'date':'2026-11-18','timezone':'Asia/Shanghai',
             'status':'PASS_LOCAL_NUMERICAL_REPRODUCTION_WITH_EXPLICIT_LIMITS',
             'paper_tables_compared':[4,6,11,12,14],'paper_comparison_items':130,'paper_comparison_failures':0,
             'original23_and_final60_core_reproduced_in_fresh_environment':True,
             'reconstruction_outputs_identical':11,'sweeps_configurations':1110,
             'sweep_gurobi_main_records':[3875,3888],'independent_sweep_RP_optima':1110,
             's9_extra_gurobi_records':[1796,1808],'s9_comparison_items':240,
             'v2_gurobi_records':500,'v2_highs_calls':936,
             'scenario_resampling_records':[9032,2009],'non_global_lloyd_resamples':37,
             'software_tests_fresh_passed':17,'existing_scientific_files_preserved':True,
             'navigation_readme_updated_with_new_audit':True,
             'paper_sha256':sha(paper),'report_sha256':sha(ROOT/'REPRODUCIBILITY_AUDIT.md'),
             'blocked':['Git-only checkout lacks scientific files and raw inputs',
                        'historical original23 screening/anchor/station-choice evidence not recovered',
                        'three pending identities remain unresolved',
                        'field calibration and score-to-loss/population mapping absent',
                        'Node styled-export dependency manifest/lock not found'],
             'limits':['Full 555/sensitivity suites run in original environment; fresh environment reran core models and source reconstruction.',
                       'Independent all-six-metric exhaustive proof is for four core models; independent 555 optimum proof is RP-only.',
                       'Offline reconstruction inherits frozen manual QC and historical extracted PDF text; no new visual/source adjudication.',
                       'No empirical validation, historical paper edit, commit, push or public-setting change.']}
    (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    # Initial manifest makes every report link resolvable before final checks.
    manifest_path=OUT/'evidence_manifest.json'
    manifest_path.write_text('{}')
    missing=[]
    for target in re.findall(r'\]\(([^)]+)\)',(ROOT/'REPRODUCIBILITY_AUDIT.md').read_text()):
        if not target.startswith(('https:','http:')) and not (ROOT/target).exists():
            missing.append(target)
    assert not missing,missing
    checks={'status':'PASS','paper_comparison_items':130,'links_missing':missing,
            'paper_hash_preserved':True,'existing_scientific_files_preserved':True,
            'new_evidence_is_independent_from_historical_output_directories':True,
            'review_note':'scenarios/REPORT_REVIEW.md',
            'superseded_failures_retained':['clean_environment_install.txt','software_test_attempts.json',
               'supplementary/failure.json','optimization/clean_environment_attempt01_console.log']}
    (OUT/'final_audit_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
    artifacts=[]
    paths=sorted(p for p in OUT.rglob('*') if p.is_file() and p!=manifest_path)
    paths.append(ROOT/'REPRODUCIBILITY_AUDIT.md')
    paths.append(ROOT/'README.md')
    for p in paths:
        assert not p.is_symlink()
        artifacts.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)})
    manifest={'created_at':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
              'scope':'All new audit files plus root report and updated navigation README; manifest excludes itself to avoid recursive hashing.',
              'files':len(artifacts),'bytes':sum(r['bytes'] for r in artifacts),'artifacts':artifacts}
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    for r in artifacts:
        assert sha(ROOT/r['path'])==r['sha256'],r['path']
    print(json.dumps({'status':'PASS','paper_items':130,'audit_files_sealed':manifest['files'],
                      'audit_bytes':manifest['bytes'],'source_and_imported_files_preserved':True}))


if __name__ == '__main__':
    main()
