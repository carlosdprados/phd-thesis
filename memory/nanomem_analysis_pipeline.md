---
name: nanomem-analysis-pipeline
description: "The Python tooling in Nanomem_Devices_Library — feature_extraction, device_cleaner, graphmaker, scripts_general — and how raw data flows into the DATABASE and curated device lists"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 74103bc0-6a21-4b5a-ade9-98c719e23346
---

# Analysis Pipeline (Nanomem_Devices_Library)

Data model & schemas these tools read/write live in [[phd_data_structure]]. **Version-controlled copy of this in the repo:** `docs/experimental_archive_and_pipeline.md`. Flow:
`DEVICES_LAB_DATA` (raw) → **project_feature_extraction** → `DATABASE/*.csv` → **project_device_cleaner** → `FILTERED_DEVICES.csv`. The hand-maintained fabrication spreadsheet → `DEVICES_LIBRARY.csv` → (`update_devices_library.py`) → `UPDATED_DEVICES_LIBRARY.csv`.

## project_feature_extraction/  (raw → DATABASE)

- Entry: `feature_extraction_master.py`. Run interactively: pick quarters, then analysis type **1 profilometry · 2 hysteresis · 3 pulses · 4 delaytime · 5 EIS · 6 vconstant**; optionally emits per-curve figures.
- `feature_extraction_modules/`: per measurement type a `*_navigation.py` (walks folders, parses `Day<N>`/`device_name`/pixel, finds raw files) + a `*_processing.py` (extracts features, writes the per-pixel CSVs into the raw folders AND aggregates into `DATABASE/DEVICES_<TYPE>_{DEVICE,PIXEL,CURVE}_INFO.csv` + `ALL_DATAPOINTS.csv`). Plus `data_reading.py` (reads `D1_all.txt` or `D1_I/V/T.txt`), `eis_features.py`, `modeling.py`, `global_variables.py` (physical constants + EIS circuit params), `plotting.py`, `user_input.py`.
- ⚠️ **Scope limits baked into `global_navigation.py`**: only quarters with year **≥ 2021** are processed, and `extract_device_name` requires the `_(...)` parenthetical in the folder name. So 2020-Q4 and any folder lacking the descriptor are silently skipped. `TASKS.md` lists known unfinished work (dualhyst/negahyst reading, deadzone subtraction, curve-shape classification, CV/AFM/UV-Vis/IR-ATR ingestion, more decimals).

## project_device_cleaner/  (DATABASE → curated good devices)

- **Streamlit app**; entry `device_cleaner_master.py` (`streamlit run device_cleaner_master.py` from inside the folder — `BASE_DIR = ../DATABASE`). Loads `UPDATED_DEVICES_LIBRARY.csv`.
- Wizard: **Components Group → Ion-Conducting Polymer Mass Ratio → Salt Mass Ratio → Measurement Type → gallery** (thumbnails per device·day) → detail view → toggle a flag. Flags are written to `DATABASE/FILTERED_DEVICES.csv` = the **red-flag EXCLUSION list** of erratic/nonsensical device-pixels to drop before modeling (NOT a "good" list; likely incomplete). Also has a feature-distribution explorer and an "all results" overview.
- `device_cleaner_modules/`: `data_io.py` (loads, caches, flag save/load), `filters.py`, `navigation.py`, `gallery.py`, `plotting.py` (IV / I–t / V–t / hysteresis), `overview.py`, `features_explorer.py`.

## scripts_general/

- `visualization_tools/` — standalone interactive viewers: `hyst_visualizer.py`, `nyquist_visualizer.py`, `bodemod_visualizer.py`, `bodephz_visualizer.py`, `eis_models_visualizer.py`, `chemvar_visualizer.py` (compare across chemistry/composition), `temporal_quick_hyst_viz.py`.
- `helper_tools/` — `update_devices_library.py` (DEVICES_LIBRARY → UPDATED_…), `database_updater.py`, `D1_all-I-V-sign_converter.py`, `hyst_file_wave_converter.py`, `AFM_finder.py`, `OptImg_finder.py`, `determine_prog_IV_delays.py`.
- `application_tools/Simulation_SNN.py` — spiking-neural-network simulation (the neuromorphic application/demo built on the device behavior).
- `OUTDATED/` — superseded analyzers (hysteresis/pulse/STDP/PotDepot scripts, old `jupyter_analysis.ipynb`, `interactive_dash.py`). Ignore unless asked.

## project_graphmaker/

- Single `graphmaker.py` (newest tool, mid-2025) — produces thesis-style figures. `DATABASE/figures/` holds outputs (DelayTime/Pulses PNGs, `tfsi/` and `tr/` subfolders).

## Other Nanomem_Devices_Library folders (not pipeline)

- `TSB_scripts_upd2025-05/` — Keithley TestScript Builder (.tsp/TSP) measurement programs (Hysteresis, STDP, EPSC, Constant_Voltage, Frequency, pulse trains, + many vendor examples) that produce the raw `D1_*.txt`.
- `Common/` — cross-cutting experiment sets (impedance first-steps, lock-in freq sweeps, substrate-difference studies, concentration-variation series).
- `Equipment_Manuals/` — Keithley 2450, SR865A lock-in, IKA hotplate.
- `temp/` — scratch.

## Caveats for future sessions

- DATABASE CSVs were last regenerated **May 2025** and are the **canonical source of truth** (confirmed by user). `FILTERED_DEVICES.csv` last edited **2025-06-04**. Remember it is an **exclusion** list (erratic devices to drop) and is possibly incomplete — don't assume an unlisted device is automatically clean.
- Module files are mode `-rw-------` (owner-only) — readable here, but they `import` each other relative to their package dir, so run scripts from inside their project folder.
