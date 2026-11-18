"""Inventory the reviewed submission candidates without staging or committing."""
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
TSV = OUT / 'git_submission_files.tsv'
SUMMARY = OUT / 'final_package_summary.json'
VALIDATION = OUT / 'final_repository_validation.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    for p in (TSV, SUMMARY, VALIDATION):
        if not p.exists():
            p.write_text('')
    candidates = sorted(set(git('ls-files', '-c', '-o', '--exclude-standard', '-z').decode().split('\0')) - {''})
    tracked = set(git('ls-files', '-z').decode().split('\0')) - {''}
    candidate_set = set(candidates)
    errors = []
    links_checked = 0
    for rel in ('README.md', 'SUBMISSION_REPOSITORY_CHECKLIST.md', 'THIRD_PARTY_NOTICES.md',
                'data/README.md', 'src/README.md', 'results/README.md',
                'supplementary/README.md', 'supplementary/ARCHIVE_INDEX.md',
                'supplementary/Supplementary_Methods_and_Results.md'):
        for match in re.finditer(r'!?\[[^\]\n]*\]\((<[^>\n]+>|[^\s)]+)[^)]*\)', (ROOT / rel).read_text()):
            target = match.group(1).strip('<>')
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            links_checked += 1
            p = ((ROOT / rel).parent / unquote(parts.path)).resolve()
            if not p.is_relative_to(ROOT):
                errors.append({'type': 'link_outside_repository', 'path': rel})
                continue
            dest = p.relative_to(ROOT).as_posix()
            if dest not in candidate_set and not any(x.startswith(dest.rstrip('/') + '/') for x in candidates):
                errors.append({'type': 'link_not_in_candidate', 'path': rel, 'target': dest})
    supplement = json.loads((OUT / 'supplementary_index.json').read_text())
    missing_supplement = [r['path'] for r in supplement['local_links']
                          if r['path'] not in candidate_set and
                          not any(p.startswith(r['path'].rstrip('/') + '/') for p in candidates)]
    errors.extend({'type': 'missing_supplement_target', 'path': p} for p in missing_supplement)
    tested = json.loads((OUT / 'tested_final_candidate_manifest.json').read_text())
    tested_by_path = {r['path']: r for r in tested['files']}
    scientific = [p for p in candidates if p.startswith(('01_Data/', '02_Model/', '03_Experiments/', '05_Code/'))
                  or p in {'src/reproduce_submission.py', 'src/submission/scenarios.py',
                           'src/submission/suite60.py', 'src/submission/verify60.py',
                           'audit/reproducibility_20261118/optimization/run_core.py',
                           'audit/reproducibility_20261118/optimization/independent_enumeration.py',
                           'manuscript_revision/audit/ci01_independent_20261104/analysis/reconstructed_model_input.csv',
                           'manuscript_revision/audit/ci01_independent_20261104/Inclusion_Exclusion_Audit.csv'}]
    for p in scientific:
        if p not in tested_by_path or sha(ROOT / p) != tested_by_path[p]['sha256']:
            errors.append({'type': 'scientific_file_differs_from_tested_tree', 'path': p})
    tokens = {
        'private_key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
        'github_token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})\b'),
        'openai_token': re.compile(r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b'),
        'aws_key': re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
        'cookie_header': re.compile(r'^Set-Cookie:\s*\S+', re.I | re.M),
    }
    text_files, binary_files, log_files = 0, 0, 0
    for rel in candidates:
        p = ROOT / rel
        if p.is_symlink():
            errors.append({'type': 'symlink', 'path': rel})
        if p.suffix.lower() in {'.headers', '.lic', '.key', '.pem', '.docx', '.zip'} or p.name == 'network_probe_headers.txt':
            errors.append({'type': 'excluded_category_is_candidate', 'path': rel})
        raw = p.read_bytes()
        log_files += p.suffix == '.log'
        if b'\0' in raw:
            binary_files += 1
            continue
        text_files += 1
        text = raw.decode('utf-8', errors='replace')
        for kind, pattern in tokens.items():
            match = pattern.search(text)
            if match:
                errors.append({'type': kind, 'path': rel, 'line': text.count('\n', 0, match.start()) + 1})
    local = json.loads((ROOT / 'results/repository_audit/submission_final.json').read_text())
    if local['status'] != 'PASS':
        errors.append({'type': 'repository_audit_failed'})
    baseline = json.loads((OUT / 'clean_test_location.json').read_text())
    staged = [x for x in git('diff', '--cached', '--name-only', '-z').decode().split('\0') if x]
    if staged or sha(ROOT / '.git/index') != baseline['actual_index_sha256']:
        errors.append({'type': 'real_index_changed'})
    if git('rev-parse', 'HEAD').decode().strip() != baseline['original_head']:
        errors.append({'type': 'head_changed'})
    validation = {'status': 'PASS_PACKAGE_CHECKS_WITH_RELEASE_BLOCKERS' if not errors else 'FAIL',
                  'errors': errors, 'navigation_links_checked': links_checked,
                  'supplement_candidate_links': len(supplement['local_links']),
                  'scientific_files_identical_to_tested_candidate': len(scientific),
                  'text_files_scanned': text_files, 'binary_files_not_text_scanned': binary_files,
                  'execution_log_files_scanned': log_files,
                  'scan_scope': 'Recognizable tokens/private keys/cookie headers; not an exhaustive secret detector',
                  'repository_audit': local['status'], 'staged_files': staged,
                  'git_index_unchanged': not staged and sha(ROOT / '.git/index') == baseline['actual_index_sha256'],
                  'head_unchanged': git('rev-parse', 'HEAD').decode().strip() == baseline['original_head'],
                  'release_ready': False,
                  'release_blockers': ['Scientific candidates uncommitted; real clone is incomplete',
                                       'Distribution terms/notices and raw-archive access unresolved',
                                       'A real clone of the selected future commit still needs verification']}
    VALIDATION.write_text(json.dumps(validation, indent=2) + '\n')
    no_self_hash = {TSV.relative_to(ROOT).as_posix(), SUMMARY.relative_to(ROOT).as_posix()}
    records = []
    for rel in candidates:
        p = ROOT / rel
        records.append({'path': rel, 'git_state': 'modified_tracked' if rel in tracked else 'untracked_candidate',
                        'bytes': '' if rel in no_self_hash else p.stat().st_size,
                        'sha256': 'SELF_INVENTORY_NOT_HASHED' if rel in no_self_hash else sha(p)})
    with TSV.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['path', 'git_state', 'bytes', 'sha256'], delimiter='\t')
        writer.writeheader()
        writer.writerows(records)
    payload = [x for x in records if x['path'] not in no_self_hash]
    large = sorted(payload, key=lambda x: int(x['bytes']), reverse=True)
    summary = {'created_utc': datetime.now(timezone.utc).isoformat(),
               'kind': 'Final uncommitted candidate inventory; no staging/commit/push',
               'file_count_including_inventory_files': len(records),
               'payload_bytes_excluding_inventory_files': sum(int(x['bytes']) for x in payload),
               'self_reference_convention': 'TSV and this summary are listed but omit their own sizes/hashes; all other files have exact SHA256',
               'tracked_modified': sorted(tracked), 'untracked_candidates': len(records)-len(tracked),
               'directory_file_counts': dict(Counter(x['path'].split('/')[0] for x in records)),
               'files_over_50MiB': [x for x in large if int(x['bytes']) > 50*1024*1024],
               'largest_files': large[:10], 'real_git_index_unchanged': validation['git_index_unchanged'],
               'package_check_status': validation['status'], 'release_ready': False}
    SUMMARY.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({k: summary[k] for k in ('file_count_including_inventory_files',
                     'payload_bytes_excluding_inventory_files', 'untracked_candidates',
                     'files_over_50MiB', 'package_check_status', 'real_git_index_unchanged')}, indent=2))
    if errors:
        raise SystemExit('Package errors: see final_repository_validation.json')


if __name__ == '__main__':
    main()
