"""Optional independent Parquet-to-JSON parity check; requires pyarrow."""
import argparse
import json
from pathlib import Path
import medical_decision_dataset as data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, default=data.DEFAULT)
    args = parser.parse_args()
    try:
        import pyarrow
        import pyarrow.parquet as parquet
    except ImportError:
        parser.error('Install optional pyarrow to independently decode original Parquet files.')
    lock = {x['name']: x for x in json.loads((args.dataset / 'sources.lock.json').read_text())['files']}
    reports = []
    for item in json.loads((args.dataset / 'table_exports.json').read_text())['exports']:
        resource = lock[item['resource']]
        raw = data.locked_source_bytes(args.dataset, resource)
        original = parquet.read_table(pyarrow.BufferReader(raw)).to_pylist()
        path = (args.dataset / item['path']).resolve()
        if not path.is_relative_to(args.dataset.resolve()) or data.file_sha(path) != item['sha256']:
            raise ValueError('Unverified JSON table export')
        exported = json.loads(path.read_text())
        if original != exported or len(exported) != item['rows']:
            raise ValueError('Original Parquet and decoded JSON differ: ' + item['resource'])
        reports.append({'resource': item['resource'], 'rows': len(original), 'all_values_equal': True})
    print(json.dumps({'pyarrow_version': pyarrow.__version__, 'checks': reports}, indent=2))


if __name__ == '__main__':
    main()
