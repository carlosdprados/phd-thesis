# Handout 18 — UV-Vis dataset: assessment for Chapter 4

**Date:** 2026-06-05 · **Script:** `scripts/ch4_uvvis.py` · **Figure:** `figures/chapter4/uvvis_bandedge.pdf`

## 1. What the data is

JASCO UV-Vis absorbance on 2025 **TMPE-host** blend films v317–v320 (SY/TMPE/metal-triflate,
lead cell 0.3/0.09, **Au** generation, "newmixing"): a Li/Na/K cation series + a salt-free
control. All four contain SY (confirmed in `UPDATED_DEVICES_LIBRARY.csv`).

- v317 SY/TMPE/Li · v318 SY/TMPE/Na · v319 SY/TMPE/K · v320 SY/TMPE (no salt)
- Files: `<ion>_View*.csv` = raw **absorbance vs nm**; `<ion>_conv*.csv` = **converted
  Kubelka–Munk vs energy [eV]** (Tauc/band-gap form). JASCO export: `;`-delimited, comma
  decimal, header + `XYDATA`.

## 2. Finding — SY band edge is invariant to the cation

SY π–π* absorption peak and 50 %-onset:

| | peak (nm) | onset (nm / eV) |
|---|---|---|
| Li | 445 | 495 / 2.50 |
| Na | 446 | 496 / 2.50 |
| K  | 446 | 496 / 2.50 |
| no salt | 448 | 508 / 2.44 |

**Li/Na/K are identical** (peak 445–446 nm, onset 2.50 eV) — the cation does **not** perturb
the semiconductor's optical/electronic structure. The salt-free control matches on the red
(band-edge) side; its slightly different blue side and low absorbance (A≈0.29 vs ≈1.0) are
thickness/scattering, not electronic. No new sub-gap / charge-transfer band from any salt.

**Caveats:** n=1 per chemistry; **different generation** from the ATR/XRD set (Au, 2025,
TMPE-only, newmixing) — it speaks to SY electronic structure *generally*, not the exact
v126–133 specimens; absorbance magnitudes are thickness-confounded (only peak/onset
**positions** are read); deep-UV (<280 nm) baseline is unreliable. Illustrative tier.

## 3. Does it add to the ATR + XRD story?

**Yes — it is the electronic-structure leg of the microscopic triad**, and it underwrites the
chapter's *foundational premise* (vary ion transport, hold the SY electronic transport fixed),
which was asserted but not shown:

- **ATR** → ion association (νsSO₃ ~1030, no cation shift) + host local order.
- **XRD** → morphology (X-ray amorphous, homogeneous, salt dissolved).
- **UV-Vis** → **electronic structure: SY band edge ~2.50 eV invariant to the cation** → the
  electrolyte chemistry tunes ionic dynamics, not the semiconductor's electronic states.

It reinforces "the cation is not a clean lever" from a third, independent direction and closes
the loop: the differences seen electrically are ionic, not a change in SY's optical gap.

## 4. Recommendation

**Include, briefly** — one compact figure (`fig:ch4_uvvis`, the normalised band-edge overlay)
1--2 sentences in §4.5 (cation paragraph / host context) and a clause in the §4.7 discussion,
stated as illustrative and flagged as a separate (Au/2025/TMPE) generation. Do not over-claim:
it is an invariance (a controlled negative), valuable precisely because it pins the SY
electronic backbone as fixed across the electrolyte chemistries.
