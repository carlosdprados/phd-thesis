#!/usr/bin/env python3
"""Chapter 4 figures (in-silico, no external data):
  fig:ch4_mc_curve        -> mc_curve.pdf        (MC(k): heterogeneous broadens memory)
  fig:ch4_composition_sweep -> composition_sweep.pdf (total MC + NARMA per composition)

Run from the repo root:  python3 scripts/ch4_figures.py
Depends on scripts/ch4_reservoir.py + scripts/ch4_model.py.
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ch4_reservoir import (load_cards, make_nodes, run_states, memory_capacity,
                           nodes_from, _full, narma10, task_nrmse, DT)  # noqa: E402

FIGDIR = "figures/chapter4"
plt.rcParams.update({"font.family": "serif", "font.size": 9, "figure.dpi": 150,
                     "savefig.bbox": "tight"})


def fig_mc_curve(cards, N=24, max_k=30):
    u = np.random.default_rng(0).uniform(0, 1, 4000)
    out = {}
    for label, het in [("homogeneous (all PEO0.3/0.09)", False),
                       ("heterogeneous (composition bank)", True)]:
        nodes = make_nodes(cards, N, het, np.random.default_rng(1))
        out[label] = memory_capacity(run_states(nodes, u), u, max_k=max_k)
    k = np.arange(1, max_k + 1)
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    ax.plot(k, out["homogeneous (all PEO0.3/0.09)"], "o-", ms=3, color="#4c72b0",
            label=f"homogeneous (MC={out['homogeneous (all PEO0.3/0.09)'].sum():.1f})")
    ax.plot(k, out["heterogeneous (composition bank)"], "s-", ms=3, color="#c44e52",
            label=f"heterogeneous (MC={out['heterogeneous (composition bank)'].sum():.1f})")
    ax.set_xlabel(f"delay $k$ (lags of $\\Delta t={DT:g}$ s)")
    ax.set_ylabel("memory capacity MC$_k$")
    ax.set_title(f"Memory capacity vs lag (N={N} nodes)")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "mc_curve.pdf"); fig.savefig(p); plt.close(fig)
    print("wrote", p)


def fig_composition_sweep(cards, N=16, max_k=30):
    rng = np.random.default_rng(0)
    u_mc = rng.uniform(0, 1, 4000); u_na = rng.uniform(0, 0.5, 4000); y_na = narma10(u_na)
    rows = []
    for c in sorted(_full(cards), key=lambda z: (float(z.peo), float(z.salt))):
        nodes = nodes_from([c], N, np.random.default_rng(7))
        mc = memory_capacity(run_states(nodes, u_mc), u_mc, max_k=max_k).sum()
        nrmse = task_nrmse(run_states(nodes, u_na), y_na)
        rows.append((f"{c.peo}/{c.salt}", mc, nrmse,
                     c.peo == "0.3" and c.salt == "0.09"))
    labels = [r[0] for r in rows]; mcs = [r[1] for r in rows]; nrs = [r[2] for r in rows]
    x = np.arange(len(rows))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0))
    cols = ["#dd8452" if r[3] else "#4c72b0" for r in rows]
    a1.bar(x, mcs, color=cols, edgecolor="0.2", linewidth=0.5)
    a1.set_xticks(x); a1.set_xticklabels(labels, rotation=45, ha="right", fontsize=7)
    a1.set_ylabel("total memory capacity"); a1.set_title("(a) MC by composition")
    a2.bar(x, nrs, color=cols, edgecolor="0.2", linewidth=0.5)
    a2.set_xticks(x); a2.set_xticklabels(labels, rotation=45, ha="right", fontsize=7)
    a2.set_ylabel("NARMA-10 NRMSE (lower better)"); a2.set_title("(b) NARMA-10 by composition")
    fig.text(0.5, -0.04, "PEO / salt mass fraction (orange = lead cell 0.3/0.09)",
             ha="center", fontsize=8)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "composition_sweep.pdf"); fig.savefig(p); plt.close(fig)
    print("wrote", p)


def main():
    os.makedirs(FIGDIR, exist_ok=True)
    cards = load_cards(li_only=True)
    fig_mc_curve(cards)
    fig_composition_sweep(cards)


if __name__ == "__main__":
    main()
