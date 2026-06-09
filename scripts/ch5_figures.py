#!/usr/bin/env python3
"""Chapter 5 figures:
  fig:ch5_mc_curve          -> mc_curve.pdf          (MC(k): heterogeneous broadens memory)
  fig:ch5_composition_sweep -> composition_sweep.pdf (total MC + NARMA per composition)
  fig:ch5_wesad             -> wesad_affect.pdf       (WESAD: Demo A window task +
                                streaming Demo B decomposition; needs the dataset)

Run from the repo root:  python3 scripts/ch5_figures.py
Depends on scripts/ch5_reservoir.py + scripts/ch5_model.py (+ ch5_wesad.py & the
WESAD dataset for the last figure, which is skipped if the data is absent).
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ch5_reservoir import (load_cards, make_nodes, run_states, memory_capacity,
                           nodes_from, _full, narma10, task_nrmse,
                           mc_curve_seeded, composition_sweep, paired_stats,
                           ipc_seeded, DT)  # noqa: E402

import figstyle

FIGDIR = "figures/chapter5"
figstyle.apply()
COLORS = figstyle.COLORS


def fig_mc_curve(cards, N=24, max_k=30):
    hom_m, hom_sd, hom_tot = mc_curve_seeded(cards, False, N, max_k)
    het_m, het_sd, het_tot = mc_curve_seeded(cards, True, N, max_k)
    st = paired_stats(het_tot, hom_tot)
    k = np.arange(1, max_k + 1)
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    ax.plot(k, hom_m, "o-", ms=3, color=COLORS["blue"],
            label=f"homogeneous (MC$={hom_tot.mean():.1f}\\pm{hom_tot.std(ddof=1):.1f}$)")
    ax.fill_between(k, hom_m - hom_sd, hom_m + hom_sd, color=COLORS["blue"], alpha=0.18)
    ax.plot(k, het_m, "s-", ms=3, color=COLORS["red"],
            label=f"heterogeneous (MC$={het_tot.mean():.1f}\\pm{het_tot.std(ddof=1):.1f}$)")
    ax.fill_between(k, het_m - het_sd, het_m + het_sd, color=COLORS["red"], alpha=0.18)
    ax.set_xlabel(f"delay $k$ (lags of $\\Delta t={DT:g}$ s)")
    ax.set_ylabel("memory capacity MC$_k$")
    ax.set_title(f"Memory capacity vs lag (N={N} nodes)")
    ax.legend(frameon=False, fontsize=8, title=f"Wilcoxon $p={st['p']:.1e}$",
              title_fontsize=7)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "mc_curve.pdf"); fig.savefig(p); plt.close(fig)
    print(f"wrote {p}  (hom {hom_tot.mean():.2f}, het {het_tot.mean():.2f}, "
          f"ratio {het_tot.mean()/hom_tot.mean():.2f}, p={st['p']:.1e})")


def fig_composition_sweep(cards, N=16, max_k=30):
    rows0 = composition_sweep(cards, N=N, max_k=max_k)   # (card, mc, mc_sd, nrmse, nrmse_sd)
    rows0 = sorted(rows0, key=lambda r: (float(r[0].peo), float(r[0].salt)))
    rows = [(f"{c.peo}/{c.salt}", mc, mcsd, nr, nrsd, c.peo == "0.3" and c.salt == "0.09")
            for c, mc, mcsd, nr, nrsd in rows0]
    labels = [r[0] for r in rows]
    mcs = [r[1] for r in rows]; mcsd = [r[2] for r in rows]
    nrs = [r[3] for r in rows]; nrsd = [r[4] for r in rows]
    x = np.arange(len(rows))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0))
    cols = [COLORS["orange"] if r[5] else COLORS["blue"] for r in rows]
    ek = dict(ecolor="0.3", capsize=2, error_kw={"lw": 0.8})
    a1.bar(x, mcs, yerr=mcsd, color=cols, edgecolor="0.2", linewidth=0.5, **ek)
    a1.set_xticks(x); a1.set_xticklabels(labels, rotation=45, ha="right", fontsize=7)
    a1.set_ylabel("total memory capacity"); figstyle.panel(a1, "a", "MC by composition")
    a2.bar(x, nrs, yerr=nrsd, color=cols, edgecolor="0.2", linewidth=0.5, **ek)
    a2.set_xticks(x); a2.set_xticklabels(labels, rotation=45, ha="right", fontsize=7)
    a2.set_ylabel("NARMA-10 NRMSE (lower better)"); figstyle.panel(a2, "b", "NARMA-10 by composition")
    fig.text(0.5, -0.04, "PEO / salt mass fraction (orange = lead cell 0.3/0.09); "
             "error bars $\\pm 1$ SD over 10 seeds", ha="center", fontsize=8)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "composition_sweep.pdf"); fig.savefig(p); plt.close(fig)
    print("wrote", p)


def fig_robustness(cards, N=24, jitters=(0.0, 0.06, 0.12, 0.20, 0.30, 0.40)):
    """Total memory capacity versus injected device-to-device scatter (jitter), for
    the homogeneous and heterogeneous banks. Substantiates the claim that scatter
    is part of the computational substrate, not a yield problem: the heterogeneous
    bank keeps its advantage across the whole realistic spread, and modest scatter
    does not degrade -- and slightly aids -- recoverable memory."""
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    for het, col, mk, lab in [(False, COLORS["blue"], "o", "homogeneous"),
                              (True, COLORS["red"], "s", "heterogeneous")]:
        means, sds = [], []
        for j in jitters:
            _, _, tot = mc_curve_seeded(cards, het, N, jitter=j)
            means.append(tot.mean()); sds.append(tot.std(ddof=1))
        means, sds = np.array(means), np.array(sds)
        ax.plot(jitters, means, mk + "-", ms=4, color=col, label=lab)
        ax.fill_between(jitters, means - sds, means + sds, color=col, alpha=0.18)
    ax.axvline(0.12, ls=":", c="0.5", lw=0.9)
    ax.text(0.125, ax.get_ylim()[0] + 0.3, "measured\nscatter", fontsize=6.6, color="0.45")
    ax.set_xlabel("injected device-to-device scatter (jitter)")
    ax.set_ylabel("total memory capacity")
    ax.set_title(f"Robustness to device scatter (N={N})", fontsize=9.5)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "robustness.pdf"); fig.savefig(p); plt.close(fig)
    print(f"wrote {p}")


def fig_ipc(cards, N=24):
    """Information-processing capacity split into linear (degree 1) and nonlinear
    (degree 2) parts for the homogeneous vs heterogeneous bank. Shows that the
    devices supply a real nonlinear capacity (the compressive write) on top of
    their linear memory, and that heterogeneity raises both. Bounded above by N."""
    hom = ipc_seeded(cards, False, N)
    het = ipc_seeded(cards, True, N)
    st = paired_stats(het["_total_seeds"], hom["_total_seeds"])
    fig, ax = plt.subplots(figsize=(4.4, 3.3))
    x = np.arange(2)
    lin = [hom["linear"][0], het["linear"][0]]
    nl = [hom["nonlinear"][0], het["nonlinear"][0]]
    tot_sd = [hom["total"][1], het["total"][1]]
    ax.bar(x, lin, width=0.6, color=COLORS["blue"], edgecolor="0.2", linewidth=0.5,
           label="linear (degree 1)")
    ax.bar(x, nl, width=0.6, bottom=lin, color=COLORS["orange"], edgecolor="0.2",
           linewidth=0.5, label="nonlinear (degree 2)")
    tot = [a + b for a, b in zip(lin, nl)]
    ax.errorbar(x, tot, yerr=tot_sd, fmt="none", ecolor="0.2", capsize=3, lw=0.8)
    ax.axhline(N, ls="--", c="0.5", lw=0.8)
    ax.text(1.45, N - 0.6, f"$N={N}$ bound", ha="right", fontsize=7, color="0.4")
    for xi, (l, n) in enumerate(zip(lin, nl)):
        ax.text(xi, l / 2, f"{l:.1f}", ha="center", va="center", color="white", fontsize=8)
        ax.text(xi, l + n / 2, f"{n:.1f}", ha="center", va="center", color="white", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(["homogeneous", "heterogeneous"])
    ax.set_ylabel("information-processing capacity")
    ax.set_ylim(0, N + 1)
    ax.set_title("Linear vs nonlinear capacity", fontsize=9.5)
    ax.legend(frameon=False, fontsize=7.6, loc="upper left",
              title=f"total het$-$hom $p={st['p']:.1e}$", title_fontsize=6.8)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "ipc_capacity.pdf"); fig.savefig(p); plt.close(fig)
    print(f"wrote {p}  (hom tot {hom['total'][0]:.2f}, het tot {het['total'][0]:.2f})")


def fig_tau_coverage(cards):
    """The Ch3->Ch4 bridge as a picture: each composition cell placed at its
    measured fading-memory time tau on a log time axis, overlaid on the
    characteristic timescale bands of the peripheral affective signals. Shows at a
    glance which cells cover which channels, and where the composition grid leaves
    a gap (the tonic, minutes band) -- the visual statement of 'the application
    selects the timescale, the device family must cover it'."""
    from ch5_model import lead_card
    full = sorted(_full(cards), key=lambda z: z.tau)
    lead = lead_card(cards)

    # affective signal bands (s): (name, lo, hi)  -- cf. Table 4.1
    bands = [
        ("Phasic EDA (SCR)", 1.0, 10.0, COLORS["orange"]),
        ("Respiration",      3.0, 5.0,  COLORS["green"]),
        ("HRV (HF)",         2.5, 7.0,  COLORS["purple"]),
        ("HRV (LF)",         7.0, 25.0, COLORS["blue"]),
        ("Tonic SCL",        60.0, 300.0, COLORS["red"]),
    ]

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    # band tracks (upper region)
    y0 = len(bands)
    for i, (name, lo, hi, col) in enumerate(bands):
        y = y0 - i
        ax.barh(y, hi - lo, left=lo, height=0.6, color=col, alpha=0.5,
                edgecolor=col, linewidth=0.8)
        ax.text(lo * 0.85, y, name, ha="right", va="center", fontsize=7.6)

    # composition-cell tau markers (lower track). Several cells sit at nearly
    # identical tau (~3 s), so the dots stay at their true tau while the labels
    # are fanned out to evenly spaced positions and joined by thin leader lines.
    # Cells are tau-sorted and labels are placed in the same order, so leaders
    # never cross.
    ytick = 0.0
    y_lab = -1.35
    lab_xs = np.logspace(np.log10(1.15), np.log10(26.0), len(full))
    for c, lx in zip(full, lab_xs):
        is_lead = (c.peo == "0.3" and c.salt == "0.09")
        col = COLORS["orange"] if is_lead else "#333333"
        ax.plot([c.tau, c.tau], [0.4, y0 + 0.4], color=col,
                lw=1.4 if is_lead else 0.6, alpha=0.55 if is_lead else 0.25,
                zorder=0)
        ax.plot(c.tau, ytick, "o", ms=7 if is_lead else 5, color=col, zorder=3)
        ax.plot([c.tau, lx], [ytick - 0.18, y_lab + 0.30], color=col,
                lw=0.5, alpha=0.45, zorder=1)
        ax.annotate(f"{c.peo}/{c.salt}", (lx, y_lab), ha="center", va="top",
                    rotation=90, fontsize=6.2,
                    color=col, fontweight="bold" if is_lead else "normal")
    ax.text(0.92, ytick, "composition\ncells ($\\tau$)",
            ha="right", va="center", fontsize=7.6)

    ax.set_xscale("log")
    ax.set_xlim(0.8, 400)
    ax.set_ylim(-2.9, y0 + 1.0)
    ax.set_yticks([])
    ax.set_xlabel("characteristic timescale (s)")
    ax.set_title("device fading-memory times vs affective-signal bands", fontsize=9.5)
    # mark the uncovered tonic gap (annotation sits in the band region, not on labels)
    gap_lo = max(c.tau for c in full) * 1.05
    ax.axvspan(gap_lo, 60, color="0.85", alpha=0.35, zorder=-1)
    ax.text(np.sqrt(gap_lo * 60), y0 - 1.4, "grid gap\n(drive-boost /\nfuture work)",
            ha="center", va="center", fontsize=6.2, color="0.45", style="italic")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    p = os.path.join(FIGDIR, "tau_coverage.pdf"); fig.savefig(p); plt.close(fig)
    print(f"wrote {p}  (cells tau {full[0].tau:.1f}-{full[-1].tau:.1f}s; "
          f"lead {lead.tau:.1f}s)")


def fig_wesad(cards, seeds=range(5)):
    """WESAD affective computing (needs the dataset). Two honest panels:
    (a) Demo A window-level binary stress/baseline: reservoir vs static baseline
        -> the single-timescale window task is quasi-static (RC ~= static).
    (b) Demo B streaming 3-class decomposition: instantaneous -> +dimensionality
        -> +memory -> +heterogeneity, with seed error bars -> memory helps; the
        timescale-heterogeneity increment is within noise on this affect task."""
    import ch5_wesad as W
    if not (os.path.isdir(W.WESAD_DIR) and
            __import__("glob").glob(os.path.join(W.WESAD_DIR, "S*", "S*.pkl"))):
        print("skip wesad_affect.pdf (WESAD dataset not present)")
        return
    raw = W.load_raw()
    C = len(W.CHANNELS); dt = W.DT_WES; sm = int(W.SMOOTH_S / dt)
    eda = W.CHANNELS.index("EDA")

    # (a) Demo A: reservoir vs static, binary, EDA windows
    subs = {sid: W.windows_from(U, lab) for sid, (U, lab) in raw.items()}
    lead = nodes_from([__import__("ch5_model").lead_card(cards)], W.N_NODES,
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
    from ch5_model import lead_card
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
    a1.bar([0, 1], [f1A_res, f1A_stat], color=[COLORS["orange"], "#b0b0b0"],
           edgecolor="0.2", linewidth=0.5, width=0.6)
    a1.set_xticks([0, 1]); a1.set_xticklabels(["device\nreservoir", "static\nbaseline"])
    a1.set_ylim(0, 1); a1.set_ylabel("LOSO macro-F1")
    figstyle.panel(a1, "a", "Demo A: window binary\nstress/baseline (EDA)")
    a1.axhline(0.5, ls=":", c="0.5", lw=0.8); a1.text(1.5, 0.52, "chance", fontsize=6.5,
                                                      ha="right", color="0.5")
    for x, v in zip([0, 1], [f1A_res, f1A_stat]):
        a1.text(x, v + 0.02, f"{v:.2f}", ha="center", fontsize=7.5)
    # panel (b)
    labels = ["instantaneous\n(no memory)", "memoryless\nbank (dim.)",
              "homogeneous\n(memory, 1$\\tau$)", "heterogeneous\n(memory, $\\tau$ spread)"]
    vals = [f1_inst, mem0.mean(), hom.mean(), het.mean()]
    errs = [0, mem0.std(), hom.std(), het.std()]
    cols = ["#b0b0b0", "#8c8c8c", COLORS["blue"], COLORS["red"]]
    x = np.arange(4)
    a2.bar(x, vals, yerr=errs, color=cols, edgecolor="0.2", linewidth=0.5,
           width=0.62, capsize=3, error_kw={"lw": 0.8})
    a2.set_xticks(x); a2.set_xticklabels(labels, fontsize=7.2)
    a2.set_ylim(0.6, 0.81); a2.set_ylabel("LOSO macro-F1")
    figstyle.panel(a2, "b", "Demo B: streaming 3-class affect tracking")
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


def fig_robust_monitoring(cards):
    """Continuous stress monitoring: fading memory is a noise-robust affective
    substrate. (a) binary stress-detection macro-F1 vs injected sensor-noise sigma --
    the memory banks stay flat while the instantaneous and memoryless controls
    collapse, because temporal integration rejects transient artefact. (b) accuracy
    in the hard region near label transitions on clean streams -- memory lifts it,
    where the instantaneous level is most ambiguous. Needs the WESAD dataset."""
    import ch5_onset as O
    if not os.path.isdir("data/wesad/WESAD"):
        print("skip robust_monitoring.pdf (WESAD dataset not present)")
        return
    raw = O.load_raw()
    sw = O.noise_sweep(raw, cards)
    sig = sw["sigmas"]
    rN = O.evaluate(raw, cards, sigma=sig[-1])         # per-subject scores at the top sigma
    style = {"inst": ("#b0b0b0", "o", "instantaneous (no memory)"),
             "mem0": ("#8c8c8c", "^", "memoryless bank (dim. only)"),
             "hom":  (COLORS["blue"], "s", "homogeneous (memory, 1$\\tau$)"),
             "het":  (COLORS["red"], "D", "heterogeneous (memory, $\\tau$ spread)")}
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.2),
                                 gridspec_kw={"width_ratios": [1.45, 1]})
    for b, (col, mk, lab) in style.items():
        m = np.array([v for v, _ in sw["banks"][b]["f1"]])
        s = np.array([e for _, e in sw["banks"][b]["f1"]])
        a1.plot(sig, m, mk + "-", ms=4, color=col, label=lab)
        a1.fill_between(sig, m - s, m + s, color=col, alpha=0.15)
    a1.set_xlabel("injected sensor-noise $\\sigma$ (channels $\\in[0,1]$)")
    a1.set_ylabel("binary stress-detection macro-F1")
    figstyle.panel(a1, "a", "robustness to sensor noise")
    a1.legend(frameon=False, fontsize=6.4, loc="lower left")
    # panel (b): per-subject het vs inst at the top noise level -> all above diagonal
    si = rN["inst"]["subj_f1"]; sh = rN["het"]["subj_f1"]
    keys = [k for k in sh if k in si]
    xi = np.array([si[k] for k in keys]); yi = np.array([sh[k] for k in keys])
    lo = min(xi.min(), yi.min()) - 0.03; hi = max(xi.max(), yi.max()) + 0.03
    a2.plot([lo, hi], [lo, hi], "--", c="0.6", lw=0.9)
    a2.scatter(xi, yi, s=22, color=COLORS["red"], edgecolor="0.2", linewidth=0.4, zorder=3)
    a2.set_xlim(lo, hi); a2.set_ylim(lo, hi); a2.set_aspect("equal")
    a2.set_xlabel("instantaneous F1"); a2.set_ylabel("heterogeneous F1")
    n_above = int(np.sum(yi > xi))
    figstyle.panel(a2, "b", f"per subject, $\\sigma={sig[-1]:g}$\n({n_above}/{len(keys)} above diagonal)")
    fig.tight_layout()
    p = os.path.join(FIGDIR, "robust_monitoring.pdf"); fig.savefig(p); plt.close(fig)
    print(f"wrote {p}  (sigma{sig[-1]:g} binF1 inst {sw['banks']['inst']['f1'][-1][0]:.3f} "
          f"-> het {sw['banks']['het']['f1'][-1][0]:.3f}; {n_above}/{len(keys)} subjects up)")


def main():
    os.makedirs(FIGDIR, exist_ok=True)
    cards = load_cards(li_only=True)
    fig_tau_coverage(cards)
    fig_ipc(cards)
    fig_robustness(cards)
    fig_mc_curve(cards)
    fig_composition_sweep(cards)
    fig_wesad(cards)
    fig_robust_monitoring(cards)


if __name__ == "__main__":
    main()
