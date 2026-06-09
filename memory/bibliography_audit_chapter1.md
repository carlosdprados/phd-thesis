---
name: bibliography-audit-chapter1
description: Thesis references.bib citation-audit log. Ch1 had LLM-hallucinated DOIs/titles (fixed 2026-05-19). Ch2 verified clean (2026-06-03). Ch3-6 verified clean (2026-06-08) — whole bib now CrossRef-verified.
metadata: 
  node_type: memory
  type: project
  originSessionId: 58ccc534-9e9d-461a-a6a8-df261570d354
---

`bibliography/references.bib` for `chapters/chapter1_introduction.tex` was audited against crossref on 2026-05-19. Several entries had wrong DOIs (didn't resolve), wrong titles (DOI pointed to a different paper), or fabricated content (no matching paper exists in crossref). The pattern is consistent with LLM-hallucinated citations.

**Why:** When chapter 2/3 prose lands, the same verification step is needed before relying on any citation. Don't assume bib entries are right just because they parse — verify against crossref by DOI.

**How to apply:** When the user adds new prose with `\cite{...}` keys, scan the cited keys, pull each entry's DOI from references.bib, and hit `https://api.crossref.org/works/{doi}` to confirm the title matches. Flag mismatches before the user submits. Watch especially for DOIs that don't resolve (HTTP 404 from crossref) and DOIs whose resolved title is completely unrelated — those are LLM hallucination tells.

Entries fixed in chapter 1:
- `Park2020`, `Goswami2020` (wrong titles/DOIs)
- `Bichler2012`, `Wagberg2008`, `vanReenen2010`, `Zakhidov2010`, `Lei2014` (wrong DOIs)
- `Mardegan2021`, `NatureBottleneck2018`, `Xu2016` (wrong titles)
- `Edman2008` deleted — was a duplicate of `Wagberg2008` with fabricated title
- `Shih2017` deleted — DOI fabricated, no matching paper; replaced by `Shih2016` (real Mater. Horiz. review) at one site and `ScottBozano2007` + `Yang2006` at the organic-CBRAM sites

**Chapter 2 — audited clean 2026-06-03.** All 59 cited keys in `chapters/chapter2_proof_of_concept.tex` were verified against crossref by DOI (automated parse→query→diff). Every key resolves to a real, correctly attributed work — **no hallucinations found** (unlike chapter 1). Edge cases were all benign: `<sub>` markup in CrossRef titles (`Lightfoot1993`), "deMello" vs "de Mello" spacing, and online-vs-print year for `Heremans2011`/`Liu2016` (bib uses correct print year). Two books (`Hebb1949`, `Gray1991`) were retyped `@article`→`@book`. So chapter 2 does **not** need re-auditing.

**Chapters 3–6 — audited clean 2026-06-08.** The 11 cite keys new to Ch3 (bridge), Ch4 (comparative), Ch5 (temporal), Ch6 (conclusions) beyond the Ch1/Ch2 set were verified against CrossRef by DOI (9 with DOIs all exact; `Jaeger2002STM` techreport and `ChourpiliadisBhardwaj2022` StatPearls are non-CrossRef source types, cited correctly). **No hallucinations.** Log in `handouts/25_bibliography_audit_ch3_6.md`. The whole thesis bibliography is now CrossRef-verified — no chapter needs re-auditing unless new keys are added.

See [[user_profile]] for who is doing this work. Broader thesis-polish context in [[thesis_jury_audit_polish]].
