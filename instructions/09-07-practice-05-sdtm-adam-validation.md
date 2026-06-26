# 09-07 — Practice 5: ADaM/SDTM validation failure and fix

## Break the validation deliberately
Remove `EOSSTT` from the header row of:

```text
data/adam/csv/adsl.csv
```

Expected failed job output:
```text
ADAM.ADSL missing-variables — Missing required variables: EOSSTT
```

## Fix
Restore `EOSSTT`, commit, push, and confirm the pipeline passes.
