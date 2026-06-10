#!/usr/bin/env python3
"""
Chapter 4 --- UV-Vis corroboration: the SY electronic structure is invariant
to the electrolyte cation.

Reads the archived UV-Vis absorbance spectra (JASCO) for the 2025 TMPE-host
blend films v317-v320 (SY / TMPE / metal-triflate, lead cell 0.3/0.09, Au
generation, 'newmixing'): a Li/Na/K cation series plus a salt-free control.

  v317 SY/TMPE/LiTr   v318 SY/TMPE/NaTr   v319 SY/TMPE/KTr   v320 SY/TMPE (no salt)

Files: '<ion>_View*.csv'      = raw absorbance vs nm   (X nm, Y absorbance)
       '<ion>_conv*View*.csv' = converted Kubelka-Munk vs energy [eV] (Tauc form)
CSV is JASCO export: ';'-delimited, comma decimal, header then 'XYDATA'.

Result: the SY pi-pi* absorption peaks at ~446 nm with a ~2.50 eV onset in
EVERY cation (Li/Na/K identical; salt-free ~the same), so the cation does not
perturb the semiconductor's optical/electronic structure -- the chemistry acts
on ion transport, not on the SY electronic backbone. n=1 per chemistry;
absorbance magnitudes are thickness-confounded (only peak/onset POSITIONS are
read); deep-UV (<280 nm) is unreliable (baseline). Illustrative tier.
"""
from __future__ import annotations
import os
import glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import figstyle
figstyle.apply()
COLORS = figstyle.COLORS

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
LAB = os.path.normpath(os.path.join(
    REPO, "..", "Nanomem_Devices_Library", "DEVICES_LAB_DATA"))
FIGDIR = os.path.join(REPO, "figures", "chapter4")
HANDOUTS = os.path.join(REPO, "handouts")
os.makedirs(FIGDIR, exist_ok=True)

Q1 = os.path.join(LAB, "2025-Q1_Devices")
BASE = {
    "Li":     (f"{Q1}/2025-02-26_NM_v317_(TMPELiTr,Au,3000rpm,90deg,newmixing,UV-Vis)/Day1_UV-Vis/", COLORS["blue"]),
    "Na":     (f"{Q1}/2025-02-26_NM_v318_(TMPENaTr,Au,3000rpm,90deg,newmixing,UV-Vis)/Day1_UV-Vis/", COLORS["green"]),
    "K":      (f"{Q1}/2025-02-26_NM_v319_(TMPEKTr,Au,3000rpm,90deg,newmixing,UV-Vis)/Day1_UV-Vis/", COLORS["red"]),
    "no salt": (f"{Q1}/2025-02-26_NM_v320_(TMPE,Au,3000rpm,90deg,newmixing,UV-Vis)/Day1_UV-Vis/", "0.45"),
}


def load(p):
    rows, started = [], False
    for line in open(p, encoding="utf-8", errors="replace"):
        if started:
            q = line.strip().split(";")
            if len(q) >= 2:
                try:
                    rows.append((float(q[0].replace(",", ".")),
                                 float(q[1].replace(",", "."))))
                except ValueError:
                    pass
        if line.startswith("XYDATA"):
            started = True
    a = np.array(rows)
    o = np.argsort(a[:, 0])
    return a[o, 0], a[o, 1]


def raw_file(b):
    g = [f for f in glob.glob(b + "*View*.csv") if "conv" not in os.path.basename(f)]
    return g[0] if g else None


def main():
    spectra = {}
    print("-- SY absorption peak / onset (raw absorbance) --")
    for ion, (b, c) in BASE.items():
        rf = raw_file(b)
        if not rf or not os.path.exists(rf):
            print("  missing", ion)
            continue
        x, y = load(rf)
        spectra[ion] = (x, y, c)
        m = (x > 400) & (x < 540)
        xp = x[m][np.argmax(y[m])]
        pk = y[m].max()
        mm = (x > 420) & (x < 660)
        idx = np.where(y[mm] >= 0.5 * pk)[0]
        onset = x[mm][idx].max() if len(idx) else np.nan
        print(f"  {ion:7s} peak={xp:.0f} nm  A_peak={pk:.2f}  "
              f"onset(50%)={onset:.0f} nm = {1239.8/onset:.2f} eV")

    fig, ax = plt.subplots(figsize=(4.8, 3.6))
    for ion in ["Li", "Na", "K", "no salt"]:
        if ion not in spectra:
            continue
        x, y, c = spectra[ion]
        m = (x >= 300) & (x <= 650)
        xx, yy = x[m], y[m]
        # normalise to the SY peak so only the band shape/edge is compared
        pk = yy[(xx > 400) & (xx < 540)].max()
        ls = "--" if ion == "no salt" else "-"
        ax.plot(xx, yy / pk, color=c, lw=1.4, ls=ls)
    ax.axvline(496, color="0.7", ls=":", lw=0.8)
    ax.text(502, 0.93, "onset\n$\\approx$2.50 eV", fontsize=7, color="0.4", ha="left")
    # direct labels: the three cation curves are superimposed (that is the
    # result), so they are labelled once as a group
    ax.text(0.03, 0.99, "SY/TMPE/{Li, Na, K}\n(superimposed)",
            transform=ax.transAxes, fontsize=7.5, color=COLORS["blue"], va="top")
    ax.text(0.03, 0.81, "SY/TMPE, no salt\n(dashed)",
            transform=ax.transAxes, fontsize=7.5, color="0.45", va="top")
    ax.set_xlim(320, 620)
    ax.set_xlabel("wavelength (nm)")
    ax.set_ylabel("normalised absorbance (SY peak = 1)")
    secx = ax.secondary_xaxis("top", functions=(lambda w: 1239.8 / np.clip(w, 1, None),
                                                lambda e: 1239.8 / np.clip(e, 1e-6, None)))
    secx.set_xlabel("energy (eV)", fontsize=8)
    secx.spines["top"].set_visible(True)   # keep the secondary energy axis line
    fig.tight_layout()
    p = os.path.join(FIGDIR, "uvvis_bandedge.pdf")
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


if __name__ == "__main__":
    main()
