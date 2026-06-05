# Supervisor-Comment Response Plan

**Date:** 2026-06-05
**Source PDF:** `/Users/carlosdprados/Downloads/RT_aporte/1_2026-06-05_thesis_RT.pdf`
**Scope:** Approved response plan for supervisor comments on the earlier thesis PDF. The extracted annotations are concentrated in the first 63 PDF pages, corresponding to Chapter 1 / thesis framing. No supervisor comments were found on Chapters 2--4 in the annotated PDF.

## Decision Status

Approved for implementation:

1. Add a thesis-level Motivation, Objectives, and Structure section before Chapter 1.
2. Rewrite the opening of Chapter 1 around the direct computing-energy / data-movement problem.
3. Compress the biology section toward synapse-only relevance, but do not touch figure-related prose or figures yet.
4. Rebuild the memristor / organic state-of-the-art flow so it is shorter, more thesis-relevant, and technically cleaner.

Not approved yet:

5. Do not redraw or replace the major Chapter 1 figures yet, including the composition/cation timescale figure. Figure work should wait until the remaining chapters are finalized to avoid repeated redraws.

## Working Interpretation

The supervisor's comments should be treated as useful global-reader feedback, not as a literal edit script. The main valid signal is that Chapter 1 reads too much like an encyclopedic review and not enough like a tribunal-facing introduction to this specific thesis. The implementation should therefore make Chapter 1 shorter, more directed, and more tightly connected to the final thesis structure.

At the same time, several comments must be adapted rather than followed literally. In particular, the current thesis plan depends on:

- Chapter 3: composition as the replicated quantitative axis; host, anion, and cation as an illustrative, sample-limited chemical landscape; drive protocol as a methodological lever.
- Chapter 4: temporal / reservoir computing as the application framework, with heterogeneity claimed only where the simulations support it.

Therefore, temporal-computing material should be compressed and better positioned, not removed.

## Approved Change 1: Front-Matter Motivation, Objectives, and Structure

### Problem

The current `Scope and Objectives` section appears at the end of Chapter 1. The supervisor correctly notes that the thesis should first tell the reader what the thesis is about, why it matters, what it asks, and how it is structured.

### Implementation

Create an unnumbered thesis-level section before `\chapter{Introduction}` in `thesis.tex` or a separate included front-matter file.

Working title:

```tex
\chapter*{Motivation, Objectives and Structure of the Thesis}
\addcontentsline{toc}{chapter}{Motivation, Objectives and Structure of the Thesis}
```

Content to move/rewrite from `chapters/chapter1_introduction.tex`:

- The current `Scope and Objectives` section.
- The open scientific questions.
- The thesis objectives.
- The chapter outline.

The rewritten version should function like a short thesis roadmap, not like another review section. It should state:

- The computing problem: data movement and energy cost are becoming unsustainable, especially for AI and sensor-stream workloads.
- The device idea: volatile polymer-electrolyte organic memristors as tunable, fading-memory elements.
- The evidence hierarchy: Chapter 2 is the fully characterised exemplar; Chapter 3 has a replicated composition spine and sample-limited chemistry landscape; Chapter 4 is an in-silico temporal-computing demonstration from measured dynamics.
- The thesis structure in five chapters.

### Guardrail

Do not leave a duplicate full `Scope and Objectives` section at the end of Chapter 1. Chapter 1 can end with a short transition to Chapter 2 instead.

## Approved Change 2: Direct Opening of Chapter 1

### Problem

The current opening begins too gently and contains vague phrasing such as "highly successful" without immediately saying successful at what, and why that success has become insufficient.

### Implementation

Rewrite the start of Chapter 1 and the beginning of `The Crisis in Modern Computing` so the first pages move directly through:

1. Growth of data processing and AI workloads.
2. Energy and latency costs dominated by moving data between memory and processor.
3. The von Neumann bottleneck as the architectural origin of that cost.
4. Industrial / research responses: near-memory, in-memory, neuromorphic, event-driven, and temporal computing.
5. Why biological synapses motivate a physical element that co-localizes signal transmission, memory, and dynamics.

The Horowitz energy table should remain, but the text should contextualize whether the values are large or small by connecting per-operation energy to workload scale. The point is not only that DRAM access is expensive relative to addition, but that modern workloads require huge numbers of such accesses.

### Guardrail

Do not overfit this opening to a generic AI-energy introduction. It must still lead naturally to organic memristive devices, volatile dynamics, and reservoir-style computation.

## Approved Change 3: Compress Biology, Without Figure Work Yet

### Problem

The supervisor correctly identifies that the biology section spends too much time on whole-neuron anatomy and action-potential mechanics. The thesis devices are artificial synaptic elements, not full artificial neurons.

### Implementation

Compress the biology section around synapse-specific concepts:

- Keep only enough neuron anatomy to locate the synapse.
- Reduce axon/action-potential detail to the minimum required for understanding pre-synaptic events.
- Present synaptic transmission, short-term plasticity, long-term plasticity, and STDP in a shorter and more purposeful order.
- Emphasize the thesis-relevant abstraction: a synapse transmits signals, changes its response with recent history, and stores activity-dependent state across multiple timescales.
- Move or integrate the brain-power / synapse-count comparison earlier, near the motivation for biological inspiration.

### Explicit Exclusion

Do not touch figures or figure-related prose yet for this change. In particular:

- Do not remove the neuron/action-potential figure yet.
- Do not merge the neuron and synapse figures yet.
- Do not rewrite captions whose final content depends on figure decisions.

This preserves the option of retaining some broader biological material if the final Chapter 1 figure set still needs it.

## Approved Change 4: Rebuild Memristor and Organic State-of-the-Art Flow

### Problem

The current Chapter 1 reads as a long review split into many explicit subsections: memristor theory, TiO2 history, mechanism classification, key parameters, dynamic paradigms, inorganic devices, organic advantages, organic mechanisms, organic history, polymer electrolytes, LECs, and composite rationale. The supervisor's underlying point is valid: this needs to become a shorter argument for the specific device family and thesis plan.

### Implementation

Refactor the flow into fewer, more purposeful blocks:

1. Memristive devices as history-dependent two-terminal elements.
2. Major physical mechanisms and what they are good for.
3. Why inorganic devices dominate non-volatile memory but do not exhaust the useful memristor design space.
4. Why volatile ionic / mixed ionic-electronic devices are relevant to temporal computing.
5. Why organic materials are attractive specifically for chemically tunable, solution-processed, soft ionic devices.
6. Why the thesis uses polymer-electrolyte composites, drawing on LEC precedent and organic electrochemical examples.

Specific technical fixes:

- Simplify the memristor definition and avoid excessive formalism.
- Keep the Chua-Kang memristive-system idea only insofar as it legitimizes volatile relaxing devices as memristive systems.
- Add or retain halide perovskite examples where discussing ion-migration-based systems.
- Fix the statement that organic memristors, unlike inorganic memristors, do not specify a single mechanism. Both organic and inorganic memristors span multiple mechanisms; the distinction should be made in terms of material families and tunability, not mechanism uniqueness.
- Fold "advantages of organic memristors" into the discussion using concrete literature examples rather than a standalone list of advantages.
- Fold LEC precedent into the organic / polymer-electrolyte discussion unless a separate short subsection is still clearly justified.
- Keep the temporal / reservoir-computing material, but shorten it and align it with the final Chapter 4 plan.

### Guardrail

Do not erase the evidence-discipline language already built into the current draft:

- Composition is the replicated quantitative lever in Chapter 3.
- Host, anion, and cation comparisons are illustrative and n-limited.
- The Li > Na > K cation ordering is a tested hypothesis, not a law.
- Chapter 4 uses measured behavioural models and reports the heterogeneity null on WESAD labels honestly.

## Deferred Figure Work

Figure-related supervisor comments are acknowledged but deferred.

Deferred decisions include:

- Whether to remove or merge the neuron/action-potential figure.
- Whether to add representative literature figures for inorganic mechanisms.
- Whether to redesign dense state-of-the-art figures.
- Whether to replace the composite architecture / cation-timescale ladder figure.

The reason for deferral is strategic: Chapter 1 figures should be finalized only after Chapters 2--4 are stable, otherwise figure redrawing will likely be repeated.

## Implementation Order

1. Create the front-matter motivation/objectives/structure section.
2. Remove or reduce the duplicate scope/objectives material at the end of Chapter 1.
3. Rewrite the Chapter 1 opening and modern-computing crisis section.
4. Compress the biology prose while preserving figure dependencies.
5. Refactor the memristor / state-of-the-art sections into a shorter thesis-directed narrative.
6. Rebuild the PDF and check page count, cross-references, and duplicated content.

## Success Criteria

The revision succeeds if:

- A tribunal reader understands the thesis objective and structure before entering Chapter 1.
- Chapter 1 no longer feels like an encyclopedic review.
- The computing problem is stated directly in the first pages.
- Biology is present only as much as needed to motivate artificial synapses and fading memory.
- Memristor and organic-device background leads directly to the polymer-electrolyte composite platform.
- No approved edit weakens the current evidence hierarchy of Chapters 3 and 4.
- No major figure redrawing is performed before the rest of the thesis is finalized.
