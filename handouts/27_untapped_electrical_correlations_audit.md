# Untapped Electrical-Characterisation Correlations — Data-Mining Audit

Date: 2026-06-10
Scope: the **same electrical characterisation already run across the whole device
library** (HYST, PULSES, DELAYTIME, VCONST, EIS in `DATABASE/DEVICES_*_*.csv`).
Question asked: *given what the thesis already claims, is there anything in the
existing electrical data — correlations or structure across devices — that we
have measured but not noticed or shown, and that would pay off to include?*
This is **not** about new experiment types; only re-mining what exists.

## Provenance recap (source of truth)

- Raw Keithley sweeps: `Nanomem_Devices_Library/DEVICES_LAB_DATA/<quarter>/<device>/Day<N>_<MeasType>/<pixel>/D1_all.txt`.
- `project_feature_extraction` → the **canonical processed truth**:
  `DATABASE/DEVICES_<TYPE>_{DEVICE,PIXEL,CURVE}_INFO.csv` (+ `ALL_DATAPOINTS`),
  last regenerated May 2025. Fabrication metadata: `UPDATED_DEVICES_LIBRARY.csv`.
  Red-flag exclusions: `FILTERED_DEVICES.csv` (drop-list, possibly incomplete).
- Keys: `device_name` (NM_vXXX substrate) · `pixel` (16 junctions) · `day`
  (days since fabrication). The comparative chapter rests on three of these:
  `_Hyst`, `_NmbPls`, `_DlyTime`.

All numbers below were computed live from the May-2025 CSVs on 2026-06-10.

---

## TL;DR — what's worth doing

| # | Finding | Payoff | Effort |
|---|---------|--------|--------|
| 1 | The "measured device-to-device scatter ≈ 0.12" that the Ch5 robustness claim cites is **wrong by ~15×**; the real measured value is σ(ln τ) ≈ **2.0**. | **High** — fixes a viva-exposed factual gap *and* strengthens the heterogeneity-as-resource thesis | Low |
| 2 | A library-wide **dynamical property map** exists in the data but is shown only for the Li/PEO spine; extend it to the **HYST window axis** and the **full chemistry palette**. | High — visually grounds the "heterogeneous palette" for the whole library | Low–Med |
| 3 | Memory window and retention are **weakly positively coupled** across the library (Spearman ρ=0.23, p=0.04, n=81) — currently unreported. | Med — a real cross-measurement relationship for node selection | Low |
| 4 | **VCONST** constant-voltage relaxation is essentially **unextracted** (rich features, but only 8 devices). | Low — optional third τ probe for those 8 | Low |

And two things I checked and **reject** (see end) so the audit is honest:
sweep-rate dependence of the hysteresis loop, and yield-by-composition.

---

## FINDING 1 — The heterogeneity number the central claim cites is ~15× too small (and the truth helps you)

**What the thesis currently does.** `scripts/ch5_reservoir.py` injects
device-to-device variation as a lognormal `jitter` (default **0.12**):
`tau = c.tau * exp(N(0, jitter))`. `scripts/ch5_figures.py:96-97`
draws a vertical line at **0.12 labelled "measured scatter"** on the robustness
figure, and the surrounding text argues the heterogeneous bank keeps its
advantage "across the whole realistic spread" (sweep 0 → 0.40).

**The problem.** The 0.12 is **not derived from the data anywhere** — it is the
same number as the default `jitter` argument, re-labelled "measured". The
`jitter` parameter is exactly σ of ln τ for devices at fixed chemistry, so it is
directly measurable. Measured from `DEVICES_DELAYTIME_PIXEL_INFO.csv`, the
device-to-device scatter of ln τ **within a single fixed composition cell**:

| composition cell | n devices | σ(ln τ) |
|---|---|---|
| SY, PEO, LiTr (lead) | 37 | **1.99** |
| SY, TMPE, LiTr | 6 | 4.48 |
| SY, PEO, ImTr | 4 | 2.14 |
| SY, TMPE, ImTr | 4 | 3.98 |
| pooled within-cell (device-level) | — | **2.13** |

So the realised device-to-device scatter is **σ(ln τ) ≈ 2.0**, not 0.12 — a
factor of **~15×**. (Consistent with the library τ spanning P10–P90 ≈ 0.8–27 s,
a ~34× range.) Part of this is pixel noise / un-excluded bad pixels, so 2.0 is an
upper bound; even halved it is ~8× the cited figure.

**Why this is good news, not bad.** The whole Ch5 thesis is "heterogeneity is a
computational resource." The robustness figure already shows the heterogeneous
bank's advantage *grows* with scatter. The data say the real devices are **far
more diverse than the model assumed** — i.e. the heterogeneity resource is
*larger* than claimed and the result was conservative. The current figure
accidentally **understates your own strongest argument** and mislabels a line.

**What to do (low effort, high payoff).**
1. Replace the hardcoded `0.12` "measured scatter" line in `ch5_figures.py`
   with the value computed from `DEVICES_DELAYTIME_PIXEL_INFO.csv` (per-cell
   σ(ln τ)); extend the jitter sweep x-axis past 2.0 so the measured value is
   *on* the plot, and confirm the heterogeneous advantage at the real spread.
2. Add one sentence + the per-cell table above to the Ch5 methods/SI: "the
   device-to-device scatter used is anchored to the measured σ(ln τ)≈2.0."
3. Keep the conservative low-jitter curve too, framed as "even at a fraction of
   the measured spread the advantage holds."
4. Sanity-check the clips in `nodes_from` (α∈[0.05,2], β∈[0.2,2], τ floor): at
   σ=2 a non-trivial fraction of nodes will hit them — make sure the conclusion
   isn't an artifact of clipping, and report what fraction clip.

---

## FINDING 2 — Promote the per-device design map from "Li/PEO spine" to "whole library"

**What exists.** `ch4_comparative_figures.py:fig_design_space` already plots a
per-device map of fading-memory t½ vs potentiation peak ratio — but **filtered to
`cation=="Li"`** and effectively the PEO spine. `fig_heterogeneity` similarly
swarms t½ and α **Li-only, PEO 0.3/0.6/1.2**. Good figures, narrow domain.

**What's untapped.** The same two CSVs plus HYST cover the **full chemistry
palette** — Na/K/Im cations, PEO/TMPE/Hybrane hosts, triflate/TFSI anions — and
a **third, currently-unused axis**: the HYST **memory window** (`on-off ratio
mean`, n=1728 pixels / 204 devices; `normalized area mean`). The design-space map
today uses only PULSES + DELAYTIME; the HYST window is the dimension that most
directly *is* the "memristive switching" the thesis is about, and it is missing
from the map.

**Proposed figure (one panel, high payoff).** A library-wide property map of
every device as a point in (memory window × fading τ), point colour = host,
marker = cation/anion, the lead PEO 0.3/0.09 highlighted. This is the literal
picture of the "heterogeneous palette of timescales and windows" the thesis
argues for — currently asserted in prose and shown only for one corner. n≈81
devices have both axes; 204 have the window axis. Optional third encoding =
potentiation depth (size).

---

## FINDING 3 — Window and retention are weakly coupled (measured, unreported)

Merging device-median HYST `on-off ratio mean` with device-median DELAYTIME τ
(n=81 devices with both): **Spearman ρ = 0.23, p = 0.042** (log–log). A small but
statistically real **positive** coupling — devices with a larger switching window
also tend to retain slightly longer. This matters because the reservoir treats
window (gain) and τ (memory) as independent knobs; the data say they are mildly
correlated, which (a) is honest to report and (b) informs node selection (you
cannot freely pick high-window + ultra-short-τ nodes — they are rare). One
sentence + it falls out of the Finding-2 scatter for free.

---

## FINDING 4 — VCONST relaxation is measured but never featurised (minor)

`DEVICES_VCONST_ALL_DATAPOINTS.csv` is 210 MB of constant-voltage current
transients, but `DEVICES_VCONST_PIXEL_INFO.csv` has **no features** (7 admin
columns). `DEVICES_VCONST_CURVE_INFO.csv` *does* carry relaxation descriptors
(`mean relative rate of change (%/s)`, `min relative rate of change`,
`time at min relative rate of change`, …) — but only for **8 devices / 244
curves**. Constant-voltage current decay is an **independent probe of the same
ionic relaxation timescale** that DELAYTIME measures via Kohlrausch τ. For those
8 devices it could serve as a cheap cross-check ("two independent measurements
agree on the ionic timescale"). **Low priority**: 8 devices is too thin for a
library-wide claim, and the `TASKS.md` extraction work to grow it is out of scope
for the thesis. Flag only.

---

## Checked and rejected (so the audit is trustworthy)

- **Sweep-rate dependence of the hysteresis loop area.** The classic ionic
  signature (loop area ∝ sweep rate) would have given an independent τ. But the
  HYST data has **no real per-pixel rate sweep**: the "distinct" sweep rates are
  numerically-identical duplicates all clustered at ≈0.083 V/s (e.g.
  0.0827083 / 0.0827087 / 0.0827090). Per-pixel area-vs-rate slopes are
  ill-conditioned (range −2e4…+2e4). **Not feasible with current data.**
- **Yield / breakage by composition.** `is broken` and `is saturated` are
  ~all-false in the aggregate CSVs (QC actually lives in the hand-curated
  `FILTERED_DEVICES.csv`), so there is no composition-resolved yield signal to
  mine. **No signal.**

---

## Recommended order of work

1. **Finding 1** first — it is a correctness fix to a headline claim and is
   nearly free (recompute σ(ln τ), relabel the line, extend the x-axis, report
   clip fraction). Highest payoff per hour.
2. **Finding 2** — one new library-wide map figure; reuses existing loaders,
   just drops the `cation=="Li"` filter and adds the HYST window axis.
3. **Finding 3** — one sentence + annotation on the Finding-2 figure.
4. **Finding 4** — note in SI/limitations only.

Touch points: `scripts/ch5_figures.py` (robustness annotation),
`scripts/ch5_reservoir.py` (jitter default / measured anchor),
`scripts/ch4_comparative_figures.py` (`fig_design_space`, drop Li filter, add
window axis). Source CSVs unchanged — this is all re-mining the May-2025 truth.
