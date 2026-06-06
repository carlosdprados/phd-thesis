<!-- markdownlint-disable-file MD013 -->

# Bridge Chapter — Implementation Plan (standalone, new Chapter 3)

**Date:** 2026-06-06 · **Rev 3** (quantitative degradation now verified incl. raw fixed-voltage reconstruction; v061/v064 reframed; Hybrane-stock attribution firmed; Ch6 reserved).
**Decision (user):** Build the Hybrane→PEO material pivot as a **standalone short chapter**, inserted between current Ch2 and Ch3. Companion assessment: `21_bridge_chapter_hybrane_peo_assessment.md`. Reproducible evidence: `scripts/bridge_hybrane_peo_reproducibility.py` → `handouts/bridge_hybrane_peo_summary.csv`.
**Working title:** *Reproducibility, Degradation, and the Device-Provenance Infrastructure* (alt: *From Hybrane to PEO: A Reproducibility-Driven Materials Pivot*).
**Length:** 12–18 pp. Methods + negative-result chapter, **not** a lab diary.

---

## 0. What changed (author corrections, now verified)

Rev 2 → Rev 3 incorporates the second round of author answers:

1. **The degradation is BATCH-over-CALENDAR-TIME, caused by the physical Hybrane reagent stock aging** — *not* individual devices aging after fabrication.
2. **v061/v064 is NOT degradation evidence — it is the OPPOSITE.** That >100-day study (raw data in their `DayX` folders) shows Hybrane *devices* hold their characteristics for weeks after fabrication — a *positive* property of Hybrane-made devices. It supports the Ch2 shelf-stability claim and the "Hybrane was excellent until the *supply* degraded" framing. Pull it out of the degradation section; cite it as positive device-level stability.
3. **Attribution = the Hybrane stock (firm).** Old vs new Super Yellow did *not* change results significantly and they kept buying new SY, so the SY co-suspect is eliminated. Conclude Hybrane stock (ITO mentioned once by a colleague, but the author's verdict is the Hybrane supply).
4. **The quantitative degradation IS establishable** (author's instruction) — verified in §1 below, including a raw fixed-voltage reconstruction to defeat a sweep-range confound.
5. **The real campaign record is in the free-text notes** (`Fabrication Notes`, `Characterization Notes`), not the Y/N columns. All 116 Hybrane device notes read; primary qualitative source.
6. **Full renaming approved + reserve `chapter6_conclusions.tex`.**

---

## 1. The reproducible quantitative signal (verified; `scripts/bridge_hybrane_peo_reproducibility.py`)

The degradation reproduces and is **quantitatively establishable** across three consistent, mutually reinforcing measures on the SY/Hy/LiTr/Ag corpus (all 77 devices with HYST, saturated devices INCLUDED — they are signal, not noise):

**(a) Switching window shrinks over the campaign (sweep-range-robust shape metrics).** Device-level (freshest day), Spearman vs fabrication date:

- normalized loop area: **ρ=−0.32, p=0.004**
- on-off ratio: **ρ=−0.31, p=0.006**

**(b) Conductivity rises ~90× over the campaign (raw fixed-voltage reconstruction).** The processed "current/conductance at max V" is **confounded**: the median sweep range jumped from **1.2 V (Feb–Apr 2021) to 3 V (mid-2021 on)**, and those features are read *at* max V. Reconstructing conductance at a **fixed |V| = 1.0 V** from the raw datapoint table (`DEVICES_HYST_ALL_DATAPOINTS.csv`, streamed) removes the confound. Over the **core campaign Feb 2021–Feb 2022 (n=67)**:

- conductance@1V: **Spearman ρ=+0.59, p≈1×10⁻⁷**; log-linear **≈1.47×/month** ⇒ **~90× over the year** (median ≈4 µS → ≈360 µS).
- The 2022 *recovery* batch (v104–113, deliberately reverted conditions) is **excluded** (anomalously low, ~0.02 µS; documented in the notes); including it washes the trend out, so it must be shown as a separate coda, not pooled.

**(c) Device-health collapse (the blunt summary metric).** Fraction of pixels flagged broken/saturated rises from ~0.4–0.68 (Feb–Apr 2021) to **1.00 every month May 2021→Feb 2022**.

These cohere into one mechanism: as the Hybrane stock aged, the composite became progressively **more conductive / ohmic** (b, c), so the hysteresis loop closed and lost its multi-level analogue range (a). This is exactly the notes' *"old low-current, high-area, multi-level behaviour"* → *"high-conductivity, undesirable / short-circuit"* transition. "Smaller area" and "more conductive" are the same physical event.

### Honest caveats the chapter must carry
- **Deliberate-stress confound.** The mid-2021 corpus is enriched in *intentionally* stressed/control devices (no-Hybrane, no-salt, air exposure, baby-chamber transport). So the health metric (c) over-states pure stock-aging; lead instead on (a) the sweep-robust window collapse and (b) the fixed-voltage conductivity rise, which are device-level trends across the natural batch sequence.
- **Sweep-range confound (handled).** Never use "current/conductance at max V" for the timeline — use the fixed-1V reconstruction (b). Use `DEVICES_LIBRARY.csv` (not `UPDATED_…`, which coarsens Date to month) for true dates.
- **Attribution (firm per author): the Hybrane stock.** SY eliminated (old/new SY no significant change; new SY kept being purchased). State Hybrane-supply degradation as the conclusion; mention the colleague's one-off ITO remark only as a contemporaneous alternative that was not borne out.

### The Hybrane→PEO contrast (the SOLID resolution)
On valid devices: normalized area median **0.21→0.39**, device-to-device **CV 0.54→0.34**, on-off **1.9→4.3**. Switching to fresh PEO host restored a *wider, more reproducible* window — the evidence-based justification for the pivot, on replicated devices.

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
- **Positive device-level stability — v061/v064 (2021-10), raw in their `DayX` folders:** *"measured for more than 100 days, assessing evolution"*. This is the **opposite** of the degradation story — it shows Hybrane *devices* retain their characteristics for weeks/months, a desirable property. Use it to make the point sharply: the device physics was fine; the **supply** degraded. Reconcile with Ch2's shelf-stability claim rather than contradict it.
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
3. **The quantitative degradation signal.** Lead with the sweep-robust window collapse (area ↓ p=0.004, on-off ↓ p=0.006) and the fixed-1V conductivity rise (~90× over the year, ρ=+0.59, p≈1e-7); health-collapse as the blunt summary. Carry the deliberate-stress and sweep-range caveats (§1). **Contrast with v061/v064**: individual devices were stable for >100 days, so this is *supply* degradation across batches, not device instability.
4. **The resolution: switch to PEO.** The Hybrane→PEO contrast (F3): wider, more reproducible window (CV 0.54→0.34). Evidence-based pivot, not arbitrary. Attribution: Hybrane stock (SY eliminated).
5. **The infrastructure that made the diagnosis possible** (§3) — methods-foundation framing; forward-points to the comparative + temporal chapters.
6. **Reconciliation with Chapter 2 + bridge to the comparative study** (§6 below).

---

## 5. Figures (all reproducible; new folder `figures/chapter3_bridge/`)

- **F1 — degradation timeline (headline)**: per-device, vs fabrication date — (a) normalized area ↓ and on-off ↓; (b) conductance@1V ↑ (~90×, log axis), with the 2022 recovery batch marked as an excluded coda. All from the audit script Q1/Q3/Q4 (extend to emit PDF). This is the quantitative version of the author's remembered "area vs date" figure, now confound-controlled.
- **F2 — device-health collapse** (blunt summary): fraction broken/saturated by month → 1.0. From Q2; caption the deliberate-stress caveat.
- **F3 — Hybrane vs PEO contrast**: per-device normalized-area & on-off distributions (box/strip), PEO higher median + tighter spread. From Q1.
- **F4 — positive device stability (v061/v064)**: a feature (area/conductance) vs *days since fabrication* staying flat over >100 days — the counterpoint that isolates *supply* (not device) degradation. Reconstruct from their raw `DayX` folders.
- **T1 — methods-of-elimination table** (§2).
- **F5 (optional) — provenance schema / pipeline flow**: adapt `docs/experimental_archive_and_pipeline.md`.

Extend `scripts/bridge_hybrane_peo_reproducibility.py` (or add `scripts/bridge_figures.py`) to render F1–F4 PDFs. Optionally cross-check F1 against the contemporaneous `Common/2021-12-29_EVO.pptx` deck for narrative consistency.

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

1. ✅ Evidence audit (Q1–Q4, incl. raw fixed-V reconstruction) — `scripts/bridge_hybrane_peo_reproducibility.py` + summary.
2. Add `scripts/bridge_figures.py` to render F1–F3 PDFs into `figures/chapter3_bridge/`; reconstruct F4 from the v061/v064 `DayX` raw folders. (Optional: cross-check F1 vs `Common/2021-12-29_EVO.pptx`.)
3. Draft `chapters/chapter3_bridge.tex` (§4), citing only verified numbers (§1) + note quotes (§2).
4. Reconcile Ch2 §2.7 (§6); fix forward/back pointers.
5. Rename files + stub `chapter6_conclusions.tex` + `thesis.tex` + `Makefile` (§7); build full thesis.
6. Update structure handouts + memory (§7).

---

## 10. Resolved decisions (author, 2026-06-06)

1. **Timeline figure** — reconstruct quantitatively from the DATABASE + raw (F1, done in the audit script); the area-vs-date story is now confound-controlled. EVO deck is an optional narrative cross-check, not the data source.
2. **Attribution = Hybrane stock** (firm). SY eliminated. v061/v064 used to show device-level stability (supply, not device, degraded).
3. **Reserve `chapter6_conclusions.tex`** — yes.

Nothing outstanding blocks drafting. The only remaining build-time tasks are the figure PDFs (F1–F4) and the raw `DayX` reconstruction for F4.
