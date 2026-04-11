<!-- markdownlint-disable-file MD013 -->

# Chapter 4 — Data-Driven Temporal Computing with Volatile Ion-Mediated Polymeric Memristors: Detailed Outline

**Author:** Carlos David Prado-Socorro  
**Date:** April 11, 2026  
**Status:** Planning document for the new Chapter 4 (5-chapter thesis structure, v2).

---

## Purpose of This Chapter

Chapters 2 and 3 establish *what* the devices are and *why* their behaviour depends on ion identity. Chapter 4 answers the next question: *what are they good for, and how do we use them?*

The answer, argued in detail in the chapter, is that the SY/Hybrane/Li–Na–K family is naturally suited to **temporal computing** — computing that uses the transients of a dynamical system, not its steady state, to represent and classify time-varying signals. The chapter re-purposes every dataset already measured in Chapters 2 and 3 as input to compact behavioural models, and uses those models to demonstrate three application schemes in simulation, without any new fabrication.

**One-sentence thesis of the chapter:** *Volatile, variable, ion-mediated organic memristive devices are not flawed non-volatile memories — they are heterogeneous fading-memory primitives, and when treated as such they deliver physical reservoir computing, spike coincidence detection, and multi-timescale transient filtering directly from the datasets of Chapters 2 and 3.*

**What the chapter does *not* claim:**

- It does not claim these devices beat crossbar ReRAM or SRAM on density, endurance, or retention.
- It does not present newly fabricated circuits or on-chip demonstrations.
- It does not benchmark against digital memory. It benchmarks against other temporal / reservoir / neuromorphic substrates.

---

## Natural Conceptual Flow

**Reframe → Consolidate → Model → Apply → Constrain → Rules**

1. **Reframe** the device family from "weak non-volatile memory" to "heterogeneous temporal primitive".
2. **Consolidate** the datasets from Chapters 2 and 3 into a single experimental basis.
3. **Model** each ion species (Li, Na, K) with a compact, physically motivated behavioural model fitted directly to those datasets.
4. **Apply** the models to three simulated application schemes: reservoir computing (flagship), coincidence detection, and transient filter bank.
5. **Constrain** the schemes by realistic circuit integration (1T1M addressing, current compliance, read/write protocols, variability envelopes).
6. **Rules:** distil design rules and scope limits — where these devices are genuinely useful, and where they are not.

---

## Full Hierarchical Outline

### 4.1 Motivation: Volatility and Variability as Computational Resources

#### 4.1.1 The framing problem

- How the field typically judges organic memristive devices — against crossbar ReRAM figures of merit (retention, endurance, ON/OFF ratio, linearity)
- Why this is the wrong yardstick for a device whose intrinsic time constants sit in the 10⁰–10¹ s range
- Historical parallel: early CMOS was also "too slow to beat bipolar" until the right application appeared

#### 4.1.2 Fading memory as a computational asset

- Echo state property: why a dynamical reservoir must forget in order to be trainable
- Leaky integrators in biology: short-term plasticity, dendritic filtering, cortical adaptation
- The link between retention time and application-relevant timescale matching

#### 4.1.3 Variability as heterogeneity

- Device-to-device spread as an effective expansion of the state space
- Cycle-to-cycle variability as a source of useful stochasticity (as in stochastic gradient-like dynamics, dithering of thresholds)
- The trade-off between *trained* systems (where variability hurts) and *projected* systems (where it helps)

#### 4.1.4 What this chapter will therefore show

- A compact data-driven model of the Li/Na/K family
- Three application schemes using only that model
- Circuit-level constraints that make the schemes physically plausible

---

### 4.2 Experimental Dataset Consolidation

*The authoritative data/protocol/pipeline specification for this section is `handouts/05_chapter4_data_pipeline.md`. This subsection only summarises it.*

#### 4.2.1 Provenance

- Mapping of each dataset to its originating device generation in `Nanomem_Devices_Library/DEVICES_LAB_DATA/YYYY-QN/NM_vXXX_.../`
- Curated device list frozen in `handouts/ch4_device_manifest.csv` (≥ 3 devices per ion species, all passing the read-disturb sanity check)
- Chapter 2 Paper 1 Li device: full measurement suite, used as reference / prior
- Chapter 3 Ag-electrode series (LiTFSI, NaTFSI, KTFSI): common measurement suite restricted to the three datasets below, under a common protocol

#### 4.2.2 Dataset inventory table — common Li/Na/K data

The only datasets Chapter 4 assumes as universally available across Li, Na and K are the three listed below. They map one-to-one to the three ingredients of the compact model in §4.3.

| Dataset type | Folder | Li | Na | K | Quantity extracted | Model role |
|--------------|--------|:--:|:--:|:--:|---------------------|------------|
| I–V hysteresis (triangular sweep) | `Day1_Hyst` | ✓ | ✓ | ✓ | Threshold, nonlinearity, read/write asymmetry, conductance window | Read transfer function f_i(V_read, x) |
| N-pulse potentiation (log-sweep in N) | `Day2_NmbPls` | ✓ | ✓ | ✓ | Per-pulse conductance update, saturation curve | State update φ_i(V_write, t_write, x) |
| Delay-time depotentiation (log-sweep in Δt) | `Day2_DlyTime` | ✓ | ✓ | ✓ | Stretched-exponential τ_i, β_i; fading-memory window; asymptotic floor | Fading-memory decay λ_i(Δt) |

Device-to-device and cycle-to-cycle spread are obtained from replicates within each of these three datasets, not from a separate measurement type.

#### 4.2.3 Ion-specific supplementary data (sanity checks and priors only)

The following datasets exist but only for a *subset* of the Li/Na/K devices — typically only for the Paper 1 Li device and a few Chapter 3 repeats. Chapter 4 uses them as **sanity checks and functional-form priors**, never as the primary fitting input for application simulations.

| Dataset | Available for | Role in Chapter 4 |
|---------|---------------|-------------------|
| EPSC (multi-state pulse train) | Paper 1 Li; partial Ch. 3 repeats | Sanity check that fitted φ_i(x) reproduces the measured state ladder |
| STDP (paired-pulse kernel) | Paper 1 Li | Prior for the coincidence kernel shape in §4.5; *not* used for Na and K claims |
| Separated STM/LTM retention (two-voltage protocol) | Paper 1 Li | Prior on stretched-exponential functional form in §4.3 |
| Impedance spectroscopy | Paper 1 Li; partial Ch. 3 | Hard lower bound on the fastest meaningful Δt; RC-level plausibility check |
| Long-term profile (`Day14_Prof`) | Subset of Ch. 3 devices | Stability envelope for the §4.7 integration discussion |

**Rule:** every statement in Chapter 4 that relies on any of these ion-specific datasets must be flagged in the text as "prior" or "sanity check" and must not be used to justify quantitative application-level claims for ion species where the dataset does not exist.

#### 4.2.4 Common pre-processing

- Normalisation conventions (G/G₀, ΔG/G₀, t/τ)
- Baseline drift correction and read-disturb sanity check (see §3.4 of `05_chapter4_data_pipeline.md`)
- Outlier rejection policy documented per dataset type
- Python analysis pipeline orchestrated by a single entry-point script `chapter4_pipeline.py` in `scripts_general/`
- Full pipeline output (cleaned datasets, fits, parameter cards, validation artefacts) emitted to a single timestamped directory for reproducibility

---

### 4.3 Compact Behavioural Model Extraction

#### 4.3.1 Model family

- Discrete-time, single-state-variable model per device, indexed by ion species *i* ∈ {Li, Na, K}
- State update:
  \[ x_{k+1} = \lambda_i(\Delta t)\,x_k + \varphi_i(V_\text{write}, t_\text{write}, x_k) + \xi_k \]

- Read-out:
  \[ G_k = g_i(x_k, V_\text{read}),\quad I_k = f_i(V_\text{read}, x_k) \]

- Noise term ξ_k captures cycle-to-cycle variability; device-level parameter draws capture device-to-device variability

#### 4.3.2 Mapping datasets to model parameters

The model is identified from exactly the three common Li/Na/K datasets. Each of the three ingredients λ_i, φ_i, f_i is fit from one, and only one, of them. Supplementary ion-specific datasets (see §4.2.3) are used as priors and sanity checks only.

| Experimental dataset (common Li/Na/K) | Extracted quantity | Role in the model |
|---------------------------------------|---------------------|-------------------|
| I–V hysteresis (`Day1_Hyst`) | Low-V slope, high-V slope, conductance window, forward/backward asymmetry | Shape of f_i(V_read, x) |
| N-pulse potentiation (`Day2_NmbPls`) | Initial per-pulse update, saturation knee, asymptotic state | Form of φ_i(V_write, t_write, x) at the fixed protocol |
| Delay-time depotentiation (`Day2_DlyTime`) | Stretched-exponential τ_i, β_i, asymptotic floor | Form of λ_i(Δt); also serves as the fading-memory temporal kernel K_i(Δt) used in §4.5 |
| Replicates within the three datasets above | Device-to-device and cycle-to-cycle parameter distributions | Prior over (λ_i, φ_i, f_i) across an ensemble |

Supplementary (Paper 1 Li only; used only as prior / sanity check):

| Supplementary dataset | Use |
|-----------------------|-----|
| EPSC multi-state pulse train | Sanity check that fitted φ_i(x) reproduces the measured state ladder on the Li device |
| STDP paired-pulse kernel | Functional-form prior for the Li coincidence kernel; not used for Na/K |
| Separated STM/LTM retention (two-voltage protocol) | Prior for stretched-exponential functional form |
| Impedance spectroscopy | Hard lower bound on the fastest meaningful Δt (RC-level sanity bound) |

#### 4.3.3 Model validation

- **Leave-one-dataset-out validation** across the three common datasets: fit on {I–V, N-pulse}, predict the delay-time decay shape; then fit on {I–V, delay-time}, predict the N-pulse saturation curve; report R² and residual RMS on the held-out dataset
- **Cross-species sanity checks:** the Li/Na/K time-constant hierarchy (τ_Li > τ_Na > τ_K, or its measured ordering) must emerge from the delay-time fits, not be imposed by hand
- **Supplementary sanity checks (Li only):** predicted EPSC state ladder from the fitted φ_Li must reproduce the Paper 1 EPSC measurements within a stated tolerance; predicted coincidence kernel from the fitted λ_Li must be consistent with the Paper 1 STDP data
- **Fit-quality metrics:** R² on delay-time curves, RMSE on N-pulse curves, RMSE on I–V low-V and high-V slopes, KL divergence between simulated and measured cycle-to-cycle distributions
- **Pipeline-level reproducibility:** the validation report is produced automatically by `chapter4_pipeline.py` (see `05_chapter4_data_pipeline.md` §5.5)

#### 4.3.4 Resulting "parameter cards"

- One per ion species, summarising λ_i, φ_i, f_i with mean and spread
- These cards are the input to every simulation in §4.4–§4.6

---

### 4.4 Application I (Flagship) — Heterogeneous Physical Reservoir Computing

#### 4.4.1 Why this is the flagship

- Uses almost every dataset type measured in Chapters 2 and 3
- Makes fading memory and heterogeneity first-order *advantages*, not tolerated flaws
- Standard benchmarks exist; the chapter can report numbers that the reader can compare

#### 4.4.2 Reservoir architecture

- Input layer: pulse-encoded time series (rate or delta-coded)
- Reservoir layer: a bank of Li/Na/K devices used as parallel fading-memory nodes
  - Li bank: slow nodes (long τ)
  - Na bank: intermediate nodes
  - K bank: fast nodes

- Read-out: conductance state sampled at fixed delays, fed into a trained linear classifier

#### 4.4.3 Hardware sketch

- 1T1M bank per row, shared column read-out
- Row driver with current compliance
- Transimpedance amplifier → sample-and-hold → multiplexer → ADC → MCU/FPGA
- Readout layer trained offline (ridge regression) on the sampled state vector

#### 4.4.4 Benchmark tasks

- NARMA-10 and memory-capacity task (standard reservoir benchmarks)
- Spoken-digit temporal classification (Lyon-cochleagram encoded)
- Non-linear temporal XOR (classic fading-memory test)
- Simple biomedical waveform classification (e.g. ECG beat class), using published open datasets

#### 4.4.5 Metrics reported

- Memory capacity (linear and nonlinear)
- Class separability (Fisher criterion on the reservoir state)
- Classification accuracy vs. reservoir size
- Robustness to variability: performance vs. injected device-to-device and cycle-to-cycle spread, using the measured distributions from §4.3
- Estimated energy per inference, computed from EPSC energy per event (≈ 50 nJ in Paper 1)
- Comparison table with published reservoir implementations (software, memristive, photonic)

#### 4.4.6 Expected scientific claims

- Li/Na/K heterogeneity increases memory capacity vs. a single-species reservoir of the same size
- Measured variability *improves* (or at least does not hurt) classification robustness, within a quantified envelope
- The energy-per-inference figure is competitive at the "temporal edge" scale (sub-kHz signals)

---

### 4.5 Application II — Spike Coincidence Detection and Temporal Feature Extraction

#### 4.5.1 Motivation

- Coincidence detection is a canonical biological computation (e.g. sound localisation in the auditory brainstem)
- Requires exactly the behaviour that Li/Na/K devices already have: a state variable that rises with an event and decays with a controllable time constant
- Natural self-reset via volatility avoids explicit erase cycles

#### 4.5.2 Circuit scheme

- Pre-spike stream + post-spike stream → analog summing block → volatile memristor → comparator → event detected / not detected
- The device's fading memory implements the coincidence window directly
- Li, Na and K devices provide different (and pre-characterised) coincidence windows

#### 4.5.3 Data-driven simulation

- Use the measured **delay-time depotentiation curves** from Chapter 3 (common Li/Na/K dataset) as the temporal correlation function K_i(Δt): the device's fading-memory decay directly defines the coincidence window, because two events separated by Δt interact through the residual state that has not yet decayed
- For the Paper 1 Li device only, the measured STDP kernel is used as a sanity check that the shape of K_Li(Δt) obtained from the delay-time fit is consistent with the paired-pulse measurement
- Simulate detection probability vs. inter-event interval Δt for each ion species
- Inject noise and false-event streams to compute false-positive and false-negative rates
- Show how swapping Li → Na → K shifts the useful timing window, with the span quantified from the fitted τ_Li, τ_Na, τ_K

#### 4.5.4 Metrics reported

- Detection probability P_det(Δt) for each ion species
- ROC-like curves (true positive vs. false positive) under realistic noise
- Energy per detection event
- Effective timing resolution and its dependence on cycle-to-cycle variability

#### 4.5.5 Expected scientific claims

- The delay-time kernels from Chapter 3 define a tunable coincidence window bank
- If the fitted $\tau_i$ values are sufficiently separated, Li/Na/K should provide a composition-controlled span in useful coincidence-window width
- The accessible timing window is to be reported directly from the fitted delay-time constants; no broader timing-range claim is assumed a priori

---

### 4.6 Application III — Multi-Timescale Transient Filter Bank

#### 4.6.1 Motivation

- Many edge-sensing tasks need a leaky integrator or a bank of them (onset detection, burst detection, envelope extraction)
- A single device with a single τ is a single filter; a heterogeneous bank is a multi-resolution filter
- Li/Na/K naturally define a slow/medium/fast trio of time constants

#### 4.6.2 Circuit scheme

- Sensor pulses → split into Li, Na, K branches in parallel → three transient conductance traces → weighted sum / classifier
- Equivalent to a three-tap temporal wavelet-like decomposition, but at the analog front-end
- Compatible with 1T1M addressing and shared read-out

#### 4.6.3 Data-driven simulation

- Drive the parameter-card models of §4.3 with canonical inputs: step, impulse, burst, chirp, band-limited noise
- Compute the impulse responses of each branch directly from the measured **delay-time depotentiation** curves (λ_i) and **N-pulse potentiation** curves (φ_i) — both of which are common Li/Na/K datasets (see §4.2.2)
- Show decomposition of a composite signal into slow/medium/fast components
- Demonstrate a simple downstream task (e.g. onset detection, burst-rate estimation) using the three filtered channels

#### 4.6.4 Metrics reported

- Impulse responses h_i(t) for each ion species, compared to the ideal leaky integrators with the same τ
- Signal-reconstruction error when only the three bands are used
- Task performance on a simple onset-detection benchmark
- Sensitivity of task performance to device variability

#### 4.6.5 Expected scientific claims

- Li/Na/K devices act, to first order, as three leaky integrators with measurable and distinct time constants
- The heterogeneity provides a usable multi-resolution analog front-end without digital filtering
- This is the "cheapest" of the three applications in terms of circuit complexity — a credible near-term target for a physical demonstration

---

### 4.7 Circuit-Integration Constraints

#### 4.7.1 Addressing: why 1T1M

- Bare crossbar is incompatible with volatile, rectification-free devices (sneak paths, read disturb, lack of selector)
- 1T1M (one transistor + one memristor) is the minimum viable architecture: the access transistor provides selection, current compliance, and read/write isolation
- Trade-off: density loss vs. readout discipline gained

#### 4.7.2 Read/write protocol

- Write pulses: amplitude and width defined by the φ_i fits of §4.3
- Read pulses: low-amplitude, sub-threshold, chosen so that the state update per read is at least one order of magnitude below the target resolution
- Read disturb budget: estimate the maximum number of consecutive reads tolerated before the state drifts by one resolvable level

#### 4.7.3 Front-end electronics

- Pulse generator / DAC + driver
- Access transistor per device
- Current-limiting element
- Transimpedance amplifier or precision shunt
- Sample-and-hold + ADC
- Digital readout / training block (MCU or FPGA)

#### 4.7.4 Variability envelope

- Derived directly from the parameter-card distributions in §4.3
- Reported as "acceptable performance region" in a figure: accuracy (or detection probability) vs. injected variability
- Used to define the *fabrication tolerance* that would be required for a real hardware build

#### 4.7.5 Sanity checks from Paper 1 impedance data

- Impedance spectroscopy is a supplementary, Li-only dataset (see §4.2.3): it is used *only* as a cross-check on the fastest meaningful timescale, not as a primary fitting input
- The RC timescales measured on the Paper 1 Li device set a hard lower bound on the fastest meaningful Δt in every simulation
- Any application that would require dynamics faster than this bound is explicitly ruled out in the chapter, rather than silently extrapolated to Na and K

---

### 4.8 Design Rules and Scope

#### 4.8.1 Where these devices are useful

- Temporal edge processing at sub-kHz rates
- Event-driven sensing with sparse activity
- Biomedical or environmental waveform classification with second-scale context
- Any task where a fading-memory bank with τ ∈ [10⁻¹, 10¹] s is a good match
- Applications where variability is either tolerable (reservoir) or averaged out (statistical detectors)

#### 4.8.2 Where they are *not* useful — and the chapter will say so

- High-density non-volatile storage
- Trained crossbar inference where weights must be precise and stable
- GHz-scale logic or signal processing
- Applications where retention > minutes is required without active refresh

#### 4.8.3 Design rules in one table

| Design goal | Lever | Mechanism |
|-------------|-------|-----------|
| Longer fading memory | Harder-acid cation (Li) | Stronger cation–oxygen coordination in Hybrane |
| Shorter fading memory | Softer-acid cation (K) | Weaker coordination, faster relaxation |
| More heterogeneous reservoir | Mixed-species device population | Distinct λ_i and φ_i per device |
| Lower write energy | Smaller pulse amplitude / number | Sublinear φ_i at low drive |
| Lower read disturb | Lower read voltage | Sub-threshold f_i evaluation |
| Better coincidence timing resolution | Faster species (K) | Narrower K(Δt) |
| Better memory capacity (reservoir) | Slower species (Li) | Longer λ_i |

#### 4.8.4 What Chapter 5 will inherit from this chapter

- Design rules → future hardware build list
- Variability envelopes → fabrication tolerance requirements
- Application benchmarks → the metrics against which future work should be judged

---

## Figures Planned for Chapter 4

*(Analogous in scope to the Chapter 2 figure reference list in `03_chapter2_figures_needed.md`. Numbering is indicative only.)*

| Label | Description | Source / How generated |
|-------|-------------|-----------------------|
| `fig:ch4_framing` | Conceptual schematic contrasting a static-weight crossbar with a heterogeneous fading-memory bank | Original schematic |
| `fig:ch4_dataset_map` | Visual inventory of the three common Li/Na/K datasets (I–V, N-pulse, delay-time) across the `ch4_device_manifest.csv` devices | `chapter4_pipeline.py` over `Nanomem_Devices_Library/` |
| `fig:ch4_model_fits` | Example model fits overlayed on I–V (`Day1_Hyst`), N-pulse potentiation (`Day2_NmbPls`), and delay-time depotentiation (`Day2_DlyTime`) for one Li, one Na and one K device | `chapter4_pipeline.py` |
| `fig:ch4_param_cards` | Parameter distributions (f_i from I–V, φ_i from N-pulse, λ_i from delay-time) for Li, Na, K across the manifest devices | `chapter4_pipeline.py` |
| `fig:ch4_reservoir_arch` | Schematic of the heterogeneous reservoir architecture with Li/Na/K banks and linear readout | Original schematic |
| `fig:ch4_reservoir_bench` | Memory capacity and classification accuracy vs. reservoir size and heterogeneity | Simulation from parameter cards |
| `fig:ch4_reservoir_variability` | Accuracy vs. injected device-to-device and cycle-to-cycle spread | Simulation from parameter cards |
| `fig:ch4_coincidence_kernel` | Fitted delay-time depotentiation curves reinterpreted as coincidence kernels K_i(Δt) for Li, Na, K | From Chapter 3 `Day2_DlyTime` data |
| `fig:ch4_coincidence_det` | Detection probability vs. Δt for each ion species under noise | Simulation from parameter cards |
| `fig:ch4_filterbank_impulse` | Impulse responses h_Li(t), h_Na(t), h_K(t) reconstructed from (λ_i, φ_i), compared to ideal leaky integrators with the same τ | Simulation from parameter cards |
| `fig:ch4_filterbank_task` | Onset / burst-detection performance using the three-channel filter bank | Simulation from parameter cards |
| `fig:ch4_1t1m` | 1T1M cell schematic, read/write protocol waveforms, read-disturb budget (bound from Paper 1 impedance data) | Original schematic |
| `fig:ch4_design_rules` | Visual summary of the §4.8.3 design-rules table | Original schematic |

---

## Datasets Required (All Already Acquired)

*Authoritative specification: `handouts/05_chapter4_data_pipeline.md`.*

**Common Li/Na/K datasets (primary inputs for every simulation):**

- I–V hysteresis (`Day1_Hyst`) — triangular sweep, common protocol across Li/Na/K
- N-pulse potentiation (`Day2_NmbPls`) — fixed V_write/t_write, logarithmic sweep in N
- Delay-time depotentiation (`Day2_DlyTime`) — fixed potentiation burst, logarithmic sweep in Δt
- Replicates within each of the above provide both device-to-device and cycle-to-cycle spread

**Paper 1 Li supplementary datasets (priors and sanity checks only, *never* used to support Na/K claims):**

- EPSC multi-state pulse train
- STDP paired-pulse kernel
- Separated STM/LTM retention (two-voltage protocol)
- Impedance spectroscopy

**Curated device list:** `handouts/ch4_device_manifest.csv`, frozen at the start of Chapter 4 writing, with ≥ 3 devices per ion species all passing the read-disturb sanity check (§3.4 of `05_chapter4_data_pipeline.md`).

No new fabrication is required. This is a deliberate design choice: it keeps the chapter scope achievable and makes the thesis independent of any future experimental campaign.

---

## What Chapter 4 Must *Not* Do

- It must not drift into speculative "future hardware that we did not build" territory. Every claim must be supported by (i) measured data, (ii) a fitted compact model, or (iii) a clearly labelled simulation based on those two.
- It must not re-run the retention/endurance benchmark language of the ReRAM literature. Those metrics are mentioned only to state, briefly, why they are the wrong yardstick.
- It must not train nonlinear readouts on the reservoir state (the whole point of reservoir computing is that only the readout is linear). Any departure from this rule is a red flag.
- It must not claim device-level novelty beyond what Chapters 2 and 3 have already established. Chapter 4's novelty is in *use and framing*, not in new materials.

---

## Pedagogical Notes for Writing

- The chapter should read as a *deliberate reinterpretation* of the Chapter 2–3 data, not as a new experimental chapter. The reader should feel that the data were always pointing this way and Chapters 2 and 3 were one step short of saying so.
- The flagship reservoir computing section (§4.4) carries most of the chapter's scientific weight. It should be the longest and most carefully written section.
- The coincidence detection (§4.5) and filter bank (§4.6) sections are supporting cases. They are shorter, but each must stand on its own by reporting measurable metrics, not just intuitions.
- Every simulation figure must name its input dataset in the caption (e.g. "fitted to retention curves of NM_vXXX–NM_vYYY"). This is what separates the chapter from pure theory.
- The §4.7 circuit-integration section is necessary for credibility. Without it, the chapter can be attacked as "just simulation". With it, the chapter defines a clear, physically implementable route to a real build.
- The §4.8 design-rules section is the chapter's hand-off to Chapter 5. Write it so that a reader could skip directly from §4.8 to Chapter 5's future-directions list and understand the link immediately.
- Tone: definitive and active, as in the other chapters. *"We extract", "the model predicts", "the reservoir achieves"* — not *"one could imagine"*.
- The chapter's last sentence should close the thesis-wide framing loop: these devices are not failed non-volatile memories; they are functional temporal computing primitives whose chemistry is the design knob.
