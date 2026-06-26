#!/usr/bin/env python3
import argparse, csv, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--root', default='.')
ap.add_argument('--rules', default='metadata/sdtm_adam_validation_rules.csv')
ap.add_argument('--report-dir', default='reports')
args = ap.parse_args()
root = Path(args.root)
report = Path(args.report_dir); report.mkdir(parents=True, exist_ok=True)
issues=[]
with (root/args.rules).open(newline='', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        std=row['standard'].upper(); dom=row['domain'].upper(); folder=row['source_folder']
        path=root/folder/f'{dom.lower()}.csv'
        required=[v.upper() for v in row['required_variables'].split()]
        keys=[v.upper() for v in row['key_variables'].split()]
        if not path.exists():
            issues.append((std,dom,'missing-domain',f'Missing expected file {path.as_posix()}'))
            continue
        with path.open(newline='', encoding='utf-8-sig') as pf:
            headers=[h.strip().upper() for h in next(csv.reader(pf))]
        missing=[v for v in required if v not in headers]
        if missing: issues.append((std,dom,'missing-variables','Missing required variables: '+', '.join(missing)))
        missing_keys=[v for v in keys if v not in headers]
        if missing_keys: issues.append((std,dom,'missing-key-variables','Missing key variables: '+', '.join(missing_keys)))
md=report/'sdtm-adam-structure-validation.md'
md.write_text('# SDTM/ADaM structure validation\n\n' + ('\n'.join(f'- **{s}.{d}** `{c}` — {m}' for s,d,c,m in issues) if issues else 'PASSED\n'), encoding='utf-8')
xml=report/'sdtm-adam-structure-validation.xml'
xml.write_text('<testsuite name="sdtm-adam-structure-validation" tests="{}" failures="{}"></testsuite>'.format(max(1,len(issues)), len(issues)), encoding='utf-8')
print(md.read_text(encoding='utf-8'))
sys.exit(1 if issues else 0)
