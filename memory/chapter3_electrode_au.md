---
name: chapter3_electrode_au
description: Ch3 §3.8 electrode section added — active-Ag vs inert-Au contrast + cross-electrode replication of chemistry claims
metadata:
  type: project
---

Ch3 §3.8 "Electrode Dependence: Active Silver versus Inert Gold" added (2026-06-05).

The Au-electrode corpus (50 devices) is **entirely at the lead composition 0.3/0.09** — a
chemistry-axis set, so it **cannot test the composition spine** (which stays Ag-only). All Au
delaytime use the same 2.0 V read as Ag (directly comparable), but **no human PNG curation** exists
for Au curves (automated screen only).

Findings (illustrative tier):
- **Electrode lever:** inert Au vs active Ag at matched chemistry → narrower switching window,
  weaker/flatter potentiation, higher activation voltage, but **longer** fading memory
  (PEO/Li: t½ ≈ 87 s on 2 clean Au devices vs ≈19 s Ag). Read as active-electrode (Ag⁺
  electrochemical-metallisation, volatile) vs noble-inert (Au, polymer-electrolyte ionic only).
  Higher Vact on thinner Au films rules out a thickness origin.
- **Cross-electrode replication:** host effect (PEO≫TMPE retention) and the **cation null** (flat
  Li/Na/K window on Au TMPE/OTf, on-off ≈1.3–1.5) both reproduce on Au → strengthens the chemistry
  landscape ([[chapter3_iratr_corroboration]]). Au also gives clean host-free/salt-free negative
  controls (no window, no potentiation).
- **Confound:** Au is 2024–25, Ag chemistry/lead-cell decays 2022–23 (electrode ⊗ generation); the
  matched Ag batch v271–276 has no decay data. Stated as future work (matched-generation split batch).

Decision: **folded into Ch3** (not a new chapter — single composition, small n, uncurated;
not left-as-is — it strengthens the weakest tier). Repro: `scripts/ch3_electrode.py` →
`figures/chapter3/electrode_contrast.pdf`, `handouts/ch3_electrode_by_cell.csv`,
assessment `handouts/19_electrode_au_assessment.md`. See [[fabrication_confound_audit]],
[[thickness_rpm_confound_audit]].
