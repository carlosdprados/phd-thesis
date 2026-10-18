# Handout 30 — Composition-Designed Device Filter Bank for Electrodermal Activity

**Date:** 2026-10-18.
**Script:** `scripts/ch5_filterbank.py` (registered in `scripts/reproduce.py`,
physiological steps). **Tests:** `tests/test_ch5_filterbank.py`.
**Figure:** `figures/chapter5/filterbank.pdf` (not referenced by the thesis).
**Outputs:** `handouts/ch5_filterbank_{design,synthetic,wesad,tier2,device_vs_rc}.csv`.
**Status: INTEGRATED** as Chapter 5 §"Designed Filters from the Component Cards" and Appendix D (handout 31).

---

## 1. Question

The Chapter 5 reservoir uses the device bank as a random temporal feature
generator, and a digital EMA matches or beats it. This analysis asks a narrower,
hardware-relevant question: used as **designed analogue filters**, do the
measured relaxation kernels perform the standard phasic-EDA preprocessing step?
The two topologies are:

- **HP** (one device as a baseline tracker): `x − LP_c(x)`.
- **BP** (two compositions): `LP_fast(x) − LP_slow(x)`, with zero DC gain.

The fair hardware comparator is an **RC filter with the same half-life**. The
accuracy reference is a causal Butterworth phasic filter (0.05–1 Hz), with an
EDASymp-band variant (0.045–0.25 Hz; Posada-Quintero et al. 2016).

## 2. Bottom line

1. **A single fastest-composition device performs tonic removal with no
   measurable loss.**
   - Synthetic SCR detection F1 is 0.713 / 0.680 / 0.676 (clean / noisy /
     artefacts), against 0.701 / 0.669 / 0.647 for the digital reference.
   - WESAD within-subject stress-vs-baseline AUC of per-minute phasic power is
     0.952 for the device and 0.951 for the digital reference on the chest.
   - On the wrist it is 0.921 vs 0.927, with Spearman agreement ρ = 0.98–0.99
     between the two features.
2. **That device is an RC filter.** The best cell (PEO 1.2/0.045, t½ 2.74 s)
   has β = 1.00, so its kernel is a single exponential.
   - Across all eight cells, the measured stretched kernel never beats RC at
     the same half-life.
   - The two β = 0.61 cells are slightly worse: WESAD chest −0.009 AUC, with
     p = 0.013 and p = 0.038.
3. **Two-composition band-passes sit below the phasic band.**
   - Every device HP corner is 0.003–0.041 Hz, below the EDASymp lower edge of
     0.045 Hz.
   - No cell can set an upper band edge.
   - The best BP passes 0.002–0.047 Hz (peak 0.012 Hz) and leaks tonic drift:
     tonic/phasic output power 1.95, against 0.10 for the digital reference.
   - It is the worst design on every metric.
4. **The case for the device therefore rests on non-electrical properties**
   (footprint, printability, no capacitor) against a printed RC, not on filter
   performance.

## 3. Methods (summary)

- **Tier 1 (primary):** linear superposition with the measured Kohlrausch
  kernel `exp[−(t/τ)^β]`, applied by exact causal convolution at 4 Hz.
  - Kernels reproduce every measured half-life to within one sample (tested).
  - Filters start in steady state at the first sample, so they are causal.
- **Tier 2 (sensitivity):** the Chapter 5 composed node generalised to
  stretched decay.
  - Pulse progress `p` is filtered with `h^(1/α)` and the enhancement is
    `x = p^α`. A single write decays exactly as `h`.
  - For β = 1 it equals `run_states` (tested).
  - Read-out gain is fixed on a 60 s calibration prefix.
- **Synthetic ground truth:** 40-min sessions with:
  - 5-min alternating calm/aroused blocks (≈2 and ≈7 SCR/min);
  - Bateman SCRs (rise 0.5–1.2 s, decay 2–7 s, log-normal amplitudes with a
    0.2 µS median);
  - tonic drift with an aroused-block SCL rise;
  - conditions clean (0.005 µS white noise), noisy (0.03 µS) and artefacts
    (1/min sharp 0.2–1.5 µS spikes).
- **Detection and scoring:**
  - Threshold and lag are calibrated on 12 sessions; scores come from 30
    separate sessions.
  - Device instances carry the measured within-cell scatter σ(ln τ) = 0.264;
    RC filters are ideal.
  - Synthetic sessions are reported as mean, SD and sign counts, without
    p-values (Chapter 5 convention).
- **WESAD:**
  - Raw chest EDA (700 Hz, causal 0.25 s block mean) and wrist E4 EDA (4 Hz),
    in µS.
  - Non-overlapping 60 s windows inside protocol segments.
  - Per-subject AUC (stress vs baseline), then a paired Wilcoxon over 15
    subjects.

## 4. Results

### Design space (E1)

| Design | −3 dB band (Hz) | Mean gain in 0.045–0.25 Hz | Gain at 0.01 Hz |
| --- | --- | --- | --- |
| Device HP, PEO 1.2/0.045 (t½ 2.7 s) | 0.041–Nyquist | 0.88 | 0.23 |
| Device HP, PEO 0.3/0.09 (lead, t½ 19 s) | 0.004–Nyquist | 0.99 | 0.89 |
| Device BP, PEO 1.2/0.045 − PEO 0.3/0.045 | 0.002–0.047 | 0.34 | 0.82 |
| Digital phasic 0.05–1 Hz | 0.050–1.0 | 0.93 | 0.04 |

The fastest cells sit near the conventional 0.05 Hz tonic/phasic split, while
slower cells pass the tonic band.

### Synthetic SCR detection (E2), test F1 mean

| Design | Clean | Noisy | Artefacts | Tonic leak (clean) |
| --- | --- | --- | --- | --- |
| Digital phasic 0.05–1 Hz | 0.701 | 0.669 | 0.647 | 0.10 |
| Digital EDASymp band | 0.658 | 0.648 | 0.624 | 0.09 |
| **Device HP PEO 1.2/0.045** | **0.713** | **0.680** | **0.676** | 0.15 |
| RC HP, same t½ | 0.712 | 0.677 | 0.675 | 0.15 |
| Device HP, lead cell | 0.694 | 0.648 | 0.660 | 0.78 |
| Device BP (best pair) | 0.539 | 0.540 | 0.496 | 1.95 |
| RC BP, same pair | 0.561 | 0.537 | 0.522 | 0.75 |
| Raw signal (no filter) | 0.690 | 0.638 | 0.657 | 3.87 |

Device HP minus digital is +0.029 under artefacts (29/30 sessions positive).
Peak detection by prominence already tolerates slow baselines, so even the raw
signal scores 0.69. Filtering matters most for noise and artefacts. High-pass
filtering sharpens overlapping SCRs, so these filters beat detection on the
noise-free phasic trace itself (0.662 clean). That trace is therefore not a
ceiling.

### WESAD (E3): stress vs baseline AUC, per-minute phasic power

| Design | Chest | Wrist |
| --- | --- | --- |
| Digital phasic 0.05–1 Hz | 0.951 | 0.927 |
| Digital EDASymp band | 0.947 | 0.922 |
| **Device HP PEO 1.2/0.045** | **0.952** | **0.921** |
| RC HP, same t½ | 0.951 | 0.920 |
| Device BP (best pair) | 0.903 | 0.880 |
| RC BP, same pair | 0.923 | 0.893 |
| *Tonic SCL (window mean)* | *0.915* | *0.885* |

Paired tests over 15 subjects:

- Device HP minus digital: chest +0.001 (p = 0.94); wrist −0.006 (2/15
  positive, p = 0.038).
- Device BP minus RC BP: chest −0.020 (p = 0.062); wrist −0.013 (p = 0.10).

SCR-count AUCs use thresholds transferred from synthetic calibration. They are
secondary, and the BP counts follow tonic leakage.

### Tier 2 (E4), clean synthetic

| Design | Read-out | F1 | r with true phasic |
| --- | --- | --- | --- |
| Device HP | Tier 1 (measured kernel) | 0.713 | 0.56 |
| Device HP | Tier 2, level-matched | 0.712 | 0.61 |
| Device HP | Tier 2, small-signal matched | 0.748 | 0.53 |
| Device HP | Tier 2, linearised kernel h^(1/α) | 0.746 | 0.33 |
| Device BP | Tier 2, level-matched | 0.636 | 0.002 |
| Device BP | Tier 2, small-signal matched | 0.638 | 0.67 |

- **The drive level cancels exactly.** The `p^α` compression is scale-free, so
  results are identical at drive 0.05 and 1.0, and nothing saturates (max
  progress 0.06 for HP, 0.59 for BP).
- **The read-out must match small-signal gain.** A level-matched read-out
  under-subtracts the baseline by a factor α. For the BP pair, whose cells have
  α = 0.33 and 1.11, it fails completely.
- **The Tier-2 kernel is a model consequence, not a measurement.** If the
  composed model holds, the small-signal kernel is `h^(1/α)`, which is faster
  (τ·α^(1/β)). For the fastest cell that is τ ≈ 1.3 s, a corner near 0.12 Hz
  inside the EDASymp band.

## 5. Caveats

- Both tiers are assumptions about superposition and drive–retention
  composition. The one-sample = one-pulse mapping at 4 Hz is a convention.
- The synthetic generator's SCR and tonic parameters are chosen ranges, not
  fitted to a corpus.
- WESAD stress is the TSST (speech, movement, fixed protocol order). Part of
  the phasic-power separation may come from motion or protocol position. This
  is the same for all filters, so the comparison between them is unaffected.
- RC components are idealised, with no tolerance. Energy, area and read
  circuitry are not modelled.

## 6. What would change the conclusion

- **A bench measurement of the small-signal relaxation** at an operating point
  (a small write superposed on a written state). If it follows `h^(1/α)` rather
  than `h`, the fastest cells move into the phasic band and could set the upper
  edge as well.
- **A footprint and variability comparison** of the device against a printed RC
  realising τ ≈ 4 s on the same substrate.

## 7. Side finding: per-step decay compounding in the Chapter 5 model

`ch5_reservoir.run_states` applies `λ = exp[−(Δt/τ)^β]` once per step. For
β < 1 this compounds into a plain exponential whose half-life depends on Δt,
instead of the measured stretched decay. Simulated vs measured half-lives:

| Cell | Measured t½ | Simulated at Δt = 1 s (WESAD) | Simulated at Δt = 5 s (benchmarks) |
| --- | --- | --- | --- |
| PEO 0.3/0.045 | 15.8 s | 5.9 s | 10.5 s |
| PEO 0.3/0.09 (lead) | 19.2 s | 11.5 s | 15.2 s |
| PEO 0.6/0.18 | 5.5 s | 2.9 s | 5.3 s |

All Chapter 5 reservoir and WESAD numbers inherit this. The text's statement
that each card "reproduces the cell-median half-time exactly" holds for a single
interval, not over a simulated trajectory. A convolution or Prony-series node,
as used here, would fix it.

**Fixed on 2026-10-18** (commit `61e250f`): nodes now follow the sampled kernel,
and every Chapter 5 result was regenerated (handout 31).

## 8. Reproduce

```sh
python scripts/ch5_filterbank.py   # ~75 s with the cached WESAD EDA
python -m pytest -q tests/test_ch5_filterbank.py
```

The first run builds `data/wesad/_cache_filterbank_eda_uS_4hz.npz` from the
WESAD pickles. That takes several minutes on iCloud storage.
