<!-- markdownlint-disable-file MD013 -->

# Chapters 3 & 4 — Claims Audit and Data-Coverage Ledger

**Author:** Carlos David Prado-Socorro · **Started:** 2026-06-03 · **Status:** living document — updated incrementally and committed after each pass.

**Purpose.** Decide, from the *actual* experimental archive, **what Chapters 3 and 4 can and cannot defensibly claim** — before writing. Every claim is rated against the data on disk, not against the plan. Companion docs: the forward spec [`05_chapter4_data_pipeline.md`](05_chapter4_data_pipeline.md), the chapter plan [`01_thesis_structure.md`](01_thesis_structure.md), and the as-built archive reference [`../docs/experimental_archive_and_pipeline.md`](../docs/experimental_archive_and_pipeline.md).

---

## 0. Resume pointer (read first)

- **Method:** analysis driven from `Nanomem_Devices_Library/DATABASE` (regenerated May 2025) — `UPDATED_DEVICES_LIBRARY.csv` for chemistry, the `*_PIXEL_INFO.csv` tables for measurement presence, `FILTERED_DEVICES.csv` for erratic-pixel flags. Corpus = **PEO host + triflate salt = 149 devices**.
- **Artifact:** [`ch3_ch4_device_inventory.csv`](ch3_ch4_device_inventory.csv) — one row per PEO/triflate device with chemistry, electrode, and per-type pixel counts. Regenerate with the script noted in §5.
- **Done:** §1 coverage, §2 scope, §3 ledger, §6 first-pass trends + verdicts, §7 clean manifest candidates ([`ch4_device_manifest_DRAFT.csv`](ch4_device_manifest_DRAFT.csv)).
- **Next:** stretched-exponential τ/β decay fits (DELAYTIME) and saturating pulse-update fits (PULSES) on the clean stratum-A composition cells = the Chapter-4 model identification (`05` §3, §5.3), then per-cell parameter cards (`05` §5.4). Optional: confirm common protocols (sweep rate, V_write, Δt range) within each cell before fitting.
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
| C1 | PEO/LiTr switching window (on-off ratio, loop area) is tunable by composition | 3 (core) | 🟡 | Window shrinks as PEO rises at fixed salt; large spread, not cleanly monotonic (§6.2). Qualitatively yes; a quantitative law needs proper fits. |
| C2 | Composition sets the fading-memory timescale (delay-time decay) in PEO/LiTr | 3→4 | 🟡 | Forgetting present everywhere; composition slope weak/noisy (§6.3). Needs stretched-exp τ fits on a matched protocol. |
| C3 | Cation identity orders the dynamics Li > Na > K (timescale / retention) | 3 (secondary) | 🔴 | Clean HYST n=1 for Na and K; delay/pulse n=2; point estimates do **not** follow Li>Na>K (§6.1, §6.3). Qualitative/preliminary at most — not a quantitative claim. |
| C4 | All three common measurements (I–V, N-pulse, delay) exist across the comparative corpus | 3/4 | 🟡 | True only for the Li composition grid; 41/149 overall, thin (n≤2) for Na/K. |
| C5 | EPSC / STDP / separated STM-LTM / impedance compared across Li/Na/K | 3/4 | 🔴 | Ch2 (Paper 1, SY/Hybrane/LiTf) only. Use as Li-only priors/sanity checks; never propagate to Na/K. (Matches `01`/`05`.) |
| C6 | Compact behavioural models (read fn, pulse update, decay) identifiable per composition cell | 4 | ⏳ | Requires the three fits per cell on the Li grid; feasible given coverage, pending fit quality. |
| C7 | Heterogeneous reservoir / coincidence / filter-bank simulations grounded in measured cells | 4 | ⏳ | Depends on C1/C2/C6; the timescale spread to exploit is composition-driven (per §2), not cation-driven. |
| C8 | Devices show volatile fading memory (forgetting) and pulse potentiation across the corpus | 2/3/4 | ✅ | Delay slopes negative and pulse slopes positive in every cell tested (§6.3). Robust qualitative behaviour. |
| C9 | Large device-to-device / cycle variability — usable as heterogeneity for reservoir computing | 3/4 | ✅ | Feature sd ≈ mean across cells (§6); reframed as a resource, consistent with the thesis framing. |

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
