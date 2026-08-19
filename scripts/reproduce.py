#!/usr/bin/env python3
"""Preflight and sequentially regenerate the thesis analysis artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT.parent / "Nanomem_Devices_Library"
CHECKSUMS = ROOT / "provenance" / "database_inputs.sha256"


@dataclass(frozen=True)
class Step:
    name: str
    script: str


CORE_STEPS = (
    Step("Chapter 2 figures and fitted evidence", "ch2_figures.py"),
    Step("Hybrane-to-PEO reproducibility summary", "bridge_hybrane_peo_reproducibility.py"),
    Step("Chapter 3 bridge figures", "bridge_figures.py"),
    Step("Chapter 4 cell-resolved dynamics fits", "ch4_dynamics_fits.py"),
    Step("Chapter 4 statistical controls", "ch4_rigor.py"),
    Step("Chapter 4 comparative figures", "ch4_comparative_figures.py"),
    Step("ATR analysis", "ch4_iratr.py"),
    Step("XRD analysis", "ch4_xrd.py"),
    Step("UV-visible analysis", "ch4_uvvis.py"),
    Step("Impedance analysis", "ch4_eis.py"),
    Step("Electrode contrast", "ch4_electrode.py"),
    Step("Uncategorised Au/TMPE raw audit", "uncat_au_tmpe_audit.py"),
    Step("Uncategorised Au/TMPE findings", "uncat_au_tmpe_findings.py"),
    Step("Polarity figure", "ch4_polarity.py"),
    Step("Lock-in raw audit", "lockin_au_tmpe_audit.py"),
    Step("Lock-in findings", "lockin_au_tmpe_findings.py"),
    Step("Lock-in figure", "ch4_lockin.py"),
    Step("Chapter 5 variability audit", "ch5_scatter_audit.py"),
    Step("Chapter 5 bounded node cards", "ch5_model.py"),
    Step("Chapter 5 reservoir benchmarks", "ch5_reservoir.py"),
)

PHYSIO_STEPS = (
    Step("WESAD task benchmarks", "ch5_wesad.py"),
    Step("WESAD temporal-context reconstruction", "ch5_physio_context.py"),
    Step("WESAD onset and noise controls", "ch5_onset.py"),
    Step("PhysioNet Non-EEG replication", "ch5_noneeg.py"),
    Step("Chapter 5 figures", "ch5_figures.py"),
    Step("Deployment calculations", "ch5_deployment.py"),
)


def steps_for(scope: str) -> tuple[Step, ...]:
    if scope == "core":
        return CORE_STEPS
    if scope == "physio":
        return PHYSIO_STEPS
    return CORE_STEPS + PHYSIO_STEPS


def read_checksums(path: Path = CHECKSUMS) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, relative = line.split(maxsplit=1)
        rows[relative.strip()] = digest
    return rows


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def preflight_core(allow_input_drift: bool = False) -> list[str]:
    problems: list[str] = []
    for relative in ("DATABASE", "DEVICES_LAB_DATA", "Common"):
        path = ARCHIVE / relative
        if not path.exists():
            problems.append(f"missing experimental archive path: {path}")
    if problems:
        return problems
    for relative, expected in read_checksums().items():
        path = ARCHIVE / relative
        if not path.is_file():
            problems.append(f"missing checksummed input: {path}")
            continue
        actual = sha256(path)
        if actual != expected and not allow_input_drift:
            problems.append(
                f"input checksum differs: {relative} "
                f"(expected {expected[:12]}..., found {actual[:12]}...)"
            )
    return problems


def preflight_physio() -> list[str]:
    problems: list[str] = []
    wesad = sorted((ROOT / "data" / "wesad" / "WESAD").glob("S*/S*.pkl"))
    noneeg = sorted((ROOT / "data" / "noneeg").glob("Subject*_AccTempEDA.hea"))
    if len(wesad) != 15:
        problems.append(f"WESAD requires 15 subject pickles; found {len(wesad)}")
    if len(noneeg) != 20:
        problems.append(f"Non-EEG requires 20 subject headers; found {len(noneeg)}")
    return problems


def preflight(scope: str, allow_input_drift: bool = False) -> list[str]:
    problems: list[str] = []
    if scope in {"core", "all"}:
        problems.extend(preflight_core(allow_input_drift))
    if scope in {"physio", "all"}:
        problems.extend(preflight_physio())
    return problems


def run(scope: str, allow_input_drift: bool = False) -> int:
    selected = steps_for(scope)
    env = os.environ.copy()
    env.update(
        PYTHONHASHSEED="0",
        MPLBACKEND="Agg",
        MPLCONFIGDIR=str(ROOT / "tmp" / "matplotlib"),
    )
    Path(env["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc)
    for index, step in enumerate(selected, 1):
        print(f"\n[{index:02d}/{len(selected):02d}] {step.name}", flush=True)
        command = [sys.executable, str(ROOT / "scripts" / step.script)]
        completed = subprocess.run(command, cwd=ROOT, env=env, check=False)
        if completed.returncode:
            print(f"FAILED: {step.script} returned {completed.returncode}")
            return completed.returncode

    metadata = {
        "scope": scope,
        "started_utc": started.isoformat(),
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "steps": [step.script for step in selected],
        "allow_input_drift": allow_input_drift,
        "case_included": False,
    }
    output = ROOT / "build" / "reproduction" / "last_run.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"\nReproduction complete; run record: {output.relative_to(ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scope", choices=("core", "physio", "all"))
    parser.add_argument("--check-only", action="store_true", help="validate required inputs without running analyses")
    parser.add_argument("--list", action="store_true", help="print the ordered analysis steps without running them")
    parser.add_argument(
        "--allow-input-drift",
        action="store_true",
        help="report but do not reject a database snapshot whose hashes differ",
    )
    args = parser.parse_args()

    if args.list:
        for index, step in enumerate(steps_for(args.scope), 1):
            print(f"{index:02d}. {step.script}: {step.name}")
        return 0

    problems = preflight(args.scope, args.allow_input_drift)
    if problems:
        print("Input preflight: FAIL")
        for problem in problems:
            print(f"  - {problem}")
        print("See docs/reproducibility.md for placement and provenance details.")
        return 1

    print(f"Input preflight: PASS ({args.scope})")
    if args.check_only:
        if args.scope in {"physio", "all"}:
            print("CASE is intentionally excluded: its raw corpus is unavailable and no CASE result is reported.")
        return 0
    return run(args.scope, args.allow_input_drift)


if __name__ == "__main__":
    raise SystemExit(main())
