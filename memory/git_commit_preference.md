---
name: git_commit_preference
description: "Git commit workflow for the phd-thesis repo — commit after each build milestone, no Claude co-author trailer"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ab5351c4-a7b3-49ce-8a47-4988f4ada274
---

In the phd-thesis repo, commit after each completed build milestone rather than one large commit at the end. Do **NOT** add a `Co-Authored-By: Claude` trailer to commit messages.

**Why:** The user maintains this as a solo-authored thesis repo with linear history on `main`; AI authorship attribution is not wanted.

**How to apply:** After finishing a discrete buildable unit (e.g. bibliography additions, a chapter scaffold, a drafted section), stage and commit directly on `main` with a plain message and no co-author line. This overrides the default Claude Code co-author trailer. Related: [[chapter4_wesad_results]], [[bibliography_audit_chapter1]].
