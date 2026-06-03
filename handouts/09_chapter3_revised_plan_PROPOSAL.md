<!-- markdownlint-disable-file MD013 -->

# Chapter 3 — Revised Plan (PROPOSAL): Compositional & Chemical Control of Volatile Polymer-Electrolyte Memristors

**Author:** Carlos David Prado-Socorro · **Date:** 2026-06-03 · **Status:** PROPOSAL for review (you + advisor). The canonical plans `00_thesis_overview_memory.md` / `01_thesis_structure.md` / `05_chapter4_data_pipeline.md` are **left untouched** until this is approved. Evidence basis: the claims audit `08_chapter3_4_claims_audit.md` (§1–§16).

---

## 1. Why revise (what the data did to the April v3 plan)

The April v3 plan led with **cation identity (Li>Na>K)** as the comparative headline and relegated **TMPE host** and **TFSI anion** to "exploratory side evidence." Direct, QA'd analysis of the archive (handout 08) overturned that ordering of importance:

- **Cation Li>Na>K is not supported** and not even extractable as stated — it is confounded by potentiation-amplitude protocol (4 V vs 6 V write; §13), electrode (Ag vs Au; §16), and has n≤2 per matched cell (§16). Orderings flip across host/anion.
- The single **cleanest** cation comparison is the *relegated* TMPE/TFSI batch (§14).
- **Host and anion are larger, cleaner levers than cation** (§11, §15), but still n-limited.
- The **coverage audit (§16)** shows **only composition (PEO/LiTr/Ag) has real replication** (n=2–4 across a 3×3 grid); host/anion/cation are illustrative (n≤2 per matched side).

So the chapter should **lead with composition** (its strongest, replicated result) and present chemistry (host/anion/cation) as a clearly-labelled, n-explicit **qualitative tuning landscape** — not as four co-equal powered axes.

## 2. Claimable evidence (from §16 audit) — discipline for the chapter

| Axis | Replication (Ag, 0.3/0.09 unless noted) | Status in chapter |
| --- | --- | --- |
| Composition (PEO/LiTr) | 3×3 grid, **n=2–4/cell** | **quantitative spine** |
| Cation (Li/Na/K) | best cell TMPE/TFSI 2/2/2; others ≤1 | illustrative + honest negative |
| Host (PEO vs TMPE) | Tr/Li 3(Ag) vs 1; others 1–2 | illustrative trend |
| Anion (Tr vs TFSI) | PEO/Li 4 vs 1; others 1–2 | illustrative trend |
| Protocol amplitude | same-device evidence (v114) | **methodological result** |

## 3. Proposed chapter structure

1. **Framing & the three common measurements.** Volatile fading memory as a computational resource (not failed NVM). Define I–V hysteresis, variable-N potentiation, variable-delay depotentiation. State up front the claim discipline: composition = quantitative; chemistry/cation = illustrative, n-explicit.
2. **Quantitative spine — composition (PEO/LiTr, Ag, matched 4 V/2 V protocol).** The replicated 3×3 grid. Results: switching window and potentiation strength fall as PEO rises; **fading-memory τ tunable ≈ 2–20 s** (Kohlrausch τ, β; β≈0.6–0.9 stretched), longest at PEO0.3/0.09. Cross-validated vs pipeline τ (§8–§10). Device-to-device heterogeneity quantified as a *resource*.
3. **Chemical-tuning landscape (qualitative, n-explicit).** Host (PEO↔TMPE: ~6× at Li-triflate), anion (Tr↔TFSI: ~20× in PEO), cation (Li/Na/K). Cleanest cation datapoint: TMPE/TFSI → K shortest < Li≈Na, explicitly caveated as non-generalising. Relaxation-shape heterogeneity (stretched vs compressed β). All presented with n and as trends, not laws.
4. **Methodological contribution — protocol sets the timescale.** Potentiation amplitude dominates apparent τ (v114: 4.6→15.5 s, 3→6 V); read is suprathreshold. ⇒ any cation/chemistry comparison must hold write/read protocol, electrode and composition fixed. Recommend a future **subthreshold-read, protocol-locked, n≥3 cation series**.
5. **What this chapter does *not* claim.** No Li>Na>K law; no EPSC/STDP/STM-LTM/impedance across cations (Ch2-only); host/anion/cation are illustrative.
6. **Bridge to Chapter 4.** The composition τ ladder (2–20 s) + device heterogeneity + β-shape diversity = the heterogeneous fading-memory bank for reservoir/temporal computing.

## 4. Explicit diff vs the April v3 plan (01/05)

- **Promote** composition from "core sub-study" to the **chapter spine and quantitative result**.
- **Demote** cation Li>Na>K from secondary headline to an honest **negative result + methodological finding**.
- **Re-classify** TMPE host and TFSI anion from "exploratory side evidence" to a **named qualitative tuning landscape** (still n-limited, but no longer dismissed).
- **Add** the protocol-amplitude / electrode confound as a first-class methodological contribution.
- **Keep**: the three common measurements; the volatile/temporal framing; the Ch2-only status of EPSC/STDP/STM-LTM/impedance.

## 5. Risks / limitations to state plainly

- Only composition is replicated; everything else is n≤2 → must be framed as illustrative.
- Confounds (protocol amplitude, electrode Ag/Au, read-disturb) limit cross-device τ comparisons; control them or label results qualitative.
- Pipeline `exp decay: tau` needs per-device QA (many bad fits, §13/§16) before any quantitative use.

## 6. Open tasks before writing

- [ ] Refit (point-level QA) the composition-grid devices to publish clean per-cell τ, β, potentiation parameters (extend `scripts/ch3_4_dynamics_fits.py`).
- [ ] Read-disturb check on the composition devices (`05` prerequisite) before freezing the manifest.
- [ ] Decide figure set: composition heatmaps (window, τ), the chemistry-landscape bar charts (with n labels), the v114 amplitude-confound figure.
- [ ] If chemistry axes are kept, generate matched-protocol/electrode subsets only.

---

*If approved, this supersedes the Chapter-3 sections of `01_thesis_structure.md` (and the Ch3-facing parts of `00`/`05`); those will be updated in a single pass with a v4 revision note.*
