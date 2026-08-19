<!-- markdownlint-disable-file MD013 -->

# Thickness / Spin-Coat-RPM Covariate Audit — Chapters 4 & 5

**Author:** Carlos David Prado-Socorro · **Updated:** 2026-08-19 · **Status:** composition association persists; secondary thickness contribution not excluded.
**Reproduce:** `MPLCONFIGDIR=tmp/matplotlib python scripts/thickness_rpm_audit.py` (prints the statistics below and regenerates `figures/chapter4/thickness_control.pdf`).
**Companion:** the broader claims ledger [`08_chapter3_4_claims_audit.md`](08_chapter3_4_claims_audit.md).

---

## 0. The question

Devices were spin-coated at different RPM. Crucially, RPM was sometimes — **but not for every comparison batch** — raised for higher PEO/LiTr concentrations, deliberately, to thin the otherwise-thicker film and partially equalise thickness across the composition grid. **Source of truth for thickness = `DATABASE/DEVICES_PROFILOMETRY_STATS.csv` (nm).**

So: could the Chapter-4 composition associations (higher PEO → smaller switching window, lower potentiation exponent α, shorter fading-memory time) instead be partly a thickness effect? This audit treats thickness as a measured covariate. It can test whether the composition association persists after statistical adjustment; it cannot prove that thickness has no secondary effect.

## 1. Method

The script joins **33 substrates** represented in `ch4_decay_fits.csv` and `ch4_pulse_descriptors.csv` to:

- **composition** (PEO/SY and salt/SY mass ratios) and **spin RPM** — `DATABASE/DEVICES_LIBRARY.csv` (`Spin Coating Rotational Speed [RPM]`);
- **film thickness** — `DEVICES_PROFILOMETRY_STATS.csv` (`avg_thickness (nm)`, per-substrate mean over profilometry rows);
- **dynamics metrics** — `t½`, identified `τ`, `β` (decay), growth exponent `α`, peak ratio (pulses).

Junction measurements are collapsed to a substrate median first. Statistics are restricted to the replicated **Li/Ag grid** (`PEO/SY = 0.3, 0.6, 1.2`; `salt/SY = 0.045, 0.09, 0.18`). Of its **28 substrates** with profilometry, 23 have `t½` and 27 have pulse descriptors. Correlations are Pearson and tie-aware Spearman; complementary partial correlations test the measured-covariate sensitivity.

## 2. Composition and thickness covary

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

`PEO → thickness`: **Pearson +0.65, Spearman +0.68** (n=28). PEO and thickness genuinely covary (+31% median thickness from PEO 0.3 to 1.2), so thickness cannot be described as perfectly matched or fully controlled.

## 3. Measured-covariate results

| Correlation (Li/Ag spine) | Pearson | n |
|---|---|---|
| PEO → log₁₀(t½) | **−0.46** | 23 |
| thickness → log₁₀(t½) | −0.14 | 23 |
| PEO → growth exponent α | **−0.58** | 27 |
| thickness → α | −0.24 | 27 |
| PEO → log₁₀(peak ratio) | **−0.57** | 27 |
| thickness → log₁₀(peak ratio) | −0.17 | 27 |

**Partial correlations (n=23):**
- `r(thickness, log t½ | PEO) = +0.28`.
- `r(PEO, log t½ | thickness) = −0.51`.

The second result supports the bounded chapter statement: the negative composition–timescale association persists after adjustment for measured thickness. The first is not zero and, together with the sample size and non-random fabrication design, prevents a claim that thickness is irrelevant.

Supporting evidence:

1. **Lead anchor cell PEO 0.3 / 0.09** (the Ch4 lead composition): thickness **196 → 271 nm (38% spread)** yet t½ is flat at **18.5 / 22.0 / 19.2 s**. A large thickness swing inside one composition moves the memory not at all.
2. **Activation voltage has no resolved linear thickness trend** (`r ≈ −0.06`) across a 2.6× thickness range. This disfavors simple inverse-thickness threshold scaling; it does not prove an intrinsic ionic/electrochemical threshold.
3. **Conductance ratios reduce sensitivity to absolute geometry**, but timescales and nonlinear pulse descriptors need not cancel thickness. They remain empirical observables requiring the direct audit above.

## 4. Verdict

- **Composition association:** supported. PEO remains associated with `t½` after adjustment for measured thickness, and pulse descriptors correlate more strongly with PEO than with thickness.
- **Thickness exclusion:** not supported. The design is observational, PEO and thickness covary, and a secondary thickness contribution remains possible.
- **Salt interpretation:** evaluated separately through turnover and the batch-adjusted factorial model; this audit does not establish an independent salt mechanism.
- **Chapter 5 parameters:** must use measured substrate variability and sensitivity analyses. This audit does not justify declaring all simulations unaffected.

## 5. What changed in the thesis

The thesis now states the bounded conclusion supported by the audit:

- **Ch4** §Materials: thickness is a measured covariate; it does not account for the composition association, but a secondary contribution is not excluded.
- **Ch5**: variability and sensitivity analyses must not assume that the composition mapping is deterministic.
- **This handout** + the committed `scripts/thickness_rpm_audit.py` (reproducible).
