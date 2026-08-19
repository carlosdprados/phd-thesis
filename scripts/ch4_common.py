"""Shared screening and statistics for the Chapter 4 analysis scripts.

The functions in this module are deliberately dependency-light so the screening
rules and rank statistics can be regression-tested without loading the raw
experimental archive.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


TRUE_VALUES = frozenset({"1", "true", "t", "y", "yes"})


def clean(value) -> str:
    """Return a stripped string for a possibly missing CSV value."""
    return str(value or "").strip()


def is_true_flag(value) -> bool:
    """Interpret the boolean encodings used across the database (notably Y/N)."""
    return clean(value).lower() in TRUE_VALUES


def filter_key(row, measurement_type: str | None = None) -> tuple[str, str, str, str]:
    """Canonical FILTERED_DEVICES key for a database row."""
    return (
        clean(row.get("device_name")),
        clean(row.get("day")),
        clean(row.get("pixel")),
        clean(measurement_type or row.get("measurement_type")).upper(),
    )


def load_filter_flags(path: str | Path) -> set[tuple[str, str, str, str]]:
    """Load exact curve exclusions, ignoring the all-blank CSV spacer row."""
    with open(path, newline="") as fh:
        return {
            key
            for row in csv.DictReader(fh)
            if (key := filter_key(row))[0] and key[3]
        }


def is_filtered(row, measurement_type: str, flags) -> bool:
    return filter_key(row, measurement_type) in flags


def curation_key(
    device: str,
    measurement_type: str,
    day: str = "",
    pixel: str = "",
) -> tuple[str, str, str, str]:
    return clean(device), clean(measurement_type).upper(), clean(day), clean(pixel)


def load_curation_registry(path: str | Path):
    """Load curation keyed by device, measurement, day, and pixel.

    Blank day or pixel fields are retained as intentional wildcards. Values are
    pairs of verdict and kept-points set (or None).
    """
    registry = {}
    path = Path(path)
    if not path.exists():
        return registry
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            key = curation_key(
                row.get("device_name"),
                row.get("measurement_type"),
                row.get("day"),
                row.get("pixel"),
            )
            if not key[0] or not key[1]:
                continue
            verdict = clean(row.get("verdict")).lower()
            raw_points = clean(row.get("kept_points"))
            kept = None
            if verdict == "clean" and raw_points and raw_points.lower() != "all":
                kept = frozenset(float(x) for x in raw_points.split(";") if clean(x))
            registry[key] = (verdict, kept)
    return registry


def curation_for(
    registry,
    device: str,
    measurement_type: str,
    day: str = "",
    pixel: str = "",
):
    """Resolve the most specific curation entry for a curve.

    Precedence is exact day+pixel, day-wide, pixel-wide, then device-wide. This
    preserves explicit per-curve decisions while supporting the existing blank
    wildcard fields in the registry.
    """
    device, measurement_type, day, pixel = curation_key(
        device, measurement_type, day, pixel
    )
    candidates = (
        (device, measurement_type, day, pixel),
        (device, measurement_type, day, ""),
        (device, measurement_type, "", pixel),
        (device, measurement_type, "", ""),
    )
    seen = set()
    for key in candidates:
        if key not in seen and key in registry:
            return registry[key]
        seen.add(key)
    return None


def row_is_excluded(
    row,
    measurement_type: str,
    flags,
    curation=None,
    broken_fields=(),
) -> bool:
    """Apply FILTERED, curation-discard, and database broken flags consistently."""
    if is_filtered(row, measurement_type, flags):
        return True
    if any(is_true_flag(row.get(field)) for field in broken_fields):
        return True
    if curation is not None:
        decision = curation_for(
            curation,
            row.get("device_name"),
            measurement_type,
            row.get("day"),
            row.get("pixel"),
        )
        if decision and decision[0] == "discard":
            return True
    return False


def average_ranks(values):
    """Average ranks for ties, as in scipy.stats.rankdata(method='average')."""
    values = np.asarray(values, dtype=float)
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    start = 0
    while start < len(values):
        stop = start + 1
        while stop < len(values) and values[order[stop]] == values[order[start]]:
            stop += 1
        ranks[order[start:stop]] = 0.5 * (start + stop - 1) + 1.0
        start = stop
    return ranks


def pearson(x, y):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def spearman(x, y):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if len(x) < 3:
        return float("nan")
    return pearson(average_ranks(x), average_ranks(y))


def permute_within(values, rng, blocks=None):
    """Permute values globally or independently within each named block."""
    values = np.asarray(values)
    if blocks is None:
        return rng.permutation(values)
    blocks = np.asarray(blocks, dtype=object)
    out = values.copy()
    for block in dict.fromkeys(blocks.tolist()):
        idx = np.flatnonzero(blocks == block)
        out[idx] = rng.permutation(values[idx])
    return out


def perm_p_spearman(x, y, rng, B=20_000, blocks=None):
    """Two-sided permutation p-value for a tie-aware Spearman correlation."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    obs = abs(spearman(x, y))
    if not np.isfinite(obs):
        return float("nan")
    count = 0
    for _ in range(B):
        if abs(spearman(x, permute_within(y, rng, blocks))) >= obs - 1e-12:
            count += 1
    return (count + 1) / (B + 1)


def holm_adjust(pvalues):
    """Holm family-wise adjusted p-values in the input order."""
    pvalues = np.asarray(pvalues, dtype=float)
    adjusted = np.full(len(pvalues), np.nan)
    finite = np.flatnonzero(np.isfinite(pvalues))
    order = finite[np.argsort(pvalues[finite])]
    running = 0.0
    m = len(order)
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * pvalues[idx])
        adjusted[idx] = min(running, 1.0)
    return adjusted


def freedman_lane_pvalues(X, y, rng, term_indices, B=20_000, blocks=None):
    """Conditional coefficient tests using Freedman--Lane residual permutation.

    Each tested term is removed from the reduced model. Reduced-model residuals
    are permuted within acquisition batches when blocks are supplied, added back
    to the reduced fitted values, and the full model is refitted.
    """
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pvalues = {}
    for term in term_indices:
        reduced = np.delete(X, term, axis=1)
        reduced_beta, *_ = np.linalg.lstsq(reduced, y, rcond=None)
        fitted = reduced @ reduced_beta
        residual = y - fitted
        observed = abs(beta[term])
        count = 0
        for _ in range(B):
            y_perm = fitted + permute_within(residual, rng, blocks)
            perm_beta, *_ = np.linalg.lstsq(X, y_perm, rcond=None)
            if abs(perm_beta[term]) >= observed - 1e-12:
                count += 1
        pvalues[term] = (count + 1) / (B + 1)
    return beta, pvalues
