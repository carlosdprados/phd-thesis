<!-- markdownlint-disable-file MD013 -->

# Bridge Chapter — Implementation Plan (standalone, new Chapter 3)

**Date:** 2026-06-06 · **Rev 4** (everything re-done WITHIN matched sweep-amplitude strata; two Rev-3 claims dropped as protocol-confounded; v061/v064 stability moved to Ch2 SI).
**Decision (user):** Build the Hybrane→PEO material pivot as a **standalone short chapter**, inserted between current Ch2 and Ch3. Companion assessment: `21_bridge_chapter_hybrane_peo_assessment.md`. Reproducible evidence: `scripts/bridge_hybrane_peo_reproducibility.py` → `handouts/bridge_hybrane_peo_summary.csv`.
**Working title:** *Reproducibility, Degradation, and the Device-Provenance Infrastructure* (alt: *From Hybrane to PEO: A Reproducibility-Driven Materials Pivot*).
**Length:** 12–18 pp. Methods + negative-result chapter, **not** a lab diary.

---

## 0. What changed (author corrections, now verified)

Rev 2 → Rev 3 incorporates the second round of author answers:

1. **The degradation is BATCH-over-CALENDAR-TIME, caused by the physical Hybrane reagent stock aging** — *not* individual devices aging after fabrication.
2. **v061/v064 is NOT degradation evidence — it is the OPPOSITE, and moves to Ch2 SI.** That >100-day study (raw in their `DayX` folders) shows Hybrane *devices* hold their characteristics for weeks — a *positive* of Hybrane-made devices. The **multi-day stability figure belongs in the Ch2 proof-of-concept SI** (author). In the bridge chapter, v061/v064 contribute **only their fresh-day data points** to the feature-vs-fabrication-date scatter (per author's point 3), not their aging curve.
3. **Attribution = the Hybrane stock (firm).** Old vs new Super Yellow did *not* change results significantly and they kept buying new SY, so the SY co-suspect is eliminated. Conclude Hybrane stock (ITO mentioned once by a colleague, but the author's verdict is the Hybrane supply).
4. **The quantitative degradation IS establishable** (author's instruction) — verified in §1 below, including a raw fixed-voltage reconstruction to defeat a sweep-range confound.
5. **The real campaign record is in the free-text notes** (`Fabrication Notes`, `Characterization Notes`), not the Y/N columns. All 116 Hybrane device notes read; primary qualitative source.
6. **Full renaming approved + reserve `chapter6_conclusions.tex`.**

---

## 1. The reproducible quantitative signal — AFTER protocol stratification (`scripts/bridge_hybrane_peo_reproducibility.py`)

**The dominant confound (author).** Hysteresis is a 0→+X→0 loop; a larger sweep amplitude X drives more ionic redistribution, so the device conducts more and shows a different loop area even when read at the same voltage. Amplitude is confounded with **both** date (Hybrane swept ~1.2 V early-2021 → ~3 V later) **and** material (Hybrane mostly ~1.2 V; PEO mostly ~2–3 V). So **every comparison must be made within a matched sweep-amplitude stratum** (binned from `max voltage (V)`). Reading at a fixed voltage from raw does *not* fix this — the *state* at the read still depends on X — so the Rev-3 fixed-1V reconstruction was removed.

**What survives stratification — the chapter's quantitative spine (only these two):**

1. **Resolution — PEO has a wider window than Hybrane at matched ~3 V** (valid devices): normalized area **0.26 (Hy, n=10) → 0.42 (PEO, n=19)**, Mann-Whitney **p=0.018**; on-off **2.45→4.91**. Real, not a protocol artifact.
2. **Degradation — within Hybrane, normalized area at fixed ~1.2 V sweep declines over the campaign**: Spearman **ρ=−0.31, p=0.007 (n=76)**. (At ~3 V the trend is absent, ρ=−0.12, p=0.34 — plausibly the heavy excitation swamps the intrinsic window difference; the gentle 1.2 V sweep is the sensitive probe.)

**What did NOT survive — must be dropped or reported as confounded:**

- **Conductivity rise over time** — within strata ρ=+0.11 (1.2 V, p=0.36) / +0.23 (3 V, p=0.07). The Rev-3 "~90× rise" was substantially the amplitude change. **Do not claim material conductivity increase.**
- **On-off-ratio decline over time** — within strata p=0.14 / 0.17 (n.s.).
- **"PEO more reproducible" (CV 0.54→0.34)** — at matched 3 V the CVs are equal (Hy 0.38, PEO 0.41). The CV gap was the amplitude pooling. **Drop the reproducibility claim;** keep only the window-*magnitude* claim (#1).

**Qualitative only (carry the stress caveat):** device-health collapse — fraction broken/saturated rises ~0.4 → 1.0 across mid-2021. But the mid-2021 corpus is enriched in *deliberately-stressed* controls (no-Hybrane, no-salt, air exposure), so this is narrative support, not a clean stock-aging rate.

**Net:** the honest quantitative basis is **modest but real** — (1) PEO's wider window at matched protocol, and (2) the 1.2 V window decline within Hybrane — plus the overwhelming qualitative campaign record (§2). The mechanism narrative ("composite went ohmic / lost multi-level range") is consistent with the notes and the 1.2 V area decline, but the *magnitude* metrics (conductivity, on-off) are protocol-confounded and must not be quantified as degradation.

**Attribution (firm per author): the Hybrane stock.** SY eliminated (old/new SY no significant change; new SY kept being purchased); the colleague's one-off ITO remark was not borne out. Use `DEVICES_LIBRARY.csv` for true dates (`UPDATED_…` coarsens to month).

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
- **Independent corroboration — NM_v067 (2021-10-21):** *"Lorenzo has the same problems with devices"* → a *systemic/material* cause across people, not one operator's technique. (The same note guesses ITO; the author's verdict is the Hybrane supply.)
- **Positive device-level stability — v061/v064 (2021-10), raw in their `DayX` folders:** *"measured for more than 100 days, assessing evolution"*. The **opposite** of degradation: Hybrane *devices* retain characteristics for weeks/months → the device physics was fine; the **supply** degraded. The multi-day curve → **Ch2 SI**; only the fresh-day points enter the bridge timeline.
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
3. **The quantitative degradation signal.** Lead with the **only surviving quantitative metric**: normalized-area decline at fixed ~1.2 V sweep (ρ=−0.31, p=0.007). Present the protocol-confound explicitly as a *methodological result* of the chapter (amplitude sets the response in these ionic devices) — it both disciplines this analysis and connects to the comparative chapter's protocol message. Health-collapse as qualitative support (stress caveat). Conductivity/on-off trends explicitly flagged as protocol-confounded, not claimed.
4. **The resolution: switch to PEO.** The Hybrane→PEO contrast at **matched ~3 V** (F3): wider window, normalized area 0.26→0.42 (p=0.018), on-off 2.45→4.91. Evidence-based pivot. **No reproducibility-CV claim** (confounded). Attribution: Hybrane stock (SY eliminated).
5. **The infrastructure that made the diagnosis possible** (§3) — methods-foundation framing; forward-points to the comparative + temporal chapters.
6. **Reconciliation with Chapter 2 + bridge to the comparative study** (§6 below).

---

## 5. Figures (all reproducible; new folder `figures/chapter3_bridge/`)

- **F1 — degradation timeline (headline)**: normalized area vs fabrication date, **coloured by sweep-amplitude stratum**, showing the significant decline within the ~1.2 V points (ρ=−0.31) and the flat ~3 V points — i.e. the figure *also visualises the protocol confound*. Fresh-day points include v061/v064. From audit Q2.
- **F2 — device-health collapse** (qualitative): fraction broken/saturated by month → 1.0. From Q4; caption the deliberate-stress caveat.
- **F3 — Hybrane vs PEO at matched ~3 V**: per-device normalized-area & on-off distributions (box/strip) within the 3 V stratum only, PEO higher (p=0.018). From Q1.
- **T1 — methods-of-elimination table** (§2).
- **F4 (optional) — provenance schema / pipeline flow**: adapt `docs/experimental_archive_and_pipeline.md`.
- **[Ch2 SI, not here] — v061/v064 multi-day stability** curve.

Add `scripts/bridge_figures.py` to render F1–F3 PDFs into `figures/chapter3_bridge/`. Optionally cross-check F1 against `Common/2021-12-29_EVO.pptx` for narrative consistency.

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
- Rename: `chapter3_comparative.tex`→`chapter4_comparative.tex`; `chapter4_temporal.tex`→`chapter5_temporal.tex`; **reserve `chapter6_conclusions.tex`** (author-approved) — stub it now with `\chapter{Conclusions}\label{ch:conclusions}` so the structure is locked.
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

1. ✅ Evidence audit (stratification-first, Q1–Q4) — `scripts/bridge_hybrane_peo_reproducibility.py` + summary.
2. Add `scripts/bridge_figures.py` → F1–F3 PDFs into `figures/chapter3_bridge/`. (Optional: cross-check F1 vs `Common/2021-12-29_EVO.pptx`.)
3. Draft `chapters/chapter3_bridge.tex` (§4), citing only the surviving stratified numbers (§1) + note quotes (§2).
4. Reconcile Ch2 §2.7 (§6); add the v061/v064 multi-day stability figure to **Ch2 SI**; fix forward/back pointers.
5. Rename files + stub `chapter6_conclusions.tex` + `thesis.tex` + `Makefile` (§7); build full thesis.
6. Update structure handouts + memory (§7).

---

## 10. Resolved decisions (author, 2026-06-06)

1. **Timeline figure** — reconstruct quantitatively from the DATABASE + raw (F1, done in the audit script); the area-vs-date story is now confound-controlled. EVO deck is an optional narrative cross-check, not the data source.
2. **Attribution = Hybrane stock** (firm). SY eliminated. v061/v064 used to show device-level stability (supply, not device, degraded).
3. **Reserve `chapter6_conclusions.tex`** — yes.

Nothing outstanding blocks drafting. Remaining build-time tasks: the figure PDFs (F1–F3) and the v061/v064 multi-day stability figure for **Ch2 SI** (raw `DayX` reconstruction).

**Key methodological lesson (Rev 4):** sweep amplitude dominates these ionic devices and is confounded with both date and material — so the chapter's quantitative claims are deliberately narrow (1.2 V window decline; matched-3 V PEO advantage), and the protocol-confound itself becomes a stated methodological result rather than a buried caveat.
