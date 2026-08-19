#!/usr/bin/env python3
"""Fail if the complete-thesis build is absent or carries serious LaTeX defects."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ERROR_PATTERNS = (
    ("LaTeX error", re.compile(r"^! LaTeX Error:", re.MULTILINE)),
    ("fatal TeX error", re.compile(r"^!  ==> Fatal error occurred", re.MULTILINE)),
    ("undefined control sequence", re.compile(r"Undefined control sequence")),
    ("undefined citations", re.compile(r"There were undefined citations")),
    ("undefined references", re.compile(r"There were undefined references")),
    ("overfull box", re.compile(r"Overfull \\[hv]box")),
)


def inspect_build(log_path: Path, pdf_path: Path) -> list[str]:
    """Return human-readable problems found in a completed thesis build."""
    problems: list[str] = []
    if not log_path.is_file():
        problems.append(f"missing LaTeX log: {log_path}")
        return problems
    if not pdf_path.is_file():
        problems.append(f"missing thesis PDF: {pdf_path}")
    elif pdf_path.stat().st_size < 10_000:
        problems.append(f"thesis PDF is implausibly small: {pdf_path.stat().st_size} bytes")

    text = log_path.read_text(encoding="utf-8", errors="replace")
    for label, pattern in ERROR_PATTERNS:
        if pattern.search(text):
            problems.append(label)
    if not re.search(r"Output written on .+\(\d+ pages?[,)]", text):
        problems.append("log has no successful PDF page-count record")
    return problems


def page_count(log_path: Path) -> int | None:
    text = log_path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"Output written on .+\((\d+) pages?[,)]", text)
    return int(match.group(1)) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, default=Path("build/thesis.log"))
    parser.add_argument("--pdf", type=Path, default=Path("build/thesis.pdf"))
    args = parser.parse_args()

    problems = inspect_build(args.log, args.pdf)
    if problems:
        print("Thesis build check: FAIL")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(
        f"Thesis build check: PASS ({page_count(args.log)} pages, "
        f"{args.pdf.stat().st_size / 1_000_000:.1f} MB)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
