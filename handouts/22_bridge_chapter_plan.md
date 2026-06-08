<!-- markdownlint-disable-file MD013 -->

# Bridge Chapter — Implementation Plan (standalone, new Chapter 3)

**Date:** 2026-06-06 · **Rev 5** (mature methodology honoring the procedure: per-device weighting + standard-protocol corpus + amplitude match + recovery-tail sensitivity; degradation re-established on a controlled multi-feature panel; mirrors `project_feature_explorer`).
**Decision (user):** Build the Hybrane→PEO material pivot as a **standalone short chapter**, inserted between current Ch2 and Ch3. Companion assessment: `21_bridge_chapter_hybrane_peo_assessment.md`. Reproducible evidence: `scripts/bridge_hybrane_peo_reproducibility.py` → `handouts/bridge_hybrane_peo_summary.csv`.
**Working title:** *Reproducibility, Degradation, and the Device-Provenance Infrastructure* (alt: *From Hybrane to PEO: A Reproducibility-Driven Materials Pivot*).
**Length:** 12–18 pp. Methods + negative-result chapter, **not** a lab diary.

---

## 0. What changed (author corrections, now verified)

**Rev 5 (mature methodology).** Per the author's procedural points, the degradation analysis now enforces four controls (see §1A), mirroring the interactive tool `Nanomem_Devices_Library/project_feature_explorer`. Net effect: the conductivity-rise + potentiation-loss degradation **re-establishes robustly** once the standard-protocol corpus is isolated and per-device weighting is used (it had looked confounded in Rev 4 because the wrong, pixel-pooled, all-corpus metric was used). The normalized-area/on-off decline is real but tail-driven; `broken %` is *not* a valid degradation metric. Earlier rev history retained below for traceability.

Standing author corrections (Rev 2–4):

1. **The degradation is BATCH-over-CALENDAR-TIME, caused by the physical Hybrane reagent stock aging** — *not* individual devices aging after fabrication.
2. **v061/v064 is NOT degradation evidence — it is the OPPOSITE, and moves to Ch2 SI.** That >100-day study (raw in their `DayX` folders) shows Hybrane *devices* hold their characteristics for weeks — a *positive* of Hybrane-made devices. The **multi-day stability figure belongs in the Ch2 proof-of-concept SI** (author). In the bridge chapter, v061/v064 contribute **only their fresh-day data points** to the feature-vs-fabrication-date scatter (per author's point 3), not their aging curve.
3. **Attribution = the Hybrane stock (firm).** Old vs new Super Yellow did *not* change results significantly and they kept buying new SY, so the SY co-suspect is eliminated. Conclude Hybrane stock (ITO mentioned once by a colleague, but the author's verdict is the Hybrane supply).
4. **The quantitative degradation IS establishable** (author's instruction) — verified in §1 below, including a raw fixed-voltage reconstruction to defeat a sweep-range confound.
5. **The real campaign record is in the free-text notes** (`Fabrication Notes`, `Characterization Notes`), not the Y/N columns. All 116 Hybrane device notes read; primary qualitative source.
6. **Full renaming approved + reserve `chapter6_conclusions.tex`.**

---

## 1. The reproducible quantitative signal (`scripts/bridge_hybrane_peo_reproducibility.py`)

### 1A. Four controls the analysis MUST enforce (each verified to matter)

1. **Per-device weighting (mandatory).** `number_pixels_measured` collapses 16 → 2 over the campaign and is strongly anti-correlated with date (**Spearman ρ=−0.80, p≈1×10⁻¹⁵**). Pixel-pooled statistics are therefore biased toward early devices. Reduce every feature to **one value per device** (median over its freshest-day curves) *before* any test. NB: the `DEVICE_INFO` `saturated/broken pixel %` columns are unpopulated/constant — compute health from curve-level `is_saturated`/`is_broken`.
2. **Standard-protocol corpus only** (n=69): SY/Hy/LiTr/Ag, anneal **75 °C**, no 2nd stage, Hy **0.3**, LiTr **0.09**. Excludes the invasive experiments — above all the **150 °C high-temperature batch that PARTIALLY RECOVERED devices a year in** (author), plus composition variants — which would otherwise contaminate the feature-vs-date story.
3. **Sweep-amplitude match.** A 0→+X→0 loop excites the device more at larger X, so it conducts more even when read at the same voltage; amplitude is confounded with date *and* material. Confine within-Hybrane trends to a **tightly matched ~1.2 V band** (the standard corpus sweeps at discrete 0.6/1.0/1.2/2.6/3.0 V; 1.0–1.45 V is the matched low-V probe). Draw the Hybrane↔PEO contrast at matched ~3 V.
4. **Recovery-tail sensitivity.** Report every trend with and without the last months (≥2022-03), the deliberately-reverted recovery batches.

### 1B. Read each feature at the amplitude where it is *expressed*

A subtle but decisive point: **window features (on-off ratio, normalized area) only open up at high sweep amplitude.** At ~1.2 V they sit near unity for *every* device (early or late) and cannot show a collapse; they must be read in the **~3 V stratum**. Conductivity features are read in the matched **~1.2 V** band. And because the notes place a behavioural **inflection at NM_v026 (2021-04-22)**, the window collapse is a step there — tested as **early (≤Apr 2021) vs later** (Mann-Whitney), which is more faithful and more powerful than a whole-campaign correlation.

**HEADLINE — switching-window collapse at ~3 V (standard corpus, per-device, pre/post inflection):**

| Feature | early (≤Apr 2021) | later | Mann-Whitney |
|---|---|---|---|
| on-off ratio | **2.44** (n=10) | **1.21** (n=42) | **p=0.0019** |
| normalized area | **0.235** | **0.027** | **p=0.0005** (~9×) |
| % change in max-V current (potentiation) | **+17.9 %** | **−2.1 %** | **p=0.013** |

on-off → ~1.2 *and* normalized area → ~0.03 *and* potentiation flipping positive→negative are the **same functional event**: the device loses its switching window and therefore its potentiation capability (the author's point — no on-off ratio ⇒ no potentiation ⇒ ruined device). This matches the recollection of "~2.5 early → 1–1.7 later" and is anchored to the documented inflection. (Pixel-info cross-check: on-off 2.33→1.26.)

**MECHANISM — ohmic drift at matched ~1.2 V (per-device Spearman vs date; strengthens dropping the recovery tail):**

| Feature | all dates | drop recovery tail |
|---|---|---|
| current at max V | ρ=+0.45, p=0.0002 | ρ=+0.55, p<0.0001 |
| raw area V·µA | ρ=+0.57, p<0.0001 | ρ=+0.69, p<0.0001 |
| current diff at on-off | ρ=+0.51, p<0.0001 | ρ=+0.63, p<0.0001 |

Absolute current rises within tightly matched amplitude (so it is material aging, not the sweep change): the composite drifts toward more ohmic conduction. Window collapse (relative hysteresis →0) + ohmic drift (absolute current ↑) are two faces of the same degradation.

**Health flags:** `is broken` *decreases* over time (ρ=−0.40, p=0.001) — it tracks early electrode-contact/handling problems the team fixed (the notes are full of them), so it is **not** a Hybrane-degradation metric; the right one is `is saturated` (fails-to-potentiate), which rises (ρ=+0.27, p=0.03). This corrects the initial expectation that "broken %" worsened.

Two earlier mis-calls now fixed: Rev 4 called conductivity "confounded" because it used a single-point `conductance at max V` on all-corpus pooled pixels; Rev 5 called the window decline "tail-driven" because it read window features at 1.2 V with a whole-campaign correlation. Read at the expressing amplitude with the pre/post-inflection contrast, **both the window collapse and the ohmic drift are strong and significant.**

### 1C. Resolution — why PEO (the positive turn of the story)

Two distinct, both-defensible wins (and a clear statement of what "reproducible" means here):

1. **Better features (wider/stronger window).** At matched ~3 V, valid devices: normalized area **0.26 (Hy) → 0.42 (PEO)**, Mann-Whitney **p=0.018**; on-off **2.45 → 4.91**.
2. **Temporal reproducibility — the actual crisis solution.** PEO/Ag sustained a *usable* switching window across **~2.5 years** (2022→2024, n=46): on-off @3 V median **2.61** (yearly 3.3 / 2.6 / 1.9, no significant trend, ρ=−0.21 p=0.16). Hybrane sat at **1.35** after its stock-driven collapse to ~1.2. PEO simply did **not** exhibit the supply-degradation failure — that is the reproducibility win.

**Be precise about "reproducible":** it is *temporal/batch* reproducibility (no stock collapse over years), **not** a within-batch device-to-device CV claim — at matched 3 V the CVs are only modestly different (PEO 0.38 vs Hy 0.47). Do not over-state CV; lead on temporal stability + window magnitude.

### 1D. Attribution & data notes

**Hybrane stock (firm):** SY eliminated (old/new SY no significant change; new SY kept being bought); the colleague's one-off ITO guess was not borne out. Use `DEVICES_LIBRARY.csv` for true dates (`UPDATED_…` coarsens to month). The mechanism — drift to ohmic conduction + loss of potentiation — matches the notes' *"old low-current, high-area, multi-level"* → *"high-conductivity, undesirable"* transition.

### 1E. Mechanistic hypothesis (include as a clearly-labelled hypothesis, ~½ page)

The chapter should offer a *candidate chemistry*, not a proven one — the rest of the thesis is mechanistic, so a black-box "the stock went bad" is a gap a jury will probe; but a definitive answer is **not supportable** (no EIS on any Hybrane device — verified 0 rows; no GPC/NMR/Karl-Fischer of the stock; the aged stock no longer exists). Frame strictly as hypothesis + the experiments that would confirm it.

**Leading hypothesis — moisture-driven hydrolytic aging of the hyperbranched polyester-amide Hybrane stock.** Hybrane is ester/amide-rich and strongly hygroscopic; over ~a year in the bottle it takes up water and slowly hydrolyses (chain scission). This accounts for *all* the measured signatures:

- **Ohmic drift** (current ↑ at matched 1.2 V): absorbed water + polar scission products raise baseline ionic/leakage conductivity and plasticise the matrix.
- **Window + potentiation collapse** (on-off → ~1.2, area → ~0.03, %ΔI → −2 %): memristance needs a matrix stiff enough to *hold* a field-displaced ionic profile (the Ch2 metastable-polarisation picture). A plasticised, lower-MW, water-laden host relaxes/leaks, so the loop closes and successive sweeps stop building up.
- *(secondary)* acidic hydrolysis products could partially **dope the PPV-type Super Yellow**, adding a fixed irreversible conductance — another route to "high-conductivity, undesirable."

**Internal support already in hand:**

1. **Annealing recovery (quantified, suggestive).** Among late (degraded-era) devices, aggressive **150 °C annealing restores the 3 V window** — on-off median **1.95 (n=6) vs 1.22 (n=44)** standard-75 °C late, **Mann-Whitney p=0.024**, back to ~early-standard level (1.74). Driving off absorbed water / re-densifying the film is the natural explanation; a handling-only or inert-stock story does not predict this. *(Caveat: n=6, co-varying tweaks, 2 devices had measurement-pin issues — present as suggestive.)*
2. The full **electrical signature** (ohmic drift + window/potentiation collapse) is the textbook fingerprint of a water-plasticised, ion-leaky film.
3. The **material class** (hyperbranched polyester-amide) is hydrolytically labile and hygroscopic by construction.

**Confirming experiments to list as future work / SI:** FTIR (ester C=O loss, –OH growth) and GPC (MW drop) on *retained aged vs fresh* stock; Karl-Fischer / TGA for water content; EIS to show Rion fell. None were run on the Hybrane corpus, so the hypothesis stays open — and, honestly, may never fully close because it concerns a consumable that no longer exists in its aged state.

Reproduced by the `mechanism_annealing_recovery` block of `scripts/bridge_hybrane_peo_reproducibility.py`.

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

## 3. The methodological legacy — the positive turn, carried forward

This is a **forward-looking, positive** beat, not just credit for past effort: the crisis *forced* a methodological apparatus into existence, and that apparatus became the standard machinery for the entire rest of the thesis (Ch3 comparative, Ch4 temporal) and the group beyond. Frame it as "the crisis paid a lasting dividend." (≤2 pp.) Five durable outputs:

- **A fabrication-provenance standard — DEVICES_LIBRARY.** The 88-column per-device schema *exists because* the crisis forced pinning every variable (storage atmosphere, light, baby-chamber, SY/cyclohexanone lot, operator, evaporation profile, free-text notes). It made the diagnosis possible and is now the permanent record for every device.
- **A normalized electrical-characterization procedure.** A hard lesson of §1A/§1C is that *protocol sets the response* (sweep amplitude, pulse/read scheme). The campaign converged on fixed, documented protocols (the HYST/PULSES/DELAYTIME schemes used throughout Ch3/Ch4) so that devices and batches are finally comparable — the methodological precondition for the comparative chapter.
- **A data pipeline for hundreds–thousands of tests — project_feature_extraction** (~6 mo): raw Keithley → `DATABASE/DEVICES_<TYPE>_{DEVICE,PIXEL,CURVE}_INFO.csv`; every feature in the §1B panel and in Ch3/Ch4 comes from here.
- **Visualization / trend-discovery tools — project_feature_explorer** (Dash; the tool with which the trends were originally found; §1 controls reproduce its slicing), **project_device_cleaner** (Streamlit curation → `FILTERED_DEVICES.csv`), and **scripts_general/visualization_tools** (timeline/`chemvar` viewers). These turn the archive into discoverable trendlines.
- **project_graphmaker** — thesis-figure generation. Canonical as-built description: `docs/experimental_archive_and_pipeline.md`.

Framing line: *"The diagnosis required instrumentation that did not exist; building it — provenance capture, a normalized characterization procedure, an automated feature pipeline, and trend-discovery tooling — is itself a contribution, and it is the same instrumentation that produces every quantitative result in the comparative and temporal-computing chapters that follow."* So the Hybrane failure is, in the end, what made the rest of the thesis measurable.

---

## 4. Proposed chapter structure (sections → evidence)

1. **The reproducibility problem.** Scientific question, not confession: the Ch2 proof-of-concept was validated, but as the campaign scaled the memristive hysteresis became progressively harder to obtain — successive batches collapsed toward high-conductivity, low-area behaviour. Anchor on the v026 inflection.
2. **Was it us or the materials? A controlled elimination.** Compact **methods-of-elimination table** (one row per tested cause from §2 → test → verdict). This is where the provenance library is *motivated*. Include the Lorenzo cross-person corroboration.
3. **The quantitative degradation signal.** Open with the four controls (§1A) as the chapter's *methodological backbone* (per-device weighting — pixels/device fell 16→2; standard-protocol corpus; amplitude match; tail sensitivity). Headline = **switching-window + potentiation collapse at 3 V** (on-off 2.44→1.21, normalized area 0.235→0.027, %ΔI +18%→−2%; §1B); **mechanism** = ohmic drift at matched 1.2 V (current/area rise); **chemical hypothesis** = §1E (moisture-driven hydrolytic stock aging) with the annealing-recovery test. Note `broken %` is a handling metric, not degradation.
4. **The resolution: why PEO (the positive turn).** Two wins (§1C): **better features** — wider window at matched 3 V (area 0.26→0.42, p=0.018; on-off 2.45→4.91); and **temporal reproducibility** — PEO sustained a usable window (on-off ~2.6) across ~2.5 years (2022–2024) with no stock-driven collapse, which is the crisis solved. State "reproducible" precisely (temporal/batch, not within-batch CV). Attribution: Hybrane stock (SY eliminated).
5. **The methodological legacy carried forward (§3).** The crisis's lasting dividend: the provenance standard (DEVICES_LIBRARY), the normalized characterization procedure, the feature pipeline, and the trend-discovery tooling — the same apparatus that produces every quantitative result in the comparative and temporal-computing chapters. Frame as the positive going-forward beat, not biography.
6. **Reconciliation with Chapter 2 + bridge to the comparative study** (§6 below).

---

## 5. Figures (all reproducible; new folder `figures/chapter3_bridge/`)

- **F1 — degradation panel (headline)**: per-device features vs fabrication date on the standard corpus, matched ~1.2 V — (a) current/raw-area RISE (conductivity, log axis); (b) % change in max-V current FALLS (potentiation). Mark the recovery-tail devices distinctly (excluded from the fit). Fresh-day points include v061/v064. From §1B.
- **F2 — per-device weighting & confound visual**: `number_pixels_measured` vs date (ρ=−0.80) and a small sweep-amplitude×date panel — makes the methodology (why per-device + amplitude match) legible to the jury.
- **F3 — Hybrane vs PEO at matched ~3 V**: per-device normalized-area & on-off distributions (box/strip), PEO higher (p=0.018). From §1C.
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
- Completed rename: `chapter3_comparative.tex`→`chapter4_comparative.tex`; `chapter4_temporal.tex`→`chapter5_temporal.tex`; `chapter6_conclusions.tex` reserved and drafted.
- `thesis.tex`: insert `\include{chapters/chapter3_bridge}` after chapter2 (line ~53) and update the renamed includes.
- `Makefile`: update chapter targets/paths.
- Figures: bridge chapter under `figures/chapter3/`; comparative figures under `figures/chapter4/`; temporal-computing figures under `figures/chapter5/`.
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
