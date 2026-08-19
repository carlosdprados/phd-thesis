from pathlib import Path

from scripts.check_thesis_build import inspect_build, page_count
from scripts.reproduce import CORE_STEPS, PHYSIO_STEPS, read_checksums, steps_for


def test_build_checker_accepts_complete_log_and_pdf(tmp_path):
    log = tmp_path / "thesis.log"
    pdf = tmp_path / "thesis.pdf"
    log.write_text("Output written on thesis.pdf (264 pages, 123 bytes).\n")
    pdf.write_bytes(b"%PDF-1.7\n" + b"x" * 10_000)
    assert inspect_build(log, pdf) == []
    assert page_count(log) == 264


def test_build_checker_rejects_undefined_and_overfull(tmp_path):
    log = tmp_path / "thesis.log"
    pdf = tmp_path / "thesis.pdf"
    log.write_text(
        "There were undefined references.\n"
        "Overfull \\hbox (2.0pt too wide)\n"
        "Output written on thesis.pdf (10 pages, 123 bytes).\n"
    )
    pdf.write_bytes(b"%PDF-1.7\n" + b"x" * 10_000)
    problems = inspect_build(log, pdf)
    assert "undefined references" in problems
    assert "overfull box" in problems


def test_reproduction_steps_are_unique_and_case_is_excluded():
    all_steps = steps_for("all")
    names = [step.script for step in all_steps]
    assert len(all_steps) == len(CORE_STEPS) + len(PHYSIO_STEPS)
    assert len(names) == len(set(names))
    assert "ch5_case.py" not in names


def test_checksum_manifest_has_valid_digests():
    manifest = read_checksums(Path("provenance/database_inputs.sha256"))
    assert "DATABASE/DEVICES_LIBRARY.csv" in manifest
    assert len(manifest) >= 10
    assert all(len(digest) == 64 for digest in manifest.values())
    assert all(set(digest) <= set("0123456789abcdef") for digest in manifest.values())
