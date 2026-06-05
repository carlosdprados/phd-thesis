<!-- markdownlint-disable-file MD013 -->

# Fabrication-Confound Audit — Do Ch3/Ch4 Effects Really Come from Chemistry/Composition?

**Author:** Carlos David Prado-Socorro · **Date:** 2026-06-05 · **Status:** complete
**Reproduce:** `python3 scripts/fabrication_confound_audit.py`
**Sources of truth:** `DATABASE/DEVICES_LIBRARY.csv` (88 fabrication columns, 1 row/device), `DATABASE/UPDATED_DEVICES_LIBRARY.csv` (`Components Group`), `DATABASE/DEVICES_DELAYTIME_PIXEL_INFO.csv` (measurement `day`), and the per-device cell map in `handouts/ch4_decay_fits.csv` + `ch4_pulse_descriptors.csv`.

## Purpose

Chapters 3 and 4 attribute the measured changes in parameters/features (switching window, potentiation strength/turnover, fading-memory time τ/t½) to deliberate changes in **composition** (PEO/LiTr mass fraction) and **chemistry** (host, anion, cation). This audit asks the jury's question: *could some other fabrication variable, recorded per device, be the real driver?* It walks **every** column of `DEVICES_LIBRARY.csv` for the **exact 61 devices** that feed Ch3/Ch4 and classifies each variable as (i) held constant → cannot confound; (ii) varying but **crossed** with composition (spans all levels) → not a confound; or (iii) varying and **covarying/confounded** with the axis of interest.

Three confounds were already settled and are **not** re-litigated here: spin-coat RPM / film thickness (handout 14 + `scripts/thickness_rpm_audit.py`), write/read protocol amplitude (handout 08 §13), and electrode metal Ag vs Au (handout 08 §16, §23b). This audit covers **everything else**.

---

## 1. Composition spine (Li / Ag, n=30) — verdict: **claims stand, very well controlled**

### 1.1 Held constant across all 30 spine devices (cannot confound composition)

The decisive result of the audit. The following are **identical** for every device in the composition grid, so none can explain the composition trends:

- **Device architecture:** `Device Type = Vertical`; `Substrate = ITO` (ITO3 / ITO3-16 are the 8- vs 16-pixel layout of the same ITO substrate); junction unchanged.
- **Semiconductor:** `SY mass ratio = 1` and `SY final concentration = 8.71–8.73 mg/mL` (0.2 % spread → effectively constant). No PVK/F8BT/MEHPPV. No MoS₂.
- **Only one ion conductor (PEO) and one salt (LiTr):** every other ion-polymer and salt column is `NA` — so the only electrolyte variables present are the two design axes themselves.
- **Annealing:** `Annealing Temperature = 75 °C` for all; **no second-stage anneal** (all `NA`). (Anneal *time* is the one near-exception — see §1.3.)
- **Electrode:** `Ag thickness = 100 nm`; no Au/Al; **metal evaporation done by the same person (CDPS)** for all.
- **Atmosphere / humidity:** `Storage in Glovebox = Y` **and** `Measurements in Glove Box = Y` for **all** devices. This is important — PEO is hygroscopic and water plasticises ion transport, but every spine device was stored *and* measured under glovebox atmosphere, so ambient humidity is controlled out.
- **Process hygiene:** `Solvent = cyclohexanone`, `Dark Vials = N`, `UV-Ozone = N`, `Dried substrate = N`, `Spin time = 60 s`, `Hot-plate ramp = Y`, `Filtered Salt = N`, `Scratched ITO = N`, `Sample-holder contact board = Y` — all constant.

### 1.2 Crossed with PEO (varies, but spans all composition levels) → not confounds

- **Fabrication date / batch (6 dates):** every replicated cell is built from **multiple independent batches** (2022-11, 2023-02, 2023-03, 2023-10, 2024-06). The composition trend reproduces *across* batches, operators, and SY lots — a strength, not a confound.
- **Operator** (`Who Prepared Solutions` / `Who Performed Spin-Coating`: CDPS for 2022+2024, DDDT for 2023): each composition cell contains both operators → crossed.
- **Measurement age (aging):** median delay-measurement day = **3 for every PEO level**; within each batch *all* PEO levels are measured on the **same day** (2022-11 batch all day 10; 2023-02/03 all day 3; 2023-10 all day 5; 2024-06 all day 1). Aging is crossed, not confounded.
- **Solution mixing times** (SY-soln agitation 19 vs 139 h; final-soln 1/24/26 h), **cooldown after anneal** (30/1099/4320 min), **applied volume** (0.35–0.45 mL), **evaporation rates** (per-run scatter; Ag thickness fixed): all vary by batch logistics and span PEO levels; none track PEO monotonically. (Applied volume is largely irrelevant in static spin-coating — excess is flung off.)
- **QA defect flags** (`Faulty Spin Coating Coverage`, `Fallen Substrate`, `Features Remained`): isolated `Y`s, handled downstream by FILTERED + the curation registry, not composition-linked.

### 1.3 The single strongest control

Within the **2022-11-17 batch** (one day, one operator CDPS, one SY lot, one anneal, **constant RPM = 2000** for all six devices), composition is the *only* thing that varies, and the trend is fully present:

| device | PEO | salt | RPM | t½ (s) | τ (s) |
|---|---|---|---|---|---|
| v140 | 0.3 | 0.09 | 2000 | 18.6 | 17.2 |
| v142 | 0.6 | 0.09 | 2000 | 2.9 | 0.4 |
| v144 | 1.2 | 0.09 | 2000 | 6.0 | 5.5 |
| v143 | 0.6 | 0.18 | 2000 | 4.3 | 2.8 |
| v145 | 1.2 | 0.18 | 2000 | 11.2 | 10.0 |

Because RPM (hence thickness) is **held constant** here, higher PEO → thicker film *and* shorter retention — yet in the 2023-10 batch RPM was *escalated* with PEO (1500→2900, partially equalising thickness) and the **same** trend holds. The composition effect therefore survives whether or not thickness is compensated, independently corroborating handout 14's partial-correlation result.

### 1.4 Residual items a jury could raise (all minor; documented)

1. **Anneal time 3 h vs 3.5 h.** The 3.5 h value appears **only** in the 2023-03 batch (v152–157), which is entirely PEO 0.6/1.2 — so longer anneal *partially coincides* with higher PEO. **Mitigation:** every one of those high-PEO cells *also* has 3 h-anneal replicates (2023-10, 2024-06) giving the same short retention, so the 3.5 h is not the driver. Worth a one-line acknowledgement.
2. **Old SY used (Y) in the 2023-02 & 2023-03 batches** (v146–157). Aged semiconductor could shift electronic transport. **Mitigation:** these are crossed with fresh-SY replicates at every replicated cell; the PEO trend is present in the fresh-SY-only batches (2022-11, 2023-10, 2024-06). The only cells resting *solely* on old-SY devices are the **PEO 0.15 row** (v150/v151) — which the chapter already treats as outside the replicated grid (n=1, curation-salvaged).
3. **Weighing precision at the low-mass corner.** Fabrication notes flag ±2–5 % mass error; this is worst at PEO 0.3/salt 0.045 (smallest absolute masses). This is x-axis uncertainty on the composition axis, not a confound, but it partly explains the large within-cell scatter there (e.g. v259 t½ 3.3 s vs v260 36.7 s).
4. **Light incidence / storage history varies** (some devices sat on a hotplate under light for 3 days pre-evaporation; most stored in glovebox without light). Crossed with composition, but an uncontrolled aging-style variable worth listing alongside §1.4.2.

---

## 2. Chemistry landscape (host / anion / cation) — verdict: mixed, already labelled illustrative

The chapter already restricts these to an *illustrative* tier (n ≤ 2 per matched cell). The audit clarifies **which comparisons are clean and which carry an additional fabrication confound**:

- **Cation series are excellent same-batch comparisons.** Every cation triplet was fabricated on a **single day with identical process**, swapping *only* the salt cation:
  - PEO/triflate (v247/248/249) — 2023-10-17, RPM 2000, identical.
  - TMPE/triflate (v250/251/252) — 2023-10-17, RPM 2000, identical.
  - PEO/TFSI (v321–326) — 2025-03-13, RPM 3000, identical.
  - TMPE/TFSI (v333–338) — 2025-05-14, RPM 3000, identical.
  - old PEO/triflate (v114/115/116) — 2022-05-26, CDPS, identical.

  → The honest-negative cation conclusion ("no robust host/anion-independent Li>Na>K") is a **genuine chemistry result, not a fabrication artifact** — the strongest part of the landscape, methodologically.

- **Host (PEO vs TMPE) carries a residual batch confound.** The *designed* clean test is the 2023-10-17 2-host × 3-cation matrix — but the **PEO-Li corner (v247) is the broken/discarded device**, so the cleanest within-batch PEO-vs-TMPE *Li* pair is unavailable. The chapter's "PEO ~20–25 s (n=3) vs TMPE ~4 s (n=1)" therefore compares PEO-Li (v140/v146/v241) against TMPE-Li (v250) **across batches**. *Mitigation:* v241 (PEO-Li, 2023-10-05) vs v250 (TMPE-Li, 2023-10-17) is a near-matched contrast (same month, operator DDDT, fresh SY, glovebox; RPM 1500 vs 2000) and still shows ~6×. Recommend stating that the within-batch Li host pair was lost to a broken device and the host claim leans on a near-matched cross-batch pair.

- **Anion (triflate vs TFSI) is the most weakly controlled comparison.** PEO/triflate (v140/146/241, 2022–2023, RPM 2000–2100, unfiltered salt) vs PEO/TFSI (v321, 2025-03, **RPM 3000**, **Filtered Salt = Y**). So the anion swap is *also* a ~2.5-year, RPM-2000→3000, and unfiltered→filtered-salt change. The ~20× shortening is large and the comparison is explicitly illustrative, but these co-varying process differences should be named. (RPM/thickness is already shown not to drive retention; filtered salt should only *help* the TFSI side.)

---

## 3. Bottom line

- **Composition spine (the quantitative core of Ch3 and the parameter cards behind every Ch4 number): no new confound found.** All major fabrication levers — annealing, electrode, atmosphere/humidity, salt filtering, semiconductor loading, solvent — are held constant; the rest (batch, operator, SY lot, aging, mixing, cooldown) are crossed with composition; and a single-batch, constant-RPM control reproduces the trend on its own. Nothing in Ch3/Ch4 needs to change. This strengthens, and does not contradict, handout 14.
- **Chemistry landscape: cation comparisons are clean (same-batch); host and especially anion comparisons carry additional cross-generation process differences (RPM, year, filtered salt, and a broken within-batch PEO-Li device).** These are already in the "illustrative, n≤2" tier, but the specific extra confounds are worth one or two added sentences in §3.6 (Chemistry) / §3.8 (Limitations) for full jury-proofing.

## 4. Suggested (small) text additions — optional

1. Ch3 §3.6/§3.8: note that the host PEO-vs-TMPE Li contrast lost its within-batch pair (v247 broken) and leans on a near-matched cross-batch pair; and that the anion triflate→TFSI contrast also spans a change in spin speed, fabrication generation, and salt filtering.
2. Ch3 §3.8 (or the materials paragraph): one clause stating that annealing temperature, electrode, and glovebox storage/measurement atmosphere were held constant across the composition grid, and that batch, operator, and SY lot are crossed with composition (so the trend is reproduced within single batches). This converts an implicit strength into an explicit, defensible statement.

See [[14_thickness_rpm_confound_audit]] and `handouts/08_chapter3_4_claims_audit.md` §13/§16/§23 for the previously-closed confounds.
