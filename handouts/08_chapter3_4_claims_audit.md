<!-- markdownlint-disable-file MD013 -->

# Chapters 3 & 4 — Claims Audit and Data-Coverage Ledger

**Author:** Carlos David Prado-Socorro · **Started:** 2026-06-03 · **Status:** living document — updated incrementally and committed after each pass.

**Purpose.** Decide, from the *actual* experimental archive, **what Chapters 3 and 4 can and cannot defensibly claim** — before writing. Every claim is rated against the data on disk, not against the plan. Companion docs: the forward spec [`05_chapter4_data_pipeline.md`](05_chapter4_data_pipeline.md), the chapter plan [`01_thesis_structure.md`](01_thesis_structure.md), and the as-built archive reference [`../docs/experimental_archive_and_pipeline.md`](../docs/experimental_archive_and_pipeline.md).

---

## 0. Resume pointer (read first)

- **Method:** analysis driven from `Nanomem_Devices_Library/DATABASE` (regenerated May 2025) — `UPDATED_DEVICES_LIBRARY.csv` for chemistry, the `*_PIXEL_INFO.csv` tables for measurement presence, `FILTERED_DEVICES.csv` for erratic-pixel flags. Corpus = **PEO host + triflate salt = 149 devices**.
- **Artifact:** [`ch3_ch4_device_inventory.csv`](ch3_ch4_device_inventory.csv) — one row per PEO/triflate device with chemistry, electrode, and per-type pixel counts. Regenerate with the script noted in §5.
- **Done:** §1–§3 coverage/scope/ledger, §6 first-pass trends, §7 manifest candidates, §8 dynamics, §9 cross-validation, §10 **τ,β** alignment, §11 cation expansion, §12 PNG QA (2023-10), §13 **read-voltage confound (decisive)**. Artifacts: `ch3_ch4_device_inventory.csv`, `ch4_device_manifest_DRAFT.csv`, `ch4_decay_fits.csv`, `ch4_pulse_descriptors.csv`, `scripts/ch3_4_dynamics_fits.py`.
- **Cation verdict (C3):** at matched protocol (4 V/2 V) PEO/triflate shows Li longest (HSAB-consistent, n=1 Na/K) but it does **not** generalise across host/anion → no universal Li>Na>K. The dominant τ lever is **potentiation amplitude** (write/read protocol), not cation (§13, C12). **Composition result (C1/C2) stands** (uniform 4 V/2 V).
- **TFSI QA done (§14):** PEO/TFSI collapsed (only v321 Li usable); TMPE/TFSI all clean → cleanest cation comparison = K shortest, Li≈Na (n=2), but not robust across families. Cation analysis is now **complete**: no universal ordering; potentiation amplitude ≫ host > anion > cation.
- **Coverage audit (step A) done — §16 + `ch3_coverage_audit.csv`:** only composition (PEO/LiTr/Ag) is replicated (n=2–4); host/anion/cation are n≤2 illustrative; Au-electrode confound caught (corrected §15).
- **Rework APPROVED & SHIPPED (v4):** full Ch3 plan = `10_chapter3_comparative_plan.md`; canonical `00`/`01`/`05` + README updated to v4. Proposal/diff retained in `09_…PROPOSAL.md`.
- **Delay-fit QA scan (§17)** + **rescue outcomes:** v149 discard (both), v148 delay discard / pulses keep, v151 delay salvageable (2/5/10/60/300 s). Composition spine = good-fit {0.3,0.6,1.2}×{0.045,0.09} cells.
- **Curation registry shipped (§18):** `handouts/ch3_png_qa_curation.csv` is the single source of truth for hand-picked points; `scripts/ch3_4_dynamics_fits.py` reads + applies it (reproducible refits).
- **Next:** broaden the fit script beyond manifest candidates to do the **good-fit composition refit** over all PEO/LiTr cells (using the registry, incl. v151), publish clean per-cell τ/β; then write Ch3 or formalise the Ch4 model. Always match protocol + electrode + composition.
- **Caveats on current numbers:** "has measurement" = ≥1 pixel row in that type's `PIXEL_INFO`; the §1 coverage counts do **not** exclude flagged pixels (they are an upper bound), whereas the §6/§7 trend + clean-manifest counts **do**. Neither yet verifies a common protocol or replicate quality.
- **Flag granularity (verified 2026-06-03):** FILTERED exclusion is applied per `(device, day, pixel, measurement_type)`, **not** per device — a flag removes only that pixel's that-type aggregate. All **221 flags match a real measurement row (100%)**, partial flagging is preserved (e.g. NM_v009: 6 of 27 HYST pixels dropped, 21 kept), and including `day` is equivalent to `(device, pixel)` for the current flags. **Caveat — flagging is HYST-heavy: 207 HYST vs only 3 PULSES + 11 DELAYTIME flags.** FILTERED has screened almost nothing in PULSES/DELAYTIME, so the decay (τ/β) and potentiation fits must apply their **own** goodness-of-fit + read-disturb screening rather than rely on FILTERED.

---

## 1. Data coverage of the PEO/triflate corpus (the empirical basis)

Of 353 library devices, **149** are PEO host + triflate salt. Cation split is extremely lopsided:

| Cation | Devices (any data) | With all 3 common measurements |
| --- | ---: | ---: |
| **Li** | 143 | (≈37) |
| **Na** | **3** | 2 |
| **K** | **3** | 2 |

PEO/triflate devices with all three common measurements (≥1 pixel each in HYST + PULSES/N-pulse + DELAYTIME): **41 / 149**.

**Fixed-composition cation cell (PEO = 0.3, salt = 0.09):**

| Cation | Devices in cell | With all 3 |
| --- | ---: | ---: |
| Li | 57 | 11 |
| Na | 3 | 2 |
| K | 3 | 2 |

**PEO/LiTr composition grid** (devices / with-all-3), the concentration series:

| PEO ↓ \ salt → | 0.045 | 0.09 | 0.18 |
| --- | --- | --- | --- |
| 0.15 | 1 / 1 | 1 / 1 | 1 / 1 |
| 0.3 | 10 / 4 | **57 / 11** | 2 / 1 |
| 0.6 | 3 / 3 | 12 / 3 | 9 / 3 |
| 1.2 | 3 / 3 | 12 / 3 | 9 / 3 |

Plus two off-grid clusters with **zero** all-3 coverage: `PEO 0.37 / salt 0.055` (17 devices) and `PEO 0.42 / salt 0.03` (6 devices) — likely older partial/test batches (e.g. profilometry-only rpm sweeps); flagged for exclusion pending the depth audit.

---

## 2. What this means for scope (vs the planning docs)

1. **The Li/Na/K cation comparison cannot be a primary quantitative claim.** There are literally **3 Na and 3 K devices** (2 each with all three common measurements). This is at/below the ≥3-replicate-per-cell bar in `05` §2.3. It supports a *preliminary, explicitly-labelled* trend statement at most — exactly the caution `01`/`05` already mandate; this audit quantifies *why*.
2. **The composition (concentration) series is the strong Ch3 pillar.** The PEO/LiTr grid gives a genuine 2-D sweep (PEO 0.15→1.2, an 8× range; salt 0.045→0.18, a 4× range) with **n = 3 all-3 replicates** in each cell of the clean `{0.3,0.6,1.2} × {0.045,0.09,0.18}` block. Recommend foregrounding composition-driven dynamics as the quantitative core, with cation identity as a smaller, honestly-limited comparison.
3. **Coverage attrition is real:** only 41/149 PEO/triflate devices currently have all three common measurements. The eventual Chapter-4 manifest will be a fraction of "300+ generations"; plan around tens of devices, not hundreds.

---

## 3. Claims ledger (living)

Status key: ✅ supported by data · 🟡 limited / preliminary · 🔴 unsupported / out of scope · ⏳ needs analysis (coverage exists).

| # | Candidate claim | Chapter | Status | Evidence / why |
| --- | --- | --- | --- | --- |
| C1 | PEO/LiTr memristive response (switching window, potentiation) is tunable by composition | 3 (core) | ✅ | Coherent across HYST window (§6.2), potentiation steepness+peak (§8.2) and fading-memory t½ (§8.1): higher PEO → weaker response. n = 2–9 dev/cell. |
| C2 | Composition sets the fading-memory timescale in PEO/LiTr | 3→4 | ✅ | Model-free t½ composition-tunable ≈ 3–19 s, longest at PEO0.3/0.09; identified τ agrees (§8.1). **Corroborated by the pipeline's pre-computed exp-τ (corr 0.93–0.97; old τ reproduces the trend — §9).** The Ch4 timescale ladder. |
| C3 | Cation identity orders the dynamics Li > Na > K (timescale / retention) | 3 (secondary) | 🔴 | No universal ordering. Cleanest comparison (TMPE/TFSI, n=2 same batch, §14): **K shortest ~3.5 s < Li≈Na ~6–7 s**; but PEO/triflate (matched, n=1 Na/K) gave Li>K>Na and TMPE/triflate K-longest → families contradict. Dominant τ levers: potentiation amplitude ≫ host > anion > cation. Reframe as future subthreshold, protocol-locked, n≥3 cation series. |
| C4 | All three common measurements (I–V, N-pulse, delay) exist across the comparative corpus | 3/4 | 🟡 | True only for the Li composition grid; 41/149 overall, thin (n≤2) for Na/K. |
| C5 | EPSC / STDP / separated STM-LTM / impedance compared across Li/Na/K | 3/4 | 🔴 | Ch2 (Paper 1, SY/Hybrane/LiTf) only. Use as Li-only priors/sanity checks; never propagate to Na/K. (Matches `01`/`05`.) |
| C6 | Compact behavioural models (read fn, pulse update, decay) identifiable per composition cell | 4 | 🟡 | Per-cell parameters extracted (t½, retention, potentiation exp/peak/turnover; §8.5). Decay τ only ~half-identified at 8 pts; full φ(x) update + read transfer function still to formalise. |
| C7 | Heterogeneous reservoir / coincidence / filter-bank simulations grounded in measured cells | 4 | ⏳ | Depends on C1/C2/C6; the timescale spread to exploit is composition-driven (per §2), not cation-driven. |
| C8 | Devices show volatile fading memory (forgetting) and pulse potentiation across the corpus | 2/3/4 | ✅ | Delay slopes negative and pulse slopes positive in every cell tested (§6.3). Robust qualitative behaviour. |
| C9 | Large device-to-device / cycle variability — usable as heterogeneity for reservoir computing | 3/4 | ✅ | Feature sd ≈ mean across cells (§6); the t½ ladder (≈3–19 s, §8.1) is a concrete heterogeneity resource. |
| C10 | Potentiation saturates / reverses (turnover) at high N — caps usable pulse count | 3/4 | ✅ | ~half the cells peak then decline by N=1000 (§8.2); sets a safe operating range for Ch4 pulse protocols. |
| C11 | Anion (triflate vs TFSI) and host (PEO vs TMPE) modulate retention τ more strongly than cation | 3 | 🟡 (illustrative) | Anion: PEO/Tr τ≈20 s vs PEO/TFSI τ≈1 s. Host: Ag-matched PEO/LiTr τ≈20–25 s (n=3) vs TMPE/LiTr τ≈3.8 s (n=1) — ~6× (§15). Real, directionally clear effects, but **n≤2 on a side once electrode+protocol matched (§16)** → illustrative, not powered. |
| C12 | Potentiation amplitude (write/read protocol) dominates apparent retention τ | 3 (method) | ✅ | Same device v114: τ 4.6 s (3 V write/1.5 V read) → 15.5 s (6 V/3 V); #pulses (30) & timing (0.103 s) constant, write/read voltages locked (§13). Cross-device τ must use one matched protocol; ideally subthreshold read. Higher write drives more ion/electrode processes → deeper, longer-lived state. |

---

## 4. Analysis backlog

- [ ] Na/K depth audit: per device, pixel count, flagged %, measurement days, and whether HYST/N-pulse/delay share a common protocol (sweep rate, V_write, Δt range) with the Li cells.
- [ ] PEO/LiTr grid quality: confirm n=3 all-3 per cell survives flag-exclusion; check measurement-day spread (aging confound).
- [ ] Trend tests (exclude FILTERED first):
  - HYST: on-off ratio, normalized loop area, activation voltage vs (PEO, salt) and vs cation.
  - PULSES: ΔG/G₀ saturation curve vs composition / cation.
  - DELAYTIME: decay time constant (stretched-exp τ, β) vs composition / cation — the central fading-memory claim.
- [ ] Decide and freeze the Chapter-4 device manifest subset (`05` §2.3 columns).
- [ ] Cross-check off-grid clusters (0.37/0.055, 0.42/0.03) — include, relabel, or exclude.

## 5. Reproducibility

Coverage numbers and [`ch3_ch4_device_inventory.csv`](ch3_ch4_device_inventory.csv) were produced by an ad-hoc Python pass over the DATABASE CSVs on 2026-06-03 (pandas-free, stdlib `csv`). When this is promoted to a committed script it should live at `scripts/` (thesis repo) or `scripts_general/chapter4_pipeline.py` (`05` §5.1) and take the inventory/manifest as output.

---

## 6. First-pass trend findings (2026-06-03)

**Method & caveat.** Features aggregated per cell from the DATABASE tables, **excluding FILTERED (erratic) and `is broken` pixels**. HYST uses the pre-extracted `*_PIXEL_INFO` features. DELAYTIME/PULSES use a *crude* per-device slope — a linear fit of `ratio` vs `log₁₀(delay s)` (forgetting → negative) and `ratio` vs `log₁₀(N pulses)` (potentiation → positive). These are **rough directional indicators only**: not normalized, not protocol-matched, not stretched-exponential fits. Magnitudes are unreliable; proper τ/β decay fits and saturating-update fits on protocol-matched subsets are the Chapter-4 pipeline job.

### 6.1 HYST — cation cell (PEO 0.3 / salt 0.09), clean pixels

| Cation | devices | pixels | on-off ratio | \|norm. area\| | activation V |
| --- | --: | --: | --- | --- | --- |
| Li | 19 | 79 | 3.67 ± 1.73 | 0.31 ± 0.14 | 2.29 ± 0.86 |
| Na | **1** | 4 | 1.65 ± 0.12 | 0.11 | 2.37 |
| K | **1** | 2 | 4.08 ± 0.18 | 0.33 | 2.38 |

After flag/broken exclusion the cation comparison collapses to **n = 1 device each for Na and K** (one of the two "all-3" devices per cation had its HYST pixels flagged or broken). Activation voltage ≈ 2.3–2.4 V for all three; on-off ratio does **not** follow Li>Na>K. → no quantitative cation claim from HYST.

### 6.2 HYST — PEO/LiTr composition grid, clean pixels

on-off ratio / |norm. area| (device count); activation V ≈ 2.2–2.4 V everywhere with no composition trend:

| PEO ↓ \ salt → | 0.045 | 0.09 | 0.18 |
| --- | --- | --- | --- |
| 0.15 | 2.0 / 0.05 (1) | — | — |
| 0.3 | 7.8 / 0.50 (4) | 3.7 / 0.31 (19) | 2.4 / 0.24 (2) |
| 0.6 | 2.1 / 0.12 (3) | 3.5 / 0.21 (6) | 3.0 / 0.24 (3) |
| 1.2 | 1.9 / 0.09 (3) | 2.5 / 0.18 (6) | 2.4 / 0.19 (3) |

At fixed salt 0.09 the switching window (on-off, area) **decreases as PEO rises** 0.3→1.2; the `PEO0.3/salt0.045` cell is a standout (on-off ≈ 7.8, area ≈ 0.5). Spreads are large (sd ≈ 30–50 % of mean) and the surface is not cleanly monotonic.

### 6.3 DELAYTIME (forgetting) & PULSES (potentiation) slopes

| Cell | delay slope d(ratio)/d(log₁₀ s) | pulse slope d(ratio)/d(log₁₀ N) |
| --- | --- | --- |
| Li 0.3/0.09 | −19.2 ± 40.5 (n=10) | +25.6 ± 24.9 (n=11) |
| Na 0.3/0.09 | −10.3 ± 9.8 (n=2) | +7.3 ± 5.2 (n=2) |
| K 0.3/0.09 | −30.4 ± 4.7 (n=2) | +22.5 ± 9.4 (n=2) |
| Li PEO0.6/0.09 | −19.3 ± 10.2 (n=3) | +66.4 ± 29.1 (n=3) |
| Li PEO1.2/0.09 | −9.3 ± 8.5 (n=3) | +15.6 ± 13.0 (n=2) |

- **Qualitative behaviour holds everywhere:** delay slopes negative (forgetting), pulse slopes positive (potentiation) → supports C8.
- **Cation ordering Li>Na>K not supported:** n=2 for Na/K, Li sd > |mean|, and point estimates don't follow the predicted order (Na slowest, K fastest).
- **Variability is large** (sd ≈ mean throughout) → supports C9 (heterogeneity resource), not a defect.

### 6.4 Strategic implication for Chapter 3

Lead with **composition (PEO/LiTr concentration series)** as the quantitative spine; present **cation identity (Li/Na/K) as an honestly-limited, n≤3 preliminary observation** that motivates future work — exactly the delimited "side evidence" framing in `01`/`05`. The volatile-forgetting + potentiation behaviours and the large heterogeneity are the durable, defensible through-line into Chapter 4.

---

## 7. Clean manifest candidates (2026-06-03) — `ch4_device_manifest_DRAFT.csv`

Re-counting with **clean all-3** (flag-excluded everywhere; HYST also `is broken`-excluded) and stratum tags yields **31 manifest-candidate devices** ([`ch4_device_manifest_DRAFT.csv`](ch4_device_manifest_DRAFT.csv), `manifest_candidate=1`). This is the realistic curated set — tighter than the loose §1 coverage, and the basis for the eventual frozen `05` manifest.

**Cation cell (stratum B, PEO 0.3 / salt 0.09), clean all-3:** Li = **9**, Na = **1**, K = **1**. Confirms C3 cannot be quantitative (n=1 per non-Li cation).

**Composition design (stratum A, Li), clean all-3 device counts:**

| PEO ↓ \ salt → | 0.045 | 0.09 | 0.18 |
| --- | --: | --: | --: |
| 0.3 | 4 | 9 \* | 0 |
| 0.6 | 3 | 3 | 2 |
| 1.2 | 3 | 2 | 3 |

\* The 0.3/0.09 reference is tagged stratum B but is shared by both designs. The PEO 0.15 row and the PEO 0.3 / salt 0.18 cell have **no** clean all-3 device and drop out.

This supports a defensible **2-axis composition design with replicates**: a **PEO sweep** (0.3→0.6→1.2) at fixed salt (clean columns at salt 0.045 and 0.09) **and** a **salt sweep** (0.045→0.09→0.18) at fixed PEO (clean rows at PEO 0.6 and 1.2), n ≈ 2–4 devices each. That is the quantitative spine for Chapters 3–4; cation identity rides along as n ≤ 1-per-cation honest side evidence. **Caveat:** `passed_read_disturb` and common-protocol checks are not yet done — both required by `05` before the manifest is frozen.

---

## 8. Quantitative dynamics — model identification (2026-06-03)

Artifacts: [`ch4_decay_fits.csv`](ch4_decay_fits.csv), [`ch4_pulse_descriptors.csv`](ch4_pulse_descriptors.csv); reproducible via `scripts/ch3_4_dynamics_fits.py`. DELAYTIME restricted to the common **2.0 V read** protocol (grid 1–300 s); PULSES at **1.5 V** (grid N = 1–1000).

**Why t½, not τ.** The stretched-exponential `A·exp[−(t/τ)^β]+C` is only **identified in 16/30** delay curves — with 8 points, β and τ trade off and several fits collapse to τ→0. So the **primary timescale is a model-free half-enhancement time `t½`** (log-interpolated delay at which the conductance enhancement halves); the identified τ agrees with t½ where it converges, and is reported as secondary.

### 8.1 Fading-memory timescale is composition-tunable (Li, model-free `t½`)

| PEO ↓ \ salt → | 0.045 | 0.09 | 0.18 |
| --- | --- | --- | --- |
| 0.3 | 15.8 s (n=4) | **19.2 s (n=8)** | — |
| 0.6 | 3.3 s (n=3) | 3.5 s (n=3) | 5.5 s (n=2) |
| 1.2 | 2.7 s (n=3) | 5.5 s (n=2) | 9.0 s (n=3) |

At fixed salt, t½ drops sharply from PEO 0.3 (longest, ~16–19 s) to PEO 0.6/1.2 (~3–9 s) → a composition-tunable fading-memory time over ≈ **3–19 s (≈6×)**. retention@60 s mirrors it (0.41 at the PEO0.3/0.09 reference vs 0.02–0.13 at higher PEO).

### 8.2 Potentiation strength decreases with PEO (PULSES)

| Cell (Li) | growth exp (log-log) | peak ratio | turnover |
| --- | --- | --- | --- |
| PEO0.3/0.045 | 1.11 (n=4) | ~480 | yes |
| PEO0.3/0.09 | 0.75 (n=9) | ~102 | rare |
| PEO0.6/* | 0.57–0.83 | 15–200 | mixed |
| PEO1.2/* | 0.33–0.49 | 4–43 | mixed |

Both the potentiation steepness (growth exponent) and the peak conductance gain fall as PEO rises. ~Half the cells show **turnover** — ratio peaks then declines by N=1000 (over-potentiation/degradation), which caps the usable pulse count.

### 8.3 Coherent composition story (all three measurements)

HYST window (§6.2), potentiation (§8.2) and fading-memory time (§8.1) all point the same way: **higher PEO mass fraction → weaker memristive response and faster forgetting.** This is the quantitative spine of Chapter 3 (n = 2–9 devices/cell), and the t½ spread plus device-to-device scatter give Chapter 4 a genuine heterogeneous fading-memory bank.

### 8.4 Cation Li/Na/K (n=1 Na, n=1 K) — preliminary only

`t½`: Li 19.2 s (n=8) · Na 27.4 s (n=1) · K 8.0 s (n=1). K is shortest (consistent with weakest cation–oxygen coordination → least retention), but Na > Li contradicts a strict Li>Na>K order. At n=1 for Na/K this is anecdotal — a motivating preliminary observation, not a result.

### 8.5 Parameter set now available for Chapter 4 models

Per composition cell: fading-memory `t½` (and identified τ where available), `retention@60 s`, potentiation `growth exponent` + `peak gain` + `turnover-N`. These seed the per-cell behavioural model (read function / pulse update φ / decay λ): the ~3→19 s timescale ladder is the resource for heterogeneous reservoir computing; the turnover-N sets the safe operating range. **Still to do for a full Ch4 model:** formalise φ(x) (state-dependent update) and a read transfer function, and quantify cycle-to-cycle vs device-to-device variance separately.

---

## 9. Cross-validation against pipeline pre-computed features (2026-06-03)

The DATABASE `PIXEL_INFO` tiers already carry pipeline-computed features from years ago — DELAYTIME `exp decay: tau (s)` (a **simple**-exponential fit) and `max ratio`; PULSES `max ratio`, `number of pulses at saturation`, `is pixel saturated`. Checking my fresh analysis against them:

**DELAYTIME (30 matched pixels).**

- my `r1` ≡ pipeline `max ratio`: corr **1.000** (data join verified).
- my model-free `t½` vs pipeline `exp-τ`: corr **0.93**; my identified stretched-τ vs pipeline `exp-τ`: corr **0.97** → independent methods agree on the timescale.
- median `t½/τ_pipeline` ≈ **0.95** (not the 0.69 of a pure single-exponential) ⇒ the decays are **stretched** (Kohlrausch, β<1); the pipeline's single-exp τ is an *effective* constant. Consistent with Paper 1's stretched-exponential retention.
- **The pipeline's τ (computed long ago) independently reproduces the composition trend:** PEO0.3 ≈ 21–25 s (longest) → PEO0.6/1.2 ≈ 1.5–10 s. ⇒ strongly corroborates C2.

**PULSES (31 matched pixels).**

- my `peak_ratio` ≡ pipeline `max ratio`: corr **1.000**.
- my `N_peak` ≡ pipeline `number of pulses at saturation`: corr **1.000**, exact match on all 13 pixels where the pipeline recorded one ⇒ corroborates the peak/turnover (C10).
- **Discrepancy (definitional, not a contradiction):** pipeline `is pixel saturated` = False for *all* matched pixels, although 42 % show turnover and the pipeline itself recorded a saturation-N for many. Its *numeric* saturation agrees with mine; its *boolean* flag uses a stricter/unpopulated criterion. Don't rely on `is pixel saturated`; use `number of pulses at saturation` (or my turnover).

**Verdict.** The freshly-extracted findings are **consistent with, and corroborated by, the pipeline's pre-computed values** — the fading-memory composition trend is reproduced by two independent computations. For Chapter 4, the pipeline's per-pixel `exp decay: tau (s)` can be used directly as a complementary timescale estimate (available for the full 117 DELAYTIME pixel rows, beyond my fitted subset).

---

## 10. Decay parameters aligned to the thesis & pipeline (τ, β) — adopt going forward

**Canonical model = Kohlrausch stretched exponential** (Ch2 `eq:kohlrausch`, identical symbols):

ΔG(t) = ΔG₀·exp[−(t/τ)^β] + ΔG∞ — **τ** = characteristic relaxation time, **β** = stretch exponent (0<β≤1), ΔG₀ initial change, ΔG∞ residual. Paper 1: τ_S ≈ 2.5–3 s (STM), τ_L ≈ 4.7 s (LTM).

The pipeline `exp decay: A / tau (s) / y0` is the **β = 1 special case** (ΔG₀ / τ / ΔG∞). **Decision (more useful going forward): report τ + β; use the pipeline τ as the primary value** (stable, already computed for all 117 delay pixels), with β from stretched fits to capture the multi-timescale character; the model-free t½ of §8 is kept only as a robustness cross-check (t½ ≈ τ here).

Per-cell **τ (pipeline, β=1)** for the Li PEO grid — replaces t½ as the headline, same trend, now in thesis units:

| PEO ↓ \ salt → | 0.045 | 0.09 | 0.18 |
| --- | --- | --- | --- |
| 0.3 | 25.0 s (n=4) | **19.6 s (n=11)** | — |
| 0.6 | 1.9 s (n=3) | 4.1 s (n=3) | 5.0 s (n=3) |
| 1.2 | 1.5 s (n=3) | 6.2 s (n=3) | 10.4 s (n=3) |

β is mostly **0.6–0.9 (< 1)** → stretched/multi-timescale within a *single* device (matches the "distribution of activation barriers" reading in Ch2). Context: PEO0.3 (τ ≈ 20–25 s) sits *beyond* the Paper-1 LTM (4.7 s), while high-PEO cells (τ ≈ 2–5 s) sit in the STM range — composition tunes the device across the STM↔LTM ladder (cross-host comparison, qualitative).

---

## 11. Cation comparison — expanded candidates & cross-family τ (2026-06-03)

The strict PEO/triflate clean-all-3 set gave only n=1 Na/K (§7). Broadening to **all hosts (PEO, TMPE) × anions (Tr, TFSI)** at fixed 0.3/0.09 yields ~2 devices per (host, anion, cation) and, importantly, **three *designed* same-batch Li/Na/K sets**:

- **2023-10 (triflate):** PEO v247(Li)/v248(Na)/v249(K) + TMPE v250(Li)/v251(Na)/v252(K) — all carry EIS. Cleanest matched comparison.
- **2025-03 (PEO·TFSI):** v321/322(Li), v323/324(Na), v325/326(K). n=2 each, clean, 2.0 V.
- **2025-05 (TMPE·TFSI):** v333/334(Li), v335/336(Na), v337/338(K). n=2 each, clean, 2.0 V.

**Cross-family τ (pipeline, s) at 0.3/0.09:**

| Family | Li | Na | K |
| --- | --- | --- | --- |
| PEO · triflate | 19.6 (n=11) | 19.2 (n=2) | 20.4 (n=2) |
| PEO · TFSI | 1.0 (n=2) | 1.5 (n=2) | 0.3 (n=2) |
| TMPE · triflate | 3.6 (n=6) | 3.2 (n=2) | 7.7 (n=2) |
| TMPE · TFSI | 6.3 (n=2) | 7.0 (n=2) | 3.5 (n=2) |

**Verdict: no consistent Li>Na>K ordering**, even with the expansion. PEO/triflate shows ~equal τ (~20 s) across cations; the dominant effects are **anion** (PEO/Tr ~20 s vs PEO/TFSI ~1 s) and host/composition. The only repeatable cation hint is **K shortest in the TFSI families**. This is a more rigorous basis than n=1 anecdote — it points to a *negative/nuanced* result (cation effect weak, anion/host-dependent), which is itself defensible.

**Caveats (to settle by PNG review):** v115/v116 (old PEO/Tr Na/K) are flagged ×6 and read at **3.0 V** (off-protocol vs 2.0 V) → their long τ (30–38 s) is suspect. Most Na/K devices have only **1 delay pixel**. Au-electrode TMPE devices (v298, v300/301/304/305/306) lack pulse/delay data. **Next:** user reviews PNGs for the three designed batches; if decays are clean, report "no robust cation ordering across n=2×3 batches; anion/host/composition dominate" (a real finding), and possibly "K shortest with TFSI". Then C3 is resolved (not merely scraped).

---

## 12. PNG QA + cleaned fits — 2023-10 designed batch (user review 2026-06-03)

The user visually inspected the per-pixel PNGs of the 2023-10 set. Verdicts and refits (delay refit in thesis τ units; **v248** refit with the two outlier points t=10 s and t=300 s removed):

| Device | Chem | DELAY (cleaned fit) | PULSES | HYST |
| --- | --- | --- | --- | --- |
| v247 | PEO-Li | **broken** — flat/noisy, R²=0.17 → discard | erratic (barely rises) → discard | ~open-circuit → discard (flag device) |
| v248 | PEO-Na | usable after dropping t=10,300 s: **τ≈3.0 s** (R² 0.76→0.88); weak (max ratio 2.7) | weak; flat to 300, jump at 1000 | "pointy banana" (atypical) |
| v249 | PEO-K | clean, **τ≈10.7 s** (R²0.91) | mountain; turnover by 1000 | fine |
| v250 | TMPE-Li | clean, **τ≈3.8 s** (R²0.93) | sensible rising | fine |
| v251 | TMPE-Na | clean, **τ≈5.0 s** (R²0.99, β≈0.42) | strong to 300 (~600), turnover | broad/round (ideal) |
| v252 | TMPE-K | clean, **τ≈6.7 s** (R²0.96) | sharp to 300, turnover | fine |

**Data-quality lessons.** (i) The pipeline's stored τ is **not robust to outliers**: v248 stored 0.95 s vs cleaned 3.0 s. Key devices should be **refit after point-level QA**, not taken from `exp decay: tau` blindly. (ii) v247 is dead across all three → recommend flagging it (it sits in the n=11 PEO/Tr Li anchor but contributes only HYST there). (iii) v115/v116 stay excluded (flagged, 3.0 V).

**Cleaned cation comparison (2023-10, triflate).**

- **PEO/triflate:** Li ≈ **20 s** (n=11 pool) > K ≈ **10.7 s** (v249) > Na ≈ **3.0 s** (v248). Li retains longest — directionally consistent with strongest Li–O binding (HSAB) — but **Na < K breaks strict Li>Na>K**, and Na/K are n=1.
- **TMPE/triflate:** Li 3.8 ≈ Na 5.0 ≈ K 6.7 s — **clustered within device scatter, no ordering** (Li even shortest).

**Verdict.** The two hosts disagree on magnitude (PEO-Li ~20 s vs TMPE-Li ~3.8 s) *and* cation order → **no robust host-independent Li>Na>K**. What we can claim now: (a) clean (stretched-)exponential fading memory in 5/6 devices; (b) host & composition strongly tune τ (the headline); (c) *within PEO/triflate*, Li retains longest among the cations measured (weak — n=1 Na/K — consistent with HSAB). What we cannot: a universal Li>Na>K law. **Pulses** add a separate point: same-cation devices differ wildly by host (v248 PEO-Na weak vs v251 TMPE-Na ratio ~600) → potentiation is host- and device-specific, not a cation signature.

---

## 13. Write/read protocol-amplitude confound + the matched-protocol comparison (2026-06-03)

User point-selection salvaged the old 2022 PEO/triflate devices (clean fits): **v114 Li τ=14.4 s, v115 Na τ=34.0 s, v116 K τ=27.1 s** (R²≥0.96). Pulling the **full delay protocol** (`DELAYTIME_PIXEL_INFO`: reading voltage, pulse voltage, number of pulses, timing) then reframed the confound. Number of potentiation pulses (**30**) and inter-pulse timing (**0.103 s**) are **constant across the whole archive**; the only variable is amplitude, and write/read voltages are *locked together*:

| protocol | pulse V (write) | read V | devices |
| --- | --- | --- | --- |
| low | 3.0 V | 1.5 V | v114 (day 2) |
| **standard** | **4.0 V** | **2.0 V** | entire 2023–2025 corpus (~30 devices) |
| old | 6.0 V | 3.0 V | 2022 batch: v114/115/116, v120/121/122 |

Decisive evidence — **same device v114 at two amplitudes: τ = 4.6 s (3 V write / 1.5 V read) → 15.5 s (6 V write / 3 V read)**. Higher potentiation drives more ion displacement (and at 6 V likely electrode reactions) → a deeper, longer-lived written state; the suprathreshold read (>0.7 V threshold) compounds it. **The potentiation amplitude is the dominant lever on apparent τ, not the cation** (the earlier "read-voltage flip" was really 4 V vs 6 V write).

**Fix — compare only within the matched standard protocol (4 V write / 2 V read):**

| family (4 V/2 V) | Li (clean) | Na | K |
| --- | --- | --- | --- |
| PEO · triflate | ~20 s (v140 19.6, v146 23, v241 25, v269 8.7, v270 7.9) | 3.0 (v248) | 10.7 (v249) |
| TMPE · triflate | ~3 s (v250 3.8, v291 3.4, v314 3.0, v315 2.7) | 5.0 (v251) | 6.7 (v252) |
| PEO · TFSI | 0.4–1.6 (v321/322) | 1.0–2.0 (v323/324) | 0.1–0.5 (v325/326) |
| TMPE · TFSI | 3.7–9.0 (v333/334) | 6.6–7.5 (v335/336) | 3.2–3.7 (v337/338) |

At matched protocol: **PEO/triflate → Li (~20 s) > K (10.7) > Na (3.0)** — Li retains longest (HSAB-consistent), though Na<K breaks the strict order and Na/K are n=1. It does **not** generalise: TMPE/triflate is a flat ~3–7 s cluster, PEO/TFSI all sub-2 s, TMPE/TFSI ~3–9 s. **Host and anion dominate; cation is a weak, non-universal effect even at matched protocol.**

**Caveats:** pipeline τ has many bad fits even at matched protocol (v266 0.1 s, v267 2040 s, v268 79 s, v294 74 s, v120 2×10⁵ s) → per-device QA is mandatory before trusting any τ. Na/K stay n=1 per matched-protocol family.

**Scope note (unchanged):** §8/§10 **composition** used uniform 4 V/2 V, so that headline result is *not* affected — only the **cation** comparison was confounded (it mixed 4 V and 6 V batches).

---

## 14. TFSI-batch QA + the cleanest cation comparison (2026-06-03)

User PNG review of the 2025 TFSI batches:

- **PEO/TFSI collapses:** only **v321** (Li) usable — refit on points {1,2,5,10,60,300 s} → τ≈**0.4 s** (R²=0.99). v322 flat/broken; **v323/v324 (Na) and v325/v326 (K) are not proper decays** → discard. So *no* PEO/TFSI cation comparison.
- **TMPE/TFSI (v333–338) all clean** (R²≥0.97) → the **only n=2-per-cation, same-batch, matched-protocol (4 V/2 V) cation comparison** in the archive:

| TMPE/TFSI (4 V/2 V) | τ (devices) | median | shape |
| --- | --- | --- | --- |
| Li | v333 9.0, v334 3.7 | 6.3 s | stretched (β≈0.8–0.9) |
| Na | v335 7.5, v336 6.6 | 7.0 s | sharp/compressed |
| K | v337 3.7, v338 3.2 | **3.5 s** | sharp/compressed |

**Result: K shortest (~3.5 s) < Li ≈ Na (~6–7 s)** — consistent with the weakest K⁺–ether-oxygen coordination (HSAB), but Li/Na indistinguishable (no full Li>Na>K).

**Does not reconcile across families:** TMPE/triflate (n=1) had K *longest* (6.7 s vs Li 3.8, Na 5.0); PEO/triflate (n=1 Na/K) had Na shortest, K middle, Li longest. So **"K shortest" is a TFSI-only pattern, not robust.**

**Host effect (fixed Li/TFSI):** PEO-Li-TFSI (v321) ≈ 0.4 s vs TMPE-Li-TFSI ≈ 6.3 s → **~15× longer in TMPE**. Host strongly modulates τ.

**Net cation verdict (all evidence).** No cation ordering is robust across host × anion. The single highest-quality comparison (TMPE/TFSI, n=2, same batch) gives **K shortest, Li≈Na** — reportable as the best available datapoint *if* explicitly caveated that triflate families contradict it. **Dominant τ levers, in order: potentiation amplitude ≫ host > anion > cation.** Curve shapes also vary (TFSI Na/K are compressed "cliff" decays, β≈2; triflate/PEO are stretched, β<1) — a heterogeneity in relaxation form worth noting for Ch4.

---

## 15. Host comparison: PEO vs TMPE for triflate (2026-06-03)

Better-supported than any cation cell, because both hosts have multiple Li devices. Matched protocol (4 V/2 V, 0.3/0.09), per-device simple-exp fits with QA (R²≥0.90, plausible τ, real signal max ratio > 2):

| host (Li-triflate) | QA-clean τ (s) | n | signal (max ratio) |
| --- | --- | --- | --- |
| PEO/LiTr | 8.7, 19.6, 23.2, 25.1, 67, 79 → median **~24 s** | 6 | strong (4–79×) |
| TMPE/LiTr | v250 3.8 clear; v291 3.4 / v314 3.0 / v315 2.7 weak | 1 clear + ~3 weak | weak (1.5–10×) |

**Finding:** **PEO/LiTr retains ~6× longer (τ ≈ 20–25 s) than TMPE/LiTr (τ ≈ 3.8 s).** ⚠️ **Correction (per §16 audit):** the "n=6 PEO" above mixed **3 Ag (v140 19.6, v146 23.2, v241 25.1 — tight) + 3 Au (v265 67, v268 79, v269 8.7)**; the wide 9–79 s spread was largely the **Au** devices. Electrode-matched **Ag-only PEO/LiTr is n=3 (~20–25 s, tight)** vs TMPE/LiTr Ag **n=1 (v250 3.8 s)** — v291/v314/v315 are also Au. So the host effect (~6×) holds directionally but rests on n=3 (Ag PEO) vs n=1 (Ag TMPE), not n=6. Na/K host pairs n=1, mixed. **Host is a real but n-limited (illustrative) axis — see §16.**

---

## 16. Coverage audit (step A) — what each axis can actually claim (2026-06-03)

Clean all-3 (flag- and broken-excluded) device counts per cell, SY-based, **Ag electrode, 0.3/0.09** unless noted. Full matrix: [`ch3_coverage_audit.csv`](ch3_coverage_audit.csv).

**Axis 1 — Composition (PEO/LiTr/Ag), peo × salt:**

| PEO ↓ \ salt → | 0.045 | 0.09 | 0.18 |
| --- | --: | --: | --: |
| 0.3 | 4 | 4 | 0 |
| 0.6 | 2 | 3 | 2 |
| 1.2 | 3 | 2 | 3 |

→ a genuine **3×3 grid, n=2–4/cell** (PEO0.15 row and PEO0.3/0.18 empty). **The only axis with real replication.**

**Axis 2 — Cation @0.3/0.09/Ag (Li / Na / K):** PEO/Tr 4/1/1 · PEO/TFSI 1/1/1 · TMPE/Tr 1/2/2 · **TMPE/TFSI 2/2/2** (best). No cell reaches n≥3 for all cations.

**Axis 3 — Host @0.3/0.09/Ag (PEO vs TMPE):** Tr/Li **4 vs 1** · TFSI/Li 1 vs 2 · Na/K 1–2 each. No host pair has n≥3 on both sides.

**Axis 4 — Anion @0.3/0.09/Ag (Tr vs TFSI):** PEO/Li **4 vs 1** · TMPE/Li 1 vs 2 · Na/K 1–2 each.

**Electrode confound:** 7 Au-electrode all-3 devices (v265, v268, v269, v270, v291, v314, v315) — keep **separate** from Ag (this corrected §15).

**See §17 for a delay-fit quality scan** that flags which devices need the v248-style point-level double-check (esp. low-n cells), and tightens the composition grid to *good-fit* coverage.

**Verdict for the rework.** Only **composition (PEO/LiTr/Ag/4 V)** sustains real replication (n=2–4 across a 3×3 grid) — it is the **only statistically-claimable quantitative axis**. **Host, anion, and cation are all n≤2 on at least one matched side** → present them as *illustrative trends/observations with explicit n*, not as powered claims. Best comparison cell anywhere = TMPE/TFSI cation (2/2/2). This argues for a disciplined reframe: composition-led quantitative spine + a clearly-labelled qualitative "chemical-tuning landscape" (host/anion/cation), **not** four co-equal first-class axes. Confounds to hold fixed in any τ comparison: protocol amplitude (§13), electrode (§16), composition.

---

## 17. Delay-fit quality scan — which decays need the v248-style double-check (2026-06-03)

Scanned every claim-relevant delay curve (64 device·day·pixel groups) with a simple-exp fit; **flagged if R²<0.90, or τ∉[0.3,300] s, or max ratio <3** (weak signal → τ ill-defined). 24 flagged.

**Validation:** the flag reproduces the user's PNG verdicts on all 10 already-reviewed devices — v322/v323/v324/v325/v326 ("not proper decays") R²≈0; v247 (broken) R²=0.17; v248/v114/v115/v116 (the ones we cleaned) all flagged. ⇒ the flag is reliable for the un-reviewed devices.

**High priority — rescue candidates (real signal, bad fit, not yet reviewed):**

| device | cell | maxR | R² | why check |
| --- | --- | --: | --: | --- |
| **v149** | PEO/LiTr 0.15/0.09 Ag | 9.1 | 0.00 | strong signal, terrible fit → bad points; best rescue |
| **v148** | PEO/LiTr **0.3/0.18** Ag | 3.8 | 0.00 | would fill a composition cell empty in the clean grid |
| v151 | PEO/LiTr 0.15/0.18 Ag | 4.2 | 0.89 | borderline |

**Not worth it (near-flat, maxR<3 → no real decay):** v150, v153, v154, v120 (broken, 6 V), v294, v314, v315.

**Au-electrode (separate confound set, §16):** v266, v267, v270 (maxR 8.9, rescuable if Au sub-analysis), v291.

**Implication for the composition spine.** "Has all-3" (§16) over-counts usable τ: the **PEO 0.15 row and salt-0.18 column are mostly flat/bad fits**. The robust composition τ result rests on the **PEO {0.3, 0.6, 1.2} × salt {0.045, 0.09}** cells. Action: PNG-check v149 / v148 (could rescue 0.15/0.09 and 0.3/0.18); otherwise present the grid as good-fit-only with honest per-cell n. Any quantitative composition τ should come from a refit over **good-fit** devices, not the raw "has-data" set.

**Rescue outcome (PNG review, 2026-06-04 — recorded in §18 registry):** v149 delay **and** pulses discarded (erratic beyond repair); v148 delay discarded but **pulses kept** (more defensible); **v151 delay salvageable** (keep 2/5/10/60/300 s; pulses discarded). Net: the PEO0.15 row and the 0.3/0.18 delay cell stay thin (v151 partially fills 0.15); the composition τ spine remains the {0.3,0.6,1.2}×{0.045,0.09} cells.

---

## 18. Curation registry — single source of truth for hand-picked points (2026-06-04)

**Gap closed.** Until now the PNG-derived point selections lived only as prose (§12–§17). They are now consolidated in a machine-readable registry — **`handouts/ch3_png_qa_curation.csv`** — one row per (device, measurement_type): `verdict` (use / clean / discard), `kept_points` (hand-picked delay-times in s, or pulse counts), `day`, `pixel`, `reviewer`, `date`, `notes`. **`scripts/ch3_4_dynamics_fits.py` now reads and applies it** (discard → drop the curve; clean → keep only listed points; use/absent → all points), so every refit is reproducible from the registry rather than from scattered notes.

Captured so far (all PNG-reviewed): 2023-10 batch (v247–v252), old PEO/Tr (v114/115/116), TFSI batches (v321–v326, v333–v338), and the §17 rescue candidates (v148/v149/v151). Verified applied: v248's decay now refits on its 6 cleaned points; discarded curves are dropped.

**Maintenance rule:** when a new device is PNG-reviewed, add a registry row and re-run the script — the per-cell τ/β and potentiation summaries update automatically. Note: for weak-signal devices (e.g. v248, max ratio ≈2.7) the model-free `t_half` and the exp-`τ` can diverge (≈24 s vs ≈3 s) — a further reason those n=1 cells are illustrative only.

## 19. Broadened composition refit — full PEO/LiTr/Ag population + v151 (2026-06-04)

**Change.** `scripts/ch3_4_dynamics_fits.py` previously built its composition `cell` map from `manifest_candidate==1` only. It now includes **all** PEO/LiTr/Ag devices (chemistry-landscape cells still come from manifest candidates), so the curation-salvaged low-concentration row enters the spine. Data-availability + FILTERED + curation `discard` + the quality screen filter the rest downstream, so broadening is safe — in practice the only new contributor is **v151** (the bulk of non-candidates, v092–103 / v164–175, carry no DELAYTIME/PULSES data; v247 is a curation `discard`).

**New honesty gate.** A reported stretched-`τ` now also requires **n ≥ 6** points (keeps ≥ 2 dof on the 4-parameter fit). v151's curated 5-point decay therefore contributes the **model-free `t½` only**, not an over-fitted `τ`. (The `clean`-curve floor for *entering* the fit was lowered 6 → 5 so v151's 5 hand-picked points are admitted at all.)

**Result — composition spine now spans 4 PEO levels (Li, Ag, 4 V/2 V), `t½` median:**

| salt \ PEO | 0.15 | 0.3 | 0.6 | 1.2 |
|---|---|---|---|---|
| 0.045 | — | 15.8 (n=4) | 3.3 (n=3) | 2.7 (n=3) |
| 0.09  | — | 19.2 (n=8) | 3.5 (n=3) | 6.0 (n=3) |
| 0.18  | 22.4 (n=1, v151) | — | 5.5 (n=2) | 9.0 (n=3) |

Identified `τ`: PEO0.3 ≈ 24–26 s (β 0.64–0.82) → PEO0.6 ≈ 3–4.6 s → PEO1.2 ≈ 7–10 s. The **lower-PEO → longer-retention** trend holds and v151 (22.4 s, the longest single cell) **extends** it to PEO 0.15 — corroborating, not part of, the replicated grid. Newly filled pulse cell PEO0.3/salt0.18 (v141+v148, n=2): weak, peak ≈ 3.8, no turnover — consistent with the "more dilute SY → weaker potentiation" reading. Chapter 3's stated numbers (2–20 s; PEO0.3 longest ≈19 s; τ≈20–25 s; β 0.6–0.9) are unchanged by the refit.

**New artifacts (single source for figures):** `handouts/ch3_decay_by_cell.csv`, `handouts/ch3_pulses_by_cell.csv` (per-cell medians with n_dev / n_identified).

## 20. Chapter-3 figures generated + HYST median-vs-mean correction (2026-06-04)

**`scripts/ch3_figures.py`** produces the three Ch3 figures into `figures/chapter3/` (composition_heatmaps, chemistry_landscape, protocol_overlay), wired into `chapters/chapter3_comparative.tex` (placeholders replaced; builds standalone + in thesis, exit 0).

- **Composition heatmaps** recompute the HYST window metrics from DATABASE (FILTERED + broken excluded; device-median-of-curve-medians) and read `t½` from `ch3_decay_by_cell.csv`. Each cell annotated with value + n.
- **HYST aggregation correction.** The on-off-ratio distribution is strongly right-skewed (e.g. PEO0.3/salt0.045: median **3.4**, mean **7.8**, max **40**, n=4 devices). §6.2's "7.8" was the **mean**; the figure and chapter now use the robust **device-median** (3.4) throughout, so a few outlying sweeps don't define a cell. Chapter §3.4 text updated to match (on-off 3.3→2.4 across PEO at salt0.09; largest *area* 0.44 at the low-salt/low-PEO corner; per-sweep skew noted explicitly).
- **Protocol overlay** = v114 R4 at its two protocols. Reproduced 4.6 s (3 V, R²=0.82, noisy) → 15.5 s (6 V, R²=0.97) with a **single** exponential (the chapter's methodology); the 4-param stretched form is degenerate on the clean 6 V curve. Model-free t½ corroborates (4.5→13.4 s).
- **Chemistry bars** are illustrative values from §14–§15 / curation (host PEO 22 s n=3 vs TMPE 3.8 s n=1; anion PEO/Tr 20 s n=3 vs PEO/TFSI 0.4 s n=1; cation TMPE/TFSI Li 6.3 / Na 7.0 / K 3.5 s, n=2 each), each bar n-labelled.

## 21. Pulse (number-of-pulses) study — application-relevant findings + Fig 3.2 (2026-06-04)

The PULSES descriptors ([`ch4_pulse_descriptors.csv`](ch4_pulse_descriptors.csv), per-cell in [`ch3_pulses_by_cell.csv`](ch3_pulses_by_cell.csv)) give the **input-integration / write transfer function** that Ch4 needs. Two *separate, sensical* composition axes emerge (verified per-device, not just cell medians):

- **PEO sets potentiation strength.** Growth exponent α (log–log slope) falls with PEO — cleanest at salt0.045 where per-device values are tight: PEO0.3 [1.06,1.23,1.02,1.16]≈1.1 → PEO0.6 ≈0.5 → PEO1.2 [0.33,0.33,0.28]≈0.31. Peak ratio (usable dynamic range) maximal at the low-PEO/low-salt corner (≈480× at PEO0.3/0.045), few-fold at high PEO. *Noisier at salt0.18*; the PEO0.3/salt0.18 cell (α≈0.18) is the sparse n=2 curation-salvaged cell (v141/v148) and is not leaned on.
- **Salt sets the turnover ceiling.** Device-consistent: **salt0.045 → all cells turn over by N≈100–300** (turnover 3/4, 3/3, 2/3); **salt0.18 → none turn over, growth sustained to N≈1000** (0/2, 1/3, 0/3); salt0.09 mixed (transition). More salt = more chargeable states before saturation.

**Application reading (Ch4):** composition gives a tunable, predominantly **compressive** and (low-salt) **non-monotone** integration of the pulse train — the nonlinear input encoding a reservoir uses. Memory time and α co-vary with PEO (not orthogonal knobs); salt independently sets dynamic range/turnover.

**Key honest caveat (now in Ch3 §3.8 limitations):** integration was measured at a **single fixed inter-pulse interval (0.103 s)** and forgetting separately (post-potentiation decay). No experiment varies input *timing*, so Ch4 must **compose** φ(N) and τ — a modelling assumption, not a measured fact. A varied-interval pulse-train experiment is the test.

**Figure:** `fig_potentiation()` in `scripts/ch3_figures.py` → `figures/chapter3/potentiation_grid.pdf` = Fig 3.2 (α, peak ratio, turnover fraction over the grid; n annotated).
