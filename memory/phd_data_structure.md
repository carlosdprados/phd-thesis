---
name: phd-research-data-structure
description: "How experimental data is organized in Nanomem_Devices_Library — raw lab data, the device library, the processed DATABASE schema, and key/naming conventions"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 74103bc0-6a21-4b5a-ade9-98c719e23346
---

# Experimental Data Organization (Nanomem_Devices_Library)

Root: `Nanomem_Devices_Library/` (sibling of the `phd-thesis` git repo, inside the same UV-Nanotech iCloud folder). Four folders matter most: `DEVICES_LAB_DATA`, `DATABASE`, `project_feature_extraction`, `project_device_cleaner`. The Python tooling is documented in [[nanomem_analysis_pipeline]].

**Version-controlled copy:** the same facts (data layout + pipeline, as-built) are committed in the thesis repo at `docs/experimental_archive_and_pipeline.md` — the canonical, shareable copy. Update it when these facts change.

## 1. Raw lab data — `DEVICES_LAB_DATA/`

Organized by quarter: `YYYY-QN_Devices/` (2020-Q4 → 2025-Q2). Hierarchy:

```text
<quarter>/                e.g. 2025-Q2_Devices
  <device-folder>/        e.g. 2025-05-14_NM_v333_(TMPELiBis,Ag,3000rpm,75deg,usualmixing,scratchedSY)
    Day<N>_<MeasType>/     e.g. Day1_Hyst, Day1_NmbPls, Day1_DlyTime, Day14_Prof
      <pixel>/             one of 16 junctions: L1–L8 (left col) / R1–R8 (right col); leading T (e.g. TL3) = Test pixel, skipped by the pipeline
        D1_all.txt         raw Keithley: 3 rows = current, voltage, time (comma-delim, comments='TSP')
                           (older devices instead have D1_I.txt / D1_V.txt / D1_T.txt)
        <type>_curves_data.csv / <type>_data.csv / <type>_pixel_data.csv   ← written by feature extraction
```

- Device-folder name = `DATE_NM_vXXX_(free-text fabrication descriptor)`. The stable key is **`device_name = NM_vXXX`**. Descriptor grammar is loose and changed over time (early: `(diff_rpm)`, `(hbrn_and_salt)`; later structured: `(PEO0.3,LiTr0.09,prof,test,1500rpm)`; recent: `(TMPELiBis,Ag,3000rpm,75deg,usualmixing,scratchedSY)`). **Do not parse the descriptor for truth — use the device library (§3) for fabrication parameters.**
- `MeasType` folder suffixes: `_Hyst` (I–V hysteresis), `_NmbPls` (number-of-pulses), `_DlyTime` (delay/retention time), `_Prof` (profilometry); EIS and Vconstant also exist as measurement types. Profilometry folder holds `Prof.txt` + `profilometry_data.csv` + `profilometry_stats.csv`.
- Very old 2020-Q4 devices use a completely different layout (Origin `.opj`, Excel, manual `N pulses/` and `Delay/<time>/` subfolders) and also include `L_vXXX` devices (NOT `NM_`). These are **excluded from the automated pipeline** (see §2 + [[nanomem_analysis_pipeline]]).

## 2. Keys / naming conventions (used as columns across all processed CSVs)

- **device_name** — `NM_vXXX` (e.g. NM_v333) = one fabricated **substrate** (one blend / fabrication run).
- **day** — integer from the `Day<N>` folder = **days since fabrication** (day 0 = fabrication day). Tracks aging/stability across a device's measurement campaign.
- **pixel** — one of the **16 crossbar junctions** on a substrate where a top evaporated-metal strip crosses the bottom ITO band: **8 in the Left column (L1–L8) + 8 in the Right column (R1–R8)**. Each junction is treated as an **independent device** even though it shares the substrate + blend. A leading **`T` (e.g. `TL3`, `TR5`) marks a "Test" pixel**, deliberately renamed so the extraction pipeline does NOT count it as a characterized device.
- **pixel iteration** — repeated measurement of the same pixel (often blank).
- **interface** — EIS-only; records the **Gamry EIS instrument model** ("Interface"-series potentiostat) used — instrument metadata, *not* a physical electrode interface.
- **curve** — index of an individual sweep/cycle within a pixel's measurement.
- **measurement_type** — HYST, PULSES, DELAYTIME, EIS, VCONST (PROFILOMETRY handled separately).

## 3. The device library (fabrication metadata)

- `DATABASE/DEVICES_LIBRARY.csv` — master, one row per device, ~90 columns: per-component **mass ratio + final concentration** for each semiconductive polymer (SY, PVK, F8BT, MEHPPV), ion-conducting polymer (Hy, PEO, TMPE), and salt (LiTr, NaTr, KTr, ImTr, EMIm, BMIm, LiTFSI, NaTFSI, KTFSI), plus MoS2, solvent (cyclohexanone), spin-coat rpm/time, annealing temp/time (+ 2nd stage), metal (Ag/Au/Al) thickness & evap rates, storage/measurement conditions, who-did-what, free-text notes.
- `DATABASE/UPDATED_DEVICES_LIBRARY.csv` — **derived/cleaned** version (built by `scripts_general/helper_tools/update_devices_library.py`). Collapses per-component columns into convenience categoricals: **`Components Group`** (e.g. `SY, Hy, LiTr`), **`Used Metal`**, single `Ion-Conducting Polymer Mass Ratio`, `Salt Mass Ratio`, `…Final Concentration`, `Total Evaporation Time`, `Second Stage Annealing`. **This is the file the device_cleaner app loads.**
- **353 devices**, `NM_v005`→`NM_v338`. All `Device Type = Vertical` (ITO/active-blend/metal sandwich). Metal: Ag ×182, Au ×50, blank ×121.
- Active-blend families by frequency (`Components Group`): `SY, PEO, LiTr` ×143 · `SY, Hy, LiTr` ×105 · `SY, TMPE, LiTr` ×29 · `SY, TMPE, {KTr/NaTr/ImTr/NaTFSI…}` · minor `PVK/F8BT` blends. Typical ion-polymer mass ratio 0.3, salt 0.09.
- Material decode: **SY = Super Yellow** (PPV-type emissive semiconductive polymer); **Hy = Hybrane** (hyperbranched polyester ion conductor); **PEO** = poly(ethylene oxide); **TMPE** = trimethylolpropane ethoxylate; **LiTr/NaTr/KTr = Li/Na/K triflate (= LiOTf etc.)**; **…TFSI / …Bis** = bis(trifluoromethanesulfonyl)imide salts.
- **Chapter mapping (confirmed by user 2026-06-03):** both thesis chapters use **Ag** top electrodes. **Ch2** (proof of concept, Paper 1, [[paper1_summary]]) = `SY, Hybrane, LiOTf`(LiTr). **Ch3** = Ag devices varying the ion conductor **PEO (main) / TMPE (exploratory)** and salt cation **LiOTf (main) / NaOTf, KOTf (exploratory)**, scanning PEO/LiTr mass ratios and cation identity (Li⁺/Na⁺/K⁺). See [[thesis_structure]].

## 4. Processed data — `DATABASE/*.csv`

For each electrical measurement type there are up to **4 nested levels** (coarse→fine):

- `DEVICES_<TYPE>_DEVICE_INFO.csv` — 1 row per device (aggregate, e.g. number_pixels_measured, saturated/broken pixel %).
- `DEVICES_<TYPE>_PIXEL_INFO.csv` — 1 row per (device, day, pixel, iteration) = means across that pixel's curves.
- `DEVICES_<TYPE>_CURVE_INFO.csv` — 1 row per individual sweep/cycle.
- `DEVICES_<TYPE>_ALL_DATAPOINTS.csv` — every raw (I,V,T) point (huge: HYST ≈165 MB, VCONST ≈210 MB).

Types & their headline features:

- **HYST** (memristive I–V loops): on-off ratio, normalized loop area, activation/deactivation voltage (Von/threshold) & current, sweep rate, R/G/ρ/σ/sheet-R/current-density at max-V and max-I, `is_saturated`, `is_broken`. The core neuromorphic-switching metrics.
- **PULSES**: `number of pulses` → `ratio` (synaptic potentiation/depression).
- **DELAYTIME**: `delay time (s)` → `ratio` (retention/forgetting / relaxation).
- **VCONST**: constant-voltage hold — mean/max current, rate-of-change, relaxation metrics.
- **EIS**: very rich Nyquist/Bode feature set + equivalent-circuit fits in `DEVICES_EIS_MUNAR0VDC_ECHEM_MODEL_VARFREE.csv` and `..._PYTHON_MODEL_BOUNDS.csv`. Circuit (at 0 V DC, see `global_variables.py`): cable L≈6.38 µH + R≈57.3 Ω, polymer R_SY≈658 MΩ, ITO electric-double-layer cap ≈26.7 µF, CPEs for evaporated-electrode EDL and the LEC section → a light-emitting-electrochemical-cell / memristor model.
- **PROFILOMETRY**: `DEVICES_PROFILOMETRY_STATS.csv` — avg/std/min/max film thickness (nm) per device·day. `ITO3` device area = 8.25e-6 m².
- `FILTERED_DEVICES.csv` — **red-flag EXCLUSION list** (NOT a "good" list): device·pixel·measurement combos that showed erratic/nonsensical behaviour and must be **dropped before building models** (columns: device_name, day, pixel, pixel iteration, interface, measurement_type). Hand-flagged in the device_cleaner app; ~230 rows, mostly HYST. ⚠️ Likely **incomplete** — more bad pixels may exist un-flagged, so an absent device is not guaranteed clean. "Devices that make sense" = the good-behaving ones NOT in this list. See [[nanomem_analysis_pipeline]].
