#!/usr/bin/env python3
"""bridge_figures.py — render the bridge-chapter figures (F1-F4).

Reuses the loaders and corpus definition of
scripts/bridge_hybrane_peo_reproducibility.py so that the figures plot exactly
the same per-device, standard-protocol, amplitude-matched quantities that the
audit script tests (and only the numbers it prints).

Run from the repo root:  python scripts/bridge_figures.py
Writes PDFs into figures/chapter3/:
  F1  bridge_window_collapse.pdf   on-off & normalized area @3V, early vs later
  F2  bridge_mechanism.pdf         ohmic drift @1.2V vs date (+ methodology panels)
  F3  bridge_resolution.pdf        Hy vs PEO @3V, and PEO on-off vs year 2022-24
  F4  bridge_annealing_recovery.pdf  late-device window restored by hot anneal
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

import figstyle

from bridge_hybrane_peo_reproducibility import load, hybrane_standard, DB, TAIL

FIGDIR = "figures/chapter3"
INFL = pd.Timestamp("2021-05-01")  # post-NM_v026 inflection (2021-04-22)

figstyle.apply()
COLORS = figstyle.COLORS

C_EARLY = COLORS["blue"]    # early / pristine
C_LATE = COLORS["orange"]   # later / degraded
C_PEO = COLORS["green"]     # PEO host
C_HOT = COLORS["purple"]    # elevated-T anneal


def per_device(df, col, date_map):
    """One value per device: median across its freshest-day curves. -> (date, y)."""
    d = df.dropna(subset=[col]).copy()
    d["_v"] = pd.to_numeric(d[col], errors="coerce")
    fd = d.groupby("device_name")["day"].transform("min")
    d = d[d["day"] == fd]
    pdv = d.groupby("device_name").agg(date=("date", "first"), y=("_v", "median")).dropna()
    return pdv


def jitter(n, w=0.08):
    return (np.random.RandomState(0).rand(n) - 0.5) * 2 * w


def box_strip(ax, groups, labels, colors, ylabel, title, log=False, letter=None):
    data = [g.values for g in groups]
    bp = ax.boxplot(data, widths=0.45, showfliers=False, patch_artist=True,
                    medianprops=dict(color="black", lw=1.5),
                    whiskerprops=dict(color="0.4", lw=0.9),
                    capprops=dict(color="0.4", lw=0.9))
    for patch, c in zip(bp["boxes"], colors):
        patch.set_facecolor(mcolors.to_rgba(c, 0.16))
        patch.set_edgecolor(c)
        patch.set_linewidth(1.0)
    for i, (g, c) in enumerate(zip(groups, colors), start=1):
        x = np.full(len(g), i) + jitter(len(g))
        ax.scatter(x, g.values, s=16, color=c, edgecolor="white", lw=0.4,
                   alpha=0.9, zorder=3)
    ax.set_xticks(range(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_ylabel(ylabel)
    if letter:
        figstyle.panel(ax, letter, title)
    else:
        ax.set_title(title, loc="left")
    if log:
        ax.set_yscale("log")


def median_labels(ax, groups, colors, fmt="{:.2f}", dx=0.32):
    """Direct median read-outs beside each box, in the group colour."""
    for i, (g, c) in enumerate(zip(groups, colors), start=1):
        ax.text(i + dx, g.median(), fmt.format(g.median()), color=c,
                fontsize=7, ha="left", va="center", fontweight="bold")


def sig_bracket(ax, x1, x2, y, text):
    """Nature-style significance bracket between group positions x1 and x2."""
    yl = ax.get_ylim()
    h = (yl[1] - yl[0]) * 0.03
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], color="0.25", lw=0.9,
            solid_capstyle="butt", clip_on=False)
    ax.text((x1 + x2) / 2, y + 1.4 * h, text, ha="center", va="bottom",
            fontsize=7.5, color="0.15")
    if yl[1] < y + 7 * h:
        ax.set_ylim(yl[0], y + 7 * h)


def date_axis(ax, maxticks=5):
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=maxticks))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))


# ---------------------------------------------------------------------------
def main():
    os.makedirs(FIGDIR, exist_ok=True)
    L = load()
    std = hybrane_standard(L)
    date = dict(zip(std["device_name"], std["Date"]))
    stdset = set(std["device_name"])

    cur = pd.read_csv(os.path.join(DB, "DEVICES_HYST_CURVE_INFO.csv"), low_memory=False)
    cur = cur[cur["device_name"].isin(stdset)].copy()
    cur["date"] = cur["device_name"].map(date)
    mv = pd.to_numeric(cur["max voltage (V)"], errors="coerce")
    cur12 = cur[(mv >= 1.0) & (mv <= 1.45)].copy()   # conductivity probe
    cur3 = cur[(mv >= 2.6) & (mv <= 3.4)].copy()      # window probe

    # ===================== F1 — window collapse @3V ========================
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2))
    for ax, col, ylab, letter, ttl, fmt in [
        (axes[0], "on-off ratio", "on–off ratio at 3 V", "a", "switching window", "{:.2f}"),
        (axes[1], "normalized area", "normalized area at 3 V", "b", "normalized hysteresis area", "{:.3f}"),
    ]:
        pdv = per_device(cur3, col, date)
        e = pdv[pdv["date"] < INFL]["y"]
        l = pdv[pdv["date"] >= INFL]["y"]
        _, p = stats.mannwhitneyu(e, l, alternative="two-sided")
        box_strip(ax, [e, l],
                  [f"early\n($\\leq$Apr 2021)\nn={len(e)}", f"later\nn={len(l)}"],
                  [C_EARLY, C_LATE], ylab, ttl, letter=letter)
        median_labels(ax, [e, l], [C_EARLY, C_LATE], fmt)
        yl = ax.get_ylim()
        sig_bracket(ax, 1, 2, max(e.max(), l.max()) + 0.04 * (yl[1] - yl[0]),
                    f"$p={p:.4f}$")
        ax.set_xlim(0.45, 2.75)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "bridge_window_collapse.pdf"))
    plt.close(fig)
    print("F1 written:", os.path.join(FIGDIR, "bridge_window_collapse.pdf"))

    # ===================== F2 — mechanism + methodology ====================
    fig = plt.figure(figsize=(9.4, 3.3))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.25, 0.85, 1.15], wspace=0.45)
    axA, axB, axC = (fig.add_subplot(gs[0, i]) for i in range(3))

    # (a) ohmic drift at matched ~1.2 V, log y, recovery tail marked
    ax = axA
    pdv_full = per_device(cur12, "area (V*uA)", date)
    # Spearman on the full per-device set (matches tab:bridge_degradation);
    # the log display below can only show the positive areas.
    xd_full = (pdv_full["date"] - pdv_full["date"].min()).dt.days.values.astype(float)
    tail_full = (pdv_full["date"] >= TAIL).values
    rho_all, p_all = stats.spearmanr(xd_full, pdv_full["y"].values)
    rho_dt, p_dt = stats.spearmanr(xd_full[~tail_full], pdv_full["y"].values[~tail_full])
    print(f"F2a Spearman: rho_all={rho_all:+.2f} (p={p_all:.2g}), "
          f"rho_droptail={rho_dt:+.2f} (p={p_dt:.2g}), n={len(pdv_full)}")
    pdv = pdv_full[pdv_full["y"] > 0]
    x = pdv["date"]
    tail = pdv["date"] >= TAIL
    ax.scatter(x[~tail], pdv["y"][~tail], s=20, color=C_LATE, edgecolor="white",
               lw=0.4, alpha=0.9, label="standard corpus")
    ax.scatter(x[tail], pdv["y"][tail], s=30, marker="D", facecolor="none",
               edgecolor=C_HOT, lw=1.1, label="recovery tail ($\\geq$2022-03)")
    ax.set_yscale("log")
    ax.set_ylabel("hysteresis area at 1.2 V  (V$\\cdot\\mu$A)")
    ax.set_xlabel("fabrication date")
    figstyle.panel(ax, "a", "ohmic drift at matched $\\sim$1.2 V")
    ax.text(0.03, 0.97, "Spearman vs date\n"
            f"$\\rho={rho_all:+.2f}$ (all)\n$\\rho={rho_dt:+.2f}$ (drop tail)",
            transform=ax.transAxes, ha="left", va="top", fontsize=7.5, color="0.25")
    ax.legend(loc="lower right", fontsize=7)
    date_axis(ax, maxticks=5)

    # (b) pixels measured per device falls with date -> per-device weighting
    ax = axB
    dev = pd.read_csv(os.path.join(DB, "DEVICES_HYST_DEVICE_INFO.csv"))
    dev = dev[dev["device_name"].isin(stdset)].copy()
    dev["date"] = dev["device_name"].map(date)
    dpix = dev.dropna(subset=["number_pixels_measured", "date"])
    xpd = (dpix["date"] - dpix["date"].min()).dt.days.values.astype(float)
    rho_pix, _ = stats.spearmanr(xpd, dpix["number_pixels_measured"].values)
    ax.scatter(dpix["date"], dpix["number_pixels_measured"], s=14, color="0.35",
               edgecolor="white", lw=0.3, alpha=0.8)
    ax.set_ylabel("pixels measured per device")
    ax.set_xlabel("fabrication date")
    figstyle.panel(ax, "b", "why per-device weighting")
    ax.text(0.97, 0.97, f"$\\rho={rho_pix:.2f}$", transform=ax.transAxes,
            ha="right", va="top", fontsize=7.5, color="0.25")
    date_axis(ax, maxticks=4)

    # (c) amplitude x date confound
    ax = axC
    cur_amp = cur.dropna(subset=["date"]).copy()
    cur_amp["mv"] = pd.to_numeric(cur_amp["max voltage (V)"], errors="coerce")
    cur_amp = cur_amp.dropna(subset=["mv"])
    ax.scatter(cur_amp["date"], cur_amp["mv"] + jitter(len(cur_amp), 0.04),
               s=5, color="0.4", alpha=0.25)
    ax.axhspan(1.0, 1.45, color=C_LATE, alpha=0.15, lw=0)
    ax.axhspan(2.6, 3.4, color=C_EARLY, alpha=0.15, lw=0)
    # direct band labels in the empty stratum between the probes
    ax.text(0.985, 2.68, "$\\sim$3 V window probe", transform=ax.get_yaxis_transform(),
            ha="right", va="bottom", fontsize=7.5, color=C_EARLY)
    ax.text(0.985, 1.52, "matched $\\sim$1.2 V conductivity probe",
            transform=ax.get_yaxis_transform(),
            ha="right", va="bottom", fontsize=7.5, color=C_LATE)
    ax.set_ylabel("sweep max voltage (V)")
    ax.set_xlabel("fabrication date")
    figstyle.panel(ax, "c", "amplitude is confounded with date")
    date_axis(ax, maxticks=5)

    fig.canvas.draw()
    for ax in (axA, axB, axC):
        for lab in ax.get_xticklabels():
            lab.set_rotation(30)
            lab.set_ha("right")
    fig.savefig(os.path.join(FIGDIR, "bridge_mechanism.pdf"))
    plt.close(fig)
    print("F2 written:", os.path.join(FIGDIR, "bridge_mechanism.pdf"))

    # ===================== F3 — resolution (Hy vs PEO) =====================
    m = pd.read_csv(os.path.join(DB, "DEVICES_HYST_PIXEL_INFO.csv"))
    m = m.merge(L[["device_name", "Components Group", "Used Metal"]], on="device_name", how="left")
    m3 = m[(pd.to_numeric(m["max voltage (V)"], errors="coerce") >= 2.6)
           & (m["is broken"] != "Y") & (m["is saturated"] != "Y")]

    def host_dev(grp, col):
        v = m3[(m3["Components Group"] == grp) & (m3["Used Metal"] == "Ag")]
        return v.groupby("device_name")[col].median().dropna()

    hy_na = host_dev("SY, Hy, LiTr", "normalized area mean")
    peo_na = host_dev("SY, PEO, LiTr", "normalized area mean")
    hy_oo = host_dev("SY, Hy, LiTr", "on-off ratio mean")
    peo_oo = host_dev("SY, PEO, LiTr", "on-off ratio mean")
    _, p_na = stats.mannwhitneyu(hy_na, peo_na, alternative="two-sided")

    fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.2))
    box_strip(axes[0], [hy_na, peo_na],
              [f"Hybrane\nn={len(hy_na)}", f"PEO\nn={len(peo_na)}"],
              [C_LATE, C_PEO], "normalized area at 3 V", "hysteresis area", letter="a")
    median_labels(axes[0], [hy_na, peo_na], [C_LATE, C_PEO])
    yl = axes[0].get_ylim()
    sig_bracket(axes[0], 1, 2, max(hy_na.max(), peo_na.max()) + 0.04 * (yl[1] - yl[0]),
                f"$p={p_na:.3f}$")
    axes[0].set_xlim(0.45, 2.75)

    box_strip(axes[1], [hy_oo, peo_oo],
              [f"Hybrane\nn={len(hy_oo)}", f"PEO\nn={len(peo_oo)}"],
              [C_LATE, C_PEO], "on–off ratio at 3 V", "switching window", letter="b")
    median_labels(axes[1], [hy_oo, peo_oo], [C_LATE, C_PEO])
    axes[1].set_xlim(0.45, 2.75)

    # (c) PEO on-off vs year, no stock collapse; Hybrane reference line
    cur_o = pd.read_csv(os.path.join(DB, "DEVICES_HYST_CURVE_INFO.csv"), low_memory=False)
    peo_devs = set(L[(L["Components Group"] == "SY, PEO, LiTr") & (L["Used Metal"] == "Ag")]["device_name"])
    c = cur_o[cur_o["device_name"].isin(peo_devs)].copy()
    c["date"] = c["device_name"].map(dict(zip(L["device_name"], L["Date"])))
    mvv = pd.to_numeric(c["max voltage (V)"], errors="coerce")
    c = c[(mvv >= 2.6) & (mvv <= 3.4)].dropna(subset=["on-off ratio"])
    fd = c.groupby("device_name")["day"].transform("min")
    d = c[c["day"] == fd].groupby("device_name").agg(date=("date", "first"),
                                                     oo=("on-off ratio", "median")).dropna()
    d["yr"] = d["date"].dt.year
    years = sorted(d["yr"].unique())
    groups = [d[d["yr"] == y]["oo"] for y in years]
    box_strip(axes[2], groups, [f"{y}\nn={len(g)}" for y, g in zip(years, groups)],
              [C_PEO] * len(years), "on–off ratio at 3 V",
              "PEO temporal reproducibility", letter="c")
    median_labels(axes[2], groups, [C_PEO] * len(years), fmt="{:.1f}", dx=0.30)
    axes[2].axhline(1.35, color=C_LATE, ls="--", lw=1.2)
    axes[2].text(0.03, 1.42, "degraded Hybrane (1.35)",
                 transform=axes[2].get_yaxis_transform(),
                 ha="left", va="bottom", fontsize=7, color=C_LATE)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "bridge_resolution.pdf"))
    plt.close(fig)
    print("F3 written:", os.path.join(FIGDIR, "bridge_resolution.pdf"))

    # ===================== F4 — annealing recovery ========================
    hyA = L[(L["Components Group"] == "SY, Hy, LiTr") & (L["Used Metal"] == "Ag")].copy()
    hyA["hot"] = (hyA["Annealing Temperature [°C]"] >= 150) | (hyA["Second Stage Annealing Temperature [°C]"] >= 150)
    dall = dict(zip(hyA["device_name"], hyA["Date"]))
    ca = cur_o[cur_o["device_name"].isin(set(hyA["device_name"]))].copy()
    ca["date"] = ca["device_name"].map(dall)
    mva = pd.to_numeric(ca["max voltage (V)"], errors="coerce")
    c3a = ca[(mva >= 2.6) & (mva <= 3.4)].dropna(subset=["on-off ratio"])
    fda = c3a.groupby("device_name")["day"].transform("min")
    ooa = c3a[c3a["day"] == fda].groupby("device_name")["on-off ratio"].median()
    late = set(hyA[hyA["Date"] >= INFL]["device_name"])
    hot = set(hyA[hyA["hot"]]["device_name"])
    g_hot = ooa[ooa.index.isin(late & hot)]
    g_std = ooa[ooa.index.isin(late - hot)]
    g_ref = ooa[ooa.index.isin(set(hyA[hyA["Date"] < INFL]["device_name"]) - hot)]
    _, p_rec = stats.mannwhitneyu(g_hot, g_std, alternative="greater")

    fig, ax = plt.subplots(figsize=(4.3, 3.4))
    box_strip(ax, [g_ref, g_std, g_hot],
              [f"early\nstandard 75°C\nn={len(g_ref)}",
               f"late\nstandard 75°C\nn={len(g_std)}",
               f"late\nhot $\\geq$150°C\nn={len(g_hot)}"],
              [C_EARLY, C_LATE, C_HOT], "on–off ratio at 3 V",
              "annealing recovery of the window")
    median_labels(ax, [g_ref, g_std, g_hot], [C_EARLY, C_LATE, C_HOT])
    yl = ax.get_ylim()
    sig_bracket(ax, 2, 3, max(g_std.max(), g_hot.max()) + 0.04 * (yl[1] - yl[0]),
                "$p=0.024$ (one-sided)" if round(p_rec, 3) == 0.024
                else f"$p={p_rec:.3f}$ (one-sided)")
    ax.set_xlim(0.45, 3.75)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "bridge_annealing_recovery.pdf"))
    plt.close(fig)
    print("F4 written:", os.path.join(FIGDIR, "bridge_annealing_recovery.pdf"))


if __name__ == "__main__":
    main()
