#!/usr/bin/env python3
"""bridge_figures.py — render the bridge-chapter figures (F1-F4).

Reuses the loaders and corpus definition of
scripts/bridge_hybrane_peo_reproducibility.py so that the figures plot exactly
the same per-device, standard-protocol, amplitude-matched quantities that the
audit script tests (and only the numbers it prints).

Run from the repo root:  python scripts/bridge_figures.py
Writes PDFs into figures/chapter3/:
  F1  bridge_window_collapse.pdf   on-off & normalized area @3V, early vs later
  F2  bridge_mechanism.pdf         ohmic drift @1.2V vs date (+ methodology insets)
  F3  bridge_resolution.pdf        Hy vs PEO @3V, and PEO on-off vs year 2022-24
  F4  bridge_annealing_recovery.pdf  late-device window restored by hot anneal
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from bridge_hybrane_peo_reproducibility import load, hybrane_standard, DB, TAIL

FIGDIR = "figures/chapter3"
INFL = pd.Timestamp("2021-05-01")  # post-NM_v026 inflection (2021-04-22)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
})

C_EARLY = "#2c7fb8"   # early / pristine
C_LATE = "#d95f0e"    # later / degraded
C_PEO = "#31a354"     # PEO host
C_HOT = "#756bb1"     # elevated-T anneal


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


def box_strip(ax, groups, labels, colors, ylabel, title, log=False):
    data = [g.values for g in groups]
    bp = ax.boxplot(data, widths=0.5, showfliers=False, patch_artist=True,
                    medianprops=dict(color="black", lw=1.4))
    for patch, c in zip(bp["boxes"], colors):
        patch.set_facecolor(c)
        patch.set_alpha(0.30)
    for i, (g, c) in enumerate(zip(groups, colors), start=1):
        x = np.full(len(g), i) + jitter(len(g))
        ax.scatter(x, g.values, s=16, color=c, edgecolor="black", lw=0.3, alpha=0.85, zorder=3)
    ax.set_xticks(range(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if log:
        ax.set_yscale("log")


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
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.4))
    for ax, col, ylab, ttl in [
        (axes[0], "on-off ratio", "on-off ratio @3 V", "(a) switching window"),
        (axes[1], "normalized area", "normalized area @3 V", "(b) normalized hysteresis area"),
    ]:
        pdv = per_device(cur3, col, date)
        e = pdv[pdv["date"] < INFL]["y"]
        l = pdv[pdv["date"] >= INFL]["y"]
        _, p = stats.mannwhitneyu(e, l, alternative="two-sided")
        box_strip(ax, [e, l],
                  [f"early\n($\\leq$Apr 2021)\nn={len(e)}", f"later\nn={len(l)}"],
                  [C_EARLY, C_LATE], ylab, ttl)
        ymax = max(e.max(), l.max())
        ax.annotate(f"Mann–Whitney $p={p:.4f}$\nmedian {e.median():.2f} $\\to$ {l.median():.2f}"
                    if col == "on-off ratio" else
                    f"Mann–Whitney $p={p:.4f}$\nmedian {e.median():.3f} $\\to$ {l.median():.3f}",
                    xy=(0.5, 0.97), xycoords="axes fraction", ha="center", va="top",
                    fontsize=8, bbox=dict(boxstyle="round", fc="white", ec="0.6", alpha=0.9))
    fig.suptitle("Switching-window collapse across the campaign "
                 "(standard SY/Hy/LiTr/Ag corpus, per device)", fontsize=9)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(FIGDIR, "bridge_window_collapse.pdf"))
    plt.close(fig)
    print("F1 written:", os.path.join(FIGDIR, "bridge_window_collapse.pdf"))

    # ===================== F2 — mechanism + methodology ====================
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.6))

    # (a) ohmic drift at matched ~1.2 V, log y, recovery tail marked
    ax = axes[0]
    pdv = per_device(cur12, "area (V*uA)", date)
    pdv = pdv[pdv["y"] > 0]
    x = pdv["date"]
    tail = pdv["date"] >= TAIL
    ax.scatter(x[~tail], pdv["y"][~tail], s=20, color=C_LATE, edgecolor="black",
               lw=0.3, alpha=0.85, label="standard corpus")
    ax.scatter(x[tail], pdv["y"][tail], s=30, marker="D", facecolor="none",
               edgecolor=C_HOT, lw=1.1, label="recovery tail ($\\geq$2022-03)")
    ax.set_yscale("log")
    ax.set_ylabel("hysteresis area @1.2 V  (V$\\cdot\\mu$A)")
    ax.set_xlabel("fabrication date")
    ax.set_title("(a) ohmic drift at matched $\\sim$1.2 V")
    xd = (pdv["date"] - pdv["date"].min()).dt.days.values.astype(float)
    rho_all, p_all = stats.spearmanr(xd, pdv["y"].values)
    m = ~tail.values
    rho_dt, p_dt = stats.spearmanr(xd[m], pdv["y"].values[m])
    ax.annotate(f"Spearman vs date\n$\\rho={rho_all:+.2f}$ (all)\n"
                f"$\\rho={rho_dt:+.2f}$ (drop tail)",
                xy=(0.03, 0.97), xycoords="axes fraction", ha="left", va="top",
                fontsize=8, bbox=dict(boxstyle="round", fc="white", ec="0.6", alpha=0.9))
    ax.legend(loc="lower right", fontsize=7, framealpha=0.9)
    for lab in ax.get_xticklabels():
        lab.set_rotation(30)
        lab.set_ha("right")

    # inset: pixels-measured vs date (why per-device weighting)
    dev = pd.read_csv(os.path.join(DB, "DEVICES_HYST_DEVICE_INFO.csv"))
    dev = dev[dev["device_name"].isin(stdset)].copy()
    dev["date"] = dev["device_name"].map(date)
    dpix = dev.dropna(subset=["number_pixels_measured", "date"])
    xpd = (dpix["date"] - dpix["date"].min()).dt.days.values.astype(float)
    rho_pix, _ = stats.spearmanr(xpd, dpix["number_pixels_measured"].values)
    axin = ax.inset_axes([0.50, 0.58, 0.46, 0.38])
    axin.scatter(dpix["date"], dpix["number_pixels_measured"], s=8, color="0.35", alpha=0.7)
    axin.set_title(f"pixels/device  $\\rho={rho_pix:.2f}$", fontsize=7)
    axin.tick_params(labelsize=6)
    axin.set_xticks([dpix["date"].min(), dpix["date"].max()])
    axin.set_xticklabels([str(dpix["date"].min().date()), str(dpix["date"].max().date())],
                         fontsize=6, rotation=20, ha="right")

    # (b) amplitude x date confound
    ax = axes[1]
    cur_amp = cur.dropna(subset=["date"]).copy()
    cur_amp["mv"] = pd.to_numeric(cur_amp["max voltage (V)"], errors="coerce")
    cur_amp = cur_amp.dropna(subset=["mv"])
    ax.scatter(cur_amp["date"], cur_amp["mv"] + jitter(len(cur_amp), 0.04),
               s=5, color="0.4", alpha=0.25)
    ax.axhspan(1.0, 1.45, color=C_LATE, alpha=0.18, label="matched $\\sim$1.2 V probe")
    ax.axhspan(2.6, 3.4, color=C_EARLY, alpha=0.18, label="$\\sim$3 V window probe")
    ax.set_ylabel("sweep max voltage (V)")
    ax.set_xlabel("fabrication date")
    ax.set_title("(b) sweep amplitude is confounded with date")
    ax.legend(loc="upper right", fontsize=7, framealpha=0.9)
    for lab in ax.get_xticklabels():
        lab.set_rotation(30)
        lab.set_ha("right")

    fig.suptitle("Mechanism (ohmic drift) and the methodology that isolates it", fontsize=9)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
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

    fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.4))
    box_strip(axes[0], [hy_na, peo_na],
              [f"Hybrane\nn={len(hy_na)}", f"PEO\nn={len(peo_na)}"],
              [C_LATE, C_PEO], "normalized area @3 V", "(a) hysteresis area")
    axes[0].annotate(f"Mann–Whitney $p={p_na:.3f}$\n{hy_na.median():.2f} $\\to$ {peo_na.median():.2f}",
                     xy=(0.5, 0.97), xycoords="axes fraction", ha="center", va="top",
                     fontsize=8, bbox=dict(boxstyle="round", fc="white", ec="0.6", alpha=0.9))
    box_strip(axes[1], [hy_oo, peo_oo],
              [f"Hybrane\nn={len(hy_oo)}", f"PEO\nn={len(peo_oo)}"],
              [C_LATE, C_PEO], "on-off ratio @3 V", "(b) switching window")
    axes[1].annotate(f"median {hy_oo.median():.2f} $\\to$ {peo_oo.median():.2f}",
                     xy=(0.5, 0.97), xycoords="axes fraction", ha="center", va="top",
                     fontsize=8, bbox=dict(boxstyle="round", fc="white", ec="0.6", alpha=0.9))

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
              [C_PEO] * len(years), "on-off ratio @3 V", "(c) PEO temporal reproducibility")
    axes[2].axhline(1.35, color=C_LATE, ls="--", lw=1.2)
    axes[2].annotate("degraded Hybrane (1.35)", xy=(0.5, 1.35), xycoords=("axes fraction", "data"),
                     fontsize=7, color=C_LATE, ha="center", va="bottom")
    fig.suptitle("Resolution: PEO restores and sustains the switching window", fontsize=9)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
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

    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    box_strip(ax, [g_ref, g_std, g_hot],
              [f"early\nstandard 75°C\nn={len(g_ref)}",
               f"late\nstandard 75°C\nn={len(g_std)}",
               f"late\nhot $\\geq$150°C\nn={len(g_hot)}"],
              [C_EARLY, C_LATE, C_HOT], "on-off ratio @3 V",
              "Annealing recovery of the window")
    ax.annotate(f"hot > std (late): Mann–Whitney $p={p_rec:.3f}$\n"
                f"median {g_std.median():.2f} $\\to$ {g_hot.median():.2f} (early ref {g_ref.median():.2f})",
                xy=(0.5, 0.97), xycoords="axes fraction", ha="center", va="top",
                fontsize=7.5, bbox=dict(boxstyle="round", fc="white", ec="0.6", alpha=0.9))
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "bridge_annealing_recovery.pdf"))
    plt.close(fig)
    print("F4 written:", os.path.join(FIGDIR, "bridge_annealing_recovery.pdf"))


if __name__ == "__main__":
    main()
