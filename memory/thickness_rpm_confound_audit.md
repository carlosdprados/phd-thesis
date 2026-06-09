---
name: thickness-rpm-confound-audit
description: "Ch3/4 thickness/RPM confound checked (2026-06-04) — composition claims stand, thickness is a controlled covariate"
metadata: 
  node_type: memory
  type: project
  originSessionId: 466a1a68-a966-42a2-b638-592e73e496aa
---

Audited (2026-06-04) whether differing spin-coat RPM / film thickness confounds Chapter 3's composition claims and Chapter 4's parameter cards. RPM was deliberately (but non-uniformly) raised for higher-PEO cells to partially equalise thickness; residual thickness still covaries with PEO (Pearson +0.68, median 227→298 nm for PEO 0.3→1.2).

**Verdict: claims/values/simulations STAND — thickness is a controlled covariate, not a confound.** Decisive evidence: partial correlation r(thickness, log t½ | PEO) ≈ +0.05 (thickness adds nothing beyond composition) while r(PEO | thickness) ≈ −0.42 survives; lead cell PEO0.3/0.09 has 38% thickness spread with flat t½ (18–22 s); metrics are dimensionless ratios/timescales; activation V flat (r=−0.06) across 2.6× thickness range. Nothing re-computed — MC 1.49×, WESAD, physio-context all unaffected.

Source of truth for thickness = `DATABASE/DEVICES_PROFILOMETRY_STATS.csv`. Reproduce: `python3 scripts/thickness_rpm_audit.py` (also makes `figures/chapter3/thickness_control.pdf`). Full record: `handouts/14_thickness_rpm_confound_audit.md`. Documentation added to Ch3 §Materials (paragraph + fig:ch3_thickness_control) and Ch4 §Limitations. This closes a gap: handout 08 controlled protocol-amplitude/electrode/aging but never thickness. See [[chapter4_wesad_results]], [[bibliography_audit_chapter1]].
