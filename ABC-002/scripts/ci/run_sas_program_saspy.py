#!/usr/bin/env python3
import argparse, os, sys, re
from pathlib import Path
try:
    import saspy
except ImportError:
    print('ERROR: saspy is not installed/configured on this GitLab runner.')
    sys.exit(1)

ap=argparse.ArgumentParser()
ap.add_argument('--program', required=True)
ap.add_argument('--log', required=True)
ap.add_argument('--cfgname', default=os.getenv('SASPY_CFGNAME','iom'))
ap.add_argument('--sas-root', default=os.getenv('SAS_ROOT','d:/workshop/training/ABC-002'))
args=ap.parse_args()
program=Path(args.program); log=Path(args.log); log.parent.mkdir(parents=True, exist_ok=True)
code = '%let root=' + args.sas_root.replace('\\','/') + ';\n' + program.read_text(encoding='utf-8')
sas = saspy.SASsession(cfgname=args.cfgname)
res = sas.submit(code)
log.write_text(res.get('LOG',''), encoding='utf-8')
log_text=res.get('LOG','')
if re.search(r'^(ERROR:|ERROR \d+-\d+:)', log_text, re.I|re.M):
    print(f'SAS execution failed. See {log}')
    sys.exit(1)
print(f'SAS execution completed. Log written to {log}')
