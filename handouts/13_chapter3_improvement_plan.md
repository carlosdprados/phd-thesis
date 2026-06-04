<!-- markdownlint-disable-file MD013 -->

# Chapter 3 — Improvement Plan

**Date:** 2026-06-04  
**Purpose:** Convert the Chapter 3 audit into an actionable plan for strengthening the chapter as a thesis chapter and as a possible future publication basis.

> **Progress (2026-06-04, critically verified):**
> - **#1 protocol correction — DONE & VERIFIED.** Confirmed from `DEVICES_*_PIXEL_INFO.csv`: composition PULSES are **3 V/1.5 V** (32/32), DELAYTIME **4 V/2 V** (30/32; v114 is the 3 V/6 V overlay). Added **Table 3.1** (per-measurement protocols), fixed the §3.2 prose and the §3.4 "common 4 V/2 V" claim, and **sharpened limitation #4 + the Ch4 caveat** to the real point: φ (3 V) and λ (4 V) are at *different write amplitudes*, so the Ch4 composition assumes a compatibility the protocol result shows is only approximate. Builds clean (chapter + thesis).
> - Remaining items triaged below; figures (#3–#5) and prose (#6–#7) next, supplementary (#8–#11) deferred as genuinely supplementary.

## Executive Direction

Chapter 3 already has the correct central structure: the replicated `SY/PEO/LiTr/Ag` composition grid is the quantitative spine; host, anion and cation comparisons are an illustrative chemistry landscape; and the drive-protocol result is a methodological warning and design rule.

The main work now is not to invent a new headline. It is to improve protocol precision, show representative raw behaviour, make variability visible, and move archive/provenance details into a clean methods or supplementary structure.

## Main-Chapter Additions

### 1. Correct and clarify the electrical protocols

**Priority:** highest  
**Placement:** `Materials, Devices, and Measurement Protocol` and/or `Methods of Analysis`

The current chapter compresses the modern protocol too much. It states that potentiation and delay-time measurements share the common `4 V write / 2 V read` protocol, but the DATABASE indicates:

- **DELAYTIME:** mostly `4 V` write / `2 V` read, `30` pulses, `0.103 s` spacing.
- **PULSES/N-pulse:** mostly `3 V` write / `1.5 V` read, variable `N <= 1000`, `0.104 s` spacing, `0.155 s` read delay.
- **Protocol-amplitude comparison:** same-device `NM_v114` remains valid as the drive-protocol result: `3 V / 1.5 V` versus `6 V / 3 V`.

**Action:**

- Replace the broad protocol paragraph with a small table separating HYST, PULSES, and DELAYTIME.
- Explicitly state that pulse integration and forgetting are measured in separate protocols, so Chapter 4 composes them as behavioural ingredients.
- Re-check figure captions that call the composition grid a uniform `4 V/2 V` protocol. That is safe for DELAYTIME, but not for PULSES.

**Acceptance criterion:** a reader can tell exactly which voltage/read protocol produced HYST, PULSES, DELAYTIME, chemistry bars, and the protocol-overlay figure.

### 2. Add a data-provenance and QA schematic

**Priority:** high  
**Placement:** end of Methods, or first figure in Methods if space allows

The archive has a strong provenance story that is currently mostly outside the chapter:

```text
DEVICES_LAB_DATA
  -> project_feature_extraction
  -> DATABASE/*.csv
  -> project_device_cleaner / FILTERED_DEVICES.csv
  -> ch3_png_qa_curation.csv
  -> scripts/ch3_4_dynamics_fits.py
  -> ch3_decay_by_cell.csv / ch3_pulses_by_cell.csv / figures
```

**Action:**

- Add a compact schematic or table showing the raw-to-figure pipeline.
- Name the key reproducibility artifacts:
  - `docs/experimental_archive_and_pipeline.md`
  - `handouts/ch3_png_qa_curation.csv`
  - `scripts/ch3_4_dynamics_fits.py`
  - `scripts/ch3_figures.py`
  - `handouts/ch3_decay_by_cell.csv`
  - `handouts/ch3_pulses_by_cell.csv`

**Acceptance criterion:** the reader understands that the figures are not hand-assembled from cherry-picked PNGs; the curation registry is machine-readable and applied automatically.

### 3. Add representative raw/fit curves

**Priority:** high  
**Placement:** main Chapter 3, likely immediately before or after the composition heatmaps

The chapter currently uses summary heatmaps and bars. It needs at least one figure showing what the measurements look like.

**Recommended figure:**

- Panel A: representative HYST curves for low-PEO/long-memory and high-PEO/fast-memory cells.
- Panel B: representative PULSES curves showing strong growth, compressive growth, and turnover.
- Panel C: representative DELAYTIME curves with fitted/stated `t_{1/2}` or stretched-exponential overlay.

**Candidate contrasts:**

- `PEO 0.3 / salt 0.045` or `0.09`: strong potentiation, long retention.
- `PEO 0.6` or `1.2`: faster relaxation and weaker response.
- Include a low-salt turnover case and a high-salt sustained-growth case if possible.

**Acceptance criterion:** a reader can visually understand `on-off ratio`, `alpha`, `peak ratio`, `turnover`, and `t_{1/2}` before reading the heatmap summaries.

### 4. Add a heterogeneity/variability figure

**Priority:** high  
**Placement:** composition results or Discussion

The text already frames variability as useful reservoir heterogeneity, but the current figures mostly show cell medians. Add a figure that makes spread visible.

**Recommended figure options:**

- Swarm/box plot of `t_{1/2}` by composition.
- Swarm/box plot of pulse growth exponent `alpha` and peak ratio by composition.
- Optional overlay of device-level points on top of heatmap-style medians.

**Action:**

- Use device-level data from `handouts/ch4_decay_fits.csv` and `handouts/ch4_pulse_descriptors.csv`.
- Show cell medians plus individual devices.
- Keep chemistry points separate or visually labelled as illustrative only.

**Acceptance criterion:** the chapter no longer only says variability is a resource; it shows the distribution that Chapter 4 will exploit.

### 5. Add a design-space scatter plot

**Priority:** high-to-medium  
**Placement:** bridge to Chapter 4 or Discussion

The bridge currently states that fading-memory time and input nonlinearity are coupled through PEO fraction, while salt partly controls dynamic range and turnover. This can be made much stronger with a visual.

**Recommended figure:**

- `x`: pulse growth exponent `alpha`, peak ratio, or turnover `N_peak`.
- `y`: fading-memory time `t_{1/2}`.
- Color: PEO mass fraction.
- Marker shape or outline: salt mass fraction.
- Optional marker size: peak ratio.

**Expected message:**

- PEO does not independently tune memory and nonlinearity; each composition selects a paired operating point.
- Salt acts more like a dynamic-range/turnover lever.
- Chapter 4 should assemble a bank of compositions rather than search for a single optimum.

**Acceptance criterion:** the design-rule paragraph in the bridge is supported by a direct visual summary.

## Prose and Interpretation Improvements

### 6. Expand the physical hypothesis

**Priority:** medium  
**Placement:** Discussion

Current physical interpretation is defensible but terse. Add a cautious mechanism paragraph:

- Increasing PEO may dilute or interrupt the SY electronic percolation pathway, reducing the switching window and pulse-driven conductance modulation.
- Higher ion-host fraction may also allow ionic redistribution to relax more readily, shortening memory.
- Lower PEO/SY-richer compositions may generate stronger electronic bottlenecks, deeper interfacial charge redistribution, or slower relaxation.
- Salt content may set the number of chargeable/mobile ionic states before saturation or over-potentiation, explaining why high salt suppresses turnover to larger pulse counts.
- Host/anion effects likely reflect coordination strength, ion-pairing, segmental mobility, and the distribution of local activation barriers.

**Constraint:** frame this as a working hypothesis, not a proven microscopic mechanism. Avoid turning HSAB into a quantitative law.

### 7. Make the protocol-dependence result more explicit as a design rule

**Priority:** medium  
**Placement:** protocol section and Discussion

The protocol result should do two jobs:

- It explains why chemistry comparisons cannot be treated as powered material laws.
- It is a positive design rule: apparent memory time is co-set by material and drive.

**Action:**

- Tie the `NM_v114` result more directly to supra-threshold read/write disturbance.
- State that any future cross-chemistry comparison must fix composition, electrode, write amplitude, read amplitude, pulse count, and timing.
- Note that sub-threshold reads are the cleaner future protocol.

## Supplementary or Appendix Material

### 8. Add a coverage and attrition table

**Priority:** medium  
**Placement:** supplementary/appendix, with a short main-text pointer

The archive starts broad and narrows substantially after protocol matching and QA. This is important context.

**Recommended table:**

- Total device library count.
- Ch3-relevant chemistry counts.
- Devices with HYST/PULSES/DELAYTIME.
- Devices surviving FILTERED exclusion.
- Devices surviving PNG/fit curation.
- Final `n` per composition and chemistry cell.

**Source artifacts:**

- `handouts/ch3_coverage_audit.csv`
- `handouts/ch3_ch4_device_inventory.csv`
- `handouts/ch4_device_manifest_DRAFT.csv`
- `handouts/ch3_decay_by_cell.csv`
- `handouts/ch3_pulses_by_cell.csv`

**Acceptance criterion:** the evidence-tier distinction is auditably visible, not just asserted.

### 9. Add profilometry as context/confound control

**Priority:** medium-to-low  
**Placement:** supplementary/appendix, with optional one-sentence main-text note

Profilometry exists and should be acknowledged because thickness may vary with composition.

**Observed context from DATABASE:**

- PEO/LiTr/Ag lower-PEO cells are often around `~200-250 nm`.
- Higher-PEO cells are often closer to `~300 nm`.

**Action:**

- Add a table or small heatmap of median film thickness by composition.
- State that thickness was recorded but not modelled as an independent variable.
- Treat it as a limitation/confound rather than a result unless a dedicated analysis shows otherwise.

### 10. Keep EIS mostly supplementary unless a clear analysis is added

**Priority:** medium-to-low  
**Placement:** supplementary/appendix

EIS exists in the archive and `v247-v252` have EIS rows, but the current Chapter 3 claims are not built on EIS.

**Action:**

- Add an SI note that EIS is available but not used as a replicated comparative axis.
- Do not use it to support a mechanism unless a dedicated EIS comparison is performed and passes the same protocol/electrode/sample-size discipline.
- Clarify the Gamry-vs-SR865A distinction if impedance is discussed.

### 11. Move full archive and folder details to supplementary

**Priority:** medium  
**Placement:** supplementary/appendix

The following are useful but too detailed for the main flow:

- Raw Keithley file formats.
- `DEVICES_LAB_DATA` quarter/device/day/pixel hierarchy.
- Device-folder naming drift and why `UPDATED_DEVICES_LIBRARY.csv` is canonical.
- `FILTERED_DEVICES.csv` semantics: exclusion list, not a good-device list.
- The fact that the working pipeline is CSV/TXT, not consolidated HDF5/Parquet.
- Which data types exist but are not used as Chapter 3 claims: VCONST, EIS, AFM/IR/UV-Vis placeholders, lock-in HDF5 side data.

**Acceptance criterion:** Chapter 3 remains readable, while the thesis still documents the data infrastructure well enough for reproducibility.

## Figure Roadmap

### Main Chapter

1. **Existing:** composition heatmaps: HYST window and fading time.
2. **Existing:** potentiation grid: `alpha`, peak ratio, turnover.
3. **Existing:** chemistry landscape bars.
4. **Existing:** protocol overlay.
5. **Add:** representative raw/fit curves for HYST, PULSES, DELAYTIME.
6. **Add:** heterogeneity/swarm plot across composition cells.
7. **Add if space allows:** design-space scatter linking `t_{1/2}` with `alpha`, peak ratio, or turnover.

### Supplementary

1. Coverage/attrition ledger.
2. Full per-device fit table.
3. Curation-registry summary.
4. Profilometry thickness table/heatmap.
5. Optional EIS availability note or exploratory plots.
6. Full data-provenance and archive map.

## Text Edits Checklist

- [ ] Split protocol description by HYST, PULSES, DELAYTIME.
- [ ] Remove or qualify any statement implying PULSES and DELAYTIME share the same write/read amplitude.
- [ ] Add the raw-to-summary data-provenance schematic/table.
- [ ] State explicitly how medians are computed: curve/pixel/device/cell aggregation.
- [ ] State that HYST summaries use robust medians because on-off ratios are right-skewed.
- [ ] Add a physical-hypothesis paragraph in Discussion.
- [ ] Strengthen the link between variability and Chapter 4.
- [ ] Add a short statement that profilometry exists and thickness is a possible confound.
- [ ] Keep chemistry conclusions explicitly illustrative.
- [ ] Keep the cation result as an honest negative: no host/anion-independent `Li > Na > K` law.

## Recommended Execution Order

1. Fix protocol prose and captions first. This is the only item that affects correctness.
2. Add the representative raw/fit curve figure.
3. Add the heterogeneity or design-space figure.
4. Expand Discussion with the physical hypothesis and design-rule framing.
5. Add supplementary coverage/provenance/profilometry material.
6. Rebuild chapter and thesis PDFs.

## Open Decisions

- Whether the representative raw/fit curves should be one figure or split into one composition figure plus one chemistry/protocol figure.
- Whether the heterogeneity plot and design-space plot both fit in the main chapter, or whether one should move to Chapter 4.
- Whether to do an EIS analysis now or explicitly reserve EIS for supplementary context/future work.
- Whether to create a formal supplementary information chapter/file or append these materials to an appendix.

