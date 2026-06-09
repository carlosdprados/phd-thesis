#!/usr/bin/env python3
"""Chapter 5 -- continuous stress monitoring on real WESAD streams: the affective
task where fading MEMORY is decisively useful.

The sustained-label classification of ch5_wesad.py is an honest but unflattering
application test: a 60 s window is quasi-static (a static feature baseline ties the
reservoir, Demo A) and, once a slow tonic band is available, timescale
heterogeneity adds little (Demo B, +0.005 ns). That is because those scores are
dominated by long stretches of steady state, where the instantaneous signal level
already says everything.

A deployed wearable is judged on the parts those averages hide: it must (i) flag a
stressor EARLY, as the signal rises, and (ii) keep working under sensor noise and
motion artefact. Both are temporal problems on which an instantaneous classifier is
structurally handicapped and a fading-memory reservoir is not:

  * EARLY DETECTION needs the recent trajectory (is arousal rising?), which a bank
    of different time constants encodes as the spread between fast- and slow-tau
    states -- the instantaneous level alone cannot.
  * NOISE ROBUSTNESS is the defining property of a leaky integrator: fading memory
    is a temporal low-pass that averages transient artefact away, whereas an
    instantaneous (or memoryless) read reacts to every spike -> false alarms.

Task: binary streaming stress detection, stress (WESAD label 2) vs not-stress
(baseline 1 + amusement 3), leave-one-subject-out, single linear ridge read-out --
the same discipline as ch5_wesad.py. Banks compared on matched masks and size:
  inst : instantaneous input, no reservoir memory   -- the static control
  mem0 : memoryless N-node bank (decay=0)           -- dimensionality only
  hom  : homogeneous lead-only bank (memory, 1 tau)
  het  : heterogeneous composition bank (memory, tau spread)

Metrics:
  - binary macro-F1 (overall sanity)
  - transition-window F1: scored only within +/-W s of a label change (the hard part)
  - onset detection latency: seconds from each not-stress->stress onset to the first
    STABLE stress call (>=H s sustained); censored at the episode end
  - noise robustness: binary-F1 and false-alarm rate vs injected sensor-noise sigma

Run from the repo root:  python3 scripts/ch5_onset.py
In-silico devices (Chapter 4 parameter cards); linear read-out only.
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch5_model import load_cards, lead_card                       # noqa: E402
from ch5_reservoir import nodes_from, run_states, _full, paired_stats  # noqa: E402
from ch5_wesad import (load_raw, stream_subject, _ridge_onehot_fit, _predict,  # noqa: E402
                       macro_f1, _roll_mode, LABELS, WASHOUT_S, SMOOTH_S,
                       N_NODES, DT_WES, CHANNELS)

STRESS = 2                       # WESAD stress label
STABLE_S = 5.0                   # sustained-call horizon for "detected" [s]
TRANS_W_S = 20.0                 # +/- window around a label change for transition-F1 [s]
NOISE_SIGMAS = (0.0, 0.05, 0.1, 0.2, 0.3, 0.4)   # injected sensor noise (channels ~[0,1])


# ----------------------------------------------------------------------------
# Noise model: additive sensor noise + occasional motion-artefact bursts
# ----------------------------------------------------------------------------
def add_noise(U, sigma, rng, burst_rate=0.01, burst_gain=3.0):
    """Inject realistic wearable corruption into a scaled (~[0,1]) stream:
    per-sample Gaussian sensor noise of magnitude `sigma`, plus sparse motion-
    artefact bursts (short windows of amplified noise) at rate `burst_rate`.
    Clipped back to [0,1]. sigma=0 returns the clean stream unchanged."""
    if sigma <= 0:
        return U
    T, C = U.shape
    noise = rng.normal(0.0, sigma, size=(T, C))
    if burst_rate > 0:
        starts = np.where(rng.random(T) < burst_rate)[0]
        for s in starts:
            e = min(s + rng.integers(2, 8), T)
            noise[s:e] += rng.normal(0.0, sigma * burst_gain, size=(e - s, C))
    return np.clip(U + noise, 0.0, 1.0)


# ----------------------------------------------------------------------------
# Feature builders (per subject, temporal order preserved)
# ----------------------------------------------------------------------------
def _kept(ls):
    """Boolean mask of steps with a defined affect label, after the washout."""
    keep = np.isin(ls, list(LABELS))
    keep[:int(WASHOUT_S / DT_WES)] = False
    return keep


def bank_features(nodes, raw, dt, sigma=0.0, seed=0, with_input=False):
    """{sid: (X_kept (S,F), ybin_kept (S,))} driving the bank over the full
    (optionally noised) session and keeping defined-label steps in order.
    ybin = 1 for stress, 0 for not-stress."""
    rng = np.random.default_rng(900 + seed)
    feats = {}
    for sid, (U, lab) in raw.items():
        Us, ls = stream_subject(U, lab, dt)
        Us = add_noise(Us, sigma, rng)
        X = run_states(nodes, Us)
        if with_input:
            X = np.hstack([X, Us])
        keep = _kept(ls)
        feats[sid] = (X[keep], (ls[keep] == STRESS).astype(int))
    return feats


def instant_features(raw, dt, sigma=0.0, seed=0):
    """Static control: instantaneous (noised) channel values, no reservoir memory."""
    rng = np.random.default_rng(900 + seed)
    feats = {}
    for sid, (U, lab) in raw.items():
        Us, ls = stream_subject(U, lab, dt)
        Us = add_noise(Us, sigma, rng)
        keep = _kept(ls)
        feats[sid] = (Us[keep], (ls[keep] == STRESS).astype(int))
    return feats


# ----------------------------------------------------------------------------
# LOSO binary read-out, returning per-subject ordered prediction sequences
# ----------------------------------------------------------------------------
def loso_binary(feats, smooth=0):
    """Leave-one-subject-out 2-class ridge. Returns (macro_F1, {sid:(y_true,y_pred)})
    with each held-out subject's sequences in temporal order (for latency/transition
    scoring)."""
    sids = list(feats)
    classes = [0, 1]
    f1s, per = [], {}
    for s in sids:
        Ftr = np.vstack([feats[k][0] for k in sids if k != s])
        ytr = np.concatenate([feats[k][1] for k in sids if k != s])
        Fte, yte = feats[s]
        if len(np.unique(ytr)) < 2 or len(yte) == 0:
            continue
        mu, sd = Ftr.mean(0), Ftr.std(0) + 1e-9
        W = _ridge_onehot_fit((Ftr - mu) / sd, ytr, classes)
        pred = _predict((Fte - mu) / sd, W, classes)
        if smooth > 1:
            pred = _roll_mode(pred, smooth)
        f1s.append(macro_f1(yte, pred, classes))
        per[s] = (yte, pred)
    return (float(np.mean(f1s)) if f1s else float("nan")), per


# ----------------------------------------------------------------------------
# Temporal metrics from the per-subject ordered sequences
# ----------------------------------------------------------------------------
def transition_f1(per, dt, w_s=TRANS_W_S):
    """Macro-F1 restricted to steps within +/- w_s of any label change -- the hard
    region where the instantaneous level is ambiguous and memory should pay."""
    w = max(int(w_s / dt), 1)
    yt, yp = [], []
    for yte, pred in per.values():
        ch = np.where(np.diff(yte) != 0)[0]            # change points (index i -> i+1)
        if len(ch) == 0:
            continue
        mask = np.zeros(len(yte), bool)
        for c in ch:
            mask[max(0, c - w):min(len(yte), c + w + 1)] = True
        yt.append(yte[mask]); yp.append(pred[mask])
    if not yt:
        return float("nan")
    return macro_f1(np.concatenate(yt), np.concatenate(yp), [0, 1])


def onset_latency(per, dt, stable_s=STABLE_S):
    """Median detection latency (s) over all not-stress->stress onsets: time from the
    onset to the first step where the prediction is stress and stays stress for
    >=stable_s. Misses (never stably detected within the episode) are censored at the
    episode length, so a model that simply never fires is penalised, not rewarded."""
    h = max(int(stable_s / dt), 1)
    lats = []
    for yte, pred in per.values():
        onsets = np.where((yte[1:] == 1) & (yte[:-1] == 0))[0] + 1
        for o in onsets:
            end = o
            while end < len(yte) and yte[end] == 1:    # extent of this stress episode
                end += 1
            lat = (end - o) * dt                        # censored = full episode
            for t in range(o, end):
                if t + h <= end and np.all(pred[t:t + h] == 1):
                    lat = (t - o) * dt
                    break
            lats.append(lat)
    return float(np.median(lats)) if lats else float("nan"), len(lats)


def false_alarm_rate(per):
    """Fraction of not-stress steps predicted stress (pooled) -- spurious alarms,
    the cost a noisy instantaneous detector pays and a fading-memory one suppresses."""
    fp = tot = 0
    for yte, pred in per.values():
        ns = yte == 0
        fp += int(np.sum(pred[ns] == 1)); tot += int(np.sum(ns))
    return fp / tot if tot else float("nan")


def subj_f1(per):
    """Per-subject binary macro-F1 (for paired tests across the held-out subjects)."""
    return {s: macro_f1(yt, yp, [0, 1]) for s, (yt, yp) in per.items()}


def subj_transition_f1(per, dt, w_s=TRANS_W_S):
    """Per-subject transition-window macro-F1 (subjects with a label change)."""
    w = max(int(w_s / dt), 1)
    out = {}
    for s, (yt, yp) in per.items():
        ch = np.where(np.diff(yt) != 0)[0]
        if len(ch) == 0:
            continue
        m = np.zeros(len(yt), bool)
        for c in ch:
            m[max(0, c - w):min(len(yt), c + w + 1)] = True
        out[s] = macro_f1(yt[m], yp[m], [0, 1])
    return out


def _paired(a_dict, b_dict):
    """Paired stats over the common subjects of two {sid: score} dicts (a-b)."""
    keys = [k for k in a_dict if k in b_dict]
    return paired_stats([a_dict[k] for k in keys], [b_dict[k] for k in keys])


# ----------------------------------------------------------------------------
# Bank constructors
# ----------------------------------------------------------------------------
def make_banks(cards, dt, n_in, seed=7):
    rng = lambda: np.random.default_rng(seed)
    het = nodes_from(_full(cards), N_NODES, rng(), dt=dt, n_in=n_in, sparsity=0.4)
    hom = nodes_from([lead_card(cards)], N_NODES, rng(), dt=dt, n_in=n_in, sparsity=0.4)
    mem0 = [(0.0, a, w) for (_, a, w) in het]          # memoryless: same masks, no leak
    return het, hom, mem0


# ----------------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------------
def evaluate(raw, cards, dt=DT_WES, sigma=0.0, seed=7, smooth=None):
    """One full comparison (inst/mem0/hom/het) at a given noise level. Returns a
    dict of metrics per bank. The channel count is inferred from the data, so the
    same harness serves the 4-channel chest set and the 3-channel wrist set."""
    C = next(iter(raw.values()))[0].shape[1]
    smooth = int(SMOOTH_S / dt) if smooth is None else smooth
    het, hom, mem0 = make_banks(cards, dt, C, seed)
    specs = {
        "inst": instant_features(raw, dt, sigma, seed),
        "mem0": bank_features(mem0, raw, dt, sigma, seed),
        "hom":  bank_features(hom, raw, dt, sigma, seed),
        "het":  bank_features(het, raw, dt, sigma, seed),
    }
    out = {}
    for name, feats in specs.items():
        f1, per = loso_binary(feats, smooth=smooth)
        lat, n_on = onset_latency(per, dt)
        out[name] = dict(f1=f1, trans_f1=transition_f1(per, dt),
                         latency=lat, far=false_alarm_rate(per), n_onsets=n_on,
                         subj_f1=subj_f1(per), subj_trans=subj_transition_f1(per, dt))
    return out


def noise_sweep(raw, cards, sigmas=NOISE_SIGMAS, dt=DT_WES, seeds=(7, 8, 9)):
    """Binary-F1 and false-alarm rate vs injected noise sigma, seed-averaged.
    Returns {bank: {'f1':(mean,sd) per sigma, 'far':(mean,sd) per sigma}}."""
    banks = ["inst", "mem0", "hom", "het"]
    acc = {b: {"f1": [], "far": []} for b in banks}
    for sg in sigmas:
        per_seed = {b: {"f1": [], "far": []} for b in banks}
        for sd in seeds:
            r = evaluate(raw, cards, dt=dt, sigma=sg, seed=sd)
            for b in banks:
                per_seed[b]["f1"].append(r[b]["f1"])
                per_seed[b]["far"].append(r[b]["far"])
        for b in banks:
            acc[b]["f1"].append((np.mean(per_seed[b]["f1"]), np.std(per_seed[b]["f1"])))
            acc[b]["far"].append((np.mean(per_seed[b]["far"]), np.std(per_seed[b]["far"])))
    return dict(sigmas=list(sigmas), banks={b: acc[b] for b in banks})


def main():
    cards = load_cards(li_only=True)
    if not (os.path.isdir("data/wesad/WESAD")):
        print("WESAD not present; run scripts/ch5_wesad.py for download instructions.")
        return
    raw = load_raw()
    print(f"continuous stress monitoring | {len(raw)} subjects | "
          f"channels {'+'.join(CHANNELS)} | dt={DT_WES:g}s\n")

    print("CLEAN streams (sigma=0):")
    r0 = evaluate(raw, cards, sigma=0.0)
    print(f"  {'bank':5s} {'binF1':>7} {'transF1':>8} {'latency[s]':>11} {'falseAlarm':>11}")
    for b in ("inst", "mem0", "hom", "het"):
        m = r0[b]
        print(f"  {b:5s} {m['f1']:7.3f} {m['trans_f1']:8.3f} "
              f"{m['latency']:11.1f} {m['far']:11.3f}")
    print(f"  (onsets scored: {r0['het']['n_onsets']}; latency dominated by the "
          f"{int(SMOOTH_S):d}s smoothing horizon, comparable across banks)")
    st = _paired(r0["het"]["subj_trans"], r0["inst"]["subj_trans"])
    print(f"  transition-F1 het-inst = {st['mean']:+.3f} "
          f"({int(st['frac_pos']*st['n'])}/{st['n']} subjects, Wilcoxon p={st['p']:.1e})")
    stm = _paired(r0["het"]["subj_trans"], r0["mem0"]["subj_trans"])
    print(f"  transition-F1 het-memoryless = {stm['mean']:+.3f} (p={stm['p']:.1e}) "
          f"-> isolates the contribution of fading memory")
    print(f"  false alarms: inst {r0['inst']['far']:.3f} -> het {r0['het']['far']:.3f} "
          f"({100*(1-r0['het']['far']/r0['inst']['far']):.0f}% fewer)")

    print("\nNOISE ROBUSTNESS (binary-F1 vs injected sensor-noise sigma; seed-averaged):")
    sw = noise_sweep(raw, cards)
    hdr = "  ".join(f"sig={s:g}" for s in sw["sigmas"])
    print(f"  {'bank':5s}  {hdr}")
    for b in ("inst", "mem0", "hom", "het"):
        vals = "  ".join(f"{m:.3f}" for m, _ in sw["banks"][b]["f1"])
        print(f"  {b:5s}  {vals}")
    print("  false-alarm rate vs sigma:")
    for b in ("inst", "mem0", "hom", "het"):
        vals = "  ".join(f"{m:.3f}" for m, _ in sw["banks"][b]["far"])
        print(f"  {b:5s}  {vals}")

    # headline robustness statement + per-subject paired test at a representative sigma
    hi = len(sw["sigmas"]) - 1
    d = sw["banks"]["het"]["f1"][hi][0] - sw["banks"]["inst"]["f1"][hi][0]
    print(f"\n  at sigma={sw['sigmas'][hi]:g}: het binary-F1 {sw['banks']['het']['f1'][hi][0]:.3f} "
          f"vs instantaneous {sw['banks']['inst']['f1'][hi][0]:.3f}  (memory advantage {d:+.3f})")
    rN = evaluate(raw, cards, sigma=sw["sigmas"][hi])
    stN = _paired(rN["het"]["subj_f1"], rN["inst"]["subj_f1"])
    print(f"  per-subject paired (het-inst binary-F1 at sigma={sw['sigmas'][hi]:g}): "
          f"{stN['mean']:+.3f}, {int(stN['frac_pos']*stN['n'])}/{stN['n']} subjects, "
          f"Wilcoxon p={stN['p']:.1e}")


if __name__ == "__main__":
    main()
