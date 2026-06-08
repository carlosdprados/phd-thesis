#!/usr/bin/env python3
"""
Chapter 4 --- ATR-FTIR (IR-ATR) microscopic corroboration.

Reads the raw ATR-FTIR spectra archived under DEVICES_LAB_DATA for the
spectroscopy-only sample set v126--v139 (films / scratched powders of the
SY / polyether / metal-triflate blend, no top electrode), all at the lead
composition cell (ion-polymer mass ratio 0.3, salt 0.09).

Three sub-datasets:
  (A) host x cation matrix  (v126--v131, all triflate, fixed 0.3/0.09)
        PEO : Li v126(film)  Na v127(powder)  K v128(powder)
        TMPE: Li v129(film)  Na v130(film)    K v131(powder)
  (B) PEO vs TMPE Li repeat (v132/v133, powder, 30 min pre-mix)
  (C) humidity series        (v134--v139, PEO/Li film)
        glovebox     : v134 v136 v138
        ambient 2 h  : v135 v137 v139

Each spectrum is a 2-column (wavenumber cm^-1, transmittance-like) table in a
.csv (comma) or .dpt (tab) file; values are ratioed-to-background single-beam
transmittance, so absorption bands are DIPS. We convert to absorbance
A = -log10(T), do a coarse rubber-band baseline, and extract the diagnostic
triflate / polyether / water bands. Raw provenance and band assignments are
written to handouts/ch4_iratr_bands.csv.

No claim rests on a single number here: n = 1 sample per chemistry, mixed
film/powder sampling. The figures are read as an illustrative, microscopic
corroboration of the mechanistic picture, exactly like the EIS section.
"""
from __future__ import annotations
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Locate the experimental archive (sibling of the thesis repo)
# ----------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
LAB = os.path.normpath(os.path.join(
    REPO, "..", "Nanomem_Devices_Library", "DEVICES_LAB_DATA"))
FIGDIR = os.path.join(REPO, "figures", "chapter4")
HANDOUTS = os.path.join(REPO, "handouts")
os.makedirs(FIGDIR, exist_ok=True)

Q3 = os.path.join(LAB, "2022-Q3_Devices")
Q4 = os.path.join(LAB, "2022-Q4_Devices")

# device -> (relative file, host, cation, sampling, group, label)
SAMPLES = {
    # (A) host x cation matrix, all triflate, films/powders
    "v126": (f"{Q3}/2022-09-28_NM_v126_(XRD,IRATR,PEO,LiTr)/Day1_ATR/1.0.csv",
             "PEO", "Li", "film", "matrix"),
    "v127": (f"{Q3}/2022-09-28_NM_v127_(XRD,IRATR,PEO,NaTr)/Day1_ATR/2.0.csv",
             "PEO", "Na", "powder", "matrix"),
    "v128": (f"{Q3}/2022-09-28_NM_v128_(XRD,IRATR,PEO,KTr)/Day1_ATR/3.csv",
             "PEO", "K", "powder", "matrix"),
    "v129": (f"{Q3}/2022-09-28_NM_v129_(XRD,IRATR,TMPE,LiTr)/Day1_ATR/4.0.csv",
             "TMPE", "Li", "film", "matrix"),
    "v130": (f"{Q3}/2022-09-28_NM_v130_(XRD,IRATR,TMPE,NaTr)/Day1_ATR/5.0.csv",
             "TMPE", "Na", "film", "matrix"),
    "v131": (f"{Q3}/2022-09-28_NM_v131_(XRD,IRATR,TMPE,KTr)/Day1_ATR/6.0.csv",
             "TMPE", "K", "powder", "matrix"),
    # (B) PEO vs TMPE Li repeat (powder)
    "v132": (f"{Q4}/2022-10-10_NM_v132_(XRD,IRATR,PEO,LiTr)/Day1_ATR/2022-10-11_1.1.csv",
             "PEO", "Li", "powder", "repeat"),
    "v133": (f"{Q4}/2022-10-10_NM_v133_(XRD,IRATR,TMPE,LiTr)/Day1_ATR/2022-10-11_2.0.csv",
             "TMPE", "Li", "powder", "repeat"),
    # (C) humidity series (PEO/Li film); corrfin = atmospheric+baseline corrected
    "v134": (f"{Q4}/2022-10-20_NM_v134_(IRATR,PEO,LiTr,glvbx)/Day1_ATR/2022-10-21_1.0corrfin.csv",
             "PEO", "Li", "film", "glovebox"),
    "v136": (f"{Q4}/2022-10-20_NM_v136_(IRATR,PEO,LiTr,glvbx)/Day1_ATR/2022-10-21_3.0corrfin.csv",
             "PEO", "Li", "film", "glovebox"),
    "v138": (f"{Q4}/2022-10-20_NM_v138_(IRATR,PEO,LiTr,glvbx)/Day1_ATR/2022-10-21_5.0corrfin.csv",
             "PEO", "Li", "film", "glovebox"),
    "v135": (f"{Q4}/2022-10-20_NM_v135_(IRATR,PEO,LiTr,noglvbx)/Day1_ATR/2022-10-21_2.0corrfin.csv",
             "PEO", "Li", "film", "ambient2h"),
    "v137": (f"{Q4}/2022-10-20_NM_v137_(IRATR,PEO,LiTr,noglvbx)/Day1_ATR/2022-10-21_4.0corrfin.csv",
             "PEO", "Li", "film", "ambient2h"),
    "v139": (f"{Q4}/2022-10-20_NM_v139_(IRATR,PEO,LiTr,noglvbx)/Day1_ATR/2022-10-21_6.0corrfin.csv",
             "PEO", "Li", "film", "ambient2h"),
}

# XRD .xy patterns (2theta, counts) for panel (c) of the combined figure; the
# full XRD analysis lives in scripts/ch4_xrd.py + handouts/17_xrd_assessment.md.
XRD_FILES = {
    "v126": f"{Q3}/2022-09-28_NM_v126_(XRD,IRATR,PEO,LiTr)/Day1_XRD/BB-5-65-1.xy",
    "v129": f"{Q3}/2022-09-28_NM_v129_(XRD,IRATR,TMPE,LiTr)/Day1_XRD/BB-5-65-4.xy",
}
XRD_BLANK = (f"{Q3}/2022-09-28_NM_v126_(XRD,IRATR,PEO,LiTr)/Day1_XRD/"
             "ITO_Test/BB-5-80-3min_ITO.xy")


def load_xy(path):
    """Load a 2-col XRD .xy (2theta, counts), ascending in 2theta."""
    d = np.loadtxt(path)
    x, y = d[:, 0], d[:, 1]
    o = np.argsort(x)
    return x[o], y[o]


# diagnostic band windows (cm^-1) for triflate / polyether / water
BANDS = {
    "dCF3_sym":   (745, 775),    # delta_s(CF3): free~752 / CIP~757 / aggregate~762
    "nsSO3":      (1020, 1060),  # nu_s(SO3): free~1032 / CIP~1042 / aggregate~1052  (key)
    "PEO_COC":    (1080, 1170),  # PEO C-O-C triple peak / crystallinity envelope
    "nsCF3":      (1215, 1245),  # nu_s(CF3)
    "nasSO3":     (1245, 1300),  # nu_as(SO3)
    "H2O_bend":   (1600, 1680),  # H-O-H bend of absorbed water
    "OH_stretch": (3050, 3650),  # O-H stretch of absorbed water
}


def load(path):
    """Load a 2-col spectrum (auto comma/tab), return ascending-wavenumber A,T."""
    with open(path, "r", errors="replace") as fh:
        first = fh.readline()
    delim = "\t" if "\t" in first else ","
    d = np.loadtxt(path, delimiter=delim)
    x, t = d[:, 0], d[:, 1]
    o = np.argsort(x)
    x, t = x[o], t[o]
    # transmittance-like -> absorbance; clip to avoid log of <=0
    tc = np.clip(t, 1e-4, None)
    a = -np.log10(tc)
    return x, a, t


def rubberband(x, y):
    """Coarse convex-hull (rubber-band) baseline for absorbance."""
    # lower convex hull of (x,y)
    pts = np.column_stack([x, y])
    hull = [0]
    for i in range(1, len(pts)):
        while len(hull) >= 2:
            o, a, b = pts[hull[-2]], pts[hull[-1]], pts[i]
            cross = (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
            if cross <= 0:
                hull.pop()
            else:
                break
        hull.append(i)
    bl = np.interp(x, x[hull], y[hull])
    return bl


def band_metrics(x, a, lo, hi):
    """Peak position, peak height (above local baseline), and integrated area."""
    m = (x >= lo) & (x <= hi)
    if m.sum() < 3:
        return np.nan, np.nan, np.nan
    xx, aa = x[m], a[m]
    # local linear baseline between window edges
    base = np.interp(xx, [xx[0], xx[-1]], [aa[0], aa[-1]])
    corr = aa - base
    ipk = np.argmax(corr)
    pos = xx[ipk]
    height = corr[ipk]
    area = np.trapz(np.clip(corr, 0, None), xx)
    return pos, height, area


def main():
    spectra = {}
    rows = []
    for dev, (path, host, cat, samp, grp) in SAMPLES.items():
        if not os.path.exists(path):
            print("MISSING", dev, path)
            continue
        x, a, t = load(path)
        spectra[dev] = (x, a, t, host, cat, samp, grp)
        rec = dict(device="NM_" + dev, host=host, cation=cat, anion="OTf",
                   sampling=samp, group=grp, file=os.path.basename(path))
        for bn, (lo, hi) in BANDS.items():
            pos, h, area = band_metrics(x, a, lo, hi)
            rec[f"{bn}_pos"] = round(pos, 1) if np.isfinite(pos) else ""
            rec[f"{bn}_h"] = round(h, 4) if np.isfinite(h) else ""
            rec[f"{bn}_area"] = round(area, 3) if np.isfinite(area) else ""
        rows.append(rec)

    # ---- write band table ----
    import csv
    cols = list(rows[0].keys())
    out = os.path.join(HANDOUTS, "ch4_iratr_bands.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print("wrote", out)

    # ------------------------------------------------------------------
    # Humidity (glovebox vs ambient) sub-series: HONEST NULL.
    # The corrfin processing is inconsistent and the films differ wildly in
    # ATR contact (see depth of the 1030 band below), so the broad O-H water
    # band cannot be compared between samples. We document the null and do
    # NOT plot it as corroboration.
    # ------------------------------------------------------------------
    print("\n-- humidity sub-series: film contact + water-band depth (RAW .dpt) --")
    hum = {
        "v134": (f"{Q4}/2022-10-20_NM_v134_(IRATR,PEO,LiTr,glvbx)/Day1_ATR/2022-10-21_1.0.dpt", "glovebox"),
        "v136": (f"{Q4}/2022-10-20_NM_v136_(IRATR,PEO,LiTr,glvbx)/Day1_ATR/2022-10-21_3.0.dpt", "glovebox"),
        "v138": (f"{Q4}/2022-10-20_NM_v138_(IRATR,PEO,LiTr,glvbx)/Day1_ATR/2022-10-21_5.0.dpt", "glovebox"),
        "v135": (f"{Q4}/2022-10-20_NM_v135_(IRATR,PEO,LiTr,noglvbx)/Day1_ATR/2022-10-21_2.0.dpt", "ambient2h"),
        "v139": (f"{Q4}/2022-10-20_NM_v139_(IRATR,PEO,LiTr,noglvbx)/Day1_ATR/2022-10-21_6.0.dpt", "ambient2h"),
    }
    for dev, (path, grp) in hum.items():
        if not os.path.exists(path):
            print(f"  NM_{dev} {grp:9s} (no raw .dpt)")
            continue
        x, a, t = load(path)
        depth1030 = 1.0 - float(t[(x >= 1020) & (x <= 1040)].min())   # film signal
        ohdip = 1.0 - float(t[(x >= 3050) & (x <= 3650)].min())        # water dip
        print(f"  NM_{dev} {grp:9s} 1030-band depth={depth1030:.3f}  "
              f"max O-H dip={ohdip:.3f}")
    print("  -> contact (1030 depth) varies 0.0-0.8; O-H dip <=0.05 and not"
          " ordered by glovebox: humidity comparison is INCONCLUSIVE, excluded.")

    make_figures(spectra)


def make_figures(spectra):
    plt.rcParams.update({"font.size": 9, "axes.linewidth": 0.8,
                         "figure.dpi": 150})

    # ===== Figure 1: host x cation fingerprint matrix =====
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.2))
    hosts = ["PEO", "TMPE"]
    cat_color = {"Li": "#1f77b4", "Na": "#2ca02c", "K": "#d62728"}
    matrix = {("PEO", "Li"): "v126", ("PEO", "Na"): "v127", ("PEO", "K"): "v128",
              ("TMPE", "Li"): "v129", ("TMPE", "Na"): "v130", ("TMPE", "K"): "v131"}
    for ax, host in zip(axes, hosts):
        for cat in ["Li", "Na", "K"]:
            dev = matrix[(host, cat)]
            if dev not in spectra:
                continue
            x, a, t, *_ = spectra[dev]
            m = (x >= 700) & (x <= 1350)
            xx, aa = x[m], a[m]
            bl = rubberband(xx, aa)
            aa = aa - bl
            aa = aa / np.nanmax(aa)
            samp = spectra[dev][5]
            ax.plot(xx, aa + 0, color=cat_color[cat], lw=1.0,
                    label=f"{cat} ({samp})")
        for bn in ["dCF3_sym", "nsSO3", "nsCF3", "nasSO3"]:
            lo, hi = BANDS[bn]
            ax.axvspan(lo, hi, color="0.9", zorder=0)
        ax.set_title(f"{host} host, triflate (n=1 / cation)")
        ax.set_xlabel(r"wavenumber (cm$^{-1}$)")
        ax.set_xlim(1350, 700)
        ax.legend(fontsize=7, frameon=False)
    axes[0].set_ylabel("normalised absorbance (offset baseline)")
    fig.suptitle(r"ATR-FTIR fingerprint: triflate \& polyether bands "
                 "(SY blend, 0.3/0.09)", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    p1 = os.path.join(FIGDIR, "iratr_fingerprint.pdf")
    fig.savefig(p1)
    plt.close(fig)
    print("wrote", p1)

    # ===== Figure 2: triflate nu_s(SO3) ion-association band, zoom =====
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    order = [("v126", "PEO/Li"), ("v127", "PEO/Na"), ("v128", "PEO/K"),
             ("v129", "TMPE/Li"), ("v130", "TMPE/Na"), ("v131", "TMPE/K")]
    colors = plt.cm.viridis(np.linspace(0, 0.9, len(order)))
    for (dev, lab), c in zip(order, colors):
        if dev not in spectra:
            continue
        x, a, t, *_ = spectra[dev]
        m = (x >= 1000) & (x <= 1075)
        xx, aa = x[m], a[m]
        base = np.interp(xx, [xx[0], xx[-1]], [aa[0], aa[-1]])
        aa = aa - base
        aa = aa / np.nanmax(aa)
        ax.plot(xx, aa, color=c, lw=1.3, label=lab)
    for ref, txt in [(1032, "free"), (1042, "CIP"), (1052, "aggr.")]:
        ax.axvline(ref, color="0.7", ls=":", lw=0.8)
        ax.text(ref, 1.02, txt, rotation=90, fontsize=6, va="bottom", ha="center",
                color="0.4")
    ax.set_xlim(1075, 1000)
    ax.set_xlabel(r"wavenumber (cm$^{-1}$)")
    ax.set_ylabel(r"normalised $\nu_s$(SO$_3$) absorbance")
    ax.set_title(r"Triflate ion-association band (n=1 / chemistry)")
    ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    p2 = os.path.join(FIGDIR, "iratr_triflate_nsSO3.pdf")
    fig.savefig(p2)
    plt.close(fig)
    print("wrote", p2)

    # ===== Figure 4 (CHAPTER): combined chemistry-axis corroboration =====
    # (a) ATR triflate nu_s(SO3) ion-association, all host x cation -> no
    #     cation-resolved shift ('cation not a clean lever').
    # (b) ATR C-O-C envelope, PEO vs TMPE (Li, film) -> PEO retains LOCAL
    #     conformational order; TMPE amorphous.
    # (c) XRD, PEO/Li vs TMPE/Li vs ITO blank -> films are X-ray AMORPHOUS
    #     (substrate ITO peaks only): no long-range PEO crystallites, no salt
    #     phase. Disciplines (b): local order, not bulk crystallinity.
    fig, (axL, axM, axR) = plt.subplots(1, 3, figsize=(13.2, 4.1))

    order = [("v126", "PEO/Li"), ("v127", "PEO/Na"), ("v128", "PEO/K"),
             ("v129", "TMPE/Li"), ("v130", "TMPE/Na"), ("v131", "TMPE/K")]
    colors = plt.cm.viridis(np.linspace(0, 0.88, len(order)))
    for (dev, lab), c in zip(order, colors):
        if dev not in spectra:
            continue
        x, a, t, *_ = spectra[dev]
        m = (x >= 1005) & (x <= 1060)
        xx, aa = x[m], a[m]
        base = np.interp(xx, [xx[0], xx[-1]], [aa[0], aa[-1]])
        aa = aa - base
        aa = aa / np.nanmax(aa)
        axL.plot(xx, aa, color=c, lw=1.3, label=lab)
    for ref, txt in [(1032, "free"), (1042, "CIP"), (1052, "aggr.")]:
        axL.axvline(ref, color="0.75", ls=":", lw=0.8)
        axL.text(ref, 1.01, txt, rotation=90, fontsize=6, va="bottom",
                 ha="center", color="0.45")
    axL.set_xlim(1060, 1005)
    axL.set_ylim(0, 1.12)
    axL.set_xlabel(r"wavenumber (cm$^{-1}$)")
    axL.set_ylabel(r"normalised $\nu_s$(SO$_3$) absorbance")
    axL.set_title(r"(a) ATR: triflate ion-association band")
    axL.legend(fontsize=6.5, frameon=False, ncol=2)

    for dev, lab, c in [("v126", "PEO/Li (locally ordered)", "#1f77b4"),
                        ("v129", "TMPE/Li (amorphous)", "#d62728")]:
        if dev not in spectra:
            continue
        x, a, t, *_ = spectra[dev]
        m = (x >= 820) & (x <= 1300)
        xx, aa = x[m], a[m]
        aa = aa - rubberband(xx, aa)
        aa = aa / np.nanmax(aa)
        axM.plot(xx, aa, color=c, lw=1.2, label=lab)
    for ref in (843, 947, 962, 1060, 1116, 1145, 1242, 1280):
        axM.axvline(ref, color="0.85", ls=":", lw=0.6, zorder=0)
    axM.set_xlim(1300, 820)
    axM.set_xlabel(r"wavenumber (cm$^{-1}$)")
    axM.set_ylabel("normalised absorbance")
    axM.set_title("(b) ATR: host C-O-C local order (Li, film)")
    axM.legend(fontsize=7, frameon=False)

    # (c) XRD panel
    xrd = {"v126": ("PEO/Li", "#1f77b4"), "v129": ("TMPE/Li", "#d62728")}
    off = 0.0
    for dev, (lab, c) in xrd.items():
        path = XRD_FILES.get(dev)
        if not path or not os.path.exists(path):
            continue
        x, y = load_xy(path)
        norm = np.sum(y[(x >= 29.8) & (x <= 30.8)]) / 100.0
        m = (x >= 10) & (x <= 40)
        axR.plot(x[m], y[m] / norm + off, color=c, lw=0.8, label=lab)
        off += 1.6
    xb, yb = load_xy(XRD_BLANK)
    normb = np.sum(yb[(xb >= 29.8) & (xb <= 30.8)]) / 100.0
    mb = (xb >= 10) & (xb <= 40)
    axR.plot(xb[mb], yb[mb] / normb + off, color="0.35", lw=0.8, label="ITO blank")
    for pk in (21.5, 30.6, 35.5):
        axR.axvline(pk, color="0.6", ls="-", lw=0.5, zorder=0)
    for pk in (19.1, 23.3):
        axR.axvline(pk, color="#1f77b4", ls=":", lw=0.8, zorder=0)
    axR.text(30.6, off + 1.7, "ITO", fontsize=6.5, color="0.4", ha="center")
    axR.text(20.0, off + 1.7, "PEO\n(exp.)", fontsize=6, color="#1f77b4", ha="center")
    axR.set_xlim(10, 40)
    axR.set_yticks([])
    axR.set_xlabel(r"$2\theta$ (deg, Cu-K$\alpha$)")
    axR.set_ylabel("intensity (ITO-norm., offset)")
    axR.set_title("(c) XRD: films are X-ray amorphous")
    axR.legend(fontsize=7, frameon=False, loc="upper left")

    fig.suptitle("Microscopic corroboration of the chemistry axis: ATR + XRD "
                 "(SY blend, 0.3/0.09, n=1 per chemistry)", fontsize=9.5)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    p4 = os.path.join(FIGDIR, "iratr_chemistry.pdf")
    fig.savefig(p4)
    plt.close(fig)
    print("wrote", p4)

    # ===== Figure 3: host structural contrast, PEO vs TMPE (Li, triflate) =====
    # Diagnostic: the C-O-C stretching envelope (1040-1170) is a resolved
    # multiplet in semicrystalline linear PEO and a single broad band in the
    # amorphous hyperbranched TMPE. Shown for both the film pair (v126/v129)
    # and the powder repeat (v132/v133).
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.2), sharey=True)
    panels = [("film pair", {"v126": ("PEO/Li", "#1f77b4"),
                             "v129": ("TMPE/Li", "#d62728")}),
              ("powder repeat", {"v132": ("PEO/Li", "#1f77b4"),
                                 "v133": ("TMPE/Li", "#d62728")})]
    for ax, (title, devs) in zip(axes, panels):
        for dev, (lab, c) in devs.items():
            if dev not in spectra:
                continue
            x, a, t, *_ = spectra[dev]
            m = (x >= 1020) & (x <= 1180)
            xx, aa = x[m], a[m]
            base = np.interp(xx, [xx[0], xx[-1]], [aa[0], aa[-1]])
            aa = aa - base
            aa = aa / np.nanmax(aa)
            ax.plot(xx, aa, color=c, lw=1.4, label=lab)
        for ref in (1060, 1116, 1145):
            ax.axvline(ref, color="0.8", ls=":", lw=0.7)
        ax.set_xlim(1180, 1020)
        ax.set_xlabel(r"wavenumber (cm$^{-1}$)")
        ax.set_title(f"C-O-C envelope, {title}")
        ax.legend(fontsize=8, frameon=False)
    axes[0].set_ylabel("normalised absorbance")
    fig.suptitle("Host structural contrast: PEO (semicrystalline, resolved "
                 "multiplet) vs TMPE (amorphous, single band)", fontsize=9.5)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    p3 = os.path.join(FIGDIR, "iratr_host_crystallinity.pdf")
    fig.savefig(p3)
    plt.close(fig)
    print("wrote", p3)


if __name__ == "__main__":
    main()
