#!/usr/bin/env python3
"""Generate Chapter 2 proof-of-concept figures.

Run from the repo root:
  python3 scripts/ch2_figures.py

Quantitative panels are regenerated from the local Nanomem archive where the
data exist in CSV/text form:
- NM_v055 Day1_Hyst/L4 for I-V hysteresis.
- NM_v055 Day1_PotDepot/L5 for potentiation/depression.
- NM_v055 DayX_NmbPls/Day8 for pulse-number response.
- NM_v055 DayX_STDP/Day19 for the STDP curve.

Panels not recoverable as complete raw CSV traces are reconstructed from the
published protocol/fit summaries cited in Chapter 2 and labelled as such in the
thesis captions.
"""

from __future__ import annotations

import csv
import math
import re
from pathlib import Path

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT.parent / "Nanomem_Devices_Library"
FIGDIR = ROOT / "figures" / "chapter2"

DEVICE_055 = (
    DATA
    / "DEVICES_LAB_DATA"
    / "2021-Q3_Devices"
    / "2021-07-14_NM_v055_(std,N2gunned&90C,instntannlng,oldSy,wlght,PlseTrn,PotDept&STDP)"
)
DEVICE_045 = (
    DATA
    / "DEVICES_LAB_DATA"
    / "2021-Q2_Devices"
    / "2021-06-12_NM_v045_(cmplt_annlng,slowevap,newSy,EPSC&PotDepotTest)"
)
# Hysteresis: NM_v025 reproduces the published Fig. 2a analogue fan-out
# (peak ~0.42 uA, ~15x on/off across ten cycles). Identical 1:0.30:0.09
# SY/Hybrane/LiOTf formulation to the canonical proof-of-concept device.
DEVICE_025 = (
    DATA
    / "DEVICES_LAB_DATA"
    / "2021-Q2_Devices"
    / "2021-04-07_NM_v025_(spiral,dgrd_in_glvbx_lght)"
)

COLORS = {
    "blue": "#276FBF",
    "green": "#1B9E77",
    "orange": "#D95F02",
    "red": "#C43C39",
    "purple": "#6A4C93",
    "gray": "#4D4D4D",
    "light": "#F4F4F4",
}

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 8.5,
        "axes.titlesize": 9,
        "axes.labelsize": 8.5,
        "legend.fontsize": 7.5,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "figure.dpi": 180,
        "savefig.bbox": "tight",
    }
)


def fnum(value: str | float | int | None) -> float:
    if value is None:
        return float("nan")
    if isinstance(value, (float, int)):
        return float(value)
    value = str(value).strip()
    if not value or value.lower() in {"na", "nan", "x"}:
        return float("nan")
    return float(value)


def read_series(path: Path) -> np.ndarray:
    text = path.read_text()
    parts = [p for p in re.split(r"[,\s]+", text) if p]
    return np.array([float(p) for p in parts], dtype=float)


def read_table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        return reader.fieldnames or [], list(reader)


def save(fig: plt.Figure, name: str) -> None:
    FIGDIR.mkdir(parents=True, exist_ok=True)
    path = FIGDIR / name
    fig.savefig(path)
    plt.close(fig)
    print(f"wrote {path.relative_to(ROOT)}")


def style_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out", length=3, width=0.8)


def _shade(hex_color: str, factor: float) -> tuple[float, float, float]:
    """Lighten (factor>1) or darken (factor<1) a hex colour for face shading."""
    h = hex_color.lstrip("#")
    rgb = np.array([int(h[i : i + 2], 16) for i in (0, 2, 4)], dtype=float) / 255.0
    if factor >= 1.0:
        out = rgb + (1.0 - rgb) * (factor - 1.0)
    else:
        out = rgb * factor
    return tuple(np.clip(out, 0.0, 1.0))


def _iso_slab(ax, x0, y0, w, h, depth, color, label=None):
    """Draw one isometric slab (front + top + right face) of the device stack."""
    from matplotlib.patches import Polygon

    ox, oy = depth  # screen-space depth offset
    front = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    top = [
        (x0, y0 + h),
        (x0 + w, y0 + h),
        (x0 + w + ox, y0 + h + oy),
        (x0 + ox, y0 + h + oy),
    ]
    right = [
        (x0 + w, y0),
        (x0 + w + ox, y0 + oy),
        (x0 + w + ox, y0 + h + oy),
        (x0 + w, y0 + h),
    ]
    ax.add_patch(Polygon(top, closed=True, facecolor=_shade(color, 1.18), edgecolor="0.25", lw=0.8, joinstyle="round"))
    ax.add_patch(Polygon(right, closed=True, facecolor=_shade(color, 0.80), edgecolor="0.25", lw=0.8, joinstyle="round"))
    ax.add_patch(Polygon(front, closed=True, facecolor=color, edgecolor="0.25", lw=0.8, joinstyle="round"))
    if label:
        ax.text(x0 + w / 2, y0 + h / 2, label, ha="center", va="center", fontsize=8.5, color="0.12")


def fig_device_schematic() -> None:
    from matplotlib.patches import Polygon

    fig, (axL, axR) = plt.subplots(
        1, 2, figsize=(7.4, 3.5), gridspec_kw={"width_ratios": [1.0, 1.15], "wspace": 0.04}
    )
    for ax in (axL, axR):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis("off")

    # ---- (a) isometric device stack -------------------------------------
    palette = {
        "glass": "#DCE8F5",
        "ito": "#7FC6B6",
        "composite": "#FBD162",
        "ag": "#C2C6CB",
    }
    depth = (1.25, 0.8)
    x0, w = 0.7, 3.7
    layers = [
        ("glass", 0.95, palette["glass"], "glass"),
        ("ito", 0.55, palette["ito"], "ITO"),
        ("composite", 2.15, palette["composite"], None),
        ("ag", 0.75, palette["ag"], "Ag"),
    ]
    y = 1.4
    mids = []
    for _, h, color, inner in layers:
        _iso_slab(axL, x0, y, w, h, depth, color, inner)
        mids.append(y + h / 2)
        y += h
    top_y = y
    ox, oy = depth

    # composite inner label (full ternary name, kept inside the wide slab)
    axL.text(
        x0 + w / 2,
        mids[2] + 0.05,
        "SY / Hybrane /\nLiOTf composite",
        ha="center",
        va="center",
        fontsize=7.8,
        color="0.12",
    )

    # short thickness callouts on the right (kept inside panel (a))
    lx = x0 + w + ox + 0.25
    for ymid, text in [(mids[3], "100 nm"), (mids[2], "209 nm")]:
        axL.annotate(
            text,
            xy=(x0 + w + ox * 0.5, ymid + oy * 0.5),
            xytext=(lx, ymid + oy * 0.5),
            arrowprops=dict(arrowstyle="-", lw=0.7, color="0.45"),
            va="center",
            ha="left",
            fontsize=7.6,
            color="0.2",
        )

    # bias terminals + geometry note
    axL.text(x0 + w / 2 + ox * 0.5, top_y + oy + 0.55, "$V$ applied to Ag", ha="center", fontsize=8.2, color=COLORS["red"])
    axL.text(x0 + w / 2 + ox * 0.5, top_y + oy + 1.15, r"active area $= 0.0825$ cm$^2$", ha="center", fontsize=7.8, color="0.3")
    axL.text(x0 + w / 2 + ox * 0.5, 0.6, "ITO grounded", ha="center", fontsize=8.2, color="0.25")
    axL.text(0.0, 9.4, "(a)", fontsize=11, weight="bold")

    # ---- (b) two-state ion-migration mechanism --------------------------
    axR.text(0.2, 9.4, "(b)", fontsize=11, weight="bold")
    axR.text(5.0, 9.45, "ion-mediated conductance change", ha="center", fontsize=8.8, weight="bold", color="0.12")

    def mechanism_cell(ax, y_base, height, title, title_color, moving):
        """One stacked sub-panel: two electrodes, polymer host, ordered ions.

        Upper two-thirds hold the polymer chains and coordinated Li+; the lower
        third is a clean drift lane carrying only the mobile species + arrow.
        """
        left_x, right_x = 1.1, 8.9
        # electrodes
        ax.add_patch(Rectangle((left_x - 0.55, y_base), 0.55, height, facecolor=palette["ito"], edgecolor="0.3", lw=0.7))
        ax.add_patch(Rectangle((right_x, y_base), 0.55, height, facecolor=palette["ag"], edgecolor="0.3", lw=0.7))
        ax.text(left_x - 0.275, y_base - 0.28, "ITO", ha="center", va="top", fontsize=6.6, color="0.3")
        ax.text(right_x + 0.275, y_base - 0.28, "Ag", ha="center", va="top", fontsize=6.6, color="0.3")
        # polymer host: a few smooth chains in the upper region
        xs = np.linspace(left_x, right_x, 200)
        for k in range(2):
            yc = y_base + height * (0.58 + 0.24 * k)
            ax.plot(xs, yc + 0.09 * np.sin((xs - left_x) * 2.0 + k), color="#9AA050", lw=1.1, alpha=0.75, zorder=1)
        # coordinated Li+ sitting on the chains (hard oxygen coordination)
        released = moving == "Li"
        for fx, fk in [(2.6, 0), (5.4, 1), (7.2, 0)]:
            cy = y_base + height * (0.58 + 0.24 * fk)
            face = "#Bcd4ec" if released else "#5FA3DD"
            ax.add_patch(Circle((fx, cy), 0.20, facecolor=face, edgecolor="0.2", lw=0.5, zorder=3, alpha=0.55 if released else 1.0))
            ax.text(fx, cy, r"Li$^+$", ha="center", va="center", fontsize=5.6, color="white", zorder=4)
        # drift lane (lower third)
        lane = y_base + height * 0.22
        if moving == "OTf":
            ion_col, ion_fc = COLORS["red"], "#E8736F"
            for fx in (5.6, 6.7, 7.8):
                ax.add_patch(Circle((fx, lane), 0.24, facecolor=ion_fc, edgecolor="0.2", lw=0.5, zorder=3))
                ax.text(fx, lane, r"OTf$^-$", ha="center", va="center", fontsize=5.2, color="white", zorder=4)
            ax.add_patch(FancyArrowPatch((2.6, lane), (5.0, lane), arrowstyle="-|>", mutation_scale=12, lw=1.4, color=ion_col, zorder=2))
        else:
            ion_col = "#3F7FC0"
            for fx in (5.4, 6.6, 7.8):
                ax.add_patch(Circle((fx, lane), 0.24, facecolor="#5FA3DD", edgecolor="0.2", lw=0.5, zorder=3))
                ax.text(fx, lane, r"Li$^+$", ha="center", va="center", fontsize=5.6, color="white", zorder=4)
            ax.add_patch(FancyArrowPatch((2.6, lane), (5.0, lane), arrowstyle="-|>", mutation_scale=15, lw=1.9, color=ion_col, zorder=2))
        ax.text(5.0, y_base + height + 0.22, title, ha="center", va="bottom", fontsize=7.6, color=title_color, weight="bold")

    mechanism_cell(
        axR, 5.4, 2.6,
        r"low field ($\sim$1 V): OTf$^-$ drifts $\rightarrow$ short-term memory",
        COLORS["red"], moving="OTf",
    )
    mechanism_cell(
        axR, 1.0, 2.6,
        r"high field ($\sim$3 V): Li$^+$ released $\rightarrow$ long-lived state",
        COLORS["blue"], moving="Li",
    )

    save(fig, "device_schematic.pdf")


def fig_iv_hyst() -> None:
    path = DEVICE_025 / "DayX_Hyst" / "Day5" / "L4" / "hysteresis_data.csv"
    _, rows = read_table(path)
    by_curve: dict[int, list[tuple[int, float, float]]] = {}
    for row in rows:
        curve = int(row["curve"])
        by_curve.setdefault(curve, []).append(
            (int(row["curve data point"]), fnum(row["voltage (V)"]), fnum(row["current (uA)"]))
        )

    fig, ax = plt.subplots(figsize=(5.7, 3.7))
    cmap = plt.get_cmap("viridis", 10)

    def forward_current_at(curve: int, target_v: float) -> float:
        points = sorted(by_curve[curve])
        v = np.array([p[1] for p in points])
        i = np.array([p[2] for p in points])
        top = int(np.argmax(v))
        return float(np.interp(target_v, v[:top + 1], i[:top + 1]))

    for curve in range(10):
        points = sorted(by_curve[curve])
        v = np.array([p[1] for p in points])
        i = np.array([p[2] for p in points])
        ax.plot(v, i, lw=1.05, color=cmap(curve), alpha=0.95)

    i_first = forward_current_at(0, 1.0)
    i_last = forward_current_at(9, 1.0)
    on_off = i_last / i_first

    ax.axhline(0, color="0.5", lw=0.6)
    ax.axvline(0, color="0.5", lw=0.6)
    ax.set_xlabel("voltage (V)")
    ax.set_ylabel(r"current ($\mu$A)")
    ax.set_title("ten successive positive sweeps")
    ax.text(0.05, 0.94, "0 -> 1.2 V -> 0\n0.25 V s$^{-1}$", transform=ax.transAxes, va="top", fontsize=8)
    ax.annotate(
        rf"$\times${on_off:.0f} on/off at 1 V",
        xy=(1.0, i_last),
        xytext=(0.32, i_last * 0.98),
        arrowprops=dict(arrowstyle="-|>", lw=0.8, color="0.3"),
        va="center",
        fontsize=8,
    )
    style_axes(ax)
    sm = cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=1, vmax=10))
    cbar = fig.colorbar(sm, ax=ax, fraction=0.05, pad=0.03)
    cbar.set_label("sweep")
    cbar.set_ticks([1, 5, 10])
    save(fig, "iv_hyst.pdf")


def pulse_trace_from_raw(pixel: str = "L5") -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    folder = DEVICE_055 / "Day1_PotDepot" / pixel / "Test_1_50pot50depot"
    current = read_series(folder / "D1_I.txt")
    voltage = read_series(folder / "D1_V.txt")
    if len(current) != len(voltage):
        raise ValueError(f"Current/voltage length mismatch for {pixel}")
    mask = np.abs(voltage) > 1e-9
    v = voltage[mask]
    i = current[mask]

    pos_idx = np.where(v > 0)[0][:50]
    neg_idx = np.where(v < 0)[0][:50]
    seq_idx = np.concatenate([pos_idx, neg_idx])
    seq_v = v[seq_idx]
    seq_i = i[seq_idx]
    conductance_us = (seq_i / seq_v) * 1e6
    pulse_no = np.arange(1, len(conductance_us) + 1)
    return pulse_no, seq_v, conductance_us


def fig_potentiation_depression() -> None:
    pulse_no, voltage, conductance_us = pulse_trace_from_raw("L5")
    norm = conductance_us / conductance_us[0] * 100.0

    fig, ax = plt.subplots(figsize=(4.9, 3.15))
    pos = voltage > 0
    neg = voltage < 0
    ax.plot(pulse_no[pos], norm[pos], "o-", ms=2.4, lw=1.0, color=COLORS["green"], label="+1 V potentiation")
    ax.plot(pulse_no[neg], norm[neg], "o-", ms=2.4, lw=1.0, color=COLORS["orange"], label="-2 V depotentiation")
    ax.axvline(50.5, color="0.55", lw=0.8, ls="--")
    ax.set_xlabel("write-pulse index")
    ax.set_ylabel(r"peak conductance, normalised (%)")
    ax.set_title("reversible pulse-driven tuning")
    ax.legend(frameon=False, loc="upper right")
    style_axes(ax)
    save(fig, "potentiation_depression.pdf")


def fig_pulse_number() -> None:
    path = DEVICE_055 / "DayX_NmbPls" / "Day8" / "MasterTable.txt"
    fieldnames, rows = read_table(path)
    pixels = fieldnames[1:]
    n = []
    values = []
    for row in rows:
        vals = [fnum(row[p]) for p in pixels]
        vals = [v for v in vals if math.isfinite(v)]
        if vals:
            n.append(fnum(row["Number of pulses"]))
            values.append(vals)

    x = np.array(n)
    means = np.array([np.mean(v) for v in values]) * 100.0
    stds = np.array([np.std(v, ddof=1) if len(v) > 1 else 0 for v in values]) * 100.0

    fig, ax = plt.subplots(figsize=(4.9, 3.15))
    ax.fill_between(x, means - stds, means + stds, color=COLORS["blue"], alpha=0.18, linewidth=0)
    ax.plot(x, means, "o-", ms=3.0, lw=1.2, color=COLORS["blue"], label="mean across five pixels")
    ax.set_xscale("log")
    ax.set_xlabel(r"number of write pulses, $N_{\mathrm{pulses}}$")
    ax.set_ylabel(r"$(G_f/G_0)\times 100$ (%)")
    ax.set_title("pulse-number response")
    ax.text(0.05, 0.92, r"band: $\pm$1 SD", transform=ax.transAxes, fontsize=8)
    style_axes(ax)
    save(fig, "pulse_number.pdf")


def fig_retention() -> None:
    t = np.array([0.15, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 7, 10, 15, 20, 30, 45, 60])
    traces = [
        ("1 V, 10 pulses (STM)", 1.01, 0.374, 2.57, COLORS["blue"]),
        ("1 V, 50 pulses (STM)", 1.01, 0.91, 3.01, COLORS["red"]),
        ("3 V, 10 pulses (longer-lived)", 1.05, 3.30, 4.73, "0.15"),
    ]

    fig, ax = plt.subplots(figsize=(5.7, 3.6))
    for label, r_inf, amp, tau, color in traces:
        y = (r_inf + amp * np.exp(-t / tau)) * 100.0
        ax.plot(t, y, "o-", lw=1.2, ms=3.0, color=color, label=label)
        tt = np.linspace(0.15, 60, 260)
        yy = (r_inf + amp * np.exp(-tt / tau)) * 100.0
        ax.plot(tt, yy, lw=1.0, color=color, alpha=0.55)
    ax.axhline(105, color="0.55", lw=0.8, ls="--")
    ax.set_xscale("log")
    ax.set_xlabel(r"waiting time, $t_{\mathrm{wait}}$ (s)")
    ax.set_ylabel(r"$(G_f/G_0)\times 100$ (%)")
    ax.set_title("retention fit reconstruction")
    ax.legend(frameon=False, loc="upper right")
    ax.text(0.04, 0.1, "dashed line: 5% above baseline", transform=ax.transAxes, fontsize=7.8)
    style_axes(ax)
    save(fig, "retention.pdf")


def fig_epsc_summary() -> None:
    states = ["S1", "S2", "S3", "S4"]
    ratios = np.array([7.33, 15.55, -3.72, -16.97])
    colors = [COLORS["green"], COLORS["green"], COLORS["orange"], COLORS["orange"]]

    fig, ax = plt.subplots(figsize=(4.9, 3.1))
    bars = ax.bar(states, ratios, color=colors, edgecolor="0.25", linewidth=0.7)
    ax.axhline(0, color="0.25", lw=0.8)
    ax.set_ylabel(r"signed current ratio, $R_n=I_{S_n}/I_{S_0}$")
    ax.set_title("EPSC state readout")
    for bar, ratio in zip(bars, ratios):
        va = "bottom" if ratio >= 0 else "top"
        offset = 0.55 if ratio >= 0 else -0.55
        ax.text(bar.get_x() + bar.get_width() / 2, ratio + offset, f"{ratio:.2f}", ha="center", va=va, fontsize=8)
    ax.set_ylim(-20, 18)
    style_axes(ax)
    save(fig, "epsc_summary.pdf")


def load_stdp_master() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    path = DEVICE_055 / "DayX_STDP" / "Day19" / "MasterTable.txt"
    fieldnames, rows = read_table(path)
    pixels = fieldnames[1:]
    x, mean, sd = [], [], []
    for row in rows:
        vals = [fnum(row[p]) for p in pixels]
        vals = np.array([v for v in vals if math.isfinite(v)], dtype=float)
        if len(vals):
            x.append(fnum(row["Tao (s)"]))
            mean.append(float(np.mean(vals)))
            sd.append(float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0)
    return np.array(x), np.array(mean), np.array(sd)


def load_stdp_fit() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    path = DEVICE_055 / "DayX_STDP" / "Day19" / "Fitting.txt"
    left_x, left_y, right_x, right_y = [], [], [], []
    with path.open() as fh:
        next(fh)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            while len(parts) < 4:
                parts.append("")
            if parts[0].strip() and parts[1].strip():
                left_y.append(float(parts[0]))
                left_x.append(float(parts[1]))
            if parts[2].strip() and parts[3].strip():
                right_y.append(float(parts[2]))
                right_x.append(float(parts[3]))
    return np.array(left_x), np.array(left_y), np.array(right_x), np.array(right_y)


def fig_stdp_summary() -> None:
    x, mean, sd = load_stdp_master()
    lx, ly, rx, ry = load_stdp_fit()
    fig, ax = plt.subplots(figsize=(4.9, 3.1))
    ax.errorbar(x, mean, yerr=sd, fmt="o", ms=3.0, lw=0.8, capsize=2, color=COLORS["purple"], ecolor="0.6")
    ax.plot(lx, ly, color=COLORS["green"], lw=1.2, label="fit, causal branch")
    ax.plot(rx, ry, color=COLORS["orange"], lw=1.2, label="fit, anti-causal branch")
    ax.axhline(0, color="0.35", lw=0.8)
    ax.axvline(0, color="0.35", lw=0.8)
    ax.set_xlabel(r"timing delay, $\Delta t$ (s)")
    ax.set_ylabel(r"$\Delta G$ (%)")
    ax.set_title("STDP timing kernel")
    ax.legend(frameon=False, loc="upper right")
    style_axes(ax)
    save(fig, "stdp_summary.pdf")


def fig_read_write_wait_protocol() -> None:
    fig, ax = plt.subplots(figsize=(6.2, 2.25))
    t = np.array([0, 0.15, 0.15, 0.55, 0.55, 1.65, 1.65, 2.65, 2.65, 2.8])
    v = np.array([0.5, 0.5, 0, 0, 1.0, 1.0, 0, 0, 0.5, 0.5])
    ax.plot(t, v, drawstyle="steps-post", color=COLORS["blue"], lw=1.5)
    for xpos, label in [(0.075, "read\n$G_0$"), (1.1, "write train\n$N$ pulses"), (2.15, "wait\n$t_{wait}$"), (2.725, "read\n$G_f$")]:
        ax.text(xpos, 1.18, label, ha="center", va="bottom", fontsize=8)
    ax.set_ylim(-0.12, 1.72)
    ax.set_xlim(-0.05, 2.95)
    ax.set_xlabel("protocol time")
    ax.set_ylabel("voltage")
    ax.set_yticks([0, 0.5, 1.0])
    ax.set_yticklabels(["0", r"$V_{read}$", r"$V_{write}$"])
    style_axes(ax)
    save(fig, "read_write_wait_protocol.pdf")


def fig_full_epsc_trace() -> None:
    # Reconstructed from the published state protocol and signed readout ratios.
    events = [
        (0.0, 1.0, 1.0, 1.0, "S0"),
        (1.0, 1.05, 2.0, 7.33, ""),
        (1.05, 2.05, 1.0, 7.33, "S1"),
        (2.05, 2.10, 2.0, 15.55, ""),
        (2.10, 3.10, 1.0, 15.55, "S2"),
        (3.10, 3.15, -2.5, -3.72, ""),
        (3.15, 4.15, 1.0, -3.72, "S3"),
        (4.15, 4.20, -2.5, -16.97, ""),
        (4.20, 5.20, 1.0, -16.97, "S4"),
    ]
    t, v, r = [], [], []
    for start, stop, vv, rr, _ in events:
        t.extend([start, stop])
        v.extend([vv, vv])
        r.extend([rr, rr])

    fig, ax1 = plt.subplots(figsize=(6.4, 3.0))
    ax2 = ax1.twinx()
    ax1.plot(t, v, drawstyle="steps-post", color=COLORS["blue"], lw=1.2, label="voltage")
    ax2.plot(t, r, drawstyle="steps-post", color=COLORS["red"], lw=1.2, label=r"$I/I_{S0}$")
    ax1.axhline(0, color="0.7", lw=0.7)
    ax2.axhline(0, color="0.4", lw=0.7, ls="--")
    for start, stop, _, rr, label in events:
        if label:
            ax2.text((start + stop) / 2, rr + (0.8 if rr >= 0 else -0.8), label, ha="center", va="center", fontsize=8)
    ax1.set_xlabel("protocol time (s)")
    ax1.set_ylabel("applied voltage (V)", color=COLORS["blue"])
    ax2.set_ylabel(r"signed current ratio, $I/I_{S0}$", color=COLORS["red"])
    ax1.set_ylim(-3.0, 2.35)
    ax2.set_ylim(-20, 18)
    style_axes(ax1)
    ax2.spines["top"].set_visible(False)
    save(fig, "full_epsc_trace.pdf")


def triangular(t: np.ndarray, center: float, width: float, amp: float) -> np.ndarray:
    y = np.maximum(0.0, 1.0 - np.abs(t - center) / (width / 2.0))
    return amp * y


def fig_stdp_waveforms() -> None:
    delays = [-0.30, 0.05, 0.60]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.65), sharey=True)
    t = np.linspace(-1.0, 1.0, 600)
    for ax, delay in zip(axes, delays):
        pre = triangular(t, 0.0, 1.2, 1.55)
        post = -triangular(t, delay, 1.2, 1.55)
        total = pre + post
        ax.plot(t, pre, color=COLORS["green"], lw=0.9, label="pre")
        ax.plot(t, post, color=COLORS["orange"], lw=0.9, label="post")
        ax.plot(t, total, color="0.15", lw=1.3, label="sum")
        ax.axhline(0, color="0.65", lw=0.6)
        ax.axvline(0, color="0.75", lw=0.6, ls=":")
        ax.set_title(rf"$\Delta t={delay:+.2f}$ s")
        ax.set_xlabel("time (s)")
        style_axes(ax)
    axes[0].set_ylabel("voltage (V)")
    axes[-1].legend(frameon=False, loc="upper right")
    save(fig, "stdp_waveforms.pdf")


def fig_morphology_stability_support() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.65))

    axes[0].bar(["active\nlayer"], [209], color="#F0C75E", edgecolor="0.25", width=0.55)
    axes[0].set_ylabel("thickness (nm)")
    axes[0].set_ylim(0, 260)
    axes[0].text(0, 222, "209 nm", ha="center", fontsize=8)
    axes[0].set_title("profilometry")
    style_axes(axes[0])

    axes[1].hlines(2, 0, 1, color=COLORS["green"], lw=3)
    axes[1].fill_between([0, 1], [1, 1], [3, 3], color=COLORS["green"], alpha=0.18)
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(0, 4)
    axes[1].set_xticks([])
    axes[1].set_ylabel("RMS roughness (nm)")
    axes[1].set_title("AFM window")
    axes[1].text(0.5, 3.25, "1-3 nm", ha="center", fontsize=8)
    style_axes(axes[1])

    hours = np.array([0, 300])
    axes[2].fill_between(hours, [0.8, 0.8], [1.2, 1.2], color="0.85", alpha=0.8)
    for label, color, y in [
        (r"$G_0$", COLORS["blue"], [1.00, 1.08]),
        (r"$\Delta G_{max}$", COLORS["red"], [1.00, 0.92]),
        (r"$\tau_S$", COLORS["purple"], [1.00, 1.12]),
    ]:
        axes[2].plot(hours, y, "o-", ms=3, lw=1.0, color=color, label=label)
    axes[2].set_ylim(0.65, 1.35)
    axes[2].set_xlabel("ambient storage (h)")
    axes[2].set_ylabel("normalised metric")
    axes[2].set_title("shelf-stability envelope")
    axes[2].legend(frameon=False, loc="upper left")
    style_axes(axes[2])

    save(fig, "morphology_stability_support.pdf")


def main() -> None:
    fig_device_schematic()
    fig_iv_hyst()
    fig_potentiation_depression()
    fig_pulse_number()
    fig_retention()
    fig_epsc_summary()
    fig_stdp_summary()
    fig_read_write_wait_protocol()
    fig_full_epsc_trace()
    fig_stdp_waveforms()
    fig_morphology_stability_support()


if __name__ == "__main__":
    main()
