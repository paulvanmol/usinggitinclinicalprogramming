#!/usr/bin/env python3
"""
setup_study_repo.py
====================
Sets up the hands-on Git exercise environment for
"Using Git in Clinical Trials Programming".

Clone this training repo to your workshop folder, then run:

  Windows (Command Prompt or PowerShell):
    python exercise-materials\\setup_study_repo.py --root D:\\workshop --study ABC-001

  Windows (Git Bash) / Linux / macOS:
    python3 exercise-materials/setup_study_repo.py --root D:/workshop --study ABC-001

What it creates
---------------
  <root>/
  ├── prod/<study>/
  │   ├── data/          (local only - not tracked by Git)
  │   │   ├── rawdata/
  │   │   ├── sdtm/
  │   │   └── adam/
  │   ├── output/        (local only - not tracked by Git)
  │   └── programs/      Git repo, main branch
  │       ├── config/
  │       ├── macros/
  │       ├── programs/  (sdtm, adam, tfl)
  │       └── qc/        (sdtm, adam, tfl)
  │
  ├── dev/<study>/
  │   ├── data/          (local only - not tracked by Git)
  │   ├── output/        (local only - not tracked by Git)
  │   └── programs/      Git clone, dev branch checked out
  │
  └── <study>-remote.git/  bare repo (simulates the GitHub/GitLab server)

Prerequisites
-------------
  Git    : https://git-scm.com/download/win
  Python : https://www.python.org/downloads  (tick "Add Python to PATH")
"""

import argparse
import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path


# ── Helpers ───────────────────────────────────────────────────────────────────

def run(args, cwd=None, check=True):
    cmd = ["git"] + [str(a) for a in args]
    print("  $", " ".join(cmd))
    result = subprocess.run(
        cmd, cwd=str(cwd) if cwd else None,
        check=check, capture_output=True, text=True
    )
    if result.stdout.strip():
        print("   ", result.stdout.strip())
    if result.returncode != 0 and result.stderr.strip():
        print("   ERROR:", result.stderr.strip())
    return result


def write(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content).lstrip("\n"), encoding="utf-8")


def touch(path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.touch()


def banner(text):
    print()
    print("=" * 60)
    print(f"  {text}")
    print("=" * 60)


def step(n, text):
    print(f"\n── {n}. {text}")


def check_git():
    result = subprocess.run(["git", "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: 'git' not found on PATH.")
        print("  Install from https://git-scm.com/download/win")
        sys.exit(1)
    print(f"  Found: {result.stdout.strip()}")


# ── Seed file content ─────────────────────────────────────────────────────────

def seed_gitignore():
    return """\
# ============================================================
# .gitignore for SAS Clinical Study Repository
# ============================================================

# SAS execution outputs - reproducible from source, never commit
*.log
*.lst

# SAS data files - sourced from DM/EDC pipeline, not Git
*.sas7bdat
*.sas7bcat
*.sas7bndx
*.sas7bvpg
*.sas7butl
*.xpt
*.sasxport
*.cport

# Derived data lake outputs
*.parquet
*.avro

# Data and output folders - live outside the repo on disk
data/
rawdata/
output/

# SAS work directories
work/
saswork/
sasuser/
sasmacr/

# Temporary files
scratch/
temp/
tmp/
*.tmp

# OS noise
.DS_Store
Thumbs.db
desktop.ini
*.swp
*.swo
*~

# Editor / IDE settings
.vscode/settings.json
.idea/
*.iml

# Sensitive config - NEVER commit credentials
config/passwords.ini
config/secrets.ini
.env
*.env
libname_creds.sas
"""


def seed_codeowners():
    return """\
# ============================================================
# CODEOWNERS
# GitLab: place at .gitlab/CODEOWNERS
# GitHub:  place at CODEOWNERS or .github/CODEOWNERS
# ============================================================

# Default: lead programmer reviews everything
*                               @lead-programmer

# SDTM programs: lead + SDTM specialist
/programs/sdtm/*.sas            @lead-programmer @sdtm-specialist
/programs/sdtm/**/*.sas         @lead-programmer @sdtm-specialist

# ADaM programs: lead + QC statistician
/programs/adam/*.sas            @lead-programmer @qc-statistician
/programs/adam/**/*.sas         @lead-programmer @qc-statistician

# TFL programs: lead + QC programmer
/programs/tfl/*.sas             @lead-programmer @qc-programmer
/programs/tfl/**/*.sas          @lead-programmer @qc-programmer

# Macro library: macro owner only
/macros/*.sas                   @macro-library-owner
/macros/**/*.sas                @macro-library-owner

# QC programs: QC lead only
/qc/                            @qc-lead

# Specs: data manager + lead programmer
/specs/                         @data-manager @lead-programmer

# Config (libnames, env paths): lead programmer only
/config/                        @lead-programmer

# Repo config: lead programmer only
/.gitignore                     @lead-programmer
/CODEOWNERS                     @lead-programmer
"""


def seed_gitmessage():
    return """\
[TASK-ID] Short description (max 72 chars, imperative mood)

# What changed and WHY (not just what - the diff shows what):
-
-

# Reference spec / protocol section if applicable:
# per ADaM spec v___ section ___

# Known limitations or follow-up tasks:
# TODO:
"""


def seed_readme(study):
    return f"""\
# Study {study} - SAS Programming Repository

## Overview

| Item | Value |
|------|-------|
| Study | {study} |
| Protocol | v1.0 dated YYYY-MM-DD |
| Programming lead | [Name] |
| QC lead | [Name] |

## Branching conventions

| Branch | Purpose | Merge requires |
|--------|---------|----------------|
| `main` | Frozen, tagged releases | 2 approvals (lead + QC) |
| `release/vX.Y` | Release candidate, UAT | 1 QC approval |
| `dev` | Active development | 1 peer approval |
| `feature/<task-id>` | Individual task work | PR to dev |
| `hotfix/<issue-id>` | Urgent fixes against main | 2 approvals |

## Folder structure (this repo)

```
programs/          <- repo root
├── config/
│   └── libnames.sas    paths only, credentials via env variables
├── macros/             study-specific SAS macros
├── programs/
│   ├── sdtm/
│   ├── adam/
│   └── tfl/
├── qc/                 independent validation programs
│   ├── sdtm/
│   ├── adam/
│   └── tfl/
└── specs/              locked specification documents
```

## What is NOT in Git

| Not tracked | Reason |
|-------------|--------|
| `data/rawdata`, `data/sdtm`, `data/adam` | DM-owned; Git is not a data store |
| `output/` | Rendered TFLs; reproducible from tracked programs |
| `*.log`, `*.lst` | Derived outputs; re-run the program to regenerate |
| Credentials | Use environment variables; never hardcode passwords |

## Tagging a frozen version

```bash
git tag -a v1.0 -m "Database lock - YYYY-MM-DD"
git push origin v1.0
```

Tags are immutable. Never delete or force-move a tag after pushing.
"""


def seed_libnames(study):
    return f"""\
/*====================================================================
  File   : libnames.sas
  Purpose: Libname assignments for Study {study}
           Paths resolve via STUDYROOT environment variable.
           Credentials via environment variables - NEVER hardcode here.
  Usage  : %include "config/libnames.sas";
====================================================================*/
%let studyroot = %sysget(STUDYROOT);  /* set per environment */

libname rawsdtm "&studyroot/data/rawdata"  access=readonly;
libname sdtm    "&studyroot/data/sdtm";
libname adam    "&studyroot/data/adam";
"""


def seed_dm_sas(study):
    return f"""\
/*====================================================================
  Program : dm.sas
  Study   : {study}
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
  /* TODO: apply SDTM variable labels and controlled terminology */
run;
"""


def seed_m_nobs():
    return """\
/*====================================================================
  Macro  : m_nobs
  Purpose: Return the number of observations in a dataset
  Params : DS  - two-part dataset name (lib.dsname)
           MV  - macro variable to hold result (default: NOBS)
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
"""


def seed_adsl_sas(study):
    return f"""\
/*====================================================================
  Program : adsl.sas
  Study   : {study}
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
"""


# ── Populate a programs working copy ─────────────────────────────────────────

def populate_programs_repo(programs_dir, study):
    """Write all template and seed files into the programs working copy."""

    write(programs_dir / ".gitignore",  seed_gitignore())
    write(programs_dir / "CODEOWNERS",  seed_codeowners())
    write(programs_dir / ".gitmessage", seed_gitmessage())
    write(programs_dir / "README.md",   seed_readme(study))

    tracked_folders = [
        "config",
        "macros",
        "programs/sdtm",
        "programs/adam",
        "programs/tfl",
        "qc/sdtm",
        "qc/adam",
        "qc/tfl",
        "specs",
    ]
    for folder in tracked_folders:
        touch(programs_dir / folder / ".gitkeep")
        print(f"    + {folder}/")

    write(programs_dir / "config/libnames.sas",    seed_libnames(study))
    write(programs_dir / "programs/sdtm/dm.sas",   seed_dm_sas(study))
    write(programs_dir / "macros/m_nobs.sas",      seed_m_nobs())
    write(programs_dir / "programs/adam/adsl.sas", seed_adsl_sas(study))
    print("    Seeded: libnames.sas, dm.sas, adsl.sas, m_nobs.sas")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Set up the Git for Pharma workshop folder structure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples
            --------
              Windows:
                python exercise-materials\\setup_study_repo.py --root D:\\workshop --study ABC-001

              Linux / macOS:
                python3 exercise-materials/setup_study_repo.py --root ~/workshop --study ABC-001
        """)
    )
    parser.add_argument("--root",  required=True,
                        help="Workshop root folder, e.g. D:\\workshop")
    parser.add_argument("--study", required=True,
                        help="Study identifier, e.g. ABC-001")
    args = parser.parse_args()

    root   = Path(args.root).resolve()
    study  = args.study

    prod_programs = root / "prod" / study / "programs"
    dev_programs  = root / "dev"  / study / "programs"
    bare_remote   = root / f"{study}-remote.git"

    banner("Git for Pharma - Workshop Setup")
    print(f"  Root   : {root}")
    print(f"  Study  : {study}")
    print(f"  Prod   : {prod_programs}")
    print(f"  Dev    : {dev_programs}")
    print(f"  Remote : {bare_remote}")

    check_git()

    # ── 1. Local data + output folders (both sides, untracked) ───────────────
    step(1, "Creating local data and output folders (not tracked by Git)")
    for base in [root / "prod" / study, root / "dev" / study]:
        for folder in ["data/rawdata", "data/sdtm", "data/adam",
                       "output/tfl", "output/listings"]:
            p = base / folder
            p.mkdir(parents=True, exist_ok=True)
            print(f"  + {p}  (untracked)")

    # ── 2. Bare remote ────────────────────────────────────────────────────────
    step(2, f"Creating bare remote (simulates GitHub server): {bare_remote}")
    if bare_remote.exists():
        print("  Already exists - skipping.")
    else:
        run(["init", "--bare", str(bare_remote), "-b", "main"])

    # ── 3. Prod programs — init, populate, commit, push ──────────────────────
    step(3, f"Initialising prod programs repo")
    if (prod_programs / ".git").exists():
        print("  Already initialised - skipping.")
    else:
        prod_programs.mkdir(parents=True, exist_ok=True)
        run(["init", "-b", "main"], cwd=prod_programs)
        run(["config", "user.name",  "Programmer A"], cwd=prod_programs)
        run(["config", "user.email", "programmer.a@study-abc.com"], cwd=prod_programs)
        run(["remote", "add", "origin", str(bare_remote)], cwd=prod_programs)

        print("\n  Populating files...")
        populate_programs_repo(prod_programs, study)

        run(["config", "commit.template", ".gitmessage"], cwd=prod_programs)
        run(["add", "."], cwd=prod_programs)
        run(["commit", "-m",
             f"[SETUP] Initialise {study} repository structure\n\n"
             "- Added .gitignore, CODEOWNERS, README, config/libnames.sas\n"
             "- Created programs/sdtm, programs/adam, programs/tfl\n"
             "- Created qc/sdtm, qc/adam, qc/tfl\n"
             "- Seeded dm.sas (SDTM), adsl.sas (ADaM), m_nobs macro stubs"],
            cwd=prod_programs)
        run(["push", "-u", "origin", "main"], cwd=prod_programs)

    # ── 4. Dev — clone + checkout dev branch ─────────────────────────────────
    step(4, f"Cloning into dev")
    if (dev_programs / ".git").exists():
        print("  Already cloned - skipping.")
    else:
        dev_programs.parent.mkdir(parents=True, exist_ok=True)
        run(["clone", str(bare_remote), str(dev_programs)])
        run(["config", "user.name",  "Programmer A"], cwd=dev_programs)
        run(["config", "user.email", "programmer.a@study-abc.com"], cwd=dev_programs)
        run(["config", "commit.template", ".gitmessage"], cwd=dev_programs)

    branches = run(["branch", "-a"], cwd=dev_programs).stdout
    if "dev" not in branches:
        run(["checkout", "-b", "dev"], cwd=dev_programs)
        run(["push", "-u", "origin", "dev"], cwd=dev_programs)
    else:
        run(["checkout", "dev"], cwd=dev_programs)
        print("  dev branch already exists.")

    # ── Done ──────────────────────────────────────────────────────────────────
    banner("Setup complete")
    print(f"""
  {root}
  ├── prod/{study}/
  │   ├── data/          rawdata, sdtm, adam  (local only - not in Git)
  │   ├── output/        tfl, listings        (local only - not in Git)
  │   └── programs/      Git repo  [main branch]
  │
  ├── dev/{study}/
  │   ├── data/          rawdata, sdtm, adam  (local only - not in Git)
  │   ├── output/        tfl, listings        (local only - not in Git)
  │   └── programs/      Git clone [dev branch]
  │
  └── {study}-remote.git/   bare repo (simulates GitHub server)

  Branches:  main (prod)   dev (dev)

  Next step:
    Open EXERCISE_GUIDE.docx and start Exercise 1.
    All exercises run inside:
      {dev_programs}
""")


if __name__ == "__main__":
    main()
