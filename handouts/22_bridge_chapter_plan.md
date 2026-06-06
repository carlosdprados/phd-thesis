<!-- markdownlint-disable-file MD013 -->

# Bridge Chapter — Implementation Plan (standalone, new Chapter 3)

**Date:** 2026-06-06 · **Rev 2** (reassessed after author corrections on the degradation mechanism, the notes as primary source, and full renaming approval).
**Decision (user):** Build the Hybrane→PEO material pivot as a **standalone short chapter**, inserted between current Ch2 and Ch3. Companion assessment: `21_bridge_chapter_hybrane_peo_assessment.md`. Reproducible evidence: `scripts/bridge_hybrane_peo_reproducibility.py` → `handouts/bridge_hybrane_peo_summary.csv`.
**Working title:** *Reproducibility, Degradation, and the Device-Provenance Infrastructure* (alt: *From Hybrane to PEO: A Reproducibility-Driven Materials Pivot*).
**Length:** 12–18 pp. Methods + negative-result chapter, **not** a lab diary.

---

## 0. What changed in Rev 2 (author corrections, now verified)

1. **The degradation is BATCH-over-CALENDAR-TIME, caused by the physical Hybrane reagent stock aging** — *not* individual devices aging after fabrication. The within-device-aging framing of Rev 1 is **dropped** (the >100-day evolution study on v061/v064 exists but is secondary, not the spine).
2. **The real campaign record is in the free-text notes** (`Fabrication Notes`, `Characterization Notes`), not the Y/N columns. I read all 116 Hybrane device notes; they are extraordinarily detailed and are the chapter's primary qualitative source.
3. **Full renaming approved** — renumber chapters and rename `.tex`/Makefile targets freely.

---

## 1. The reproducible quantitative signal (verified against the DATABASE)

The degradation **does** reproduce — but as a **device-health / conductivity collapse**, not as a "smaller normalized loop area" on survivors. From `scripts/bridge_hybrane_peo_reproducibility.py` on SY/Hy/LiTr/Ag:

| Period | devices | fraction broken/saturated | median current @ maxV |
|---|---|---|---|
| Feb–Apr 2021 (pre-inflection) | 23 | **0.58** | **4.6 µA** |
| May–Dec 2021 (decline) | 37 | **1.00** | **946 µA** |
| monthly Jul 2021 / Feb 2022 peaks | — | 1.00 | **3 500 / 13 388 µA** |

- The healthy early device = *low-current (~µA), multi-level, high-area* hysteresis. The degraded device = *high-conductivity short* (current up **100–1000×**), flagged broken/saturated. This is exactly the notes' transition from *"old low-current high-area multi-level behaviour"* to *"high-conductivity, undesirable"* / *"short-circuits"*.
- **Why "smaller area" and "high conductivity" are the same thing:** a near-ohmic high-current device has a thin/closed loop ⇒ small normalized area and lost multi-level steps. So the author's remembered "less area / less multi-stage analog behaviour" = the conductivity collapse measured here.
- **Why normalized-area-alone misses it:** only ~20 of 81 Hybrane/Ag devices survive as non-saturated; the degraded majority are flagged out, so an area-vs-date regression on survivors is flat/positive (r=+0.36, n.s.). **Use the health-collapse metric (Q2), not survivor area, for the quantitative timeline.**

### Honest caveats the chapter must carry
- **Deliberate-stress confound.** The mid-2021 corpus is enriched in *intentionally* stressed/control devices (no-Hybrane, no-salt, air exposure, baby-chamber transport, old-SY). So the 100%-bad rate conflates natural stock-aging with designed stress. Pure calendar/stock effect is **not** cleanly isolable from the DATABASE alone — which is precisely why the team spent ~18 months and ultimately switched hosts.
- **Attribution is a retrospective synthesis.** The contemporaneous notes entertain *multiple* material suspects — Hybrane stock, *old Super Yellow bond degradation*, changing *ITO substrate* lots — not just Hybrane. The clean "it was the Hybrane batch" conclusion is the author's synthesis; the chapter should present the elimination + pragmatic host switch, and locate any definitive attribution in the contemporaneous decks (`EVO.pptx`, `gold&degr.pptx`).
- **Date source.** `UPDATED_DEVICES_LIBRARY.csv` coarsens `Date` to month — use `DEVICES_LIBRARY.csv` for true fabrication dates in any timeline.

### The Hybrane→PEO contrast (the SOLID spine — unchanged)
On valid devices: normalized area median **0.21→0.39**, device-to-device **CV 0.54→0.34**, on-off **1.9→4.3**. PEO restored a *wider, more reproducible* window. This is the evidence-based justification for the switch and rests on replicated valid devices.

---

## 2. The campaign as documented in the notes (primary qualitative source)

The Characterization/Fabrication notes trace the whole investigation. Anchor dates/quotes for the chapter narrative:

- **Inflection — NM_v026–031 (2021-04-22):** *"First devices that changed electrical behaviour … could be evaporation rate … the metal used for evaporation, and possible chemical degradation of substances."* Note explicitly says hypotheses were still open **as of 2022-01-31** → documents ~9+ months of investigation.
- **Systematic confound crossing (each is a real batch):**
  - light vs dark (v015–019, vt001–006, v041–044, v053–056);
  - storage/measurement atmosphere: glovebox vs air vs vacuum (v015–019, v088–099);
  - **baby-chamber transport matrix** — NM_v083–087 (2021-12-02), full 5-way: baby-chamber yes/no × measured in/out glovebox (on Au); and v038–040;
  - **substrate lot/colour** — v079–082 (purple "old year-long"/blue/golden/cyan ITO bands); the substrate-difference study (`Common/2021-11-24_Substrates-Differences`);
  - **old vs new Super Yellow** (v045–048): *"more viscous … maybe because of bonds degradation in the old one"* — the SY co-suspect;
  - old vs new cyclohexanone (v079, v091); evaporation rate & Ag holder (v045–048, v106–113); annealing regime, spin-coat technique, drying.
- **Independent corroboration — NM_v067 (2021-10-21):** *"Lorenzo has the same problems with devices. Maybe the culprit is the different ITO substrates we are getting now."* → a *systemic/material* cause across people, not one operator's technique.
- **>100-day evolution study — v061/v064 (2021-10):** *"measured for more than 100 days, assessing evolution"* (secondary; the within-device aging dataset).
- **Recovery attempts — v106–113 (2022-03→05):** reverted to *"year-ago"* Ag holder / annealing trying to recover the *"old, multiple-level, low-current, high-area"* behaviour vs the new *"high-conductivity, undesirable"* one — never reproducibly restored. Direct evidence that the good behaviour was a *past* state the team was chasing.
- **PEO already entering — v083 (2021-12):** *"Environment was dirty (PEO particles in the atmosphere)"* — dates the host transition.

**Action:** open `Common/2021-12-29_EVO.pptx` and `Common/2021-12-03_gold&degr.pptx` (the contemporaneous evolution/degradation decks) to recover (a) the original area-vs-date timeline figure and its metric, and (b) any explicit Hybrane-stock conclusion. These are the source for the timeline figure (F2). The author confirmed multi-day measurement data exists for devices with `DayX` folders.

---

## 3. Infrastructure to credit (the ~18 months, made visible)

Frame as the methodological backbone consumed by **both** later chapters, not biography (≤2 pp):

- **DEVICES_LIBRARY** — the 88-column per-device fabrication-provenance schema *exists because* the crisis forced pinning every variable (storage atmosphere, light, baby-chamber, SY lot, cyclohexanone lot, operator, evaporation profile, free-text notes). It is the instrument that made the diagnosis possible.
- **project_feature_extraction** (~6 mo) — raw Keithley → `DATABASE/DEVICES_<TYPE>_{DEVICE,PIXEL,CURVE}_INFO.csv`; the `is_broken`/`is_saturated` flags used for the Q2 health metric come from here.
- **project_device_cleaner** — Streamlit curation → `FILTERED_DEVICES.csv` (the per-device visual review that Ch3 already relies on).
- **scripts_general/visualization_tools** — the timeline/`chemvar` viewers behind the contemporaneous degradation diagnosis.
- **project_graphmaker** — thesis-figure generator.
- Canonical as-built description already in repo: `docs/experimental_archive_and_pipeline.md`.

Framing line: *"The diagnosis required instrumentation that did not exist; building it is itself a contribution — and it is the same instrumentation that produces every quantitative result in the comparative and temporal-computing chapters that follow."*

---

## 4. Proposed chapter structure (sections → evidence)

1. **The reproducibility problem.** Scientific question, not confession: the Ch2 proof-of-concept was validated, but as the campaign scaled the memristive hysteresis became progressively harder to obtain — successive batches collapsed toward high-conductivity, low-area behaviour. Anchor on the v026 inflection.
2. **Was it us or the materials? A controlled elimination.** Compact **methods-of-elimination table** (one row per tested cause from §2 → test → verdict). This is where the provenance library is *motivated*. Include the Lorenzo cross-person corroboration.
3. **The quantitative degradation signal.** The health-collapse timeline (F1/F2): fraction broken/saturated → 1.0 and current ↑100–1000× across 2021 batches. State the deliberate-stress and attribution caveats (§1) plainly.
4. **The resolution: switch to PEO.** The Hybrane→PEO contrast (F3): wider, more reproducible window (CV 0.54→0.34). Evidence-based pivot, not arbitrary.
5. **The infrastructure that made the diagnosis possible** (§3) — methods-foundation framing; forward-points to the comparative + temporal chapters.
6. **Reconciliation with Chapter 2 + bridge to the comparative study** (§6 below).

---

## 5. Figures (all reproducible; new folder `figures/chapter3_bridge/`)

- **F1 — device-health collapse**: by month (2021–2022), fraction broken/saturated (bar) + median current on log axis (line). From the Q2 block of the audit script (extend to emit PDF).
- **F2 — the contemporaneous timeline** (the author's remembered figure): area/analog-metric vs fabrication date — **re-digitized/reproduced from `Common/2021-12-29_EVO.pptx`** (or recomputed from raw via feature_extraction). Show as the diagnostic that drove the switch; caption the deliberate-stress caveat.
- **F3 — Hybrane vs PEO contrast**: per-device normalized-area & on-off distributions (box/strip), PEO higher median + tighter spread. From Q1.
- **T1 — methods-of-elimination table** (§2).
- **F4 (optional) — provenance schema / pipeline flow**: adapt `docs/experimental_archive_and_pipeline.md`.

Extend `scripts/bridge_hybrane_peo_reproducibility.py` (or add `scripts/bridge_figures.py`) to render F1/F3 PDFs.

---

## 6. Mandatory reconciliation with Chapter 2 (same pass)

Ch2 §2.7 (`chapters/chapter2_proof_of_concept.tex:437`) attributes *enhanced stability* to "the Hybrane matrix." Partition, don't retract:
- the **published proof-of-concept device** was genuinely stable on the validated ~2-week shelf scale — keep;
- the **batch-scale reproducibility of the Hybrane platform** collapsed over the following year (a *different* metric) — revisited in the new chapter;
- add 1–2 sentences to Ch2 §2.7/summary flagging that batch reproducibility is revisited in the new Ch3, so the reader meets the tension on the author's terms.

---

## 7. Renumbering & renaming mechanics (author approved full rename)

LaTeX cross-refs use labels (`ch:poc`, `ch:comparative`, `ch:temporal`), so numbers auto-update; the work is filenames + docs.

- New file `chapters/chapter3_bridge.tex` with label `\label{ch:bridge}` and the `\ifdefined\thesismode` standalone guard.
- Rename: `chapter3_comparative.tex`→`chapter4_comparative.tex`; `chapter4_temporal.tex`→`chapter5_temporal.tex` (conclusions follow if/when added).
- `thesis.tex`: insert `\include{chapters/chapter3_bridge}` after chapter2 (line ~53) and update the renamed includes.
- `Makefile`: update chapter targets/paths.
- Figures: new chapter under `figures/chapter3_bridge/`; existing Ch3 figures stay put (the comparative chapter keeps its folder even as it becomes Ch4 — or rename for tidiness in the same commit).
- Update Ch2 summary forward-pointer and comparative-chapter back-pointer to `\cref{ch:bridge}`.
- **Docs/memory renumber:** `handouts/01_thesis_structure.md`, `handouts/00_thesis_overview_memory.md`, and memory `thesis_structure.md` from 5- to 6-chapter plan (Intro · PoC · **Bridge** · Comparative · Temporal · Conclusions). Grep handouts/memory for "Chapter 3/4" assumptions.
- Build the full thesis after renaming to confirm numbering/refs resolve.

---

## 8. Risks / verify before drafting

- [ ] **Do not over-claim attribution.** Present multi-suspect elimination + pragmatic host switch; reserve a definitive "Hybrane stock" verdict for what `EVO.pptx`/`gold&degr.pptx` actually concluded.
- [ ] **Carry the deliberate-stress caveat** wherever the 2021 health-collapse numbers appear.
- [ ] **Timeline figure (F2) provenance:** confirm `EVO.pptx` holds the area-vs-date figure and that its data is recoverable; else reconstruct from raw `DayX` folders via feature_extraction (real task, uncertain yield).
- [ ] **Don't deflate Ch2** — the §6 partition is load-bearing.
- [ ] **Length discipline** — elimination = one table + 2–3 paragraphs; infrastructure ≤2 pp.

---

## 9. Execution order (each step = a commit)

1. ✅ Evidence audit (reframed) — `scripts/bridge_hybrane_peo_reproducibility.py` + summary.
2. Open `Common/2021-12-29_EVO.pptx` + `2021-12-03_gold&degr.pptx`; record the original timeline metric/figure and any stock conclusion into this handout.
3. Add F1/F3 PDF rendering; attempt F2 reconstruction.
4. Draft `chapters/chapter3_bridge.tex` (§4), citing only verified numbers (§1) + note quotes (§2).
5. Reconcile Ch2 §2.7 (§6); fix forward/back pointers.
6. Rename files + `thesis.tex` + `Makefile` (§7); build full thesis.
7. Update structure handouts + memory (§7).

---

## 10. Open questions for the user

1. **EVO deck:** does `Common/2021-12-29_EVO.pptx` contain the area-vs-date timeline you remember, with recoverable underlying data — or should the timeline (F2) be reconstructed from the raw `DayX` folders via feature_extraction?
2. **Attribution strength:** how firmly should the chapter conclude it was specifically the *Hybrane stock* vs presenting an honest "multiple material suspects, reproducibility unrecoverable, switched host" — given the notes also implicate old SY and ITO lots?
3. **Conclusions chapter:** the current plan has no Ch5/6 conclusions file yet — should the rename reserve `chapter6_conclusions.tex`, or keep 5 numbered chapters for now?
