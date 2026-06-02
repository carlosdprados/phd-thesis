<!-- markdownlint-disable-file MD013 -->

# Chapter 2 — Improvements Checklist (Path to a Top-Tier PhD Chapter)

**Author:** Carlos David Prado-Socorro  
**Date:** 2026-06-02  
**Status:** Actionable checklist. Each item records the problem, its location in `chapters/chapter2_proof_of_concept.tex`, the fix, and a done-criterion. Tiers are ordered by importance: **Tier 0** must be fixed before the chapter can be read as written; **Tier 1** are rigor/correctness issues a committee will challenge; **Tier 2** strengthen completeness; **Tier 3** are polish.  
**Progress (2026-06-02 pass):** 12 of 18 items resolved and committed (all text/framing/arithmetic fixes plus figure scaffolding). The 6 remaining items are blocked on external experimental data or a pending decision — see the Resolution log below. After each fix, `make exports` was confirmed to exit 0.

> **Note on line numbers.** Line references reflect the state of the file at audit time (2026-06-02) and will drift as edits land. Each item also names the `\label` or section it lives in — anchor on that if the line number no longer matches.

---

## How to use this document

- Work top-down: Tier 0 → Tier 1 → Tier 2 → Tier 3. Lower tiers assume the figures exist.
- Tick `- [x]` when the item is both fixed **and** the chapter rebuilds clean (`make chapter2` with no new warnings).
- Items marked **JUDGEMENT** require a scientific decision, not a mechanical edit — do not auto-apply; decide, then record the decision inline.
- Header glyphs: ☑ = done & committed · ☐ = open. A header suffix marks why an open item is parked: **BLOCKED (needs data)**, **PARTIAL**, or **DEFERRED**.

---

## Status summary

| Tier | Theme | Items | Done | Remaining |
|------|-------|-------|------|-----------|
| 0 | Blocking — chapter non-functional | 1 | 1 | 0 |
| 1 | Rigor / correctness | 7 | 5 | 2 (1.2, 1.7) |
| 2 | Completeness / strengthening | 6 | 2 | 4 (2.1, 2.2, 2.4, 2.6) |
| 3 | Polish | 4 | 4 | 0 |
| **Total** | | **18** | **12** | **6** |

---

## Resolution log — 2026-06-02 pass

All resolved items were committed individually, each gated on a clean `make exports` (exit 0).

| Item | Disposition | Commit | Note |
|------|-------------|--------|------|
| 0.1 | ☑ Done | `docs(chapter2): scaffold eight figure floats…` | Placeholder floats with final captions/labels; **drop in real plots** to finish. All `\cref{fig:…}` now resolve. |
| 1.1 | ☑ Done | `fix(chapter2): reframe short-time conductance overshoot…` | "Momentum" replaced by continued redistribution / residual-field + doping-front. |
| 1.2 | ☐ **DEFERRED** | — | STDP Hebbian vs anti-Hebbian: user undecided; terminology left untouched. |
| 1.3 | ☑ Done | `fix(chapter2): correct energy-density area unit…` | ~6 fJ per µm² (was "per 100 nm²", off by 10⁴). |
| 1.4 | ☑ Done | `fix(chapter2): reconcile EPSC read-out bias…` | +1 V EPSC bias clarified as the state-defining read-out, distinct from the 0.5 V probe. |
| 1.5 | ☑ Done | `fix(chapter2): use signed current-ratio notation…` | `R_n = I_{Sn}/I_{S0}`; conductance no longer written negative. |
| 1.6 | ☑ Done | `fix(chapter2): separate cycling endurance…` | Section retitled "Ambient Shelf Stability"; endurance flagged uncharacterised. |
| 1.7 | ☐ **BLOCKED (needs data)** | — | Device/batch N for every RSD/error-band; cannot be fabricated. |
| 2.1 | ☐ **PARTIAL** | (figures via 0.1) | Eight main floats scaffolded; importing the AFM/profilometry/degradation SI data + plots still pending. |
| 2.2 | ☐ **BLOCKED (needs CrossRef)** | — | Verify metadata of all 53 citations (web/CrossRef). |
| 2.3 | ☑ Done | `fix(chapter2): correct first-author attribution…` | "Malliaras 2010" → "Zakhidov 2010" in the comparison table. |
| 2.4 | ☐ **BLOCKED (needs data)** | — | Stretch exponent β and fit quality from the actual retention fits. |
| 2.5 | ☑ Done | `docs(chapter2): frame ED/ECD timescale assignment…` | Marked a working interpretation with a Ch.3-testable consequence. |
| 2.6 | ☐ **PARTIAL** | — | Chirality wording ("clockwise") **verified correct** for forward>return in Q1 → no change; the within-sweep vs across-sweep reconciliation needs the real `fig:iv_hyst`. |
| 3.1 | ☑ Done | `style(chapter2): reduce repetition of the carried-forward handoff` | Intro role paragraph and comparison recap de-duplicated. |
| 3.2 | ☑ Done | `style(chapter2): temper promotional register…` | Seven intensifiers softened. |
| 3.3 | ☑ Done | `docs(chapter2): make the STDP fit explicitly piecewise…` | Per-branch fit in absolute delay with branch-specific `A_±`, `τ_±`. |
| 3.4 | ☑ Done | `docs(chapter2): distinguish Li+ site binding energy…` | Well-depth vs migration-barrier disambiguated. |

**What is needed to clear the remaining six.** 1.7 and 2.4 need the per-device statistics and retention-fit parameters from the experimental archive. 2.2 needs CrossRef/web verification. 2.1 needs the SI datasets brought in (and folds into the real-figure effort that finishes 0.1). 2.6 needs the plotted I–V data to confirm the within/across-sweep description. 1.2 needs your decision on the STDP polarity label.

---

## Tier 0 — Blocking (the chapter does not function as written)

### ☑ 0.1 — Insert the eight missing figures — DONE (placeholders scaffolded; real plots still to drop in)

- **Problem:** The chapter `\cref`s eight figures (`fig:device_schematic`, `fig:iv_hyst`, `fig:potentiation`, `fig:stm_ltm`, `fig:npulse`, `fig:retention`, `fig:epsc`, `fig:stdp`) but contains **no `\begin{figure}` or `\includegraphics`** — only the comparison `sidewaystable`. The build log shows all eight resolving to undefined `??`. The entire Electrical Characterisation section (§Electrical Characterisation, `\label{sec:elec_char}`) points at evidence that is not in the document.
- **Locations:** references at lines 130, 185–186, 204, 214, 226–228, 233–234, 254–255, 286–287, 372.
- **Fix:**
  1. Generate the plots from the published data / Python pipeline (`Nanomem_Devices_Library/`).
  2. Create `figures/chapter2/` (mirrors `figures/chapter1/`).
  3. Insert `figure` environments using the captions, labels, and source mapping already drafted in `handouts/03_chapter2_figures_needed.md`.
  4. Consider also adding the mechanism schematic (`fig:mechanism_schematic`) in §`sec:mechanism` and the thesis-only supporting figures (AFM vs spin speed, profilometry, degradation, HSAB energy landscape) listed in that handout — these double as the fix for items 2.1 and 1.6.
- **Done when:** `make chapter2` produces zero undefined-`fig:` warnings and every figure is cited from the text before it appears.

---

## Tier 1 — Rigor / correctness (committee will challenge)

### ☑ 1.1 — Reframe the "ionic momentum / inertia" explanation **[JUDGEMENT]** — DONE

- **Problem:** The short-time conductance *overshoot* is attributed to ions that "continue to migrate briefly… under their momentum" after the field is removed. Ion transport in the polymer is heavily overdamped (momentum relaxation ~fs); literal inertia cannot produce a sub-second effect.
- **Location:** `\label{subsec:stm_ltm}`, line 236.
- **Fix:** Keep the post-tetanic-potentiation analogy, but replace the mechanism with a defensible one: continued diffusional redistribution / slow doping-front kinetics / RC (double-layer charging) relaxation. State it as the proposed cause, not "momentum."
- **Done when:** No appeal to ionic inertia/momentum remains; the overshoot has a physically sound proposed origin.

### ☐ 1.2 — Resolve the Hebbian / anti-Hebbian contradiction **[JUDGEMENT]** — DEFERRED (awaiting your decision)

- **Problem:** The text defines pre-before-post (Δt<0) → potentiation, post-before-pre → depression — the classic **Hebbian** causal rule — yet labels the result "asymmetric anti-Hebbian" in two places. Internal contradiction; also the Δt sign convention is never stated.
- **Locations:** definition at line 268; "anti-Hebbian" at lines 287 and 296; also propagates into the `fig:stdp` caption in `handouts/03_chapter2_figures_needed.md`.
- **Fix:** Decide the convention (recommend stating Δt = t_post − t_pre explicitly), then make the label consistent with the measured polarity. If causal stimulation potentiates, it is Hebbian; reserve "anti-Hebbian" for causal depression. Update both the chapter and the figure caption.
- **Done when:** Sign convention is stated once, and the verbal rule, the equation, the figure, and the label all agree.

### ☑ 1.3 — Fix the energy-density unit error — DONE

- **Problem:** "≈50 nJ, or approximately 6 fJ per 100 nm² of device area." With the stated area (0.0825 cm²), 50 nJ = **6.06 fJ per µm²**, i.e. ~6×10⁻⁴ fJ per 100 nm². The figure "6" is right; the area unit is wrong by 10⁴.
- **Location:** `\label{subsec:pulse_potentiation}`, line 210.
- **Fix:** Change "per 100 nm²" → "per µm²" (or recompute and restate consistently). Verify the 50 nJ figure itself against the raw current trace while here.
- **Done when:** The normalised energy is dimensionally correct and matches the area used.

### ☑ 1.4 — Reconcile EPSC read voltage with the non-perturbing-read threshold — DONE

- **Problem:** §`subsec:pulse_potentiation` sets V_read = 0.5 V *because* the ionic threshold is >0.7 V (non-perturbing read). The EPSC protocol instead initialises/holds at +1 V — above that threshold — so its "read" would itself perturb the state.
- **Locations:** threshold + 0.5 V read at line 216; EPSC +1 V initialise/hold at lines 257–258.
- **Fix:** Either justify why the +1 V EPSC read is acceptable (e.g. it is the deliberate read-out drive, not a passive probe) and rename it accordingly, or harmonise the read voltages. Make the two conventions explicitly consistent.
- **Done when:** A reader cannot find two contradictory statements about what voltage is "non-perturbing."

### ☑ 1.5 — Remove unphysical negative "conductance" notation — DONE

- **Problem:** `G_{S3}/G_{S0} = -3.72`, `G_{S4}/G_{S0} = -16.97`. Conductance cannot be negative. The prose correctly calls this a "signed current response," then writes it as `G`.
- **Locations:** line 262 (chapter); also the `fig:epsc` caption in the figures handout.
- **Fix:** Introduce a distinct symbol for the signed readout ratio (e.g. `R_n = I_{S_n}/I_{S_0}` or a named EPSC ratio) and use it consistently in text, equation, and caption. Reserve `G` for non-negative conductance.
- **Done when:** No negative quantity is denoted `G` anywhere in the chapter or its figure captions.

### ☑ 1.6 — Separate endurance (cycling) from shelf/operational stability **[JUDGEMENT]** — DONE

- **Problem:** §`subsec:lifetime` opens by defining lifetime as *switching cycles* ("millions-to-billions of weight updates") then reports a **2-week ambient storage** result. Cycling endurance (cycle count to failure) is never measured.
- **Location:** `\label{subsec:lifetime}`, lines 361–367.
- **Fix:** Reframe the section as *shelf / operational stability* honestly, and explicitly list cycling endurance as not-yet-measured / future work — or add endurance data if it exists in the archive.
- **Done when:** The section no longer promises an endurance metric it does not deliver.

### ☐ 1.7 — State sample sizes (N) for every reproducibility claim — BLOCKED (needs device/batch N from the experimental archive)

- **Problem:** RSD <10% / <15% / <20%, "multiple independent devices," and the shaded error bands are all reported without N (devices/batches) or a definition of the band (SD vs SEM vs CI).
- **Locations:** lines 228 (`subsec:npulse` band), 373–375 (`subsec:reproducibility`).
- **Fix:** Add N for each statistic and define what the shaded band represents. Cross-check the same N in the `fig:npulse` caption.
- **Done when:** Each statistical claim carries an explicit N and band definition.

---

## Tier 2 — Completeness / strengthening

### ☐ 2.1 — Bring own-work supporting data into the thesis (stop deferring to the paper SI) — PARTIAL (main floats scaffolded via 0.1; SI data/plots pending)

- **Problem:** The spin-speed optimisation, AFM images, and degradation study are deferred to the SI of `PradoSocorro2022` (your own paper). A thesis should reproduce its own supporting evidence.
- **Locations:** lines 146, 163, 363.
- **Fix:** Add the thesis-only figures already specified in `handouts/03_chapter2_figures_needed.md` (AFM vs spin speed, profilometry trace, degradation time series) to `figures/chapter2/` and reference them in-chapter (or in a thesis appendix). Overlaps with item 0.1.
- **Done when:** The three supporting datasets appear in the thesis itself, not only as "see SI of Ref."

### ☐ 2.2 — Audit all 53 citations against CrossRef — BLOCKED (needs CrossRef/web verification)

- **Problem:** `references.bib` has previously contained LLM-hallucinated DOIs/titles (see memory note `bibliography_audit_chapter1.md`). All 53 keys in this chapter resolve, but key existence ≠ correct metadata.
- **Scope:** every `\cite` in the chapter; prioritise the comparison table (`tab:comparison`).
- **Fix:** Verify author/title/year/DOI of each entry against CrossRef; correct or remove anything unverifiable.
- **Done when:** Every Chapter 2 citation is CrossRef-verified and logged.

### ☑ 2.3 — Fix the author-name inconsistency for `Zakhidov2010` — DONE

- **Problem:** The comparison table labels this reference "Malliaras 2010"; the intro attributes it to "Zakhidov and co-workers." Same key, two names.
- **Locations:** intro line 56; table line 393.
- **Fix:** Choose the correct first-author attribution and use it in both places (and confirm against the verified bib entry from item 2.2).
- **Done when:** The reference is attributed identically wherever it appears.

### ☐ 2.4 — Report the stretch exponent β (and fit quality) for the retention fits — BLOCKED (needs β/fit values from the data)

- **Problem:** The Kohlrausch stretched-exponential fit underpins the "distribution of activation barriers" argument, but only τ is reported; β is never given.
- **Locations:** Eq. `eq:kohlrausch` (line 240) and the τ values at line 247.
- **Fix:** Report β for STM and LTM conditions, with R² or equivalent goodness-of-fit. Add the same to the `fig:retention` caption.
- **Done when:** β and fit quality are stated alongside τ.

### ☑ 2.5 — Anchor the ED/ECD model assignment to evidence **[JUDGEMENT]** — DONE (framed as interpretation)

- **Problem:** §`sec:mechanism` (subsecs `ed_model`, `ec_model`, `model_resolution`) reads textbook-like; the assignment "fast = anion / ED, slow = cation / ECD" is asserted rather than tied to a discriminating observable.
- **Locations:** lines 311–334.
- **Fix:** Either connect the assignment to a measurable (temperature, thickness, or sweep-rate dependence) or explicitly frame it as interpretation to be tested by the Chapter 3 cation sweep. Avoid presenting it as established for this device alone.
- **Done when:** The mechanism claim is either evidence-anchored or clearly labelled as interpretation.

### ☐ 2.6 — Verify I–V loop chirality and within-sweep vs across-sweep description — PARTIAL (chirality verified correct; within/across needs the real figure)

- **Problem (revised 2026-06-02):** On re-derivation the "clockwise" claim is **correct** — for forward > return in the first quadrant the loop is traversed clockwise (up the high/forward branch, down the low/return branch), so no change is needed there; the original counter-clockwise concern was mistaken. What still needs the plotted data is the apparent tension between "forward > return within a single sweep" (a within-sweep drop) and "current increases across successive sweeps" (across-sweep growth): confirm both hold and that the figure is consistent with progressive accumulation despite within-cycle hysteresis.
- **Location:** `\label{subsec:iv_hyst}`, line 192.
- **Fix:** Check the actual `fig:iv_hyst` data, correct the chirality wording if needed, and ensure the within-sweep and across-sweep statements are not read as contradictory.
- **Done when:** The loop description matches the plotted data unambiguously.

---

## Tier 3 — Polish

### ☑ 3.1 — Consolidate the repeated "carried-forward vs not-propagated" handoff — DONE

- **Problem:** The "three dynamical measurements carried forward / EPSC–STM/LTM–STDP not propagated" point is stated ~6 times.
- **Locations:** lines 60, 62, 180, 411, 418, 440.
- **Fix:** State it crisply once in the introduction and once in the summary; trim the intermediate repetitions to single-clause cross-references.
- **Done when:** The handoff is clear without redundancy.

### ☑ 3.2 — Temper promotional register for thesis prose — DONE

- **Problem:** Paper-style intensifiers ("profound consequences," "dramatically increases," "exceptionally large") sit above the flatter register expected in a thesis.
- **Locations:** e.g. lines 309, 326; scan the whole chapter.
- **Fix:** Replace with measured phrasing.
- **Done when:** Claims are quantitative or neutral rather than promotional.

### ☑ 3.3 — Clarify the STDP fit form — DONE

- **Problem:** A single `A·exp(−Δt/τ)` is presented across both branches; STDP is conventionally fit piecewise in |Δt|.
- **Location:** Eq. `eq:stdp_fit`, lines 289–294.
- **Fix:** State that each branch is fit separately in |Δt| with its own (A, τ), and report both branch values.
- **Done when:** The fitting procedure is unambiguous and reproducible from the text.

### ☑ 3.4 — Disambiguate the two energy scales (binding vs hopping barrier) — DONE

- **Problem:** Binding energy "~k_BT × 10²" (~250 kJ/mol) and hopping barrier "~50 kJ/mol" can read as inconsistent.
- **Locations:** hopping barrier at line 102; binding energy at line 340.
- **Fix:** Add a clause noting these are distinct quantities (site binding energy vs migration activation barrier) so they are not mistaken for the same number.
- **Done when:** A reader cannot mistake the two values for a contradiction.

---

## Cross-cutting done-criteria (check after all tiers)

- ☑ `make chapter2` (standalone) builds with **no undefined references** to `fig:` labels and no new warnings. *(Verified: 0 undefined `fig:` refs; only the expected cross-chapter `ch:`/`subsec:` refs remain in standalone.)*
- ☑ `make thesis` (full build) resolves all `\cref` to Chapter 1 (`ch:intro`, `subsec:*`) — these are expected-undefined only in the standalone build. *(Verified: full thesis build has 0 undefined references.)*
- ☑ Every figure is cited in the text *before* it appears, and every caption matches the numbers in the body. *(Each float placed after its first citation; captions cross-checked against body.)*
- ☐ All chapter numbers, ratios, τ/β values, and energies are internally consistent between text, equations, figure captions, and the summary list (`sec:ch2_summary`). *(Pending β from item 2.4.)*
- ☐ The comparison table (`tab:comparison`) author labels match the verified bibliography. *(Author label fixed in 2.3; full bib verification pending item 2.2.)*

---

## Provenance

This checklist was produced from a full read of `chapters/chapter2_proof_of_concept.tex` plus the build log on 2026-06-02. The figure captions/sources referenced above live in `handouts/03_chapter2_figures_needed.md`. The citation-verification concern derives from the prior `references.bib` audit recorded in memory (`bibliography_audit_chapter1.md`).
