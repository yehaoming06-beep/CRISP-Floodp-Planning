"""Compare fresh core metrics with the frozen manuscript table transcription."""
from pathlib import Path
import argparse
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]


def checkout_path(path):
    """Resolve relative command-line paths from the checkout root."""
    return (ROOT / path).resolve() if not path.is_absolute() else path.resolve()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--core-metrics', type=Path, required=True,
                        help='Fresh core_metrics.csv; relative paths start at the checkout root')
    parser.add_argument('--output', type=Path, required=True,
                        help='New comparison directory; existing directories are refused')
    args = parser.parse_args()
    metrics_path = checkout_path(args.core_metrics)
    out = checkout_path(args.output)
    # Never overwrite frozen evidence or a previous comparison.
    out.mkdir(parents=True, exist_ok=False)
    reference_path = ROOT / 'audit/reproducibility_20261118/optimization/paper_table6_table14_comparison.csv'
    with metrics_path.open(newline='') as stream:
        fresh = {(row['dataset'], row['id']): row for row in csv.DictReader(stream)}
    with reference_path.open(newline='') as stream:
        reference = list(csv.DictReader(stream))
    rows = []
    for ref in reference:
        metric, model = ref['metric'], ref['model']
        if ref['column'] == 'delta':
            value = float(fresh['reconstructed60', model][metric]) - float(fresh['original23', model][metric])
        else:
            value = float(fresh[ref['column'], model][metric])
        printed = float(ref['paper_text'].replace('\u2212', '-'))
        delta = abs(value - printed)
        tolerance = float(ref['rounding_tolerance'])
        rows.append({**ref, 'recomputed': value, 'signed_error': value-printed,
                     'absolute_error': delta, 'status': 'PASS' if delta <= tolerance else 'FAIL'})
    with (out / 'fresh_core_paper_comparison.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    passed = len(rows) == 48 and all(row['status'] == 'PASS' for row in rows)
    result = {'status': 'PASS' if passed else 'FAIL', 'paper_cells': len(rows),
              'max_abs_error': max(row['absolute_error'] for row in rows),
              'core_metrics_sha256': hashlib.sha256(metrics_path.read_bytes()).hexdigest(),
              'paper_reference_sha256': hashlib.sha256(reference_path.read_bytes()).hexdigest(),
              'reference_role': 'Paper comparison only; not used to construct scientific inputs'}
    (out / 'fresh_core_paper_validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
    if not passed:
        raise RuntimeError('Core paper comparison failed; see the new comparison directory')


if __name__ == '__main__':
    main()
