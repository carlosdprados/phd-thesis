<!-- markdownlint-disable-file MD013 -->

# Chapters 3 & 4 — Claims Audit and Data-Coverage Ledger

**Author:** Carlos David Prado-Socorro · **Started:** 2026-06-03 · **Status:** living document — updated incrementally and committed after each pass.

**Purpose.** Decide, from the *actual* experimental archive, **what Chapters 3 and 4 can and cannot defensibly claim** — before writing. Every claim is rated against the data on disk, not against the plan. Companion docs: the forward spec [`05_chapter4_data_pipeline.md`](05_chapter4_data_pipeline.md), the chapter plan [`01_thesis_structure.md`](01_thesis_structure.md), and the as-built archive reference [`../docs/experimental_archive_and_pipeline.md`](../docs/experimental_archive_and_pipeline.md).

---

## 0. Resume pointer (read first)

- **Method:** analysis driven from `Nanomem_Devices_Library/DATABASE` (regenerated May 2025) — `UPDATED_DEVICES_LIBRARY.csv` for chemistry, the `*_PIXEL_INFO.csv` tables for measurement presence, `FILTERED_DEVICES.csv` for erratic-pixel flags. Corpus = **PEO host + triflate salt = 149 devices**.
- **Artifact:** [`ch3_ch4_device_inventory.csv`](ch3_ch4_device_inventory.csv) — one row per PEO/triflate device with chemistry, electrode, and per-type pixel counts. Regenerate with the script noted in §5.
- **Done:** §1 coverage inventory, §2 scope implication, §3 initial claims ledger.
- **Next:** (a) Na/K cell depth audit — pixels, flagged %, measurement days, common protocol; (b) trend tests — DELAYTIME Li/Na/K ordering, HYST switching window, PULSES potentiation; (c) PEO/LiTr concentration-grid trend tests; (d) freeze a Chapter-4 manifest subset (`05` §2.3).
- **Caveats on current numbers:** "has measurement" = ≥1 pixel row in that type's `PIXEL_INFO`; this does **not** yet exclude flagged/erratic pixels, nor verify a common protocol, nor check replicate quality. §1 counts are an upper bound on usable coverage; later passes tighten them.

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
| C1 | PEO/LiTr conductance & switching are tunable by composition (PEO and salt mass fraction) | 3 (core) | ⏳ | Coverage strong: 3×3 grid, n=3 all-3 per cell. Trend not yet tested. |
| C2 | Composition sets the fading-memory timescale (delay-time decay) in PEO/LiTr | 3→4 | ⏳ | Same grid; needs DELAYTIME decay-fit trend across the grid. |
| C3 | Cation identity orders the dynamics Li > Na > K (timescale / retention) | 3 (secondary) | 🟡 | Only n=3 Na, n=3 K devices. At best a labelled preliminary trend; never a primary quantitative claim. |
| C4 | All three common measurements (I–V, N-pulse, delay) exist across the comparative corpus | 3/4 | 🟡 | True only for the Li composition grid; 41/149 overall, thin (n≤2) for Na/K. |
| C5 | EPSC / STDP / separated STM-LTM / impedance compared across Li/Na/K | 3/4 | 🔴 | Ch2 (Paper 1, SY/Hybrane/LiTf) only. Use as Li-only priors/sanity checks; never propagate to Na/K. (Matches `01`/`05`.) |
| C6 | Compact behavioural models (read fn, pulse update, decay) identifiable per composition cell | 4 | ⏳ | Requires the three fits per cell on the Li grid; feasible given coverage, pending fit quality. |
| C7 | Heterogeneous reservoir / coincidence / filter-bank simulations grounded in measured cells | 4 | ⏳ | Depends on C1/C2/C6; the timescale spread to exploit is composition-driven (per §2), not cation-driven. |

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
