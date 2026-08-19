#!/usr/bin/env python3
"""Chapter 5 -- continuous valence/arousal tracking on the CASE corpus.

Run from the repo root:
  python scripts/ch5_case.py

Purpose
-------
The WESAD label task (sec:ch5_wesad) is dominated by sustained, single-timescale
states, so timescale heterogeneity does not separably beat a slow homogeneous
bank there, and on the binary stress monitor a classical moving average matches
the device. Both are single-timescale tasks. This script adds the missing test:
a real, downstream affective target that is INTRINSICALLY MULTI-TIMESCALE, namely
the continuous valence and arousal a viewer reports moment-to-moment. Continuous
affect carries fast phasic excursions and slow tonic drift at once, so it is the
task on which a spread of device timescales should pay where a single one cannot,
and on which the device nonlinearity + spread should separate from a linear EMA.

Corpus
------
CASE (Continuously Annotated Signals of Emotion), Sharma et al., Sci. Data 2019
(figshare 10.6084/m9.figshare.c.4260668). 30 subjects; joystick valence/arousal
in [0.5, 9.5] at 20 Hz; physiology at 1000 Hz (ecg, bvp, gsr, rsp, skt, 3x emg).
We use the WESAD-analogue slow channel set EDA(gsr)/Resp(rsp)/Temp(skt)/HR(ecg),
the eight emotional videos (IDs 1-8; the blue baseline IDs 10/11/12 are dropped),
resampled to a 1 s reservoir cadence and scaled from a fixed initial 60 s
calibration interval.

Method (same RC discipline as the rest of the chapter)
------
- Reservoir state from the measured parameter cards (ch5_model), DT = 1 s, N nodes.
- Read-out is a single linear ridge regression; the reservoir state is reset and
  a short washout dropped at each video boundary, so no memory bleeds across stimuli.
- Banks: instantaneous / memoryless / homogeneous(lead) / heterogeneous(grid),
  plus a classical EMA control (single-tau and a tau-spread bank) -- the linear
  fading-memory filter that ties the device on the single-timescale monitor.
- Metric: concordance correlation coefficient (CCC, the continuous-affect
  standard) and R2, leave-one-subject-out, for valence and arousal.

Outputs
-------
  handouts/ch5_case_results.csv
  figures/chapter5/case_valence_arousal.pdf
"""
import csv
from dataclasses import replace
import glob
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ch5_model import load_cards, lead_card          # noqa: E402
from ch5_reservoir import (_full, memoryless_nodes, nodes_from, run_states,
                           paired_stats)  # noqa: E402
import ch5_wesad as W                                # noqa: E402

DT = 1.0                       # reservoir cadence [s]
N_NODES = 48                   # bank size (affect tier)
SEEDS = range(10)              # bank/mask draw seeds
RIDGE = 1e-3
WASHOUT_S = 10.0               # dropped at each video boundary [s]
PHYS_FS = 1000.0               # CASE physiological rate [Hz]
ANNO_FS = 20.0                 # CASE annotation rate [Hz]
CHANNELS = ["EDA", "Resp", "Temp", "HR"]
TARGETS = ["valence", "arousal"]
EMO_VIDEOS = set(range(1, 9))  # emotional stimuli; 10/11/12 are blue baseline

# CASE interpolated CSVs: env override, else repo data/case, else /tmp extraction.
def _find_case_dir():
    if os.environ.get("CASE_DIR"):
        return os.environ["CASE_DIR"]
    for p in ("data/case/interpolated", "/tmp/CASE_full/data/interpolated"):
        if os.path.isdir(p):
            return p
    return "data/case/interpolated"


CASE_DIR = _find_case_dir()
CACHE = f"data/case/_cache_v4_causalcal{W.CALIBRATION_S:g}_case_1hz.npz"
OUT_CSV = "handouts/ch5_case_results.csv"
FIG_PATH = "figures/chapter5/case_valence_arousal.pdf"


# ----------------------------------------------------------------------------
# Loading: 1000 Hz physiology + 20 Hz annotations -> a common 1 s grid
# ----------------------------------------------------------------------------
def _bin_mean(x, k):
    """Mean over consecutive blocks of k samples (drops the ragged tail)."""
    x = np.asarray(x, float)
    n = (len(x) // k) * k
    return x[:n].reshape(-1, k).mean(axis=1)


def _bin_mode(x, k):
    x = np.asarray(x)
    n = (len(x) // k) * k
    blk = x[:n].reshape(-1, k)
    return np.array([np.bincount(b.astype(int)).argmax() for b in blk])


def _parse_subject(sid):
    """Return (U raw (T,4), valence (T,), arousal (T,), video (T,)) on a 1 s grid."""
    phys = os.path.join(CASE_DIR, "physiological", f"sub_{sid}.csv")
    anno = os.path.join(CASE_DIR, "annotations", f"sub_{sid}.csv")
    P = np.loadtxt(phys, delimiter=",", skiprows=1)        # daqtime,ecg,bvp,gsr,rsp,skt,emg*3,video
    A = np.loadtxt(anno, delimiter=",", skiprows=1)        # jstime,valence,arousal,video
    kp = int(PHYS_FS)                                       # 1000 samples / s
    ka = int(ANNO_FS)                                       # 20 samples / s
    gsr, rsp, skt = P[:, 3], P[:, 4], P[:, 5]
    hr = W.hr_from_ecg(P[:, 1], fs=PHYS_FS, fs_out=1.0)     # robust R-peak HR at 1 Hz
    eda1, rsp1, skt1 = _bin_mean(gsr, kp), _bin_mean(rsp, kp), _bin_mean(skt, kp)
    vid1 = _bin_mode(P[:, 9], kp)
    val1, aro1 = _bin_mean(A[:, 1], ka), _bin_mean(A[:, 2], ka)
    T = min(len(eda1), len(rsp1), len(skt1), len(hr), len(vid1), len(val1), len(aro1))
    U = np.column_stack([eda1[:T], rsp1[:T], skt1[:T], hr[:T]])
    return U, val1[:T], aro1[:T], vid1[:T]


def load_raw(cache=True):
    """Return {sid: (U scaled (T,4), Y (T,2) [valence,arousal], video (T,))}.

    Caches the compact 1 Hz streams so the 4.5 GB of 1000 Hz CSVs are parsed once."""
    paths = sorted(glob.glob(os.path.join(CASE_DIR, "physiological", "sub_*.csv")),
                   key=lambda p: int(os.path.basename(p).split("_")[1].split(".")[0]))
    anno_paths = sorted(glob.glob(os.path.join(CASE_DIR, "annotations", "sub_*.csv")))
    signature = W._source_signature(paths + anno_paths)
    cached = W._load_stream_cache(CACHE, signature, fields=("U", "Y", "v")) if cache else None
    if cached is not None:
        raw = cached
        print(f"  (loaded {len(raw)} CASE subjects from cache {CACHE})")
        return raw
    if not paths:
        print(f"CASE not found under {CASE_DIR}. Fetch CASE_full.zip from figshare\n"
              f"  (10.6084/m9.figshare.8869157) and extract data/interpolated, or set CASE_DIR.")
        sys.exit(1)
    raw, store = {}, {}
    for p in paths:
        sid = os.path.basename(p).split("_")[1].split(".")[0]
        U, val, aro, vid = _parse_subject(sid)
        Us = W._scale_subject(U, fs=1.0)
        Y = np.column_stack([val, aro])
        raw[sid] = (Us, Y, vid)
        store[f"{sid}_U"], store[f"{sid}_Y"], store[f"{sid}_v"] = Us, Y, vid
        print(f"  sub_{sid}: T={len(Us)}s  emotional={int(np.isin(vid, list(EMO_VIDEOS)).sum())}s")
    if cache:
        packed = {sid: (store[f"{sid}_U"], store[f"{sid}_Y"], store[f"{sid}_v"])
                  for sid in raw}
        W._save_stream_cache(CACHE, signature, packed, fields=("U", "Y", "v"))
        print(f"  (cached {len(raw)} subjects -> {CACHE})")
    return raw


def _video_segments(vid):
    """Contiguous index slices of each emotional video (IDs 1-8)."""
    segs, n = [], len(vid)
    i = 0
    while i < n:
        if int(vid[i]) in EMO_VIDEOS:
            j = i
            while j < n and vid[j] == vid[i]:
                j += 1
            segs.append((i, j))
            i = j
        else:
            i += 1
    return segs


# ----------------------------------------------------------------------------
# Feature builders
# ----------------------------------------------------------------------------
def _ema_features(U, taus, dt=DT):
    """Per-channel exponential moving average at one or more time constants:
    s_t = d s_{t-1} + (1-d) x_t, d = exp(-dt/tau). Stacks all (channel x tau)
    smoothed copies -- the classical linear fading-memory filter bank."""
    cols = []
    for tau in taus:
        d = float(np.exp(-dt / tau))
        s = np.zeros_like(U)
        s[0] = U[0]
        for t in range(1, len(U)):
            s[t] = d * s[t - 1] + (1 - d) * U[t]
        cols.append(s)
    return np.hstack(cols)


def _states(condition, U, nodes, cards):
    """Feature matrix for one video segment under the given condition."""
    if condition == "instantaneous":
        return U
    if condition == "ema_single":
        return _ema_features(U, (float(lead_card(cards).tau),))
    if condition == "ema_bank":
        return _ema_features(U, sorted(float(card.tau) for card in _full(cards)))
    return run_states(nodes, U)                          # reservoir banks + memoryless


def _build_nodes(condition, cards, seed):
    full = _full(cards)
    slow = lead_card(cards)
    rng = np.random.default_rng(seed)
    C = len(CHANNELS)
    if condition in ("instantaneous", "ema_single", "ema_bank"):
        return None
    if condition == "memoryless":
        nodes = nodes_from(full, N_NODES, rng, dt=DT, n_in=C, sparsity=0.4)
        return memoryless_nodes(nodes)
    if condition == "homogeneous":
        return nodes_from([slow], N_NODES, rng, dt=DT, n_in=C, sparsity=0.4)
    if condition == "heterogeneous":
        return nodes_from(full, N_NODES, rng, dt=DT, n_in=C, sparsity=0.4)
    if condition == "heterogeneous_perchan":
        # tau spread, but each node reads ONE channel (no random cross-channel
        # mixing): the apples-to-apples device analogue of the linear EMA bank, so
        # the device-vs-EMA gap isolates the compressive nonlinearity, not the mask.
        base = nodes_from(full, N_NODES, rng, dt=DT, n_in=C, sparsity=0.0)
        out = []
        for i, node in enumerate(base):
            oneh = np.zeros(C)
            oneh[i % C] = float(np.linalg.norm(node.w)) or 1.0
            out.append(replace(node, w=oneh))
        return out
    raise ValueError(condition)


def feature_dict(raw, condition, cards, seed):
    """{sid: (F, Y)} with per-video reset + washout, emotional videos only."""
    nodes = _build_nodes(condition, cards, seed)
    wo = int(WASHOUT_S / DT)
    out = {}
    for sid, (U, Y, vid) in raw.items():
        Fs, Ys = [], []
        for (i, j) in _video_segments(vid):
            seg = U[i:j]
            F = _states(condition, seg, nodes, cards)
            k = min(wo, max(0, len(seg) - 5))            # keep at least a few steps
            Fs.append(F[k:]); Ys.append(Y[i:j][k:])
        if Fs:
            out[sid] = (np.vstack(Fs), np.vstack(Ys))
    return out


# ----------------------------------------------------------------------------
# Metrics + LOSO ridge regression
# ----------------------------------------------------------------------------
def ccc(y, p):
    """Lin's concordance correlation coefficient between 1-D y and p."""
    y, p = np.asarray(y, float), np.asarray(p, float)
    vy, vp = y.var(), p.var()
    cov = ((y - y.mean()) * (p - p.mean())).mean()
    den = vy + vp + (y.mean() - p.mean()) ** 2
    return float(2 * cov / den) if den > 0 else 0.0


def _ridge_fit(F, Y, lam=RIDGE):
    Fb = np.hstack([F, np.ones((len(F), 1))])
    gram = Fb.T @ Fb / len(Fb)
    rhs = Fb.T @ Y / len(Fb)
    return np.linalg.solve(gram + lam * np.eye(Fb.shape[1]), rhs)


def loso(feats):
    """Leave-one-subject-out ridge. Returns pooled per-target CCC and R2, and the
    per-subject mean-over-targets CCC (for the paired significance tests)."""
    sids = list(feats)
    yT, yP, persub = [], [], {}
    for sid in sids:
        Ftr = np.vstack([feats[k][0] for k in sids if k != sid])
        Ytr = np.vstack([feats[k][1] for k in sids if k != sid])
        Fte, Yte = feats[sid]
        f_mu, f_sd = Ftr.mean(0), Ftr.std(0) + 1e-9
        y_mu, y_sd = Ytr.mean(0), Ytr.std(0) + 1e-9
        Wt = _ridge_fit((Ftr - f_mu) / f_sd, (Ytr - y_mu) / y_sd)
        Fb = np.hstack([(Fte - f_mu) / f_sd, np.ones((len(Fte), 1))])
        pred = (Fb @ Wt) * y_sd + y_mu
        yT.append(Yte); yP.append(pred)
        persub[sid] = float(np.mean([ccc(Yte[:, t], pred[:, t]) for t in range(Yte.shape[1])]))
    Y, P = np.vstack(yT), np.vstack(yP)
    cccs = [ccc(Y[:, t], P[:, t]) for t in range(Y.shape[1])]
    ss_res = np.sum((Y - P) ** 2, 0)
    ss_tot = np.sum((Y - Y.mean(0)) ** 2, 0) + 1e-12
    r2 = 1.0 - ss_res / ss_tot
    return np.array(cccs), np.array(r2), persub


CONDITIONS = [
    ("instantaneous", "instantaneous (no memory)"),
    ("memoryless",    "memoryless bank"),
    ("ema_single",    "EMA, single tau (classical)"),
    ("ema_bank",      "EMA bank, tau spread (classical)"),
    ("homogeneous",   "homogeneous (memory, lead tau)"),
    ("heterogeneous", "heterogeneous (memory, tau spread)"),
    ("heterogeneous_perchan", "heterogeneous, per-channel (device)"),
]


def evaluate(raw, cards, seeds=SEEDS):
    """Seed-averaged CCC/R2 per condition + per-subject CCC for paired tests."""
    res = {}
    for cond, _ in CONDITIONS:
        seed_ccc, seed_r2, persub_acc = [], [], {}
        sds = [None] if cond in ("instantaneous", "ema_single", "ema_bank") else seeds
        for s in sds:
            feats = feature_dict(raw, cond, cards, 0 if s is None else s)
            c, r, ps = loso(feats)
            seed_ccc.append(c); seed_r2.append(r)
            for sid, v in ps.items():
                persub_acc.setdefault(sid, []).append(v)
        res[cond] = dict(
            ccc=np.mean(seed_ccc, 0), ccc_sd=np.std(seed_ccc, 0),
            r2=np.mean(seed_r2, 0),
            persub={sid: float(np.mean(v)) for sid, v in persub_acc.items()},
        )
    return res


def _paired(res, a, b):
    sids = sorted(set(res[a]["persub"]) & set(res[b]["persub"]))
    da = np.array([res[a]["persub"][s] for s in sids])
    db = np.array([res[b]["persub"][s] for s in sids])
    st = paired_stats(da, db)
    return st, len(sids)


def report(res):
    print("\nCASE continuous valence/arousal  | N=%d nodes | LOSO ridge | DT=%gs" % (N_NODES, DT))
    print(f"{'condition':34s} {'CCC val':>8s} {'CCC aro':>8s} {'CCC mean':>9s} "
          f"{'R2 val':>7s} {'R2 aro':>7s}")
    for cond, label in CONDITIONS:
        d = res[cond]
        print(f"{label:34s} {d['ccc'][0]:8.3f} {d['ccc'][1]:8.3f} {d['ccc'].mean():9.3f} "
              f"{d['r2'][0]:7.3f} {d['r2'][1]:7.3f}")
    print("\nPaired tests over subjects (mean-CCC per subject, seed-averaged):")
    for a, b, tag in [
        ("heterogeneous", "instantaneous", "memory vs instantaneous"),
        ("heterogeneous", "homogeneous",   "heterogeneity vs homogeneous"),
        ("ema_bank",      "ema_single",    "tau spread vs single (EMA)"),
        ("heterogeneous", "ema_bank",      "mixed device vs EMA bank"),
        ("heterogeneous_perchan", "ema_bank", "per-channel device vs EMA bank"),
    ]:
        st, n = _paired(res, a, b)
        print(f"  {tag:32s} dCCC={st['mean']:+.4f}  {int(st['frac_pos']*n)}/{n} subj+  "
              f"p={st['p']:.1e}  r_rb={st['r_rb']:+.2f}")


def write_csv(res, path=OUT_CSV):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["condition", "target", "ccc", "ccc_sd", "r2"])
        for cond, _ in CONDITIONS:
            d = res[cond]
            for ti, t in enumerate(TARGETS):
                w.writerow([cond, t, f"{d['ccc'][ti]:.4f}", f"{d['ccc_sd'][ti]:.4f}",
                            f"{d['r2'][ti]:.4f}"])
    print(f"wrote {path}")


def make_figure(res, path=FIG_PATH):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from figstyle import apply, COLORS, panel, save
    except Exception as e:
        print(f"  (figure skipped: {e})")
        return
    apply()
    order = ["instantaneous", "ema_single", "ema_bank", "heterogeneous", "heterogeneous_perchan"]
    short = {"instantaneous": "instant.", "ema_single": r"single $\tau$",
             "ema_bank": r"$\tau$ spread", "heterogeneous": "device\n(mixed)",
             "heterogeneous_perchan": "device\n(per-ch.)"}
    col = {"instantaneous": COLORS["gray"], "ema_single": COLORS["blue"],
           "ema_bank": COLORS["green"], "heterogeneous": COLORS["orange"],
           "heterogeneous_perchan": COLORS["orange"]}
    fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0))
    x = np.arange(len(order))
    for k, t in enumerate(TARGETS):
        vals = [res[c]["ccc"][k] for c in order]
        sds = [res[c]["ccc_sd"][k] for c in order]
        ax[k].bar(x, vals, yerr=sds, color=[col[c] for c in order], capsize=2)
        ax[k].set_xticks(x)
        ax[k].set_xticklabels([short[c] for c in order], rotation=30, ha="right")
        ax[k].set_ylabel("CCC (held-out)")
        ax[k].set_ylim(0, max(0.05, max(vals) * 1.25))
        panel(ax[k], "ab"[k], t.capitalize())
    save(fig, path)
    print(f"wrote {path}")


def _self_test():
    """Synthetic smoke test: a multi-timescale target the spread should win on."""
    rng = np.random.default_rng(0)
    cards = load_cards(li_only=True)
    raw = {}
    for s in range(6):
        T = 600
        u = rng.uniform(0, 1, (T, len(CHANNELS)))
        val = np.convolve(u[:, 0], np.ones(30) / 30, "same") * 6 + 2
        aro = np.convolve(u[:, 3], np.ones(5) / 5, "same") * 6 + 2
        vid = np.full(T, 1); vid[:50] = 10
        raw[str(s)] = (u, np.column_stack([val, aro]), vid)
    feats = feature_dict(raw, "heterogeneous", cards, 0)
    c, r, ps = loso(feats)
    assert c.shape == (2,) and np.isfinite(c).all(), c
    print("self-test: PASS (CCC=%s)" % np.round(c, 3))


def main():
    cards = load_cards(li_only=True)
    raw = load_raw()
    print(f"\nloaded {len(raw)} CASE subjects")
    res = evaluate(raw, cards)
    report(res)
    write_csv(res)
    make_figure(res)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _self_test()
    else:
        main()
