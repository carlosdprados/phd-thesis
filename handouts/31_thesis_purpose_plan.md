# Handout 31 — A Practical Purpose for the Corpus: Revision Plan

**Date:** 2026-10-18.
**Inputs:** jury-style review of Chapter 5 (2026-10-18), handout 30 (device
filter bank), the Chapter 4 composition, EIS and variability results.
**Status:** PLAN, implemented in the commits that follow it.

---

## 1. Problem

The experimental core is solid and replicated: in the SY/PEO/LiOTf/Ag grid,
composition sets the fading-memory time over about one decade (t½ ≈ 2–20 s).
EIS moves along the same axis, and within-cell scatter is measured
(σ(ln t½) ≈ 0.26).

The application chapter does not yet give that control a convincing use:

- The random-reservoir framing is matched or beaten by a one-line digital EMA.
- Timescale heterogeneity does not help the affect labels.
- The WESAD scores sit below the 2018 baseline, and the binary comparison is
  missing from the literature table.
- The Chapter 5 node applies the stretched decay once per step. For β < 1 this
  shortens the simulated memory relative to the measurement (lead cell 11.5 s at
  Δt = 1 s against a measured 19.2 s).

A jury can therefore ask what the chemical knobs are for.

## 2. The spine of the revised thesis

> Composition sets the relaxation kernel (t½, β) of a two-terminal,
> solution-processed volatile element. That kernel is a usable circuit
> parameter. Read from a component table, it predicts the element's behaviour
> as a first-order temporal filter whose time constant is chosen at
> formulation. The element then performs standard slow-signal preprocessing as
> well as a digital filter, and as well as an RC filter of the same half-life.
> Used as a random reservoir, a bank of mixed compositions does not exceed
> linear filtering.

What follows from this spine:

- **What composition is for:** selecting a component value (a time constant,
  hence a corner frequency) in a printable, capacitor-free element.
- **What chemistry, drive amplitude and the gold electrode add:** further,
  sample-limited ways to move or extend that value.
- **What variability means:** a component tolerance, not a computing resource.
- **What the costs are:** write energy, operating voltage, scatter and stability.
  These are stated with the claims.

Physiological signals stay as the worked example, because their bands overlap
the device time constants. The thesis does not claim an affective-computing
advantage.

## 3. Changes by chapter

| Part | Change |
| --- | --- |
| Chapter 5 model | Exact stretched relaxation in every node (sum of exponentials fitted to the measured kernel). Regenerate all Chapter 5 results and propagate the numbers. Add a component table (t½, β, equivalent RC τ, corner frequency, α, peak ratio). |
| Chapter 5 structure | New section "Designed filters" (handout 30, rerun with the corrected kernels) placed before the reservoir tests. Reservoir results kept, framed as the tested alternative. |
| Chapter 5 controls | Linear EMA-bank controls added to physiological reconstruction, three-class tracking and the Non-EEG replication, the analyses that lacked them. Binary and wrist Schmidt et al. rows restored to the literature table. The timescale-band table and figure made consistent. |
| Chapter 4 | Discussion and bridge state the composition result as a component-value control. Variability is read as tolerance. Design-space captions are adjusted. |
| Chapter 1 and Motivation | Designed filtering is introduced as a use of fading memory alongside reservoirs. Objective 6 and the utility question are rewritten. |
| Chapter 6 | Contributions, answers, benchmarking (against RC and digital filters), limitations and outlook rewritten around the spine. A filter bench test and a printed-RC comparison replace "build the hardware reservoir" as the first experiments. |
| Abstracts (EN/ES/CA) | Rewritten consistently. The Catalan text is aligned with the English hedging on the ion-mobility mechanism. |
| README | Summary and roadmap updated. Exports refreshed. |

Chapters 2 and 3 keep their content. Ch3 gains one sentence linking the
fabrication record to measurable tolerance.

## 4. Order of work (one commit each)

1. This plan.
2. Chapter 5 node fix, tests, regenerated Chapter 5 artefacts, and number
   propagation (Ch5, SI D, abstracts, Ch6).
3. EMA-bank controls for the reservoir analyses that lacked them, with numbers
   in the text.
4. Designed-filter section and component table in Chapter 5, with the filter
   bank rerun on corrected kernels.
5. Chapter 5 literature table, band table/figure consistency, and the reframed
   introduction, summary and limitations.
6. Chapter 4 framing.
7. Chapter 1 and Motivation.
8. Chapter 6.
9. Abstracts in all three languages.
10. README and exports, with the full build audited for undefined references.

## 5. Writing rules (as in earlier passes)

- Plain declarative sentences, British spelling, no em-dashes in prose.
- No "not X but Y" constructions, no signposting adverbs ("notably",
  "crucially", "importantly") and no narration of the thesis's own honesty.
- Numbers carry their unit of replication (substrates, subjects, seeds).
- Simulated results are called simulations. Hedges sit on the claim they
  qualify and are not repeated.

## 6. Risks

- **The corrected node will change every Chapter 5 number.** If a conclusion
  flips, the text follows the new result.
- **The filter equivalence to RC is a simulation of the measured kernel.** The
  bench test that decides it (small-signal relaxation at an operating point,
  plus replay of recorded EDA into a device) is named, not claimed.
- **Chapter 5 must stay within about 35 pages.** Detail that does not carry the
  argument moves to Appendix D.
