# Handout 29 — The Au/TMPE Lock-in Frequency-Sweep Corpus: Decode, Findings, and Thesis Integration

**Date:** 2026-06-12.
**Scripts:** `scripts/lockin_au_tmpe_audit.py` (filename parser, per-file
metrics, QA panels) and `scripts/lockin_au_tmpe_findings.py` (analyses L1–L5).
**Figure:** `scripts/ch4_lockin.py` → `figures/chapter4/lockin_response.pdf`
(thesis Fig. 4.13).
**Outputs:** `handouts/lockin_manifest.csv` (549 rows, one per .txt export),
`handouts/lockin_metrics.csv` (per-file |H|/phase/DC at probe frequencies),
`handouts/lockin_findings_{divider,linearity,gain,gain_pairs,aging}.csv`,
QA panels in `figures/lockin_qa/` (regenerable, git-ignored).
**Status: INTEGRATED** — Ch4 §4.8 paragraph + Fig. 4.13, SI App. C.8
(`app:ch4_lockin`), Ch4 Discussion sentence, Ch4 bounds clause, Ch6
limitations clause + nervetronic-outlook sentence. Thesis builds clean
(267 pp, 0 undefined refs).

---

## 1. What the corpus is

`Nanomem_Devices_Library/Common/Au_TMPE_Li-Na-K_Lock-in-Amplifier_Freq_Sweeps/raw_data`
holds **549 .txt sweeper exports + 439 .hdf5 siblings** from a Zurich
Instruments **MFLI** lock-in, dated 2025-03-04 → 2025-03-26, plus the
experimenter's own tooling at the folder root (`combine_freq.py`,
`freq-filter-dataviz.py` — a Streamlit viewer) whose filename regex and
normalisation define the decode used here.

**Filename schema** (from the included scripts):
`date_chemistry-pixel_config-config_Ndaydeg_frange_capture_offset_ampVpk.txt`,
e.g. `2025-03-07_unkLi2-R4_LP-4nF-noR-config_4daydeg_500k-5kHz_100p-1s_0offset_1Vpk.txt`.

- **Single batch:** `Ndaydeg` = measurement date − **2025-03-03** for all
  549 files → one (top-electrode) fabrication date, tracked days 1–23.
- **Devices:** 3 substrates × ~4 pixels = 12 pixels: `unkLi2`, `unkNa2`,
  `unkK2` (one substrate per triflate salt; L/R pixel naming as standard).
  Not in DEVICES_LIBRARY. Most plausible identity: the **electrode-free
  UV-Vis trio v317–v319** (TMPE-Li/Na/KTr, 2025-02-26, used in Ch4's UV-Vis
  section) with Au evaporated ~2025-03-03, or unlogged siblings. Unproven
  ("unk" = the experimenter's own unknown marker). Same caveat class as
  handout 28's February campaigns.
- **Circuit:** MFLI sweeper drives `offset + amp·sin(2πft)` through the
  junction into a series capacitor to ground; output node read by the
  MFLI 10 MΩ voltage input. Configs: `LP-4nF-noR` (standard, 440 files),
  `LP-0.286…2nF-noR` (capacitor series, K-L5 day 3), `LP-2.5pF-noR`
  (no external cap, days 1–2, all chemistries, 0 offset).
- **Sweeps descend** 500 kHz → 1 Hz in three captures (500k–5kHz 100 pts,
  5k–200Hz 97 pts, 200–1Hz 200 pts; ~1 s/pt). **The 110 "500k-1Hz_400p-1s"
  files are DERIVED** — outputs of `combine_freq.py` (400 = 101+98+201
  summed capture ints; frequency-sorted so the timer runs backwards).
  Excluded from all statistics (they double-count); fine for plotting.
- **Channel decode** (verified in the hdf5): Demod 4 = output voltage at
  the drive frequency (the analysis backbone; `|H| = Demod4_R/(amp/√2)`,
  the corpus' own normalisation). Demod 2 = same signal through a second
  demod filter (mislabeled "(A)" in the txt export; equals Demod 4 at
  mid/high f, diverges at low f). Demod 3 = DC monitor of the output node
  (R = |DC|, sign in theta ±90°). Demod 1 = auxiliary current channel
  (~constant ≈350 nA at −90°), unused.
- **Protocol per day:** d1–2: 2.5pF config amplitude series (0.5–2.4 Vpk,
  0 offset). d3: 4nF 0-offset amplitude series ×3 K/Na pixels + capacitor
  series on K-L5. d4: ±1.4 V offset @ 1.4 Vpk (large-signal, drive touches
  0) on 9 pixels (+ 0-offset series Li/Na). d9/10: ±2.0 @ 0.8 and
  ±2.4 @ 0.4 Vpk (small-signal at strong bias; K/Na d9, Li d10). d23:
  unkLi2-L3 **11-point offset series** −2.5…+2.5 V step 0.5 @ 0.25 Vpk.
  Offset designs hold |offset|+amp = 2.8 V (matched peak). The day-23
  series was measured 0→+2.5 then −0.5→−2.5 (timer-verified); the
  later-measured negative branch is not elevated → symmetry is not drift.

## 2. Findings (all in `lockin_findings_*.csv`)

**L1 — divider validation.** K-L5 d3, C_ext = 0.286…4 nF at 10 kHz:
implied C_dev = C_ext·H/(1−H) stays 1.4–2.9 nF (median 2.35) — topology
and normalisation validated at factor level. Residual monotone trend of
C_dev with C_ext = lossy/CPE dielectric, as expected.

**L2 — passive band is linear.** Zero offset, f ≳ 10 Hz: plateau |H| at
1k/10 kHz varies by median **0.17–0.29 %** (max 8 %) across 0.5–2.4 Vpk —
the memristive nonlinearity is *absent* above the ionic band, the
frequency-domain counterpart of handout 28's F2 (rate-gated window).
C_dev @1 kHz: Li 2.32, Na 2.93, K 3.19 nF (substrate-confounded; ≈28–39
nF/cm² at 0.0825 cm²; ≈150–290 nm at εr 5–10 — plausible for 3000 rpm).
**Within-substrate pixel spread ≈1 %.**

**L3 — bias-activated low-frequency gain (the headline).** Day-23 series
(unkLi2-L3, 0.25 Vpk): |H| at 1–2 Hz rises **monotonically** with |offset|
from 0.49 (0 V) to **17.9 (+2.5 V) / 16.7 (−2.5 V)**, while |H|@10 Hz ≈ 1
and the ≥1 kHz plateau is offset-insensitive (0.422 vs 0.423). Population
(200–1Hz captures): median H₂ = 0.46 (0 V, n=46, 7 % >1), 1.25 (±1.4,
n=18, 72 % >1), 2.78 (±2.0, n=20), 6.69 (±2.4, n=18, 100 % >1), 17.3
(±2.5, n=2). 200 Hz boundary point repeats to median 1.2 % (n=95).
**|H|>1 at the fundamental is impossible for a passive divider into a
passive load** → the biased junction is an *active mixer*: the drive
slowly modulates the ionic conductance, which mixes the DC bias up to the
fundamental (bias powers the gain). Robust to the demod amplitude
convention (worst-case √2 → 18 becomes 13). **Polarity near-symmetric:**
n=32 matched ± pairs, median H₂(+)/H₂(−) = 1.11, Wilcoxon p = 0.013 —
weak positive excess, opposite in sign and far weaker than the DC
potentiation asymmetry (F1) → gain responds to |bias|·(modulation depth),
not to the potentiation direction. Gain band: H>2 below ~6 Hz, unity by
~10–50 Hz — coincides with the ionic/fading-memory band.

**L4 — ageing.** Plateau within pixel: K 0.444→0.450/0.451 (d3→9), Na ±2 %
(d3→9), Li +≈15 % (d4 0.35–0.37 → d10 ≈0.42; L3 d10 0.376 → d23 0.390).
One deviation: K-L5 d4 plateau 0.55 at −17…−21° phase = **conditioned
(potentiated) state** (it was the capacitor-series workhorse on d3), not
an artefact; excluded from plateau stats. Gain present at every age with
offsets (d4–23) but protocols differ per session → no matched ageing
comparison of gain. Zero-offset low-f H₂ too noisy/non-stationary for
ageing claims.

**L5 — DC monitor.** DC out tracks offset linearly in magnitude & sign
(day-23: ≈1.4× offset in export convention) → biased junction conducts
≪10 MΩ (~MΩ scale), same order as handout 28's constant-bias end states
(e.g. −2 V VCONST → ~µA). At 0 offset: median −0.18 V, 61 % negative,
binomial p = 0.18 (ns) — no significant self-rectification claimed.

**L6 — thickness bounding for the cation-ordered capacitance (added
2026-06-12, user-directed upgrade).** The C_dev ordering K 3.19 > Na 2.93 >
Li 2.32 nF (1.4× span ≫ 1 % pixel spread, same-batch trio) was initially
left unassigned (substrate ⟂ salt). The user argued — correctly — that the
thesis already reports n=1–2 host/anion orderings at the illustrative tier,
that the trio is same-batch, and that archive profilometry can bound the
thickness channel. `DEVICES_PROFILOMETRY_STATS.csv` at the matched recipe
(TMPE 0.3/salt 0.09/3000 rpm) shows: same-day cation trios differ
**6–12 %** in thickness (2024-10-29: Li 153/K 162 nm — K *thicker*, the
wrong direction to produce C_K > C_Li; 2025-05-14 TFSI trio: span 6 %),
while explaining the C span by thickness alone needs Li ≈ **37 %** thicker.
Same-salt solution-to-solution scatter does reach ~30 % (10/03 Li sextet),
so thickness is not excluded, merely unprecedented in cation-correlated
form. **Upgraded to a *candidate* dielectric cation effect** (εr rising
Li→K, the direction weaker coordination suggests; the one cation-ordered
observable in the archive — ATR/UV-Vis/dynamics all null, but those probe
different physics, no contradiction). Decisive test: profilometry on the
three substrates (they still exist). The **gain-magnitude ordering stays
unclaimed** (conditioning shifts >20 % demonstrated; sessions differ by
day/protocol). → `handouts/lockin_findings_thickness.csv`.

## 3. What was NOT claimed (and why)

- **No demonstrated cation effect**: the capacitance ordering is recorded
  at *candidate* tier only (see L6; substrate ⟂ salt at n=1 each); the
  gain-magnitude ordering is not claimed at all (state/session confounds).
- **No "gain aging" trend**: offset–amplitude protocol changed between
  sessions (±1.4@1.4 d4 → ±2.0/2.4@0.8/0.4 d9/10 → ±0.25Vpk series d23).
- **No self-oscillation claim**: demod-only data can't distinguish strong
  self-mixing from injection-locked relaxation oscillation; the smooth
  monotone bias dependence + absence of NDR in the DC corpus favours
  mixing; text says "active element / mixes the bias up to the
  fundamental".
- **Day-4 large-signal weirdness** (e.g. Li-R4 2 Hz: 0.07 at −1.4 vs 1.85
  at +1.4, then both >1 at 1 Hz): drive crosses 0 V and the state evolves
  mid-sweep; left in the CSVs, not used for headline claims (the matched
  pairs include d4 → that's the conservative direction).
- **2.5pF (device-alone) files**: decoded (plateau ≈0.9 vs 10 MΩ input;
  roll-off + amplitude-dependence below ~20 Hz) but not separately
  integrated — the 4nF corpus carries all thesis claims.
- 50 Hz mains glitch noted; probe frequencies avoid it.

## 4. Thesis integration (done, commits 1d4d59e + 21e3b29 + this)

- **Ch4 §4.8** new ¶ "The frequency-domain face: a bias-programmed
  low-frequency amplifier" + **Fig. 4.13** (`lockin_response.pdf`:
  (a) day-23 |H|(f) family; (b) bias–gain curve + per-cation medians).
- **Ch4 §4.8 bounds ¶**: lock-in bounds clause (one batch, substrate-
  confounded cations, conditioned states, inferred identities).
- **Ch4 Discussion**: spectral-boundary sentence (nonlinearity absent >10
  Hz, switchable/dialable by bias below).
- **SI App. C.8** (`app:ch4_lockin`): provenance, decode, L1–L5 with
  Table C.8 (day-23 series), bounds. Cross-refs C.7 (`app:ch4_gold_
  dynamics`) and `fig:ch4_uvvis`.
- **Ch6**: limitations item extended (frequency-domain sibling caveat);
  nervetronic outlook sentence (programmable sub-10 Hz pre-amplifier =
  single-device front-end); "Power the chemistry landscape" extended with
  the candidate capacitance ordering as a concrete target for the
  replicated cation series (2026-06-12).
- **2026-06-12 upgrade**: Ch4 §4.8 ¶ gains the candidate-ordering sentence;
  SI C.8 gains "A candidate cation-ordered capacitance" paragraph (with the
  L6 profilometry bounding) and the εr estimate tightened to ≈5–7 at the
  150–190 nm sibling thicknesses.
- **Ch5**: untouched (its gold-corpus mentions concern the drive–retention
  coupling, which the lock-in does not parameterise).

## 5. Caveats register (for whoever revisits)

- Substrate identity inferred (v317–319 + Au @ 2025-03-03 hypothesis);
  `daydeg` self-consistent but its zero point is the inferred evaporation
  date, not a logged event.
- Demod amplitude convention (possible global √2) affects absolute |H|,
  C_dev, and DC slope only; all ratios/symmetry/trends are convention-free.
- Low-frequency points are conditioned steady states (descending sweeps:
  minutes under offset before the 1–2 Hz points) — by design, also why
  they're reproducible; do not read them as pristine-state responses.
- Demod 3 identified as DC monitor behaviourally (sign in theta, scale
  tracks offset), not from a saved instrument config.
- `lockin_findings_gain_pairs.csv` pairs medians within (dev, day,
  |offset|, amp); d4 pairs are large-signal and noisier.

## 6. Leads deliberately left on the table

- Phase-resolved analysis (Demod 4 theta) of the gain band → mixing-model
  fit (G₀, G₁, lag) could turn "active mixer" into a fitted mechanism.
- The 2.5pF device-alone impedance + amplitude-onset series (days 1–2) —
  could yield |Z_dev|(f) and a nonlinearity-onset voltage per cation.
- The hdf5 siblings may hold instrument settings (demod TCs, input ranges)
  that would pin the conventions; the two inspected hold only Data tables.
- Harmonic content: no harmonics were exported (demods all at the drive
  frequency); a re-measurement with 2f/3f demods would quantify distortion
  vs bias — the natural follow-up experiment.
