<!-- markdownlint-disable-file MD013 MD060 -->

# Chapter 4 — Demonstration Plan (v4): Two-Tier Reservoir Computing for Affective Computing

**Author:** Carlos David Prado-Socorro
**Date:** 2026-06-04
**Status:** Active planning document. **Supersedes the application structure (§4.4–§4.6) of [`04_chapter4_temporal_computing_plan.md`](04_chapter4_temporal_computing_plan.md)**, which predates the v4 Chapter-3 reframe and still assumes a *comparative* cation fit (≥3 devices/cell). The modelling backbone of handout 04 (§4.3 behavioural model, validation, parameter cards) and the circuit-integration / design-rules sections (§4.7–§4.8) remain valid and are reused. Read alongside [`08_chapter3_4_claims_audit.md`](08_chapter3_4_claims_audit.md) and [`05_chapter4_data_pipeline.md`](05_chapter4_data_pipeline.md).

> **⚠️ UPDATE 2026-06-04 (WESAD downloaded & run — results are in; see new [§13](#13-measured-wesad-results-2026-06-04--honest-narrative-pivot) and [§14](#14-physiological-temporal-context-reconstruction-2026-06-04--affect-aligned-heterogeneity-benchmark)).** The flagship Demonstration-B claim as written in §2/§6 — *"the heterogeneous reservoir wins the multi-timescale affect task the homogeneous one cannot cover"* — **is NOT supported by the measured WESAD label-classification data**, even after rebuilding the task as a memory-demanding *streaming* one (the fair test). What the data DO support: (i) the in-silico device reservoir does real affective computing (Demo A binary **0.894**; Demo B 3-class **~0.76**); (ii) fading **memory** helps the streaming task (**+0.049** vs instantaneous; **+0.014–0.020** controlling for dimensionality); (iii) timescale **heterogeneity** is *within noise* on WESAD labels (**ΔF1 het−hom = +0.005 ± 0.011**, 7/10 seeds), because the discriminative label memory demand is dominated by a single slow (tonic) band the lead composition already serves. **The "heterogeneity is a computational resource" claim is therefore anchored on two measured benchmarks:** architecture-level MC (**1.49×**) and the new WESAD physiological temporal-context reconstruction (**R² 0.756 vs 0.744 best homogeneous, N=48**), while final affect labels are reported as a real downstream task with an honest heterogeneity null. §2, §6, §7 below are kept for provenance but must be read through §13–§14.

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
- φ⊗λ **composition assumption** (sharpened 2026-06-04): PULSES (φ) were measured at **3 V write / 1.5 V read**, DELAYTIME (λ) at **4 V write / 2 V read** — *different write amplitudes*, not just measured separately. Since drive amplitude co-sets the timescale (v114 4.6→15.5 s), composing a 3 V potentiation shape with a 4 V decay assumes regime-compatibility; this likely **under-estimates** the true drive↔retention coupling. Inter-pulse cadence is effectively common (0.104/0.103 s). The clean test is one matched-amplitude pulse-train experiment sweeping N and interval (flagged, not done). See Ch3 Table 3.1 + §3.8.
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
- **Spike coincidence detection** (04 §4.5) → **cut from the main chapter**; mention only as background if needed, to keep the chapter focused on the two reservoir demonstrations + affective domain.

---

## 11. Decisions — LOCKED (2026-06-04)

1. **Coincidence detection (04 §4.5): CUT.** Chapter focuses on the two reservoir demonstrations + affective domain. (May return as a one-line mention only.)
2. **Affective task granularity:** Demo A = **binary** stress-vs-baseline; Demo B = **3-class** baseline/stress/amusement.
3. **Datasets:** **WESAD primary** for the thesis; DEAP an *optional* cross-dataset robustness check, not required.
4. **Drive-amplitude diversity: INCLUDE** as a third heterogeneity axis in Demo B (cheap, already-measured via the Ch3 protocol result; strengthens "organic gives many heterogeneity knobs").

---

## 12. Next steps (build order)

1. **`scripts/ch4_model.py`** — ✅ **STARTED (2026-06-04).** `ParameterCard` per composition cell assembled from `ch3_decay_by_cell.csv` + `ch3_pulses_by_cell.csv`; `decay_factor(dt)` (identified Kohlrausch τ/β, else single-exp from t½) and `potentiation_ratio(N)` (power-law to peak + turnover roll-off); `lead_card()` = PEO0.3/0.09; runnable self-test PASSES (9 Li cards). **TODO:** leave-one-dataset-out validation vs raw curves; per-device spread for the variability envelope; pulse-encoding front end.
2. **`scripts/ch4_reservoir.py`** — ✅ **EXPANDED (2026-06-04).** Spatial multi-node bank + **linear Memory Capacity** (Jaeger, ridge), **NARMA-10**, and a **per-composition sweep**.
   - *Demo-B (heterogeneity):* heterogeneous bank total MC ≈ 6.0 vs homogeneous ≈ 4.1 → **1.47×**, gain at short lags.
   - *Demo-A validation (sweep):* **best total-MC = PEO 0.3/0.09** (the lead, MC 3.44); best NARMA-10 = PEO 0.3/0.045 (NRMSE 0.627), lead a close 2nd (0.669). **Both winners are in the low-PEO row, as Ch3 predicts** — so 0.3/0.09 is validated as the memory-capacity optimum, with 0.3/0.045 competitive on NARMA (its larger dynamic range helps drive).
   - *Caveat:* absolute NARMA NRMSE is high (~0.6–0.8) — a bank of *independent* (non-recurrent, 1T1M) leaky nodes is a weak NARMA reservoir; only the *relative* composition ranking is claimed. Self-test PASSES.
   - **TODO:** single-node *time-multiplexed* (delay-feedback) variant for Demo A; MC(k) + sweep figures; inject measured device-to-device spread; drive-diversity nodes (Demo B).
3. **`scripts/ch4_wesad.py`** — ✅ **DONE ON REAL DATA (2026-06-04).** WESAD present at `data/wesad/WESAD/S2..S17` (15 subjects). Now multichannel (chest **EDA + Resp + Temp + HR-from-ECG**; robust R-peak detection via scipy), per-subject robust scaling (preserves tonic level, LOSO-safe), cached at the scaled-stream level. **Demo A** = window-level binary stress/baseline (EDA, lead bank). **Demo B rebuilt as STREAMING** continuous per-step affect tracking (reservoir runs over the whole session; per-step ridge one-hot; LOSO; causal label smoothing) — the memory-demanding fair test — with **het / hom / instantaneous / memoryless** banks, per-class F1, seed error bars, and a dt sweep. Self-test + synthetic smoke test pass. **Results: see [§13](#13-measured-wesad-results-2026-06-04--honest-narrative-pivot).** Net: multichannel + per-subject scaling lifted Demo A to **0.894**; the streaming reformulation made the task memory-demanding (memory helps) but **Demo B did NOT clear the homogeneous control** (ΔF1 = +0.005 ± 0.011, ns).
4. ✅ **`scripts/ch4_physio_context.py` (2026-06-04)** — **NEW affect-aligned heterogeneity benchmark.** Uses real WESAD EDA/Resp/Temp/HR streams, but the target is multi-lag physiological context reconstruction rather than final affect labels: reconstruct each channel at 1, 3, 8, 20 and 45 s delays from the reservoir state (LOSO, linear ridge, N=48). Results: instantaneous R² **0.673**, memoryless **0.674**, homogeneous fast **0.741**, homogeneous slow **0.744**, heterogeneous **0.756 ± 0.002**. Heterogeneity gain over the best homogeneous control = **+0.012 R²**; memory gain over instantaneous = **+0.084 R²**. Outputs: `handouts/ch4_physio_context_results.csv`, `figures/chapter4/physio_context_reconstruction.pdf`. See [§14](#14-physiological-temporal-context-reconstruction-2026-06-04--affect-aligned-heterogeneity-benchmark).
5. ✅ **`scripts/ch4_figures.py` (2026-06-04)** — `figures/chapter4/mc_curve.pdf` (MC(k), heterog. 6.0 vs homog. 4.1) + `composition_sweep.pdf` (MC & NARMA by cell). Demo-A/B figures done. The physiology-context figure is generated by `scripts/ch4_physio_context.py`.
6. **Single-node *time-multiplexed* (delay-feedback) Demo-A variant** — optional alternative architecture; not required for the claim.
7. Draft `chapters/chapter4_temporal.tex` around the three-level evidence structure: MC/NARMA → physiological-context reconstruction → WESAD label task.

---

## 13. Measured WESAD results (2026-06-04) — honest narrative pivot

WESAD downloaded (15 subjects, S2–S17) → `data/wesad/WESAD/` (gitignored). Labelled material after windowing/streaming: baseline ≈ 17 610 s, stress ≈ 9 965 s, amusement ≈ 5 574 s. All numbers below are **leave-one-subject-out (LOSO)**, in-silico devices (Ch3 parameter cards), linear (ridge) readout only.

### 13.1 Demonstration A — window-level binary stress/baseline (single channel EDA, lead bank)

| Model | LOSO macro-F1 | per-class F1 |
| --- | --- | --- |
| Device reservoir (lead PEO 0.3/0.09) | **0.894** | baseline 0.93 · stress 0.88 |
| Static feature baseline (mean/std/last/slope of EDA) | 0.899 | — |

**Read:** a single composition is a competent node for a single-timescale affect feature (✅ the Demo-A claim). *But* a static baseline matches it → **the 60 s-window task is quasi-static (no fading memory required)**, which is exactly why timescale heterogeneity cannot help it. This motivated rebuilding Demo B as a memory-demanding streaming task.

### 13.2 Demonstration B — streaming 3-class affect tracking (multichannel EDA+Resp+Temp+HR, dt=1 s, 15 s smoothing)

Reservoir runs continuously over each session; the affect class is read out at every step. Means ± SD over 10 random bank seeds (matched input masks across conditions):

| Model | LOSO macro-F1 | increment |
| --- | --- | --- |
| Instantaneous input (no memory) | 0.709 | — (static ceiling) |
| Memoryless 24-node bank (decay = 0) | 0.737 | **+0.028 dimensionality** |
| Homogeneous bank (memory, single τ) | 0.753 ± 0.009 | **+0.016 memory** |
| Heterogeneous bank (memory, τ ≈ 3→26 s) | 0.758 ± 0.006 | **+0.005 heterogeneity (ns; 7/10 seeds >0)** |

- **het − instantaneous = +0.049 ± 0.006** (robust across dt 0.5–4 s) — but most of this is dimensionality.
- **Genuine fading-memory gain = +0.014 to +0.020** (heterogeneous vs a *same-size memoryless* bank) — modest but consistent.
- **Timescale-heterogeneity gain = +0.005 ± 0.011** — **within noise.** dt sweep: het−hom ∈ [+0.002, +0.007] across dt; positive but never separable from zero.

Per-class (best bank): baseline 0.90 · stress 0.92 · **amusement 0.55** — amusement (short, low-arousal) is the hard class for all models.

### 13.3 Why heterogeneity does not pay off on affect (the honest mechanism)

Affect labels are slowly-varying sustained states; the discriminative memory demand is **dominated by one slow (tonic) band** that the lead composition's τ (~19–26 s) already serves. Heterogeneity only converts into task performance when the target requires memory at **many distinct lags simultaneously** — which the architecture-level **Memory Capacity** benchmark *does* (het 6.12 vs hom 4.10, **1.49×**; broader MC(k)), and NARMA/MC rank the **lead PEO 0.3/0.09** top. So:

- **"Heterogeneity is a computational resource" → keep, but anchor it on the benchmarks where it is measured cleanly: MC/NARMA (task-agnostic) and physiological temporal-context reconstruction (affect-aligned).**
- **On affect → the honest claim is: the devices perform real affective computing (0.89 binary; 0.76 streaming 3-class), fading memory contributes (+0.014–0.020), and composition-timescale *matching* (the Ch3 result) is the design lever; heterogeneity is a generality/robustness hedge, not required when one timescale dominates.**

This *unifies* Ch3 → Ch4: Ch3 shows composition (and drive) **set** the device timescale; Ch4 shows you then **match** that timescale to the task, and that a spread of timescales buys memory breadth on both random-input benchmarks and real physiological histories, rather than a guaranteed win on any one final label set.

### 13.4 Figure & artefacts

- `figures/chapter4/wesad_affect.pdf` — (a) Demo A reservoir vs static; (b) Demo B streaming decomposition (inst → +dim → +memory → +heterog) with seed error bars.
- `figures/chapter4/mc_curve.pdf`, `composition_sweep.pdf` — unchanged architecture-level heterogeneity result.
- `figures/chapter4/physio_context_reconstruction.pdf`, `handouts/ch4_physio_context_results.csv` — real-WESAD physiological temporal-context reconstruction result.
- Cache: `data/wesad/_cache_EDA-Resp-Temp-HR_4hz.npz` (scaled streams; gitignored with the dataset).

### 13.5 Scope / caveats to state in the chapter

In-silico devices; linear readout; HR from chest ECG (cleaner than wrist BVP); per-step ridge with 15 s causal smoothing; single dataset (WESAD). The het−hom null is reported as a **negative result with error bars**, not hidden. A matched-amplitude varied-cadence pulse-train experiment (φ⊗λ assumption, §3) remains the key future bench test.

### 13.6 Open decision for the writing pass

Chapter framing options were put to the author; **selected: build the streaming task** (done, above). Remaining call for the draft: present Ch4 as **(benchmarks = where heterogeneity wins) + (WESAD = where the devices do real affect, memory helps, heterogeneity is an honest null)** — the recommended honest structure — before writing `chapters/chapter4_temporal.tex`.

---

## 14. Physiological temporal-context reconstruction (2026-06-04) — affect-aligned heterogeneity benchmark

**Why this benchmark was added.** The WESAD label task is a fair downstream affective-computing test, but the labels are sustained states; once the slow tonic context is available, additional timescale diversity has little separable effect. The new benchmark keeps the **real WESAD physiology** but changes the target to the thing heterogeneity is supposed to provide: simultaneous access to fast, medium and slow physiological history.

**Task.** Input streams are chest **EDA + Resp + Temp + ECG-derived HR**, sampled at `dt=1 s` after the existing WESAD preprocessing. The reservoir runs continuously over each subject. A linear ridge readout reconstructs each input channel at delays of **1, 3, 8, 20 and 45 s**. These delays map to fast phasic / beat-to-beat context, respiration/HF-HRV-scale context, and tonic/LF-HRV-scale context. Evaluation is leave-one-subject-out over the 15 WESAD subjects, restricted to baseline/stress/amusement periods.

**Controls.** Same-size 48-node banks:

| Model | Held-out mean R² | fast 1–3 s | mid 8 s | slow 20–45 s |
| --- | ---: | ---: | ---: | ---: |
| Instantaneous input | 0.673 | 0.715 | 0.670 | 0.632 |
| Memoryless bank | 0.674 ± 0.000 | 0.721 | 0.667 | 0.630 |
| Homogeneous fast bank | 0.741 ± 0.003 | **0.815** | 0.735 | 0.669 |
| Homogeneous slow bank | 0.744 ± 0.002 | 0.787 | 0.724 | **0.711** |
| **Heterogeneous composition bank** | **0.756 ± 0.002** | **0.815** | **0.737** | 0.708 |

**Read.** The heterogeneous bank is not magic: the fast homogeneous bank is best at the fastest context and the slow homogeneous bank is best at the slowest context. The point is that the heterogeneous bank gives the best **single bank** across the whole physiological context vector. Its gain over instantaneous input is **+0.084 R²**; its gain over the best homogeneous same-size control is **+0.012 R²**. This is the affect-aligned result that the WESAD final-label classifier could not expose.

**Drafting use.** This should sit between MC/NARMA and the WESAD label classifier:

1. MC/NARMA: task-agnostic proof that timescale spread broadens memory.
2. Physiological context reconstruction: real affective streams; heterogeneity improves multi-lag physiological encoding.
3. WESAD labels: downstream affective classification; devices work and memory helps, but heterogeneity is not required because one slow timescale dominates the labels.
