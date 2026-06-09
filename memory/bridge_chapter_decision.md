---
name: bridge-chapter-decision
description: Decision to add a standalone Hybrane→PEO bridge chapter (new Ch3) and the verified degradation evidence behind it
metadata: 
  node_type: memory
  type: project
  originSessionId: 854e49b9-b505-4bb5-b890-b4ece17f57c0
---

User decided (2026-06-06) to add a **standalone short bridge chapter** between current Ch2 and Ch3, documenting the Hybrane→PEO material pivot. New order: Intro · PoC · **Bridge** · Comparative · Temporal · Conclusions (full chapter renaming approved; LaTeX cross-refs use labels so numbers auto-update). Plan: `handouts/22_bridge_chapter_plan.md`; assessment: `handouts/21_*`; reproducible evidence: `scripts/bridge_hybrane_peo_reproducibility.py` → `handouts/bridge_hybrane_peo_summary.csv`.

**Why:** ~18 months of solo work (the reproducibility crisis, the 88-column DEVICES_LIBRARY, the feature_extraction pipeline, device_cleaner) is currently invisible/uncredited and the Hybrane→PEO pivot is unexplained. A methods + negative-result chapter fixes both.

**STATUS (2026-06-07):** Bridge chapter drafted (`chapters/chapter3_bridge.tex`, `\label{ch:bridge}`) + figures (`figures/chapter3_bridge/`); 6-chapter renumber DONE and thesis builds clean: intro=1, poc=2, **bridge=3**, comparative=4 (`chapter4_comparative.tex`), temporal=5 (`chapter5_temporal.tex`), conclusions=6 (`chapter6_conclusions.tex` stub — still needs drafting). Hardcoded `Chapter~N` refs converted to `\Cref{ch:...}` labels throughout; frontmatter updated. Conclusions chapter is the remaining TODO.

**How to apply (non-obvious, verified facts):**
- Degradation is **batch-over-calendar-time, caused by the physical Hybrane reagent stock aging** — NOT within-device aging.
- **FOUR CONTROLS are mandatory** (verified each matters; mirror `Nanomem_Devices_Library/project_feature_explorer`, the Dash app the author used to find the trends): (1) **per-device weighting** — pixels/device falls 16→2, ρ=−0.80 vs date, so reduce each feature to one value/device before testing; DEVICE_INFO saturated/broken% are unpopulated, use curve-level; (2) **standard-protocol corpus** SY/Hy/LiTr/Ag, 75°C anneal, no 2nd stage, Hy0.3/LiTr0.09 (n=69) — excludes the 150°C high-temp PARTIAL-RECOVERY batch + composition variants; (3) **amplitude match** (bin `max voltage (V)`; within-Hybrane at tight ~1.0–1.45V, Hy↔PEO at ~3V); (4) **recovery-tail sensitivity** (±dropping ≥2022-03).
- **READ EACH FEATURE AT ITS EXPRESSING AMPLITUDE** (key nuance): window features (on-off, normalized area) only open at high amplitude — at 1.2V they sit near unity for all devices and can't show collapse; read them at ~3V. Conductivity features read at matched ~1.2V. Test window collapse as a STEP at the documented NM_v026 inflection (early ≤Apr2021 vs later, Mann-Whitney), not a whole-campaign correlation.
- **Mature degradation result** (`scripts/bridge_hybrane_peo_reproducibility.py`, standard corpus, per-device):
  - HEADLINE window collapse @3V, early→later: on-off **2.44→1.21 (MWU p=0.002)**; normalized area **0.235→0.027 (p=0.0005, ~9×)**; potentiation %change-in-maxV-current **+18%→−2% (p=0.013)**. on-off→~1.2 ⇒ no window ⇒ no potentiation = functional death (matches author's memory "2.5→1-1.7").
  - MECHANISM ohmic drift @matched 1.2V (Spearman vs date, strengthens dropping recovery tail): current at maxV ρ=+0.45→+0.55, raw area +0.57→+0.69, current-diff-at-on-off +0.51→+0.63 (p<1e-3).
  - `is broken` DECREASES (ρ=−0.40, handling/contacts improved — NOT a degradation metric); `is saturated` rises (ρ=+0.27).
  - Resolution: PEO wider window at matched 3V (narea 0.26→0.42, MWU p=0.018). PEO "reproducibility" win is TEMPORAL not within-batch CV: PEO/Ag on-off@3V holds usable window (median 2.61) across 2.5 yrs (2022-2024, yearly 3.3/2.6/1.9, no collapse) vs Hybrane stuck ~1.35 post-collapse; within-batch CV only modestly better (0.38 vs 0.47). State "reproducible" precisely = temporal/batch (no stock collapse) + better features.
  - Forward-looking methods legacy (plan §3, positive going-forward beat): crisis forced lasting apparatus — DEVICES_LIBRARY (provenance), normalized characterization procedure (fixed protocols), project_feature_extraction (pipeline), project_feature_explorer/device_cleaner/visualization_tools (trend discovery) — the same machinery powering Ch3/Ch4.
  - DROPPED as confounded: the earlier "~90× conductivity rise" (single-point all-corpus metric) and "PEO more reproducible CV 0.54→0.34" (CVs equal at matched 3V).
  - Two corrected mis-calls: don't read window features at 1.2V; don't use whole-campaign Spearman for a step change.
- **Mechanistic hypothesis (chapter includes it, labelled as hypothesis NOT proven):** moisture-driven hydrolytic aging of the hyperbranched polyester-amide Hybrane stock — water uptake + ester/amide chain scission → ohmic drift + window/potentiation collapse; secondary: acidic products doping PPV-type SY. Supported by: annealing recovery (late 150C-annealed devices recover on-off @3V to 1.95 vs 1.22 standard, MWU p=0.024), the electrical signature, and the material class. Definitive proof NOT supportable (no EIS on Hybrane devices=0 rows; no GPC/NMR/Karl-Fischer of stock; aged stock gone). Confirming experiments (FTIR/GPC/Karl-Fischer/EIS on retained aged-vs-fresh stock) → future work/SI. Plan §1E.
- **v061/v064 (>100-day study, raw in DayX folders) is POSITIVE evidence** — devices hold characteristics for weeks ⇒ supply, not device, degraded. Multi-day stability figure → **Ch2 SI**; only fresh-day points enter the bridge timeline.
- **Attribution = Hybrane stock (firm).** Old/new SY made no significant difference; SY eliminated. ITO was a one-off colleague guess, not the verdict.
- **Primary source = free-text `Fabrication Notes` + `Characterization Notes`** in DEVICES_LIBRARY.csv (not the Y/N columns). Anchors: v026 (2021-04-22) inflection; Lorenzo cross-person corroboration (v067); 2022 recovery attempts (v106–113).
- **Caveat:** mid-2021 corpus enriched in deliberately-stressed controls, so lead on the window-collapse + fixed-V conductivity trends, not the broken/saturated health metric. Use `DEVICES_LIBRARY.csv` for true dates (UPDATED coarsens to month).
- Hybrane→PEO contrast (resolution): window 0.21→0.39, device-to-device CV 0.54→0.34, on-off 1.9→4.3.
- New chapter order: Intro·PoC·Bridge·Comparative·Temporal·**Conclusions(reserve chapter6_conclusions.tex)**. Must reconcile Ch2 §2.7 (praises Hybrane stability) in the same pass — partition: device shelf-stability real, batch/supply reproducibility collapsed.

Relates to [[thesis_structure]], [[phd_data_structure]], [[fabrication_confound_audit]].
