<!-- markdownlint-disable-file MD013 -->

# Chapter 1 — Introduction: Detailed Outline

**Author:** Carlos David Prado-Socorro  
**Date:** April 12, 2026  
**Revision:** v4 status overlay — current-source warnings added on 2026-06-04. v3 updated the thesis-wide chemistry framing: the chapter introduces volatile fading-memory devices and event-driven temporal computing as a first-class application domain, while the forward references to Chapters 3 and 4 point at the actual experimental corpus: a PEO-based triflate comparative series (PEO/LiTr, PEO/NaTr, PEO/KTr at mass fractions 0.3 / 0.09, plus a PEO/LiTr concentration sub-study) characterised through three common dynamical measurements — I–V hysteresis, variable-N potentiation, and variable-delay depotentiation. The Chapter 2 SY/Hybrane/LiTf device remains the only fully characterised synaptic exemplar. TMPE-based and alkali-TFSI composites are treated as exploratory side evidence. v2 (2026-04-11) introduced volatile / temporal-computing framing and added §1.2.5, §1.2.6, §3.5, §6.3.5, §6.3.6.

**Current status (2026-06-04):** Historical planning document. Chapter 1 is now drafted in `chapters/chapter1_introduction.tex` with figures inserted. Use this handout only for original outline intent; do not copy the objective list or Chapter-4 application bullets below without applying the status notes. For current Chapter 4 framing, use `handouts/12_chapter4_demonstration_plan_v4.md`: MC/NARMA reservoir benchmarks plus WESAD demonstrations. Coincidence detection is cut from the main chapter, and standalone filter-bank language is folded into the heterogeneous-reservoir framing.

---

## Natural Conceptual Flow

The introduction must take any physical chemist or materials scientist — even one unfamiliar with neuromorphic devices — from first principles through to the precise scientific niche this thesis occupies. The flow is:

Computing limits → Brain-inspired solutions → The memristor (static *and* dynamic views) → Inorganic implementations → Why organic → Why polymer composites → Why ionic → Why volatility and variability are resources → This thesis

The revised flow adds two inflection points:

1. After introducing the memristor, the reader is shown that "memristive device" is a broader concept than "non-volatile weight": it also covers volatile, fading-memory, time-varying elements.
2. Before stating the thesis objectives, the reader is shown that a device family with tunable fading memory and controlled heterogeneity is the natural substrate for *temporal* computing, with physical reservoir computing as the active Chapter-4 route. Coincidence detection and leaky filtering remain useful introductory paradigms, but they are not co-equal Chapter-4 demonstrations in the current thesis plan.

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
- **3.4.9 Memory timescale as a device-design variable** *(updated status)* — composition is the demonstrated quantitative knob for matching device dynamics to application-relevant timescales; cation identity remains a chemical hypothesis tested in Chapter 3, not an assumed universal ordering.

#### 3.5 Dynamic Computing Paradigms for Volatile Memristors *(new section)*

- **3.5.1 Reservoir computing: nonlinear projection plus fading memory** — a bank of volatile nonlinear nodes projects a temporal input into a high-dimensional state; only a linear readout layer is trained
- **3.5.2 Coincidence detection and temporal correlation extraction** — background paradigm: volatile devices whose state decays between events naturally compute whether two events arrived within a tunable time window. This is no longer a main Chapter-4 demonstration.
- **3.5.3 Multi-timescale filtering and transient preprocessing** — background paradigm folded into the current reservoir framing: a heterogeneous set of fading-memory devices acts as a bank of leaky filters with different time constants, performing temporal decomposition at the analog front-end.
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

- 6.1.1 Polyether hosts: PEO and its derivatives (including hyperbranched polyester-amides such as Hybrane); coordination of alkali cations
- 6.1.2 Ion transport mechanisms: vehicular (ion + solvation shell), Grotthuss (hopping), segmental motion
- 6.1.3 Conductivity–flexibility relationship: glass transition temperature (Tg) effects
- 6.1.4 Hard-soft acid-base (HSAB) theory: predicting cation–polymer binding affinity
- 6.1.5 Composition knobs: polymer-to-semiconductor mass ratio and salt-to-semiconductor mass ratio as independent levers on the ionic dynamics of a composite

#### 6.2 Light-Emitting Electrochemical Cells (LECs) as Precedent

- 6.2.1 LEC operating principle: ionic redistribution to form p-i-n junction in situ
- 6.2.2 Role of the solid electrolyte in LECs
- 6.2.3 Connection to memristive operation: ionic redistribution as the shared mechanism
- 6.2.4 Mardegan et al. (2021): Hybrane DEO750 8500 + Super Yellow in LEC; long operational lifetime validates material stability

#### 6.3 Rationale for the Composite Approach

- 6.3.1 Decoupling electronic and ionic functions: semiconductor + ion-transport polymer
- 6.3.2 Salt selection: high charge asymmetry between anion and cation → two mobility regimes → two memory timescales (demonstrated on the Chapter 2 SY/Hybrane/LiTf exemplar)
- 6.3.3 One-step fabrication: blend processing from single solution
- 6.3.4 Design freedom: tunable concentration, cation identity, polymer backbone
- **6.3.5 Composition and chemistry as timescale knobs** — polymer and salt mass fractions provide the demonstrated quantitative control over the effective fading-memory constant. Cation identity is tested as a chemically motivated hypothesis, but Chapter 3 shows that any cation ordering is contingent on the rest of the chemistry rather than a robust host/anion-independent design rule.
- **6.3.6 Mixed populations of devices as a temporal kernel bank** — a small number of composition-distinct devices, deliberately combined on a single chip or in simulation, define a bank of temporal kernels with a spread of time constants. The heterogeneity that would be harmful for a trained crossbar becomes the *point* of the design for reservoir computing, and it is the principle that Chapter 4 exploits using the dynamical dataset of the PEO/triflate corpus.

---

### 7. Scope and Objectives of This Thesis

#### 7.1 Open Scientific Questions

- Can a fully reversible 2-T organic memristive device be fabricated from a solution-processable polymer composite?
- Can such a device exhibit both STM and LTM simultaneously in a single component?
- What is the physicochemical origin of the memory regimes?
- How do polymer-to-semiconductor and salt-to-semiconductor mass fractions, within a common polyether host, affect the dynamical response of the device?
- Does the identity of the mobile cation (Li⁺, Na⁺, K⁺), at fixed host chemistry and fixed mass fractions, produce a robust fading-memory ordering, or is any trend contingent on anion, host, and device variability?
- **Can volatile organic memristors be exploited as temporal computing primitives rather than static memories?**
- **Can composition, and more cautiously chemistry, be used as design knobs for application-level timescale matching?**
- **Can measured variability improve computational richness in heterogeneous networks rather than degrade it?**

#### 7.2 Thesis Objectives

1. Design, fabricate, and characterise a proof-of-concept 2-T organic memristive device based on a SY/Hybrane/LiTf composite (Chapter 2)
2. Demonstrate full synaptic functionality — analog switching, EPSC, separated STM/LTM, STDP, and impedance response — in that single exemplar device (Chapter 2)
3. Provide a mechanistic explanation of memory regimes in terms of ionic migration and Lewis acid–base chemistry (Chapter 2)
4. Build a PEO/triflate polymer-electrolyte comparative corpus and characterise it through three common dynamical measurements: I–V hysteresis, variable-N potentiation, and variable-delay depotentiation (Chapter 3)
5. Using that common dataset, quantify (a) the composition dependence of the dynamics in a PEO/LiTr concentration series and (b) whether cation identity in a PEO/LiTr, PEO/NaTr, PEO/KTr set at fixed PEO and salt mass fractions of 0.3 and 0.09 produces a robust trend. The current Chapter 3 answer is composition yes, cation no as a host/anion-independent rule (Chapter 3)
6. Treat TMPE-based and alkali-TFSI (LiBis/NaBis/KBis) composites transparently as exploratory side evidence with a clearly limited dataset, not as parallel main platforms (Chapter 3)
7. **Build compact data-driven models from the three common dynamical measurements of the Chapter 3 corpus, using the Chapter 2 Paper 1 device only as a source of priors and sanity checks (EPSC, STDP, separated STM/LTM, impedance)** — Chapter 4
8. **Demonstrate application-level temporal computing from those models without further fabrication, using heterogeneous reservoir computing as the main route: MC/NARMA benchmarks plus WESAD affective-computing demonstrations** — Chapter 4

#### 7.3 Thesis Outline

Brief paragraph-level description of what each of the five chapters covers and how they connect. Emphasise that Chapter 2 is a single-device proof of concept with the richest synaptic dataset of the thesis; Chapter 3 is the main multi-device comparative experimental chapter, built on the three common dynamical measurements of the PEO/triflate corpus; Chapter 4 is data-driven and builds compact models and reservoir-computing demonstrations from those same three measurements, with Chapter 2 supplying priors; Chapter 5 is synthesis.

---

## Pedagogical Notes for Writing

- The introduction should move from **broad (computing crisis)** to **narrow (this specific composite, used this specific way)** — a "funnel" structure standard in materials science theses.
- Each section transition should be a logical step, not a jump: the reader should feel they could have predicted the next section before reading it.
- The revised structure has two funnels in parallel: a *materials* funnel (device chemistry) and an *applications* funnel (temporal computing). They converge at §7 into a unified thesis objective list.
- Every major claim about limitations of prior art should be substantiated with specific citations.
- Figures included in the drafted Chapter 1: von Neumann architecture diagram; neuron/synapse schematic; memristor theory and mechanism figures; organic-memristor timeline; polymer-electrolyte chemistry; LEC models; composite architecture/timescale ladder; and the static-weight vs fading-memory contrast. The timescale-ladder framing should now be read as composition-led, with cation ordering treated as a tested hypothesis rather than an assumed result.
- Keep the tone active where the data support it: "we demonstrate" and "the results show" for established claims, and explicit limitation language for sample-limited chemistry comparisons and Chapter-4 WESAD heterogeneity results.
- The "why some useful computing elements should forget" subsection (§1.2.6) is load-bearing: it is the first place where the reader is given permission to stop treating volatility as a defect. Write it carefully.
