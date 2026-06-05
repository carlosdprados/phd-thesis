# Handout 16 — IR-ATR (ATR-FTIR) dataset: assessment for Chapter 3

**Date:** 2026-06-05
**Script:** `scripts/ch3_iratr.py` · **Band table:** `handouts/ch3_iratr_bands.csv`
**Chapter figure:** `figures/chapter3/iratr_chemistry.pdf` (combined, used in §3.5).
**Exploratory figures:** `…/iratr_fingerprint.pdf`, `…/iratr_triflate_nsSO3.pdf`,
`…/iratr_host_crystallinity.pdf`

**STATUS (2026-06-05): integrated.** Folded into §3.5 (chemistry landscape) per the
recommendation below — intro sentence + one combined figure `fig:ch3_iratr`; the
ν_s(SO₃)/cation-null added to the cation paragraph, the PEO/TMPE crystallinity contrast to
the host paragraph, and a corroboration clause to the §3.7 mechanistic discussion. Humidity
set excluded. Chapter builds clean.

## 1. What the data is

ATR-FTIR (attenuated-total-reflectance Fourier-transform IR) spectra archived under
`DEVICES_LAB_DATA` for **spectroscopy-only samples v126–v139** — films or scratched
powders of the SY / polyether / metal-triflate blend, **no top electrode** (`Used Metal`
blank in the library). All at the **lead composition cell** (ion-polymer mass ratio 0.3,
salt 0.09). Raw instrument files are Bruker OPUS (ATR Platinum Diamond, dated 29/09/2022 &
21/10/2022, H₂O-vapour compensation on). Each spectrum is a 2-column table
(wavenumber cm⁻¹, **transmittance-like** single-beam ratio) in `.csv` (comma) / `.dpt`
(tab); the no-extension file is the raw OPUS binary. `corr`/`corrfin` = atmospheric +
baseline corrected (OPUS), but **inconsistent** across batch-3 samples (several distorted).

Three sub-datasets:

| Set | Devices | Design | Sampling | Status |
|-----|---------|--------|----------|--------|
| **A. Host × cation** | v126–v131 | PEO/TMPE × Li/Na/K, all triflate, 0.3/0.09 | mixed film/powder | usable, illustrative |
| **B. PEO vs TMPE Li repeat** | v132/v133 | host contrast at Li | powder | usable, illustrative |
| **C. Humidity** | v134–v139 | PEO/Li glovebox vs ambient-2h | film | **inconclusive — excluded** |

Marker `.txt` files (blank, name = note): `Film*` / `Powder*` record the sampling mode.
Chemistry confirmed against `UPDATED_DEVICES_LIBRARY.csv` (all SY, 0.3/0.09; v130 salt 0.10).

## 2. Findings

**(1) Constituents confirmed.** Triflate bands — δ_s(CF₃) ~752–759, ν_s(SO₃) ~1030,
ν_s(CF₃) ~1226, ν_as(SO₃) ~1270 — and the polyether C–O–C envelope appear in **every**
chemistry. The salt and ion-transport polymer are present and intact in the SY blend.
(Intensities are **not** comparable across samples — film vs powder contact differs.)

**(2) Cation: no clean ion-association ordering (corroborates the chapter).**
The diagnostic ν_s(SO₃) "ion-association" band sits at **~1029–1032 cm⁻¹ in all six
host×cation samples** (free-ion / contact-ion-pair boundary; free≈1032, CIP≈1042,
aggregate≈1052). Spread ≤3 cm⁻¹ — at/below instrument resolution, and **not ordered by
cation**. → Microscopically consistent with the chapter's honest conclusion that the
**cation is not a clean, transferable lever** on the dynamics. The δ_s(CF₃) band hints Li
(~759) sits above Na/K (~752) but its height is ≈noise (n=1); not relied upon.

**(3) Host structural contrast (supporting, weaker).** In the **film pair** (v126 PEO vs
v129 TMPE, Li) the C–O–C envelope (1040–1170) is a **resolved multiplet** for linear PEO
(local maxima ~1122 & 1139 cm⁻¹ — *local conformational* order) but a **single broad band**
for hyperbranched TMPE (~1138 — amorphous). **CORRECTED (see handout 17 / XRD):** read this as
*local/conformational* order, NOT "semicrystalline" — XRD shows the composite is X-ray
amorphous (no bulk PEO crystallites). Chapter wording updated accordingly. This is the expected crystalline-vs-amorphous
host difference and plausibly underlies the host effect on relaxation (amorphous TMPE →
higher segmental mobility → faster ionic relaxation → ~6× shorter t₁/₂, as measured §3.5).
**Caveats:** the contrast is subtle and partly confounded by the overlapping ν_s(SO₃) band,
by film-vs-powder sampling, and by contact-dependent intensity; the **powder repeat**
(v132/v133) does **not** separate the hosts cleanly. n=1 per host.

**(4) Humidity series — honest NULL, excluded.** Batch-3 films differ wildly in ATR
contact (1030-band depth 0.0–0.81), the broad O-H water band is ≤0.05 transmittance dip and
**not** ordered by glovebox vs ambient (one glovebox and one ambient film both show ~0.81
contact and no water; only v135 shows a ~0.04 O-H dip). Film-contact variation dominates;
water uptake **cannot** be compared. Do **not** use to support the hygroscopy/glovebox
claim.

## 3. Soundness

- **Real, well-provenanced data**; assignments are standard (triflate + PEO literature).
- **Strictly illustrative tier**: n=1 per chemistry, mixed film/powder, no peak
  deconvolution, ATR penetration-depth (∝λ) not corrected, band shifts near resolution.
- Same evidential tier as the chemistry landscape (§3.5) and EIS (§3.7) — **corroborative,
  not quantitative**. Magnitudes/positions are indicative; no statistical power.

## 4. Recommendation

**Include as a short, explicitly-illustrative paragraph/subsection**, paralleling the EIS
section but more hedged. Best scientific value:
- **Headline:** ν_s(SO₃) ≈ 1030 cm⁻¹ in all chemistries with no cation-resolved shift →
  independent microscopic support that the **cation is not a clean lever** (reinforces the
  chapter's most counter-intuitive, honest claim — the HSAB hypothesis is not borne out).
- **Secondary:** the PEO-crystalline / TMPE-amorphous structural contrast as a *cautious*
  microscopic correlate of the host effect.
- **Constituent confirmation** as a one-line baseline.
- **Do NOT** claim water uptake / humidity from set C.

Slot: either a 2-paragraph subsection §3.8 "Microscopic corroboration II: vibrational
spectroscopy" after EIS, or fold finding (2) into the cation paragraph of §3.5 and (3) into
the host paragraph, with one figure. EIS corroborates the **composition** axis; IR-ATR
corroborates the **chemistry** axis — they are complementary.
