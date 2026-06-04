<!-- markdownlint-disable-file MD013 -->

# Thesis Chapter Structure

**Author:** Carlos David Prado-Socorro  
**Date:** April 12, 2026  
**Revision:** v5 (2026-06-04) — Status and Chapter-4 application structure updated to match the current repo. Chapter 1 and Chapter 3 are now drafted in LaTeX. The active Chapter-4 source of truth is `12_chapter4_demonstration_plan_v4.md`: two-tier reservoir computing for affective computing, with MC/NARMA benchmarks and WESAD demonstrations. Coincidence detection is cut from the main chapter, and the standalone filter-bank idea is folded into the heterogeneous-reservoir framing. Previous v4 (2026-06-03) re-scoped Chapter 3 after direct, QA'd archive analysis: composition (PEO/LiTr) is the quantitative spine; host/anion/cation are illustrative; Li>Na>K is an honest negative; and drive amplitude co-sets the apparent fading-memory time.

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

### Chapter 3 — Compositional and Chemical Control of Volatile Polymer-Electrolyte Memristive Dynamics

*The main comparative experimental chapter. Built on the dataset that actually **replicates**: SY/PEO/LiTr composites across a composition grid, characterised by the three common dynamical measurements. **Composition is the quantitative spine; electrolyte chemistry (host, anion, cation) is an illustrative tuning landscape; and the drive protocol is shown to set the apparent timescale.** Framed as a physical-chemistry study of volatile dynamics, not a memory shoot-out. Full plan: `10_chapter3_comparative_plan.md`; evidence: `08_chapter3_4_claims_audit.md`.*

Scope: ~30–40 pages  
Key content:

- Motivation: from the single Ch2 SY/Hybrane/LiTf exemplar to a polymer-electrolyte platform; introduce the three common measurements and the explicit claim discipline (quantitative vs illustrative).
- Fabrication under a **reported, matched protocol** (SY / PEO or TMPE / Li–Na–K triflate or TFSI; Ag electrode; 30 pulses, 4 V write / 2 V read).
- **Quantitative spine — composition (PEO/LiTr, Ag).** Replicated 3×3 grid (PEO {0.3,0.6,1.2} × salt {0.045,0.09,0.18}, n=2–4/cell): switching window and potentiation strength fall as PEO rises; **fading-memory τ tunable ≈ 2–20 s** (Kohlrausch τ, β≈0.6–0.9); device-to-device heterogeneity quantified as a *resource*.
- **Chemical-tuning landscape (illustrative, n-explicit).** Host (PEO vs TMPE, ~6× at Li-triflate), anion (triflate vs TFSI, ~20× in PEO), cation (Li/Na/K). Cleanest cation comparison (TMPE/TFSI, n=2): **K shortest < Li≈Na**, caveated as non-generalising. **No robust Li>Na>K.** HSAB kept as qualitative framing only.
- **Methodological result — the drive protocol sets the timescale.** Potentiation amplitude inflates apparent τ (same device, 4.6→15.5 s at 3→6 V write); cross-device τ comparison requires matched protocol + electrode + composition.
- **What this chapter does *not* claim.** No Li>Na>K law; no EPSC/STDP/separated STM-LTM/impedance across cations (Chapter-2-only, labelled as prior/sanity-check); host/anion/cation are illustrative (n≤2), not powered.
- **Reframing:** composition and chemistry as *timescale-engineering knobs*; variability (device-to-device, cycle-to-cycle) as a *resource* that Chapter 4 exploits.

### Chapter 4 — Data-Driven Temporal Computing with Volatile Polymer-Electrolyte Memristors

*Translates the experimental datasets of Chapters 2 and 3 into application-level functionality using compact, experimentally grounded behavioural models. Uses only datasets already acquired — no additional fabrication is required. The active plan is not the old three-application structure; it is a focused reservoir-computing chapter with architecture-level benchmarks and WESAD affective-computing demonstrations.*

Scope: ~35–45 pages  
Key content:

- Re-statement of the design philosophy: volatile, variable, heterogeneous elements as temporal computing primitives, not as flawed non-volatile memories.
- Consolidation of the evidence base, with the **common comparative basis restricted to the three abundant dynamical measurements from Chapter 3**: I–V hysteresis, variable-N potentiation, and variable-delay depotentiation. Chapter 2 EPSC/STDP/separated STM-LTM/impedance remain Li-only priors and sanity checks.
- Extraction of compact behavioural models from the current tables and scripts: `handouts/ch3_decay_by_cell.csv`, `handouts/ch3_pulses_by_cell.csv`, `handouts/ch4_decay_fits.csv`, `handouts/ch4_pulse_descriptors.csv`, `scripts/ch4_model.py`.
- **Architecture benchmarks:** memory-capacity and NARMA-style tests from `scripts/ch4_reservoir.py` / `scripts/ch4_figures.py`, where heterogeneous composition banks broaden memory capacity relative to homogeneous banks.
- **Affective-computing demonstrations:** WESAD simulations from `scripts/ch4_wesad.py`. Current result: the device reservoir performs real affective computing and fading memory helps modestly, but heterogeneity is not separable from a homogeneous control on WESAD; this negative result is reported honestly.
- Circuit-integration constraints and design rules from the still-valid parts of handout 04 (§4.7–§4.8).
- **Cut from the main plan:** spike coincidence detection. **Folded into the reservoir plan:** standalone multi-timescale filter bank.

Status: modelling and figures in progress; no Chapter-4 LaTeX draft yet. Active companion outline: `handouts/12_chapter4_demonstration_plan_v4.md`. Older `handouts/04_chapter4_temporal_computing_plan.md` is only valid for modelling backbone, circuit integration, and design rules.

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
  4. Hardware demonstration of a task-matched reservoir using composition-diverse PEO/triflate banks
  5. Nervetronic applications (biocompatibility, flexible substrate) leveraging volatile dynamics
  6. Deeper synaptic characterisation (EPSC, STDP, impedance) of the PEO/triflate family to lift those measurements from Chapter-2-only evidence to full comparative status

---

## Rationale for This Structure

The five-chapter structure follows a logical and defensible scientific narrative, and — importantly — corrects a framing error present in the earlier four-chapter plan.

1. **Introduction** establishes why the research matters. The revised version explicitly introduces volatile and event-driven computing as a first-class application target, not as an afterthought to crossbar memories.

2. **Chapter 2** presents the first demonstration of the concept, validated through publication in a peer-reviewed high-impact journal. It establishes all fundamental memristive functionalities in a single, well-characterised device.

3. **Chapter 3** takes the validated concept to a polymer-electrolyte platform. Its **quantitative spine is the PEO/LiTr composition grid** — the only axis that replicates (n=2–4 across a 3×3 grid). Electrolyte **chemistry — host (PEO/TMPE), anion (triflate/TFSI), cation (Li/Na/K) — is an illustrative, sample-limited tuning landscape** (n≤2 per matched cell), with the **Li>Na>K hypothesis reported as an honest negative** (confounded by drive-protocol amplitude and electrode). A **methodological result** shows that potentiation amplitude sets the apparent fading-memory timescale. Anchored in the three common dynamical measurements; no overreach into EPSC / STDP / impedance.

4. **Chapter 4** converts those physical properties into application-level design rules. It uses only existing datasets plus compact data-driven simulations, which makes it fully achievable without further fabrication. It provides the link from the device chemistry of Chapters 2–3 to circuit-level temporal computing through reservoir computing: MC/NARMA benchmarks establish the architecture-level heterogeneity benefit, while WESAD tests whether that benefit translates to a real slow physiological task. Every quantitative application-level claim traces back to the three common dynamical measurements of Chapter 3; the Chapter 2 Paper 1 device provides priors and sanity checks only.

5. **Chapter 5** synthesises the whole, places it in context, and opens the scientific conversation to the next generation of researchers in the field.

The logical arc is now:

- **Chapter 2** proves the platform exists on a single, fully characterised SY/Hybrane/LiTf device.
- **Chapter 3** quantifies how **composition** (the PEO/LiTr grid — the replicated result) tunes the dynamics, and surveys how electrolyte **chemistry** (host/anion/cation) shifts them further (illustrative, n-limited), through the three common measurements.
- **Chapter 4** shows how those different dynamical behaviours can be *used* for reservoir-style temporal computing, and reports both positive benchmark results and the honest WESAD heterogeneity null.
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
| Ch. 3 | Lead with the **composition grid** as the quantitative result; present host/anion/cation as an n-explicit *tuning landscape*, not retention rankings. Variability → heterogeneity resource. Report the Li>Na>K cation hypothesis as an honest negative + the protocol-amplitude confound. |
| Ch. 4 | Focused reservoir-computing chapter grounded in the three common dynamical measurements: MC/NARMA benchmarks plus WESAD affective-computing demonstrations. Coincidence detection is cut; filter-bank logic is folded into heterogeneous reservoirs. |
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
