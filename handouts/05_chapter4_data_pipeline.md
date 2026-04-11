# Chapter 4 — Data, Protocols and Analysis Pipeline Specification
**Author:** Carlos David Prado-Socorro  
**Date:** April 11, 2026  
**Status:** Specification document. Defines exactly which datasets exist for Li/Na/K devices, where they live, which measurement protocols are common across the three ion species, and which analysis outputs are required before Chapter 4 writing starts. This document is the contract between the experimental archive and Chapter 4.

---

## Purpose

Chapter 4 is a data-driven chapter: it fits compact behavioural models to measured data and then simulates application-level schemes from those models. The achievability of the chapter therefore depends entirely on:

1. **What datasets actually exist** across Li, Na and K devices.
2. **Whether those datasets share a common protocol**, so that fitted parameters are comparable across ion species.
3. **What the analysis pipeline must produce**, in the form of "parameter cards" per ion species, to feed the simulations in §4.4–§4.6 of `04_chapter4_temporal_computing_plan.md`.

This handout fixes all three before writing begins. Every simulation figure in Chapter 4 must be traceable, via this document, back to a specific device generation and a specific measurement folder.

---

## 1. The Three Common Dataset Types (Li / Na / K)

Across the Ag-electrode NM_vXXX series employing LiTFSI, NaTFSI and KTFSI salts, the **common** experimental measurements — i.e. those present for all three ion species under a comparable protocol — are exactly three:

| Short name | Measurement | Folder convention | What it captures |
|------------|-------------|-------------------|------------------|
| **I–V** | Triangular-sweep current–voltage hysteresis | `Day1_Hyst` | Threshold, conductance window, read/write asymmetry, nonlinearity of the steady-state transfer |
| **N-pulse** | Variable-number-of-pulses potentiation (fixed amplitude, fixed width) | `Day2_NmbPls` | Per-pulse conductance update, saturation curve, cumulative potentiation law |
| **Delay-time** | Depotentiation by variable wait time after a fixed potentiation burst | `Day2_DlyTime` | Fading-memory decay, characteristic time constant, stretched-exponential shape |

These three datasets are the *only* datasets Chapter 4 is allowed to assume as universally available for Li, Na and K. Everything else is treated as ion-specific supplementary data (see §4 below).

**Why these three are sufficient.** They provide, in the language of the compact model in §3:

- **I–V → read transfer function f_i(V_read, x)** — shape of the current as a function of voltage and internal state.
- **N-pulse → state update φ_i(V_write, t_write, x)** — how the internal state advances per write pulse, including saturation.
- **Delay-time → fading-memory decay λ_i(Δt)** — how the internal state relaxes between pulses in the absence of drive.

Given these three, the discrete-time dynamical model of §3 is fully identified for each ion species. No additional measurement is required to simulate reservoir computing, coincidence detection or a transient filter bank at the level of claim that Chapter 4 makes.

---

## 2. Data Location and Naming Convention

### 2.1 Root path
```
Nanomem_Devices_Library/DEVICES_LAB_DATA/
    YYYY-QN/
        NM_vXXX_<polymer><salt><electrode><speed><temp>/
            Day1_Hyst/
            Day2_NmbPls/
            Day2_DlyTime/
            Day14_Prof/          <-- stability, optional; not required by Ch. 4
```

- `YYYY-QN` — calendar quarter of fabrication (e.g. `2023-Q4`)
- `NM_vXXX` — sequential device generation number
- `<polymer>` — typically `TMPE` (Hybrane-class)
- `<salt>` — one of `LiBis`, `NaBis`, `KBis` (TFSI salts)
- `<electrode>` — `Ag` for the entire Chapter 3–4 series
- `<speed>` — spin-coating speed in rpm
- `<temp>` — annealing temperature in °C

### 2.2 File formats
- **CSV / TXT** — primary raw files dumped by the Keithley 2450 TSB scripts
- **HDF5** — consolidated post-processing containers (used by the Python pipeline)
- Each measurement subfolder contains one file per sweep/run; multiple runs per device are expected to quantify cycle-to-cycle spread

### 2.3 Device set for Chapter 4
Chapter 4 uses a **curated subset** of the NM_vXXX series, not the full 300+ generations. The selection criteria are:

1. Ag electrode (consistent with the Chapter 3 Ag-electrode framing).
2. SY / Hybrane-class / MBis composite with the same mass-ratio protocol across Li, Na and K (so that composition is not a confound).
3. All three measurement types (`Day1_Hyst`, `Day2_NmbPls`, `Day2_DlyTime`) present for the same device.
4. At least ≥ 3 devices per ion species that pass criteria 1–3, so that a parameter distribution (not only a point estimate) can be extracted in §3.

The final curated device list is to be frozen at the start of Chapter 4 writing and stored in a single CSV manifest:
```
handouts/ch4_device_manifest.csv
```
with columns `device_id, ion, quarter, electrode, speed_rpm, anneal_C, has_hyst, has_npulse, has_delaytime, notes`. The manifest is the canonical reference; every figure in Chapter 4 must cite at least one row from it.

---

## 3. Common Measurement Protocols

For each dataset type, Chapter 4 requires a **single common protocol** across Li, Na and K so that fitted parameters are directly comparable. The protocols below are the reference definition; any device whose measurement deviates significantly must either be re-measured under the common protocol or excluded from the manifest.

### 3.1 I–V hysteresis (`Day1_Hyst`)
- **Waveform:** triangular voltage sweep, starting at 0 V
- **Peak amplitude:** fixed across Li/Na/K (to be set from the Chapter 3 common protocol; typical range +1.0 to +3.0 V)
- **Sweep rate:** fixed across Li/Na/K (typical: 0.25 V/s, as in Paper 1)
- **Cycles per run:** ≥ 10 successive sweeps per device, to capture cycle-to-cycle drift and eventual steady-state hysteresis
- **Read direction:** positive-only or bipolar, documented per device; Chapter 4 uses only the positive branch unless otherwise stated
- **Current compliance:** documented per device and used as a hard upper limit in simulations

**Extracted quantities:** low-V conductance, high-V conductance, hysteresis area, pinched-point voltage, ΔG(V) per sweep, cycle-to-cycle drift of the first three quantities.

### 3.2 N-pulse potentiation (`Day2_NmbPls`)
- **Pulse amplitude V_write:** fixed across Li/Na/K
- **Pulse width t_write:** fixed across Li/Na/K
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

**Extracted quantities:** G(Δt) normalised to G immediately after the burst, stretched-exponential parameters (τ_i, β_i), asymptotic floor G_∞, effective fading-memory window for the application band.

### 3.4 Read-disturb sanity check (cross-cutting)
- Before any model is fit, each device must be checked for read-disturb using a long train of pure read pulses in the absence of write pulses. The state must not drift by more than one resolvable level over the timescale of interest for Chapter 4.
- Devices that fail this check are excluded from the manifest or have their read voltage lowered until they pass.

---

## 4. Ion-Specific Supplementary Data (Not Assumed Common)

The following data exist, but only for a *subset* of the Li/Na/K devices — typically only for the Paper 1 Li device and a handful of Chapter 3 repeats. Chapter 4 is allowed to use these datasets as **sanity checks and model priors**, but not as the primary fitting input for application simulations, because they are not available uniformly across Li, Na and K.

| Dataset | Available for | Role in Chapter 4 |
|---------|---------------|-------------------|
| EPSC (multi-state pulse train) | Paper 1 Li device (Ch. 2); partial Ch. 3 repeats | Sanity check that the fitted φ_i(x) reproduces the measured state ladder |
| STDP (pre/post paired pulses) | Paper 1 Li device (Ch. 2) | Prior for the coincidence kernel shape in §4.5 of the Ch. 4 plan; *not* used as the sole input for the Na and K coincidence simulations — those are built from the delay-time kernel alone |
| STM/LTM separated retention (two-voltage protocol) | Paper 1 Li device (Ch. 2) | Prior for the stretched-exponential form used in §3.3; guides the choice of functional form for the Li/Na/K common fits |
| Impedance spectroscopy (lock-in) | Paper 1 Li device; partial Ch. 3 | Hard lower bound on the fastest meaningful Δt in any simulation; sanity check on the RC-level plausibility of the compact model |
| Long-term profile (`Day14_Prof`) | Subset of Ch. 3 devices | Stability envelope for the §4.7 circuit-integration discussion; not used in the application simulations themselves |

**Rule:** if a statement in Chapter 4 relies on any of these ion-specific datasets, it must be flagged in the text as a "sanity check" or "prior" and must not be used to justify quantitative application-level claims for ion species for which the dataset does not exist.

---

## 5. Analysis Pipeline — What It Must Produce

The existing Python analysis pipeline (`Nanomem_Devices_Library/scripts_general/` and project-specific subfolders) already contains the tool families listed in the memory record: visualization, helper, application, device_cleaner, feature_extraction, graphmaker. Chapter 4 does **not** require new tool families. It requires a specific set of *outputs* produced by that pipeline, organised as a single reproducible run.

### 5.1 Pipeline entry point
A single orchestrating script is required. Suggested location and name:
```
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

### 5.4 Per-ion parameter cards
The pipeline must aggregate the per-device fits into three **parameter cards**, one per ion species. Each card is a single JSON (or YAML) file:

```
ch4_outputs/<timestamp>/parameter_cards/
    Li.json
    Na.json
    K.json
```

Each card contains, at minimum:

- Number of devices contributing
- Mean and standard deviation of every fit parameter across devices
- Covariance structure where it matters (e.g. between τ and β)
- A serialisable "draw a device" function specification: given a random seed, return a parameter tuple sampled from the empirical distribution
- A versioning header (pipeline version, manifest hash, date of run)

These three cards are the canonical interface between the experimental data and every simulation in §4.4–§4.6 of the Chapter 4 plan. No simulation figure in Chapter 4 may bypass them.

### 5.5 Validation artefacts
The pipeline must emit, for transparency:

- Fit-overlay plots for every device (raw data + fitted curve) in a single PDF per ion species
- A leave-one-dataset-out cross-validation report: fit on {I–V, N-pulse} and predict the delay-time decay shape; then fit on {I–V, delay-time} and predict the N-pulse saturation; report agreement metrics
- A summary table of all fit parameters across all devices (CSV) for inclusion in the Chapter 4 appendix

### 5.6 Reproducibility
- The pipeline must be run as a single command with the manifest CSV as its only required argument
- The output directory must contain a `run.json` capturing: git commit hash of `scripts_general/`, Python version, package versions, manifest hash, command line, date, host
- Re-running with the same manifest must produce byte-identical parameter cards (given a fixed RNG seed for bootstrap resamples)

---

## 6. Dataset → Chapter 4 Section Traceability

Every section of the Chapter 4 plan is now grounded in a specific subset of these three datasets. The table below is the traceability matrix.

| Chapter 4 section | I–V (`Day1_Hyst`) | N-pulse (`Day2_NmbPls`) | Delay-time (`Day2_DlyTime`) | Purpose |
|-------------------|:---:|:---:|:---:|---------|
| §4.2 Dataset consolidation | ✓ | ✓ | ✓ | Inventory |
| §4.3 Compact behavioural model | ✓ (f_i) | ✓ (φ_i) | ✓ (λ_i) | Model identification |
| §4.4 Reservoir computing (flagship) | ✓ | ✓ | ✓ | Node update + state read-out + fading memory |
| §4.5 Coincidence detection | — | ✓ | ✓ | Temporal kernel from delay-time; cumulative update from N-pulse |
| §4.6 Transient filter bank | — | ✓ | ✓ | Impulse response from N-pulse (onset) + delay-time (decay) |
| §4.7 Circuit integration | ✓ | ✓ | ✓ | Read voltage, read-disturb budget, variability envelopes |
| §4.8 Design rules | ✓ | ✓ | ✓ | Quantified by the parameter cards |

**Note:** the earlier draft of the Chapter 4 plan claimed that EPSC, STDP and impedance datasets were available for Li/Na/K. This is incorrect — those datasets exist primarily for the Paper 1 Li device. The traceability matrix above is the authoritative one, and the Chapter 4 plan has been updated to match.

---

## 7. Pre-Flight Checklist Before Writing Chapter 4

The following must all be true *before* Chapter 4 writing starts:

- [ ] `handouts/ch4_device_manifest.csv` exists and lists ≥ 3 devices per ion species that have all three measurement types present
- [ ] All devices in the manifest have passed the read-disturb sanity check (§3.4)
- [ ] The common protocols in §3.1–§3.3 are confirmed to be the same across all manifest devices (or deviations are explicitly documented)
- [ ] The `chapter4_pipeline.py` orchestration script exists and runs end-to-end on the manifest
- [ ] The three parameter cards `Li.json`, `Na.json`, `K.json` have been produced
- [ ] The leave-one-dataset-out cross-validation report shows acceptable agreement (thresholds to be set, but ≥ 0.9 R² on the held-out dataset is the nominal target)
- [ ] Fit-overlay PDFs for each ion species have been visually inspected and are free of gross failures
- [ ] The ion-specific supplementary datasets of §4 have been catalogued with one-line descriptions of how (or whether) they will be used

Only when every item above is ticked does Chapter 4 have a defensible empirical basis.

---

## 8. Open Items and Known Risks

- **Protocol drift:** the NM_vXXX series spans several quarters; N-pulse and delay-time protocols may have been refined mid-series. The manifest must record the protocol version for each device, and any protocol mismatch across Li/Na/K must either be reconciled or disqualify the device.
- **Cycle-to-cycle volatility vs. device-to-device volatility:** the pipeline must report both separately. Chapter 4's reservoir robustness claim depends on this distinction.
- **Stretched-exponential β is temperature-dependent:** all measurements should be documented as room-temperature, and devices measured outside a narrow temperature band should be flagged.
- **Compliance-limited sweeps:** any I–V curve that saturates against the Keithley current compliance has truncated f_i(V_read, x) and must be either re-measured at a higher compliance or excluded from the high-V part of the fit.
- **Pipeline versioning:** if the `scripts_general/` analysis code is updated between dry runs and final Chapter 4 figures, all parameter cards must be regenerated — not retroactively edited.
