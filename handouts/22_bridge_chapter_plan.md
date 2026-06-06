<!-- markdownlint-disable-file MD013 -->

# Bridge Chapter — Implementation Plan (standalone, new Chapter 3)

**Date:** 2026-06-06
**Decision (user, 2026-06-06):** Build the Hybrane→PEO material pivot as a **standalone short chapter**, inserted between the current Ch2 and Ch3. Companion assessment: `21_bridge_chapter_hybrane_peo_assessment.md`.
**Working title:** *Reproducibility, Degradation, and the Device-Provenance Infrastructure* (alt: *From Hybrane to PEO: A Reproducibility-Driven Materials Pivot*).
**Target length:** 12–18 pp. Methods + negative-result chapter, **not** a lab diary.

---

## 0. Headline guidance (read first)

The chapter must be built on **what the data actually supports**, which is *not* exactly the remembered narrative. I re-derived this directly from the regenerated DATABASE (May 2025) via `scripts/bridge_hybrane_peo_reproducibility.py` → `handouts/bridge_hybrane_peo_summary.csv`:

- **SOLID — the spine of the chapter.** On the silver corpus, after the red-flag exclusion list and dropping broken/saturated pixels, PEO is both *more reproducible* and *stronger* than Hybrane:
  - normalized hysteresis area: Hybrane median **0.21, CV 0.54** → PEO median **0.39, CV 0.34**;
  - on–off ratio: Hybrane **1.93** → PEO **4.33**.
  - This is the defensible, quantitative justification for the switch: PEO gives a wider switching window with lower device-to-device scatter.
- **SUPPORTING (small n).** Within-device aging: of Hybrane devices tracked ≥3 days, **78 % lose normalized area over days post-fabrication** (median slope −0.015 /day, n=9). PEO has *no* device tracked ≥3 days — multi-day aging campaigns were concentrated on Hybrane, which is itself part of the story.
- **HONEST NULL — do not claim.** The remembered "normalized area vs **calendar date** declines across 2021" trend does **not** reproduce in this DATABASE slice: Hybrane early-day area vs calendar time is flat (Pearson r=+0.04, p=0.91; Spearman ρ=+0.36, p=0.28, n=11). Only 20 of 81 silver Hybrane devices have clean HYST in the regenerated tables, so the slice is small and the original timeline was likely made live on a larger/raw slice.

**Consequence for framing:** lead with the *Hybrane-vs-PEO reproducibility/window contrast* (solid) + *within-device aging* (supporting). The calendar-time degradation timeline may be shown **only** if it can be reproduced from the contemporaneous primary record (`Common/2021-12-29_EVO.pptx`, `Common/2021-12-03_gold&degr.pptx`); otherwise present it as the contemporaneous diagnostic that *motivated* the campaign, explicitly flagged as not re-derivable from the final DATABASE slice. Never assert a clean monthly decline as a result.

---

## 1. Source-of-truth inventory (every claim must point here)

All paths relative to the sibling data root `Nanomem_Devices_Library/` unless noted.

| Element | Source of truth | Notes |
|---|---|---|
| Material/era decode | `DATABASE/UPDATED_DEVICES_LIBRARY.csv` — `Components Group`, `Used Metal`, `Date` | 353 devices; Hybrane corpus = 116 (SY/Hy/LiTr ×105), span **2021-02 → 2022-05**, 98 in 2021 |
| Per-device fabrication provenance | `DATABASE/DEVICES_LIBRARY.csv` — 88 columns | the library that *is* the infrastructure story |
| HYST metrics | `DATABASE/DEVICES_HYST_PIXEL_INFO.csv` — `normalized area mean`, `on-off ratio mean`, `day` | day = days since fabrication |
| Curation / red-flags | `DATABASE/FILTERED_DEVICES.csv` | exclusion list (~230 rows), hand-flagged in device_cleaner; possibly incomplete |
| Confound campaign (codified) | library columns 75–80 (see §2) | the campaign survives *as data*, not anecdote |
| Confound campaign (contemporaneous analysis) | `Common/` artifacts (see §2) | primary records for figures/timeline |
| Pipeline as-built | repo `docs/experimental_archive_and_pipeline.md` (13.7 kB) | canonical shareable description; chapter methods draw from it |
| Verified statistics | `scripts/bridge_hybrane_peo_reproducibility.py` + `handouts/bridge_hybrane_peo_summary.csv` | reproducible; re-run before drafting numbers |

---

## 2. The confound-elimination campaign is codified in the data

These are real, queryable variables in `DEVICES_LIBRARY.csv` (counts on the 116 Hybrane devices) — this is what lets the chapter present a *methods-of-elimination table* rather than a story:

- **Light Incidence after Fabrication** — Y=98 / N=18 (deliberate light vs dark)
- **Storage in Glovebox after Fabrication** — Y=93 / N=23 (deliberate degradation vs protected)
- **Measurements in Glove Box** — Y=63 / N=34 (measurement atmosphere)
- **Storage Inside Baby Chamber after Fabrication** — N for all Hybrane (the "baby chamber" cylinder variable was introduced/used on later, non-Hybrane devices — verify before attributing it to the Hybrane crisis)
- **Old SY Used** — Y=37 / N=28 / blank=51 (semiconductor lot aging)
- **Used Dark Vials** — Y=6 (light during solution prep)
- **Substrate Type** — uniform `ITO3-16` across the Hybrane set; the substrate-difference study lives in `Common/2021-11-24_Substrates-Differences` + `Substrates-Differences25112021.xlsx`

Contemporaneous analysis artifacts in `Common/` (primary record for figures and the "we systematically eliminated causes" narrative):

- `2021-12-29_EVO.pptx` — device **evolution over time** (the likely origin of the area-vs-date timeline)
- `2021-12-03_gold&degr.pptx` — gold electrode & **degradation**
- `2021-11-24_Substrates-Differences/`, `Subtrates-Differences.docx/.pptx` — substrate study
- `Zona muerta/` — "dead-zone" study; `v140ish_ConcVar/`, `ConcVar_Hyst_Preview2.odp` — concentration variation; `Efecto-Copa.ods` — "cup effect"

**Action:** open the `.pptx/.ods` artifacts (or ask the user) to recover (a) which confounds were tested and their verdicts, (b) whether the EVO timeline is the area-vs-date figure, and (c) the deliberate-degradation result. Build the elimination table from these + the library columns.

---

## 3. The infrastructure to credit (the ~18 months made visible)

Pitch as the methodological backbone consumed by **both** later chapters, not biography. Accurate, from memory + verification:

- **DEVICES_LIBRARY** — 88-column per-device fabrication provenance schema (composition, spin/anneal, evaporation rates, storage/measurement atmosphere, operator-who-did-what, free-text notes). Born *because* the crisis demanded pinning every fabrication variable. `UPDATED_DEVICES_LIBRARY.csv` adds convenience categoricals (`Components Group`, `Used Metal`, mass ratios).
- **project_feature_extraction** — raw Keithley `D1_*.txt` → `DATABASE/DEVICES_<TYPE>_{DEVICE,PIXEL,CURVE}_INFO.csv` + `ALL_DATAPOINTS.csv` for HYST/PULSES/DELAYTIME/EIS/VCONST/profilometry. ~6 months of programming.
- **project_device_cleaner** — Streamlit curation app → `FILTERED_DEVICES.csv` red-flag exclusion list; the visual per-device review that Ch3 §3.3 already relies on (the "curation registry").
- **scripts_general/visualization_tools** — hyst/nyquist/bode/chemvar/temporal viewers; the timeline viewers behind the contemporaneous degradation diagnosis.
- **project_graphmaker** — thesis-figure generator.

Framing line for the chapter: *"The diagnosis required instrumentation that did not exist; building it is itself a contribution, and it is the same instrumentation that produces every quantitative result in Chapters 4 and 5."*

---

## 4. Proposed chapter structure (sections → evidence)

1. **Introduction — the reproducibility problem.** State the puzzle: the Ch2 proof-of-concept (SY/Hybrane/LiOTf) was validated, but as the campaign scaled, the hysteresis response became harder to reproduce (smaller loop area, weaker analog multi-stage behaviour). Frame as a scientific question, not a confession.
2. **Was it us or the material? A controlled elimination.** Compact **methods-of-elimination table** (one row per tested cause: light, measurement/storage atmosphere, substrate lot, SY lot/age, solution prep, deliberate degradation) → test → verdict. Built from library columns §2 + `Common/` artifacts. This is where the provenance library is *motivated*.
3. **The verdict: the host, not the procedure.** Two evidential legs:
   - within-device aging (78 % negative area-vs-day slopes, Hybrane; n=9) — supporting;
   - the Hybrane→PEO contrast (window 0.21→0.39, CV 0.54→0.34, on-off 1.9→4.3) — the decisive, replicated leg.
   Conclusion: an evidence-based switch to PEO for a wider, more reproducible window.
4. **The infrastructure that made the diagnosis possible** (§3) — library, feature_extraction, device_cleaner/curation, visualization. Methods-foundation framing; forward-points to Ch4/Ch5 reliance.
5. **Reconciliation with Chapter 2 + bridge to the comparative study.** Explicitly partition the claims (see §5 below) and hand off to the PEO composition grid.

---

## 5. Mandatory reconciliation with Chapter 2 (do in the same pass)

Current Ch2 §2.7 (`chapters/chapter2_proof_of_concept.tex:437`) attributes *enhanced stability* to "the Hybrane matrix" (≈300 h shelf, <15–20 % variability). Left unqualified this contradicts the bridge chapter. Fix by partitioning, not retraction:

- The **published proof-of-concept device** was stable on the validated ~2-week ambient-shelf scale — keep that claim, it stands.
- The **broader campaign** exposed device-to-device irreproducibility and within-device aging of the *Hybrane composite as a fabrication platform* — a *different* metric (batch reproducibility / aging) from the single-device shelf retention reported in Ch2.
- Add one or two sentences to Ch2 §2.7 (or its summary) flagging that batch-scale reproducibility is revisited in the new Ch3, so the reader meets the tension on the author's terms.

---

## 6. Figures (candidates; all reproducible)

- **F1 — Hybrane vs PEO contrast** (the headline): paired panels of per-device normalized-area and on-off distributions (box/strip), showing PEO's higher median + tighter spread. From `bridge_hybrane_peo_reproducibility.py` (extend to emit a PDF).
- **F2 — within-device aging**: normalized area vs day post-fabrication for Hybrane devices with ≥3 days, with per-device regression lines (78 % negative).
- **F3 — the elimination table** (table, not figure) — from §2.
- **F4 — the provenance schema** — a schematic/annotated excerpt of the 88-column library + the raw→DATABASE→curated pipeline flow (can adapt `docs/experimental_archive_and_pipeline.md`).
- **F5 (conditional) — the EVO timeline**: area (or analog-behaviour metric) vs calendar date — **only if** reproducible from `Common/2021-12-29_EVO.pptx` primary data; otherwise cite as the contemporaneous diagnostic.

Extend `scripts/bridge_hybrane_peo_reproducibility.py` (or a new `scripts/bridge_figures.py`) to render F1–F2 as PDFs into `figures/chapter3_bridge/`. Keep the current Ch3 figures under their existing folder; the new chapter gets its own.

---

## 7. Renumbering mechanics (accurate)

- LaTeX cross-references in the `.tex` sources use **labels** (`\cref{ch:poc}`, `ch:comparative`, `ch:temporal`), so inserting a chapter **auto-renumbers within the build** — no manual edit of in-text references.
- Concrete edits:
  - new file `chapters/chapter3_bridge.tex` (mirror the `\ifdefined\thesismode` standalone guard used by the others);
  - add `\include{chapters/chapter3_bridge}` in `thesis.tex` between lines 53–54 (after chapter2, before chapter3_comparative);
  - **rename for clarity (optional but recommended):** `chapter3_comparative.tex`→`chapter4_comparative.tex`, `chapter4_temporal.tex`→`chapter5_temporal.tex`, and update the four `\include` lines + `Makefile` targets. (Filenames are cosmetic; labels carry the refs.)
  - give the new chapter a label e.g. `\label{ch:bridge}`; update the Ch2 summary forward-pointer and Ch(now 4) intro back-pointer to `\cref{ch:bridge}`.
- **Documentation renumber (the real cost):** update `handouts/01_thesis_structure.md`, `handouts/00_thesis_overview_memory.md`, and memory `thesis_structure.md` from a 5-chapter to a 6-chapter plan (Intro · PoC · **Bridge** · Comparative · Temporal · Conclusions). Search handouts/memory for "Chapter 3"/"Chapter 4" references that assume the old numbering.

---

## 8. Risks / things to verify before drafting

- [ ] **Calendar-trend claim:** do NOT assert it. Recover the EVO timeline from `Common/2021-12-29_EVO.pptx`; if it can't be reproduced, frame as contemporaneous-diagnostic-only.
- [ ] **Baby chamber:** all Hybrane devices are `Storage Inside Baby Chamber = N`. Confirm with the user whether baby-chamber experiments belong to the Hybrane crisis (likely later/PEO). If not, mention it as a transport-degradation control in the campaign narrative but don't attribute it to the Hybrane verdict.
- [ ] **Small clean-HYST n (20/81 Hybrane):** state sample sizes explicitly; consider whether more Hybrane HYST can be recovered by re-running feature_extraction on skipped 2021-Q1 folders (pipeline scope = year ≥2021 + requires `_(...)` descriptor; some early devices skipped).
- [ ] **PEO aging blank:** PEO has no ≥3-day device — so "PEO ages less" is *not* shown, only "PEO starts wider and more uniform." Phrase accordingly.
- [ ] **Don't deflate Ch2:** the partition in §5 is load-bearing.
- [ ] **Length discipline:** elimination campaign = one table + 2–3 paragraphs, not a per-batch narrative.

---

## 9. Execution order (each step = a commit)

1. ✅ Evidence audit script + summary (`scripts/bridge_hybrane_peo_reproducibility.py`) — done.
2. Recover the confound-campaign verdicts + EVO timeline from `Common/` artifacts (read the `.pptx/.ods` or ask the user); write findings into this handout.
3. Extend the script to emit F1–F2 PDFs into `figures/chapter3_bridge/`.
4. Draft `chapters/chapter3_bridge.tex` (sections §4), citing only §0-verified numbers.
5. Reconcile Ch2 §2.7 (§5) and fix forward/back pointers.
6. Renumber files + `thesis.tex` + `Makefile` (§7); build the full thesis to confirm numbering/refs.
7. Update structure handouts + memory (§7).

---

## 10. Open questions for the user

1. **EVO timeline:** does `Common/2021-12-29_EVO.pptx` contain the "normalized area vs date" figure you remember, and is its underlying data available to reproduce? (Decides whether F5/the calendar story is shown as a result or as motivation only.)
2. **Baby chamber:** was the baby-chamber (transport-degradation) experiment part of the *Hybrane* crisis or a later PEO/TMPE-era control? (Library says Hybrane = all N.)
3. **Scope of "infrastructure" section:** keep it tight (1–2 pp, methods-foundation framing) — confirm you don't want a full software/architecture treatment that would tip the chapter toward an engineering report.
4. **Filename renaming:** OK to rename `chapter3_comparative.tex`→`chapter4_comparative.tex` etc. for clarity, or keep filenames and let only the printed numbers shift?
