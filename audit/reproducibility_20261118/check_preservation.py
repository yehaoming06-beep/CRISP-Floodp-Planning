#!/usr/bin/env python3
"""Read-only hash, Git, and historical-guard checks for this numerical audit."""
import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path('/Users/yehaoming/Desktop/climate_Devin')
OUT = Path(__file__).resolve().parent


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def main(stage):
    imported = read_csv(ROOT / 'audit/import_manifest.csv')
    sources = read_csv(ROOT / 'audit/source_inventory.csv')
    mapping = {r['source_path']: r for r in imported}
    tracked = set(subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')) - {''}
    paths = [r['repository_path'] for r in imported]
    ignored = set(subprocess.run(['git', 'check-ignore', '--stdin', '-z'],
        input=('\0'.join(paths) + '\0').encode(), capture_output=True, cwd=ROOT).stdout.decode().split('\0')) - {''}
    source_issues, imported_issues, rows = [], [], []
    for row in sources:
        rel = row['source_path']
        p = SOURCE / rel
        observed = sha(p) if p.is_file() else None
        if observed != row['sha256']:
            source_issues.append({'path': rel, 'expected': row['sha256'], 'observed': observed})
        copy = mapping.get(rel)
        target = ROOT / copy['repository_path'] if copy else None
        repository_hash = sha(target) if target and target.is_file() else None
        if copy and repository_hash != copy['sha256']:
            imported_issues.append({'path': copy['repository_path'], 'expected': copy['sha256'], 'observed': repository_hash})
        state = ('TRACKED' if copy['repository_path'] in tracked else
                 'LOCAL_IGNORED' if copy['repository_path'] in ignored else 'LOCAL_UNTRACKED') if copy else 'ORIGINAL_WORKSPACE_ONLY'
        rows.append({'source_path': rel, 'repository_path': copy['repository_path'] if copy else '',
                     'source_exists': p.is_file(), 'source_sha256': observed,
                     'source_matches_pre_audit_inventory': observed == row['sha256'],
                     'repository_exists': bool(target and target.is_file()), 'repository_sha256': repository_hash,
                     'git_state': state, 'prior_disposition': row['disposition']})
    guards = {}
    for name, base in [('repository', ROOT), ('original_workspace', SOURCE)]:
        gp = base / 'manuscript_revision/peer_review_validation_20261105_v2/frozen_manifest_before.json'
        manifest = json.loads(gp.read_text())
        issues = []
        for rel, expected in manifest.items():
            p = base / rel
            observed = sha(p) if p.is_file() else None
            if observed != expected:
                issues.append({'path': rel, 'expected': expected, 'observed': observed})
        guards[name] = {'guard_file': str(gp), 'expected_count': len(manifest),
                        'mismatches_or_missing': len(issues), 'issues': issues, 'pass': not issues}
    with (OUT / f'file_inventory_{stage}.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    report = {'timestamp': datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(), 'stage': stage,
              'source_baseline_files': len(sources), 'source_hash_matches': len(sources)-len(source_issues),
              'source_issues': source_issues, 'imported_baseline_files': len(imported),
              'imported_hash_matches': len(imported)-len(imported_issues), 'imported_issues': imported_issues,
              'tracked_files': sorted(tracked), 'source_inventory_git_states': dict(Counter(r['git_state'] for r in rows)),
              'historical_guard_checks': guards}
    if stage == 'after':
        before = {r['source_path']: r for r in read_csv(OUT/'file_inventory_before.csv')}
        changed = [r['source_path'] for r in rows
                   if r['source_sha256'] != before[r['source_path']]['source_sha256']
                   or (r['repository_sha256'] or '') != before[r['source_path']]['repository_sha256']]
        report['changed_since_this_audit_before'] = changed
        report['existing_source_and_imported_files_preserved'] = not changed
    (OUT / f'preservation_{stage}.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({k:v for k,v in report.items() if k != 'historical_guard_checks'}, ensure_ascii=False))
    print(json.dumps({k:{a:b for a,b in v.items() if a != 'issues'} for k,v in guards.items()}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--stage', required=True, choices=['before','after'])
    main(p.parse_args().stage)
