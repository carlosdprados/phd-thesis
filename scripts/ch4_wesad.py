#!/usr/bin/env python3
"""Chapter 4 affective-computing task harness (WESAD).

Run from the repo root:  python3 scripts/ch4_wesad.py
  - If the WESAD dataset is present at data/wesad/WESAD/, runs the two
    demonstrations on real data.
  - If not, prints download instructions and runs a SYNTHETIC SMOKE TEST that
    exercises the entire pipeline (windowing -> reservoir encoding -> readout ->
    macro-F1) on fabricated labelled windows, so the code is verified ready.

Demonstrations (handout 12):
  A (non-heterogeneous): binary stress(2) vs baseline(1), single-composition bank
     built from the lead cell PEO 0.3/0.09.
  B (heterogeneous): 3-class baseline/stress/amusement (1/2/3), bank spanning the
     composition grid.

Pipeline: a slow physiological channel (chest EDA, the canonical arousal signal;
multichannel = TODO) is resampled to the reservoir step, sliced into windows,
each window drives the device bank, the pooled reservoir state is classified by a
linear (ridge one-hot) readout. Leave-one-subject-out CV; macro-F1 reported.

Honesty: in-silico devices (Ch3-fitted parameter cards); single-channel input for
now; linear readout only (RC discipline). See handout 12 sec 9.
"""
import os, sys, glob, pickle
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch4_model import load_cards, lead_card  # noqa: E402
from ch4_reservoir import nodes_from, run_states, _full, DT  # noqa: E402

WESAD_DIR = "data/wesad/WESAD"
SLOW_FS = 4.0          # Hz, common slow sampling rate for the physiological channel
WIN_S = 60.0          # window length [s]
STRIDE_S = 30.0       # window stride [s]
LABELS = {1: "baseline", 2: "stress", 3: "amusement"}

DOWNLOAD_MSG = f"""
WESAD not found at '{WESAD_DIR}'.
Download (~2.1 GB) from:
  https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection
Unzip so that the per-subject pickles live at:
  {WESAD_DIR}/S2/S2.pkl , {WESAD_DIR}/S3/S3.pkl , ... S17 (15 subjects)
Then re-run this script. (Running a synthetic smoke test instead.)
"""


# ----------------------------------------------------------------------------
# WESAD loading
# ----------------------------------------------------------------------------
def _resample(x, fs_in, fs_out):
    x = np.asarray(x, float).ravel()
    n_out = max(int(len(x) * fs_out / fs_in), 1)
    idx = np.linspace(0, len(x) - 1, n_out)
    return np.interp(idx, np.arange(len(x)), x)


def load_subject(pkl_path):
    """Return (eda_slow @ SLOW_FS, label_slow @ SLOW_FS) for one WESAD subject."""
    with open(pkl_path, "rb") as fh:
        d = pickle.load(fh, encoding="latin1")
    chest = d["signal"]["chest"]
    eda = np.asarray(chest["EDA"], float).ravel()      # 700 Hz
    label = np.asarray(d["label"], float).ravel()      # 700 Hz
    eda_s = _resample(eda, 700.0, SLOW_FS)
    lab_s = np.round(_resample(label, 700.0, SLOW_FS)).astype(int)
    return eda_s, lab_s


def windows_from(sig, lab, rng=None):
    """Slice into fixed windows keeping only pure-label windows in LABELS."""
    w = int(WIN_S * SLOW_FS); s = int(STRIDE_S * SLOW_FS)
    out = []
    for a in range(0, len(sig) - w + 1, s):
        seg, lseg = sig[a:a + w], lab[a:a + w]
        vals, counts = np.unique(lseg, return_counts=True)
        dom = int(vals[counts.argmax()])
        if dom in LABELS and counts.max() / w > 0.8:
            out.append((seg, dom))
    return out


def load_wesad():
    subs = {}
    for pkl in sorted(glob.glob(os.path.join(WESAD_DIR, "S*", "S*.pkl"))):
        sid = os.path.basename(pkl).split(".")[0]
        try:
            sig, lab = load_subject(pkl)
            subs[sid] = windows_from(sig, lab)
        except Exception as e:
            print(f"  ! skip {sid}: {e}")
    return subs


# ----------------------------------------------------------------------------
# Reservoir encoding + linear readout
# ----------------------------------------------------------------------------
def encode_window(nodes, seg):
    """Resample a window to reservoir steps, normalise to [0,1], drive the bank,
    return a pooled state feature vector (mean + last state)."""
    steps = max(int(WIN_S / DT), 8)
    u = _resample(seg, SLOW_FS, steps / WIN_S)
    u = (u - u.min()) / (u.ptp() + 1e-9)
    X = run_states(nodes, u)
    wo = min(2, X.shape[0] // 4)
    return np.concatenate([X[wo:].mean(0), X[-1]])


def features(nodes, subs):
    F, y, grp = [], [], []
    for sid, wins in subs.items():
        for seg, lab in wins:
            F.append(encode_window(nodes, seg)); y.append(lab); grp.append(sid)
    return np.array(F), np.array(y), np.array(grp)


def _ridge_onehot_fit(F, y, classes, lam=1e-3):
    Y = np.zeros((len(y), len(classes)))
    for i, c in enumerate(classes):
        Y[y == c, i] = 1.0
    Fb = np.hstack([F, np.ones((len(F), 1))])
    W = np.linalg.solve(Fb.T @ Fb + lam * np.eye(Fb.shape[1]), Fb.T @ Y)
    return W


def _predict(F, W, classes):
    Fb = np.hstack([F, np.ones((len(F), 1))])
    return np.array(classes)[(Fb @ W).argmax(1)]


def macro_f1(y_true, y_pred, classes):
    f1s = []
    for c in classes:
        tp = np.sum((y_pred == c) & (y_true == c))
        fp = np.sum((y_pred == c) & (y_true != c))
        fn = np.sum((y_pred != c) & (y_true == c))
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1s.append(2 * prec * rec / (prec + rec) if prec + rec else 0.0)
    return float(np.mean(f1s))


def loso_eval(F, y, grp, classes, lam=1e-3):
    """Leave-one-subject-out macro-F1 (standardise on train folds)."""
    f1s = []
    for s in np.unique(grp):
        tr, te = grp != s, grp == s
        if len(np.unique(y[tr])) < len(classes) or te.sum() == 0:
            continue
        mu, sd = F[tr].mean(0), F[tr].std(0) + 1e-9
        Ftr, Fte = (F[tr] - mu) / sd, (F[te] - mu) / sd
        W = _ridge_onehot_fit(Ftr, y[tr], classes, lam)
        f1s.append(macro_f1(y[te], _predict(Fte, W, classes), classes))
    return float(np.mean(f1s)) if f1s else float("nan")


def run_demos(subs, cards):
    N = 24
    lead = nodes_from([lead_card(cards)], N, np.random.default_rng(7))
    bank = nodes_from(_full(cards), N, np.random.default_rng(7))

    # Demo A: binary stress vs baseline, single-composition (lead) bank
    A = {s: [(seg, l) for seg, l in w if l in (1, 2)] for s, w in subs.items()}
    Fa, ya, ga = features(lead, A)
    f1a = loso_eval(Fa, ya, ga, classes=[1, 2]) if len(Fa) else float("nan")

    # Demo B: 3-class, heterogeneous composition bank
    Fb, yb, gb = features(bank, subs)
    f1b = loso_eval(Fb, yb, gb, classes=[1, 2, 3]) if len(Fb) else float("nan")
    # control: same 3-class task on the homogeneous lead bank
    Fc, yc, gc = features(lead, subs)
    f1c = loso_eval(Fc, yc, gc, classes=[1, 2, 3]) if len(Fc) else float("nan")

    print(f"\nDemo A  binary stress/baseline (lead PEO0.3/0.09 bank)  LOSO macro-F1 = {f1a:.3f}")
    print(f"Demo B  3-class affect (heterogeneous bank)             LOSO macro-F1 = {f1b:.3f}")
    print(f"  control: 3-class on homogeneous lead bank             LOSO macro-F1 = {f1c:.3f}")
    print(f"  heterogeneous - homogeneous (3-class)                 ΔF1 = {f1b - f1c:+.3f}")


# ----------------------------------------------------------------------------
# Synthetic smoke test (no WESAD): verify the full pipeline executes
# ----------------------------------------------------------------------------
def synthetic_subjects(rng):
    """Fabricate slow EDA-like windows whose class differs in timescale content,
    so a multi-timescale reservoir *can* in principle separate them."""
    subs = {}
    t = np.arange(int(WIN_S * SLOW_FS)) / SLOW_FS
    for s in range(6):
        wins = []
        for _ in range(30):
            lab = rng.integers(1, 4)
            f = {1: 0.02, 2: 0.1, 3: 0.04}[lab]          # class-dependent slow rate
            seg = (np.sin(2 * np.pi * f * t) + 0.3 * rng.standard_normal(len(t))
                   + 0.5 * lab)
            wins.append((seg, int(lab)))
        subs[f"S{s}"] = wins
    return subs


def main():
    cards = load_cards(li_only=True)
    if os.path.isdir(WESAD_DIR) and glob.glob(os.path.join(WESAD_DIR, "S*", "S*.pkl")):
        print(f"WESAD found at {WESAD_DIR} -- loading real data.")
        subs = load_wesad()
        nwin = sum(len(w) for w in subs.values())
        print(f"  {len(subs)} subjects, {nwin} usable windows.")
        run_demos(subs, cards)
    else:
        print(DOWNLOAD_MSG)
        subs = synthetic_subjects(np.random.default_rng(0))
        run_demos(subs, cards)
        print("\nsmoke test: pipeline executed end-to-end on synthetic data.")


if __name__ == "__main__":
    main()
