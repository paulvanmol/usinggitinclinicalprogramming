# Using Git in Clinical Trials Programming

Training materials for the hands-on workshop on Git version control
for clinical SAS programmers.

---

## Quick start

### Step 1 — Clone this repo to your workshop folder

```
git clone https://github.com/paulvanmol/usinggitinclinicaltrialsprogramming.git D:\workshop\training
```

Or to a different location:

```
git clone https://github.com/paulvanmol/usinggitinclinicaltrialsprogramming.git /path/to/workshop/training
```

### Step 2 — Run the setup script

The script creates the full study folder structure under your workshop root.

**Windows (Command Prompt or PowerShell):**
```
cd D:\workshop\training\exercise_materials
python setup_study_repo.py --root D:\workshop --study ABC-001
```

**Windows (Git Bash) / Linux / macOS:**
```
cd D:/workshop/training
python3 exercise-materials/setup_study_repo.py --root D:/workshop --study ABC-001
```

### Step 3 — Open the exercise guide

Open `EXERCISE_GUIDE.docx` and follow Exercise 1.

All exercises run inside `D:\workshop\dev\ABC-001\programs\`.

---

## What the setup script creates

```
D:\workshop\
├── training\                      <- this repo (cloned in step 1)
│   ├── EXERCISE_GUIDE.docx
│   └── exercise-materials\
│       ├── setup_study_repo.py
│       ├── setup_study_repo.sh    (Linux version)
│       ├── .gitignore
│       ├── .gitmessage
│       ├── CODEOWNERS
│       └── README.md
│
├── prod\ABC-001\
│   ├── data\                      NOT in Git (DM-owned)
│   │   ├── rawdata\
│   │   ├── sdtm\
│   │   └── adam\
│   ├── output\                    NOT in Git
│   └── programs\                  Git repo — main branch
│       ├── config\libnames.sas
│       ├── macros\m_nobs.sas
│       ├── programs\sdtm, adam, tfl
│       └── qc\sdtm, adam, tfl
│
├── dev\ABC-001\
│   ├── data\                      NOT in Git (local copy)
│   ├── output\                    NOT in Git
│   └── programs\                  Git clone — dev branch
│
└── ABC-001-remote.git\            bare repo (simulates GitHub server)
```

---

## Prerequisites

| Tool | Download | Notes |
|------|----------|-------|
| Git | https://git-scm.com/download/win | Tick "Git Bash" during install |
| Python 3.6+ | https://www.python.org/downloads | Tick "Add Python to PATH" |

No additional Python packages are required — the setup script uses only the standard library.

---

## Repository contents

| File / folder | Purpose |
|---------------|---------|
| `EXERCISE_GUIDE.docx` | Step-by-step exercise guide with 5 exercises |
| `exercise-materials/setup_study_repo.py` | Cross-platform setup script (Windows + Linux) |
| `exercise-materials/setup_study_repo.sh` | Bash version for Linux/macOS |
| `exercise-materials/.gitignore` | Study repo template — excludes data and outputs |
| `exercise-materials/.gitmessage` | Commit message template |
| `exercise-materials/CODEOWNERS` | Role-based approval rules |
| `exercise-materials/README.md` | Study repo README template |

---

## Exercises overview

| # | Title | Duration | Key skills |
|---|-------|----------|------------|
| 1 | Set up your repository | 15 min | init, clone, config, .gitignore |
| 2 | Daily programming workflow | 20 min | add, commit, push, log, diff |
| 3 | Feature branch & pull request | 25 min | branch, merge, CODEOWNERS |
| 4 | Audit trail — who changed what? | 15 min | log, blame, revert |
| 5 | Freeze a study version | 15 min | tag, release branch |
