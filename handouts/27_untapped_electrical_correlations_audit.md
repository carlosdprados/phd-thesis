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

> **Confound update (2026-06-10, same day).** Every finding was re-checked against
> fabrication/experimental covariates (composition mass ratios, RPM, anneal,
> film thickness, metal, aging/day). Two findings changed materially: Finding 1's
> magnitude was over-stated (my first pass conflated the *designed* PEO×salt sweep
> with random scatter — corrected below), and **Finding 3 is retracted** (the
> window↔τ correlation is entirely composition-mediated). See the *Confound check*
> section before each finding. Net: Findings 1 (corrected), 2, 4 proceed; 3 retracted.

---

## TL;DR — what's worth doing

| # | Finding | Payoff | Effort |
|---|---------|--------|--------|
| 1 | The "measured device-to-device scatter ≈ 0.12" that the Ch5 robustness claim cites is **never derived from data**; the confound-checked value is σ(ln τ) ≈ **0.85** (~7× larger). | **High** — fixes a viva-exposed factual gap *and* strengthens the heterogeneity-as-resource thesis | Low |
| 2 | A library-wide **dynamical property map** exists in the data but is shown only for the Li/PEO spine; extend it to the **HYST window axis** and the **full chemistry palette**. | High — visually grounds the "heterogeneous palette" for the whole library | Low–Med |
| ~~3~~ | ~~window↔τ coupling~~ **RETRACTED** — the apparent ρ=0.23 is composition-mediated and vanishes at fixed composition (ρ=0.03, p=0.79). | Reframed as: window & τ are *independent* knobs at fixed composition (validates the reservoir model) | — |
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
`jitter` parameter is exactly σ of ln τ for devices **at fixed composition**, so
it is directly measurable from `DEVICES_DELAYTIME_PIXEL_INFO.csv`.

**Confound check (this is the important part).** A first naive estimate grouped
only by the qualitative *Components Group* "SY, PEO, LiTr" and gave σ(ln τ)≈2.0 —
**but that pools the deliberate PEO×salt mass-ratio sweep** (the comparative
chapter's whole tuning axis) as if it were random scatter. That is exactly the
confound the supervisor warned about. Decomposing properly (Ag only, n=31 lead-cell
devices, device-median ln τ):

| level | σ(ln τ) | what it contains |
|---|---|---|
| total within "SY,PEO,LiTr" group | 1.59 | **inflated** — includes designed PEO×salt tuning |
| within **exact (PEO, salt) cell** | **0.85** | genuine device-to-device scatter (cells ≥3 dev, n=27) |
| + control RPM & anneal (OLS resid) | 0.91 | RPM/anneal add ~nothing |
| residual vs **thickness** | ρ=0.07, p=0.70 | thickness does **not** explain it |
| residual vs **aging/day** | ρ=−0.05, p=0.80 | aging does **not** explain it (day range 1–13) |

So the **confound-checked device-to-device scatter is σ(ln τ) ≈ 0.85**, not 0.12
(still ~7×) and not the conflated 2.0. It is genuine: unexplained by composition,
RPM, anneal, film thickness, or aging. Thickness coverage is complete (31/31).

**The claim still holds at the measured value.** Running the reservoir's own
`mc_curve_seeded` at the measured jitter (verified 2026-06-10): the heterogeneous
bank still wins at σ=0.85 (total MC 6.11 vs homogeneous 5.19, **+0.92**; cf.
+2.23 at the old 0.12). The advantage shrinks but stays clearly positive across
0 → 1.0 — so correcting the number *strengthens honesty without breaking the
result*, and shows the devices are more diverse than the model assumed.

**What to do (low effort, high payoff).**
1. `scripts/ch5_scatter_audit.py` recomputes σ(ln τ)≈0.85 with the controls above
   and writes it to `handouts/ch5_scatter_audit.csv` (single source of truth).
2. `fig_robustness` in `ch5_figures.py`: extend jitter sweep to ≥1.0, replace the
   hardcoded 0.12 "measured scatter" line with the audited value, fix the label.
3. Quantify the scatter in `chapter4_comparative.tex` ("device-to-device scatter
   within each cell is substantial") and update the `chapter5_temporal.tex`
   robustness caption/text to state the measured σ≈0.85 and that the advantage
   holds there.
4. (Optional) report the fraction of nodes hitting the `nodes_from` clips
   (α∈[0.05,2], β∈[0.2,2], τ floor) at the measured jitter, for completeness.

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

## FINDING 3 — Window↔τ coupling — **RETRACTED after confound check**

Initial observation: device-median HYST `on-off ratio mean` vs device-median
DELAYTIME τ correlated at **ρ = 0.23, p = 0.042** (n=81, log–log), and *more*
strongly within the SY/PEO/LiTr/Ag spine (ρ = 0.39, p = 0.030, n=31).

**Confound check kills it as a device-level relationship.** Both window and τ
co-vary along the *designed* PEO×salt composition axis, so the raw correlation is
composition-mediated. Partialling out composition cell + chemistry (per-device
residuals): **ρ = 0.03, p = 0.79** (n=76); adding film thickness: ρ = 0.08,
p = 0.53 (n=71). The coupling is an artefact of the composition design grid.

**Reframed (and useful):** at *fixed* composition, switching window and fading-τ
are statistically **independent**. That is exactly the assumption the reservoir
model makes (τ, α, window jittered independently in `nodes_from`), so this is a
small *validation* of the model, not a new trade-off to exploit. Worth one honest
sentence in the Ch5 model/SI; no new figure or claim.

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

1. **Finding 1** first — correctness fix to a headline claim, nearly free
   (audit script for σ(ln τ)≈0.85, relabel the line, extend the x-axis).
   Highest payoff per hour. **Confound-checked; survives.**
2. **Finding 2** — one new library-wide map figure; reuses existing loaders,
   just drops the `cation=="Li"` filter and adds the HYST window axis. Organise
   by composition (the dominant axis) so it is read as a palette, not a trade-off.
3. ~~**Finding 3**~~ — retracted; fold the one-line independence note into the
   Ch5 model/SI if convenient.
4. **Finding 4** — note in SI/limitations only.

**Implementation status (2026-06-10):** Findings 1 & 2 implemented in this pass;
3 retracted; 4 left as a note. See commits referencing handout 27.

Touch points: `scripts/ch5_figures.py` (robustness annotation),
`scripts/ch5_reservoir.py` (jitter default / measured anchor),
`scripts/ch4_comparative_figures.py` (`fig_design_space`, drop Li filter, add
window axis). Source CSVs unchanged — this is all re-mining the May-2025 truth.
