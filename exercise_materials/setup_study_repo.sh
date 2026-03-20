#!/usr/bin/env bash
# ============================================================
# setup_study_repo.sh
# Initialises a local Git practice environment for the
# "Git for Pharma" hands-on exercises.
#
# Usage:
#   chmod +x setup_study_repo.sh
#   ./setup_study_repo.sh
#
# What it creates:
#   practice-repo/   — your working copy (plays role of GitLab remote)
#   origin-remote/   — bare repo simulating the team server
# ============================================================

set -e

REPO_DIR="practice-repo"
REMOTE_DIR="origin-remote.git"
BLUE='\033[0;34m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo -e "${BLUE}=== Git for Pharma — Exercise Setup ===${NC}"
echo ""

# ---- 1. Create bare remote (simulates GitLab/Azure DevOps) ----
if [ -d "$REMOTE_DIR" ]; then
  echo -e "${YELLOW}Removing existing remote: $REMOTE_DIR${NC}"
  rm -rf "$REMOTE_DIR"
fi
echo -e "${GREEN}Creating simulated remote server...${NC}"
git init --bare "$REMOTE_DIR" -b main
echo ""

# ---- 2. Clone into working copy ----
if [ -d "$REPO_DIR" ]; then
  echo -e "${YELLOW}Removing existing repo: $REPO_DIR${NC}"
  rm -rf "$REPO_DIR"
fi
git clone "$REMOTE_DIR" "$REPO_DIR"
cd "$REPO_DIR"

# ---- 3. Minimal git config for the exercise ----
git config user.name  "Programmer A"
git config user.email "programmer.a@study-abc.com"

# ---- 4. Copy in template files ----
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES="$SCRIPT_DIR"

cp "$TEMPLATES/.gitignore"   .gitignore
cp "$TEMPLATES/CODEOWNERS"   CODEOWNERS
cp "$TEMPLATES/README.md"    README.md

# ---- 5. Create folder skeleton ----
# Tracked folders (source programs, specs, macros, utilities)
mkdir -p programs/sdtm
mkdir -p programs/adam
mkdir -p programs/tfl
mkdir -p macros
mkdir -p specs/shell_templates
mkdir -p utilities
mkdir -p config
mkdir -p validation/sdtm
mkdir -p validation/adam
mkdir -p validation/tfl

# Untracked data folders — created locally but excluded via .gitignore
mkdir -p rawdata/sdtm
mkdir -p rawdata/transfer
mkdir -p data/sdtm
mkdir -p data/adam
mkdir -p output/tfl
mkdir -p output/listings

# Git does not track empty folders — add .gitkeep to tracked folders only
for dir in programs/sdtm programs/adam programs/tfl macros specs specs/shell_templates \
           utilities config validation/sdtm validation/adam validation/tfl; do
  touch "$dir/.gitkeep"
done

# Seed a libnames config stub (no credentials — paths only)
cat > config/libnames.sas << 'ENDCONFIG'
/*====================================================================
  File   : libnames.sas
  Purpose: Libname assignments for Study ABC-001
           Paths resolve relative to the study root.
           Credentials are supplied via environment variables —
           NEVER hardcode passwords here.
====================================================================*/
%let studyroot = /path/to/study-ABC;   /* override per environment */

libname rawsdtm "&studyroot/rawdata/sdtm"  access=readonly;
libname sdtm    "&studyroot/data/sdtm";
libname adam    "&studyroot/data/adam";
ENDCONFIG

# ---- 6. Seed source programs ----

# SDTM stub
cat > programs/sdtm/dm.sas << 'ENDSDTM'
/*====================================================================
  Program : dm.sas
  Study   : ABC-001
  Purpose : Demographics SDTM domain (DM)
  Spec    : SDTM Spec v1.0 (TBD)
  Author  : Programmer A
  Date    : &sysdate9
  Input   : rawsdtm.dm_raw (EDC extract)
  Output  : sdtm.dm
====================================================================*/
%include "../../config/libnames.sas";

data sdtm.dm;
  set rawsdtm.dm_raw;
  /* TODO: apply SDTM variable labels, controlled terminology */
run;
ENDSDTM

# ---- 7. Seed a simple macro ----
cat > macros/m_nobs.sas << 'ENDMACRO'
/*====================================================================
  Macro  : m_nobs
  Purpose: Return the number of observations in a dataset
  Params : DS  — two-part dataset name (lib.dsname)
           MV  — macro variable name to hold the result (default: NOBS)
  Author : Programmer A
  Date   : &sysdate9
====================================================================*/
%macro m_nobs(ds=, mv=NOBS);
  %global &mv;
  %let &mv = 0;
  %if %sysfunc(exist(&ds)) %then %do;
    data _null_;
      if 0 then set &ds nobs=_n;
      call symputx("&mv", _n);
      stop;
    run;
  %end;
  %else %put WARNING: [m_nobs] Dataset &ds does not exist.;
%mend m_nobs;
ENDMACRO

# ---- 8. Seed a stub ADaM program ----
cat > programs/adam/adsl.sas << 'ENDSAS'
/*====================================================================
  Program : adsl.sas
  Study   : ABC-001
  Purpose : Subject-level analysis dataset (ADSL)
  Spec    : ADaM Spec v1.0 (TBD)
  Author  : Programmer A
  Date    : &sysdate9
  Input   : sdtm.dm, sdtm.ds
  Output  : adam.adsl
====================================================================*/
%include "../../config/libnames.sas";

/* --- Step 1: Base population from DM --- */
data work.adsl_base;
  set sdtm.dm (where=(armcd ne "SCRNFAIL"));
  if      age < 18            then agegr1 = "<18";
  else if 18 <= age <= 64     then agegr1 = "18-64";
  else                             agegr1 = ">=65";
  label agegr1 = "Age Group";
run;

/* TODO: merge DS for disposition, derive DCSREAS, EOSSTT */
ENDSAS

# ---- 9. Initial commit ----
git add .
git commit -m "[SETUP] Initialise study-ABC repository structure

- Added .gitignore, CODEOWNERS, README, config/libnames.sas
- Created programs/sdtm, programs/adam, programs/tfl folder layers
- Created rawdata/, data/, output/ (untracked data directories)
- Seeded dm.sas (SDTM), adsl.sas (ADaM), m_nobs macro stubs"

# ---- 9. Create develop branch and push both ----
git checkout -b develop
git push -u origin main
git push -u origin develop
git checkout main

# ---- 10. Summary ----
cd ..
echo ""
echo -e "${GREEN}=== Setup complete ===${NC}"
echo ""
echo "  Working repo : ./$REPO_DIR"
echo "  Remote (bare): ./$REMOTE_DIR"
echo ""
echo "  Branches created:"
echo "    main    (default, protected)"
echo "    develop (integration)"
echo ""
echo "  Next: open EXERCISE_GUIDE.md and start Exercise 1."
echo ""
