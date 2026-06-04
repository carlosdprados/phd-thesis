#!/usr/bin/env python3
"""Chapter 4 figures:
  fig:ch4_mc_curve          -> mc_curve.pdf          (MC(k): heterogeneous broadens memory)
  fig:ch4_composition_sweep -> composition_sweep.pdf (total MC + NARMA per composition)
  fig:ch4_wesad             -> wesad_affect.pdf       (WESAD: Demo A window task +
                                streaming Demo B decomposition; needs the dataset)

Run from the repo root:  python3 scripts/ch4_figures.py
Depends on scripts/ch4_reservoir.py + scripts/ch4_model.py (+ ch4_wesad.py & the
WESAD dataset for the last figure, which is skipped if the data is absent).
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


def fig_wesad(cards, seeds=range(5)):
    """WESAD affective computing (needs the dataset). Two honest panels:
    (a) Demo A window-level binary stress/baseline: reservoir vs static baseline
        -> the single-timescale window task is quasi-static (RC ~= static).
    (b) Demo B streaming 3-class decomposition: instantaneous -> +dimensionality
        -> +memory -> +heterogeneity, with seed error bars -> memory helps; the
        timescale-heterogeneity increment is within noise on this affect task."""
    import ch4_wesad as W
    if not (os.path.isdir(W.WESAD_DIR) and
            __import__("glob").glob(os.path.join(W.WESAD_DIR, "S*", "S*.pkl"))):
        print("skip wesad_affect.pdf (WESAD dataset not present)")
        return
    raw = W.load_raw()
    C = len(W.CHANNELS); dt = W.DT_WES; sm = int(W.SMOOTH_S / dt)
    eda = W.CHANNELS.index("EDA")

    # (a) Demo A: reservoir vs static, binary, EDA windows
    subs = {sid: W.windows_from(U, lab) for sid, (U, lab) in raw.items()}
    lead = nodes_from([__import__("ch4_model").lead_card(cards)], W.N_NODES,
                      np.random.default_rng(7), dt=dt, n_in=1)
    Fr, yr, gr = W.window_features(lead, subs, cols=[eda], labels=(1, 2), dt=dt)
    f1A_res = W.loso_window(Fr, yr, gr, [1, 2])[0]
    Fs, ys, gs = [], [], []
    for sid, wins in subs.items():
        for seg, lab in wins:
            if lab not in (1, 2):
                continue
            x = seg[:, eda]; t = np.linspace(0, 1, len(x))
            Fs.append([x.mean(), x.std(), x[-1], np.polyfit(t, x, 1)[0]])
            ys.append(lab); gs.append(sid)
    f1A_stat = W.loso_window(np.array(Fs), np.array(ys), np.array(gs), [1, 2])[0]

    # (b) Demo B streaming decomposition
    from ch4_model import lead_card
    f1_inst = W.loso_stream(W.instant_features(raw, dt), [1, 2, 3], smooth=sm)[0]
    mem0, hom, het = [], [], []
    for s in seeds:
        h = nodes_from(_full(cards), W.N_NODES, np.random.default_rng(s),
                       dt=dt, n_in=C, sparsity=0.4)
        m = nodes_from([lead_card(cards)], W.N_NODES, np.random.default_rng(s),
                       dt=dt, n_in=C, sparsity=0.4)
        z = [(0.0, a, w) for (_, a, w) in h]                       # memoryless control
        het.append(W.loso_stream(W.stream_features(h, raw, dt), [1, 2, 3], smooth=sm)[0])
        hom.append(W.loso_stream(W.stream_features(m, raw, dt), [1, 2, 3], smooth=sm)[0])
        mem0.append(W.loso_stream(W.stream_features(z, raw, dt), [1, 2, 3], smooth=sm)[0])
    het, hom, mem0 = map(np.array, (het, hom, mem0))

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.2),
                                 gridspec_kw={"width_ratios": [1, 1.7]})
    # panel (a)
    a1.bar([0, 1], [f1A_res, f1A_stat], color=["#dd8452", "#b0b0b0"],
           edgecolor="0.2", linewidth=0.5, width=0.6)
    a1.set_xticks([0, 1]); a1.set_xticklabels(["device\nreservoir", "static\nbaseline"])
    a1.set_ylim(0, 1); a1.set_ylabel("LOSO macro-F1")
    a1.set_title("(a) Demo A: window binary\nstress/baseline (EDA)", fontsize=8.5)
    a1.axhline(0.5, ls=":", c="0.5", lw=0.8); a1.text(1.5, 0.52, "chance", fontsize=6.5,
                                                      ha="right", color="0.5")
    for x, v in zip([0, 1], [f1A_res, f1A_stat]):
        a1.text(x, v + 0.02, f"{v:.2f}", ha="center", fontsize=7.5)
    # panel (b)
    labels = ["instantaneous\n(no memory)", "memoryless\nbank (dim.)",
              "homogeneous\n(memory, 1$\\tau$)", "heterogeneous\n(memory, $\\tau$ spread)"]
    vals = [f1_inst, mem0.mean(), hom.mean(), het.mean()]
    errs = [0, mem0.std(), hom.std(), het.std()]
    cols = ["#b0b0b0", "#8c8c8c", "#4c72b0", "#c44e52"]
    x = np.arange(4)
    a2.bar(x, vals, yerr=errs, color=cols, edgecolor="0.2", linewidth=0.5,
           width=0.62, capsize=3, error_kw={"lw": 0.8})
    a2.set_xticks(x); a2.set_xticklabels(labels, fontsize=7.2)
    a2.set_ylim(0.6, 0.81); a2.set_ylabel("LOSO macro-F1")
    a2.set_title("(b) Demo B: streaming 3-class affect tracking", fontsize=8.5)
    # cumulative decomposition: inst -> +dim -> +memory -> +heterogeneity
    def _step(x0, x1, y, txt):
        a2.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="->", lw=0.8, color="0.25"))
        a2.text((x0 + x1) / 2, y + 0.005, txt, ha="center", fontsize=6.6, color="0.25")
    _step(0, 1, 0.752, f"+dim {mem0.mean()-f1_inst:+.3f}")
    _step(1, 2, 0.770, f"+memory {hom.mean()-mem0.mean():+.3f}")
    _step(2, 3, 0.788, f"+heterog {het.mean()-hom.mean():+.3f} (ns)")
    for xi, v in zip(x, vals):
        a2.text(xi, 0.61, f"{v:.3f}", ha="center", fontsize=7, color="white")
    fig.tight_layout()
    p = os.path.join(FIGDIR, "wesad_affect.pdf"); fig.savefig(p); plt.close(fig)
    print(f"wrote {p}  (Demo A res {f1A_res:.3f}/static {f1A_stat:.3f}; "
          f"Demo B inst {f1_inst:.3f} memless {mem0.mean():.3f} hom {hom.mean():.3f} het {het.mean():.3f})")


def main():
    os.makedirs(FIGDIR, exist_ok=True)
    cards = load_cards(li_only=True)
    fig_mc_curve(cards)
    fig_composition_sweep(cards)
    fig_wesad(cards)


if __name__ == "__main__":
    main()
