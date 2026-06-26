#!/usr/bin/env python3
import argparse, re, sys
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('--log-root', default='logs'); ap.add_argument('--junit', default='reports/sas-log-scan.xml'); args=ap.parse_args()
Path(args.junit).parent.mkdir(parents=True, exist_ok=True)
findings=[]
root=Path(args.log_root)
for log in root.rglob('*.log') if root.exists() else []:
    for n,line in enumerate(log.read_text(errors='ignore').splitlines(),1):
        if re.search(r'^(ERROR:|ERROR \d+-\d+:)|uninitialized|Invalid data|Apparent symbolic reference .* not resolved', line, re.I): findings.append(('ERROR', log, n, line.strip()))
        elif re.search(r'^WARNING:', line, re.I): findings.append(('WARNING', log, n, line.strip()))
md=Path(args.junit).parent/'sas-log-scan.md'
md.write_text('# SAS log scan\n\n' + ('\n'.join(f'- `{p}` line {n}: **{sev}** — {txt}' for sev,p,n,txt in findings) if findings else 'PASSED\n'), encoding='utf-8')
Path(args.junit).write_text('<testsuite name="sas-log-scan" tests="{}" failures="{}"></testsuite>'.format(max(1,len(findings)), sum(1 for f in findings if f[0]=='ERROR')), encoding='utf-8')
print(md.read_text(encoding='utf-8'))
sys.exit(1 if any(f[0]=='ERROR' for f in findings) else 0)
