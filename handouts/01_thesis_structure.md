<!-- markdownlint-disable-file MD013 -->

# Thesis Chapter Structure

**Author:** Carlos David Prado-Socorro  
**Date:** April 12, 2026  
**Revision:** v3 — Chapter 3 and Chapter 4 re-scoped to match the real experimental archive. The main comparative corpus is PEO + triflate (LiTr, NaTr, KTr) composites at PEO = 0.3 and salt = 0.09 mass fractions, with a PEO/LiTr concentration series as a systematic sub-study. TMPE- and alkali-TFSI-based formulations are treated only as exploratory side evidence. The common comparative measurements are restricted to I–V hysteresis, variable-N potentiation, and variable-delay depotentiation; EPSC, STDP, separated STM/LTM and impedance remain Chapter 2 results only. v2 (2026-04-11) introduced the 5-chapter structure and the temporal-computing framing.

---

## Proposed 5-Chapter Structure

### Chapter 1 — Introduction

*Full narrative background to justify the research, contextualise the problem, and establish the scientific framework for Chapters 2, 3 and 4. Critically, this revised introduction re-frames the target device: not as a candidate non-volatile memory that must compete with crossbar ReRAM, but as a volatile, heterogeneous, temporally rich element whose natural place is in event-driven and temporal computing architectures.*

Scope: ~45–65 pages  
Key topics: von Neumann bottleneck → neuromorphic computing → memristors → organic electronics → polymer composites → ionic memristors → **volatile vs. non-volatile dynamics** → **temporal and event-driven computing paradigms** → thesis objectives.

### Chapter 2 — Proof of Concept: Polymer-Based Composite Organic Memristive Devices

*Based on Paper 1 (Prado-Socorro et al., Adv. Electron. Mater. 2022). Expanded PhD-thesis treatment of the SY/Hybrane/LiCF₃SO₃ composite device fabrication and characterisation. This chapter remains the one fully characterised synaptic exemplar of the thesis, and is the only device on which EPSC, STDP, separated STM/LTM retention, and impedance spectroscopy are used as primary evidence.*

Scope: ~25–35 pages  
Key content: Materials design rationale, full fabrication protocol, morphological characterisation (AFM, profilometry), complete electrical characterisation (I–V hysteresis, potentiation/depression, EPSC, separated STM/LTM, STDP, impedance), ion transport mechanism, device stability, comparison with state of the art.

Status: Written (April 2026) — see `chapters/chapter2_proof_of_concept.tex`

### Chapter 3 — PEO–Triflate Polymer-Electrolyte Memristive Devices: Composition and Ion-Identity Dependence

*The main comparative experimental chapter of the thesis. It is built on the abundant dataset that actually exists for multiple devices: PEO-based polymer-electrolyte composites loaded with alkali-metal triflate salts, characterised across a common set of three dynamical measurements. The chapter is framed as a physical-chemistry investigation of composition- and ion-driven dynamics, not as a performance shoot-out against digital memories.*

Scope: ~30–40 pages  
Key content:

- Motivation for moving from the Chapter 2 SY/Hybrane/LiTf exemplar to a broader polymer-electrolyte platform, and for focusing on triflate salts in PEO as the hosts where the comparative dataset is most abundant
- Composite preparation, processing, and device fabrication under a common protocol
- **Core study — PEO/LiTr concentration series.** Systematic variation of PEO and LiTr mass fractions around the reference composition (PEO = 0.3, salt = 0.09). Common characterisation: (i) I–V hysteresis, (ii) variable-number-of-pulses potentiation, and (iii) variable-delay-time depotentiation. These three datasets define the shared comparative basis for the rest of the chapter and for Chapter 4.
- **Secondary study — PEO/LiTr, PEO/NaTr, PEO/KTr at fixed composition (0.3 / 0.09).** Cross-cation comparison on the same three common measurements, read as a cation-identity sweep at fixed host chemistry and fixed mass fractions. The ion hierarchy Li > Na > K is discussed as an expected fading-memory timescale ordering, to be confirmed or corrected by the delay-time fits — never imposed.
- **Exploratory side evidence.** A clearly delimited section reports a small number of TMPE-based composites and alkali-TFSI (LiBis / NaBis / KBis) devices. These are presented honestly as sparse, not as part of the main corpus, and are used only to motivate future work or to cross-check specific trends.
- HSAB interpretation of the cation–oxygen binding strength, kept as a chemical framing rather than as a quantitative claim that requires EPSC / STDP / impedance data across Li/Na/K.
- Device-to-device and cycle-to-cycle variability quantified directly from replicates within the three common datasets, not from any separate measurement type.
- **What this chapter does *not* claim.** It does not present EPSC, STDP, separated STM/LTM retention, or impedance spectroscopy as common comparative measurements across PEO/LiTr, PEO/NaTr and PEO/KTr. Any reference to those measurements points back to the Chapter 2 device and is explicitly labelled as prior / sanity-check evidence.
- **Explicit reframing:** ion identity and composition are treated as *timescale-engineering knobs*, not as defects that prevent persistence. Variability (device-to-device and cycle-to-cycle) is characterised quantitatively as a *resource* that Chapter 4 will exploit.

### Chapter 4 — Data-Driven Temporal Computing with Volatile Polymer-Electrolyte Memristors

*Translates the experimental datasets of Chapters 2 and 3 into application-level functionality using compact, experimentally grounded behavioural models. Uses only datasets already acquired — no additional fabrication is required. The chapter argues, and then demonstrates in simulation, that the PEO/triflate device family is naturally suited to heterogeneous physical reservoir computing, spike coincidence detection, and multi-timescale transient filtering.*

Scope: ~35–45 pages  
Key content:

- Re-statement of the design philosophy: volatile, variable, heterogeneous elements as temporal computing primitives, not as flawed non-volatile memories
- Consolidation of the experimental evidence base, with the **common comparative basis explicitly restricted to the three abundant dynamical measurements from Chapter 3: I–V hysteresis, variable-N potentiation, and variable-delay depotentiation on the PEO/LiTr concentration series and the PEO/LiTr, PEO/NaTr, PEO/KTr fixed-composition set**; the Chapter 2 SY/Hybrane/LiTf device (EPSC, STDP, separated STM/LTM, impedance) is used only as a prior and sanity-check source, and its richer metrics are never propagated to Na or K claims
- Extraction of a compact behavioural model per composition and per cation, with fading-memory time constant, nonlinear pulse update, device-to-device spread, and read transfer function, all fit from the three common datasets
- **Application I (flagship): heterogeneous physical reservoir computing** for temporal classification — the composition- and cation-driven timescale spread of the PEO/triflate family provides parallel fading-memory nodes for a linear readout layer
- **Application II: spike coincidence detection and temporal feature extraction**, built directly on the measured variable-delay depotentiation kernels of the PEO/triflate corpus. The Chapter 2 STDP kernel is used only as a Li-specific consistency check, never as the primary input for Na/K claims
- **Application III: multi-timescale transient filter bank**, using devices with distinct fitted time constants as a leaky filter bank for onset/edge/burst detection
- Circuit-integration constraints: 1T1M addressing, current compliance, read/write protocols, variability envelopes
- Design rules: where these devices are useful, and — equally important — where they are not

Status: Not started. See companion outline `handouts/04_chapter4_temporal_computing_plan.md`.

### Chapter 5 — Conclusions and Outlook

*Synthesis of contributions, limitations, and forward-looking research directions across the device-chemistry axis (Chapters 2 and 3) and the application-level axis (Chapter 4).*

Scope: ~12–18 pages  
Key content:

- Summary of key scientific contributions in three layers: (i) a reversible 2-T organic memristive platform demonstrated in a single fully characterised device (Chapter 2), (ii) composition- and ion-chemistry control of its dynamics established on the PEO/triflate comparative corpus through the three common dynamical measurements (Chapter 3), (iii) a demonstration that those dynamics are exploitable as temporal computing primitives (Chapter 4)
- Benchmarking not against digital memory but against other temporal / reservoir / neuromorphic hardware
- Limitations of the current evidence base, stated plainly: the richer synaptic metrics (EPSC, STDP, separated STM/LTM, impedance) remain Chapter-2-device-only; the comparative corpus is anchored in the three common dynamical measurements; alkali-TFSI and TMPE-based devices are exploratory and deserve a dedicated follow-up
- Limitations of the current material system (stability, retention drift, encapsulation, read-disturb under continuous pulsing)
- Future directions:
  1. Chemical tailoring of the polyether host and the salt for finer timescale engineering
  2. Encapsulation strategies for air-stable long-run temporal inference
  3. Integration into 1T1M arrays with on-chip readout electronics
  4. Hardware demonstration of a heterogeneous reservoir using composition- and cation-diverse PEO/triflate banks
  5. Nervetronic applications (biocompatibility, flexible substrate) leveraging volatile dynamics
  6. Deeper synaptic characterisation (EPSC, STDP, impedance) of the PEO/triflate family to lift those measurements from Chapter-2-only evidence to full comparative status

---

## Rationale for This Structure

The five-chapter structure follows a logical and defensible scientific narrative, and — importantly — corrects a framing error present in the earlier four-chapter plan.

1. **Introduction** establishes why the research matters. The revised version explicitly introduces volatile and event-driven computing as a first-class application target, not as an afterthought to crossbar memories.

2. **Chapter 2** presents the first demonstration of the concept, validated through publication in a peer-reviewed high-impact journal. It establishes all fundamental memristive functionalities in a single, well-characterised device.

3. **Chapter 3** takes the validated concept forward by systematically exploring the *real* comparative corpus that exists in quantity: PEO/triflate polymer-electrolyte composites. The core is a PEO/LiTr concentration series; the secondary study is a PEO/LiTr, PEO/NaTr, PEO/KTr comparative set at fixed mass fractions; exploratory systems (TMPE, alkali-TFSI) are retained only as side evidence and clearly labelled as such. The chapter is anchored in the three common dynamical measurements — I–V hysteresis, variable-N potentiation, and variable-delay depotentiation — and does not overreach into EPSC / STDP / impedance claims for devices where those measurements do not exist.

4. **Chapter 4** converts those physical properties into application-level design rules. It uses only existing datasets plus compact data-driven simulations, which makes it fully achievable without further fabrication. It provides the first credible link from the device chemistry of Chapters 2–3 to circuit-level temporal computing schemes, using reservoir computing as the flagship case. Every quantitative application-level claim traces back to the three common dynamical measurements of Chapter 3; the Chapter 2 Paper 1 device provides priors and sanity checks only.

5. **Chapter 5** synthesises the whole, places it in context, and opens the scientific conversation to the next generation of researchers in the field.

The logical arc is now:

- **Chapter 2** proves the platform exists on a single, fully characterised SY/Hybrane/LiTf device.
- **Chapter 3** quantifies how composition (PEO/LiTr concentration series) and cation identity (PEO/LiTr, PEO/NaTr, PEO/KTr at fixed mass fractions) change its dynamical behaviour, through the three common measurements that are abundant across the corpus.
- **Chapter 4** shows how those different dynamical behaviours can be *used* for temporal computing.
- **Chapter 5** generalises and looks forward.

This structure satisfies the requirements of a monograph-style PhD thesis: coherent, sequential, and building cumulatively toward a defensible original contribution that is no longer vulnerable to the standard objection *"your device is not a good non-volatile memory"*.

---

## Key Framing Decision

**Do not frame these devices as bad non-volatile memories.**  
Frame them as good volatile, heterogeneous temporal elements.

This single decision propagates across all five chapters:

| Chapter | Framing consequence |
| --------- | -------------------- |
| Ch. 1 | Introduce event-driven / temporal computing alongside crossbar computing. Add a subsection on "why some useful computing elements should forget". |
| Ch. 2 | No change in content, but language around STM / LTM avoids apologising for short retention — retention is a feature, not a defect. |
| Ch. 3 | Present the PEO/triflate concentration and cation sweeps as *timescale-engineering knobs*, not as retention rankings. Variability → heterogeneity resource. Exploratory TMPE / alkali-TFSI data is kept strictly delimited. |
| Ch. 4 | Flagship application: heterogeneous physical reservoir computing, grounded in the three common dynamical measurements. Supporting: coincidence detection and transient filter banks. |
| Ch. 5 | Benchmarks drawn from neuromorphic / reservoir / event-driven hardware, not from DRAM/SRAM/ReRAM. |

---

## Target Length (Approximate)

| Chapter | Estimated pages |
| --------- | ---------------- |
| Chapter 1 (Introduction) | 45–65 |
| Chapter 2 (Proof of concept — SY/Hybrane/LiTf) | 25–35 |
| Chapter 3 (PEO–triflate comparative series) | 30–40 |
| Chapter 4 (Data-driven temporal computing) | 35–45 |
| Chapter 5 (Conclusions & Outlook) | 12–18 |
| Front matter, bibliography, appendices | 15–25 |
| **Total** | **~160–225 pages** |
