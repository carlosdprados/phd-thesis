---
name: fabrication-confound-audit
description: "Full per-device fabrication audit (2026-06-05) — every DEVICES_LIBRARY.csv column checked vs Ch3/4 composition & chemistry claims; composition claims fully controlled, cation clean, host/anion carry cross-generation confounds"
metadata: 
  node_type: memory
  type: project
  originSessionId: 95fb5f37-e87b-4cb5-af16-e8c7e96842b3
---

Audited (2026-06-05) whether any fabrication variable other than chemistry/composition drives the Ch3/Ch4 effects, by walking **all 88 columns of `DATABASE/DEVICES_LIBRARY.csv`** for the exact 61 Ch3/4 devices (joined with measurement `day` for aging). Extends the earlier thickness/RPM (handout 14), protocol-amplitude (handout 08 §13), and electrode (§16) audits to everything else.

**Composition spine (Li/Ag, n=30) — claims STAND, very well controlled.** Held constant across the whole grid: SY loading (ratio 1, ~8.72 mg/mL), annealing temp (75 °C, no 2nd stage), Ag thickness (100 nm), metal-evap operator, **glovebox storage + measurement (humidity controlled — key for hygroscopic PEO)**, solvent, salt filtering (N), no MoS₂. Crossed (not confounded) with composition: fabrication date/batch (6 batches), operator (CDPS/DDDT), SY lot, **measurement age** (each batch measures all PEO levels on the same day; median day 3 everywhere), mixing/cooldown/volume/evap-rate. Decisive single-batch control: 2022-11-17, constant RPM=2000, one operator/SY lot → higher PEO still gives shorter retention (v140 t½18.6→v142 2.9→v144 6.0 s); trend also holds when RPM was escalated with PEO (2023-10). Residual minor flags: anneal 3.5 h appears only in the 2023-03 high-PEO batch (but replicated at 3 h elsewhere); Old SY used in 2023-02/03 batches (crossed with fresh-SY replicates; only PEO 0.15 row rests solely on old SY, already off-grid); weighing ±2–5 % worst at low-mass 0.3/0.045 corner.

**Chemistry landscape — mixed (already labelled illustrative).** Cation series are **clean same-batch** comparisons (v247–252 same day; v321–326; v333–338; v114–116) → honest-negative "no robust Li>Na>K" is a real chemistry result, not an artifact. **Host PEO-vs-TMPE** lost its within-batch Li pair (v247 PEO-Li broken/discarded) → leans on near-matched cross-batch v241 vs v250. **Anion triflate→TFSI** also spans RPM 2000→3000, a ~2.5-yr generation gap, and unfiltered→filtered salt — the weakest-controlled comparison.

Reproduce: `python3 scripts/fabrication_confound_audit.py`. Full record: `handouts/15_fabrication_confound_audit.md`. Optional small text adds suggested (host/anion extra confounds; explicit "constant annealing/electrode/atmosphere, crossed batch/operator/SY" clause). See [[thickness_rpm_confound_audit]], [[chapter4_wesad_results]].
