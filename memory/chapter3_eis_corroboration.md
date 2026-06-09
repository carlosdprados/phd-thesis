---
name: chapter3_eis_corroboration
description: Ch3 §3.7 EIS impedance corroboration of composition->ionic-transport mechanism; method verdict + reproducible script
metadata: 
  node_type: memory
  type: project
  originSessionId: 5827e353-7cb4-4e53-a058-5ab5e0929581
---

Added Chapter 3 §3.7 "Microscopic Corroboration: Impedance Spectroscopy" (2026-06-05). EIS (0 V DC, 40 mV AC, 1 Hz–1 MHz, Ag, SY/PEO/LiTr) independently confirms the composition mechanism the chapter previously only hypothesised.

**Finding:** the impedance resistance scale falls >3 orders of magnitude as PEO rises and tracks the fading-memory time. Model-free Nyquist-apex Zreal: Spearman(PEO)=−0.69 per device (n=26), r=−0.83 cell medians; r(log Zapex, log t½)=+0.61 per device (n=23), +0.74 cells. Not a thickness artifact (partial r=−0.60; Zapex spans ×10⁴ vs thickness ×2.6 — ties into the §3.2 thickness-covariate argument). Honest nuances kept in text: PEO is the common cause of both; it's the resistance *scale* not the EIS relaxation *frequency* that tracks t½ (apex freq → sub-second RC, not the seconds-long forgetting clock).

**Method verdict (which of the 2 archived fits):** VARFREE (Gamry Echem Analyst, free fit, has error cols) > BOUNDS (the repo's project_feature_extraction python Nelder-Mead fit — Rion capped at 10 MΩ, spectra smoothed). VARFREE r(PEO)=−0.84/r(t½)=+0.80 vs BOUNDS −0.61/+0.59. Per-pixel circuit fits are genuinely ill-conditioned (independent refit confirms), so the chapter leads with the model-free apex descriptor and uses Rion only as corroboration. Circuit = MUNAR 0VDC model from Munar et al. Adv. Funct. Mater. 2012, 22, 1511 (DOI 10.1002/adfm.201102687) — verified via CrossRef, added as Munar2012 to references.bib.

**Artifacts:** scripts/ch3_eis.py → figures/chapter3/eis_ionic.pdf + handouts/ch3_eis_by_cell.csv. Chapter builds clean (23 pp standalone). Discussion hedge softened; limitations note bias-resolved EIS (up to 3 V DC) + chemistry-varied spectra remain untapped future work.

Related: [[fabrication_confound_audit]], [[thickness_rpm_confound_audit]]. Per [[bibliography_audit_chapter1]] the Munar DOI was CrossRef-verified, not LLM-generated.
