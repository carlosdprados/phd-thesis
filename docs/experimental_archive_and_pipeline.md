<!-- markdownlint-disable-file MD013 -->

# Experimental Archive & Analysis Pipeline — As-Built Reference

**Author:** Carlos David Prado-Socorro · **Verified:** 2026-06-03 (against the files on disk)

This is the **ground-truth description of what actually exists** in the experimental archive and its Python tooling, as observed directly in the files. It is the empirical counterpart to the forward-looking specification in [`../handouts/05_chapter4_data_pipeline.md`](../handouts/05_chapter4_data_pipeline.md): that document defines what Chapters 3–4 *will require*; this one records what is *already there*. Where they disagree, this document reflects the disk and the other is the plan.

The data and code live **outside this git repo**, in a sibling folder:

```text
…/UV (Universitat de València) - Nanotech/
  ├── phd-thesis/                 ← this LaTeX repo
  └── Nanomem_Devices_Library/    ← the experimental archive + tooling (described here)
```

`Nanomem_Devices_Library/` is large (hundreds of MB of CSV) and is **not** version-controlled; only this reference is.

## 1. Top-level map of `Nanomem_Devices_Library/`

| Folder | Role |
| --- | --- |
| `DEVICES_LAB_DATA/` | Raw measurements, organized by quarter → device → day/measurement → pixel |
| `DATABASE/` | Processed feature tables (CSV) — the canonical analysis source of truth |
| `project_feature_extraction/` | Python: raw data → DATABASE CSVs |
| `project_device_cleaner/` | Streamlit app: flag erratic device-pixels → `FILTERED_DEVICES.csv` |
| `project_graphmaker/` | `graphmaker.py` — thesis-figure generation |
| `scripts_general/` | Visualizers, helper tools, and the SNN application simulation |
| `TSB_scripts_upd2025-05/` | Keithley TestScript Builder (TSP) measurement programs (produce the raw `.txt`) |
| `Common/` | Cross-cutting experiment sets (impedance first-steps, lock-in freq sweeps, substrate/concentration studies) |
| `Equipment_Manuals/`, `temp/` | Instrument manuals; scratch |

## 2. Raw lab data — `DEVICES_LAB_DATA/`

Organized by quarter, `YYYY-QN_Devices/` (2020-Q4 → 2025-Q2):

```text
<quarter>/                e.g. 2025-Q2_Devices
  <device-folder>/        e.g. 2025-05-14_NM_v333_(TMPELiBis,Ag,3000rpm,75deg,usualmixing,scratchedSY)
    Day<N>_<MeasType>/     e.g. Day1_Hyst, Day1_NmbPls, Day1_DlyTime, Day14_Prof
      <pixel>/             e.g. R4, L5  (a single crossbar junction)
        D1_all.txt         raw Keithley: 3 rows = current, voltage, time (comma-delimited, comments='TSP')
                           (older devices instead have D1_I.txt / D1_V.txt / D1_T.txt)
        <type>_curves_data.csv / <type>_data.csv / <type>_pixel_data.csv   ← written back by feature extraction
```

- **Device folder** = `DATE_NM_vXXX_(free-text descriptor)`. The stable identifier is **`device_name = NM_vXXX`**. The parenthetical descriptor grammar is loose and drifted over the years (early `(diff_rpm)`, later `(PEO0.3,LiTr0.09,…)`, recent `(TMPELiBis,Ag,3000rpm,…)`). **Do not parse the descriptor for fabrication truth — use the device library (§4).** This matches the warning in `05` §2.1.
- **`MeasType` suffixes:** `_Hyst` (I–V hysteresis), `_NmbPls` (number-of-pulses potentiation), `_DlyTime` (delay-time depotentiation), `_Prof` (profilometry); EIS and Vconstant also exist. The `DayN` number is **days since fabrication** (see §3), not a fixed protocol stage — e.g. v333 has `Day1_Hyst`, `Day1_NmbPls`, `Day1_DlyTime` all on day 1.
- **Pixel = one of 16 crossbar junctions** on a substrate where a top evaporated-metal strip crosses the bottom ITO band: **8 in the Left column (`L1`–`L8`) + 8 in the Right column (`R1`–`R8`)**. Each junction is treated as an **independent device** even though it shares the substrate and blend. A **leading `T` (e.g. `TL3`, `TR5`) marks a "Test" pixel**, deliberately renamed so the extraction pipeline does **not** count it as a characterized device.
- **Raw file formats:** CSV / TXT only. The Keithley dumps are `D1_all.txt` (or split `D1_I/V/T.txt`); feature extraction writes per-pixel `.csv` alongside them. **There is no HDF5 in this pipeline.** (The only `.hdf5` files in the archive are raw SR865A lock-in frequency-sweep data under `Common/Au_TMPE_Li-Na-K_Lock-in-Amplifier_Freq_Sweeps/`, a side dataset not consumed by the feature-extraction pipeline. See §8.)
- **Out of scope:** 2020-Q4 devices use a different legacy layout (Origin `.opj`, Excel, manual `N pulses/` and `Delay/<t>/` subfolders) and include `L_vXXX` (lateral) devices. These are **skipped by the pipeline** (§6).

## 3. Keys (columns shared across all processed tables)

| Key | Meaning |
| --- | --- |
| `device_name` | `NM_vXXX` — one fabricated **substrate** (one blend / fabrication run) |
| `day` | integer from `Day<N>` = **days since fabrication** (day 0 = fabrication day); tracks aging |
| `pixel` | one of the 16 junctions (`L1`–`L8` / `R1`–`R8`); leading `T` = Test pixel (excluded) |
| `pixel iteration` | repeated measurement of the same pixel (often blank) |
| `interface` | **EIS only** — the **Gamry instrument model** ("Interface"-series potentiostat) used; instrument metadata, *not* a physical electrode interface |
| `curve` | index of an individual sweep/cycle within a pixel's measurement |
| `measurement_type` | `HYST`, `PULSES`, `DELAYTIME`, `EIS`, `VCONST` (profilometry handled separately) |

## 4. Device library (fabrication metadata)

- `DATABASE/DEVICES_LIBRARY.csv` — master, one row per device, ~90 columns: per-component **mass ratio + final concentration** for each semiconductive polymer (SY, PVK, F8BT, MEHPPV), ion-conducting polymer (Hy, PEO, TMPE), and salt (LiTr, NaTr, KTr, ImTr, EMIm, BMIm, LiTFSI, NaTFSI, KTFSI); plus MoS₂, solvent (cyclohexanone), spin-coat rpm/time, annealing temp/time (+ 2nd stage), metal (Ag/Au/Al) thickness & evaporation rates, storage/measurement conditions, personnel, and free-text notes.
- `DATABASE/UPDATED_DEVICES_LIBRARY.csv` — **derived/cleaned** (built by `scripts_general/helper_tools/update_devices_library.py`). Collapses the per-component columns into convenience categoricals: **`Components Group`** (e.g. `SY, Hy, LiTr`), **`Used Metal`**, single `Ion-Conducting Polymer Mass Ratio`, `Salt Mass Ratio`, etc. **This is the file the device_cleaner loads.**
- **353 devices**, `NM_v005`→`NM_v338`; all `Device Type = Vertical` (ITO / active-blend / evaporated-metal sandwich). Top metal: **Ag ×182, Au ×50**, blank ×121.
- Active-blend families (`Components Group`, by count): `SY, PEO, LiTr` ×143 · `SY, Hy, LiTr` ×105 · `SY, TMPE, LiTr` ×29 · `SY, TMPE, {KTr/NaTr/ImTr/NaTFSI…}` · minor `PVK`/`F8BT` blends. Typical ion-polymer mass ratio 0.3, salt 0.09.
- **Material decode:** **SY** = Super Yellow (PPV-type conjugated semiconductor); **Hy** = Hybrane (hyperbranched polyester ion host); **PEO** = poly(ethylene oxide); **TMPE** = trimethylolpropane ethoxylate; **LiTr/NaTr/KTr** = Li/Na/K triflate (= LiOTf etc.); **…TFSI / …Bis** = bis(trifluoromethanesulfonyl)imide salts.
- **Chapter mapping** (see [`../handouts/01_thesis_structure.md`](../handouts/01_thesis_structure.md)): both chapters use **Ag** electrodes. **Ch2** (proof of concept, Paper 1) = `SY / Hybrane / LiOTf`. **Ch3** = PEO (main) / TMPE (exploratory) hosts with LiOTf (main) / NaOTf, KOTf (exploratory), scanning PEO/LiTr mass ratios and cation identity (Li⁺/Na⁺/K⁺). TMPE and alkali-TFSI/Bis devices are exploratory side systems.

## 5. Processed data — `DATABASE/*.csv` (24 CSV files)

For each electrical measurement type there are up to **4 nested levels** (coarse → fine):

- `DEVICES_<TYPE>_DEVICE_INFO.csv` — 1 row per device (aggregate; e.g. `number_pixels_measured`, saturated/broken pixel %).
- `DEVICES_<TYPE>_PIXEL_INFO.csv` — 1 row per (device, day, pixel, iteration) = means across that pixel's curves.
- `DEVICES_<TYPE>_CURVE_INFO.csv` — 1 row per individual sweep/cycle.
- `DEVICES_<TYPE>_ALL_DATAPOINTS.csv` — every raw (I, V, T) point (large: HYST ≈165 MB, VCONST ≈210 MB).

Types and headline features:

- **HYST** (memristive I–V loops): on-off ratio, normalized loop area, activation/deactivation voltage (Von/threshold) & current, sweep rate, R/G/ρ/σ/sheet-R/current-density at max-V and max-I, `is_saturated`, `is_broken`. The core switching metrics.
- **PULSES:** `number of pulses` → `ratio` (potentiation/depression).
- **DELAYTIME:** `delay time (s)` → `ratio` (retention / fading-memory relaxation).
- **VCONST:** constant-voltage hold — mean/max current, rate-of-change, relaxation metrics.
- **EIS:** rich Nyquist/Bode feature set + equivalent-circuit fits (`DEVICES_EIS_MUNAR0VDC_ECHEM_MODEL_VARFREE.csv`, `..._PYTHON_MODEL_BOUNDS.csv`). Circuit at 0 V DC (`feature_extraction_modules/global_variables.py`): cable L ≈ 6.38 µH + R ≈ 57.3 Ω, polymer R_SY ≈ 658 MΩ, ITO double-layer cap ≈ 26.7 µF, CPEs for the evaporated-electrode EDL and the LEC section → a light-emitting-electrochemical-cell / memristor model.
- **PROFILOMETRY:** `DEVICES_PROFILOMETRY_STATS.csv` — avg/std/min/max film thickness (nm) per device·day. `ITO3` junction area = 8.25 × 10⁻⁶ m² (0.0825 cm²).
- **`FILTERED_DEVICES.csv` — red-flag EXCLUSION list, NOT a "good" list.** Device·pixel·measurement combos that showed erratic/nonsensical behaviour and must be **dropped before modeling** (columns: `device_name, day, pixel, pixel iteration, interface, measurement_type`). Hand-flagged in the device_cleaner; ~230 rows, mostly HYST. **Likely incomplete** — more bad pixels may exist un-flagged, so an absent device is not guaranteed clean. "Devices that make sense" = the good-behaving ones *not* in this list.

## 6. Analysis pipeline (the Python projects)

**Flow:** `DEVICES_LAB_DATA` → `project_feature_extraction` → `DATABASE/*.csv` → `project_device_cleaner` → `FILTERED_DEVICES.csv`. The fabrication spreadsheet → `DEVICES_LIBRARY.csv` → (`update_devices_library.py`) → `UPDATED_DEVICES_LIBRARY.csv`.

- **`project_feature_extraction/`** — entry `feature_extraction_master.py` (interactive: choose quarters, then analysis type **1 profilometry · 2 hysteresis · 3 pulses · 4 delaytime · 5 EIS · 6 vconstant**). Modules: per type a `*_navigation.py` (walk folders, parse keys, find raw files) + `*_processing.py` (extract features, write per-pixel CSVs and aggregate into the DATABASE tables), plus `data_reading.py`, `eis_features.py`, `modeling.py`, `global_variables.py`, `plotting.py`, `user_input.py`. **Scope limits baked into `global_navigation.py`: only quarters with year ≥ 2021 are processed, and the device-folder must contain the `_(…)` descriptor** — so 2020-Q4 and any folder lacking the parenthetical are silently skipped. `TASKS.md` lists unfinished work (dualhyst/negahyst, deadzone subtraction, curve-shape classification, CV/AFM/UV-Vis/IR-ATR ingestion).
- **`project_device_cleaner/`** — Streamlit app, entry `device_cleaner_master.py` (`streamlit run device_cleaner_master.py`; `BASE_DIR = ../DATABASE`). Wizard: Components Group → ion ratio → salt ratio → measurement type → gallery → flag erratic pixels into `FILTERED_DEVICES.csv` (the exclusion list above). Includes a feature-distribution explorer.
- **`project_graphmaker/graphmaker.py`** — thesis-figure generation (outputs under `DATABASE/figures/`).
- **`scripts_general/`** — `visualization_tools/` (hyst, nyquist, bode-mod, bode-phz, eis_models, chemvar, temporal_quick_hyst); `helper_tools/` (`update_devices_library.py`, `database_updater.py`, `D1_all-I-V-sign_converter.py`, `hyst_file_wave_converter.py`, `AFM_finder.py`, `OptImg_finder.py`, `determine_prog_IV_delays.py`); `application_tools/Simulation_SNN.py` (spiking-neural-network simulation); `OUTDATED/` (superseded analyzers — ignore).

> Run scripts from inside their project folder — modules import relative to their package directory.

## 7. Status of the planned Chapter-4 artifacts

As of 2026-06-03, the artifacts that `05` plans **do not yet exist**: `handouts/ch4_device_manifest.csv` and `scripts_general/chapter4_pipeline.py` are absent, and no consolidated HDF5/Parquet containers are produced. The DATABASE CSVs (regenerated May 2025) plus `FILTERED_DEVICES.csv` (June 2025) are the **current canonical source of truth**.

## 8. Corrections / open points vs the planning docs

- **HDF5:** `05` §2.2 lists HDF5 as "consolidated post-processing containers (used by the Python pipeline)." On disk, the working pipeline is **CSV/TXT only** (0 of 86 `.py` files reference HDF5/Parquet; `DATABASE/` is 24 CSVs). HDF5 appears **only** as *raw* SR865A lock-in frequency-sweep data under `Common/Au_TMPE_Li-Na-K_Lock-in-Amplifier_Freq_Sweeps/raw_data/`. Consolidated HDF5/Parquet is a **planned** Ch4 output (`05` §5.2), not an existing artifact. (`05` §2.2 corrected + cross-linked accordingly.)
- **Impedance instruments — to confirm:** the `DATABASE` EIS tables key on a Gamry "Interface" potentiostat (the `interface` column), while the `Common/…Lock-in…` HDF5 sweeps and `handouts/00` §5 reference an **SR865A lock-in amplifier**. These look like two distinct impedance methods/eras (Gamry vs lock-in); worth confirming which underlies which EIS figures before relying on them.
