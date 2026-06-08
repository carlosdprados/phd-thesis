<!-- markdownlint-disable-file MD013 -->

# Thickness / Spin-Coat-RPM Confound Audit — Chapters 3 & 4

**Author:** Carlos David Prado-Socorro · **Date:** 2026-06-04 · **Status:** resolved — claims stand.
**Reproduce:** `python3 scripts/thickness_rpm_audit.py` (prints the table below + regenerates `figures/chapter4/thickness_control.pdf`).
**Companion:** the broader claims ledger [`08_chapter3_4_claims_audit.md`](08_chapter3_4_claims_audit.md), which controlled protocol amplitude (§13), electrode Ag/Au (§16), and aging — but **not** film thickness. This handout closes that gap.

---

## 0. The question

Devices were spin-coated at different RPM. Crucially, RPM was sometimes — **but not for every comparison batch** — raised for higher PEO/LiTr concentrations, deliberately, to thin the otherwise-thicker film and partially equalise thickness across the composition grid. **Source of truth for thickness = `DATABASE/DEVICES_PROFILOMETRY_STATS.csv` (nm).**

So: are the Chapter-4 composition claims (higher PEO → smaller switching window, lower potentiation exponent α, shorter fading-memory time) and the Chapter-5 parameter cards / simulations **contaminated** by this deliberate thickness tuning, i.e. is "PEO effect" partly a "thickness effect"?

## 1. Method

For all **32** devices in the Ch3/Ch4 quantitative spine (the ones in `ch4_decay_fits.csv` + `ch4_pulse_descriptors.csv`), joined per device:

- **composition** (PEO, salt mass fraction) and **spin RPM** — `DATABASE/DEVICES_LIBRARY.csv` (`Spin Coating Rotational Speed [RPM]`);
- **film thickness** — `DEVICES_PROFILOMETRY_STATS.csv` (`avg_thickness (nm)`, per-device mean over profilometry rows);
- **dynamics metrics** — `t½`, identified `τ`, `β` (decay), growth exponent `α`, peak ratio (pulses).

Stats restricted to the **Li / Ag composition spine (n = 30)** — the only replicated quantitative axis (handout 08 §16). Correlations are Pearson + Spearman; the decisive test is the **partial correlation** of thickness vs dynamics controlling for PEO.

## 2. The confound is real at the fabrication level (as suspected)

**RPM was escalated with PEO, but not uniformly** — confirming "adjusted, but not for every batch":

| PEO | spin RPM seen in spine |
|---|---|
| 0.15 | 1500, 2050 |
| 0.3 | 1500, 1950, 2000, 2100, 2400 |
| 0.6 | 2000, 2100, 2350, 2600, 2700, 2900 |
| 1.2 | 2000, 2900, 3000, 3350, 3400, 3500 |

(e.g. batch v141–v145 held **2000 rpm fixed** across PEO 0.3→1.2 — no compensation; batches v150–157, v241–264 ramped RPM with PEO — compensation.)

**Compensation was incomplete** — residual thickness still climbs with PEO:

| PEO | thickness median (nm) | range | n |
|---|---|---|---|
| 0.3 | 227 | 196–271 | 10 |
| 0.6 | 248 | 151–325 | 9 |
| 1.2 | 298 | 272–392 | 9 |

`PEO → thickness`: **Pearson +0.68, Spearman +0.72** (n=30). PEO and thickness genuinely covary (+31% median thickness from PEO 0.3 to 1.2). So the question is legitimate.

## 3. But thickness is *not* the driver — five independent lines

| Correlation (Li/Ag spine) | Pearson | n |
|---|---|---|
| PEO → log₁₀(t½) | **−0.51** | 25 |
| thickness → log₁₀(t½) | −0.31 | 25 |
| PEO → growth exponent α | **−0.44** | 28 |
| thickness → α | −0.14 | 28 |
| PEO → log₁₀(peak ratio) | **−0.43** | 28 |
| thickness → peak ratio | −0.08 | 28 |

**Partial correlations (decisive):**
- `r(thickness, log t½ | PEO) = +0.05` (n=25) → **once composition is fixed, thickness explains essentially nothing.**
- `r(PEO, log t½ | thickness) = −0.42` (n=25) → **the composition effect survives controlling for thickness.**

The raw thickness↔dynamics correlation is entirely *mediated* by PEO; thickness is a downstream consequence of how much ion-transport polymer is in the film, not an independent cause.

Supporting evidence:

1. **Lead anchor cell PEO 0.3 / 0.09** (the Ch4 lead composition): thickness **196 → 271 nm (38% spread)** yet t½ is flat at **18.5 / 22.0 / 19.2 s**. A large thickness swing inside one composition moves the memory not at all.
2. **Within-cell pooled** (center thickness & log t½ per cell, then pool, n=24/8 cells): r = −0.25 — much weaker than the cross-PEO −0.51, and near-zero after the partial.
3. **Metrics are dimensionless** (on–off *ratio*, log–log *slope* α, *timescale* t½/τ, β): a pure series-resistance / geometry effect of thickness cancels.
4. **Activation voltage is flat** (2.17–2.56 V; `thickness → activation V` r = **−0.06**) across a **2.6× thickness range (151–392 nm)**. If switching were a bulk-field (V/thickness) effect, the threshold would scale with thickness. It does not → the threshold is an intrinsic ionic/electrochemical property, ruling out the main mechanism by which thickness *could* matter.
5. **Sign is wrong for a thickness mechanism:** thicker films show *shorter* memory; a longer ionic transit path would predict *longer* retention. Only an ion-transport-fraction driver explains the observed direction.

## 4. Verdict

- **Composition claims (Ch3 quantitative spine): STAND.** Thickness is a **controlled covariate, not a confound.**
- **Salt axis: STANDS.** salt → thickness weak (+0.31); the salt claim is about turnover/dynamic range, composition-intrinsic.
- **Parameters & simulations (Ch4): UNCHANGED.** Parameter cards are per-cell composition aggregates; the composition→dynamics mapping is intact. MC 4.10→6.12 (1.49×), the WESAD numbers, and the physiological-context results are unaffected.
- **Chemistry axis (illustrative/null): one minor note.** The K device v249 happens to be thin (164 nm); since the cation result is already an honest null, no claim rests on it.

## 5. What changed in the thesis

No values, parameter cards, or simulations were re-computed (the audit shows none should). Added for **transparency** so the question is answered on the record:

- **Ch4** §Materials: a "thickness is controlled, not confounding" paragraph + the supplementary figure `fig:ch4_thickness_control` (`figures/chapter4/thickness_control.pdf`).
- **Ch5** §Limitations: one sentence cross-referencing the Ch4 thickness control.
- **This handout** + the committed `scripts/thickness_rpm_audit.py` (reproducible).
