#!/usr/bin/env python3
"""Generate the three Chapter-3 figures into figures/chapter4/.

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
FIGDIR = "figures/chapter4"

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


def fig_design_space():
    """Per-device (Ag-only) design space: fading memory t_half vs potentiation
    dynamic range (peak ratio), coloured by PEO, marked by salt. Shows BOTH the
    PEO coupling and the genuine device-to-device scatter (the reservoir resource).
    Reads handouts/ch4_decay_fits.csv + ch4_pulse_descriptors.csv (Li, Ag)."""
    import collections
    dec = collections.defaultdict(list); pul = collections.defaultdict(list); meta = {}
    for r in csv.DictReader(open(os.path.join(OUT, "ch4_decay_fits.csv"))):
        if r["cation"] != "Li":
            continue
        th = fnum(r.get("t_half_s"))
        if th:
            dec[r["device_id"]].append(th); meta[r["device_id"]] = (r["peo"], r["salt"])
    for r in csv.DictReader(open(os.path.join(OUT, "ch4_pulse_descriptors.csv"))):
        if r["cation"] != "Li":
            continue
        pk = fnum(r.get("peak_ratio"))
        if pk:
            pul[r["device_id"]].append(pk); meta[r["device_id"]] = (r["peo"], r["salt"])
    both = sorted(set(dec) & set(pul))

    peo_col = {"0.15": "#6a3d9a", "0.3": "#1f78b4", "0.6": "#33a02c", "1.2": "#e31a1c"}
    salt_mk = {"0.045": "o", "0.09": "s", "0.18": "^"}
    fig, ax = plt.subplots(figsize=(5.0, 3.6))
    for d in both:
        peo, salt = meta[d]
        ax.scatter(np.median(pul[d]), np.median(dec[d]),
                   c=peo_col.get(peo, "0.4"), marker=salt_mk.get(salt, "o"),
                   s=42, edgecolor="0.2", linewidth=0.4, alpha=0.85)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("potentiation dynamic range (peak ratio)")
    ax.set_ylabel("fading-memory time $t_{1/2}$ (s)")
    ax.set_title("Per-device design space (Ag, Li)")
    # legends: colour = PEO, marker = salt
    from matplotlib.lines import Line2D
    ph = [Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=7,
                 markeredgecolor="0.2", label=f"PEO {p}") for p, c in peo_col.items()]
    sh = [Line2D([0], [0], marker=m, color="w", markerfacecolor="0.6", markersize=7,
                 markeredgecolor="0.2", label=f"salt {s}") for s, m in salt_mk.items()]
    leg1 = ax.legend(handles=ph, fontsize=7, loc="lower right", title="colour", title_fontsize=7)
    ax.add_artist(leg1)
    ax.legend(handles=sh, fontsize=7, loc="upper left", title="shape", title_fontsize=7)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "design_space.pdf"); fig.savefig(p); plt.close(fig)
    print("wrote", p, f"| {len(both)} devices")


# ----------------------------------------------------------------------------
# Figure 0 — representative raw curves (HYST / PULSES / DELAYTIME)
# ----------------------------------------------------------------------------
# Grounds every summary metric in what the measurements actually look like.
# Exemplar devices are chosen to sit near their cell medians (not cherry-picked
# extremes); all are SY/PEO/LiTr/Ag from the replicated composition spine.
def _stretched(t, A, tau, beta, C):
    return A * np.exp(-((t / tau) ** beta)) + C


def fig_representative():
    flags = filtered_flags()

    # ---- panel (a): HYST I-V loops, wide (low-PEO) vs narrow (high-PEO) ----
    def hyst_curve(dev):
        """Return (V, I) of the curve whose on-off ratio is nearest this device's
        median, excluding FILTERED/broken curves."""
        ratios = {}
        for r in load("DEVICES_HYST_CURVE_INFO.csv"):
            if g(r, "device_name") != dev:
                continue
            if (dev, g(r, "day"), g(r, "pixel"), "HYST") in flags:
                continue
            if g(r, "is broken").lower() in ("true", "1"):
                continue
            rr = fnum(g(r, "on-off ratio"))
            if rr is not None and np.isfinite(rr):
                ratios[(g(r, "day"), g(r, "pixel"), g(r, "curve"))] = rr
        if not ratios:
            return None, None, None
        target = np.median(list(ratios.values()))
        key = min(ratios, key=lambda k: abs(ratios[k] - target))
        pts = []
        for r in load("DEVICES_HYST_ALL_DATAPOINTS.csv"):
            if (g(r, "device_name"), g(r, "day"), g(r, "pixel"), g(r, "curve")) == (dev,) + key:
                v, i, n = fnum(g(r, "voltage (V)")), fnum(g(r, "current (uA)")), fnum(g(r, "curve data point"))
                if v is not None and i is not None and n is not None:
                    pts.append((n, v, i))
        pts.sort()
        return (np.array([p[1] for p in pts]), np.array([p[2] for p in pts]), ratios[key])

    # ---- panel (b): PULSES potentiation, three qualitative shapes ----
    def pulse_curve(dev):
        pts = []
        for r in load("DEVICES_PULSES_CURVE_INFO.csv"):
            if g(r, "device_name") != dev:
                continue
            if (dev, g(r, "day"), g(r, "pixel"), "PULSES") in flags:
                continue
            N, y = fnum(g(r, "number of pulses")), fnum(g(r, "ratio"))
            if N and N > 0 and y is not None:
                pts.append((N, y))
        pts = sorted(set(pts))
        return np.array([p[0] for p in pts]), np.array([p[1] for p in pts])

    # ---- panel (c): DELAYTIME decay with stretched-exp overlay + t_half ----
    def decay_curve(dev):
        pts = []
        for r in load("DEVICES_DELAYTIME_CURVE_INFO.csv"):
            if g(r, "device_name") != dev:
                continue
            if (dev, g(r, "day"), g(r, "pixel"), "DELAYTIME") in flags:
                continue
            t, y = fnum(g(r, "delay time (s)")), fnum(g(r, "ratio"))
            if t and t > 0 and y is not None:
                pts.append((t, y))
        pts = sorted(set(pts))
        return np.array([p[0] for p in pts]), np.array([p[1] for p in pts])

    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.7))

    # (a) HYST: each loop normalised to its own peak current, so the comparison
    # is the loop *openness* (switching window), not absolute conductance --- the
    # high-PEO device carries more current but opens a narrower window.
    ax = axes[0]
    for dev, lab, col in [("NM_v146", "PEO 0.3: wider window", "#1f78b4"),
                          ("NM_v144", "PEO 1.2: narrower", "#e31a1c")]:
        V, I, rr = hyst_curve(dev)
        if V is not None and np.nanmax(np.abs(I)) > 0:
            ax.plot(V, I / np.nanmax(I), color=col, lw=1.0, label=lab)
    ax.set_xlabel("voltage (V)"); ax.set_ylabel("current / peak current")
    ax.set_title("(a) hysteresis loop (norm., salt 0.09)")
    ax.legend(frameon=False, fontsize=7, loc="upper left")

    # (b) PULSES
    ax = axes[1]
    for dev, lab, col, mk in [("NM_v241", "0.3/0.09: strong, $\\alpha{\\approx}0.9$", "#1f78b4", "o"),
                              ("NM_v244", "0.3/0.045: turnover", "#33a02c", "^"),
                              ("NM_v155", "1.2/0.09: compressive, $\\alpha{\\approx}0.4$", "#e31a1c", "s")]:
        N, y = pulse_curve(dev)
        if len(N):
            ax.plot(N, y, color=col, lw=1.0, marker=mk, ms=3.5, label=lab)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("number of pulses $N$"); ax.set_ylabel("conductance ratio")
    ax.set_title("(b) pulse potentiation")
    ax.legend(frameon=False, fontsize=6.3, loc="lower right")

    # (c) DELAYTIME
    ax = axes[2]
    for dev, lab, col, mk in [("NM_v146", "PEO 0.3: $t_{1/2}{\\approx}22$ s", "#1f78b4", "o"),
                              ("NM_v144", "PEO 1.2: $t_{1/2}{\\approx}6$ s", "#e31a1c", "s")]:
        t, y = decay_curve(dev)
        if len(t) < 4:
            continue
        y0 = y / y[0]
        ax.scatter(t, y0, s=18, color=col, marker=mk, zorder=3)
        try:
            p, _ = curve_fit(_stretched, t, y0, p0=[max(y0.max() - y0.min(), 1e-3),
                             float(np.median(t)), 0.7, max(y0.min(), 0.0)],
                             bounds=([0, 1e-2, 0.1, 0], [np.inf, 1e5, 2.0, np.inf]), maxfev=40000)
            tt = np.logspace(np.log10(t.min()), np.log10(t.max()), 200)
            ax.plot(tt, _stretched(tt, *p), color=col, lw=1.1, label=lab)
            # mark half-enhancement time
            thalf = p[1] * (np.log(p[0] / (0.5 - p[3]))) ** (1.0 / p[2]) if (0.5 - p[3]) > 0 else np.nan
        except Exception:
            ax.plot(t, y0, color=col, lw=1.0, label=lab)
        ax.axhline(0.5, color="0.7", lw=0.6, ls=":")
    ax.set_xscale("log")
    ax.set_xlabel("delay time (s)"); ax.set_ylabel("normalised enhancement")
    ax.set_title("(c) fading-memory decay")
    ax.legend(frameon=False, fontsize=6.6, loc="upper right")

    fig.tight_layout()
    p = os.path.join(FIGDIR, "representative_curves.pdf")
    fig.savefig(p); plt.close(fig)
    print("wrote", p)


# ----------------------------------------------------------------------------
# Figure 1c — heterogeneity: per-device spread of t_half and alpha by PEO
# ----------------------------------------------------------------------------
# Shows the within-cell device-to-device scatter that the cell-median heatmaps
# average away, and that Chapter 4 exploits as reservoir heterogeneity.
def fig_heterogeneity():
    import collections as _c

    def dev_medians(path, col, want_cols=("peo",)):
        d = _c.defaultdict(list); meta = {}
        for r in csv.DictReader(open(os.path.join(OUT, path))):
            if r["cation"] != "Li":
                continue
            v = fnum(r.get(col))
            if v is not None and np.isfinite(v):
                d[r["device_id"]].append(v)
                meta[r["device_id"]] = tuple(r[w] for w in want_cols)
        return {k: (np.median(v), meta[k]) for k, v in d.items()}

    th = dev_medians("ch4_decay_fits.csv", "t_half_s")
    al = dev_medians("ch4_pulse_descriptors.csv", "growth_exp")

    peo_order = ["0.3", "0.6", "1.2"]
    peo_col = {"0.3": "#1f78b4", "0.6": "#33a02c", "1.2": "#e31a1c"}

    def swarm(ax, data, ylabel, logy=False):
        rng = np.random.default_rng(0)
        for xi, peo in enumerate(peo_order):
            vals = [v for v, (p,) in data.values() if p == peo]
            if not vals:
                continue
            jit = rng.uniform(-0.13, 0.13, size=len(vals))
            ax.scatter(np.full(len(vals), xi) + jit, vals, s=34, color=peo_col[peo],
                       edgecolor="0.2", linewidth=0.4, alpha=0.85, zorder=3)
            ax.scatter([xi], [np.median(vals)], marker="_", s=900, color="0.15",
                       linewidth=1.8, zorder=4)
        ax.set_xticks(range(len(peo_order))); ax.set_xticklabels(peo_order)
        ax.set_xlabel("PEO mass fraction"); ax.set_ylabel(ylabel)
        if logy:
            ax.set_yscale("log")

    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.9))
    swarm(axes[0], th, "fading-memory time $t_{1/2}$ (s)", logy=True)
    axes[0].set_title("(a) retention spread")
    swarm(axes[1], al, r"growth exponent $\alpha$")
    axes[1].set_title("(b) potentiation-strength spread")
    fig.tight_layout()
    p = os.path.join(FIGDIR, "heterogeneity.pdf")
    fig.savefig(p); plt.close(fig)
    print("wrote", p)


def main():
    os.makedirs(FIGDIR, exist_ok=True)
    fig_representative()
    fig_heterogeneity()
    fig_composition()
    fig_potentiation()
    fig_chemistry()
    fig_protocol()
    fig_design_space()


if __name__ == "__main__":
    main()
