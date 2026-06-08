# Thesis Jury Audit — Structure, SI, Consistency, Signposting, Citations

Date: 2026-06-08
Scope: full manuscript as bound by `thesis.tex` (front matter + Ch1–Ch6 + Appendix A).
Reading stance: a thesis-committee member reading linearly, then probing.

Overall: the scientific argument is strong, the evidence grading (replicated vs
illustrative) is unusually disciplined, and citation *coverage* is good. The
issues below are about **proportion and packaging**, not correctness. They are
ordered by how much a jury would notice them.

---

## A. The biggest structural issue: SI asymmetry

**Finding.** Only Chapter 2 has a Supporting-Information appendix (Appendix A).
Chapters 3 (bridge), 4 (comparative), and 5 (temporal) carry *more*
methodological/provenance machinery than Chapter 2 — but all of it sits in the
main text. A jury reads the polished, SI-thin Chapter 2, then hits dense methods
plumbing inline for the rest of the thesis. The packaging is inconsistent with
the chapter that sets the standard.

Quantitatively, inline reproducibility pointers (`scripts/…`, `handouts/…`,
`\texttt{}`, `\path{}`) per chapter:

| Chapter | inline pointers |
|---|---|
| Ch3 bridge | 18 |
| **Ch4 comparative** | **59** |
| Ch5 temporal | 5 |

**Recommendation — create Appendix B/C/D mirroring Appendix A**, and move:

- **Ch4 → SI (strongest case):**
  - The raw-to-summary provenance table (`tab:ch4_provenance`) — pure data lineage.
  - The "aggregation ladder" paragraph and the data-quality / curation-registry
    details (`sec:ch4_methods`).
  - The Kohlrausch fit-identification thresholds and the β-range discussion.
  - The **thickness-confound** four-point enumerated argument + partial
    correlations, and the **"other fabrication variables"** paragraph. Keep in
    main text: one result sentence ("thickness covaries with PEO but the
    dynamics track composition; full audit in SI") + `fig:ch4_thickness_control`.
  - The EIS equivalent-circuit description (Munar circuit, the
    freely-fitted-vs-bounded caveat, ill-conditioning) — condense to the
    model-free headline in main text, push circuit detail to SI.
- **Ch3 → SI:** the per-feature health-flag statistics and the four-controls
  derivation can be tightened in-text with full numbers in SI. (The
  elimination *table* is good narrative — keep it.)
- **Ch5 → SI:** lightest; a short "model identification" SI for the
  `φ ⊗ λ ⊗ f` parameter-card construction would suffice.

**Data currently invisible to the jury.** Several key quantitative tables exist
*only* as external CSVs (`handouts/ch4_decay_by_cell.csv`,
`ch4_pulses_by_cell.csv`, `ch4_eis_by_cell.csv`, …). A committee cannot open
`handouts/*.csv`. Promote the per-cell median/`n` tables into the new SI so every
plotted number is verifiable inside the document. This *adds* the missing data
rather than moving it.

**Conversely**, the chapters do *not* silently leave experimental data behind:
the bias-resolved EIS (to 3 V), chemistry-resolved impedance, the uncurated gold
corpus, and the EPSC population are all explicitly named as future work. That is
handled honestly — no action needed beyond the SI repackaging above.

---

## B. Consistency issues

1. **Internal labels/paths lagging the chapter renumbering — resolved
   2026-06-08.** After the bridge was inserted as Ch3, the comparative and
   temporal artifacts temporarily retained old `ch3_*`/`ch4_*` prefixes. Active
   chapter labels, figure directories, scripts, and current machine-readable
   CSVs now follow the bound order (`ch4_*` for the comparative chapter,
   `ch5_*` for the temporal-computing chapter). The canonical map is
   `docs/current_chapter_numbering.md`.

2. **Dead code:** `\figplaceholder` macro defined in `chapter4_comparative.tex`
   is unused (all figures are real). → **Fixed in this pass** (removed).

3. **Register seam between Ch2 and Ch3+.** Ch2 carries the published-paper voice
   (assertive); Ch3–5 adopt a heavily hedged audit voice. Both are defensible,
   but the tonal jump at the Ch2→Ch3 boundary is palpable. Consider softening a
   few of Ch2's most assertive claims or adding one sentence at the top of Ch3
   acknowledging the deliberate shift to a more cautious, archive-based register.

4. **"Three common measurements"** is introduced in Ch2 and re-introduced "as a
   named set" in Ch4 — acceptable redundancy for standalone readability, but the
   Ch4 re-introduction could shorten to a back-reference.

---

## C. Over-explaining / over-signposting

1. **The "honesty" tic.** `honest|honestly|honesty` appears 16× (Ch5 ×7, Ch6 ×4,
   Ch4 ×3, Ch3 ×1, front matter ×1). Plus "this is a scientific question, not a
   confession", "deserves a positive rather than an apologetic reading", and
   "shown, not averaged" (verbatim in both a body sentence *and* a caption).
   Repeatedly announcing one's own honesty reads as defensive — a jury trusts the
   disclosure more when it is *made* than when it is *labelled*. Recommend
   cutting the meta-labels and keeping the substance (the error bars, the nulls,
   the `n`s already do the work).

2. **Triple structural signposting.** Front-matter "Structure of the Thesis" +
   each chapter's own "Introduction and Scope" roadmap + end-of-chapter "bridge"
   sections + Ch6 re-summary. The per-chapter "this chapter is organised as
   follows" list (esp. Ch2 §intro) duplicates the section headings the reader is
   about to see. Keep the front-matter roadmap and the bridges; trim the
   in-chapter section-by-section enumerations to a sentence.

3. **Cross-reference density.** Nearly every paragraph points elsewhere. In the
   Ch4 Discussion and the Ch5 "Design Rule" section it becomes a hall of mirrors.
   Thin the back-references where the point stands on its own.

4. **Ch2 §intro re-litigates the Ch1 literature gap** (Erokhin/Zakhidov/Liu/OECT)
   almost verbatim from Ch1 §organic_precedents. Compress to a pointer +
   one-sentence gap statement.

5. **The two-metric distinction (shelf vs batch stability)** in Ch3 is stated in
   §problem, restated in §reconciliation, and echoed in Ch6. One canonical
   statement + pointers is enough.

---

## D. Citations

Coverage is generally strong and claims are well-anchored. Two items:

1. **HIGH PRIORITY — verification status.** Per the project bibliography audit,
   Ch1 previously contained LLM-hallucinated DOIs/titles (since fixed) and Ch2 is
   fully CrossRef-verified. The chapters added later — **Ch3 bridge, Ch4
   comparative, Ch5 temporal, Ch6 conclusions — have NOT been CrossRef-verified.**
   Any newly introduced reference (e.g. `Munar2012`, `Frech1999PEOLiTf`,
   `Sturman2003`, `Schmidt2018WESAD`, `AtiyaParlos2000`, `Jaeger2002STM`,
   `Dambre2012`, `Appeltant2011`, `Picard1997`, `Boucsein2012EDA`,
   `TaskForce1996HRV`, `ChourpiliadisBhardwaj2022`, the 2024 organic-neuromorphic
   reviews) should be checked against CrossRef before submission. This is the
   single most important citation action.

2. **Minor thin spots** (defensible but could be hardened):
   - Ch3 hydrolysis hypothesis: "hyperbranched polyester-amides are
     hydrolytically labile and hygroscopic by construction" leans on a single
     review (`VoitLederer2009`); a second source would harden the mechanistic
     claim that anchors the whole degradation chapter.
   - Ch1 is citation-rich; no gaps found.
   - No quantitative claim was found that is stated without either a citation or
     an explicit in-thesis data pointer.

---

## Suggested action order

1. **Run the CrossRef verification pass on Ch3–Ch6** (correctness; pre-submission
   blocker). [D1]
2. **Create SI appendices B/C/D** and move the provenance/confound/fit-threshold
   material out of Ch4 (and lighter Ch3/Ch5 methods), promoting per-cell tables
   *into* SI. [A]
3. **One editorial pass** to cut the honesty meta-labels and the duplicated
   structural signposting. [C]
4. **Rename internal `ch3_*/ch4_*` labels and figure dirs** to match bound order,
   or document the offset. [B1]
5. (done) Remove dead `\figplaceholder` macro. [B2]

Items 2–4 are editorial decisions for the author; item 1 is a correctness blocker.

---

## Resolution (2026-06-08)

All five items were implemented across five commits:

1. **[D1] Citations** — all 11 new Ch3–Ch6 references CrossRef-verified clean (no
   hallucinations); hydrolysis claim grounded in ester/amide chemistry with two
   bib sources. See `25_bibliography_audit_ch3_6.md`. The full thesis bibliography
   is now CrossRef-verified.
2. **[A] SI appendices** — Appendix B (Ch3 controls), C (Ch4 provenance +
   confound audits + fit thresholds + EIS circuit + **promoted per-cell decay /
   pulses / EIS / electrode tables**), D (Ch5 parameter-card sourcing +
   simulation settings). Main chapters keep result + figures + a guarded
   one-line SI pointer (`\si*Ref`, standalone-safe like Ch2's `\chTwoSIRef`).
3. **[C] Editorial pass** — all 16 honesty meta-labels removed; "not a
   confession", "apologetic", duplicate "shown, not averaged", and
   "hold it throughout" cut; Ch2 intro relitigation and section roadmap compressed.
4. **[B] Consistency** — internal labels (`ch3_→ch4_`, `ch4_→ch5_`) and figure
   directories renamed to the bound chapter order; includegraphics + script
   `FIGDIR` outputs updated; stale banner comments fixed; naming convention
   documented in `README.md`.
5. **[B2] Dead `\figplaceholder` macro** removed.

Final state: full thesis builds clean, **215 pages, 0 undefined references / 0
undefined citations**; standalone chapter builds compile (only the expected
cross-chapter refs are undefined in standalone mode).
