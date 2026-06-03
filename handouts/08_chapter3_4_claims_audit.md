<!-- markdownlint-disable-file MD013 -->

# Chapters 3 & 4 — Claims Audit and Data-Coverage Ledger

**Author:** Carlos David Prado-Socorro · **Started:** 2026-06-03 · **Status:** living document — updated incrementally and committed after each pass.

**Purpose.** Decide, from the *actual* experimental archive, **what Chapters 3 and 4 can and cannot defensibly claim** — before writing. Every claim is rated against the data on disk, not against the plan. Companion docs: the forward spec [`05_chapter4_data_pipeline.md`](05_chapter4_data_pipeline.md), the chapter plan [`01_thesis_structure.md`](01_thesis_structure.md), and the as-built archive reference [`../docs/experimental_archive_and_pipeline.md`](../docs/experimental_archive_and_pipeline.md).

---

## 0. Resume pointer (read first)

- **Method:** analysis driven from `Nanomem_Devices_Library/DATABASE` (regenerated May 2025) — `UPDATED_DEVICES_LIBRARY.csv` for chemistry, the `*_PIXEL_INFO.csv` tables for measurement presence, `FILTERED_DEVICES.csv` for erratic-pixel flags. Corpus = **PEO host + triflate salt = 149 devices**.
- **Artifact:** [`ch3_ch4_device_inventory.csv`](ch3_ch4_device_inventory.csv) — one row per PEO/triflate device with chemistry, electrode, and per-type pixel counts. Regenerate with the script noted in §5.
- **Done:** §1 coverage, §2 scope, §3 ledger, §6 first-pass trends, §7 clean manifest candidates, §8 quantitative dynamics (t½ ladder + potentiation), §9 cross-validation vs pipeline pre-computed features. Artifacts: `ch3_ch4_device_inventory.csv`, `ch4_device_manifest_DRAFT.csv`, `ch4_decay_fits.csv`, `ch4_pulse_descriptors.csv`, `scripts/ch3_4_dynamics_fits.py`.
- **Next:** formalise the Ch4 behavioural model (state-dependent pulse-update φ(x) + read transfer function), separate cycle-to-cycle vs device-to-device variance, run the read-disturb check to freeze the manifest. Ch3 prose/figures can already be drafted from §6/§8/§9.
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
| C3 | Cation identity orders the dynamics Li > Na > K (timescale / retention) | 3 (secondary) | 🔴 | Clean HYST n=1 for Na and K; delay/pulse n=2; point estimates do **not** follow Li>Na>K (§6.1, §6.3). Qualitative/preliminary at most — not a quantitative claim. |
| C4 | All three common measurements (I–V, N-pulse, delay) exist across the comparative corpus | 3/4 | 🟡 | True only for the Li composition grid; 41/149 overall, thin (n≤2) for Na/K. |
| C5 | EPSC / STDP / separated STM-LTM / impedance compared across Li/Na/K | 3/4 | 🔴 | Ch2 (Paper 1, SY/Hybrane/LiTf) only. Use as Li-only priors/sanity checks; never propagate to Na/K. (Matches `01`/`05`.) |
| C6 | Compact behavioural models (read fn, pulse update, decay) identifiable per composition cell | 4 | 🟡 | Per-cell parameters extracted (t½, retention, potentiation exp/peak/turnover; §8.5). Decay τ only ~half-identified at 8 pts; full φ(x) update + read transfer function still to formalise. |
| C7 | Heterogeneous reservoir / coincidence / filter-bank simulations grounded in measured cells | 4 | ⏳ | Depends on C1/C2/C6; the timescale spread to exploit is composition-driven (per §2), not cation-driven. |
| C8 | Devices show volatile fading memory (forgetting) and pulse potentiation across the corpus | 2/3/4 | ✅ | Delay slopes negative and pulse slopes positive in every cell tested (§6.3). Robust qualitative behaviour. |
| C9 | Large device-to-device / cycle variability — usable as heterogeneity for reservoir computing | 3/4 | ✅ | Feature sd ≈ mean across cells (§6); the t½ ladder (≈3–19 s, §8.1) is a concrete heterogeneity resource. |
| C10 | Potentiation saturates / reverses (turnover) at high N — caps usable pulse count | 3/4 | ✅ | ~half the cells peak then decline by N=1000 (§8.2); sets a safe operating range for Ch4 pulse protocols. |

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
