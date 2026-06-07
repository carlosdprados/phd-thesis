<!-- markdownlint-disable-file MD013 -->

# Chapter 2 — Figures Reference List

**Author:** Carlos David Prado-Socorro  
**Date:** April 7, 2026  

This document lists all figures referenced in `chapter2_proof_of_concept.tex` with their labels, captions, and source instructions.

---

## Figure List

### `fig:device_schematic`

**Label:** `\label{fig:device_schematic}`  
**Caption (suggested):** Schematic representation of the two-terminal vertical synaptic device architecture. (a) Depiction of the biological neural synapse with pre- and postsynaptic neurons and neurotransmitters as the biological template. (b) Device architecture: ITO-glass bottom electrode / composite active layer / Ag top electrode (100 nm). (c) Molecular structures of the three active layer components: Super Yellow (SY, semiconducting PPV copolymer), Hybrane DEO750 8500 (ion-transport hyperbranched polyester), and lithium triflate (LiCF₃SO₃). (d) Proposed mechanism of STM and LTM: at low voltage, fast-moving triflate anions redistribute (STM); at high voltage, slow-moving Li⁺ cations are also displaced (LTM).  
**Source:** Figure 1 of Prado-Socorro et al. *Adv. Electron. Mater.* 2022, 8, 2101192.  
**File path (suggested):** `figures/ch2_fig1_device_schematic.pdf`

---

### `fig:iv_hyst`

**Label:** `\label{fig:iv_hyst}`  
**Caption (suggested):** Current–voltage hysteresis characterisation of the composite memristive device. (a) Ten successive positive triangular voltage sweeps (0 to +1.2 V, 0.25 V/s, 10 s between cycles) showing progressive increase of conductance. The current at 1 V increases by 140% from cycle 1 to cycle 2. (b) Pulsed voltage sequence (50 × +1 V pulses followed by 50 × −2 V pulses) used for multi-state conductance modulation shown in (c). (c) Potentiation and depression of device conductance, demonstrating >200% tuning range.  
**Source:** Figure 2 of Prado-Socorro et al. *Adv. Electron. Mater.* 2022, 8, 2101192.  
**File path (suggested):** `figures/ch2_fig2_iv_hysteresis.pdf`

---

### `fig:potentiation`

**Label:** `\label{fig:potentiation}`  
**Caption (suggested):** Analog multi-state conductance tunability under a pulse-train protocol. Fifty consecutive write pulses of +1 V continuously potentiate the device conductance by more than 200%, and fifty subsequent write pulses of −2 V depotentiate it back toward the initial state. The smooth and monotonic trajectories demonstrate reversible analog tuning without abrupt SET/RESET transitions.  
**Source:** Figure 2c of Prado-Socorro et al. *Adv. Electron. Mater.* 2022, 8, 2101192.  
**File path (suggested):** `figures/ch2_fig3_potentiation_depression.pdf`

---

### `fig:epsc`

**Label:** `\label{fig:epsc}`  
**Caption (suggested):** Excitatory post-synaptic current (EPSC) measurements. (a) Applied voltage and measured current as a function of time during the EPSC protocol. Ground state S₀ is established at +1 V; positive pulses of +2 V produce excited states S₁ and S₂; negative pulses of −2.5 V produce inhibitory states S₃ and S₄. Signed EPSC readout ratios, referenced to the ground-state response under the fixed measurement convention, are: S₁ = 7.33, S₂ = 15.55, S₃ = −3.72, S₄ = −16.97. The four states are readily distinguishable, demonstrating robust multi-state operation.  
**Source:** Figure 3a of Prado-Socorro et al. *Adv. Electron. Mater.* 2022, 8, 2101192.  
**File path (suggested):** `figures/ch2_fig4_epsc.pdf`

---

### `fig:stm_ltm`

**Label:** `\label{fig:stm_ltm}`  
**Caption (suggested):** Two-step protocol used for the STM/LTM retention measurements. A low read pulse establishes the baseline conductance $G_0$, a train of write pulses perturbs the ionic configuration, and a second read pulse after a controlled waiting time $t_\mathrm{wait}$ measures the relaxed state $G_f$.  
**Source:** Figure 3b of Prado-Socorro et al. *Adv. Electron. Mater.* 2022, 8, 2101192.  
**File path (suggested):** `figures/ch2_fig4_stm_ltm_protocol.pdf`
**Note:** This label is reserved for the retention-protocol schematic cited in the text at the start of the STM/LTM subsection. The actual decay curves remain under `fig:retention`.

---

### `fig:npulse`

**Label:** `\label{fig:npulse}`  
**Caption (suggested):** Dependence of conductance change (ΔG = G_f/G₀ × 100%) on the number of applied write pulses ($N_\mathrm{pulses}$) for $V_\mathrm{write}$ = 1 V and $t_\mathrm{wait}$ = 150 ms. The monotonically increasing relationship plotted on a logarithmic pulse-number axis demonstrates analog potentiation controllable over more than three decades of pulse count. The shaded region indicates the standard deviation of measurements across multiple independent devices.  
**Source:** Figure 3c of Prado-Socorro et al. *Adv. Electron. Mater.* 2022, 8, 2101192.  
**File path (suggested):** `figures/ch2_fig5_npulse.pdf`

---

### `fig:retention`

**Label:** `\label{fig:retention}`  
**Caption (suggested):** Memory retention kinetics. Conductance ratio (G_f/G₀ × 100%) as a function of waiting time $t_\mathrm{wait}$ for STM (1 V, 10 and 50 pulses, blue/red) and the longer-lived regime conventionally denoted LTM (3 V, 10 pulses, black). Solid lines are fits to the modified Kohlrausch stretched exponential function (Eq. 2.1). Characteristic times: $\tau_S$ = 2.5–3 s (STM); $\tau_L$ = 4.7 s (LTM). Operational retention: 10–15 s (STM); >45 s (LTM).  
**Source:** Figure 3d of Prado-Socorro et al. *Adv. Electron. Mater.* 2022, 8, 2101192.  
**File path (suggested):** `figures/ch2_fig6_retention.pdf`

---

### `fig:stdp`

**Label:** `\label{fig:stdp}`  
**Caption (suggested):** Spike-timing dependent plasticity (STDP) characterisation. (a) Measured STDP function: percentage conductance change ΔG as a function of pre/post-synaptic spike timing delay Δt, fitted to the asymmetric Hebbian model (Eq. 2.2; Δt = t_post − t_pre). Δt < 0: synaptic potentiation; Δt > 0: synaptic depression. Fitted time constant τ = 85–90 ms, consistent with biological values (~100 ms). Inset: schematic of pre- and postsynaptic voltage waveforms separated by delay Δt. (b–d) Total applied voltage waveform for Δt = +600, −300, and +50 ms, respectively, showing the algebraic summation of pre- and postsynaptic spike waveforms.  
**Source:** Figure 4 of Prado-Socorro et al. *Adv. Electron. Mater.* 2022, 8, 2101192.  
**File path (suggested):** `figures/ch2_fig7_stdp.pdf`

---

### `fig:mechanism_schematic`

**Label:** (for the ion transport mechanism, Figure 5 in the paper)  
**Caption (suggested):** Schematic 1D representation of ion transport mechanisms in the composite active layer. (a) Electrodynamic model: in the injection-limited regime, ionic double layers at the electrodes bend the polymer valence/conduction bands, reducing the Schottky barrier and increasing charge injection. (b) Electrochemical Doping model: in the ohmic injection regime, ionic double layers electrochemically dope the polymer, producing p-doped (anode) and n-doped (cathode) regions with enhanced conductivity.  
**Source:** Figure 5 of Prado-Socorro et al. *Adv. Electron. Mater.* 2022, 8, 2101192.  
**File path (suggested):** `figures/ch2_fig8_mechanism.pdf`

---

## Additional Figures Recommended for the Thesis Version (Beyond the Paper)

### `fig:afm_comparison`

**Description:** AFM topography images at multiple spin speeds (500, 1000, 2000, 3000 rpm) showing smooth surface and low RMS roughness; histogram of RMS roughness values.  
**Source:** Supporting Information, Prado-Socorro et al. 2022.  
**File path (suggested):** `figures/ch2_fig_afm_spinspeed.pdf`

### `fig:profilometry`

**Description:** Representative profilometry trace across a masked step edge, showing film thickness of 209 nm at 2000 rpm; plot of thickness vs. spin speed.  
**Source:** Supporting Information, Prado-Socorro et al. 2022.  
**File path (suggested):** `figures/ch2_fig_profilometry.pdf`

### `fig:device_optical`

**Description:** Optical microscopy image of a completed device showing ITO finger pattern, active layer area, and Ag top electrode pads.  
**Source:** Supporting Information (Figure S5), Prado-Socorro et al. 2022.  
**File path (suggested):** `figures/ch2_fig_device_optical.pdf`

### `fig:degradation`

**Description:** Time evolution of key device parameters (G₀, ΔG_max, τ_S) over two weeks under ambient conditions (non-encapsulated).  
**Source:** Supporting Information (Figure S4), Prado-Socorro et al. 2022.  
**File path (suggested):** `figures/ch2_fig_degradation.pdf`

### `fig:hsab_diagram`

**Description:** Schematic of HSAB (Hard-Soft Acid-Base) interactions between Li⁺, CF₃SO₃⁻, and the Hybrane O-atom coordination sites; energy landscape illustration showing differential activation barriers for Li⁺ vs. triflate migration.  
**Source:** Original schematic (to be created).  
**File path (suggested):** `figures/ch2_fig_hsab_mechanism.pdf`

---

## Notes on Figure Quality for Thesis Submission

- All figures must be provided at ≥300 DPI for raster images; vector (PDF/EPS) preferred for plots
- Font size in figure labels must be consistent with body text (≥8 pt)
- Scale bars required in all AFM and optical microscopy images
- All axes must have units; use SI units throughout
- Colour schemes should be perceptually uniform and colour-blind friendly (e.g., viridis, cividis)
- Raw data for all figures is available in `Nanomem_Devices_Library/` under the relevant device/quarter folder
