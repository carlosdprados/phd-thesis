<!-- markdownlint-disable-file MD013 -->

# Chapter 4 — Data, Protocols and Analysis Pipeline Specification

**Author:** Carlos David Prado-Socorro  
**Date:** April 12, 2026  
**Status:** Specification document. Defines exactly which datasets exist across the PEO/triflate comparative corpus, where they live, which measurement protocols are common across the corpus, and which analysis outputs are required before Chapter 4 writing starts. This document is the contract between the experimental archive and Chapter 4.

**v3 (2026-04-12) — correction of scope.** Earlier revisions described the comparative corpus as an Ag-electrode NM_vXXX series employing LiTFSI / NaTFSI / KTFSI salts in a Hybrane-class / TMPE host. That description was inherited from a stale planning note and does not reflect the real archive. The actual comparative corpus is a PEO-based triflate series: a PEO/LiTr concentration sub-study plus a PEO/LiTr, PEO/NaTr, PEO/KTr fixed-composition set at PEO and salt mass fractions of 0.3 and 0.09. TMPE-based composites and alkali-TFSI (LiBis / NaBis / KBis) devices exist but are *exploratory* and are explicitly excluded from the Chapter 4 manifest. Chapter 2 supplementary measurements (EPSC, STDP, separated STM/LTM, impedance) remain Paper 1 (SY/Hybrane/LiTf) data and are used only as Li-only priors and sanity checks.

---

## Purpose

Chapter 4 is a data-driven chapter: it fits compact behavioural models to measured data and then simulates application-level schemes from those models. The achievability of the chapter therefore depends entirely on:

1. **What datasets actually exist** across the PEO/triflate comparative corpus.
2. **Whether those datasets share a common protocol**, so that fitted parameters are comparable across composition and cation cells.
3. **What the analysis pipeline must produce**, in the form of "parameter cards" per composition–cation cell, to feed the simulations in §4.4–§4.6 of `04_chapter4_temporal_computing_plan.md`.

This handout fixes all three before writing begins. Every simulation figure in Chapter 4 must be traceable, via this document, back to a specific device generation and a specific measurement folder.

---

## 1. The Three Common Dataset Types (PEO/triflate corpus)

Across the PEO/triflate comparative corpus — the PEO/LiTr concentration series and the PEO/LiTr, PEO/NaTr, PEO/KTr fixed-composition set at PEO = 0.3 and salt = 0.09 mass fractions — the **common** experimental measurements, i.e. those present for every cell of the corpus under a comparable protocol, are exactly three:

| Short name | Measurement | Folder convention | What it captures |
| ------------ | ------------- | ------------------- | ------------------ |
| **I–V** | Triangular-sweep current–voltage hysteresis | `Day1_Hyst` | Threshold, conductance window, read/write asymmetry, nonlinearity of the steady-state transfer |
| **N-pulse** | Variable-number-of-pulses potentiation (fixed amplitude, fixed width) | `Day2_NmbPls` | Per-pulse conductance update, saturation curve, cumulative potentiation law |
| **Delay-time** | Depotentiation by variable wait time after a fixed potentiation burst | `Day2_DlyTime` | Fading-memory decay, characteristic time constant, stretched-exponential shape |

These three datasets are the *only* datasets Chapter 4 is allowed to assume as universally available across the corpus. Everything else is treated as Chapter 2 supplementary data (see §4 below).

**Why these three are sufficient.** They provide, in the language of the compact model in §3:

- **I–V → read transfer function f_c(V_read, x)** — shape of the current as a function of voltage and internal state.
- **N-pulse → state update φ_c(V_write, t_write, x)** — how the internal state advances per write pulse, including saturation.
- **Delay-time → fading-memory decay λ_c(Δt)** — how the internal state relaxes between pulses in the absence of drive.

Given these three, the discrete-time dynamical model of §3 is fully identified for each composition–cation cell of the corpus. No additional measurement is required to simulate reservoir computing, coincidence detection or a transient filter bank at the level of claim that Chapter 4 makes.

---

## 2. Data Location and Naming Convention

### 2.1 Root path

```text
Nanomem_Devices_Library/DEVICES_LAB_DATA/
    YYYY-QN/
        NM_vXXX_<host><salt><electrode><speed><temp>/
            Day1_Hyst/
            Day2_NmbPls/
            Day2_DlyTime/
            Day14_Prof/          <-- stability, optional; not required by Ch. 4
```

- `YYYY-QN` — calendar quarter of fabrication (e.g. `2023-Q4`)
- `NM_vXXX` — sequential device generation number
- `<host>` — ion-transport polymer host. For the Chapter 4 comparative corpus this is **PEO**. Other hosts (e.g. `TMPE`, `Hybrane`) appear elsewhere in the archive but are excluded from the Chapter 4 manifest
- `<salt>` — for the Chapter 4 comparative corpus this is one of `LiTr`, `NaTr`, `KTr` (alkali-metal triflates). Alkali-TFSI salts (`LiBis`, `NaBis`, `KBis`) appear elsewhere in the archive but are excluded from the Chapter 4 manifest
- `<electrode>` — documented per device in the manifest; devices in a single cell must share the same electrode stack
- `<speed>` — spin-coating speed in rpm
- `<temp>` — annealing temperature in °C

**Note on folder encodings.** The historic folder naming convention has drifted across quarters. The manifest CSV (see §2.3) is the canonical reference; folder-name substrings should be treated as hints, and discrepancies must be resolved by consulting the lab notebook and the manifest, not by reverse-engineering the folder name.

### 2.2 File formats

- **CSV / TXT** — primary raw files dumped by the Keithley 2450 TSB scripts
- **HDF5** — consolidated post-processing containers (used by the Python pipeline)
- Each measurement subfolder contains one file per sweep/run; multiple runs per device are expected to quantify cycle-to-cycle spread

### 2.3 Device set for Chapter 4

Chapter 4 uses a **curated subset** of the NM_vXXX series, not the full 300+ generations. The selection criteria are:

1. **Host / salt chemistry:** PEO host with a triflate salt (LiTr, NaTr or KTr). TMPE-based and alkali-TFSI (LiBis / NaBis / KBis) devices are explicitly excluded — they belong to the Chapter 3 exploratory side-evidence section, not to the Chapter 4 comparative corpus.
2. **Composition cell:** each device must fall into one of the two strata defined below:
   - **Stratum A — PEO/LiTr concentration series.** PEO and LiTr mass fractions swept around the reference point (PEO = 0.3, salt = 0.09). Composition values must be recorded per device.
   - **Stratum B — PEO/{Li,Na,K}Tr fixed-composition set.** PEO = 0.3, salt = 0.09 mass fractions, all three cations present.
3. **Common electrode and processing protocol** within each stratum, so that composition or cation is the only significant variable between otherwise-matched devices.
4. **Measurement coverage:** all three measurement types (`Day1_Hyst`, `Day2_NmbPls`, `Day2_DlyTime`) present for the same device, under the common protocols of §3.
5. **Replicate count:** ≥ 3 devices per composition–cation cell that pass criteria 1–4, so that a parameter distribution (not only a point estimate) can be extracted in §5.

The final curated device list is to be frozen at the start of Chapter 4 writing and stored in a single CSV manifest:

```text
handouts/ch4_device_manifest.csv
```

with columns `device_id, stratum, host, salt, cation, peo_mass_fraction, salt_mass_fraction, quarter, electrode, speed_rpm, anneal_C, has_hyst, has_npulse, has_delaytime, passed_read_disturb, notes`. The manifest is the canonical reference; every figure in Chapter 4 must cite at least one row from it.

---

## 3. Common Measurement Protocols

For each dataset type, Chapter 4 requires a **single common protocol** across the PEO/triflate corpus so that fitted parameters are directly comparable within each stratum (concentration series and fixed-composition set). The protocols below are the reference definition; any device whose measurement deviates significantly must either be re-measured under the common protocol or excluded from the manifest.

### 3.1 I–V hysteresis (`Day1_Hyst`)

- **Waveform:** triangular voltage sweep, starting at 0 V
- **Peak amplitude:** fixed across the corpus (to be set from the Chapter 3 common protocol; typical range +1.0 to +3.0 V)
- **Sweep rate:** fixed across the corpus (typical: 0.25 V/s, as in Paper 1)
- **Cycles per run:** ≥ 10 successive sweeps per device, to capture cycle-to-cycle drift and eventual steady-state hysteresis
- **Read direction:** positive-only or bipolar, documented per device; Chapter 4 uses only the positive branch unless otherwise stated
- **Current compliance:** documented per device and used as a hard upper limit in simulations

**Extracted quantities:** low-V conductance, high-V conductance, hysteresis area, pinched-point voltage, ΔG(V) per sweep, cycle-to-cycle drift of the first three quantities.

### 3.2 N-pulse potentiation (`Day2_NmbPls`)

- **Pulse amplitude V_write:** fixed across the corpus
- **Pulse width t_write:** fixed across the corpus
- **Inter-pulse interval:** fixed and short enough that inter-pulse decay is negligible compared to the per-pulse update
- **Read pulse:** a single low-amplitude, sub-threshold read pulse after each block of N write pulses
- **Pulse-count sweep:** logarithmic in N, covering at least two decades (e.g. N ∈ {1, 3, 10, 30, 100, 300})
- **Repeats per N:** ≥ 3 repeats per (device, N) to quantify cycle-to-cycle spread

**Extracted quantities:** ΔG/G₀ as a function of N, saturation level, initial slope (per-pulse update at x ≈ 0), saturation knee location.

### 3.3 Delay-time depotentiation (`Day2_DlyTime`)

- **Pre-burst:** a fixed-N potentiation burst using the same V_write, t_write as in §3.2, sufficient to drive the device to a repeatable elevated state
- **Wait time Δt:** swept logarithmically, covering at least the range [10⁻¹, 10²] s (three decades), with enough points to resolve a stretched-exponential decay
- **Read pulse:** a single low-amplitude, sub-threshold read pulse at the end of each wait interval; the read must not significantly perturb the state (verified by the read-disturb check in §3.4)
- **Repeats per Δt:** ≥ 3 repeats per (device, Δt) to quantify cycle-to-cycle spread

**Extracted quantities:** G(Δt) normalised to G immediately after the burst, stretched-exponential parameters (τ_c, β_c), asymptotic floor G_∞, effective fading-memory window for the application band.

### 3.4 Read-disturb sanity check (cross-cutting)

- Before any model is fit, each device must be checked for read-disturb using a long train of pure read pulses in the absence of write pulses. The state must not drift by more than one resolvable level over the timescale of interest for Chapter 4.
- Devices that fail this check are excluded from the manifest or have their read voltage lowered until they pass.

---

## 4. Chapter 2 Supplementary Data (Not Assumed Common)

The following data exist for the Chapter 2 Paper 1 device (SY/Hybrane/LiTf) only. They are **not** uniformly present across the Chapter 3 PEO/triflate corpus, and must never be treated as comparative Li/Na/K or composition-series evidence. Chapter 4 is allowed to use them as **sanity checks and functional-form priors**, but not as primary fitting inputs for application simulations.

| Dataset | Available for | Role in Chapter 4 |
| --------- | --------------- | ------------------- |
| EPSC (multi-state pulse train) | Paper 1 SY/Hybrane/LiTf device | Sanity check that the fitted φ(x) can reproduce a multi-state ladder on a representative Li device; not propagated to Na or K |
| STDP (pre/post paired pulses) | Paper 1 SY/Hybrane/LiTf device | Li-only prior for the coincidence-kernel shape in §4.5 of the Ch. 4 plan; *not* used for Na, K or any composition-series claim — those are built from the variable-delay depotentiation kernel alone |
| STM/LTM separated retention (two-voltage protocol) | Paper 1 SY/Hybrane/LiTf device | Prior for the stretched-exponential form used in §3.3; guides the choice of functional form for the PEO/triflate common fits |
| Impedance spectroscopy (lock-in) | Paper 1 SY/Hybrane/LiTf device | Hard lower bound on the fastest meaningful Δt in any simulation; qualitative RC-level plausibility check, applied with caution because the PEO/triflate host is chemically distinct |
| Long-term profile (`Day14_Prof`) | Subset of Chapter 3 PEO/triflate devices | Stability envelope for the §4.7 circuit-integration discussion; not used in the application simulations themselves |

**Rule:** if a statement in Chapter 4 relies on any of these Chapter 2 datasets, it must be flagged in the text as a "Chapter 2 prior" or "Li-only sanity check" and must not be used to justify quantitative application-level claims for Na, K or composition-series cells.

---

## 5. Analysis Pipeline — What It Must Produce

The existing Python analysis pipeline (`Nanomem_Devices_Library/scripts_general/` and project-specific subfolders) already contains the tool families listed in the memory record: visualization, helper, application, device_cleaner, feature_extraction, graphmaker. Chapter 4 does **not** require new tool families. It requires a specific set of *outputs* produced by that pipeline, organised as a single reproducible run.

### 5.1 Pipeline entry point

A single orchestrating script is required. Suggested location and name:

```text
Nanomem_Devices_Library/scripts_general/chapter4_pipeline.py
```

Inputs: the device manifest CSV from §2.3.  
Outputs: everything listed in §5.2–§5.5, written to a single timestamped output directory `ch4_outputs/<timestamp>/`.

### 5.2 Per-device cleaned datasets

For each device in the manifest, the pipeline must emit a consolidated HDF5 (or Parquet) file containing:

- Raw and baseline-corrected I–V sweeps
- Raw and normalised N-pulse potentiation curves (ΔG/G₀ vs N, per run)
- Raw and normalised delay-time depotentiation curves (G/G₀ vs Δt, per run)
- Per-run metadata (date, compliance, read voltage, read pulse width, etc.)
- A boolean `passed_read_disturb` flag (from §3.4)

### 5.3 Per-device fitted quantities

For each device, the pipeline must fit and persist:

- **I–V fit:** parameters of a parametric form for f_i(V_read, x) — at minimum low-V slope, high-V slope, and an asymmetry parameter between forward and backward branches
- **N-pulse fit:** parameters of φ_i at fixed V_write, t_write — at minimum initial per-pulse update and saturation level
- **Delay-time fit:** stretched-exponential parameters (τ_i, β_i) and asymptotic floor G_∞, plus a goodness-of-fit metric (R² and residual RMS)
- Standard errors on all fit parameters

### 5.4 Per-cell parameter cards

The pipeline must aggregate the per-device fits into one **parameter card per composition–cation cell** in the manifest. Cells come from two strata: (i) the PEO/LiTr concentration series and (ii) the PEO/LiTr, PEO/NaTr, PEO/KTr fixed-composition set at 0.3 / 0.09. Each card is a single JSON (or YAML) file, named by stratum and cell:

```text
ch4_outputs/<timestamp>/parameter_cards/
    concentration/
        PEO-LiTr_<peoMF>_<saltMF>.json
        ...
    fixed_0p3_0p09/
        PEO-LiTr.json
        PEO-NaTr.json
        PEO-KTr.json
```

Each card contains, at minimum:

- Number of devices contributing
- Mean and standard deviation of every fit parameter across devices
- Covariance structure where it matters (e.g. between τ and β)
- A serialisable "draw a device" function specification: given a random seed, return a parameter tuple sampled from the empirical distribution
- A versioning header (pipeline version, manifest hash, date of run)

The full set of cards is the canonical interface between the experimental data and every simulation in §4.4–§4.6 of the Chapter 4 plan. No simulation figure in Chapter 4 may bypass them.

### 5.5 Validation artefacts

The pipeline must emit, for transparency:

- Fit-overlay plots for every device (raw data + fitted curve) in a single PDF per composition–cation cell
- A leave-one-dataset-out cross-validation report: fit on {I–V, N-pulse} and predict the delay-time decay shape; then fit on {I–V, delay-time} and predict the N-pulse saturation; report agreement metrics
- A summary table of all fit parameters across all devices (CSV), indexed by stratum, cell and device, for inclusion in the Chapter 4 appendix

### 5.6 Reproducibility

- The pipeline must be run as a single command with the manifest CSV as its only required argument
- The output directory must contain a `run.json` capturing: git commit hash of `scripts_general/`, Python version, package versions, manifest hash, command line, date, host
- Re-running with the same manifest must produce byte-identical parameter cards (given a fixed RNG seed for bootstrap resamples)

---

## 6. Dataset → Chapter 4 Section Traceability

Every section of the Chapter 4 plan is now grounded in a specific subset of these three datasets. The table below is the traceability matrix.

| Chapter 4 section | I–V (`Day1_Hyst`) | N-pulse (`Day2_NmbPls`) | Delay-time (`Day2_DlyTime`) | Purpose |
| ------------------- | :---: | :---: | :---: | --------- |
| §4.2 Dataset consolidation | ✓ | ✓ | ✓ | Inventory |
| §4.3 Compact behavioural model | ✓ (f_i) | ✓ (φ_i) | ✓ (λ_i) | Model identification |
| §4.4 Reservoir computing (flagship) | ✓ | ✓ | ✓ | Node update + state read-out + fading memory |
| §4.5 Coincidence detection | — | ✓ | ✓ | Temporal kernel from delay-time; cumulative update from N-pulse |
| §4.6 Transient filter bank | — | ✓ | ✓ | Impulse response from N-pulse (onset) + delay-time (decay) |
| §4.7 Circuit integration | ✓ | ✓ | ✓ | Read voltage, read-disturb budget, variability envelopes |
| §4.8 Design rules | ✓ | ✓ | ✓ | Quantified by the parameter cards |

**Note:** the earlier drafts of the Chapter 4 plan claimed (i) that EPSC, STDP and impedance datasets were available across Li/Na/K, and (ii) that the comparative corpus was an Ag-electrode LiTFSI/NaTFSI/KTFSI series in a Hybrane-class host. Both were inherited from stale planning notes. The correct picture is the one captured by the traceability matrix above: the comparative corpus is the PEO/triflate series (concentration + fixed-composition strata); the richer Chapter 2 metrics remain Paper 1 evidence only; TMPE and alkali-TFSI devices are side evidence in Chapter 3 and are out of scope for Chapter 4. The Chapter 4 plan has been updated accordingly.

---

## 7. Pre-Flight Checklist Before Writing Chapter 4

The following must all be true *before* Chapter 4 writing starts:

- [ ] `handouts/ch4_device_manifest.csv` exists and, for each composition–cation cell in the PEO/triflate corpus, lists ≥ 3 devices that have all three measurement types present
- [ ] All devices in the manifest have passed the read-disturb sanity check (§3.4)
- [ ] The common protocols in §3.1–§3.3 are confirmed to be the same across all manifest devices (or deviations are explicitly documented)
- [ ] The `chapter4_pipeline.py` orchestration script exists and runs end-to-end on the manifest
- [ ] The per-cell parameter cards (§5.4) have been produced for every cell in both strata
- [ ] The leave-one-dataset-out cross-validation report shows acceptable agreement (thresholds to be set, but ≥ 0.9 R² on the held-out dataset is the nominal target)
- [ ] Fit-overlay PDFs for each composition–cation cell have been visually inspected and are free of gross failures
- [ ] The Chapter 2 supplementary datasets of §4 have been catalogued with one-line descriptions of how (or whether) they will be used as Li-only priors / sanity checks
- [ ] Any TMPE-based or alkali-TFSI (LiBis / NaBis / KBis) devices that could be candidates for inclusion have been explicitly logged as *excluded* with a one-line reason (typically: insufficient coverage of the three common measurements)

Only when every item above is ticked does Chapter 4 have a defensible empirical basis.

---

## 8. Open Items and Known Risks

- **Protocol drift:** the NM_vXXX series spans several quarters; N-pulse and delay-time protocols may have been refined mid-series. The manifest must record the protocol version for each device, and any protocol mismatch within a composition–cation cell must either be reconciled or disqualify the device.
- **Cycle-to-cycle volatility vs. device-to-device volatility:** the pipeline must report both separately. Chapter 4's reservoir robustness claim depends on this distinction.
- **Stretched-exponential β is temperature-dependent:** all measurements should be documented as room-temperature, and devices measured outside a narrow temperature band should be flagged.
- **Compliance-limited sweeps:** any I–V curve that saturates against the Keithley current compliance has truncated f_c(V_read, x) and must be either re-measured at a higher compliance or excluded from the high-V part of the fit.
- **Pipeline versioning:** if the `scripts_general/` analysis code is updated between dry runs and final Chapter 4 figures, all parameter cards must be regenerated — not retroactively edited.
- **Host-chemistry confound:** the Chapter 2 Paper 1 device uses a Hybrane host, while the Chapter 3 / Chapter 4 comparative corpus uses a PEO host. This is why the Chapter 2 measurements are used only as functional-form priors and cross-checks, not as comparative fits. Any use of Chapter 2 quantitative numbers in Chapter 4 must explicitly acknowledge this difference.
