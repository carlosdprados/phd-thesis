<!-- markdownlint-disable-file MD013 -->

# PhD Thesis — Durable Memory Document

**Author:** Carlos David Prado-Socorro  
**Institution:** Universitat de València — Institute of Molecular Science (ICMol)  
**Group:** Nanotech / Memristive Devices  
**Supervisor:** Salvador Cardona-Serra (PI: Eugenio Coronado)  
**Generated:** April 7, 2026  
**Revision:** v4 — 2026-06-03. After direct, QA'd analysis of the archive (handouts `08_chapter3_4_claims_audit.md` and `10_chapter3_comparative_plan.md`): Chapter 3's **quantitative spine is the PEO/LiTr composition grid** (the only statistically-replicated axis, n=2–4); **host/anion/cation form an illustrative, sample-limited tuning landscape** (n≤2 per matched cell); the **Li>Na>K cation hypothesis is reported as an honest negative** (confounded by drive-protocol amplitude and electrode); and **potentiation amplitude is shown to set the apparent fading-memory τ** (methodological result). Previous: v3 — April 12, 2026. The comparative-chapter chemistry had been re-scoped to match the actual experimental archive. The main Chapter 3 corpus is now explicitly PEO-based triflate composites (PEO/LiTr, PEO/NaTr, PEO/KTr at PEO and salt mass concentrations of 0.3 and 0.09), supplemented by a PEO/LiTr concentration series, and the common comparative measurements are restricted to I–V hysteresis, variable-number-of-pulses potentiation, and variable-delay-time depotentiation. TMPE-based and LiBis/NaBis/KBis (TFSI) devices are retained only as exploratory side systems. EPSC, STDP, separated STM/LTM retention, and impedance spectroscopy remain Chapter 2 (Paper 1) results and are no longer presented as common across the Li/Na/K family. Previous revisions: v2 (2026-04-11) inserted the data-driven temporal computing chapter and switched the framing to volatile, heterogeneous temporal computing primitives.  

---

## 1. Research Identity

**Title (working):** *Organic Memristive Devices Based on Polymer–Electrolyte Composites for Neuromorphic Computing*

**Core thesis:** That a carefully engineered composite of a semiconducting polymer (Super Yellow) and an ion-conducting polyether matrix loaded with a dissociated alkali-metal triflate salt, deposited as a thin film between two electrodes, constitutes a functional two-terminal organic memristive device whose analog, reversible conductance dynamics and fading-memory timescales are tuned by the ionic chemistry of the composite. The proof of concept (Chapter 2) is built on SY/Hybrane/LiTf and exhibits the full range of memristive functionalities — analog multi-state switching, short- and long-term memory, excitatory post-synaptic current, and spike-timing-dependent plasticity — in a single device. The main comparative study (Chapter 3) has its **quantitative spine in the PEO/LiTr composition grid** (the only axis that replicates, n=2–4): switching window, potentiation, and a Kohlrausch fading-memory τ (≈ 2–20 s) all vary systematically with composition. Electrolyte **chemistry — host (PEO/TMPE), anion (triflate/TFSI), cation (Li/Na/K) — is surveyed as an illustrative, sample-limited tuning landscape** (n≤2 per matched cell); the **Li>Na>K cation hypothesis is an honest negative** (confounded by drive-protocol amplitude and electrode), and a methodological result shows **potentiation amplitude sets the apparent τ**. The corpus rests on three common dynamical measurements — I–V hysteresis, variable-number-of-pulses potentiation, and variable-delay-time depotentiation — and the richer synaptic metrics (EPSC, STDP, separated STM/LTM, impedance) are retained only for the Chapter 2 device.

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

### 3.2 Ion-Transport Polymer Hosts

Two polyether hosts appear in the thesis, and they must not be confused:

- **Hybrane DEO750 8500** — a hyperbranched polyester-amide solid electrolyte. Used only in Chapter 2 (the SY/Hybrane/LiTf proof-of-concept device). Contains a large density of oxygen atoms (ether and ester groups) on its side chains acting as hard Lewis bases, preferentially coordinating hard Lewis acid cations. Well-characterised in LECs (Mardegan *et al.* 2021).
- **Poly(ethylene oxide) (PEO)** — a linear polyether used as the ion-transport host in the main comparative corpus of Chapter 3 (PEO + triflate salts). PEO plays the analogous role to Hybrane: its ether oxygens coordinate alkali-metal cations and its segmental mobility enables ion hopping and solvation.
- **TMPE** (hyperbranched polyether, Hybrane-class) — used only in a small exploratory set of devices; retained as side evidence, not as a pillar of the comparative chapter.

### 3.3 Ionic Salts Used

| Salt | Cation | Anion | Role in the thesis |
| ------ | -------- | ------- | ------------------ |
| LiCF₃SO₃ (LiTf) | Li⁺ (hard acid) | CF₃SO₃⁻ (triflate, soft base) | **Chapter 2** (Paper 1) — SY/Hybrane/LiTf proof of concept |
| LiCF₃SO₃ (LiTr) | Li⁺ | CF₃SO₃⁻ | **Chapter 3 core** — PEO/LiTr, concentration series + 0.3/0.09 reference |
| NaCF₃SO₃ (NaTr) | Na⁺ | CF₃SO₃⁻ | **Chapter 3 core** — PEO/NaTr at 0.3/0.09 |
| KCF₃SO₃ (KTr) | K⁺ | CF₃SO₃⁻ | **Chapter 3 core** — PEO/KTr at 0.3/0.09 |
| LiN(SO₂CF₃)₂ (LiBis/LiTFSI) | Li⁺ | TFSI⁻ | Exploratory side system (limited dataset) |
| NaN(SO₂CF₃)₂ (NaBis/NaTFSI) | Na⁺ | TFSI⁻ | Exploratory side system (limited dataset) |
| KN(SO₂CF₃)₂ (KBis/KTFSI) | K⁺ | TFSI⁻ | Exploratory side system (limited dataset) |

The key chemical insight: the difference in Lewis acid–base interaction strength between the cation and the polyether oxygen atoms determines how easily each ion migrates under an electric field, thereby governing the memory retention time (harder acid → stronger coordination → harder to displace → longer memory). This principle is demonstrated on the Chapter 2 SY/Hybrane/LiTf device and is the working hypothesis for the PEO/triflate comparative series of Chapter 3.

**Composition convention for Chapter 3.** The reference comparative formulation is PEO at mass fraction 0.3 and salt at mass fraction 0.09 relative to the semiconductor, applied uniformly across LiTr, NaTr and KTr. Chapter 3 also includes a dedicated PEO/LiTr concentration sweep in which the PEO and salt mass fractions are varied around this reference to probe composition–dynamics relationships.

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

```text
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

| Technique | Instrument | What it measures | Availability |
| ----------- | ----------- | ----------------- | ------------- |
| Profilometry | Ambios XP-1 | Active layer thickness | All devices |
| AFM (tapping mode) | Bruker Dimension Icon | Surface topography, RMS roughness | All devices |
| I–V hysteresis (triangular sweep) | Keithley 2450 + TSB | Memristive switching behaviour; read transfer function | **Common across the PEO/LiTr, PEO/NaTr, PEO/KTr comparative corpus** |
| Variable-N pulse potentiation | Keithley 2450 + TSB | Per-pulse conductance update and saturation curve | **Common across the PEO/LiTr, PEO/NaTr, PEO/KTr comparative corpus** |
| Variable-delay depotentiation | Keithley 2450 + TSB | Fading-memory decay, characteristic time constant | **Common across the PEO/LiTr, PEO/NaTr, PEO/KTr comparative corpus** |
| EPSC | Keithley 2450 + TSB | State-dependent conductance after voltage pulses | Chapter 2 (Paper 1 Li device) only; sparse elsewhere |
| Separated STM/LTM (two-voltage retention) | Keithley 2450 + TSB | Memory retention kinetics in two regimes | Chapter 2 (Paper 1 Li device) only |
| STDP | Keithley 2450 + TSB | Hebbian learning function | Chapter 2 (Paper 1 Li device) only |
| Impedance spectroscopy | SR865A Lock-in Amplifier | Ionic transport, RC equivalent circuit | Chapter 2 (Paper 1 Li device) and a few Chapter 3 repeats only |

**Rule of thumb for later chapters:** any claim in Chapters 3 or 4 about the PEO/triflate comparative corpus must be supportable from the three common measurements (I–V, N-pulse, delay-time). EPSC, STDP, separated STM/LTM and impedance are valid only as prior / sanity-check evidence from the Chapter 2 device and must be labelled as such.

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

Memory regimes explained by Lewis acid–base chemistry (Chapter 2 SY/Hybrane/LiTf device):

- CF₃SO₃⁻ (triflate): soft Lewis base → weak interaction with Hybrane O → displaced by low voltage (1 V) → STM (fast relaxation 10–15 s)
- Li⁺: hard Lewis acid → strong coordination with Hybrane O → requires high voltage (3 V) to displace → LTM (slow relaxation >45 s)

The same principle motivates the Chapter 3 PEO/LiTr, PEO/NaTr, PEO/KTr comparative series: replacing Li⁺ by Na⁺ or K⁺ in the same polyether host reduces the cation–oxygen binding strength and is expected to shift the fading-memory timescale accessible through the common delay-time depotentiation measurement. This expectation is tested as a statement about dynamical timescales, not as a claim about EPSC/STDP/separated STM/LTM for Na/K devices.

---

## 8. Thesis Narrative Arc (v2 — 5-chapter structure)

```text
Chapter 1: Introduction
    (Computing crisis → neuromorphic computing → memristors →
     organic electronics → polymer composites → ionic memristors →
     volatility and variability as computational resources →
     temporal/event-driven computing paradigms → thesis objectives)
    ↓
Chapter 2: Proof of Concept — SY/Hybrane/LiTf
    (Paper 1; demonstrates all key memristive functionalities —
     I–V hysteresis, potentiation/depression, EPSC, STM, LTM, STDP,
     impedance — in a single, fully characterised device. This is
     the richest synaptic dataset in the thesis and is the only
     device on which EPSC, STDP, separated STM/LTM and impedance
     are treated as primary evidence.)
    ↓
Chapter 3: Compositional & Chemical Control of Volatile Dynamics (main experimental chapter)
    (Quantitative spine: PEO/LiTr composition grid — the only replicated
     axis (n=2-4) — via the three common measurements; switching window,
     potentiation, and Kohlrausch fading-memory tau (~2-20 s) vary with
     composition. Illustrative tuning landscape: host (PEO/TMPE), anion
     (triflate/TFSI), cation (Li/Na/K), all n<=2 per matched cell.
     Li>Na>K is an honest negative (drive-amplitude + electrode confounds);
     potentiation amplitude sets the apparent tau (methodological result).)
    ↓
Chapter 4: Data-Driven Temporal Computing
    (No new fabrication. Compact behavioural models extracted from the
     three common dynamical measurements of Chapter 3 — I–V hysteresis,
     variable-N potentiation, variable-delay depotentiation — with the
     Chapter 2 SY/Hybrane/LiTf device supplying priors and sanity checks
     (EPSC, STDP, separated STM/LTM, impedance) that are Li-only and
     are never used to justify quantitative Na/K claims. Three application
     schemes simulated from those models: heterogeneous physical
     reservoir computing (flagship), spike coincidence detection, and
     multi-timescale transient filtering. Circuit-level integration
     constraints and design rules.)
    ↓
Chapter 5: Conclusions & Outlook
    (Synthesis across the chemistry axis (Ch. 2–3) and the application
     axis (Ch. 4). Benchmarks drawn from temporal / reservoir / event-driven
     hardware, not from digital memory.)
```

**Key framing decision carried through every chapter:** these devices are not framed as failed non-volatile memories. They are framed as good volatile, heterogeneous, temporally rich elements. **Second key framing rule (v4):** the thesis claims a **replicated, quantitative composition result** (the PEO/LiTr grid) plus an **illustrative chemical-tuning landscape** (host/anion/cation, n-limited); it does *not* claim a **Li>Na>K cation law** (reported as an honest negative, drive-amplitude/electrode-confounded) nor a uniformly measured Li/Na/K synaptic suite. The defensible shared dataset is the three common measurements; EPSC/STDP/separated STM-LTM/impedance remain the Chapter-2 device only. See `handouts/01_thesis_structure.md` (framing table) and `handouts/10_chapter3_comparative_plan.md` (full plan).

---

## 9. Key Publications and Citations (for BibTeX use)

```bibtex
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

## 10. Status of Written Work (as of 2026-04-12)

| Item | Status | Location |
| ------ | -------- | ---------- |
| Memory document (v4) | ✅ Complete | `handouts/00_thesis_overview_memory.md` |
| Thesis structure — 5 chapters (v4) | ✅ Complete | `handouts/01_thesis_structure.md` |
| Introduction chapter plan (v2, with temporal computing sections) | ✅ Complete | `handouts/02_introduction_chapter_plan.md` |
| Chapter 2 figures reference list | ✅ Complete | `handouts/03_chapter2_figures_needed.md` |
| Chapter 2 (LaTeX, full) | ✅ Complete | `chapters/chapter2_proof_of_concept.tex` |
| Chapter 4 planning document | ✅ Complete | `handouts/04_chapter4_temporal_computing_plan.md` |
| Chapter 4 data / pipeline spec | ✅ Complete | `handouts/05_chapter4_data_pipeline.md` |
| Chapter 3 & 4 claims audit (data-driven, §1–§16) | ✅ Complete | `handouts/08_chapter3_4_claims_audit.md` (+ `ch3_*.csv`, `scripts/ch3_4_dynamics_fits.py`) |
| Chapter 3 full plan (v4) + proposal/diff | ✅ Complete | `handouts/10_chapter3_comparative_plan.md`, `handouts/09_chapter3_revised_plan_PROPOSAL.md` |
| References database (`references.bib`, with reservoir-computing core added) | ✅ Complete | `bibliography/references.bib` |
| Chapter 1 (writing) | ⬜ Not started | — |
| Chapter 3 (plan, v4) | ✅ Complete | `handouts/10_chapter3_comparative_plan.md` |
| Chapter 3 (writing) | ⬜ Not started | — |
| Chapter 4 (writing) | ⬜ Not started | — |
| Chapter 5 (writing) | ⬜ Not started | — |
