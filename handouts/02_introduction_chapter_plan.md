<!-- markdownlint-disable-file MD013 -->

# Chapter 1 — Introduction: Detailed Outline

**Author:** Carlos David Prado-Socorro  
**Date:** April 11, 2026  
**Revision:** v2 — updated for the 5-chapter thesis structure. The main conceptual change is that the introduction no longer treats "analog, multi-state, reversible, **non-volatile** resistance" as the default target. It explicitly introduces volatile fading-memory devices and event-driven temporal computing as a first-class application domain, laying the groundwork for the new Chapter 4.

---

## Natural Conceptual Flow

The introduction must take any physical chemist or materials scientist — even one unfamiliar with neuromorphic devices — from first principles through to the precise scientific niche this thesis occupies. The flow is:

Computing limits → Brain-inspired solutions → The memristor (static *and* dynamic views) → Inorganic implementations → Why organic → Why polymer composites → Why ionic → Why volatility and variability are resources → This thesis

The revised flow adds two inflection points:

1. After introducing the memristor, the reader is shown that "memristive device" is a broader concept than "non-volatile weight": it also covers volatile, fading-memory, time-varying elements.
2. Before stating the thesis objectives, the reader is shown that a device family with tunable fading memory and controlled heterogeneity is the natural substrate for *temporal* computing paradigms such as physical reservoir computing, coincidence detection, and leaky filtering.

---

## Full Hierarchical Outline

### 1. The Crisis in Modern Computing

#### 1.1 Von Neumann Architecture and Its Limitations

- 1.1.1 The stored-program paradigm: CPU, memory unit, shared data bus
- 1.1.2 The von Neumann bottleneck: memory–CPU bandwidth as the limiting resource
- 1.1.3 Quantitative impact: idle CPU time, energy cost of data movement vs. arithmetic
- 1.1.4 Scaling laws: Moore's Law, Dennard scaling, and their end
- 1.1.5 Consequences for AI workloads: pattern recognition, big data, deep learning

#### 1.2 In-Memory and Event-Driven Computing Paradigms

- 1.2.1 Concept: co-locating processing and storage
- 1.2.2 Near-memory and processing-in-memory (PIM) approaches
- 1.2.3 Analog in-memory computing: vector-matrix multiplication in crossbar arrays
- 1.2.4 Energy efficiency arguments: operations per joule in conventional vs. neuromorphic hardware
- **1.2.5 Temporal in-memory computing and event-driven processing** *(new)* — reservoir computing, liquid state machines, spiking neural networks, physical temporal kernels; the idea that computation can live in the *transients* of a dynamical system rather than in its steady state
- **1.2.6 Why some useful computing elements should forget** *(new)* — fading memory as a resource for causal filtering, for bounding the state space of recurrent systems, and for building leaky integrators. Contrasts the two complementary roles: static weights (learning) vs. dynamic states (temporal representation)

---

### 2. The Biological Synapse as the Engineering Template

#### 2.1 Neural Signal Transmission: A Brief Overview

- 2.1.1 Neuron anatomy: axon, dendrite, soma
- 2.1.2 Action potentials and their propagation
- 2.1.3 The synaptic cleft: pre- and postsynaptic membranes, neurotransmitter release

#### 2.2 Synaptic Plasticity: The Physical Basis of Learning

- 2.2.1 Hebbian learning rule: "Neurons that fire together wire together"
- 2.2.2 Long-term potentiation (LTP) and long-term depression (LTD)
- 2.2.3 Short-term plasticity: facilitation and depression
- 2.2.4 Spike-timing dependent plasticity (STDP): temporal asymmetry of learning
- 2.2.5 Quantitative characteristics: synaptic time constants (τ ≈ 100 ms), power (~20 W for the whole brain)

#### 2.3 Why Hardware Emulation of the Synapse?

- 2.3.1 Limitations of software neural networks running on von Neumann hardware
- 2.3.2 Hardware neural networks (HNNs): direct mapping of weights onto device conductance
- **2.3.3 The requirement for analog, multi-state, reversible resistance** *(revised — "non-volatile" removed from the default list)*. Non-volatility is now discussed as *one* valid target, not *the* target
- **2.3.4 Static weights vs. dynamic fading-memory elements** *(new)* — two complementary computational roles for memristive devices: (i) programmable weights in trained networks; (ii) transient state variables in temporal processing
- **2.3.5 Volatile synapses as leaky integrators and temporal encoders** *(new)* — biological short-term plasticity is itself volatile; many cortical circuits rely on rapid decay for temporal feature extraction. Hardware that forgets is therefore not deficient — it is biologically faithful to a different computational mode

---

### 3. The Memristor: Theory and History

#### 3.1 Theoretical Foundation

- 3.1.1 The four fundamental circuit elements: R, L, C, and the missing element
- 3.1.2 Chua's 1971 prediction: the memristor as the R–q relationship
- 3.1.3 Memristance as a function of charge history: M(q)
- 3.1.4 The memristive system generalisation (Chua & Kang, 1976) — explicitly covers devices whose internal state decays over time, i.e. *volatile* memristive systems

#### 3.2 The First Physical Realisation: TiO₂ Memristor

- 3.2.1 Strukov et al. Nature 2008: HP Labs' TiO₂ device
- 3.2.2 Mechanism: oxygen vacancy migration and filament formation
- 3.2.3 Impact: validation of Chua's theory after 37 years

#### 3.3 Classification of Memristive Mechanisms

- 3.3.1 Filamentary switching (conductive bridges, metallic filaments)
- 3.3.2 Non-filamentary switching (interface-type, homogeneous bulk effects)
- 3.3.3 Phase-change memories (PCM): crystalline–amorphous transition
- 3.3.4 Magnetic tunnel junctions: spin-dependent transport
- 3.3.5 Ionic memristors: displacement of charged species (with explicit mention that ionic devices are intrinsically relaxation-prone and therefore natural fading-memory candidates)

#### 3.4 Key Memristive Parameters

- 3.4.1 High resistance state (HRS) and low resistance state (LRS): ON/OFF ratio
- 3.4.2 Switching voltage: SET and RESET thresholds
- 3.4.3 Retention time: data persistence without applied voltage
- 3.4.4 Endurance: number of switching cycles before degradation
- 3.4.5 Linearity and symmetry: requirements for use in crossbar arrays
- 3.4.6 Stochastic variability: cycle-to-cycle and device-to-device
- **3.4.7 Volatility as a computational parameter** *(new)* — retention time reinterpreted as a *design variable*, not a figure of merit to be maximised. A device with τ ≈ 5 s is not a bad RAM; it is a very well-matched leaky integrator for second-scale temporal signals
- **3.4.8 Variability as heterogeneity rather than only defect** *(new)* — device-to-device spread is a liability for a trained crossbar but an asset for a reservoir: it increases the effective dimensionality of the state space and the richness of the nonlinear projection
- **3.4.9 Memory timescale as a device-design variable** *(new)* — chemistry-level control over retention (e.g. via cation identity) as an engineering knob for matching device dynamics to application-relevant timescales

#### 3.5 Dynamic Computing Paradigms for Volatile Memristors *(new section)*

- **3.5.1 Reservoir computing: nonlinear projection plus fading memory** — a bank of volatile nonlinear nodes projects a temporal input into a high-dimensional state; only a linear readout layer is trained
- **3.5.2 Coincidence detection and temporal correlation extraction** — volatile devices whose state decays between events naturally compute whether two events arrived within a tunable time window
- **3.5.3 Multi-timescale filtering and transient preprocessing** — a heterogeneous set of fading-memory devices acts as a bank of leaky filters with different time constants, performing temporal decomposition at the analog front-end
- **3.5.4 Metrics for temporal computing** — memory capacity, class separability, robustness to variability, energy per event. These replace retention/endurance/ON-OFF ratio as the relevant figures of merit for this chapter's application target

---

### 4. Inorganic Memristors for Neuromorphic Computing

#### 4.1 Metal Oxide Memristors

- 4.1.1 HfO₂, TaO₂, NiO systems: properties and mechanisms
- 4.1.2 Strengths: retention, speed, CMOS compatibility
- 4.1.3 Limitations: stochastic filament formation, low reproducibility, limited multi-state

#### 4.2 Phase-Change Memory (PCM)

- 4.2.1 GST (GeSbTe) alloys: crystallisation kinetics as memory
- 4.2.2 IBM's applications in analogue deep learning (Le Gallo et al. Nat. Electron. 2018)
- 4.2.3 Energy cost: high RESET current requirement

#### 4.3 Spin-Transfer Torque Magnetic Tunnel Junctions (STT-MTJ)

- 4.3.1 Operating principle: parallel vs. antiparallel magnetisation states
- 4.3.2 Neuromorphic demonstrations: pattern recognition (Torrejon et al. Nature 2017)
- 4.3.3 Limitations: CMOS integration complexity, low thermal stability

#### 4.4 General Limitations of Inorganic Memristors

- 4.4.1 Low chemical tunability: fixed material chemistry, limited synthetic freedom
- 4.4.2 Nanostructuration challenges: top-down lithography requirements
- 4.4.3 Biocompatibility: toxic heavy metals, rigid substrates
- 4.4.4 Reproducibility: filament variability as fundamental physical limitation
- 4.4.5 Absence of large-scale commercialisation despite decades of research

---

### 5. Organic Materials for Memristive Applications

#### 5.1 Advantages of Organic Memristors

- 5.1.1 Molecular tunability: synthetic chemistry as the design tool
- 5.1.2 Solution processability: spin-coating, inkjet, roll-to-roll
- 5.1.3 Mechanical flexibility: conformable electronics, wearable devices
- 5.1.4 Biocompatibility: nervetronic applications (Park et al. Adv. Mater. 2020)
- 5.1.5 Low cost: earth-abundant materials, simple fabrication
- 5.1.6 Environmental sustainability ("green electronics")

#### 5.2 Mechanisms in Organic Memristors

- 5.2.1 Charge trapping/detrapping in insulating matrices
- 5.2.2 Redox-active molecules: switching by oxidation state change
- 5.2.3 Conformational changes: bistable molecular switches
- 5.2.4 Ionic redistribution: displacement of mobile charge carriers
- 5.2.5 Filamentary conduction: metallic nanoparticle formation (electromigration)

#### 5.3 Historical Development of Organic Memristors

- 5.3.1 Malliaras et al. (2010): [Ru(bpy)₃]²⁺/PF₆⁻ bistable electrochemical cell — first organic attempt; ionic redistribution; limited reversibility
- 5.3.2 Lei et al. (2014): polyvinyl alcohol thin film; no mechanistic insight
- 5.3.3 3-T organic devices (Gkoupidenis, Xu, Fu, et al.): OECTs as synaptic transistors; long remanence but complex architecture
- 5.3.4 Liu et al. (2016): [EV(ClO₄)]/(BTPA-F) redox 2-T device; first STM→LTM in 2-T organic; limited reversibility due to permanent redox changes
- 5.3.5 Kim et al. (2018): stretchable artificial synapse; mechanical flexibility demonstrated
- 5.3.6 Goswami et al. (2017, 2020): molecular memristors; high precision but complex molecular synthesis
- 5.3.7 State of the field by 2021: no fully reversible, multi-state, 2-T organic device with both STM and LTM coexisting in a single component

---

### 6. Polymer Electrolyte Composites: The Enabling Strategy

#### 6.1 Ion-Conducting Polymers: Principles

- 6.1.1 Polyether hosts: PEO and its derivatives; coordination of alkali cations
- 6.1.2 Ion transport mechanisms: vehicular (ion + solvation shell), Grotthuss (hopping), segmental motion
- 6.1.3 Conductivity–flexibility relationship: glass transition temperature (Tg) effects
- 6.1.4 Hard-soft acid-base (HSAB) theory: predicting cation–polymer binding affinity

#### 6.2 Light-Emitting Electrochemical Cells (LECs) as Precedent

- 6.2.1 LEC operating principle: ionic redistribution to form p-i-n junction in situ
- 6.2.2 Role of the solid electrolyte in LECs
- 6.2.3 Connection to memristive operation: ionic redistribution as the shared mechanism
- 6.2.4 Mardegan et al. (2021): Hybrane DEO750 8500 + Super Yellow in LEC; long operational lifetime validates material stability

#### 6.3 Rationale for the Composite Approach

- 6.3.1 Decoupling electronic and ionic functions: semiconductor + ion-transport polymer
- 6.3.2 Salt selection: high charge asymmetry between anion and cation → two mobility regimes → two memory timescales
- 6.3.3 One-step fabrication: blend processing from single solution
- 6.3.4 Design freedom: tunable concentration, cation identity, polymer backbone
- **6.3.5 Ion identity as built-in timescale engineering** *(new)* — Li, Na and K select, by their Lewis acidity and hydrodynamic radius, the effective fading-memory constant of the device. This is the *chemical* origin of a *computational* design knob
- **6.3.6 Mixed populations of devices as a temporal kernel bank** *(new)* — a small number of chemically distinct compositions, deliberately combined on a single chip, define a bank of temporal kernels with a spread of time constants. The heterogeneity that would be harmful for a trained crossbar becomes the *point* of the design for temporal computing

---

### 7. Scope and Objectives of This Thesis

#### 7.1 Open Scientific Questions

- Can a fully reversible 2-T organic memristive device be fabricated from a solution-processable polymer composite?
- Can such a device exhibit both STM and LTM simultaneously in a single component?
- What is the physicochemical origin of the memory regimes?
- How does the identity of the mobile ion (Li⁺, Na⁺, K⁺) quantitatively affect the memristive parameters?
- **Can volatile organic memristors be exploited as temporal computing primitives rather than static memories?** *(new)*
- **Can ion identity be used as a design knob for application-level timescale matching?** *(new)*
- **Can measured variability improve computational richness in heterogeneous networks rather than degrade it?** *(new)*

#### 7.2 Thesis Objectives

1. Design, fabricate, and characterise a proof-of-concept 2-T organic memristive device based on a SY/Hybrane/LiTf composite (Chapter 2)
2. Demonstrate full synaptic functionality: analog switching, EPSC, STM, LTM, and STDP in a single device (Chapter 2)
3. Provide a mechanistic explanation of memory regimes in terms of ionic migration and Lewis acid–base chemistry (Chapter 2)
4. Systematically investigate the effect of cation identity (Li⁺, Na⁺, K⁺) on memristive parameters in Ag-electrode devices (Chapter 3)
5. Establish structure–property relationships linking ionic chemistry to device dynamics (Chapter 3)
6. **Build compact data-driven models from the experimental I–V, pulse, retention, and delay-time datasets of Chapters 2 and 3** *(new — Chapter 4)*
7. **Demonstrate application-level temporal computing schemes — heterogeneous reservoir computing, spike coincidence detection, and multi-timescale transient filtering — using Li-, Na-, and K-mediated memristive devices without further fabrication** *(new — Chapter 4)*

#### 7.3 Thesis Outline

Brief paragraph-level description of what each of the five chapters covers and how they connect. Emphasise that Chapters 2 and 3 are experimental and Chapter 4 is data-driven/simulation; Chapter 5 is synthesis.

---

## Pedagogical Notes for Writing

- The introduction should move from **broad (computing crisis)** to **narrow (this specific composite, used this specific way)** — a "funnel" structure standard in materials science theses.
- Each section transition should be a logical step, not a jump: the reader should feel they could have predicted the next section before reading it.
- The revised structure has two funnels in parallel: a *materials* funnel (device chemistry) and an *applications* funnel (temporal computing). They converge at §7 into a unified thesis objective list.
- Every major claim about limitations of prior art should be substantiated with specific citations.
- Figures to include: von Neumann architecture diagram; neuron/synapse schematic; memristor circuit symbol and characteristic I–V pinched hysteresis loop; timeline of organic memristor development; HSAB periodic table excerpt; device schematic for this thesis; **a "static weight vs. fading-memory" conceptual schematic contrasting a trained crossbar with a reservoir**; **a "timescale ladder" schematic showing Li/Na/K mapped onto slow/medium/fast fading-memory nodes**.
- Keep the tone definitive and active: "we demonstrate", "the results show", "this establishes" — not "it seems", "might be", "could potentially".
- The "why some useful computing elements should forget" subsection (§1.2.6) is load-bearing: it is the first place where the reader is given permission to stop treating volatility as a defect. Write it carefully.
