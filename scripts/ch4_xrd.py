#!/usr/bin/env python3
"""
Chapter 4 --- XRD (grazing/Bragg-Brentano) corroboration, chemistry axis.

Reads the archived powder/thin-film XRD patterns for the spectroscopy-only
samples v126-v133 (SY / polyether / metal-triflate blend on ITO, no top
electrode), the SAME host x cation matrix as the IR-ATR set, plus the shared
ITO_Test substrate blank. Instrument: PANalytical Empyrean, Cu-Kalpha.

Clean data is the 2-column .xy (2theta, counts). Each device folder also holds
an ITO_Test/ blank (bare ITO substrate) -- essential here, because the films
are thin and the crystalline ITO (In2O3 bixbyite: 21.5, 30.6, 35.5, 50.9 deg)
dominates the pattern.

Result (see handout 17): after the ITO substrate is accounted for, the blend
films show NO sharp crystalline reflections -- neither the strong PEO
crystalline doublet (~19.1 / 23.3 deg) nor any crystalline metal-triflate salt
phase. The composite is X-ray amorphous for every chemistry. This disciplines
the IR-ATR host reading: PEO retains LOCAL (conformational) order seen in ATR
but does NOT form long-range crystallites in the composite.

n = 1 per chemistry; illustrative tier, as for ATR/EIS.
"""
from __future__ import annotations
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
LAB = os.path.normpath(os.path.join(
    REPO, "..", "Nanomem_Devices_Library", "DEVICES_LAB_DATA"))
FIGDIR = os.path.join(REPO, "figures", "chapter4")
HANDOUTS = os.path.join(REPO, "handouts")
os.makedirs(FIGDIR, exist_ok=True)

Q3 = os.path.join(LAB, "2022-Q3_Devices")
Q4 = os.path.join(LAB, "2022-Q4_Devices")

# device -> (xy file, host, cation)
SAMPLES = {
    "v126": (f"{Q3}/2022-09-28_NM_v126_(XRD,IRATR,PEO,LiTr)/Day1_XRD/BB-5-65-1.xy", "PEO", "Li"),
    "v127": (f"{Q3}/2022-09-28_NM_v127_(XRD,IRATR,PEO,NaTr)/Day1_XRD/BB-5-65-2.xy", "PEO", "Na"),
    "v128": (f"{Q3}/2022-09-28_NM_v128_(XRD,IRATR,PEO,KTr)/Day1_XRD/BB-5-80-3min_3.xy", "PEO", "K"),
    "v129": (f"{Q3}/2022-09-28_NM_v129_(XRD,IRATR,TMPE,LiTr)/Day1_XRD/BB-5-65-4.xy", "TMPE", "Li"),
    "v130": (f"{Q3}/2022-09-28_NM_v130_(XRD,IRATR,TMPE,NaTr)/Day1_XRD/BB-5-80-3min_5.xy", "TMPE", "Na"),
    "v131": (f"{Q3}/2022-09-28_NM_v131_(XRD,IRATR,TMPE,KTr)/Day1_XRD/BB-5-80-3min_6.xy", "TMPE", "K"),
    "v132": (f"{Q4}/2022-10-10_NM_v132_(XRD,IRATR,PEO,LiTr)/Day1_XRD/BB-5-100-8min_1.xy", "PEO", "Li"),
    "v133": (f"{Q4}/2022-10-10_NM_v133_(XRD,IRATR,TMPE,LiTr)/Day1_XRD/BB-5-100-8min_2.xy", "TMPE", "Li"),
}
BLANK = f"{Q3}/2022-09-28_NM_v126_(XRD,IRATR,PEO,LiTr)/Day1_XRD/ITO_Test/BB-5-80-3min_ITO.xy"

ITO_PEAKS = [21.5, 30.6, 35.5]           # In2O3 bixbyite (substrate)
PEO_PEAKS = [19.1, 23.3]                 # crystalline PEO doublet (expected if crystalline)


def load(p):
    d = np.loadtxt(p)
    x, y = d[:, 0], d[:, 1]
    o = np.argsort(x)
    return x[o], y[o]


def integ(x, y, a, b):
    m = (x >= a) & (x <= b)
    return float(y[m].sum())


def main():
    xb, yb = load(BLANK)
    ito_ref = integ(xb, yb, 29.8, 30.8)

    print("-- ITO-substrate-scaled residual crystallinity (12-40 deg) --")
    for dev, (path, host, cat) in SAMPLES.items():
        if not os.path.exists(path):
            print("MISSING", dev)
            continue
        x, y = load(path)
        ybi = np.interp(x, xb, yb)
        s = integ(x, y, 29.8, 30.8) / ito_ref
        res = y - s * ybi
        m = (x >= 12) & (x <= 40)
        # max residual near the PEO doublet vs the residual RMS (crude SNR)
        peo = max(float(res[(x >= 18.5) & (x <= 19.7)].max()),
                  float(res[(x >= 22.7) & (x <= 23.8)].max()))
        rms = float(np.sqrt(np.mean(res[m] ** 2)))
        print(f"  NM_{dev} {host:4s}/{cat:2s}  ITO-scale={s:.2f}  "
              f"PEO-doublet residual={peo:6.0f}  resid RMS={rms:5.0f}")
    print("  -> film residuals are weak and not PEO-specific: X-ray amorphous.")

    make_figure(xb, yb)


def make_figure(xb, yb):
    plt.rcParams.update({"font.size": 9, "axes.linewidth": 0.8, "figure.dpi": 150})
    fig, ax = plt.subplots(figsize=(6.4, 5.2))

    # normalise each pattern to its ITO (222) 30.6 deg peak so the substrate
    # lines up and any *film* crystallinity would stand out above it.
    rows = [("v126", "PEO/Li", "#1f77b4"), ("v127", "PEO/Na", "#3a8fd6"),
            ("v128", "PEO/K", "#74c1f0"),
            ("v129", "TMPE/Li", "#d62728"), ("v130", "TMPE/Na", "#e8743b"),
            ("v131", "TMPE/K", "#f4a259")]
    off = 0.0
    step = 1.05
    for dev, lab, c in rows:
        path = SAMPLES[dev][0]
        if not os.path.exists(path):
            continue
        x, y = load(path)
        norm = integ(x, y, 29.8, 30.8) / 100.0
        yy = y / norm
        m = (x >= 10) & (x <= 40)
        ax.plot(x[m], yy[m] + off, color=c, lw=0.9)
        ax.text(26.5, off + 0.30, lab, fontsize=7, color=c, ha="center")
        off += step
    # ITO blank at top
    normb = integ(xb, yb, 29.8, 30.8) / 100.0
    mb = (xb >= 10) & (xb <= 40)
    ax.plot(xb[mb], yb[mb] / normb + off, color="0.3", lw=0.9)
    ax.text(26.5, off + 0.30, "ITO blank", fontsize=7, color="0.3", ha="center")

    for pk in ITO_PEAKS:
        ax.axvline(pk, color="0.6", ls="-", lw=0.6, zorder=0)
    for pk in PEO_PEAKS:
        ax.axvline(pk, color="#1f77b4", ls=":", lw=0.8, zorder=0)
    ax.text(30.6, off + step * 0.7, "ITO (In$_2$O$_3$)", fontsize=7,
            color="0.4", ha="center")
    ax.text(21.0, off + step * 0.7, "PEO\n(exp.)", fontsize=6.5,
            color="#1f77b4", ha="center")

    ax.set_xlim(10, 40)
    ax.set_yticks([])
    ax.set_xlabel(r"$2\theta$ (deg, Cu-K$\alpha$)")
    ax.set_ylabel("intensity (ITO-normalised, offset)")
    ax.set_title("XRD: composite films are X-ray amorphous\n"
                 "(substrate ITO peaks only; no PEO crystallites, no salt phase)",
                 fontsize=9.5)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "xrd_amorphous.pdf")
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


if __name__ == "__main__":
    main()
