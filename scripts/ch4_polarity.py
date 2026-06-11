#!/usr/bin/env python3
"""Chapter 4 --- polarity and dynamics of the gold/TMPE corpus (figure).

Builds the main-text figure for the negative-polarity findings of the
uncategorized Au/TMPE/(Li,Na,K)OTf corpus (handout 28; scripts
uncat_au_tmpe_audit.py + uncat_au_tmpe_findings.py):

  (a) an exemplar bipolar sweep showing the strong negative/positive
      response asymmetry of the inert-electrode device;
  (b) the sweep-rate gating of the switching window (step-count series);
  (c) the sparse-read relaxation tails after -5 V potentiation -- the first
      fading-memory measurements for the TMPE host on gold.

Run from the repo root:  python3 scripts/ch4_polarity.py
Writes figures/chapter4/polarity_dynamics.pdf.
"""
import csv
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle
import uncat_au_tmpe_audit as ua

figstyle.apply()
COLORS = figstyle.COLORS
SALT_C = {"LiTr": COLORS["blue"], "NaTr": COLORS["orange"], "KTr": COLORS["green"]}
SALT_LBL = {"LiTr": "Li$^+$", "NaTr": "Na$^+$", "KTr": "K$^+$"}

OUT = "figures/chapter4"
FIGN = os.path.join(OUT, "polarity_dynamics.pdf")

DUAL_EXEMPLAR = "2025-02-04-NaTr/L7/Dual/-3V, 3V 200 steps.txt"


def load_inventory():
    rows = list(csv.DictReader(open("handouts/uncat_inventory.csv")))
    for r in rows:
        for k, v in list(r.items()):
            try:
                r[k] = float(v)
            except (TypeError, ValueError):
                pass
    return rows


def panel_a(ax):
    I, V, T = ua.parse_raw(os.path.join(ua.UNCAT, DUAL_EXEMPLAR))
    ax.semilogy(V, np.abs(I) * 1e9, lw=0.5, color=COLORS["gray"], alpha=0.85)
    a_neg = np.median(np.abs(I[np.abs(V + 3) < 0.15]))
    a_pos = np.median(np.abs(I[np.abs(V - 3) < 0.15]))
    ax.annotate("", xy=(2.62, a_neg * 1e9), xytext=(2.62, a_pos * 1e9),
                arrowprops=dict(arrowstyle="<->", lw=0.8, color=COLORS["red"]))
    ax.text(2.45, np.sqrt(a_neg * a_pos) * 1e9, f"$\\times${a_neg/a_pos:.0f}",
            ha="right", va="center", fontsize=7, color=COLORS["red"])
    ax.set_xlabel("V (V)")
    ax.set_ylabel("|I| (nA)")
    figstyle.panel(ax, "a", "polarity asymmetry")


def panel_b(ax, inv):
    import collections
    series = collections.defaultdict(list)
    for r in inv:
        if r.get("cls") != "SWEEP" or r.get("polarity") != "NEG":
            continue
        try:
            key = (r["salt"], r["campaign"], str(r["pixel"]), float(r["amp"]))
            series[key].append((float(r["rate_Vps"]), float(r["onoff_med"])))
        except (TypeError, ValueError, KeyError):
            continue
    for key, pts in sorted(series.items()):
        if len(pts) < 5:
            continue
        pts.sort()
        x = [p[0] for p in pts]
        y = [p[1] for p in pts]
        mk = "o" if key[3] <= 2.0 else "^"
        ax.plot(x, y, mk + "-", ms=3, lw=0.8, color=SALT_C[key[0]],
                alpha=0.75, mew=0)
    ax.set_xscale("log")
    ax.axhline(1, color=COLORS["gray"], lw=0.6, ls=":")
    ax.set_xlabel("sweep rate (V/s)")
    ax.set_ylabel("on/off ratio")
    h = [plt.Line2D([], [], color=SALT_C[s], marker="s", ls="", ms=4,
                    label=SALT_LBL[s]) for s in ("LiTr", "NaTr", "KTr")]
    h += [plt.Line2D([], [], color=COLORS["gray"], marker="o", ls="", ms=3,
                     label="$-2$ V"),
          plt.Line2D([], [], color=COLORS["gray"], marker="^", ls="", ms=3,
                     label="$-3$ V")]
    ax.legend(handles=h, fontsize=5.5, ncol=2, loc="upper right",
              handletextpad=0.2, columnspacing=0.8)
    figstyle.panel(ax, "b", "rate-gated window")


def panel_c(ax):
    rel = list(csv.DictReader(open("handouts/uncat_findings_relax.csv")))
    import collections
    t50s = collections.defaultdict(list)
    for r in rel:
        try:
            drop, vr, t50 = float(r["drop"]), float(r["v_read"]), float(r["t50"])
        except (TypeError, ValueError):
            continue
        if drop <= 0.3 or abs(vr) < 0.1 or not np.isfinite(t50):
            continue
        I, V, T = ua.parse_raw(os.path.join(ua.UNCAT, r["file"]))
        info = ua.classify(I, V, T)
        base = info["v_read"]
        lv = ua.runs(list(np.abs(np.round(V, 2) - base) <= 0.05))
        val, s, ln = lv[-1]
        seg = slice(s + 1, s + ln)
        y = np.abs(I[seg])
        t = T[seg] - T[seg][0]
        ax.semilogx(np.clip(t, 0.04, None), y / y[0], "-", lw=0.7,
                    color=SALT_C[r["salt"]], alpha=0.55)
        t50s[r["salt"]].append(t50)
    for i, s in enumerate(("LiTr", "NaTr", "KTr")):
        v = t50s[s]
        ax.text(0.03, 0.26 - 0.09 * i,
                f"{SALT_LBL[s]}: $t_{{50}}$ {np.median(v):.1f} s (n={len(v)})",
                transform=ax.transAxes, fontsize=6, color=SALT_C[s])
    ax.set_xlabel("time after last pulse (s)")
    ax.set_ylabel("|I$_{read}$| (norm.)")
    figstyle.panel(ax, "c", "fading memory (TMPE/Au)")


def main():
    os.makedirs(OUT, exist_ok=True)
    inv = load_inventory()
    fig, ax = plt.subplots(1, 3, figsize=(7.4, 2.6))
    panel_a(ax[0])
    panel_b(ax[1], inv)
    panel_c(ax[2])
    fig.tight_layout(w_pad=1.4)
    figstyle.save(fig, FIGN)


if __name__ == "__main__":
    main()
