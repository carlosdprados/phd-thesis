# Memory Index

> **Shared agent memory for this repo.** This folder is the team-readable
> mirror of each agent's private working memory. Any agent (Claude or otherwise)
> picking up this thesis should read these files first to avoid re-deriving — or
> contradicting — decisions already made. Each file is one fact with YAML
> frontmatter (`name` / `description` / `metadata.type`) and `[[name]]`-style
> wiki-links between related facts. When you learn something durable about this project,
> add or update a file here **and** add its one-line pointer below, then commit
> it so the rest of the team inherits it. Keep this in sync with any private
> agent memory; do not let the two drift.

- [PhD Project Overview](phd_project_overview.md) — Organic memristive devices for neuromorphic computing; UV ICMol group; 2020–2025; 1 paper, 1 patent
- [Research Data & Structure](phd_data_structure.md) — Nanomem_Devices_Library layout: raw DEVICES_LAB_DATA (quarter/device/day/pixel), 353-device library, DATABASE 4-level CSV schema, keys & material decode
- [Nanomem Analysis Pipeline](nanomem_analysis_pipeline.md) — Python tooling: feature_extraction (raw→DATABASE), device_cleaner (Streamlit→FILTERED_DEVICES), graphmaker, scripts_general; how to run + scope limits
- [Paper 1 Summary](paper1_summary.md) — Polymer-composite 2-T memristive device (SY/Hybrane/LiTf), published Adv. Electron. Mater. 2022, basis for Chapter 2
- [Thesis Structure](thesis_structure.md) — 5-chapter plan (Intro · PoC SY/Hybrane/LiOTf · PEO-triflate comparative · data-driven temporal computing · Conclusions); canonical detail in repo handouts/01 & 00
- [User Profile](user_profile.md) — PhD candidate at UV-ICMol, experimental nanotech/organic electronics researcher
- [Bibliography Audit](bibliography_audit_chapter1.md) — Ch1 had LLM-hallucinated DOIs/titles (fixed); Ch2 fully CrossRef-verified clean (2026-06-03); verify new chapters' citations against crossref before relying on them
- [Chapter 4 WESAD Results](chapter4_wesad_results.md) — WESAD/affective work (now bound as **Ch5**); heterogeneity NULL on labels reframed (not removed); jury-strengthened 2026-06-09: deployment noise-robustness (memory decisive, +0.088 15/15 p<1e-4), wrist + µW/param envelope, no-regret summary, cross-corpus replication (PhysioNet Non-EEG, +0.130 19/20 p<1e-5), SOTA table; ≈237 pp clean
- [Thickness/RPM Confound Audit](thickness_rpm_confound_audit.md) — Ch3/4 composition claims checked vs film thickness (2026-06-04); thickness is a controlled covariate, claims/sims stand; handout 14 + scripts/thickness_rpm_audit.py
- [Fabrication Confound Audit](fabrication_confound_audit.md) — all 88 DEVICES_LIBRARY columns checked vs Ch3/4 claims (2026-06-05); composition spine fully controlled, cation clean same-batch, host/anion carry cross-generation confounds; handout 15 + scripts/fabrication_confound_audit.py
- [Chapter 3 EIS Corroboration](chapter3_eis_corroboration.md) — Ch3 §3.7 added (2026-06-05): EIS impedance independently confirms composition→ionic-resistance→fading-memory; VARFREE>BOUNDS fit; model-free Nyquist-apex headline; scripts/ch3_eis.py
- [Chapter 3 Electrode (Au vs Ag)](chapter3_electrode_au.md) — Ch3 §3.8 added (2026-06-05): inert-Au vs active-Ag lever (Au narrower window/weaker potentiation but longer t½≈87s); host effect + cation null replicate on Au; Au corpus all at lead composition so composition spine stays Ag-only; scripts/ch3_electrode.py
- [Chapter 3 IR-ATR + XRD Corroboration](chapter3_iratr_corroboration.md) — Ch3 §3.5 added (2026-06-05): ATR νsSO₃ ~1030 no cation shift (cation null) + ATR local order; XRD shows composite X-ray amorphous (corrected "semicrystalline"→local order, salt dissolved); humidity null excluded; scripts/ch3_iratr.py + ch3_xrd.py
- [Chapter 6 Conclusions Draft](chapter6_conclusions_draft.md) — Ch6 Conclusions & Outlook drafted (2026-06-07); 4 evidence layers + benchmarking vs reservoir/organic/event-driven HW + limitations + outlook; full thesis builds clean (204 pp, 0 undefined refs)
- [Git Commit Preference](git_commit_preference.md) — commit after each build milestone; no Claude co-author trailer in this repo
- [Bridge Chapter Decision](bridge_chapter_decision.md) — standalone Hybrane→PEO bridge chapter approved (new Ch3, 2026-06-06); degradation = batch-level Hybrane-stock aging seen as device-health collapse (not area decline); notes are primary source; handout 22 + scripts/bridge_hybrane_peo_reproducibility.py
- [Thesis Jury Audit & Polish](thesis_jury_audit_polish.md) — 2026-06-08 audit+fixes; SI appendices B/C/D added; labels/figure-dirs renamed to bound order (NAMING GOTCHA: figure scripts keep legacy ch3_/ch4_ names); defensive language cut; whole bib verified; 215 pp clean
- [Figure House Style](figure_house_style.md) — 2026-06-09 unified sans-serif restyle via scripts/figstyle.py (Helvetica+stixsans, despined, bold left-aligned panel letters, shared palette); applied to Ch2-5 + bridge; escape-leak/label fixes; morphology & design_space redrawn; Ch1 = raster PNGs (no script), still serif = known gap
