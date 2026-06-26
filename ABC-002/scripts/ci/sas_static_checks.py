#!/usr/bin/env python3
import argparse, re, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--root', default='.')
ap.add_argument('--junit', default='reports/sas-static-checks.xml')
args = ap.parse_args()
root = Path(args.root)
report_dir = Path(args.junit).parent
report_dir.mkdir(parents=True, exist_ok=True)
issues = []
for p in root.rglob('*.sas'):
    if '.git' in p.parts or 'reports' in p.parts:
        continue
    text = p.read_text(encoding='utf-8', errors='ignore')
    rel = p.relative_to(root).as_posix()
    if not re.search(r'/\*.*?(Program|Purpose)\s*:', text[:800], re.I | re.S):
        issues.append((rel, 'missing-header', 'Missing standard SAS program header.'))
    if re.search(r'(password|pwd|token|secret)\s*=\s*["\'][^"\']+["\']', text, re.I):
        issues.append((rel, 'possible-credential', 'Possible hardcoded credential.'))
    if re.search(r'(C:\\Users\\|/home/[^/]+/|/Users/[^/]+/)', text, re.I):
        issues.append((rel, 'local-path', 'Possible local machine path.'))
for p in root.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.log','.lst','.sas7bdat','.sas7bvew'} and '.git' not in p.parts:
        issues.append((p.relative_to(root).as_posix(), 'generated-artifact', 'Generated SAS artifact should not be committed.'))
md = report_dir/'sas-static-checks.md'
md.write_text('# SAS static checks\n\n' + ('\n'.join(f'- `{r}` **{c}** — {m}' for r,c,m in issues) if issues else 'PASSED\n'), encoding='utf-8')
# Simple JUnit-style XML sufficient for GitLab report parsing demonstration
failures = len(issues)
xml = '<testsuite name="sas-static-checks" tests="{}" failures="{}">{}</testsuite>'.format(max(1,len(issues)), failures, ''.join(f'<testcase name="{c}:{r}"><failure message="{m}">{r}</failure></testcase>' for r,c,m in issues))
Path(args.junit).write_text(xml, encoding='utf-8')
print(md.read_text(encoding='utf-8'))
sys.exit(1 if issues else 0)
