# 09-03 — Practice 1: Create ABC-001 with git init

## Goal
Create local study repository **ABC-001** using `git init`.

## Configure identity
```bash
export git_user="Your Name"
export git_email="your.email@example.com"
# Backward-compatible alias in case a student typed gite_mail earlier:
export gite_mail="$git_email"

git config user.name "$git_user"
git config user.email "$git_email"
```


## Commands
```bash
cd d:/workshop/training/ABC-001
git init
git branch -M main
git status
git add README.md .gitignore programs metadata docs validation logs/.gitkeep
git commit -m "[ABC-001] Initialise clinical programming repository"
git remote add origin git@gitlab.com:YOUR-GROUP/ABC-001.git
git push -u origin main
```

## Expected output highlights
```text
Initialized empty Git repository ...
[main (root-commit) ...] [ABC-001] Initialise clinical programming repository
Branch 'main' set up to track 'origin/main'
```
