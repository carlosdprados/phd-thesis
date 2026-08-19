<!-- markdownlint-disable-file MD013 -->

# Reproducibility and Data Availability

This repository distinguishes two claims that are easy to conflate:

1. **Snapshot verification** checks the analysis code, regression tests, LaTeX source, committed derived tables/figures, references, and page layout.
2. **Raw-to-result regeneration** reruns the analysis scripts against separately held experimental and physiological inputs and intentionally replaces tracked derived artifacts.

## Verify the Public Snapshot

The tested environment is recorded in [`environment.yml`](../environment.yml). With Conda and a LaTeX installation providing `latexmk` and `biber`:

```sh
conda env create -f environment.yml
conda activate phd-thesis
make verify
```

`make verify` runs the full Python test suite, compiles `build/thesis.pdf`, and fails on LaTeX errors, undefined citations or references, and overfull boxes. It does not claim to reconstruct the committed figures from absent raw measurements.

## Regenerate the Core Experimental Analysis

The unversioned experimental archive must have this exact sibling placement:

```text
parent directory/
  phd-thesis/
  Nanomem_Devices_Library/
    DATABASE/
    DEVICES_LAB_DATA/
    Common/
```

The processed database snapshot is bound by [`provenance/database_inputs.sha256`](../provenance/database_inputs.sha256). Check placement and hashes before running anything:

```sh
python scripts/reproduce.py core --check-only
python scripts/reproduce.py core --list
make reproduce-core
```

The manifest covers the principal processed database tables. It does not hash every raw Keithley, spectroscopy, Chapter 2, or lock-in source file. The archive is not distributed with this repository, so the repository alone cannot independently regenerate the experimental results from raw data.

## Regenerate the Physiological Analysis

The physiological pipeline requires independently obtained copies of:

- WESAD: 15 subject pickles at `data/wesad/WESAD/S*/S*.pkl`.
- PhysioNet Non-EEG: 20 records at `data/noneeg/Subject*`.

The `data/` directory is deliberately ignored by Git. Once the corpora are present:

```sh
python scripts/reproduce.py physio --check-only
make reproduce-physio
```

CASE is deliberately absent from the reproduction graph. Its raw corpus was not available for the audited thesis snapshot; cached results were removed and no CASE result is reported in the thesis. The workflow will not silently substitute a stale cache for raw data.

## Regenerate Everything Available

```sh
make inputs-check
make reproduce-all
```

The orchestrator fixes `PYTHONHASHSEED=0`, uses a non-interactive Matplotlib backend, records the ordered scripts, stops at the first failure, and writes the ignored run record `build/reproduction/last_run.json`. The analysis scripts use their documented fixed seeds where stochastic sensitivity is evaluated. `make reproduce-all` then reruns the tests and complete-thesis build audit.

The committed tables and figures make the reported arithmetic and presentation auditable even without access to the raw archive. They are derived evidence, not a substitute for public raw-data deposition.
