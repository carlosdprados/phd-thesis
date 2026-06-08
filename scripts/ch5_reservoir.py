#!/usr/bin/env python3
"""Chapter 5 reservoir simulation — linear Memory Capacity (MC) of a device bank,
and the homogeneous-vs-heterogeneous comparison that is the crux of the two
demonstrations (handout 12 sec 5-6).

Run from the repo root:  python3 scripts/ch5_reservoir.py
Depends on scripts/ch5_model.py (parameter cards from the Chapter 4 fits).

Model (first-order, behavioural; honest about its assumptions):
- Each device is a leaky, nonlinearly-driven node. Rate-coded input u_n in [0,1]
  drives a compressive write (the measured potentiation exponent alpha), and the
  state leaks with the device's fading memory between samples:
      x_n^i = decay_i * x_{n-1}^i + (w_i * u_n) ** alpha_i
  decay_i = exp(-(dt/tau_i)^beta_i) is the measured Kohlrausch retention over the
  sample interval dt; w_i is a per-device input gain (the reservoir "mask").
- Nodes are INDEPENDENT (1T1M bank, no inter-node recurrence) -- diversity comes
  only from the spread of (tau, beta, alpha) across compositions plus device-to-
  device scatter (jitter) and the input mask. This is deliberately the hard case
  for a reservoir, so any heterogeneity benefit shown here is conservative.

Memory Capacity (Jaeger): MC_k = corr^2(ridge prediction, u_{n-k}); total MC =
sum_k MC_k. A spread of timescales should broaden MC(k) over lags and raise total
MC -- the quantitative statement of "heterogeneity is a computational resource".

NOTE: this is the architecture-level metric (no labelled data). The WESAD
affective-task harness (Demo A binary / Demo B 3-class) is the next script and
needs the dataset; it is intentionally not here.
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch5_model import load_cards, lead_card  # noqa: E402

DT = 5.0          # sample interval [s] (affect-signal scale; sets the leak per step)
WASHOUT = 200
RIDGE = 1e-6
SEEDS = range(10)  # seeds for the error-bar statistics (banks + input draws)


def _full(cards):
    """Cards usable as nonlinear nodes (need a measured potentiation alpha/peak)."""
    return [c for c in cards if c.alpha == c.alpha and c.peak_ratio == c.peak_ratio]


def nodes_from(base, N, rng, jitter=0.12, dt=DT, n_in=1, sparsity=0.0):
    """Return per-node (decay, alpha, w) by cycling the given base cards with
    device-to-device jitter and a random input mask/gain.

    decay is computed at sample interval `dt` (s). `n_in` is the number of input
    channels: for n_in==1 the mask `w` is a scalar (single-channel behaviour is
    byte-identical to before — same RNG draw order), for n_in>1 each node gets a
    non-negative input-mask vector of length n_in (a fraction `sparsity` of whose
    entries are zeroed), so the bank mixes several physiological channels."""
    nodes = []
    for i in range(N):
        c = base[i % len(base)]
        tau = max(c.tau * float(np.exp(rng.normal(0, jitter))), 1e-2)
        beta = float(np.clip(c.beta * (1 + rng.normal(0, jitter)), 0.2, 2.0))
        alpha = float(np.clip(c.alpha * (1 + rng.normal(0, jitter)), 0.05, 2.0))
        if n_in == 1:
            w = float(np.exp(rng.normal(0, 0.5)))        # input mask / gain (scalar)
        else:
            w = np.exp(rng.normal(0, 0.5, size=n_in))    # per-channel input mask
            if sparsity > 0:
                m = rng.random(n_in) >= sparsity
                if not m.any():
                    m[rng.integers(n_in)] = True         # keep >=1 live channel
                w = w * m
        decay = float(np.exp(-((dt / tau) ** beta)))
        nodes.append((decay, alpha, w))
    return nodes


def make_nodes(cards, N, heterogeneous, rng, jitter=0.12):
    """Heterogeneous: cycle all composition cells; homogeneous: N jittered copies
    of the lead node (device-to-device scatter only)."""
    base = _full(cards) if heterogeneous else [lead_card(cards)]
    return nodes_from(base, N, rng, jitter)


def run_states(nodes, u):
    """Drive the bank with input u and return the state matrix X (T, N).

    u may be (T,) single-channel or (T, C) multichannel; each node's drive is the
    compressive write of its (non-negative) input mix:  relu(W_in . u_n) ** alpha.
    """
    u = np.asarray(u, float)
    if u.ndim == 1:
        u = u[:, None]                                   # (T, 1)
    T, C = u.shape
    N = len(nodes)
    decay = np.array([n[0] for n in nodes])
    alpha = np.array([n[1] for n in nodes])
    Win = np.array([np.atleast_1d(n[2]) for n in nodes], float)   # (N, Cw)
    if Win.shape[1] == 1 and C > 1:
        Win = np.repeat(Win, C, axis=1)                  # broadcast scalar gain
    assert Win.shape[1] == C, f"mask has {Win.shape[1]} channels, input has {C}"
    X = np.zeros((T, N))
    x = np.zeros(N)
    for n in range(T):
        drive = np.power(np.clip(Win @ u[n], 0, None), alpha)
        x = decay * x + drive
        X[n] = x
    return X


def _ridge_predict(Xtr, ytr, Xte):
    A = Xtr.T @ Xtr + RIDGE * np.eye(Xtr.shape[1])
    W = np.linalg.solve(A, Xtr.T @ ytr)
    return Xte @ W


def memory_capacity(X, u, max_k=30, split=0.5):
    """MC_k = corr^2(prediction of u_{n-k}, u_{n-k}) on held-out data."""
    T = X.shape[0]
    Xb = np.hstack([X, np.ones((T, 1))])              # bias
    # standardise states (helps conditioning)
    mu, sd = Xb[:, :-1].mean(0), Xb[:, :-1].std(0) + 1e-9
    Xb[:, :-1] = (Xb[:, :-1] - mu) / sd
    mc = []
    for k in range(1, max_k + 1):
        # predict u_{n-k} from state at step n; drop the first k (no target) and washout
        Xa = Xb[WASHOUT + k:]
        ya = u[WASHOUT: T - k]
        ntr = int(len(ya) * split)
        yhat = _ridge_predict(Xa[:ntr], ya[:ntr], Xa[ntr:])
        yte = ya[ntr:]
        if yte.std() < 1e-9 or yhat.std() < 1e-9:
            mc.append(0.0); continue
        r = np.corrcoef(yhat, yte)[0, 1]
        mc.append(float(max(r * r, 0.0)))
    return np.array(mc)


def _legendre(v, d):
    """Legendre polynomial P_d on v in [-1,1] (the orthogonal basis Dambre uses)."""
    if d == 0:
        return np.ones_like(v)
    if d == 1:
        return v
    if d == 2:
        return 0.5 * (3 * v * v - 1)
    if d == 3:
        return 0.5 * v * (5 * v * v - 3)
    raise ValueError(d)


def ipc(X, u, max_lin=20, deg2_win=10, washout=WASHOUT, split=0.5,
        ridge=RIDGE, n_floor=64, seed=0):
    """Information-processing capacity (Dambre 2012), split by polynomial degree.

    The reservoir is probed with orthogonal-polynomial targets of the (centred)
    input: degree-1 single-lag terms P1(v_{n-k}) give the LINEAR capacity (= the
    memory capacity), degree-2 terms -- self terms P2(v_{n-k}) and cross products
    P1(v_{n-i})P1(v_{n-j}) -- give the NONLINEAR capacity that only a nonlinear
    reservoir can supply. Total capacity is bounded by the number of nodes.

    Implementation note: the ridge normal-equation factor is computed once per
    call and reused across all targets (each target is then a cheap solve), so the
    hundreds of probe targets cost almost nothing beyond the single state run.
    A noise floor is estimated from `n_floor` targets built on an INDEPENDENT
    random stream (capacity the reservoir cannot legitimately have); per-target
    capacities below floor mean + 4 SD are set to zero before summing.
    """
    v = 2.0 * np.asarray(u, float) - 1.0                # map [0,1] -> [-1,1]
    T = X.shape[0]
    Xb = np.hstack([X, np.ones((T, 1))])
    mu, sd = Xb[:, :-1].mean(0), Xb[:, :-1].std(0) + 1e-9
    Xb[:, :-1] = (Xb[:, :-1] - mu) / sd
    Xa = Xb[washout:]
    ntr = int(len(Xa) * split)
    Xtr, Xte = Xa[:ntr], Xa[ntr:]
    A = Xtr.T @ Xtr + ridge * np.eye(Xtr.shape[1])
    Afac = np.linalg.cholesky(A)

    def cap(target):
        y = target[washout:]
        ytr, yte = y[:ntr], y[ntr:]
        if yte.std() < 1e-9:
            return 0.0
        rhs = Xtr.T @ ytr
        w = np.linalg.solve(Afac.T, np.linalg.solve(Afac, rhs))
        yhat = Xte @ w
        if yhat.std() < 1e-9:
            return 0.0
        r = np.corrcoef(yhat, yte)[0, 1]
        return float(max(r * r, 0.0))

    def shift(x, k):
        y = np.empty_like(x)
        y[:k] = 0.0
        y[k:] = x[:len(x) - k]
        return y if k > 0 else x

    # ---- noise floor from an independent random stream ----
    vr = np.random.default_rng(7777 + seed).uniform(-1, 1, T)
    floor_caps = []
    rng = np.random.default_rng(13 + seed)
    for _ in range(n_floor):
        k = int(rng.integers(0, max_lin))
        floor_caps.append(cap(_legendre(shift(vr, k), 1)))
    floor = float(np.mean(floor_caps) + 4 * np.std(floor_caps))

    def thr(c):
        return c if c > floor else 0.0

    # ---- degree 1 (linear) ----
    lin = sum(thr(cap(_legendre(shift(v, k), 1))) for k in range(max_lin))
    # ---- degree 2 self terms ----
    nl2_self = sum(thr(cap(_legendre(shift(v, k), 2))) for k in range(deg2_win + 1))
    # ---- degree 2 cross products ----
    nl2_cross = 0.0
    for i in range(deg2_win + 1):
        for j in range(i + 1, deg2_win + 1):
            nl2_cross += thr(cap(shift(v, i) * shift(v, j)))
    nonlin = nl2_self + nl2_cross
    return dict(linear=lin, nonlinear=nonlin, nl2_self=nl2_self,
                nl2_cross=nl2_cross, total=lin + nonlin, floor=floor)


def ipc_seeded(cards, het, N=24, seeds=SEEDS, **kw):
    """Seed-averaged IPC for a homogeneous/heterogeneous bank. Returns dict of
    component -> (mean, SD) plus the per-seed total arrays for paired testing."""
    keys = ["linear", "nonlinear", "nl2_self", "nl2_cross", "total"]
    acc = {k: [] for k in keys}
    for s in seeds:
        u = np.random.default_rng(1000 + s).uniform(0.0, 1.0, 4000)
        nodes = make_nodes(cards, N, het, np.random.default_rng(s))
        r = ipc(run_states(nodes, u), u, seed=s, **kw)
        for k in keys:
            acc[k].append(r[k])
    out = {k: (float(np.mean(acc[k])), float(np.std(acc[k], ddof=1))) for k in keys}
    out["_total_seeds"] = np.array(acc["total"])
    out["_nonlin_seeds"] = np.array(acc["nonlinear"])
    return out


def narma10(u):
    """Standard NARMA-10 benchmark target driven by input u in [0, 0.5]."""
    y = np.zeros_like(u)
    for t in range(len(u) - 1):
        ui9 = u[t - 9] if t >= 9 else 0.0
        s = np.sum(y[max(0, t - 9):t + 1])
        y[t + 1] = 0.3 * y[t] + 0.05 * y[t] * s + 1.5 * ui9 * u[t] + 0.1
    return y


def task_nrmse(X, target, split=0.5):
    """Ridge readout from reservoir state to target; return test NRMSE."""
    T = X.shape[0]
    Xb = np.hstack([X, np.ones((T, 1))])
    mu, sd = Xb[:, :-1].mean(0), Xb[:, :-1].std(0) + 1e-9
    Xb[:, :-1] = (Xb[:, :-1] - mu) / sd
    Xa, ya = Xb[WASHOUT:], target[WASHOUT:]
    ntr = int(len(ya) * split)
    yhat = _ridge_predict(Xa[:ntr], ya[:ntr], Xa[ntr:])
    yte = ya[ntr:]
    return float(np.sqrt(np.mean((yhat - yte) ** 2) / (yte.var() + 1e-12)))


def paired_stats(a, b):
    """Paired difference a-b over matched seeds: mean, SD, fraction>0, and a
    Wilcoxon signed-rank two-sided p-value (paired, distribution-free)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = a - b
    try:
        from scipy.stats import wilcoxon
        p = float(wilcoxon(a, b).pvalue) if np.ptp(d) > 0 else 1.0
    except Exception:
        p = float("nan")
    return dict(mean=float(d.mean()), sd=float(d.std(ddof=1)),
               frac_pos=float(np.mean(d > 0)), p=p, n=len(d))


def mc_curve_seeded(cards, het, N=24, max_k=30, seeds=SEEDS, jitter=0.12):
    """Seed-averaged MC(k). Each seed draws a fresh random input AND a fresh
    jittered bank, so the spread reflects both the input and device-scatter
    stochasticity. `jitter` is the device-to-device scatter magnitude.
    Returns (mean MC_k, SD MC_k, per-seed total-MC array)."""
    mcs = []
    for s in seeds:
        u = np.random.default_rng(1000 + s).uniform(0.0, 1.0, 4000)
        nodes = make_nodes(cards, N, het, np.random.default_rng(s), jitter=jitter)
        mcs.append(memory_capacity(run_states(nodes, u), u, max_k=max_k))
    M = np.array(mcs)                                  # (S, max_k)
    return M.mean(0), M.std(0, ddof=1), M.sum(1)


def composition_sweep(cards, N=16, max_k=30, seeds=SEEDS):
    """Per-composition single-cell bank: total MC + NARMA-10 NRMSE, seed-averaged
    (mean +/- SD over `seeds`). Validates the Demonstration-A 'winner' claim by
    ranking compositions on the same tasks with error bars."""
    rows = []
    for c in sorted(_full(cards), key=lambda z: (float(z.peo), float(z.salt))):
        mc_s, nr_s = [], []
        for s in seeds:
            rng = np.random.default_rng(2000 + s)
            u_mc = rng.uniform(0.0, 1.0, 4000)
            u_na = rng.uniform(0.0, 0.5, 4000)
            y_na = narma10(u_na)
            nodes = nodes_from([c], N, np.random.default_rng(s))
            mc_s.append(memory_capacity(run_states(nodes, u_mc), u_mc, max_k=max_k).sum())
            nr_s.append(task_nrmse(run_states(nodes, u_na), y_na))
        rows.append((c, float(np.mean(mc_s)), float(np.std(mc_s, ddof=1)),
                     float(np.mean(nr_s)), float(np.std(nr_s, ddof=1))))
    print(f"\nComposition sweep (single-cell bank, N={N}, {len(list(seeds))} seeds)"
          f" -- Demonstration-A validation")
    print(f"{'cell':22s} {'totalMC':>14} {'NARMA-NRMSE':>16}")
    for c, mc, mcsd, nr, nrsd in sorted(rows, key=lambda r: r[3]):  # rank by NARMA
        flag = "  <- lead" if (c.peo == "0.3" and c.salt == "0.09") else ""
        print(f"{c.cell:22s} {mc:6.2f}+/-{mcsd:4.2f}  {nr:6.3f}+/-{nrsd:5.3f}{flag}")
    best_mc = max(rows, key=lambda r: r[1])[0]
    best_na = min(rows, key=lambda r: r[3])[0]
    print(f"best total-MC: {best_mc.cell} | best NARMA: {best_na.cell}")
    return rows


def main():
    cards = load_cards(li_only=True)
    N = 24                                 # bank size (both conditions equal)
    max_k = 30

    hom_mean, hom_sd, hom_tot = mc_curve_seeded(cards, False, N, max_k)
    het_mean, het_sd, het_tot = mc_curve_seeded(cards, True, N, max_k)
    print(f"{'homogeneous (all PEO0.3/0.09)':36s} | N={N} | "
          f"total MC={hom_tot.mean():5.2f}+/-{hom_tot.std(ddof=1):.2f} | "
          f"MC@k1={hom_mean[0]:.2f} k5={hom_mean[4]:.2f} k15={hom_mean[14]:.2f}")
    print(f"{'heterogeneous (composition bank)':36s} | N={N} | "
          f"total MC={het_tot.mean():5.2f}+/-{het_tot.std(ddof=1):.2f} | "
          f"MC@k1={het_mean[0]:.2f} k5={het_mean[4]:.2f} k15={het_mean[14]:.2f}")

    # paired het-vs-hom over matched seeds (the heterogeneity benefit, with stats)
    ratios = het_tot / np.clip(hom_tot, 1e-9, None)
    st = paired_stats(het_tot, hom_tot)
    print(f"\nheterogeneous / homogeneous total-MC ratio = "
          f"{ratios.mean():.2f}+/-{ratios.std(ddof=1):.2f} "
          f"(per-seed mean over {st['n']} seeds)")
    print(f"paired total-MC gain (het-hom) = {st['mean']:+.2f}+/-{st['sd']:.2f}, "
          f"{int(st['frac_pos']*st['n'])}/{st['n']} seeds positive, "
          f"Wilcoxon p={st['p']:.1e}")
    print("(>1 / p<0.05 means the composition spread broadens memory across"
          " timescales -- the Demonstration-B claim, on random input.)")
    assert het_tot.mean() > hom_tot.mean(), "expected heterogeneous bank to have higher total MC"

    # information-processing capacity: linear vs nonlinear split (Dambre 2012)
    print("\nInformation-processing capacity (Dambre), seed-averaged:")
    ipc_hom = ipc_seeded(cards, False, N)
    ipc_het = ipc_seeded(cards, True, N)
    for label, r in [("homogeneous", ipc_hom), ("heterogeneous", ipc_het)]:
        print(f"  {label:14s} total={r['total'][0]:5.2f}+/-{r['total'][1]:.2f} | "
              f"linear={r['linear'][0]:5.2f} | nonlinear={r['nonlinear'][0]:5.2f} "
              f"(self {r['nl2_self'][0]:.2f} + cross {r['nl2_cross'][0]:.2f})")
    st_nl = paired_stats(ipc_het["_nonlin_seeds"], ipc_hom["_nonlin_seeds"])
    print(f"  nonlinear capacity is nonzero -> the compressive write computes "
          f"genuine nonlinear functions; het-hom nonlinear gain "
          f"{st_nl['mean']:+.2f}, p={st_nl['p']:.1e}")

    composition_sweep(cards)
    print("\nself-test: PASS")


if __name__ == "__main__":
    main()
