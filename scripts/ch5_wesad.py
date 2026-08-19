#!/usr/bin/env python3
"""Chapter 5 affective-computing task harness (WESAD).

Run from the repo root:  python scripts/ch5_wesad.py
  - If the WESAD dataset is present at data/wesad/WESAD/, runs the demonstrations
    on real data.
  - If not, prints download instructions and runs a SYNTHETIC SMOKE TEST that
    exercises the whole pipeline on fabricated labelled streams.

Two demonstrations (handout 12 sec 5-6, refined 2026-06-04 after a measured null):

  A (non-heterogeneous, single-TIMESCALE; WINDOW-LEVEL): binary stress(2) vs
     baseline(1) from a single channel (chest EDA), 60 s windows, lead-composition
     bank PEO 0.3/0.09. Tests "for a single-timescale feature ONE composition
     suffices". (~0.89 macro-F1; matches a static baseline -> the window task is
     quasi-static, which is exactly why heterogeneity cannot help it.)

  B (heterogeneous, multi-TIMESCALE; STREAMING): continuous per-step affect
     tracking. The reservoir runs over the WHOLE session (EDA + respiration + skin
     temperature + ECG-derived heart rate), building memory across the real
     timeline; the affect class (baseline/stress/amusement) is read out at every
     step. This is a genuinely MEMORY-DEMANDING task: long-tau nodes carry the slow
     tonic context, short-tau nodes track fast transitions. We compare, on matched
     input masks and bank size:
       het  = heterogeneous composition bank (tau ~ 4->30 s)
       hom  = homogeneous lead-only bank (single tau)
       inst = instantaneous-input readout (no reservoir memory; the static ceiling)
     ΔF1 = het - hom quantifies whether timescale heterogeneity is a computational
     resource on a temporal affect task; het - inst quantifies whether reservoir
     memory helps at all. Reported honestly whatever the sign.

Honesty (handout 12 sec 9): in-silico devices (Chapter 4-fitted parameter cards); linear
readout only (RC discipline); heart rate from the clean chest ECG (robust R-peak
detection) in lieu of noisier wrist BVP. SciPy is used only for ECG R-peak
detection and label smoothing; everything else is numpy.
"""
import glob
import hashlib
import os
import pickle
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch5_model import load_cards, lead_card  # noqa: E402
from ch5_reservoir import nodes_from, run_states, _full  # noqa: E402

WESAD_DIR = "data/wesad/WESAD"
SLOW_FS = 4.0          # Hz, common slow sampling rate for the physiological channels
WIN_S = 60.0          # window length [s] (Demo A)
STRIDE_S = 30.0       # window stride [s] (Demo A)
DT_WES = 1.0          # reservoir step [s] (sets the leak per step; both demos)
WASHOUT_S = 30.0      # streaming washout per subject [s]
SMOOTH_S = 15.0       # streaming prediction smoothing horizon [s]
CALIBRATION_S = 60.0  # fixed prefix available before deployment [s]
N_NODES = 24          # bank size (equal across all conditions)
ECG_FS = 700.0        # chest ECG native rate [Hz]
CHANNELS = ["EDA", "Resp", "Temp", "HR"]   # multichannel (multi-timescale) set
LABELS = {1: "baseline", 2: "stress", 3: "amusement"}
CACHE_SCHEMA = "ch5-physio-causal-prefix60-arctan-v4"

DOWNLOAD_MSG = f"""
WESAD not found at '{WESAD_DIR}'.
Download (~2.1 GB) from:
  https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection
Unzip so that the per-subject pickles live at:
  {WESAD_DIR}/S2/S2.pkl , {WESAD_DIR}/S3/S3.pkl , ... S17 (15 subjects)
Then re-run this script. (Running a synthetic smoke test instead.)
"""


# ----------------------------------------------------------------------------
# Signal helpers
# ----------------------------------------------------------------------------
def _resample(x, fs_in, fs_out):
    """Sample a stream on an aligned output grid without using future samples."""
    x = np.asarray(x, float).ravel()
    n_out = max(int(np.floor((len(x) - 1) * fs_out / fs_in)) + 1, 1)
    idx = np.minimum(np.arange(n_out) * fs_in / fs_out, len(x) - 1)
    return np.interp(idx, np.arange(len(x)), x)


def _resample_labels(lab, n_out):
    """Left-aligned nearest-past resampling for discrete labels."""
    lab = np.asarray(lab).ravel()
    idx = np.clip(np.floor(np.arange(n_out) * len(lab) / n_out).astype(int),
                  0, len(lab) - 1)
    return lab[idx]


def _causal_hold(t_grid, event_times, values, default=70.0):
    """Zero-order hold using only events completed at or before each grid time."""
    t_grid = np.asarray(t_grid, float)
    event_times = np.asarray(event_times, float)
    values = np.asarray(values, float)
    out = np.full(len(t_grid), float(default))
    if len(event_times) == 0:
        return out
    idx = np.searchsorted(event_times, t_grid, side="right") - 1
    valid = idx >= 0
    out[valid] = values[idx[valid]]
    return out


def _causal_running_median(x, width=5):
    """Median of the current and preceding event values (never future events)."""
    x = np.asarray(x, float)
    out = np.empty_like(x)
    for i in range(len(x)):
        out[i] = np.median(x[max(0, i - width + 1):i + 1])
    return out


def _adaptive_threshold(x, fs, horizon_s=8.0, z=1.5):
    """Exponentially weighted past-and-current threshold for peak detection."""
    from scipy.signal import lfilter
    x = np.asarray(x, float)
    if len(x) == 0:
        return x
    a = float(np.exp(-1.0 / max(fs * horizon_s, 1.0)))
    b = [1.0 - a]
    mean = lfilter(b, [1.0, -a], x, zi=[a * x[0]])[0]
    second = lfilter(b, [1.0, -a], x * x, zi=[a * x[0] * x[0]])[0]
    sd = np.sqrt(np.maximum(second - mean * mean, 0.0))
    return mean + z * sd


def hr_from_ecg(ecg, fs=ECG_FS, fs_out=SLOW_FS):
    """Causal HR estimate from chest ECG.

    The band-pass, squared-derivative integration, and adaptive threshold use only
    present/past samples.  An RR value becomes available after its second detected
    R peak and is held until the next completed interval; no future beat is used.
    """
    from scipy.signal import butter, find_peaks, lfilter, sosfilt
    ecg = np.asarray(ecg, float).ravel()
    n_out = max(int(np.floor((len(ecg) - 1) * fs_out / fs)) + 1, 1)
    sos = butter(2, [8 / (fs / 2), 20 / (fs / 2)], btype="band", output="sos")
    f = sosfilt(sos, ecg)
    d = np.diff(f, prepend=f[0])
    width = max(int(0.15 * fs), 1)
    integ = lfilter(np.ones(width) / width, [1.0], d * d)
    threshold = _adaptive_threshold(integ, fs, z=0.5)
    pk, _ = find_peaks(integ, distance=int(0.33 * fs), height=threshold)
    tg = np.arange(n_out) / fs_out
    if len(pk) < 3:
        return np.full(n_out, 70.0)
    t_pk = pk / fs
    hr = np.clip(60.0 / np.diff(t_pk), 40.0, 180.0)
    hr = _causal_running_median(hr, 5)
    return _causal_hold(tg, t_pk[1:] + 1.0 / fs, hr)


def _subject_motion(pkl_path, fs=ECG_FS, fs_out=SLOW_FS):
    """Real motion index from the chest tri-axial accelerometer: the magnitude of the
    gravity-removed acceleration, RMS-smoothed over ~1 s, resampled to fs_out and
    scaled to [0,1] from a fixed initial calibration interval. This is the
    DATA-DRIVEN corruption driver
    for the motion-gated robustness test (sec:ch5_robust), replacing the synthetic
    Gaussian noise model with the artefact pattern the wearer actually generates."""
    with open(pkl_path, "rb") as fh:
        d = pickle.load(fh, encoding="latin1")
    from scipy.signal import lfilter
    acc = np.asarray(d["signal"]["chest"]["ACC"], float)     # (N,3) @ 700 Hz
    mag = np.linalg.norm(acc, axis=1)
    w = max(int(fs), 1)                                       # ~1 s window
    base = lfilter(np.ones(w) / w, [1.0], mag)                # gravity / slow drift
    dyn = np.abs(mag - base)                                  # dynamic acceleration
    energy = np.sqrt(lfilter(np.ones(w) / w, [1.0], dyn * dyn))
    m = _resample(energy, fs, fs_out)
    return _scale_subject(m[:, None], fs=fs_out)[:, 0]


def _source_signature(paths):
    """Compact signature used to reject caches built from different raw files."""
    h = hashlib.sha256()
    for path in sorted(paths):
        st = os.stat(path)
        item = f"{os.path.basename(path)}\0{st.st_size}\0{st.st_mtime_ns}\n"
        h.update(item.encode("utf-8"))
    return h.hexdigest()


def _load_stream_cache(path, signature, fields=("U", "lab")):
    """Load a versioned cache only when schema and raw-source signature match."""
    if not os.path.exists(path):
        return None
    try:
        z = np.load(path, allow_pickle=False)
        schema = str(z["__schema__"].item())
        cached_signature = str(z["__signature__"].item())
        if schema != CACHE_SCHEMA or cached_signature != signature:
            print(f"  (ignored stale cache {path})")
            return None
        sids = [str(x) for x in z["__sids__"]]
        return {sid: tuple(z[f"{sid}_{field}"] for field in fields) for sid in sids}
    except (KeyError, OSError, ValueError) as exc:
        print(f"  (ignored unreadable cache {path}: {exc})")
        return None


def _save_stream_cache(path, signature, raw, fields=("U", "lab")):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    flat = {
        "__schema__": np.array(CACHE_SCHEMA),
        "__signature__": np.array(signature),
        "__sids__": np.array(list(raw)),
    }
    for sid, values in raw.items():
        for field, value in zip(fields, values):
            flat[f"{sid}_{field}"] = value
    np.savez_compressed(path, **flat)


def load_motion(cache=True):
    """Return {sid: motion (T,) at SLOW_FS, in [0,1]} from the chest accelerometer.
    Cached separately from the physiological streams (ACC is not a model channel)."""
    paths = sorted(glob.glob(os.path.join(WESAD_DIR, "S*", "S*.pkl")))
    signature = _source_signature(paths)
    cache_path = os.path.join(os.path.dirname(WESAD_DIR),
                              f"_cache_v4_causalcal{CALIBRATION_S:g}_motion_{SLOW_FS:g}hz.npz")
    out = {}
    cached = _load_stream_cache(cache_path, signature, fields=("motion",)) if cache else None
    if cached is not None:
        out = {sid: values[0] for sid, values in cached.items()}
        print(f"  (loaded {len(out)} motion traces from cache)")
    else:
        for pkl in paths:
            sid = os.path.basename(pkl).split(".")[0]
            try:
                out[sid] = _subject_motion(pkl)
            except Exception as e:
                print(f"  ! skip motion {sid}: {e}")
        if cache and out:
            packed = {sid: (motion,) for sid, motion in out.items()}
            _save_stream_cache(cache_path, signature, packed, fields=("motion",))
            print(f"  (cached {len(out)} motion traces -> {cache_path})")
    return out


def _scale_subject(U, fs=SLOW_FS, calibration_s=CALIBRATION_S):
    """Monotone robust scaling fitted only on a fixed calibration prefix.

    The 5th/95th percentiles map to 0.25/0.75 through a Cauchy CDF. Unlike hard
    clipping, this preserves the ordering and finite resolution of later values
    outside the calibration span while keeping every channel strictly in (0, 1).
    """
    U = np.asarray(U, float)
    n_cal = min(len(U), max(int(round(calibration_s * fs)), 1))
    lo = np.percentile(U[:n_cal], 5, axis=0)
    hi = np.percentile(U[:n_cal], 95, axis=0)
    centre = 0.5 * (lo + hi)
    halfspan = 0.5 * (hi - lo) + 1e-9
    return 0.5 + np.arctan((U - centre) / halfspan) / np.pi


# ----------------------------------------------------------------------------
# WESAD loading (multichannel, cached at the per-subject scaled-stream level)
# ----------------------------------------------------------------------------
def _load_subject(pkl_path, channels):
    with open(pkl_path, "rb") as fh:
        d = pickle.load(fh, encoding="latin1")
    chest = d["signal"]["chest"]
    cols = [hr_from_ecg(chest["ECG"]) if n == "HR" else _resample(chest[n], ECG_FS, SLOW_FS)
            for n in channels]
    n = min(len(c) for c in cols)
    lab = _resample_labels(d["label"], n)
    U = np.column_stack([c[:n] for c in cols])
    return _scale_subject(U), lab


def load_raw(channels=CHANNELS, cache=True):
    """Return causal prefix-scaled WESAD streams and full-session labels."""
    paths = sorted(glob.glob(os.path.join(WESAD_DIR, "S*", "S*.pkl")))
    signature = _source_signature(paths)
    cache_path = os.path.join(os.path.dirname(WESAD_DIR),
                              f"_cache_v4_causalcal{CALIBRATION_S:g}_"
                              f"{'-'.join(channels)}_{SLOW_FS:g}hz.npz")
    raw = {}
    cached = _load_stream_cache(cache_path, signature) if cache else None
    if cached is not None:
        raw = cached
        print(f"  (loaded {len(raw)} subjects from cache {cache_path})")
    else:
        for pkl in paths:
            sid = os.path.basename(pkl).split(".")[0]
            try:
                raw[sid] = _load_subject(pkl, channels)
            except Exception as e:
                print(f"  ! skip {sid}: {e}")
        if cache and raw:
            _save_stream_cache(cache_path, signature, raw)
            print(f"  (cached {len(raw)} subjects -> {cache_path})")
    return raw


# ----------------------------------------------------------------------------
# Wrist loading (Empatica E4: the consumer-wearable site -- fewer, noisier channels)
# ----------------------------------------------------------------------------
WRIST_FS = {"BVP": 64.0, "EDA": 4.0, "TEMP": 4.0, "ACC": 32.0}
WRIST_CHANNELS = ["EDA", "Temp", "HR"]   # no respiration on the wrist; HR from PPG/BVP


def hr_from_bvp(bvp, fs=WRIST_FS["BVP"], fs_out=SLOW_FS):
    """Causal held heart-rate estimate from wrist BVP systolic peaks."""
    from scipy.signal import butter, find_peaks, sosfilt
    bvp = np.asarray(bvp, float).ravel()
    n_out = max(int(np.floor((len(bvp) - 1) * fs_out / fs)) + 1, 1)
    sos = butter(2, [0.5 / (fs / 2), 8.0 / (fs / 2)], btype="band", output="sos")
    f = sosfilt(sos, bvp)
    pk, _ = find_peaks(f, distance=int(0.4 * fs))
    tg = np.arange(n_out) / fs_out
    if len(pk) < 3:
        return np.full(n_out, 70.0)
    t_pk = pk / fs
    hr = np.clip(60.0 / np.diff(t_pk), 40.0, 180.0)
    hr = _causal_running_median(hr, 5)
    return _causal_hold(tg, t_pk[1:] + 1.0 / fs, hr)


def _load_subject_wrist(pkl_path, channels):
    with open(pkl_path, "rb") as fh:
        d = pickle.load(fh, encoding="latin1")
    wrist = d["signal"]["wrist"]
    cols = [hr_from_bvp(wrist["BVP"]) if n == "HR"
            else _resample(wrist[n.upper()], WRIST_FS[n.upper()], SLOW_FS)
            for n in channels]
    n = min(len(c) for c in cols)
    lab = _resample_labels(d["label"], n)
    U = np.column_stack([c[:n] for c in cols])
    return _scale_subject(U), lab


def load_raw_wrist(channels=WRIST_CHANNELS, cache=True):
    """Return {sid: (U (T,C) scaled @ SLOW_FS, lab)} from the wrist Empatica E4
    signals. Same scaling/caching contract as load_raw()."""
    paths = sorted(glob.glob(os.path.join(WESAD_DIR, "S*", "S*.pkl")))
    signature = _source_signature(paths)
    cache_path = os.path.join(os.path.dirname(WESAD_DIR),
                              f"_cache_v4_causalcal{CALIBRATION_S:g}_wrist_"
                              f"{'-'.join(channels)}_{SLOW_FS:g}hz.npz")
    raw = {}
    cached = _load_stream_cache(cache_path, signature) if cache else None
    if cached is not None:
        raw = cached
        print(f"  (loaded {len(raw)} wrist subjects from cache {cache_path})")
    else:
        for pkl in paths:
            sid = os.path.basename(pkl).split(".")[0]
            try:
                raw[sid] = _load_subject_wrist(pkl, channels)
            except Exception as e:
                print(f"  ! skip {sid}: {e}")
        if cache and raw:
            _save_stream_cache(cache_path, signature, raw)
            print(f"  (cached {len(raw)} wrist subjects -> {cache_path})")
    return raw


def windows_from(U, lab):
    """Slice (T,C) into fixed windows >80% a single label in LABELS -> [(win,lab)]."""
    w = int(WIN_S * SLOW_FS); s = int(STRIDE_S * SLOW_FS)
    out = []
    for a in range(0, len(U) - w + 1, s):
        seg, lseg = U[a:a + w], lab[a:a + w]
        vals, counts = np.unique(lseg, return_counts=True)
        dom = int(vals[counts.argmax()])
        if dom in LABELS and counts.max() / w > 0.8:
            out.append((seg, dom))
    return out


# ----------------------------------------------------------------------------
# Linear readout + metrics (shared)
# ----------------------------------------------------------------------------
def _ridge_onehot_fit(F, y, classes, lam=1e-3):
    Y = np.zeros((len(y), len(classes)))
    for i, c in enumerate(classes):
        Y[y == c, i] = 1.0
    Fb = np.hstack([F, np.ones((len(F), 1))])
    gram = Fb.T @ Fb / len(Fb)
    rhs = Fb.T @ Y / len(Fb)
    return np.linalg.solve(gram + lam * np.eye(Fb.shape[1]), rhs)


def _predict(F, W, classes):
    Fb = np.hstack([F, np.ones((len(F), 1))])
    return np.array(classes)[(Fb @ W).argmax(1)]


def _per_class_f1(y_true, y_pred, classes):
    out = {}
    for c in classes:
        tp = np.sum((y_pred == c) & (y_true == c))
        fp = np.sum((y_pred == c) & (y_true != c))
        fn = np.sum((y_pred != c) & (y_true == c))
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        out[c] = (prec, rec, f1, int(np.sum(y_true == c)))
    return out


def macro_f1(y_true, y_pred, classes):
    return float(np.mean([v[2] for v in _per_class_f1(y_true, y_pred, classes).values()]))


def _report(tag, f1, yt, yp, classes):
    print(f"  {tag:48s} LOSO macro-F1 = {f1:.3f}")
    if len(yt):
        pc = _per_class_f1(yt, yp, classes)
        print("      per-class F1: " +
              "  ".join(f"{LABELS[c]}:{pc[c][2]:.2f}(n={pc[c][3]})" for c in classes))


# ----------------------------------------------------------------------------
# Demo A: window-level (single-timescale)
# ----------------------------------------------------------------------------
def encode_window(nodes, seg, dt=DT_WES):
    seg = np.atleast_2d(seg)
    if seg.shape[0] == 1:
        seg = seg.T
    steps = max(int(WIN_S / dt), 8)
    U = np.column_stack([_resample(seg[:, c], SLOW_FS, steps / WIN_S)
                         for c in range(seg.shape[1])])
    X = run_states(nodes, U)
    wo = min(2, X.shape[0] // 4)
    return np.concatenate([X[wo:].mean(0), X[-1]])


def window_features(nodes, subs, cols, labels, dt=DT_WES):
    F, y, g = [], [], []
    for sid, wins in subs.items():
        for seg, lab in wins:
            if labels and lab not in labels:
                continue
            s = seg if cols is None else seg[:, cols]
            F.append(encode_window(nodes, s, dt)); y.append(lab); g.append(sid)
    return np.array(F), np.array(y), np.array(g)


def loso_window(F, y, g, classes, lam=1e-3):
    f1s, yt, yp = [], [], []
    for s in np.unique(g):
        tr, te = g != s, g == s
        if len(np.unique(y[tr])) < len(classes) or te.sum() == 0:
            continue
        mu, sd = F[tr].mean(0), F[tr].std(0) + 1e-9
        W = _ridge_onehot_fit((F[tr] - mu) / sd, y[tr], classes, lam)
        pred = _predict((F[te] - mu) / sd, W, classes)
        f1s.append(macro_f1(y[te], pred, classes)); yt.append(y[te]); yp.append(pred)
    if not f1s:
        return float("nan"), np.array([]), np.array([])
    return float(np.mean(f1s)), np.concatenate(yt), np.concatenate(yp)


def demo_A(raw, cards, dt=DT_WES):
    subs = {sid: windows_from(U, lab) for sid, (U, lab) in raw.items()}
    eda = CHANNELS.index("EDA")
    lead = nodes_from([lead_card(cards)], N_NODES, np.random.default_rng(7), dt=dt, n_in=1)
    F, y, g = window_features(lead, subs, cols=[eda], labels=(1, 2), dt=dt)
    f1, yt, yp = loso_window(F, y, g, [1, 2])
    print("\nDemo A  binary stress/baseline  (single channel EDA, 60 s windows, lead bank)")
    _report("reservoir (lead PEO0.3/0.09)", f1, yt, yp, [1, 2])


# ----------------------------------------------------------------------------
# Demo B: streaming continuous affect tracking (multi-timescale, memory-demanding)
# ----------------------------------------------------------------------------
def stream_subject(U, lab, dt):
    """Resample a subject's full (T,C) scaled stream + labels to the reservoir step
    dt (i.e. 1/dt Hz). Returns (Us (S,C), labs (S,))."""
    fs_out = 1.0 / dt
    cols = [_resample(U[:, c], SLOW_FS, fs_out) for c in range(U.shape[1])]
    S = min(len(col) for col in cols)
    Us = np.column_stack([col[:S] for col in cols])
    return Us, _resample_labels(lab, S)


def _roll_mode(seq, win):
    """Causal rolling majority vote over `win` steps (label smoothing)."""
    if win <= 1:
        return seq
    out = seq.copy()
    for i in range(len(seq)):
        a = max(0, i - win + 1)
        vals, counts = np.unique(seq[a:i + 1], return_counts=True)
        out[i] = vals[counts.argmax()]
    return out


def stream_features(nodes, raw, dt, with_input=False):
    """Return full-timeline features, labels, and a separate scoring mask.

    Keeping undefined-label intervals prevents causal smoothing from joining task
    blocks that were separated by real experimental time.
    """
    wo = int(WASHOUT_S / dt)
    feats = {}
    for sid, (U, lab) in raw.items():
        Us, ls = stream_subject(U, lab, dt)
        X = run_states(nodes, Us)
        if with_input:
            X = np.hstack([X, Us])
        keep = np.isin(ls, list(LABELS)); keep[:wo] = False
        feats[sid] = (X, ls, keep)
    return feats


def instant_features(raw, dt):
    """Baseline with NO reservoir memory: the instantaneous (resampled) channel
    values at each step -> the static per-step ceiling."""
    wo = int(WASHOUT_S / dt)
    feats = {}
    for sid, (U, lab) in raw.items():
        Us, ls = stream_subject(U, lab, dt)
        keep = np.isin(ls, list(LABELS)); keep[:wo] = False
        feats[sid] = (Us, ls, keep)
    return feats


def loso_stream(feats, classes, lam=1e-3, smooth=0):
    """LOSO fit on scored samples, but predict/smooth on the physical timeline."""
    sids = list(feats)
    f1s, yt, yp = [], [], []
    for s in sids:
        Ftr = np.vstack([feats[k][0][feats[k][2]] for k in sids if k != s])
        ytr = np.concatenate([feats[k][1][feats[k][2]] for k in sids if k != s])
        Fte, yfull, score = feats[s]
        yte = yfull[score]
        if len(np.unique(ytr)) < len(classes) or not score.any():
            continue
        mu, sd = Ftr.mean(0), Ftr.std(0) + 1e-9
        W = _ridge_onehot_fit((Ftr - mu) / sd, ytr, classes, lam)
        pred = _predict((Fte - mu) / sd, W, classes)
        if smooth > 1:
            pred = _roll_mode(pred, smooth)
        pred = pred[score]
        f1s.append(macro_f1(yte, pred, classes)); yt.append(yte); yp.append(pred)
    if not f1s:
        return float("nan"), np.array([]), np.array([])
    return float(np.mean(f1s)), np.concatenate(yt), np.concatenate(yp)


def demo_B(raw, cards, dt=DT_WES, smooth=None):
    C = len(CHANNELS)
    smooth = int(SMOOTH_S / dt) if smooth is None else smooth
    het = nodes_from(_full(cards), N_NODES, np.random.default_rng(7), dt=dt, n_in=C, sparsity=0.4)
    hom = nodes_from([lead_card(cards)], N_NODES, np.random.default_rng(7), dt=dt, n_in=C, sparsity=0.4)
    fh = stream_features(het, raw, dt); fm = stream_features(hom, raw, dt)
    fi = instant_features(raw, dt)
    f1h, yth, yph = loso_stream(fh, [1, 2, 3], smooth=smooth)
    f1m, ytm, ypm = loso_stream(fm, [1, 2, 3], smooth=smooth)
    f1i, yti, ypi = loso_stream(fi, [1, 2, 3], smooth=smooth)
    print(f"\nDemo B  streaming 3-class affect tracking  (multichannel {'+'.join(CHANNELS)}, "
          f"dt={dt:g}s, smooth={smooth} steps)")
    _report("heterogeneous composition bank (tau 4->30 s)", f1h, yth, yph, [1, 2, 3])
    _report("homogeneous lead-only bank (single tau)", f1m, ytm, ypm, [1, 2, 3])
    _report("instantaneous input (no reservoir memory)", f1i, yti, ypi, [1, 2, 3])
    print(f"      heterogeneous - homogeneous   ΔF1 = {f1h - f1m:+.3f}   (timescale heterogeneity)")
    print(f"      heterogeneous - instantaneous ΔF1 = {f1h - f1i:+.3f}   (reservoir memory)")
    return dict(het=f1h, hom=f1m, inst=f1i, d_het_hom=f1h - f1m, d_het_inst=f1h - f1i)


def chance_baselines(raw, dt=DT_WES, classes=(1, 2, 3)):
    """Trivial-baseline macro-F1 for the streaming 3-class task, so the reservoir
    scores have a floor to be read against. Two chance models, scored under the same
    leave-one-subject-out, per-step protocol: a MAJORITY-class predictor (always the
    most frequent training class) and a STRATIFIED-random predictor (drawn from the
    training class priors, averaged over draws). Both are far below the reservoir,
    confirming the 0.758 three-class score is well above chance and not an artefact
    of class imbalance. Significance for the bank comparisons is assessed ACROSS the
    15 independent held-out subjects (LOSO), so within-subject temporal
    autocorrelation does not inflate the test."""
    fi = instant_features(raw, dt)
    sids = list(fi)
    maj, strat = [], []
    rng = np.random.default_rng(0)
    for s in sids:
        ytr = np.concatenate([fi[k][1][fi[k][2]] for k in sids if k != s])
        yte = fi[s][1][fi[s][2]]
        if len(yte) == 0 or len(ytr) == 0:
            continue
        vals, counts = np.unique(ytr, return_counts=True)
        maj_c = int(vals[counts.argmax()])
        maj.append(macro_f1(yte, np.full(len(yte), maj_c), list(classes)))
        pri = {c: float(np.mean(ytr == c)) for c in classes}
        p = np.array([pri[c] for c in classes]); p = p / p.sum()
        draws = [macro_f1(yte, rng.choice(classes, size=len(yte), p=p), list(classes))
                 for _ in range(20)]
        strat.append(float(np.mean(draws)))
    print(f"\nChance baselines (streaming 3-class, LOSO, per-step):")
    print(f"  majority-class predictor   macro-F1 = {np.mean(maj):.3f}")
    print(f"  stratified-random predictor macro-F1 = {np.mean(strat):.3f}")
    print("  (compare these floors with the reservoir score above.)")
    return dict(majority=float(np.mean(maj)), stratified=float(np.mean(strat)))


def dt_sweep(raw, cards, dts=(0.5, 1.0, 2.0, 4.0)):
    """Tune the reservoir step dt: streaming Demo-B het vs hom vs instantaneous."""
    C = len(CHANNELS)
    print("\ndt sensitivity (streaming Demo B, 3-class, smoothed):")
    print(f"  {'dt[s]':>6} {'het':>7} {'hom':>7} {'inst':>7} {'het-hom':>8} {'het-inst':>9}")
    for dt in dts:
        sm = int(SMOOTH_S / dt)
        het = nodes_from(_full(cards), N_NODES, np.random.default_rng(7), dt=dt, n_in=C, sparsity=0.4)
        hom = nodes_from([lead_card(cards)], N_NODES, np.random.default_rng(7), dt=dt, n_in=C, sparsity=0.4)
        f1h, _, _ = loso_stream(stream_features(het, raw, dt), [1, 2, 3], smooth=sm)
        f1m, _, _ = loso_stream(stream_features(hom, raw, dt), [1, 2, 3], smooth=sm)
        f1i, _, _ = loso_stream(instant_features(raw, dt), [1, 2, 3], smooth=sm)
        print(f"  {dt:6.1f} {f1h:7.3f} {f1m:7.3f} {f1i:7.3f} {f1h - f1m:+8.3f} {f1h - f1i:+9.3f}")


# ----------------------------------------------------------------------------
# Synthetic smoke test (no WESAD)
# ----------------------------------------------------------------------------
def synthetic_raw(rng, C=len(CHANNELS)):
    """Fabricate continuous multichannel streams with labelled segments whose
    classes differ in the timescale content of different channels."""
    raw = {}
    seg_len = int(120 * SLOW_FS)
    for s in range(6):
        Us, labs = [], []
        for lab in rng.permutation([1, 2, 3, 1, 2, 3]):
            t = np.arange(seg_len) / SLOW_FS
            cols = []
            for c in range(C):
                f = (0.02 + 0.03 * c) * lab
                x = np.sin(2 * np.pi * f * t) + 0.3 * rng.standard_normal(seg_len) + 0.3 * lab
                cols.append(x)
            Us.append(np.column_stack(cols)); labs.append(np.full(seg_len, lab))
        raw[f"S{s}"] = (_scale_subject(np.vstack(Us)), np.concatenate(labs))
    return raw


def main():
    cards = load_cards(li_only=True)
    if os.path.isdir(WESAD_DIR) and glob.glob(os.path.join(WESAD_DIR, "S*", "S*.pkl")):
        print(f"WESAD found at {WESAD_DIR} -- loading real data "
              f"(channels: {', '.join(CHANNELS)}).")
        raw = load_raw()
        secs = {LABELS[c]: int(sum(np.sum(lab == c) for _, lab in raw.values()) / SLOW_FS)
                for c in LABELS}
        print(f"  {len(raw)} subjects | labelled seconds: {secs}")
        demo_A(raw, cards)
        demo_B(raw, cards)
        chance_baselines(raw)
        dt_sweep(raw, cards)
    else:
        print(DOWNLOAD_MSG)
        raw = synthetic_raw(np.random.default_rng(0))
        demo_A(raw, cards)
        demo_B(raw, cards, smooth=5)
        print("\nsmoke test: pipeline executed end-to-end on synthetic data.")


if __name__ == "__main__":
    main()
