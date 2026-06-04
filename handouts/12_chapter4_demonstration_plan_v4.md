<!-- markdownlint-disable-file MD013 MD060 -->

# Chapter 4 — Demonstration Plan (v4): Two-Tier Reservoir Computing for Affective Computing

**Author:** Carlos David Prado-Socorro
**Date:** 2026-06-04
**Status:** Active planning document. **Supersedes the application structure (§4.4–§4.6) of [`04_chapter4_temporal_computing_plan.md`](04_chapter4_temporal_computing_plan.md)**, which predates the v4 Chapter-3 reframe and still assumes a *comparative* cation fit (≥3 devices/cell). The modelling backbone of handout 04 (§4.3 behavioural model, validation, parameter cards) and the circuit-integration / design-rules sections (§4.7–§4.8) remain valid and are reused. Read alongside [`08_chapter3_4_claims_audit.md`](08_chapter3_4_claims_audit.md) and [`05_chapter4_data_pipeline.md`](05_chapter4_data_pipeline.md).

---

## 0. Decisions locked (this session)

1. **Evidence base: in-silico.** Build the behavioural model from the existing Chapter-3 fits (PULSES → φ, DELAYTIME → Kohlrausch τ/β, HYST → read transfer) and run both demonstrations as simulations grounded in measured per-device parameters. **No new fabrication.**
2. **Two demonstrations, deliberately contrasted:**
   - **Demonstration A (non-heterogeneous):** a *single composition* suffices; the lead cell **PEO 0.3 / salt 0.09** is the node. Validates the "winner" claim and judges the Ch3 findings against the application.
   - **Demonstration B (heterogeneous):** a *bank* of compositions (+ illustrative chemistry/drive diversity); this is where organic-memristor heterogeneity is a computational resource and the exploratory Ch3 landscape pays off.
3. **Task structure: benchmark + domain.** Standard reservoir benchmarks (NARMA-10, Memory Capacity) establish RC capability rigorously; the flagship **domain is affective computing** (emotion/stress recognition from slow physiological signals).

---

## 1. Alignment with the v4 Chapter-3 reframe

| Axis | Ch3 status | Role in Ch4 |
| --- | --- | --- |
| **Composition (PEO×salt, Li, Ag)** | Quantitative, replicated (n=2–9) | Primary model axis; both demonstrations |
| Cation (Li/Na/K) | Illustrative, no robust order (anion-flip) | **Not** a comparative fit axis; at most an illustrative extra node in the bank, flagged n≤2 |
| Host / anion | Illustrative (n≤2) | Illustrative bank diversity only |
| Drive amplitude | Methodological result (τ tunable by drive) | A *second* heterogeneity knob at fixed composition (per-node τ via drive) |

This corrects handout 04, which treated the cation axis as a quantitative comparative target. Chapter 4's quantitative spine is the **composition** grid; chemistry/cation nodes enter Demonstration B only as explicitly-illustrative diversity.

---

## 2. Why affective computing (the timescale argument)

Affective computing recognises human emotional/physiological state, classically from **peripheral physiological signals** that are slow and wearable-friendly. The device's measured timescale window sits directly on top of them:

| Affective signal | Characteristic timescale | Device coverage |
| --- | --- | --- |
| Phasic electrodermal response (SCR) | rise ~1–3 s, recovery ~2–10 s | low–mid PEO cells (t½ 3–19 s) |
| Respiration | ~3–5 s (0.2–0.3 Hz) | mid PEO cells |
| HRV — HF band | ~2.5–7 s (0.15–0.4 Hz) | mid PEO cells |
| HRV — LF band | ~7–25 s (0.04–0.15 Hz) | **PEO 0.3 cells (τ ≈ 19–26 s)** |
| Tonic skin-conductance level (SCL) | minutes | slowest cells / drive-boosted |

Two consequences: (i) the device is *natively matched* to these signals — no aggressive time-rescaling needed; (ii) affect information is **intrinsically multi-timescale** (fast phasic + slow tonic + HRV bands), which is the honest, task-driven motivation for Demonstration B. The narrative payoff — organic, flexible, biocompatible, low-power on-skin sensing — is exactly the affective-wearable deployment context.

---

## 3. Shared modelling backbone (built once)

Per-device, composition-indexed behavioural model (full spec: handout 04 §4.3):
- **write nonlinearity** φ_c(N): from PULSES descriptors ([`ch3_pulses_by_cell.csv`](ch3_pulses_by_cell.csv)) — compressive growth exponent α, peak/dynamic range, turnover.
- **fading memory** λ_c(Δt): Kohlrausch τ_c, β_c from DELAYTIME ([`ch3_decay_by_cell.csv`](ch3_decay_by_cell.csv)).
- **read transfer** f_c(V_read, x): from HYST window metrics.
- **noise / spread**: device-to-device + cycle-to-cycle from within-cell replicates.

**Parameter cards** = one (φ_c, λ_c, f_c, spread) per composition cell. These are the sole inputs to every simulation. Validation: leave-one-dataset-out (handout 04 §4.3.3).

**Honesty constraints baked into the model:**
- φ⊗λ **composition assumption**: integration measured at one fixed inter-pulse cadence (0.103 s), forgetting measured separately (Ch3 §3.8). The model composes them; a varied-cadence experiment is the test (flagged, not done).
- **Read perturbation**: the suprathreshold read perturbs state. Demonstrations assume a **sub-threshold read** (as in the Ch2 PoC device) or model the per-read perturbation explicitly; stated as scope.
- **Linear readout only** (ridge regression). Any nonlinear readout defeats the RC claim (handout 04 rule).

---

## 4. Common metric language

Both demonstrations are measured on the same ruler so they are directly comparable:
- **Linear Memory Capacity** MC(k) and total MC (Jaeger) — how much past input is recoverable at each lag; visualises *timescale coverage*.
- **Information Processing Capacity** (Dambre 2012) — splits total capacity into linear vs nonlinear contributions (optional but strong).
- **Task metrics**: NARMA-10 NRMSE; affective classification accuracy / macro-F1 (class-imbalanced, so F1).
- **Robustness**: performance vs injected device-to-device / cycle-to-cycle spread (measured distributions).

---

## 5. Demonstration A — non-heterogeneous (PEO 0.3 / salt 0.09 as *the* node)

**Architecture:** single-node, **time-multiplexed (delay-based) reservoir** (Appeltant 2011) — virtual nodes along a delay line supply dimensionality, so one composition is the whole reservoir.

**Runs:**
1. **Benchmark:** NARMA-10 + Memory Capacity, to establish that the single node is a competent reservoir (time-rescaled to the slow regime).
2. **Domain:** a *single-timescale* affective feature — e.g. **phasic-EDA arousal / binary stress-vs-baseline** (WESAD), where the discriminative information sits at one timescale matched to the 0.3/0.09 node.
3. **Composition sweep (the validation):** run the *same* task across all nine composition-cell models; plot MC and task-F1 vs composition. **This earns the "winner" claim** — if 0.3/0.09 is optimal (or the robust optimum given turnover-free monotonicity + n=8–9 reproducibility), report it; if a different cell wins on raw MC, report *that* honestly and explain the tradeoff.

**Claim (single-composition, defensible from n=8–9 data):** *for single-timescale affective features at the seconds scale, PEO 0.3/0.09 is the optimal single node; a heterogeneous bank is unnecessary for this application class.*

---

## 6. Demonstration B — heterogeneous (where organic shines)

**Architecture:** spatial **multi-node reservoir** built from the bank — the composition grid as the quantitative core, plus illustrative chemistry nodes and drive-amplitude-diversified nodes.

**Runs:**
1. **Domain (multi-timescale):** full affective classification — e.g. **baseline / stress / amusement** (WESAD) using EDA (phasic + tonic) + HRV + respiration, where information lives at *multiple* timescales simultaneously.
2. **The comparison that makes the point:** **homogeneous bank** (all 0.3/0.09, nodes differing only by intrinsic device scatter) vs **heterogeneous bank** (composition spread τ≈3→26 s; + illustrative chemistry; + drive-diversified τ). Show the heterogeneous reservoir (a) **broadens MC(k)** across lags and (b) **wins the multi-timescale task** the homogeneous one cannot cover.

**Claim (the organic-memristor payoff):** *cheap, intrinsic heterogeneity — composition, chemistry, drive, and device-to-device scatter — is a computational resource; the exploratory Ch3 landscape populates a multi-timescale reservoir that matches the multi-timescale structure of affect signals.* Chemistry nodes are explicitly illustrative (n≤2) → this is a **principle** demonstration.

---

## 7. The "judge the findings against the application" loop

The connective tissue between Ch3 and Ch4:
- Compute **MC(k) per composition** from the fitted (τ_c, β_c, α_c) → each cell's timescale-coverage profile.
- Overlay the **affective-signal timescale bands** (§2 table) on the composition τ-coverage → shows *which* compositions cover *which* affective channels, and whether the grid spans the full needed range.
- This makes the Ch3 composition result *actionable*: the winner (Demo A) is the cell whose τ best matches the single target channel; the bank (Demo B) is justified exactly when the target spans bands no single cell covers.

---

## 8. Datasets (open, standard; in-silico use)

- **WESAD** (Schmidt et al., ICMI 2018) — *primary.* Wearable Stress and Affect Detection; chest (RespiBAN: ECG, EDA, EMG, RESP, TEMP) + wrist (Empatica E4: BVP, EDA, TEMP); 15 subjects; baseline / stress / amusement. Slow, wearable, multimodal — ideal.
- Alternatives / robustness: **DEAP** (valence/arousal, peripheral channels), **AMIGOS**, **CASE**, **K-EmoCon**.
- **Citation hygiene:** WESAD, Picard (Affective Computing, 1997), Appeltant 2011, Jaeger 2002, Dambre 2012, NARMA (Atiya–Parlos 2000) must be **CrossRef-verified before entering `references.bib`** (per the Ch1 bibliography-audit lesson). Not yet added.

---

## 9. Honesty boundaries / scope conditions (state in the chapter)

1. In-silico; every figure caption names its input data; the model is measured φ⊗λ⊗f, not a bench RC run.
2. φ⊗λ composition assumption (single cadence); varied-cadence experiment named as future work.
3. Slow-signal operating regime (sub-kHz); affective signals are natively in-band, but fast tasks are out of scope.
4. Sub-threshold read assumed (or read-perturbation modelled).
5. Chemistry/cation bank nodes illustrative (n≤2); Demonstration B is a principle demonstration, not a powered comparison.
6. Linear readout only.

---

## 10. Fate of the handout-04 applications

- **Reservoir computing** (04 §4.4) → split into Demonstrations A and B here; remains the flagship.
- **Multi-timescale filter bank** (04 §4.6) → folded into Demonstration B as the *multi-timescale affective feature extraction* front-end (it is the same idea: parallel τ channels).
- **Spike coincidence detection** (04 §4.5) → **demote to an optional supporting vignette** or drop, to keep the chapter focused on the two reservoir demonstrations + affective domain. (Open decision below.)

---

## 11. Open decisions

1. **Coincidence detection (04 §4.5):** keep as a short supporting vignette, or cut for focus?
2. **Affective task granularity:** binary stress-vs-baseline (cleanest, class-balanced-ish) for Demo A and 3-class (baseline/stress/amusement) for Demo B — confirm.
3. **Single dataset (WESAD) or WESAD + one cross-dataset robustness check (DEAP)?**
4. **Drive-diversity as a heterogeneity axis in Demo B:** include (uses the Ch3 protocol result) or keep Demo B to composition+chemistry only?

---

## 12. Next steps (build order)

1. **`scripts/ch4_model.py`** — assemble parameter cards from the `ch3_*_by_cell.csv` artifacts (+ per-device fits); implement the discrete-time φ⊗λ⊗f model; leave-one-out validation.
2. **`scripts/ch4_reservoir.py`** — single-node time-multiplexed RC (Demo A) + spatial multi-node RC (Demo B); MC/IPC + task harness.
3. **WESAD ingestion** — load, segment, slow-channel feature streams; pulse-encode for the reservoir input layer.
4. Composition sweep (Demo A validation) → MC/F1 vs composition figure.
5. Homogeneous-vs-heterogeneous comparison (Demo B) → MC(k) breadth + task-F1 figure.
6. Draft `chapters/chapter4_temporal.tex` around the two demonstrations once the simulations produce numbers.
