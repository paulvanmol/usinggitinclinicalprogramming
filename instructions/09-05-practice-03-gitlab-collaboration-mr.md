# 09-05 — Practice 3: GitLab collaboration with Merge Request

Use **ABC-002**. Change a clinical macro or graph program, push a feature branch, and open a GitLab Merge Request.

```bash
cd d:/workshop/training/ABC-002
git checkout main
git pull
git checkout -b feature/ABC-220-graph-footnote
git add macros/m_clin_graph.sas
git commit -m "[ABC-220] Update clinical graph macro"
git push -u origin feature/ABC-220-graph-footnote
```

Expected GitLab result: create a **Merge Request**, assign reviewer, merge only after approval and passing pipeline.
