#!/usr/bin/env python3
"""Chapter 5 physiology temporal-context reconstruction benchmark.

Run from the repo root:
  python3 scripts/ch5_physio_context.py

Purpose
-------
The WESAD classification task is dominated by sustained affect labels, so the
heterogeneous bank does not clearly beat a slow homogeneous bank there. This
script adds the intermediate, affect-aligned benchmark needed for Chapter 5:

  Can the reservoir state reconstruct a multi-lag physiological context vector
  from real EDA/Resp/Temp/HR streams?

The target is not an arbitrary random memory-capacity signal. It is the real
WESAD physiological stream delayed at several affect-relevant lags:
  1, 3 s   -> fast phasic / beat-to-beat context
  8 s      -> respiration / HF-HRV-scale context
  20, 45 s -> tonic / LF-HRV-scale context

The benchmark therefore sits between the task-agnostic MC/NARMA figures and the
final WESAD label classifier: it asks whether composition heterogeneity exposes
more real physiological history to a linear readout than any single-timescale
bank of the same size.

Outputs
-------
  handouts/ch5_physio_context_results.csv
  figures/chapter5/physio_context_reconstruction.pdf

Honesty controls
----------------
All comparisons use leave-one-subject-out splits, linear ridge readouts, and the
same node count. Controls are:
  instantaneous input       current EDA/Resp/Temp/HR only, no reservoir
  memoryless bank           same nonlinear masked dimensionality, decay = 0
  homogeneous fast bank     all nodes from the fastest measured composition
  homogeneous slow bank     all nodes from the lead PEO0.3/salt0.09 composition
  heterogeneous bank        measured composition bank, same node count
"""
import csv
import glob
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ch5_model import load_cards, lead_card  # noqa: E402
from ch5_reservoir import _full, nodes_from, run_states  # noqa: E402
import ch5_wesad as W  # noqa: E402


DT = 1.0
N_NODES = 48
LAGS_S = (1, 3, 8, 20, 45)
SEEDS = range(10)
RIDGE = 1e-3
OUT_CSV = "handouts/ch5_physio_context_results.csv"
FIG_PATH = "figures/chapter5/physio_context_reconstruction.pdf"


def lag_group(lag):
    if lag <= 3:
        return "fast 1-3 s"
    if lag <= 10:
        return "mid 8 s"
    return "slow 20-45 s"


def lagged_targets(Us, lags=LAGS_S):
    """Return delayed physiological streams as (Y, metadata).

    Initial samples are padded but later excluded by the benchmark washout, which
    is at least the maximum lag.
    """
    Us = np.asarray(Us, float)
    feats, meta = [], []
    for ci, channel in enumerate(W.CHANNELS):
        x = Us[:, ci]
        for lag in lags:
            lag = int(lag)
            y = np.empty_like(x)
            y[:lag] = x[0]
            y[lag:] = x[:-lag]
            feats.append(y)
            meta.append({
                "target": f"{channel} t-{lag}s",
                "channel": channel,
                "lag_s": lag,
                "group": lag_group(lag),
            })
    return np.column_stack(feats), meta


def feature_dict(raw, nodes=None, dt=DT):
    """Build {sid: (F, Y)} for one reservoir/control condition."""
    feats = {}
    meta = None
    washout = max(int(W.WASHOUT_S / dt), max(LAGS_S))
    for sid, (U, lab) in raw.items():
        Us, ls = W.stream_subject(U, lab, dt)
        Y, meta = lagged_targets(Us)
        F = Us if nodes is None else run_states(nodes, Us)
        keep = np.isin(ls, list(W.LABELS))
        keep[:washout] = False
        feats[sid] = (F[keep], Y[keep])
    return feats, meta


def _ridge_fit(F, Y, lam=RIDGE):
    Fb = np.hstack([F, np.ones((len(F), 1))])
    return np.linalg.solve(Fb.T @ Fb + lam * np.eye(Fb.shape[1]), Fb.T @ Y)


def loso_regression(feats, per_subject=False):
    """LOSO multi-output ridge regression; returns per-target R2 and NRMSE.

    If `per_subject`, also returns {sid: mean held-out R2 over targets} computed on
    each subject's own block, for the paired het-vs-homogeneous significance test.
    """
    sids = list(feats)
    y_true, y_pred = [], []
    persub = {}
    for sid in sids:
        Ftr = np.vstack([feats[k][0] for k in sids if k != sid])
        Ytr = np.vstack([feats[k][1] for k in sids if k != sid])
        Fte, Yte = feats[sid]

        f_mu = Ftr.mean(axis=0)
        f_sd = Ftr.std(axis=0) + 1e-9
        y_mu = Ytr.mean(axis=0)
        y_sd = Ytr.std(axis=0) + 1e-9

        Wfit = _ridge_fit((Ftr - f_mu) / f_sd, (Ytr - y_mu) / y_sd)
        Fb = np.hstack([(Fte - f_mu) / f_sd, np.ones((len(Fte), 1))])
        pred = (Fb @ Wfit) * y_sd + y_mu
        y_true.append(Yte)
        y_pred.append(pred)
        if per_subject:
            ss_r = np.sum((Yte - pred) ** 2, axis=0)
            ss_t = np.sum((Yte - Yte.mean(axis=0)) ** 2, axis=0) + 1e-12
            persub[sid] = float(np.mean(1.0 - ss_r / ss_t))

    Y = np.vstack(y_true)
    P = np.vstack(y_pred)
    ss_res = np.sum((Y - P) ** 2, axis=0)
    ss_tot = np.sum((Y - Y.mean(axis=0)) ** 2, axis=0) + 1e-12
    r2 = 1.0 - ss_res / ss_tot
    nrmse = np.sqrt(np.mean((Y - P) ** 2, axis=0) / (Y.var(axis=0) + 1e-12))
    if per_subject:
        return r2, nrmse, persub
    return r2, nrmse


def evaluate_condition(raw, cards, condition, seed=None, n_nodes=N_NODES):
    full = _full(cards)
    fast = min(full, key=lambda c: c.tau)
    slow = lead_card(cards)
    rng = np.random.default_rng(0 if seed is None else seed)

    if condition == "instantaneous":
        nodes = None
    elif condition == "memoryless":
        nodes = nodes_from(full, n_nodes, rng, dt=DT, n_in=len(W.CHANNELS), sparsity=0.4)
        nodes = [(0.0, alpha, w) for _, alpha, w in nodes]
    elif condition == "homogeneous_fast":
        nodes = nodes_from([fast], n_nodes, rng, dt=DT, n_in=len(W.CHANNELS), sparsity=0.4)
    elif condition == "homogeneous_slow":
        nodes = nodes_from([slow], n_nodes, rng, dt=DT, n_in=len(W.CHANNELS), sparsity=0.4)
    elif condition == "heterogeneous":
        nodes = nodes_from(full, n_nodes, rng, dt=DT, n_in=len(W.CHANNELS), sparsity=0.4)
    else:
        raise ValueError(f"unknown condition: {condition}")

    feats, meta = feature_dict(raw, nodes)
    r2, nrmse = loso_regression(feats)
    return r2, nrmse, meta


def write_results(rows, path=OUT_CSV):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fields = ["condition", "seed", "n_nodes", "target", "channel", "lag_s",
              "group", "r2", "nrmse"]
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow(row)
    print(f"wrote {path}")


def load_results(path=OUT_CSV):
    out = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            r["seed"] = "" if r["seed"] == "" else int(r["seed"])
            r["n_nodes"] = int(r["n_nodes"])
            r["lag_s"] = int(r["lag_s"])
            r["r2"] = float(r["r2"])
            r["nrmse"] = float(r["nrmse"])
            out.append(r)
    return out


def _condition_seed_means(rows, group=None):
    tmp = {}
    for r in rows:
        if group is not None and r["group"] != group:
            continue
        key = (r["condition"], r["seed"])
        tmp.setdefault(key, []).append(r["r2"])
    return {k: float(np.mean(v)) for k, v in tmp.items()}


def print_summary(rows):
    labels = [
        ("instantaneous", "instantaneous input"),
        ("memoryless", "memoryless bank"),
        ("homogeneous_fast", "homogeneous fast"),
        ("homogeneous_slow", "homogeneous slow"),
        ("heterogeneous", "heterogeneous bank"),
    ]
    print("\nPhysiological temporal-context reconstruction")
    print(f"  targets: {', '.join(str(x) + ' s' for x in LAGS_S)} lags "
          f"x {len(W.CHANNELS)} channels | N={N_NODES} nodes | LOSO ridge")
    print(f"{'condition':24s} {'mean R2':>8s} {'seed sd':>8s} "
          f"{'fast':>8s} {'mid':>8s} {'slow':>8s}")
    for cond, label in labels:
        vals = _condition_seed_means([r for r in rows if r["condition"] == cond])
        arr = np.array(list(vals.values()))
        group_vals = []
        for group in ["fast 1-3 s", "mid 8 s", "slow 20-45 s"]:
            gv = _condition_seed_means([r for r in rows if r["condition"] == cond], group)
            group_vals.append(float(np.mean(list(gv.values()))))
        sd = 0.0 if len(arr) <= 1 else float(arr.std(ddof=1))
        print(f"{label:24s} {arr.mean():8.3f} {sd:8.3f} "
              f"{group_vals[0]:8.3f} {group_vals[1]:8.3f} {group_vals[2]:8.3f}")

    means = {cond: np.mean(list(_condition_seed_means(
        [r for r in rows if r["condition"] == cond]).values()))
        for cond, _ in labels}
    best_hom = max(means["homogeneous_fast"], means["homogeneous_slow"])
    print(f"\n  memory gain over instantaneous: heterogeneous "
          f"{means['heterogeneous'] - means['instantaneous']:+.3f} R2")
    print(f"  heterogeneity gain over best homogeneous: "
          f"{means['heterogeneous'] - best_hom:+.3f} R2")


def paired_significance(raw, cards, n_nodes=N_NODES, seeds=SEEDS):
    """Paired het-vs-best-homogeneous test across subjects on overall R2.

    For each subject, average its held-out R2 over seeds (so the comparison is not
    a single lucky bank draw), then a Wilcoxon signed-rank over the 15 subjects of
    (heterogeneous - homogeneous_slow). This stress-tests the POSITIVE heterogeneity
    result exactly as the WESAD-label null is stress-tested."""
    def persubject_over_seeds(condition):
        acc = {}
        for seed in seeds:
            _, _, ps = _evaluate_persubject(raw, cards, condition, seed, n_nodes)
            for sid, v in ps.items():
                acc.setdefault(sid, []).append(v)
        return {sid: float(np.mean(v)) for sid, v in acc.items()}

    het = persubject_over_seeds("heterogeneous")
    hom = persubject_over_seeds("homogeneous_slow")
    sids = sorted(het)
    a = np.array([het[s] for s in sids])
    b = np.array([hom[s] for s in sids])
    d = a - b
    try:
        from scipy.stats import wilcoxon
        p = float(wilcoxon(a, b).pvalue) if np.ptp(d) > 0 else 1.0
    except Exception:
        p = float("nan")
    print("\nPaired het - homogeneous(slow) over subjects (mean R2 per subject, "
          f"averaged over {len(list(seeds))} seeds):")
    print(f"  n={len(sids)} subjects | mean diff = {d.mean():+.4f} | "
          f"{int((d>0).sum())}/{len(d)} subjects positive | Wilcoxon p={p:.2e}")
    return dict(mean=float(d.mean()), n=len(sids),
                n_pos=int((d > 0).sum()), p=p)


def _evaluate_persubject(raw, cards, condition, seed, n_nodes):
    full = _full(cards)
    fast = min(full, key=lambda c: c.tau)
    slow = lead_card(cards)
    rng = np.random.default_rng(0 if seed is None else seed)
    C = len(W.CHANNELS)
    if condition == "instantaneous":
        nodes = None
    elif condition == "memoryless":
        nodes = nodes_from(full, n_nodes, rng, dt=DT, n_in=C, sparsity=0.4)
        nodes = [(0.0, alpha, w) for _, alpha, w in nodes]
    elif condition == "homogeneous_fast":
        nodes = nodes_from([fast], n_nodes, rng, dt=DT, n_in=C, sparsity=0.4)
    elif condition == "homogeneous_slow":
        nodes = nodes_from([slow], n_nodes, rng, dt=DT, n_in=C, sparsity=0.4)
    elif condition == "heterogeneous":
        nodes = nodes_from(full, n_nodes, rng, dt=DT, n_in=C, sparsity=0.4)
    else:
        raise ValueError(condition)
    feats, _ = feature_dict(raw, nodes)
    return loso_regression(feats, per_subject=True)


def make_figure(rows, path=FIG_PATH):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.rcParams.update({"font.family": "serif", "font.size": 9, "figure.dpi": 150,
                         "savefig.bbox": "tight"})

    order = [
        ("instantaneous", "instantaneous\ninput", "#b0b0b0"),
        ("memoryless", "memoryless\nbank", "#8c8c8c"),
        ("homogeneous_fast", "homogeneous\nfast", "#55a868"),
        ("homogeneous_slow", "homogeneous\nslow", "#4c72b0"),
        ("heterogeneous", "heterogeneous\nbank", "#c44e52"),
    ]
    means, errs = [], []
    for cond, _, _ in order:
        vals = np.array(list(_condition_seed_means(
            [r for r in rows if r["condition"] == cond]).values()))
        means.append(float(vals.mean()))
        errs.append(0.0 if len(vals) <= 1 else float(vals.std(ddof=1)))

    groups = ["fast 1-3 s", "mid 8 s", "slow 20-45 s"]
    group_labels = ["fast\n1-3 s", "mid\n8 s", "slow\n20-45 s"]
    group_conditions = ["homogeneous_fast", "homogeneous_slow", "heterogeneous"]
    group_colors = ["#55a868", "#4c72b0", "#c44e52"]
    group_text = ["hom. fast", "hom. slow", "heterog."]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.1),
                                 gridspec_kw={"width_ratios": [1.1, 1.2]})
    x = np.arange(len(order))
    a1.bar(x, means, yerr=errs, color=[c for _, _, c in order],
           edgecolor="0.2", linewidth=0.5, width=0.65, capsize=3,
           error_kw={"lw": 0.8})
    a1.set_xticks(x)
    a1.set_xticklabels([lab for _, lab, _ in order], fontsize=7.4)
    a1.set_ylabel("held-out $R^2$")
    a1.set_title("(a) Real physiological context", fontsize=8.5)
    a1.set_ylim(0.62, 0.78)
    for xi, val in zip(x, means):
        a1.text(xi, val + 0.006, f"{val:.3f}", ha="center", fontsize=7)

    width = 0.25
    gx = np.arange(len(groups))
    for j, cond in enumerate(group_conditions):
        vals = []
        for group in groups:
            gv = _condition_seed_means([r for r in rows if r["condition"] == cond], group)
            vals.append(float(np.mean(list(gv.values()))))
        a2.bar(gx + (j - 1) * width, vals, width=width, color=group_colors[j],
               edgecolor="0.2", linewidth=0.5, label=group_text[j])
    a2.set_xticks(gx)
    a2.set_xticklabels(group_labels)
    a2.set_ylim(0.62, 0.83)
    a2.set_ylabel("held-out $R^2$")
    a2.set_title("(b) Timescale groups", fontsize=8.5)
    a2.legend(frameon=False, fontsize=7.2, loc="upper right")

    fig.text(0.5, -0.04,
             "Target: EDA/Resp/Temp/HR reconstructed at 1, 3, 8, 20 and 45 s delays "
             f"(LOSO, linear readout, N={N_NODES}).",
             ha="center", fontsize=7.4)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    print(f"wrote {path}")


def run_benchmark():
    cards = load_cards(li_only=True)
    if os.path.isdir(W.WESAD_DIR) and glob.glob(os.path.join(W.WESAD_DIR, "S*", "S*.pkl")):
        print(f"WESAD found at {W.WESAD_DIR}; loading cached streams when available.")
        raw = W.load_raw()
    else:
        print(W.DOWNLOAD_MSG)
        raw = W.synthetic_raw(np.random.default_rng(0))

    rows = []
    conditions = ["instantaneous", "memoryless", "homogeneous_fast",
                  "homogeneous_slow", "heterogeneous"]
    for condition in conditions:
        seeds = [None] if condition == "instantaneous" else list(SEEDS)
        for seed in seeds:
            r2, nrmse, meta = evaluate_condition(raw, cards, condition, seed, N_NODES)
            for i, m in enumerate(meta):
                rows.append({
                    "condition": condition,
                    "seed": "" if seed is None else seed,
                    "n_nodes": N_NODES,
                    "target": m["target"],
                    "channel": m["channel"],
                    "lag_s": m["lag_s"],
                    "group": m["group"],
                    "r2": f"{r2[i]:.8f}",
                    "nrmse": f"{nrmse[i]:.8f}",
                })
            seed_txt = "baseline" if seed is None else f"seed {seed}"
            print(f"  {condition:18s} {seed_txt:9s} mean R2={np.mean(r2):.3f}")
    write_results(rows)
    rows = load_results()
    print_summary(rows)
    paired_significance(raw, cards)
    make_figure(rows)


if __name__ == "__main__":
    run_benchmark()
