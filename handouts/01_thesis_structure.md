<!-- markdownlint-disable-file MD013 -->

# Thesis Chapter Structure

**Author:** Carlos David Prado-Socorro  
**Date:** April 12, 2026  
**Revision:** v6 (2026-06-07) — Updated to the current six-chapter thesis map and public export set. Chapter 3 is now the reproducibility/provenance bridge, Chapter 4 is the comparative PEO/triflate study, Chapter 5 is the in-silico temporal-computing chapter, and Chapter 6 is conclusions and outlook. All six chapter `.tex` files and public chapter PDFs exist.

---

## Current 6-Chapter Structure

### Chapter 1 — Introduction

*Full narrative background to justify the research, contextualise the problem, and establish the scientific framework for the thesis. The introduction frames the target device not as a candidate non-volatile memory competing with crossbar ReRAM, but as a volatile, heterogeneous, temporally rich element whose natural place is event-driven and temporal computing.*

Status: Draft available — `chapters/chapter1_introduction.tex`, `exports/chapter1_introduction.pdf`

### Chapter 2 — Proof of Concept: Polymer-Based Composite Organic Memristive Devices

*Expanded PhD-thesis treatment of the published SY/Hybrane/LiCF3SO3 proof-of-concept device. This chapter remains the one fully characterised synaptic exemplar of the thesis, and is the only device on which EPSC, STDP, separated STM/LTM retention, and impedance spectroscopy are used as primary evidence.*

Status: Draft available — `chapters/chapter2_proof_of_concept.tex`, `exports/chapter2_proof_of_concept.pdf`

### Chapter 3 — Reproducibility, Provenance, and the Transition to PEO

*Bridge chapter that diagnoses the failed attempt to scale the original Hybrane line, separates reagent-ageing evidence from finished-device ageing, documents the provenance and normalized-feature methodology, and motivates the transition to the PEO platform.*

Status: Draft available — `chapters/chapter3_bridge.tex`, `exports/chapter3_bridge.pdf`

### Chapter 4 — Compositional and Chemical Control of Volatile Polymer-Electrolyte Memristive Dynamics

*Main comparative experimental chapter. The quantitative spine is the replicated SY/PEO/LiTr composition grid, characterised by the three common dynamical measurements: I–V hysteresis, variable-N potentiation, and variable-delay depotentiation. Composition is the robust control knob; host, anion, and cation chemistry form an illustrative, sample-limited tuning landscape; and the Li>Na>K cation hypothesis is reported as an honest negative under the available evidence.*

Status: Draft available — `chapters/chapter4_comparative.tex`, `exports/chapter4_comparative.pdf`

### Chapter 5 — Data-Driven Temporal Computing with Polymer-Electrolyte Memristor Reservoirs

*Application chapter using compact behavioural models extracted from the Chapter 4 measurements. No new fabrication is claimed. The chapter reports in-silico reservoir demonstrations with MC/NARMA benchmarks, WESAD physiological temporal-context reconstruction, and scoped WESAD affective-classification results read out by linear regression.*

Status: Draft available — `chapters/chapter5_temporal.tex`, `exports/chapter5_temporal.pdf`

### Chapter 6 — Conclusions and Outlook

*Synthesis across the device-chemistry axis (Chapters 2–4) and the application axis (Chapter 5), with limitations and future work stated against the correct benchmark class: temporal, reservoir, and event-driven neuromorphic hardware rather than digital memory.*

Status: Draft available — `chapters/chapter6_conclusions.tex`, `exports/chapter6_conclusions.pdf`

---

## Rationale for This Structure

The six-chapter structure follows the evidence trail more cleanly than the earlier five-chapter plan. Chapter 3 now prevents a reliability gap by making the Hybrane-to-PEO transition explicit instead of hiding it between the proof-of-concept and comparative chapters.

1. **Chapter 1** establishes why volatile organic devices are useful temporal elements rather than failed non-volatile memories.
2. **Chapter 2** presents the peer-reviewed proof of concept on a single, fully characterised SY/Hybrane/LiTf device.
3. **Chapter 3** explains the reproducibility crisis and records the provenance methodology that makes the later archive defensible.
4. **Chapter 4** quantifies how composition tunes the PEO/triflate dynamics while keeping chemistry claims sample-limited.
5. **Chapter 5** tests whether the measured dynamics are computationally useful under a deliberately scoped in-silico reservoir model.
6. **Chapter 6** gathers the contributions, limitations, and next experiments.

The logical arc is:

- **Chapter 2** proves the platform exists on one fully characterised device.
- **Chapter 3** explains why that original material line could not simply be scaled, and what methodology replaced ad hoc interpretation.
- **Chapter 4** quantifies the robust composition dependence and reports the chemistry landscape without overreach.
- **Chapter 5** shows how the measured dynamics can support reservoir-style temporal-computing demonstrations under constrained read-out assumptions.
- **Chapter 6** places the thesis against the correct reference class and defines the hardware work still needed.

---

## Key Framing Decision

**Do not frame these devices as bad non-volatile memories.**  
Frame them as useful volatile, heterogeneous temporal elements.

This decision propagates across all six chapters:

| Chapter | Framing consequence |
| --- | --- |
| Ch. 1 | Introduce event-driven and temporal computing alongside crossbar computing. |
| Ch. 2 | Treat short retention as functional fading memory, not as an apology. |
| Ch. 3 | Make reproducibility, reagent provenance, and the PEO transition visible. |
| Ch. 4 | Lead with the replicated composition grid; present host/anion/cation as n-explicit side evidence. |
| Ch. 5 | Keep application claims in-silico and tied to measured behavioural models plus linear read-out. |
| Ch. 6 | Benchmark against neuromorphic, reservoir, and event-driven hardware, not DRAM/SRAM/ReRAM. |

---

## Target Length (Approximate)

| Chapter | Estimated pages |
| --- | --- |
| Chapter 1 (Introduction) | 45–65 |
| Chapter 2 (Proof of concept — SY/Hybrane/LiTf) | 25–35 |
| Chapter 3 (Reproducibility/provenance bridge) | 12–20 |
| Chapter 4 (PEO–triflate comparative series) | 30–40 |
| Chapter 5 (Data-driven temporal computing) | 30–40 |
| Chapter 6 (Conclusions & outlook) | 12–18 |
| Front matter, bibliography, appendices | 15–25 |
| **Total** | **~170–240 pages** |
