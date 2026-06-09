---
name: Paper 1 Summary
description: Full scientific content of Prado-Socorro et al. Adv. Electron. Mater. 2022 — proof-of-concept organic memristive device, basis for thesis Chapter 2
type: project
---

# Paper 1: Polymer-Based Composites for Engineering Organic Memristive Devices
**Citation:** C. D. Prado-Socorro, S. Giménez-Santamarina, L. Mardegan, L. Escalera-Moreno, H. J. Bolink, S. Cardona-Serra, E. Coronado, *Adv. Electron. Mater.* **2022**, *8*, 2101192. DOI: 10.1002/aelm.202101192

## Device Architecture
- Vertical 2-T structure: ITO / active layer / Ag (100 nm)
- Active layer: SY (8.72 mg/mL) + Hybrane DEO750 8500 (2.62 mg/mL) + LiCF₃SO₃ (0.78 mg/mL) in cyclohexanone
- Mass ratio 1:0.30:0.09 (SY:Hybrane:LiTf)
- Spin-coating at 2000 rpm, 60 s; anneal 75°C, 3 h; under N₂
- Film thickness: 209 nm (profilometry); surface characterised by AFM

## Key Results
### I–V Hysteresis
- Triangular voltage sweeps (±1.2 V, rate 0.25 V/s, 10 s between cycles)
- Successive single-polarity sweeps → increasing conductance (+140% from cycle 1→2; still +6.3% at cycle 9→10)
- Negative sweeps produce different hysteresis (attributed to electrochemical side-reactions at electrodes, insulating layer formation)

### Multi-State Conductance (Potentiation/Depression)
- Pulse protocol: 50 pulses at +1 V then 50 pulses at −2 V
- Conductance tunable by ≥200% (potentiation and depression)
- Energy per event: ≈50 nJ (≈6 fJ/100 nm²)

### EPSC (Excitatory Post-Synaptic Current)
- Ground state S₀ at V₀ = 1 V for 1 s
- +2 V pulse (0.05 s) → excited states S₁, S₂; −2.5 V pulse → S₃, S₄
- EPSC ratios (Sn/S₀): S₁=7.333, S₂=15.553, S₃=−3.716, S₄=−16.967

### Short-Term Memory (STM) vs Long-Term Memory (LTM)
- Reading pulse: Vread = 0.5 V; writing: Vwrite = 1 V (STM) or 3 V (LTM)
- Reset: 300 s at short-circuit
- STM (1 V, 10 or 50 pulses): τ_S = 2.5–3 s; retention 10–15 s
- LTM (3 V, 10 pulses): τ_L = 4.7 s; retention > 45 s
- Kohlrausch stretched-exponential decay fits
- STM to LTM transition determined by ionic species mobility (Li⁺ hard acid, strongly bound to O in Hybrane → requires higher voltage)

### STDP (Spike-Timing Dependent Plasticity)
- Pre/post-synaptic spike pairs separated by Δt (−600 to +600 ms)
- Δt < 0: synaptic potentiation; Δt > 0: synaptic depression
- Asymmetric anti-Hebbian learning: ΔG = A·exp(−Δt/τ) + G₀
- τ = 85–90 ms (biological synapses: ≈100 ms)
- Spiking voltage Vsp = 1.55 V

## Transport Mechanism
Two models reconciled (van Reenen et al. 2010):
1. **Electrodynamic model** (injection-limited): ionic double layer bends valence/conduction bands, reduces Schottky barrier
2. **Electrochemical Doping model** (ohmic injection): cation/anion displacement dopes the semiconducting polymer
- Li⁺ (hard acid) ↔ O atoms of Hybrane (hard base) → strong Lewis interaction → high voltage threshold for migration → LTM
- CF₃SO₃⁻ (soft base) → weak interaction → easily displaced at low voltage → STM

## Device Stability
- Non-encapsulated devices functional for ~2 weeks (≈300 working hours) in air at RT
- Active layer robustness demonstrated in LECs (electroluminescence lifetime ≈1600 h, Mardegan et al. Adv. Funct. Mater. 2021)
