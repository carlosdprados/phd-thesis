#!/usr/bin/env python3
"""Generate the three Chapter-3 figures into figures/chapter3/.

Run from the repo root:  python3 scripts/ch3_figures.py
Depends on the per-cell summaries written by scripts/ch3_4_dynamics_fits.py
(run that first) and on the (un-versioned) DATABASE in Nanomem_Devices_Library/.

Figures produced (matching the \\label's in chapters/chapter3_comparative.tex):
  fig:ch3_composition_heatmaps -> composition_heatmaps.pdf
  fig:ch3_chemistry_landscape  -> chemistry_landscape.pdf
  fig:ch3_protocol             -> protocol_overlay.pdf

Honesty notes:
- Composition panels are the quantitative spine: HYST window metrics are recomputed
  here from the DATABASE (FILTERED-flagged HYST curves excluded); fading-memory t_half
  is read from handouts/ch3_decay_by_cell.csv. Per-cell device counts are annotated.
- The chemistry-landscape values are *illustrative* (n<=2 on at least one side) and are
  taken from the PNG-reviewed per-device fits recorded in handouts/08 (sections 14-15)
  and the curation registry; every bar is labelled with its n.
- The protocol panel fits v114 pixel R4 at its two protocols directly from the DATABASE.
"""
import csv, os, collections
import numpy as np
from scipy.optimize import curve_fit

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm

DB = "../Nanomem_Devices_Library/DATABASE"
OUT = "handouts"
FIGDIR = "figures/chapter3"

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
})

PEO_LEVELS = ["0.3", "0.6", "1.2"]      # replicated composition grid (chapter caption)
SALT_LEVELS = ["0.045", "0.09", "0.18"]


def load(f):
    with open(os.path.join(DB, f), newline="") as fh:
        return list(csv.DictReader(fh))


def g(r, k):
    return (r.get(k) or "").strip()


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


def med(v):
    v = [x for x in v if x is not None and np.isfinite(x)]
    return float(np.median(v)) if v else float("nan")


# ----------------------------------------------------------------------------
# Composition cell map (PEO/LiTr/Ag) + FILTERED flags
# ----------------------------------------------------------------------------
def composition_cells():
    cell = {}
    for r in csv.DictReader(open(os.path.join(OUT, "ch4_device_manifest_DRAFT.csv"))):
        if r["host"] == "PEO" and r["cation"] == "Li" and r["electrode"] == "Ag":
            cell[r["device_id"]] = (r["peo_mass_fraction"], r["salt_mass_fraction"])
    return cell


def filtered_flags():
    flags = set()
    for r in load("FILTERED_DEVICES.csv"):
        flags.add((g(r, "device_name"), g(r, "day"), g(r, "pixel"), g(r, "measurement_type")))
    return flags


def hyst_grid(cell, flags):
    """Per-cell median on-off ratio and |normalized area| from clean HYST curves."""
    ratio = collections.defaultdict(list)   # (peo,salt) -> [device medians]
    area = collections.defaultdict(list)
    dev_ratio = collections.defaultdict(list)   # device -> values
    dev_area = collections.defaultdict(list)
    dev_cell = {}
    for r in load("DEVICES_HYST_CURVE_INFO.csv"):
        dn = g(r, "device_name")
        if dn not in cell:
            continue
        if (dn, g(r, "day"), g(r, "pixel"), "HYST") in flags:
            continue
        if g(r, "is broken").lower() in ("true", "1"):
            continue
        rr = fnum(g(r, "on-off ratio")); ar = fnum(g(r, "normalized area"))
        if rr is not None and np.isfinite(rr):
            dev_ratio[dn].append(rr)
        if ar is not None and np.isfinite(ar):
            dev_area[dn].append(abs(ar))
        dev_cell[dn] = cell[dn]
    for dn, c in dev_cell.items():
        if dev_ratio[dn]:
            ratio[c].append(med(dev_ratio[dn]))
        if dev_area[dn]:
            area[c].append(med(dev_area[dn]))
    return ratio, area


def thalf_grid():
    """(peo,salt) -> (median t_half, n_dev) from ch3_decay_by_cell.csv (Li only)."""
    th = {}
    for r in csv.DictReader(open(os.path.join(OUT, "ch3_decay_by_cell.csv"))):
        if r["cation"] != "Li":
            continue
        if r["t_half_med"]:
            th[(r["peo"], r["salt"])] = (float(r["t_half_med"]), int(r["n_dev"]))
    return th


# ----------------------------------------------------------------------------
# Figure 1 — composition heatmaps
# ----------------------------------------------------------------------------
def fig_composition():
    cell = composition_cells(); flags = filtered_flags()
    ratio, area = hyst_grid(cell, flags); th = thalf_grid()

    def grid(d, transform=lambda x: med(x)):
        M = np.full((len(PEO_LEVELS), len(SALT_LEVELS)), np.nan)
        N = np.zeros_like(M)
        for i, peo in enumerate(PEO_LEVELS):
            for j, salt in enumerate(SALT_LEVELS):
                v = d.get((peo, salt))
                if v:
                    M[i, j] = transform(v); N[i, j] = len(v)
        return M, N

    Mr, Nr = grid(ratio); Ma, Na = grid(area)
    # t_half: dict already holds (val,n)
    Mt = np.full((len(PEO_LEVELS), len(SALT_LEVELS)), np.nan)
    Nt = np.zeros_like(Mt)
    for i, peo in enumerate(PEO_LEVELS):
        for j, salt in enumerate(SALT_LEVELS):
            if (peo, salt) in th:
                Mt[i, j], Nt[i, j] = th[(peo, salt)]

    panels = [
        (Mr, Nr, "(a) on--off ratio", "viridis", "{:.1f}", False),
        (Ma, Na, "(b) |normalised area|", "magma", "{:.2f}", False),
        (Mt, Nt, "(c) fading time $t_{1/2}$ (s)", "cividis", "{:.0f}", True),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.7))
    for ax, (M, N, title, cmap, fmt, islog) in zip(axes, panels):
        Mm = np.ma.masked_invalid(M)
        if islog:
            vmin = np.nanmin(M[np.isfinite(M)]); vmax = np.nanmax(M[np.isfinite(M)])
            im = ax.imshow(Mm, cmap=cmap, norm=LogNorm(vmin=max(vmin, 1e-2), vmax=vmax), aspect="auto")
        else:
            im = ax.imshow(Mm, cmap=cmap, aspect="auto")
        ax.set_title(title)
        ax.set_xticks(range(len(SALT_LEVELS))); ax.set_xticklabels(SALT_LEVELS)
        ax.set_yticks(range(len(PEO_LEVELS))); ax.set_yticklabels(PEO_LEVELS)
        ax.set_xlabel("salt mass fraction")
        if ax is axes[0]:
            ax.set_ylabel("PEO mass fraction")
        for i in range(len(PEO_LEVELS)):
            for j in range(len(SALT_LEVELS)):
                if np.isfinite(M[i, j]):
                    # contrast-aware text colour
                    norm = (M[i, j] - np.nanmin(M)) / (np.nanmax(M) - np.nanmin(M) + 1e-12)
                    tc = "white" if norm < 0.5 else "black"
                    ax.text(j, i, fmt.format(M[i, j]) + f"\n$n{{=}}{int(N[i, j])}$",
                            ha="center", va="center", color=tc, fontsize=7.5)
                else:
                    ax.text(j, i, "--", ha="center", va="center", color="0.5", fontsize=8)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "composition_heatmaps.pdf")
    fig.savefig(p); plt.close(fig)
    print("wrote", p)


# ----------------------------------------------------------------------------
# Figure 1b — potentiation (pulse-integration) control over the composition grid
# ----------------------------------------------------------------------------
def fig_potentiation():
    """Per-cell growth exponent, peak dynamic range, and turnover fraction from
    handouts/ch3_pulses_by_cell.csv (Li composition grid)."""
    alpha = {}; peak = {}; turn = {}; ndev = {}
    for r in csv.DictReader(open(os.path.join(OUT, "ch3_pulses_by_cell.csv"))):
        if r["cation"] != "Li":
            continue
        key = (r["peo"], r["salt"])
        ndev[key] = int(r["n_dev"])
        if r["growth_exp_med"]:
            alpha[key] = float(r["growth_exp_med"])
        if r["peak_ratio_med"]:
            peak[key] = float(r["peak_ratio_med"])
        turn[key] = float(r["turnover_pct"])

    def grid(d):
        M = np.full((len(PEO_LEVELS), len(SALT_LEVELS)), np.nan)
        N = np.zeros_like(M)
        for i, peo in enumerate(PEO_LEVELS):
            for j, salt in enumerate(SALT_LEVELS):
                if (peo, salt) in d:
                    M[i, j] = d[(peo, salt)]
                N[i, j] = ndev.get((peo, salt), 0)
        return M, N

    Ma, Na = grid(alpha); Mp, Np = grid(peak); Mt, Nt = grid(turn)
    panels = [
        (Ma, Na, r"(a) growth exponent $\alpha$", "viridis", "{:.2f}", False),
        (Mp, Np, "(b) peak ratio (dynamic range)", "magma", "{:.0f}", True),
        (Mt, Nt, "(c) turnover fraction (\\%)", "cividis", "{:.0f}", False),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.7))
    for ax, (M, N, title, cmap, fmt, islog) in zip(axes, panels):
        Mm = np.ma.masked_invalid(M)
        if islog:
            vmin = np.nanmin(M[np.isfinite(M)]); vmax = np.nanmax(M[np.isfinite(M)])
            im = ax.imshow(Mm, cmap=cmap, norm=LogNorm(vmin=max(vmin, 1), vmax=vmax), aspect="auto")
        else:
            im = ax.imshow(Mm, cmap=cmap, aspect="auto")
        ax.set_title(title)
        ax.set_xticks(range(len(SALT_LEVELS))); ax.set_xticklabels(SALT_LEVELS)
        ax.set_yticks(range(len(PEO_LEVELS))); ax.set_yticklabels(PEO_LEVELS)
        ax.set_xlabel("salt mass fraction")
        if ax is axes[0]:
            ax.set_ylabel("PEO mass fraction")
        for i in range(len(PEO_LEVELS)):
            for j in range(len(SALT_LEVELS)):
                if np.isfinite(M[i, j]):
                    norm = (M[i, j] - np.nanmin(M)) / (np.nanmax(M) - np.nanmin(M) + 1e-12)
                    tc = "white" if norm < 0.5 else "black"
                    ax.text(j, i, fmt.format(M[i, j]) + f"\n$n{{=}}{int(N[i, j])}$",
                            ha="center", va="center", color=tc, fontsize=7.5)
                else:
                    ax.text(j, i, "--", ha="center", va="center", color="0.5", fontsize=8)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "potentiation_grid.pdf")
    fig.savefig(p); plt.close(fig)
    print("wrote", p)


# ----------------------------------------------------------------------------
# Figure 2 — chemistry-tuning landscape (illustrative; values from handout 08 sec 14-15)
# ----------------------------------------------------------------------------
def fig_chemistry():
    # Values are PNG-reviewed per-device fits (simple-exp tau, s) from handout 08
    # sec 13-15 and the curation registry; all SY, 0.3/0.09, Ag, matched 4 V/2 V.
    host = [("PEO/LiTr", 22.0, 3), ("TMPE/LiTr", 3.8, 1)]                       # sec 15 (Ag)
    anion = [("PEO/Tr", 20.0, 3), ("PEO/TFSI", 0.4, 1)]                         # sec 14 (v321)
    # Cation: TMPE host, both anions -> the order inverts with the anion (honest negative).
    cation_tr = [3.8, 5.0, 6.7]            # TMPE/triflate v250/v251/v252, n=1 each (sec 13)
    cation_tfsi = [6.3, 7.0, 3.5]          # TMPE/TFSI v333-338, n=2 each (sec 14)

    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.9), sharey=True)
    # --- panels 1-2: simple two-bar comparisons ---
    for ax, (title, data, colours) in zip(
            axes[:2],
            [("Host\n(Li-triflate)", host, ["#4c72b0", "#dd8452"]),
             ("Anion\n(PEO host)", anion, ["#4c72b0", "#c44e52"])]):
        labels = [d[0] for d in data]; vals = [d[1] for d in data]; ns = [d[2] for d in data]
        x = np.arange(len(data))
        bars = ax.bar(x, vals, color=colours, width=0.62, edgecolor="0.2", linewidth=0.5)
        ax.set_yscale("log"); ax.set_title(title)
        ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8)
        for b, v, n in zip(bars, vals, ns):
            ax.text(b.get_x() + b.get_width() / 2, v * 1.08, f"{v:g}s\n$n{{=}}{n}$",
                    ha="center", va="bottom", fontsize=7.5)
        ax.set_ylim(0.2, 60)
    # --- panel 3: cation, TMPE host, grouped by anion (shows the order inverting) ---
    ax = axes[2]
    cats = ["Li", "Na", "K"]; x = np.arange(3); w = 0.38
    b1 = ax.bar(x - w / 2, cation_tr, w, color="#55a868", edgecolor="0.2", linewidth=0.5, label="triflate ($n{=}1$)")
    b2 = ax.bar(x + w / 2, cation_tfsi, w, color="#c44e52", edgecolor="0.2", linewidth=0.5, label="TFSI ($n{=}2$)")
    ax.set_yscale("log"); ax.set_title("Cation\n(TMPE host)")
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=8)
    for bars, vals in [(b1, cation_tr), (b2, cation_tfsi)]:
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v * 1.06, f"{v:g}", ha="center", va="bottom", fontsize=7)
    ax.set_ylim(0.2, 60)
    ax.legend(frameon=False, fontsize=6.5, loc="upper center", ncol=1)
    axes[0].set_ylabel("fading-memory time (s)")
    fig.tight_layout()
    p = os.path.join(FIGDIR, "chemistry_landscape.pdf")
    fig.savefig(p); plt.close(fig)
    print("wrote", p)


# ----------------------------------------------------------------------------
# Figure 3 — drive-protocol overlay (v114 pixel R4, two protocols)
# ----------------------------------------------------------------------------
def fig_protocol():
    # Simple (single) exponential, matching the methodology behind the chapter's
    # 4.6 s -> 15.5 s figure (handout 08 sec 13). The 4-parameter stretched form is
    # degenerate on the clean 6 V curve (tau/beta trade-off), so the single
    # exponential A*exp(-t/tau)+C is used here for a like-for-like comparison.
    def expdecay(t, A, tau, C):
        return A * np.exp(-t / tau) + C

    dly = load("DEVICES_DELAYTIME_CURVE_INFO.csv")

    def curve(day):
        pts = []
        for r in dly:
            if g(r, "device_name") == "NM_v114" and g(r, "pixel") == "R4" and g(r, "day") == day:
                t, y = fnum(g(r, "delay time (s)")), fnum(g(r, "ratio"))
                if t and t > 0 and y is not None:
                    pts.append((t, y))
        pts = sorted(set(pts))
        return np.array([p[0] for p in pts]), np.array([p[1] for p in pts])

    def fit(t, y):
        y0 = y / y[0]   # normalise to the shortest-delay enhancement
        p, _ = curve_fit(expdecay, t, y0, p0=[max(y0.max() - y0.min(), 1e-3),
                         float(np.median(t)), max(y0.min(), 0.0)],
                         bounds=([0, 1e-2, 0], [np.inf, 1e5, np.inf]), maxfev=40000)
        yhat = expdecay(t, *p); r2 = 1 - np.sum((y0 - yhat) ** 2) / np.sum((y0 - y0.mean()) ** 2)
        return y0, p, r2

    t3, y3 = curve("2")    # 1.5 V read / 3 V write
    t6, y6 = curve("13")   # 3.0 V read / 6 V write
    y3n, p3, r2_3 = fit(t3, y3)
    y6n, p6, r2_6 = fit(t6, y6)
    tt = np.logspace(np.log10(0.5), np.log10(300), 200)

    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    ax.scatter(t3, y3n, s=22, color="#4c72b0", label=fr"3 V write: $\tau={p3[1]:.1f}$ s", zorder=3)
    ax.plot(tt, expdecay(tt, *p3), color="#4c72b0", lw=1.2)
    ax.scatter(t6, y6n, s=22, color="#c44e52", marker="s", label=fr"6 V write: $\tau={p6[1]:.1f}$ s", zorder=3)
    ax.plot(tt, expdecay(tt, *p6), color="#c44e52", lw=1.2)
    ax.set_xscale("log")
    ax.set_xlabel("delay time (s)")
    ax.set_ylabel("normalised conductance enhancement")
    ax.set_title("NM\\_v114 (R4): same device, two drive amplitudes")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "protocol_overlay.pdf")
    fig.savefig(p); plt.close(fig)
    print("wrote", p, f"| tau3={p3[1]:.2f}s (R2={r2_3:.2f}) tau6={p6[1]:.2f}s (R2={r2_6:.2f})")


def main():
    os.makedirs(FIGDIR, exist_ok=True)
    fig_composition()
    fig_potentiation()
    fig_chemistry()
    fig_protocol()


if __name__ == "__main__":
    main()
