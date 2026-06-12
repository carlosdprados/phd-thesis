#!/usr/bin/env python3
"""Chapter 4 --- frequency-domain response of the gold/TMPE devices (figure).

Builds the main-text figure for the lock-in frequency-sweep corpus
(handout 29; scripts lockin_au_tmpe_audit.py + lockin_au_tmpe_findings.py):

  (a) the day-23 transfer-function family |H|(f) of one device at eleven
      DC offsets: a passive ~nF capacitive divider above ~10 Hz that a DC
      bias converts into a low-frequency amplifier (|H| up to ~18);
  (b) the bias-gain curve |H| at 2 Hz against DC offset --- the day-23
      series plus the day-3/4/9/10 population of all three cations.

Run from the repo root:  python3 scripts/ch4_lockin.py
Writes figures/chapter4/lockin_response.pdf.
"""
import math
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle
import lockin_au_tmpe_audit as la

figstyle.apply()
COLORS = figstyle.COLORS
CHEM_C = {"unkLi2": COLORS["blue"], "unkNa2": COLORS["orange"],
          "unkK2": COLORS["green"]}
CHEM_LBL = {"unkLi2": "Li$^+$", "unkNa2": "Na$^+$", "unkK2": "K$^+$"}

OUT = "figures/chapter4"
FIGN = os.path.join(OUT, "lockin_response.pdf")
os.makedirs(OUT, exist_ok=True)

MEASURED = ("200-1Hz", "5k-200Hz", "500k-5kHz")   # not the derived 500k-1Hz


def manifest():
    rows = []
    for fn in sorted(os.listdir(la.RAW)):
        if not fn.endswith(".txt"):
            continue
        meta = la.parse_name(fn)
        if meta:
            meta["fn"] = fn
            rows.append(meta)
    return pd.DataFrame(rows)


def stitched(man, chem, pixel, day, offset, amp):
    """Measured |H|(f) of one condition, piecewise captures concatenated."""
    sel = man[(man.chem == chem) & (man.pixel == pixel) & (man.day == day)
              & (man.offset_v == offset) & (man.amp_v == amp)
              & man.frange.isin(MEASURED)]
    fs, hs = [], []
    for fn in sel.fn:
        d = la.load_txt(os.path.join(la.RAW, fn))
        f = la.col(d, "Oscilator_frequency")
        v4 = la.col(d, "Demod_4", "_R_")
        fs.append(f)
        hs.append(v4 / (amp / math.sqrt(2)))
    if not fs:
        return None, None
    f = np.concatenate(fs)
    h = np.concatenate(hs)
    o = np.argsort(f)
    return f[o], h[o]


def main():
    man = manifest()
    gain = pd.read_csv("handouts/lockin_findings_gain.csv")
    gain = gain[gain.frange == "200-1Hz"].dropna(subset=["H_2"])

    fig, (ax_a, ax_b) = plt.subplots(
        1, 2, figsize=(7.0, 2.85), gridspec_kw={"width_ratios": [1.45, 1.0]})

    # ---- (a) day-23 offset family ----------------------------------------
    offsets = np.arange(-2.5, 2.51, 0.5)
    cmap = plt.cm.RdBu_r
    for off in offsets:
        f, h = stitched(man, "unkLi2", "L3", 23, round(off, 2), 0.25)
        if f is None:
            continue
        if abs(off) < 0.01:
            c, lw, z = COLORS["gray"], 1.4, 5
        else:
            c, lw, z = cmap(0.5 + off / 6.0), 1.0, 3
        ax_a.plot(f, h, color=c, lw=lw, zorder=z)
    ax_a.axhline(1.0, color=COLORS["gray"], lw=0.6, ls=":", zorder=1)
    ax_a.set_xscale("log")
    ax_a.set_yscale("log")
    ax_a.set_xlabel("frequency (Hz)")
    ax_a.set_ylabel(r"$|H| = V_\mathrm{out}/V_\mathrm{in}$ (RMS)")
    ax_a.set_xlim(1, 5e5)
    ax_a.set_ylim(0.15, 30)
    # direct labels instead of a legend
    ax_a.text(1.25, 23, "$+2.5$ V", fontsize=7, color=cmap(0.92))
    ax_a.text(1.25, 8.5, "$-2.5$ V", fontsize=7, color=cmap(0.08))
    ax_a.text(3.6, 0.24, "0 V bias", fontsize=7, color=COLORS["gray"])
    ax_a.text(2.2e3, 0.55, "passive divider\n($C_\\mathrm{dev}$ vs 4 nF)",
              fontsize=6.5, color=COLORS["gray"], ha="left")
    ax_a.annotate("", xy=(60, 8), xytext=(60, 1.3),
                  arrowprops=dict(arrowstyle="->", lw=0.8,
                                  color=COLORS["gray"]))
    ax_a.text(75, 3.0, "bias-activated\ngain, $f\\lesssim10$ Hz",
              fontsize=6.5, color=COLORS["gray"], va="center")
    figstyle.panel(ax_a, "a")

    # ---- (b) bias-gain curve at 2 Hz --------------------------------------
    d23 = gain[(gain.dev == "unkLi2-L3") & (gain.day == 23)].sort_values(
        "offset_v")
    ax_b.plot(d23.offset_v, d23.H_2, "-o", color=COLORS["purple"], lw=1.2,
              ms=3.5, zorder=5, label="Li$^+$ L3, day 23 (0.25 Vpk)")
    pop = gain[~((gain.dev == "unkLi2-L3") & (gain.day == 23))]
    for chem, g in pop.groupby("chem"):
        med = g.groupby("offset_v").H_2.median()
        ax_b.scatter(med.index, med.values, s=14, marker="s",
                     facecolor="none", edgecolor=CHEM_C[chem], lw=1.0,
                     zorder=4, label=f"{CHEM_LBL[chem]} days 3–10 (med.)")
    ax_b.axhline(1.0, color=COLORS["gray"], lw=0.6, ls=":", zorder=1)
    ax_b.set_yscale("log")
    ax_b.set_xlabel("DC offset (V)")
    ax_b.set_ylabel(r"$|H|$ at 2 Hz")
    ax_b.set_xticks([-2, -1, 0, 1, 2])
    ax_b.set_ylim(0.05, 40)
    ax_b.legend(fontsize=6, loc="lower left", frameon=False,
                handletextpad=0.4, borderaxespad=0.2)
    figstyle.panel(ax_b, "b")

    fig.tight_layout(w_pad=2.0)
    figstyle.save(fig, FIGN)


if __name__ == "__main__":
    main()
