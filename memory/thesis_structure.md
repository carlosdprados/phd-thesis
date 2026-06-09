---
name: thesis-structure
description: "5-chapter thesis plan (v3, April 2026). Canonical detailed copy lives in the repo (handouts/01 & 00) — trust those if they differ from this skeleton."
metadata: 
  node_type: memory
  type: project
  originSessionId: 74103bc0-6a21-4b5a-ade9-98c719e23346
---

# Thesis Chapter Plan — 5 chapters (v3)

⚠️ The **canonical, maintained** versions are version-controlled in the repo: `handouts/01_thesis_structure.md` (detailed plan + framing table) and `handouts/00_thesis_overview_memory.md` (full overview). This memory is a pointer/skeleton — **defer to those files if anything differs.** (An earlier note here said "4 chapters" — wrong; the plan became 5 chapters in v2/v3, April 2026.)

## Skeleton

1. **Introduction** — von Neumann bottleneck → neuromorphic → memristors → organic electronics → polymer-electrolyte composites → **volatile vs non-volatile / temporal & event-driven computing** framing → objectives.
2. **Proof of Concept — SY/Hybrane/LiOTf** (Paper 1, [[paper1_summary]]). The *only* fully-characterised device; EPSC, STDP, separated STM/LTM, and impedance are **Ch2-only primary evidence**. Written (April 2026), `chapters/chapter2_proof_of_concept.tex`.
3. **Composition-led Comparative Chapter** (v4 reframe — **drafted**, `chapters/chapter3_comparative.tex`). The **only quantitative axis is composition** (PEO×salt, Li, Ag, replicated n=2–9): window↓, potentiation strength↓ (α 1.1→0.3), fading memory tunable t½≈3–22 s with PEO; salt sets the potentiation turnover ceiling. **Cation/host/anion are illustrative (n≤2), not comparative** — the cation honest-negative is anchored by the TMPE-host *anion-flip* (triflate: K longest; TFSI: K shortest). Plus a methodological result: drive amplitude co-sets τ (v114 4.6→15.5 s). Lead/"winner" composition = **PEO 0.3 / salt 0.09**. See repo `handouts/08` (claims audit) & `10` (Ch3 plan).
4. **Data-Driven Temporal Computing** (v4 — **planned**, `handouts/12`). **In-silico**, no new fabrication; behavioural model = measured φ(N)⊗Kohlrausch τ⊗read transfer. **Two contrasted demonstrations:** (A) *non-heterogeneous* single-node time-multiplexed reservoir on PEO 0.3/0.09 (validated by a composition sweep); (B) *heterogeneous* multi-node reservoir where organic composition/chemistry/drive diversity pays off. Benchmark (NARMA-10, Memory Capacity) **+ affective-computing domain** (WESAD; device τ matches phasic-EDA/respiration/HRV timescales). Ch2 metrics = Li-only priors. Supersedes handout 04's three-application structure.
5. **Conclusions & Outlook.**

## Key framing rule (propagates through all chapters)

These devices are **not** framed as bad non-volatile memories but as good **volatile, heterogeneous, temporally-rich** elements. The Ch3 comparative claims rest on **only three common measurements** — I–V hysteresis, variable-N potentiation, variable-delay depotentiation (folder tags `Day*_Hyst` / `_NmbPls` / `_DlyTime`); see [[phd_data_structure]] and [[nanomem_analysis_pipeline]] for how those map to the archive.

**How to apply:** maintain the 5-chapter framing and the "volatile = feature" stance. Status (2026-06-04): **Ch2 & Ch3 drafted** (Ch3 builds standalone + in thesis, 4 figures generated from `scripts/ch3_figures.py`); Ch4 planned (handout 12, awaiting model build); Ch1 drafted earlier; Ch5 not drafted.
