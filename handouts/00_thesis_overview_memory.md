<!-- markdownlint-disable-file MD013 -->

# PhD Thesis — Durable Memory Document

**Author:** Carlos David Prado-Socorro  
**Institution:** Universitat de València — Institute of Molecular Science (ICMol)  
**Group:** Nanotech / Memristive Devices  
**Supervisor:** Salvador Cardona-Serra (PI: Eugenio Coronado)  
**Generated:** April 7, 2026  
**Revision:** v2 — April 11, 2026. Thesis restructured from 4 chapters to 5 chapters. A dedicated data-driven temporal computing chapter (new Chapter 4) is inserted before the conclusions, and the device framing is changed across the whole thesis: the Li/Na/K family is now presented as a set of volatile, heterogeneous temporal computing primitives, not as candidate non-volatile memories.  

---

## 1. Research Identity

**Title (working):** *Organic Memristive Devices Based on Polymer–Electrolyte Composites for Neuromorphic Computing*

**Core thesis:** That a carefully engineered composite of a semiconducting polymer (Super Yellow), an ion-transport polymer (Hybrane DEO750 8500), and a dissociated ionic salt (lithium, sodium, or potassium triflimide) deposited as a thin film between two electrodes constitutes a functional two-terminal organic memristive device capable of analog, reversible, multi-state conductance switching, short-term and long-term memory, and Hebbian learning in a single device — properties that arise from ionic migration mediated by Lewis acid–base interactions between the solvated ions and the polymer matrix.

---

## 2. The Scientific Problem Being Solved

### 2.1 Von Neumann Bottleneck

Modern computers physically separate the CPU from memory (RAM/storage), forcing data to traverse a shared bus for every operation. This creates a throughput ceiling — the "von Neumann bottleneck" — that becomes critical as AI workloads demand processing of petabytes of data at high frequency.

### 2.2 Neuromorphic Computing as the Solution

Biological neural networks avoid this bottleneck by co-locating computation and memory at the synapse. The synapse implements both short-term potentiation (working memory) and long-term potentiation (persistent learning) via changes in synaptic weight. Hardware that mimics this can perform in-memory computation with orders of magnitude better energy efficiency.

### 2.3 The Role of the Memristor

A memristor (Chua, 1971) is a 2-terminal passive element whose resistance depends on the history of charge or current flow. It is the natural hardware analogue of a biological synapse. The conductance of a memristor maps directly onto synaptic weight; its history-dependent resistance embodies memory; its continuous variability enables analog computation.

### 2.4 Why Organic Materials?

Inorganic memristors (TiO₂, phase-change, conductive-bridge) suffer from: poor reproducibility due to stochastic filament formation; limited chemical tunability; rigid substrates; toxicity; and biocompatibility issues for nervetronic applications. Organic materials, by contrast, offer: molecular-level tunability via synthetic chemistry; solution processability (inkjet, spin-coating); mechanical flexibility; low cost; biocompatibility; and the possibility of exploiting multiple mechanisms (ionic, redox, conformational) for richer synaptic behaviour.

---

## 3. Materials System

### 3.1 Super Yellow (SY)

Poly[{2,5-di(3′,7′-dimethyloctyloxy)-1,4-phenylenevinylene}-co-{3-(4′-(3′′,7′′-dimethyloctyloxy)phenyl)-1,4-phenylenevinylene}-co-{3-(3′-(3′,7′-dimethyloctyloxy)phenyl)-1,4-phenylenevinylene}] — a PPV-family conjugated polymer. Acts as the semiconducting matrix providing electronic conductance pathways. Soluble in cyclohexanone. Well-characterised in LECs (Mardegan et al. Adv. Funct. Mater. 2021, demonstrating 1600 h electroluminescence lifetime when formulated with Hybrane).

### 3.2 Hybrane DEO750 8500

A hyperbranched polyester-amide solid electrolyte. Contains a large density of oxygen atoms (ether and ester groups) on its side chains that act as hard Lewis bases, preferentially coordinating hard Lewis acid cations (Li⁺ > Na⁺ > K⁺ in order of charge density). Its low cohesive energy allows segmental motion, facilitating ion hopping and solvation. Serves as the ion-conductive mediator — the polymer "highway" along which ions migrate.

### 3.3 Ionic Salts Used

| Salt | Cation | Anion | Paper/Generation |
| ------ | -------- | ------- | ----------------- |
| LiCF₃SO₃ (LiTf) | Li⁺ (hard acid) | CF₃SO₃⁻ (triflate, soft base) | Paper 1; NM_v001–v200 approx. |
| LiN(SO₂CF₃)₂ (LiBis/LiTFSI) | Li⁺ | bis(trifluoromethanesulfonyl)imide⁻ | Ag-electrode series |
| NaN(SO₂CF₃)₂ (NaBis/NaTFSI) | Na⁺ | TFSI⁻ | Ag-electrode comparative series |
| KN(SO₂CF₃)₂ (KBis/KTFSI) | K⁺ | TFSI⁻ | Ag-electrode comparative series |

The key chemical insight: the difference in Lewis acid–base interaction strength between the cation and the Hybrane oxygen atoms determines how easily each ion migrates under an electric field, thereby governing the memory retention time (harder acid → stronger coordination → harder to displace → longer memory).

### 3.4 Composite Formulation (Paper 1)

- SY: 15 → 8.72 mg/mL (after mixing)
- Hybrane: 10 → 2.62 mg/mL
- LiCF₃SO₃: 5 → 0.78 mg/mL
- Mass ratio (SY:Hybrane:LiTf) = 1:0.30:0.09
- Solvent: cyclohexanone
- All steps under N₂ atmosphere

---

## 4. Device Architecture

Vertical 2-T sandwich structure:
```
         [Ag, 100 nm, evaporated]
         [Active layer, ~209 nm]
[ITO-patterned glass substrate, transparent]
```

- Active area per junction: 0.0825 cm²
- ITO bottom electrode: pre-patterned; cleaned ultrasonically (Mucasol, water, 2-propanol); dried under N₂
- Spin-coating: 2000 rpm, 60 s; anneal 75°C, 3 h (under N₂)
- Top electrode: Ag deposited by thermal evaporation through shadow mask (100 nm)
- All post-cleaning processing in N₂-filled glovebox

---

## 5. Characterisation Methods

| Technique | Instrument | What it measures |
| ----------- | ----------- | ----------------- |
| Profilometry | Ambios XP-1 | Active layer thickness |
| AFM (tapping mode) | Bruker Dimension Icon | Surface topography, RMS roughness |
| I–V hysteresis | Keithley 2450 + TSB | Memristive switching behaviour |
| EPSC | Keithley 2450 + TSB | State-dependent conductance after voltage pulses |
| STM/LTM (pulse-number & wait-time) | Keithley 2450 + TSB | Memory retention kinetics |
| STDP | Keithley 2450 + TSB | Hebbian learning function |
| Impedance spectroscopy | SR865A Lock-in Amplifier | Ionic transport, RC equivalent circuit |

---

## 6. Key Numerical Results (Paper 1)

| Property | Value |
| ---------- | ------- |
| Film thickness | 209 nm |
| Conductance potentiation | ≥200% (50 pulses, 1 V) |
| EPSC ratio S₁/S₀ | 7.333 |
| EPSC ratio S₂/S₀ | 15.553 |
| Energy per synaptic event | ≈50 nJ (≈6 fJ/100 nm²) |
| STM characteristic time τ_S | 2.5–3 s |
| LTM characteristic time τ_L | 4.7 s |
| STM retention | 10–15 s |
| LTM retention | >45 s |
| STDP time constant τ | 85–90 ms |
| Biological synapse τ | ≈100 ms |
| Device stability (non-encapsulated) | ~2 weeks (≈300 h) |

---

## 7. Theoretical Framework

Two mechanisms, reconciled by injection regime (van Reenen et al. JACS 2010):

1. **Electrodynamic model** (injection-limited): Ions accumulate at electrodes forming a charged double layer → bends polymer valence/conduction bands → lowers Schottky barrier → more charge injection.

2. **Electrochemical Doping model** (ohmic injection): Ion accumulation dopes the conjugated polymer electronically → changes polymer conductivity.

Memory regimes explained by Lewis acid–base chemistry:

- CF₃SO₃⁻ (triflate): soft Lewis base → weak interaction with Hybrane O → displaced by low voltage (1 V) → STM (fast relaxation 10–15 s)
- Li⁺: hard Lewis acid → strong coordination with Hybrane O → requires high voltage (3 V) to displace → LTM (slow relaxation >45 s)

---

## 8. Thesis Narrative Arc (v2 — 5-chapter structure)

```
Chapter 1: Introduction
    (Computing crisis → neuromorphic computing → memristors →
     organic electronics → polymer composites → ionic memristors →
     volatility and variability as computational resources →
     temporal/event-driven computing paradigms → thesis objectives)
    ↓
Chapter 2: Proof of Concept — SY/Hybrane/LiTf / Ag electrode
    (Paper 1; demonstrates all key memristive functionalities
     in a single, fully characterised device)
    ↓
Chapter 3: Ion-Dependent Device Physics — Li/Na/K / Ag electrode
    (Systematic exploration of cation chemistry effects; Li, Na, K
     framed as a fading-memory timescale ladder and variability
     characterised as a physical property, not a defect)
    ↓
Chapter 4: Data-Driven Temporal Computing
    (No new fabrication. Compact behavioural models extracted from the
     I–V, N-pulse potentiation, and delay-time depotentiation datasets
     of Chapters 2–3. Three application schemes simulated from those
     models: heterogeneous physical reservoir computing (flagship),
     spike coincidence detection, and multi-timescale transient filtering.
     Circuit-level integration constraints and design rules.)
    ↓
Chapter 5: Conclusions & Outlook
    (Synthesis across the chemistry axis (Ch. 2–3) and the application
     axis (Ch. 4). Benchmarks drawn from temporal / reservoir / event-driven
     hardware, not from digital memory.)
```

**Key framing decision carried through every chapter:** these devices are not framed as failed non-volatile memories. They are framed as good volatile, heterogeneous, temporally rich elements. See `handouts/01_thesis_structure.md` for the framing-consequence table.

---

## 9. Key Publications and Citations (for BibTeX use)

```
@article{PradoSocorro2022,
  author  = {Prado-Socorro, Carlos David and Giménez-Santamarina, Silvia and 
             Mardegan, Lorenzo and Escalera-Moreno, Luis and Bolink, Henk J. and 
             Cardona-Serra, Salvador and Coronado, Eugenio},
  title   = {Polymer-Based Composites for Engineering Organic Memristive Devices},
  journal = {Advanced Electronic Materials},
  year    = {2022},
  volume  = {8},
  pages   = {2101192},
  doi     = {10.1002/aelm.202101192}
}

@article{Chua1971,
  author  = {Chua, Leon O.},
  title   = {Memristor -- The Missing Circuit Element},
  journal = {IEEE Transactions on Circuit Theory},
  year    = {1971},
  volume  = {18},
  pages   = {507--519}
}

@article{Strukov2008,
  author  = {Strukov, Dmitri B. and Snider, Gregory S. and Stewart, Duncan R. and Williams, R. Stanley},
  title   = {The missing memristor found},
  journal = {Nature},
  year    = {2008},
  volume  = {453},
  pages   = {80--83}
}

@article{Mardegan2021,
  author  = {Mardegan, Lorenzo and Dreessen, Christopher and Sessolo, Michele and 
             Tordera, Denissé and Bolink, Henk J.},
  title   = {Hyperbranched Polyesters as Efficient Ion-Transport Hosts in Light-Emitting Electrochemical Cells},
  journal = {Advanced Functional Materials},
  year    = {2021},
  volume  = {31},
  pages   = {2104249}
}
```

---

## 10. Status of Written Work (as of 2026-04-11)

| Item | Status | Location |
| ------ | -------- | ---------- |
| Memory document (v2) | ✅ Complete | `handouts/00_thesis_overview_memory.md` |
| Thesis structure — 5 chapters (v2) | ✅ Complete | `handouts/01_thesis_structure.md` |
| Introduction chapter plan (v2, with temporal computing sections) | ✅ Complete | `handouts/02_introduction_chapter_plan.md` |
| Chapter 2 figures reference list | ✅ Complete | `handouts/03_chapter2_figures_needed.md` |
| Chapter 2 (LaTeX, full) | ✅ Complete | `handouts/chapter2_proof_of_concept.tex` |
| Chapter 4 planning document | ✅ Complete | `handouts/04_chapter4_temporal_computing_plan.md` |
| Chapter 4 data / pipeline spec | ✅ Complete | `handouts/05_chapter4_data_pipeline.md` |
| References database (`references.bib`, with reservoir-computing core added) | ✅ Complete | `handouts/references.bib` |
| Chapter 1 (writing) | ⬜ Not started | — |
| Chapter 3 (writing) | ⬜ Not started | — |
| Chapter 4 (writing) | ⬜ Not started | — |
| Chapter 5 (writing) | ⬜ Not started | — |
