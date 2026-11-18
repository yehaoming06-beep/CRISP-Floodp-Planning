#!/usr/bin/env python3
"""Verify the reviewed submission files and complete compressed execution evidence.

Uses only the standard library. Does not run scientific models or modify papers.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import tarfile

ROOT = Path(__file__).resolve().parents[1]
DELIVERY = ROOT / 'audit/delivery_20261118'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError(f'Unsafe evidence path: {relative}')
    target = ROOT / path
    if target.is_symlink() or not target.resolve().is_relative_to(ROOT):
        raise ValueError(f'Path escapes checkout: {relative}')
    return target


def verify(restore: bool = False) -> dict:
    with (DELIVERY / 'submission_files.tsv').open(newline='') as stream:
        selected = list(csv.DictReader(stream, delimiter='\t'))
    for row in selected:
        p = safe_path(row['path'])
        assert p.is_file(), f'Missing selected file: {row["path"]}'
        if row['sha256'] != 'SELF_INVENTORY':
            assert p.stat().st_size == int(row['bytes']), row['path']
            assert sha(p.read_bytes()) == row['sha256'], row['path']

    archives = json.loads((DELIVERY / 'evidence_archives.json').read_text())
    members_checked = 0
    # Validate every member and destination before optional restoration writes.
    for record in archives:
        archive = safe_path(record['archive'])
        assert archive.stat().st_size == record['bytes']
        assert sha(archive.read_bytes()) == record['sha256'], record['archive']
        rows = json.loads(safe_path(record['member_manifest']).read_text())
        assert len(rows) == record['members']
        with tarfile.open(archive, 'r:gz') as tar:
            members = tar.getmembers()
            assert len(members) == len(rows)
            for member, row in zip(members, rows):
                assert member.name == row['path'] and member.isfile(), member.name
                dest = safe_path(member.name)
                raw = tar.extractfile(member).read()
                assert len(raw) == row['bytes'] and sha(raw) == row['sha256'], member.name
                if restore and dest.exists():
                    assert dest.is_file() and sha(dest.read_bytes()) == row['sha256'], (
                        f'Refusing to replace different existing file: {member.name}')
                members_checked += 1
    if restore:
        for record in archives:
            with tarfile.open(safe_path(record['archive']), 'r:gz') as tar:
                for member in tar:
                    dest = safe_path(member.name)
                    if not dest.exists():
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        with dest.open('xb') as handle:
                            handle.write(tar.extractfile(member).read())

    supplement = ROOT / 'supplementary/Supplementary_Methods_and_Results.md'
    text = supplement.read_text()
    original = (ROOT / 'manuscript_revision/Supplementary_Methods_and_Results.md').read_text()
    remove_links = lambda s: re.sub(r'\]\([^\n)]*\)', '](LINK)', s)
    assert remove_links(text) == remove_links(original)
    assert re.findall(r'^## (S\d+) ', text, re.M) == [f'S{i}' for i in range(1, 14)]
    links = re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text)
    local_links = [x for x in links if not re.match(r'[a-z]+://', x)]
    assert len(local_links) == 32
    for target in local_links:
        p = (supplement.parent / target.split('#', 1)[0]).resolve()
        assert p.is_relative_to(ROOT) and p.exists(), target

    ci = ROOT / 'manuscript_revision/audit/ci01_independent_20261104'
    for directory, expected in [(ROOT / '04_Results/Optimization', 3875),
                                (ci / 'backend_probability60', 3888)]:
        with (directory / 'summary.csv').open() as stream:
            assert len(list(csv.DictReader(stream))) == 555
        with (directory / 'solver_audit.csv').open() as stream:
            rows = list(csv.DictReader(stream))
        assert len(rows) == expected and all(r['status'] == 'OPTIMAL' for r in rows)

    for row in json.loads((ROOT / 'data/third_party_notices/hko/retrieval.json').read_text()):
        p = ROOT / 'data/third_party_notices/hko' / row['file']
        assert sha(p.read_bytes()) == row['sha256']
    return {'status': 'PASS_SELECTED_TREE_AND_EVIDENCE', 'selected_files': len(selected),
            'archives': len(archives), 'archive_members_verified': members_checked,
            'supplement_sections': 13, 'supplement_local_links': len(local_links),
            'restored_evidence': restore,
            'scope': 'Package/hash/count/link checks; not a scientific rerun or rights guarantee'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--restore-evidence', action='store_true',
                        help='Restore archived files to original checkout paths; refuse changed files')
    parser.add_argument('--output', type=Path, help='Write verification JSON to a new file')
    args = parser.parse_args()
    result = verify(args.restore_evidence)
    if args.output:
        path = args.output if args.output.is_absolute() else ROOT / args.output
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('x') as handle:
            json.dump(result, handle, indent=2)
            handle.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
