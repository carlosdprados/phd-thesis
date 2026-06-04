<!-- markdownlint-disable-file MD013 -->

# Chapter 3 — Full Plan: Compositional and Chemical Control of Volatile Polymer-Electrolyte Memristive Dynamics

**Author:** Carlos David Prado-Socorro · **Date:** 2026-06-03 · **Status:** Historical approved plan. Chapter 3 has now been drafted in `chapters/chapter3_comparative.tex`, and follow-up work is tracked in `handouts/13_chapter3_improvement_plan.md`. Use this file for original Chapter-3 structure and evidence rationale, not for current progress status. Evidence basis: claims audit `08_chapter3_4_claims_audit.md` (§1–§16); rationale/diff: `09_chapter3_revised_plan_PROPOSAL.md`.

> **One-line thesis of the chapter.** In SY/polymer-electrolyte composites, the **composition** of the ion-transport phase is a *replicated, quantitative* knob on the volatile memristive dynamics (switching window, potentiation, and a fading-memory time constant τ tunable over ≈ 2–20 s); electrolyte **chemistry** (host, anion, cation) shifts those dynamics further but is documented here as an *illustrative, sample-limited* landscape; and the **drive protocol** (potentiation amplitude) is shown to set the apparent timescale, a result that disciplines all cross-device comparison.

---

## 1. Framing and scope (claim discipline up front)

- Continue the volatile/temporal-computing framing from Ch1–Ch2: these devices are **good volatile, heterogeneous fading-memory elements**, not failed non-volatile memories.
- Introduce the **three common dynamical measurements** carried from Ch2 and used throughout: (i) I–V hysteresis, (ii) variable-number-of-pulses potentiation, (iii) variable-delay-time depotentiation. The richer synaptic protocols (EPSC, STDP, separated STM/LTM, impedance) remain **Chapter-2 (Paper 1) only** and are not claimed across this chapter's families.
- **State the evidence discipline explicitly** (from the §16 audit): composition is the only statistically-replicated axis (n=2–4 across a grid); host/anion/cation are illustrative (n≤2 per matched cell). The chapter is written so the reader always knows which results are quantitative vs illustrative.

## 2. Materials, fabrication, and the measurement protocol

- Active layer: **Super Yellow (SY)** semiconductor + an **ion-transport host** (PEO or TMPE) + a dissolved **alkali-metal salt** (Li/Na/K, triflate `OTf`/`Tr` or `TFSI`). Vertical ITO / active / **Ag** stack (Au devices exist but are kept separate — electrode confound, §16).
- **Composition grid (the designed experiment):** PEO mass fraction ∈ {0.3, 0.6, 1.2} × salt mass fraction ∈ {0.045, 0.09, 0.18}, LiTr, Ag. (PEO 0.15 and PEO0.3/0.18 cells lack clean coverage.)
- **Drive/read protocol (must be reported and held fixed):** 30 potentiation pulses, inter-pulse 0.103 s; standard amplitude **4 V write / 2 V read** (the 2023–2025 corpus). The 2022 batch used 6 V/3 V — *not* pooled (see §5). Read is suprathreshold (>0.7 V threshold) — flagged as a limitation.

## 3. Methods & analysis (reproducible)

- Feature pipeline `Nanomem_Devices_Library` → DATABASE CSVs; per-device fits via `scripts/ch3_4_dynamics_fits.py`.
- **Fading-memory model = Kohlrausch stretched exponential** (same as Ch2 `eq:kohlrausch`): ΔG(t)=ΔG₀·exp[−(t/τ)^β]+ΔG∞. Report **τ** (relaxation time) and **β** (stretch). The pipeline `exp decay: tau` (β=1) is a stable proxy, used after **per-device QA** (point-level outlier removal; many raw fits are bad — §13/§16).
- Cross-validated against the pipeline's independently pre-computed τ/saturation (corr 0.93–1.0, §9).
- **Comparison discipline:** any cross-device τ statement holds composition, electrode, and drive protocol fixed.

## 4. Results — quantitative spine: composition control (PEO/LiTr, Ag, 4 V/2 V)

The replicated core (n=2–4/cell across the 3×3 grid). Three coherent composition trends:

- **Switching window** (HYST on-off ratio, normalized loop area) **shrinks as PEO rises** at fixed salt.
- **Potentiation strength** (pulse-count growth exponent, peak gain) **falls as PEO rises** (peak ~480×→~4×, 0.3→1.2); ~half of cells show **turnover/over-potentiation** beyond ~100–300 pulses (a usable-range ceiling).
- **Fading-memory τ is composition-tunable ≈ 2–20 s**, longest at PEO0.3/0.09 (τ≈20 s), shorter at higher PEO. β≈0.6–0.9 (stretched → multi-timescale within a single device).
- **Device-to-device heterogeneity** is quantified and **reframed as a resource** for Ch4 (a bank of timescales).
- *Figures:* composition heatmaps (window, τ); representative decay + Kohlrausch fit; potentiation curves with turnover.

## 5. Results — chemical-tuning landscape (illustrative, n-explicit)

Present as trends with sample sizes stated, never as powered laws:

- **Host (PEO vs TMPE):** at Li-triflate (Ag, matched protocol), PEO/LiTr τ≈20–25 s (n=3) vs TMPE/LiTr τ≈3.8 s (n=1 clear) — ~6× shorter and weaker in TMPE.
- **Anion (triflate vs TFSI):** in PEO, triflate τ≈20 s vs TFSI τ≈1 s — TFSI dramatically shortens retention; TFSI Na/K decays are **compressed** (β≈2 "cliff") vs stretched triflate.
- **Cation (Li/Na/K):** **no robust Li>Na>K**. Best single comparison (TMPE/TFSI, n=2 each, same batch): **K shortest (~3.5 s) < Li≈Na (~6–7 s)**, consistent with weakest K⁺–O coordination — explicitly caveated that triflate families do not reproduce the ordering.
- *Figures:* bar charts of τ by host/anion/cation **with n labels**; the stretched-vs-compressed β shapes.

## 6. Results — the drive protocol sets the timescale (methodological contribution)

- Same device **v114: τ = 4.6 s (3 V write) → 15.5 s (6 V write)** — potentiation amplitude inflates apparent τ ~3×. Higher drive moves more ions (and at 6 V likely triggers electrode reactions), writing a deeper, longer-lived state.
- Consequence: cross-device/cation/chemistry τ comparisons are **only meaningful at fixed protocol + electrode + composition**. The 2022 (6 V) and 2023+ (4 V) batches must not be pooled.
- *Figure:* v114 dual-amplitude decay overlay.

## 7. Discussion

- Ion–polymer coordination (HSAB) is retained as a **qualitative chemical framing** for the trends, not as a quantitative cation law.
- Composition as the primary timescale-engineering knob; chemistry as secondary tuning; protocol as an operational lever (and confound).
- The chapter's quantitative deliverable for Ch4: a **composition-indexed family of fading-memory time constants (τ ≈ 2–20 s) + heterogeneity + β-shape diversity** = the heterogeneous reservoir bank.

## 8. What this chapter does NOT claim

- No Li>Na>K retention law (refuted/confounded; §13–§16).
- No EPSC/STDP/STM-LTM/impedance comparison across cations (Ch2-only).
- Host/anion/cation effects are illustrative (n≤2 matched), not statistically powered.

## 9. Limitations & future work

- Only composition is replicated; chemistry axes need n≥3 at matched protocol/electrode.
- Read is suprathreshold → recommend a dedicated **subthreshold-read (≤0.7 V), protocol-locked, n≥3 cation series** to test Li/Na/K properly.
- Electrode (Ag vs Au) and aging/day effects to be controlled; encapsulation for long-run stability.

## 10. Bridge to Chapter 4

The composition τ ladder, device heterogeneity, β-shape diversity, and potentiation/turnover parameters feed the compact behavioural model and the active Chapter-4 reservoir simulations (`12`, `scripts/ch4_*.py`). The older heterogeneous-reservoir / coincidence / filter-bank split in `04`/`05` has been superseded: coincidence is cut, and filter-bank logic is folded into the reservoir framing. Ch4 must use matched-protocol, QA'd fits and state the φ⊗λ amplitude-compatibility assumption explicitly.

---

## Plan logistics

- **Scope/length:** ~30–40 pages (unchanged from `01`).
- **Status:** core composition results ready to write; chemistry-landscape figures need matched-protocol/electrode subsets; v114 protocol figure ready.
- **Open data tasks (pre-writing):** extend `scripts/ch3_4_dynamics_fits.py` to emit clean per-cell τ/β/potentiation for the composition grid; read-disturb check; freeze the composition-grid manifest.
- **Claim crosswalk:** every figure traces to a claim in `08` §3 ledger (C1/C2 composition ✅; C8/C9/C10 ✅; C11 host/anion 🟡; C3 cation 🔴; C12 protocol ✅).
