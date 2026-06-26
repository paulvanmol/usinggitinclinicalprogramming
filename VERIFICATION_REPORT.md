# Verification report

- `python scripts/ci/sas_static_checks.py --root . --junit reports/sas-static-checks.xml` → return code `0`
- `python scripts/ci/validate_sdtm_adam_structure.py --root . --rules metadata/sdtm_adam_validation_rules.csv --report-dir reports` → return code `0`
- `python scripts/ci/check_sas_logs.py --log-root logs --junit reports/sas-log-scan.xml` → return code `0`
- `python scripts/ci/validate_sdtm_adam_structure.py --root . --rules metadata/sdtm_adam_validation_rules.csv --report-dir reports_fail` → return code `1`

Overall pass: **True**

Grep checks: `{'contains_pull_request': False, 'contains_github': False, 'abc001_mentions': 9, 'abc002_mentions': 22, 'gite_mail_mentions': 2, 'git_email_mentions': 3}`
