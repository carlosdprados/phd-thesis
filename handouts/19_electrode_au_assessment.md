# Handout 19 — Gold (Au) electrode corpus: assessment for Chapter 4

**Date:** 2026-06-05 · **Script:** `scripts/ch4_electrode.py` · **Table:** `handouts/ch4_electrode_by_cell.csv`

This handout answers the question: *we also have devices with gold (Au) top electrodes instead of
silver (Ag) — do Chapter 4's claims still hold, are there new claims, and where (if anywhere) should
they go?*

All numbers below are reproduced by `scripts/ch4_electrode.py` from the same DATABASE the rest of
Chapter 4 uses (`DEVICES_LIBRARY.csv` for species identity, `UPDATED_DEVICES_LIBRARY.csv` for the
collapsed mass-ratio values and the evaporated-electrode thickness, plus the HYST / PULSES /
DELAYTIME / FILTERED tables).

---

## 1. What the Au corpus actually is

There are **50 Au devices** in the library (vs 182 Ag). The decisive structural fact:

> **Every Au device is SY-based and sits at the single lead composition (ion-polymer mass ratio
> 0.3, salt 0.09).** Off-spine Au composition devices: **zero.**

So the Au corpus is a **chemistry-axis dataset at fixed composition**, not a second composition grid.
Its chemistry coverage (all 0.3/0.09):

| chemistry | n (Au) | has decay (2 V) |
|---|---|---|
| PEO / Li / OTf | 6 | yes (2 clean) |
| TMPE / Li / OTf | 17 | curves present, none pass the screen |
| TMPE / K / OTf | 6 | hysteresis only |
| TMPE / Na / OTf | 4 | hysteresis only |
| TMPE / Na / TFSI | 2 | hysteresis only |
| Hy (Hybrane) / Li / OTf | 5 | hysteresis only (2021, the Ch2 PoC material) |
| TMPE / — (salt-free) | 2 | control |
| — / Li / OTf (host-free) | 2 | control |
| pristine SY (no electrolyte) | 6 | control |

Two consequences are immediate and non-negotiable:

1. **The composition spine — Chapter 4's only quantitative, replicated result — cannot be tested on
   Au at all.** Au has no composition variation. Nothing about the composition claims is confirmed or
   refuted by the Au data; they remain a silver-only result.
2. The Au data *can* speak to the **chemistry axis** (host / cation / anion) and to the **electrode**
   itself, both at 0.3/0.09.

The Au DELAYTIME devices all use the **same 2.0 V read protocol** as the Ag corpus, so fading-memory
times are directly comparable. **No human PNG curation exists for any Au curve** (the curation
registry covers Ag chemistry devices v321–v338 only), so Au curves get the FILTERED flags + an
automated quality screen (R²≥0.90, non-degenerate β, finite t½) and nothing more — a real honesty
limit, weaker vetting than the Ag numbers.

---

## 2. Do the Chapter 4 claims hold on Au?

### 2a. Composition claims — untestable (not contradicted)
No Au composition variation exists. The claims stand as silver-only; Au is silent.

### 2b. Chemistry claims — **reproduce on a second electrode** (this is the valuable part)

**Host (PEO vs TMPE).** Fading memory, matched 0.3/0.09/Li/OTf:
- Ag: PEO t½ ≈ 19 s (n=3)  →  TMPE t½ ≈ 3.7 s
- Au: PEO t½ ≈ **87 s** (2 clean devices, v265/v268, R²≈0.97–0.99, β≈0.56–0.60) → TMPE much shorter
  (no clean Au TMPE decay survives the screen, but window + potentiation collapse, below).

PEO > TMPE retention reproduces on Au, and the host also orders the **switching window** and
**potentiation** the same way on Au (PEO on-off 2.0, peak 29× ; TMPE on-off 1.3, peak 1.9×).
**Host claim holds on a second electrode.**

**Cation (Li/Na/K, TMPE/OTf).** Au has no Na/K *decay* data, so the retention null cannot be
re-tested on Au. But the **switching window is flat across the cation series** on Au — on-off
1.29 (Li) / 1.47 (Na) / 1.43 (K), normalised area 0.066 / 0.108 / 0.063 — i.e. **no clean cation
ordering**, the same null Chapter 4 reports for Ag, now seen on a second electrode and via an
independent observable (the steady-state window rather than the decay). **Cation null reproduces.**
(The UV-Vis band-edge invariance in §3.5 already uses this same Au/TMPE generation.)

**Anion (OTf vs TFSI).** Direction consistent: TMPE/Na/TFSI gives a smaller window than TMPE/Na/OTf
on Au (on-off 0.98 vs 1.47), matching the Ag finding that TFSI is the "weaker/faster" anion. n=1–2;
illustrative.

**Controls newly available on Au.** Host-free (SY+salt, no polymer) and salt-free (SY+TMPE, no salt)
films show **no potentiation** (peak ≈ 1.0 and 0.6) and **no switching window** (on-off ≈ 0.99),
and pristine SY likewise. These are clean negative controls supporting the mechanism (you need both
the ion-transport polymer *and* the salt) — and they did not exist in the analysed Ag set.

### 2c. The protocol claim (§3.6) — unaffected
Drive protocol still co-sets the timescale; Au changes nothing about that argument.

---

## 3. New finding: the electrode is itself a lever (Ag active vs Au inert)

At matched chemistry and composition, the Au electrode shifts **all three** behavioural families in a
**mutually consistent** direction:

| chemistry 0.3/0.09 | metric | Ag | Au |
|---|---|---|---|
| PEO/Li/OTf | on-off ratio | 3.25 | **2.00** |
| | normalised loop area | 0.332 | **0.121** |
| | activation voltage (V) | 2.38 | **2.74** |
| | potentiation peak ratio | 123× | **29×** |
| | log-log growth exponent α | 0.89 | **0.45** |
| | fading-memory t½ (s) | 19 | **87** |
| TMPE/Li/OTf | on-off ratio | 3.82 | **1.29** |
| | potentiation peak ratio | 54× | **1.9×** |

Pattern, robust across chemistries: **Au → narrower switching window, weaker/flatter potentiation,
higher activation voltage, but a LONGER fading-memory time.**

**Physical reading (coherent, literature-consistent).** Ag is an electrochemically *active*
electrode (mobile Ag⁺, the canonical electrochemical-metallization story); it contributes a large but
*volatile* component to switching (fast relaxation, larger window, lower threshold). Au is a *noble,
inert* electrode; switching is then carried by the polymer-electrolyte ionic mechanism alone —
smaller amplitude, higher threshold, but more *retentive*. That is exactly the observed
window↓ / potentiation↓ / threshold↑ / retention↑ quartet. The higher Au activation voltage rules
out a film-thickness explanation (Au devices were spun *faster*, i.e. thinner, which would *lower*
the threshold, not raise it), pointing to an interfacial/electrode origin.

**Confounds (why this is illustrative, not quantitative).**
- **Generation.** Every Au device is 2024–2025; the Ag chemistry/lead-cell decays are 2022–2023.
  Electrode is partly confounded with fabrication generation. The would-be clean control — the Ag
  batch **v271–v276 (Oct 2024, same operator, 2 weeks after the Au batch v265–v270)** — has hysteresis
  but **no DELAYTIME**, so it cannot anchor the retention contrast.
- **Small n / no curation.** The headline Au retention rests on 2 clean PEO/Li devices; Au curves were
  never human-curated.
- These are the same honesty limits as the rest of the chemistry axis — hence the same "illustrative"
  tier.

---

## 4. Recommendation: fold into Chapter 4 (do **not** spin a new chapter; do **not** leave as-is)

- **New chapter? No.** Single composition, small n per cell, no human curation, electrode/generation
  confound. It has neither the replication of the composition spine nor the independent breadth to
  carry a chapter at Chapter 4's evidential standard.
- **Leave as-is? No.** Chapter 4 previously *held Au out* (§4.2, §4.9 "electrode … held out rather
  than modelled"). But the Au data does two genuinely useful things: it **independently replicates the
  host effect and the cation null on a second electrode** (materially strengthening the illustrative
  chemistry landscape, which is Chapter 4's weakest tier), and it reveals a **clean, physically
  sensible electrode lever**. Discarding that wastes corroboration the chapter needs.
- **Fold into Chapter 4 — yes.** Concretely:
  1. A short **electrode subsection** (sibling of EIS §4.7 and the microscopic-corroboration material),
     reporting the Ag-active / Au-inert contrast as an *illustrative* finding with the quartet above,
     the active-vs-inert reading, and the generation/curation/n caveats stated plainly.
  2. One or two sentences in the **chemistry section** noting that the host effect and cation null
     **reproduce on the Au electrode** (cross-electrode replication), with n stated.
  3. Soften §4.9: the electrode is no longer merely "held out" — it is now reported illustratively and
     used as cross-electrode corroboration; the residual confound (generation) is the honest caveat.
  4. Optionally a figure (electrode contrast: window / potentiation / retention, Ag vs Au at the lead
     cell). Lower priority than the prose.

Scope stays small and squarely inside Chapter 4's existing "composition = quantitative / chemistry +
electrode = illustrative" two-tier discipline. The quantitative spine is untouched.
