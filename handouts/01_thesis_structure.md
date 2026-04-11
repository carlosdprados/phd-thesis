<!-- markdownlint-disable-file MD013 -->

# Thesis Chapter Structure

**Author:** Carlos David Prado-Socorro  
**Date:** April 11, 2026  
**Revision:** v2 — 5-chapter structure (adds application-level data-driven chapter)

---

## Proposed 5-Chapter Structure

### Chapter 1 — Introduction

*Full narrative background to justify the research, contextualise the problem, and establish the scientific framework for Chapters 2, 3 and 4. Critically, this revised introduction re-frames the target device: not as a candidate non-volatile memory that must compete with crossbar ReRAM, but as a volatile, heterogeneous, temporally rich element whose natural place is in event-driven and temporal computing architectures.*

Scope: ~45–65 pages  
Key topics: von Neumann bottleneck → neuromorphic computing → memristors → organic electronics → polymer composites → ionic memristors → **volatile vs. non-volatile dynamics** → **temporal and event-driven computing paradigms** → thesis objectives.

### Chapter 2 — Proof of Concept: Polymer-Based Composite Organic Memristive Devices

*Based on Paper 1 (Prado-Socorro et al., Adv. Electron. Mater. 2022). Expanded PhD-thesis treatment of the SY/Hybrane/LiCF₃SO₃ composite device fabrication and characterisation.*

Scope: ~25–35 pages  
Key content: Materials design rationale, full fabrication protocol, morphological characterisation (AFM, profilometry), complete electrical characterisation (I–V hysteresis, EPSC, STM/LTM, STDP), ion transport mechanism, device stability, comparison with state of the art.

Status: Written (April 2026) — see `handouts/chapter2_proof_of_concept.tex`

### Chapter 3 — Ion-Dependent Device Physics in Silver-Electrode Devices

*Based on experimental findings from the NM_vXXX Ag-electrode device series employing Li⁺, Na⁺, and K⁺ TFSI salts. Systematic comparison of how cation identity (charge density, Lewis acid strength, ionic radius) determines memristive dynamics. The chapter is framed as a physical-chemistry investigation of the device — not as a performance shoot-out against digital memories.*

Scope: ~30–40 pages  
Key content:

- Motivation for exploring multiple ionic species (beyond Li)
- Comparative synthesis of composite formulations with LiTFSI, NaTFSI, KTFSI
- Device fabrication (optimised Ag-electrode protocol)
- Systematic I–V hysteresis comparison across Li/Na/K
- Comparative EPSC, STM retention, LTM retention, delay-time/STDP response
- Conductance potentiation/depression curves per ionic species
- Effect of ionic radius and charge density on the Lewis acid–base interaction with Hybrane
- Hard–soft acid–base (HSAB) theory applied to the fading-memory hierarchy Li > Na > K
- Impedance spectroscopy analysis of ionic transport
- Thermodynamic vs. kinetic factors in conductance relaxation
- **Explicit reframing:** ion identity is treated as a *timescale-engineering knob*, not as a defect that prevents persistence. Variability (device-to-device and cycle-to-cycle) is characterised quantitatively as a *resource* that Chapter 4 will exploit.

### Chapter 4 — Data-Driven Temporal Computing with Volatile Ion-Mediated Polymeric Memristors

*Translates the experimental datasets of Chapters 2 and 3 into application-level functionality using compact, experimentally grounded behavioural models. Uses only datasets already acquired in the NM_vXXX series — no additional fabrication is required. The chapter argues, and then demonstrates in simulation, that the Li/Na/K device family is naturally suited to heterogeneous physical reservoir computing, spike coincidence detection, and multi-timescale transient filtering.*

Scope: ~35–45 pages  
Key content:

- Re-statement of the design philosophy: volatile, variable, heterogeneous elements as temporal computing primitives, not as flawed non-volatile memories
- Consolidation of experimental datasets from Chapters 2 and 3, with the **common Li/Na/K basis explicitly limited to I–V hysteresis, N-pulse potentiation, and delay-time depotentiation**; EPSC, STDP, separated STM/LTM retention, and impedance are retained as Li-dominant priors / sanity checks where available
- Extraction of a compact behavioural model per ion species (Li, Na, K), with fading-memory time constant, nonlinear pulse update, device-to-device spread, and read transfer function
- **Application I (flagship): heterogeneous physical reservoir computing** for temporal classification — Li as slow, Na as intermediate, K as fast nodes, trained with a linear readout layer
- **Application II: spike coincidence detection and temporal feature extraction**, built primarily on the measured delay-time kernels, with Li-device STDP used as a consistency check where available
- **Application III: multi-timescale transient filter bank**, using Li/Na/K as a three-constant leaky filter bank for onset/edge/burst detection
- Circuit-integration constraints: 1T1M addressing, current compliance, read/write protocols, variability envelopes
- Design rules: where these devices are useful, and — equally important — where they are not

Status: Not started. See companion outline `handouts/04_chapter4_temporal_computing_plan.md`.

### Chapter 5 — Conclusions and Outlook

*Synthesis of contributions, limitations, and forward-looking research directions across the device-chemistry axis (Chapters 2 and 3) and the application-level axis (Chapter 4).*

Scope: ~12–18 pages  
Key content:

- Summary of key scientific contributions in three layers: (i) a reversible 2-T organic memristive platform, (ii) ion-chemistry control of its dynamics, (iii) a demonstration that these dynamics are exploitable as temporal computing primitives
- Benchmarking not against digital memory but against other temporal / reservoir / neuromorphic hardware
- Limitations of the current material system (stability, retention drift, encapsulation, read-disturb under continuous pulsing)
- Future directions:
  1. Chemical tailoring of the ion-transport polymer for finer timescale engineering
  2. Encapsulation strategies for air-stable long-run temporal inference
  3. Integration into 1T1M arrays with on-chip readout electronics
  4. Hardware demonstration of a heterogeneous reservoir using physical Li/Na/K banks
  5. Nervetronic applications (biocompatibility, flexible substrate) leveraging volatile dynamics
  6. Mixed-ion gradient devices as continuously tunable temporal kernels

---

## Rationale for This Structure

The five-chapter structure follows a logical and defensible scientific narrative, and — importantly — corrects a framing error present in the earlier four-chapter plan.

1. **Introduction** establishes why the research matters. The revised version explicitly introduces volatile and event-driven computing as a first-class application target, not as an afterthought to crossbar memories.

2. **Chapter 2** presents the first demonstration of the concept, validated through publication in a peer-reviewed high-impact journal. It establishes all fundamental memristive functionalities in a single, well-characterised device.

3. **Chapter 3** takes the validated concept forward by systematically exploring the chemical parameter space (Li, Na, K), generating new, unpublished knowledge. The chapter is rewritten so that variability and volatility are quantified as *physical properties* rather than as shortcomings.

4. **Chapter 4** converts those physical properties into application-level design rules. It uses only existing datasets plus compact data-driven simulations, which makes it fully achievable without further fabrication. It provides the first credible link from the device chemistry of Chapters 2–3 to circuit-level temporal computing schemes, using reservoir computing as the flagship case.

5. **Chapter 5** synthesises the whole, places it in context, and opens the scientific conversation to the next generation of researchers in the field.

The logical arc is now:

- **Chapter 2** proves the platform exists.
- **Chapter 3** explains why Li, Na and K change its behaviour.
- **Chapter 4** shows how those different behaviours can be *used*.
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
| Ch. 3 | Present Li/Na/K as a *timescale ladder*, not as a retention ranking. Variability → heterogeneity resource. |
| Ch. 4 | Flagship application: heterogeneous physical reservoir computing. Supporting: coincidence detection and transient filter banks. |
| Ch. 5 | Benchmarks drawn from neuromorphic / reservoir / event-driven hardware, not from DRAM/SRAM/ReRAM. |

---

## Target Length (Approximate)

| Chapter | Estimated pages |
| --------- | ---------------- |
| Chapter 1 (Introduction) | 45–65 |
| Chapter 2 (PoC) | 25–35 |
| Chapter 3 (Ion-dependent physics) | 30–40 |
| Chapter 4 (Data-driven temporal computing) | 35–45 |
| Chapter 5 (Conclusions & Outlook) | 12–18 |
| Front matter, bibliography, appendices | 15–25 |
| **Total** | **~160–225 pages** |
