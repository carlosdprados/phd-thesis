---
name: thesis-jury-audit-polish
description: "Jury-style thesis audit + fixes done 2026-06-08 — SI appendices B/C/D added, chapter labels/figure-dirs renamed to bound order (scripts keep legacy names), defensive language cut, bib verified."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1d539aab-8773-4ca5-9c2b-89b59d36d424
---

A full jury-style audit of the bound thesis (front matter + Ch1–Ch6 + appendices) was done and acted on 2026-06-08. Audit report: `handouts/24_thesis_jury_audit.md`. Five committed phases.

**Durable structural facts (verify before relying):**
- **SI appendices now exist for every body chapter.** Appendix A = Ch2 (pre-existing), B = Ch3 bridge, C = Ch4 comparative (the big one: provenance, confound audits, fit thresholds, EIS circuit, plus promoted per-cell decay/pulses/EIS/electrode tables), D = Ch5 temporal (parameter-card sourcing + simulation settings). Files: `chapters/appendix_chapter{3_bridge,4_comparative,5_temporal}_SI.tex`, `\include`d from `thesis.tex` under `\appendix`. Each chapter has a standalone-safe ref macro (`\siBridgeRef`/`\siCompRef`/`\siTempRef`) that does `\cref` in thesis mode and prints a literal "Appendix X" standalone — same pattern as Ch2's `\chTwoSIRef`.
- **NAMING GOTCHA:** tex labels, internal `chN_` label prefixes, and `figures/chapterN/` dirs now follow **bound chapter order** (Ch3=bridge→`ch3`/`figures/chapter3`, Ch4=comparative→`ch4_`/`figures/chapter4`, Ch5=temporal→`ch5_`/`figures/chapter5`). BUT the figure-generation **scripts keep legacy filenames**: `scripts/ch3_figures.py` produces the **Chapter-4** figures, `scripts/ch4_figures.py` the **Chapter-5** figures (their `FIGDIR` outputs point at the correct bound dir). Per-cell data CSVs in `handouts/` also keep mixed legacy `ch3_`/`ch4_` names. Documented in `README.md` "Naming convention".

**Why:** future edits/searches will be misled if you assume script/CSV numbers match chapter numbers — they don't. The tex side is clean; the script/CSV side is legacy.

**How to apply:** when adding a figure to Ch4, edit `scripts/ch3_figures.py`; for Ch5, `scripts/ch4_figures.py`. Put new SI material in the matching `appendix_chapter*_SI.tex` and reference it from the chapter via the `\si*Ref` macro, not a bare `\cref` (keeps standalone builds clean).

Other phases: whole bib CrossRef-verified ([[bibliography_audit_chapter1]]); all "honest/honestly/honesty" meta-labels and defensive phrasing ("not a confession", "apologetic", "shown not averaged") removed for a less defensive register; dead `\figplaceholder` macro dropped. Full thesis builds clean: 215 pp, 0 undefined refs/citations. See [[thesis_structure]].
