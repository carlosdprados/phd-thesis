#!/usr/bin/env python3
"""Chapter 5 extension -- a composition-designed device filter bank for
electrodermal activity (EDA).

Run from the repo root:  python scripts/ch5_filterbank.py

Question. The reservoir analyses use the device bank as a random temporal
feature generator, and a one-line digital EMA matches or beats it. This script
asks a narrower engineering question: used as *designed* analogue filters (one
device as a baseline tracker, or two compositions as a band-pass), do the
measured relaxation kernels extract the phasic EDA information that a standard
digital pipeline extracts? The fair hardware comparator is an RC filter with the
same half-life; the digital Butterworth pipeline is the accuracy reference.

Model tiers (both are assumptions; a bench replay of EDA event trains into a
real device is the test):
  Tier 1 -- measured-kernel linear filter. The conductance enhancement is
     treated as a superposition with the measured Kohlrausch relaxation
     h(t) = exp[-(t/tau)^beta], applied as an exact causal convolution. Unlike
     the per-step recursion of ch5_reservoir.run_states, which compounds
     exp[-(dt/tau)^beta] into a plain exponential when beta < 1, this
     reproduces the measured half-life at any sample rate.
  Tier 2 -- composed bounded node. The Chapter 5 node generalised to stretched
     relaxation: pulse progress p is a linear filter of the clipped drive with
     kernel h^(1/alpha), and the enhancement is x = p^alpha. A single write
     then decays exactly as h and an unleaked train follows the measured power
     law. For beta = 1 it reduces to run_states (checked in the tests).

Experiments
  E1 design space: frequency responses of single-device high-pass (x - LP) and
     two-device band-pass (LP_fast - LP_slow) designs on the replicated grid,
     against the EDASymp band 0.045-0.25 Hz (Posada-Quintero et al. 2016).
  E2 synthetic ground truth: EDA = tonic drift + Bateman-shaped SCRs at
     calm/aroused block rates + noise (+ motion-like artefacts). Phasic
     recovery, tonic leakage, SCR detection F1 (threshold and lag calibrated on
     separate sessions) and calm/aroused window AUC.
  E3 WESAD: raw chest and wrist EDA (uS, 4 Hz). Within-subject stress-vs-
     baseline AUC of per-minute phasic power and SCR counts, and agreement with
     the digital reference.
  E4 Tier-2 drive sensitivity of the selected device designs.

Statistical units follow Chapter 5: synthetic sessions quantify simulation
sensitivity (mean, SD and sign counts, no p-values); WESAD subjects are
independent, so paired Wilcoxon tests are reported there.
"""
import csv
import glob
import math
import os
import pickle
import sys
from dataclasses import dataclass, field
from itertools import combinations

import numpy as np
from scipy.signal import (butter, fftconvolve, find_peaks, lfilter,
                          peak_prominences, sosfilt, sosfilt_zi)
from scipy.stats import spearmanr, wilcoxon

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch5_model import load_cards  # noqa: E402
from ch5_reservoir import DEFAULT_JITTER, _full  # noqa: E402
from ch5_wesad import WESAD_DIR, _resample_labels, _source_signature  # noqa: E402

OUT = "handouts"
FIG = "figures/chapter5/filterbank.pdf"
FS = 4.0                    # Hz; resolves SCR rise times (~1-3 s)
LN2 = math.log(2.0)
SEED = 20261018
KERNEL_TOL = 1e-4           # truncate the relaxation kernel below this amplitude
KERNEL_TMAX = 1200.0        # s; hard cap on kernel support
JITTER = DEFAULT_JITTER     # median within-cell sigma(ln t_half), Chapter 4 audit

# synthetic sessions
N_CAL, N_TEST = 12, 30
SESSION_MIN = 40.0
BLOCK_MIN = 5.0             # alternating calm / aroused blocks
RATES = (2.0, 8.0)          # nominal SCR onset rates per minute (calm, aroused)
REFRACTORY_S = 1.0          # added to every inter-onset gap
ARTEFACT_RATE = 1.0         # motion-like artefacts per minute (artefact condition)
NOISE_SD = 0.005            # uS, white measurement noise (clean, artefacts)
NOISY_SD = 0.03             # uS, broadband noise of a poorer contact (noisy)
A_MIN = 0.05                # uS, minimum SCR amplitude that counts as a target
CONDITIONS = {"clean": (0.0, NOISE_SD), "noisy": (0.0, NOISY_SD),
              "artefacts": (ARTEFACT_RATE, NOISE_SD)}   # (artefacts/min, white SD)

# detection and scoring
MIN_PEAK_SEP_S = 1.0
MATCH_TOL_S = 2.0
MAX_LAG_S = 12.0
N_THRESH = 40
WIN_S = 60.0
CAL_S = 60.0                # causal calibration prefix (Tier-2 read-out gain)

EDASYMP_BAND = (0.045, 0.25)   # Posada-Quintero et al. (2016)
PHASIC_BAND = (0.05, 1.0)      # conventional phasic / SCR pre-filter
TIER2_DRIVES = (0.05, 1.0)
WESAD_CACHE = os.path.join(os.path.dirname(WESAD_DIR), "_cache_filterbank_eda_uS_4hz.npz")
WESAD_SCHEMA = "ch5-filterbank-raw-eda-uS-blockmean-v1"


# ----------------------------------------------------------------------------
# Relaxation kernels and causal filtering
# ----------------------------------------------------------------------------
def kww(t, tau, beta):
    """Kohlrausch relaxation exp[-(t/tau)^beta] for t >= 0."""
    t = np.clip(np.asarray(t, float), 0.0, None)
    return np.exp(-np.power(t / tau, beta))


def relaxation_kernel(tau, beta, fs=FS, normalise=True):
    """Causal kernel sampled at fs from the measured relaxation.

    With ``normalise`` the kernel has unit DC gain (a low-pass filter);
    without it, k[0] = 1 and k reproduces the free decay of one write.
    """
    t_end = tau * math.log(1.0 / KERNEL_TOL) ** (1.0 / beta)
    n = int(math.ceil(min(t_end, KERNEL_TMAX) * fs)) + 1
    k = kww(np.arange(n) / fs, tau, beta)
    return k / k.sum() if normalise else k


def causal_filter(x, k):
    """y[n] = sum_j k[j] x[n-j], initialised in steady state at x[0].

    The pre-history is held at the first sample, i.e. the device is assumed to
    have equilibrated at the initial input. Only past samples are used.
    """
    x = np.asarray(x, float)
    pad = np.full(len(k) - 1, x[0])
    y = fftconvolve(np.concatenate([pad, x]), k, mode="full")
    return y[len(k) - 1:len(k) - 1 + len(x)]


def composed_progress(u, tau, beta, alpha, n_peak, fs=FS):
    """Tier-2 node: pulse progress p and enhancement x = p^alpha.

    Each full-scale sample advances p by 1/n_peak (the Chapter 5 convention) and
    p relaxes with h^(1/alpha) = KWW(tau * alpha^(1/beta), beta), so that the
    enhancement of a single write decays exactly as the measured h. Returns the
    unclipped progress (to report saturation) and the bounded enhancement.
    """
    tau_g = tau * alpha ** (1.0 / beta)
    g = relaxation_kernel(tau_g, beta, fs, normalise=False)
    p = causal_filter(np.clip(u, 0.0, 1.0), g) / n_peak
    return p, np.power(np.clip(p, 0.0, 1.0), alpha)


# ----------------------------------------------------------------------------
# Filter designs
# ----------------------------------------------------------------------------
def cell_label(card):
    return f"PEO{card.peo}/{card.salt}"


@dataclass(frozen=True)
class Design:
    name: str
    family: str          # device | rc | digital | raw
    topology: str        # HP (x - LP) | BP (LP_fast - LP_slow) | BAND | NONE
    cells: tuple = ()
    band: tuple = ()

    def twin(self, family):
        """Same topology and cells in another family (device <-> rc)."""
        name = self.name.replace(self.family, family, 1)
        return Design(name, family, self.topology, self.cells, self.band)


def build_designs(cells):
    """Every single-device high-pass and two-device band-pass on the grid."""
    ordered = sorted(cells, key=lambda c: c.t_half)
    out = []
    for fam in ("device", "rc"):
        for c in ordered:
            out.append(Design(f"{fam} HP {cell_label(c)}", fam, "HP", (c,)))
        for fast, slow in combinations(ordered, 2):
            if slow.t_half / fast.t_half >= 1.5:
                out.append(Design(f"{fam} BP {cell_label(fast)} - {cell_label(slow)}",
                                  fam, "BP", (fast, slow)))
    out.append(Design("digital phasic 0.05-1 Hz", "digital", "BAND", band=PHASIC_BAND))
    out.append(Design("digital EDASymp 0.045-0.25 Hz", "digital", "BAND", band=EDASYMP_BAND))
    out.append(Design("raw signal", "raw", "NONE"))
    return out


def lowpass_kernel(card, family, scale=1.0):
    """Device: measured KWW kernel. RC: single exponential at the same half-life."""
    if family == "device":
        return relaxation_kernel(card.tau * scale, card.beta)
    return relaxation_kernel(card.t_half * scale / LN2, 1.0)


def make_filter(design, rng=None, jitter=0.0):
    """Return a callable f(x) for one physical instance of the design.

    ``jitter`` draws an independent log-normal timescale scale per device, as in
    the Chapter 5 within-cell variability model.
    """
    if design.family == "raw":
        return lambda x: np.asarray(x, float).copy()
    if design.family == "digital":
        sos = butter(2, design.band, btype="bandpass", fs=FS, output="sos")
        zi0 = sosfilt_zi(sos)

        def digital(x):
            x = np.asarray(x, float)
            return sosfilt(sos, x, zi=zi0 * x[0])[0]
        return digital
    scales = [float(np.exp(rng.normal(0.0, jitter))) if (rng is not None and jitter > 0)
              else 1.0 for _ in design.cells]
    kernels = [lowpass_kernel(c, design.family, s) for c, s in zip(design.cells, scales)]
    if design.topology == "HP":
        return lambda x: np.asarray(x, float) - causal_filter(x, kernels[0])
    return lambda x: causal_filter(x, kernels[0]) - causal_filter(x, kernels[1])


def make_tier2_filter(design, drive, rng=None, jitter=0.0, readout="ac"):
    """Tier-2 composed-node version of a device design.

    The input is mapped to drive u = clip(drive * x / x_ref, 0, 1) with x_ref
    fixed on the causal calibration prefix. The enhancement is mapped back to
    input units by a fixed analogue gain set on that prefix:
      readout="dc"  matches the mean level (gain = mean u / mean x_dev);
      readout="ac"  matches the small-signal gain at the calibration operating
                    point. For x_dev = p^alpha, a fractional change in p appears
                    as alpha times that change in x_dev, so the gain is 1/alpha
                    larger than the level-matched one.
      readout="linearised" keeps the Tier-2 kernel h^(1/alpha) but removes the
                    static compression (the small-signal limit).
    Because x_dev = p^alpha is scale-free, the drive level cancels in both
    read-outs unless the progress saturates; the callable records the peak
    unclipped progress so saturation can be reported.
    """
    scales = [float(np.exp(rng.normal(0.0, jitter))) if (rng is not None and jitter > 0)
              else 1.0 for _ in design.cells]
    state = {"max_progress": 0.0}
    n_cal = int(CAL_S * FS)

    def node_lowpass(x, card, scale, x_ref):
        if readout == "linearised":
            tau_g = card.tau * scale * card.alpha ** (1.0 / card.beta)
            return causal_filter(x, relaxation_kernel(tau_g, card.beta))
        u = np.clip(drive * x / x_ref, 0.0, 1.0)
        p, enh = composed_progress(u, card.tau * scale, card.beta, card.alpha, card.n_peak)
        state["max_progress"] = max(state["max_progress"], float(p.max()))
        x0, e0 = x[:n_cal].mean(), max(enh[:n_cal].mean(), 1e-12)
        if readout == "dc":
            return enh * x0 / e0
        return x0 + (enh - e0) * x0 / (card.alpha * e0)

    def f(x):
        x = np.asarray(x, float)
        x_ref = 2.0 * float(np.percentile(x[:n_cal], 95)) + 1e-12
        lps = [node_lowpass(x, c, s, x_ref) for c, s in zip(design.cells, scales)]
        return x - lps[0] if design.topology == "HP" else lps[0] - lps[1]

    f.state = state
    return f


# ----------------------------------------------------------------------------
# E1: design space (frequency responses)
# ----------------------------------------------------------------------------
def frequency_response(design, freqs):
    """Magnitude response |H(f)| of a nominal design at the given frequencies."""
    if design.family == "raw":
        return np.ones_like(freqs)
    if design.family == "digital":
        from scipy.signal import sosfreqz
        sos = butter(2, design.band, btype="bandpass", fs=FS, output="sos")
        return np.abs(sosfreqz(sos, worN=freqs, fs=FS)[1])
    z = np.exp(-2j * np.pi * freqs / FS)

    def H(card):
        k = lowpass_kernel(card, design.family)
        return np.polyval(k[::-1], z)          # sum_j k[j] z^j

    if design.topology == "HP":
        return np.abs(1.0 - H(design.cells[0]))
    return np.abs(H(design.cells[0]) - H(design.cells[1]))


def design_space(designs):
    freqs = np.logspace(-4, math.log10(FS / 2 * 0.98), 600)
    band = (freqs >= EDASYMP_BAND[0]) & (freqs <= EDASYMP_BAND[1])
    rows = []
    for d in designs:
        if d.family == "raw":
            continue
        mag = frequency_response(d, freqs)
        pk = int(np.argmax(mag))
        half = mag >= mag[pk] / math.sqrt(2.0)
        lo = freqs[half][0]
        hi = freqs[half][-1]
        rows.append({
            "design": d.name, "family": d.family, "topology": d.topology,
            "cells": " | ".join(cell_label(c) for c in d.cells),
            "t_half_s": " | ".join(f"{c.t_half:.2f}" for c in d.cells),
            "tau_s": " | ".join(f"{c.tau:.2f}" for c in d.cells),
            "beta": " | ".join(f"{c.beta:.2f}" for c in d.cells),
            "peak_gain": round(float(mag[pk]), 4),
            "peak_freq_hz": round(float(freqs[pk]), 5),
            "band_lo_hz": round(float(lo), 5),
            "band_hi_hz": round(float(hi), 5),
            "edasymp_mean_gain": round(float(mag[band].mean()), 4),
            "tonic_gain_0.01hz": round(float(np.interp(0.01, freqs, mag)), 4),
        })
    return rows, freqs


def lowpass_corner(card, family="device", freqs=None):
    """-3 dB corner of the single-element low-pass built from a card."""
    freqs = np.logspace(-4, math.log10(FS / 2 * 0.98), 4000) if freqs is None else freqs
    z = np.exp(-2j * np.pi * freqs / FS)
    k = lowpass_kernel(card, family)
    mag = np.abs(np.polyval(k[::-1], z))
    return float(freqs[np.argmax(mag < 1.0 / math.sqrt(2.0))])


def component_cards(cells):
    """Component table: each replicated cell as a filter element."""
    rows = []
    for c in sorted(cells, key=lambda z: z.t_half):
        rows.append({
            "cell": cell_label(c), "n_substrates": c.n_dev,
            "t_half_s": round(c.t_half, 2), "beta": round(c.beta, 2),
            "tau_kww_s": round(c.tau, 2), "tau_rc_s": round(c.t_half / LN2, 2),
            "f_corner_device_hz": round(lowpass_corner(c, "device"), 4),
            "f_corner_rc_hz": round(lowpass_corner(c, "rc"), 4),
            "alpha": round(c.alpha, 2), "peak_ratio": round(c.peak_ratio, 1),
            "n_peak": int(c.n_peak),
        })
    return rows


# ----------------------------------------------------------------------------
# E2: synthetic ground truth
# ----------------------------------------------------------------------------
def bateman(t, tau_rise, tau_decay):
    """Bateman SCR template with unit peak; returns (template, time to peak)."""
    t_pk = math.log(tau_decay / tau_rise) * tau_rise * tau_decay / (tau_decay - tau_rise)
    peak = math.exp(-t_pk / tau_decay) - math.exp(-t_pk / tau_rise)
    t = np.asarray(t, float)
    b = np.where(t >= 0, np.exp(-np.clip(t, 0, None) / tau_decay)
                 - np.exp(-np.clip(t, 0, None) / tau_rise), 0.0)
    return b / peak, t_pk


@dataclass
class Session:
    x: np.ndarray
    tonic: np.ndarray
    phasic: np.ndarray
    peak_t: np.ndarray
    amp: np.ndarray
    aroused: np.ndarray = field(repr=False)


def synth_session(rng, minutes=SESSION_MIN, artefact_rate=0.0, noise_sd=NOISE_SD):
    """One synthetic EDA session (uS at FS) with known SCR peaks.

    Parameters span commonly reported SCR rise (~1-3 s) and half-recovery
    (~2-10 s) times and a minutes-scale tonic drift; aroused blocks raise both
    the SCR rate and the tonic level, as stress does in WESAD.
    """
    n = int(round(minutes * 60 * FS))
    t = np.arange(n) / FS
    block_s = BLOCK_MIN * 60.0
    aroused = (t // block_s).astype(int) % 2 == 1

    a_drift = math.exp(-1.0 / (300.0 * FS))
    drift = lfilter([1.0 - a_drift], [1.0, -a_drift], rng.normal(0, 1, n))
    drift *= 0.3 / (drift.std() + 1e-12)
    a_step = math.exp(-1.0 / (60.0 * FS))
    scl_step = lfilter([1.0 - a_step], [1.0, -a_step], aroused.astype(float))
    tonic = rng.uniform(2.0, 12.0) + drift + rng.uniform(0.2, 1.0) * scl_step

    onsets = []
    for b in range(int(math.ceil(n / FS / block_s))):
        t0, t1 = b * block_s, min((b + 1) * block_s, n / FS)
        rate = RATES[b % 2] / 60.0
        tt = t0 + rng.exponential(1.0 / rate)
        while tt < t1:
            onsets.append(tt)
            tt += REFRACTORY_S + rng.exponential(1.0 / rate)
    onsets = np.array(onsets)
    amp = np.clip(np.exp(rng.normal(math.log(0.2), 0.8, len(onsets))), 0.02, 3.0)
    phasic = np.zeros(n)
    peak_t = np.zeros(len(onsets))
    support = int(60 * FS)
    for i, (on, a) in enumerate(zip(onsets, amp)):
        tr, td = rng.uniform(0.5, 1.2), rng.uniform(2.0, 7.0)
        i0 = int(math.ceil(on * FS))
        seg = np.arange(i0, min(i0 + support, n))
        tmpl, t_pk = bateman(seg / FS - on, tr, td)
        phasic[seg] += a * tmpl
        peak_t[i] = on + t_pk

    artefact = np.zeros(n)
    for _ in range(rng.poisson(artefact_rate * minutes)):
        i0 = rng.integers(0, n)
        w = max(int(round(rng.uniform(0.25, 1.5) * FS)), 1)
        artefact[i0:i0 + w] += rng.choice([-1.0, 1.0]) * rng.uniform(0.2, 1.5)
    x = tonic + phasic + artefact + rng.normal(0, noise_sd, n)
    return Session(x, tonic, phasic, peak_t, amp, aroused)


def make_sessions():
    sessions = {}
    for ci, (cond, (rate, sd)) in enumerate(CONDITIONS.items()):
        cal = [synth_session(np.random.default_rng((SEED, ci, 0, k)), artefact_rate=rate,
                             noise_sd=sd) for k in range(N_CAL)]
        test = [synth_session(np.random.default_rng((SEED, ci, 1, k)), artefact_rate=rate,
                              noise_sd=sd) for k in range(N_TEST)]
        sessions[cond] = (cal, test)
    return sessions


def best_lag_corr(y, ref, max_lag_s=MAX_LAG_S):
    """max over lags L >= 0 of corr(y[n], ref[n-L]); returns (r, lag in s)."""
    best_r, best_l = -1.0, 0
    for L in range(int(max_lag_s * FS) + 1):
        a, b = y[L:], ref[:len(ref) - L]
        if a.std() < 1e-12 or b.std() < 1e-12:
            continue
        r = float(np.corrcoef(a, b)[0, 1])
        if r > best_r:
            best_r, best_l = r, L
    return best_r, best_l / FS


def candidate_peaks(y):
    """Local maxima (>= 1 s apart) and their prominences."""
    pk, _ = find_peaks(y, distance=max(int(round(MIN_PEAK_SEP_S * FS)), 1))
    return pk / FS, peak_prominences(y, pk)[0]


def match_counts(det_t, true_t, is_target, lag, tol=MATCH_TOL_S):
    """Greedy one-to-one matching of detections to true SCR peaks + lag.

    Detections matched to sub-threshold SCRs are neutral (neither TP nor FP).
    Returns (tp, fp, fn).
    """
    det_t = np.asarray(det_t, float)
    expected = np.asarray(true_t, float) + lag
    lo = np.searchsorted(det_t, expected - tol, "left")
    hi = np.searchsorted(det_t, expected + tol, "right")
    pairs = [(abs(det_t[j] - expected[i]), i, j)
             for i in range(len(expected)) for j in range(lo[i], hi[i])]
    pairs.sort()
    used_i, used_j = set(), set()
    tp = neutral = 0
    for _, i, j in pairs:
        if i in used_i or j in used_j:
            continue
        used_i.add(i)
        used_j.add(j)
        if is_target[i]:
            tp += 1
        else:
            neutral += 1
    fp = len(det_t) - tp - neutral
    fn = int(np.sum(is_target)) - tp
    return tp, fp, fn


def f1_score(tp, fp, fn):
    return 2 * tp / (2 * tp + fp + fn) if (tp + fp + fn) else float("nan")


def auc(pos, neg):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    diff = pos[:, None] - neg[None, :]
    return float((diff > 0).mean() + 0.5 * (diff == 0).mean())


def window_features(y, det_t, lag_s, n, label_windows):
    """Per-window SCR count and log phasic power, aligned by the filter lag."""
    shift = int(round(lag_s * FS))
    t_al = np.asarray(det_t) - lag_s
    out = []
    for a, b, lab in label_windows:
        a2, b2 = min(a + shift, n), min(b + shift, n)
        seg = y[a2:b2]
        count = int(np.sum((t_al >= a / FS) & (t_al < b / FS)))
        power = float(np.log10(seg.var() + 1e-12)) if len(seg) > 1 else float("nan")
        out.append((lab, count, power))
    return out


def session_windows(sess):
    w = int(WIN_S * FS)
    n = len(sess.x)
    return [(a, a + w, int(sess.aroused[a])) for a in range(0, n - w + 1, w)]


def calibrate(filters, sessions):
    """Lag (median phasic cross-correlation lag) and threshold (max pooled F1)."""
    ys = [f(s.x) for f, s in zip(filters, sessions)]
    lag = float(np.median([best_lag_corr(y, s.phasic)[1] for y, s in zip(ys, sessions)]))
    cands = [candidate_peaks(y) for y in ys]
    proms = np.concatenate([c[1] for c in cands])
    grid = np.unique(np.quantile(proms, np.linspace(0.5, 0.995, N_THRESH)))
    best = (-1.0, grid[0])
    for th in grid:
        tp = fp = fn = 0
        for (t, p), s in zip(cands, sessions):
            a, b, c = match_counts(t[p >= th], s.peak_t, s.amp >= A_MIN, lag)
            tp, fp, fn = tp + a, fp + b, fn + c
        f1 = f1_score(tp, fp, fn)
        if f1 > best[0]:
            best = (f1, th)
    return lag, float(best[1]), float(best[0])


def evaluate_session(f, sess, lag, th, linear=True):
    y = f(sess.x)
    r, r_lag = best_lag_corr(y, sess.phasic)
    t, p = candidate_peaks(y)
    det = t[p >= th]
    tp, fp, fn = match_counts(det, sess.peak_t, sess.amp >= A_MIN, lag)
    if linear:
        leak = float(f(sess.tonic).var() / max(f(sess.phasic).var(), 1e-12))
    else:
        leak = float("nan")
    feats = window_features(y, det, lag, len(y), session_windows(sess))
    counts = np.array([c for _, c, _ in feats])
    power = np.array([pw for _, _, pw in feats])
    aro = np.array([lab for lab, _, _ in feats]) == 1
    prec = tp / (tp + fp) if tp + fp else float("nan")
    rec = tp / (tp + fn) if tp + fn else float("nan")
    return {"r": r, "r_lag_s": r_lag, "f1": f1_score(tp, fp, fn),
            "precision": prec, "recall": rec, "tonic_leak": leak,
            "auc_count": auc(counts[aro], counts[~aro]),
            "auc_power": auc(power[aro], power[~aro])}


def variants(designs):
    """(design, jitter, label) evaluation variants: devices nominal + jittered."""
    out = []
    for d in designs:
        if d.family == "device":
            out.append((d, JITTER, d.name))
            out.append((d, 0.0, d.name + " (nominal)"))
        else:
            out.append((d, 0.0, d.name))
    return out


def synthetic_benchmark(designs, sessions):
    """Calibrate on N_CAL sessions, score on N_TEST, per condition and variant."""
    summary, per_session, calib = [], {}, {}
    for vi, (d, jit, label) in enumerate(variants(designs)):
        for ci, cond in enumerate(CONDITIONS):
            cal, test = sessions[cond]
            mk = lambda part, k: make_filter(  # noqa: E731
                d, np.random.default_rng((SEED, 7, ci, part, k, vi)), jit)
            lag, th, cal_f1 = calibrate([mk(0, k) for k in range(len(cal))], cal)
            res = [evaluate_session(mk(1, k), s, lag, th) for k, s in enumerate(test)]
            per_session[(label, cond)] = res
            calib[(label, cond)] = (lag, th, cal_f1)
            row = {"variant": label, "family": d.family, "topology": d.topology,
                   "jitter": jit, "condition": cond, "lag_s": lag, "threshold": th,
                   "cal_f1": round(cal_f1, 4)}
            for key in ("r", "r_lag_s", "f1", "precision", "recall", "tonic_leak",
                        "auc_count", "auc_power"):
                vals = np.array([z[key] for z in res], float)
                row[f"{key}_mean"] = round(float(np.nanmean(vals)), 4)
                row[f"{key}_sd"] = round(float(np.nanstd(vals)), 4)
            summary.append(row)
    return summary, per_session, calib


class _Oracle:
    """Pseudo-filter that returns the session's true phasic component."""

    def __init__(self, sess):
        self.sess = sess

    def __call__(self, x):
        return self.sess.phasic.copy()


def oracle_benchmark(sessions):
    """Detection on the true phasic signal: the ceiling for any filter."""
    rows = {}
    for cond in CONDITIONS:
        cal, test = sessions[cond]
        lag, th, _ = calibrate([_Oracle(s) for s in cal], cal)
        rows[cond] = [evaluate_session(_Oracle(s), s, lag, th, linear=False) for s in test]
    return rows


def paired_signs(a, b, key="f1"):
    """Mean difference and sign count of per-session a - b."""
    d = np.array([x[key] - y[key] for x, y in zip(a, b)], float)
    return float(np.nanmean(d)), int(np.sum(d > 0)), int(np.sum(np.isfinite(d)))


# ----------------------------------------------------------------------------
# E3: WESAD raw EDA
# ----------------------------------------------------------------------------
def load_wesad_eda(cache=True):
    """{sid: (chest uS @4 Hz, chest labels, wrist uS @4 Hz, wrist labels)}.

    Chest EDA (700 Hz) is reduced by a causal block mean over each 0.25 s; the
    label is the last label of the block. Wrist EDA is the native 4 Hz stream.
    """
    paths = sorted(glob.glob(os.path.join(WESAD_DIR, "S*", "S*.pkl")))
    if not paths:
        return {}
    signature = _source_signature(paths)
    fields = ("chest", "chest_lab", "wrist", "wrist_lab")
    if cache and os.path.exists(WESAD_CACHE):
        z = np.load(WESAD_CACHE, allow_pickle=False)
        if (str(z["__schema__"].item()) == WESAD_SCHEMA
                and str(z["__signature__"].item()) == signature):
            sids = [str(s) for s in z["__sids__"]]
            print(f"  (loaded {len(sids)} subjects from {WESAD_CACHE})")
            return {s: tuple(z[f"{s}_{k}"] for k in fields) for s in sids}
    raw = {}
    for pkl in paths:
        sid = os.path.basename(pkl).split(".")[0]
        with open(pkl, "rb") as fh:
            d = pickle.load(fh, encoding="latin1")
        block = int(700 / FS)
        chest = np.asarray(d["signal"]["chest"]["EDA"], float).ravel()
        lab = np.asarray(d["label"]).ravel()
        nb = len(chest) // block
        chest4 = chest[:nb * block].reshape(nb, block).mean(axis=1)
        chest_lab = lab[(np.arange(nb) + 1) * block - 1]
        wrist = np.asarray(d["signal"]["wrist"]["EDA"], float).ravel()
        wrist_lab = _resample_labels(lab, len(wrist))
        raw[sid] = (chest4, chest_lab.astype(int), wrist, wrist_lab.astype(int))
        print(f"  loaded {sid}: chest {len(chest4)} / wrist {len(wrist)} samples")
    if cache:
        flat = {"__schema__": np.array(WESAD_SCHEMA), "__signature__": np.array(signature),
                "__sids__": np.array(list(raw))}
        for sid, vals in raw.items():
            for k, v in zip(fields, vals):
                flat[f"{sid}_{k}"] = v
        np.savez_compressed(WESAD_CACHE, **flat)
        print(f"  (cached {len(raw)} subjects -> {WESAD_CACHE})")
    return raw


def label_windows(lab, labels=(1, 2, 3)):
    """Non-overlapping WIN_S windows fully inside one labelled protocol segment."""
    w = int(WIN_S * FS)
    bounds = np.r_[0, np.flatnonzero(np.diff(lab)) + 1, len(lab)]
    out = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        if int(lab[a]) in labels:
            out.extend((s, s + w, int(lab[a])) for s in range(a, b - w + 1, w))
    return out


def wesad_benchmark(designs, raw, calib):
    """Per-subject stress-vs-baseline AUC and agreement with the digital reference."""
    ref_name = "digital phasic 0.05-1 Hz"
    per_subject = {}
    sids = sorted(raw, key=lambda s: int(s[1:]))
    for vi, (d, jit, label) in enumerate(variants(designs)):
        lag, th, _ = calib[(label, "clean")]
        for site_i, site in enumerate(("chest", "wrist")):
            rows = []
            for si, sid in enumerate(sids):
                x, lab = raw[sid][2 * site_i], raw[sid][2 * site_i + 1]
                f = make_filter(d, np.random.default_rng((SEED, 11, site_i, si, vi)), jit)
                y = f(x)
                t, p = candidate_peaks(y)
                wins = label_windows(lab)
                feats = window_features(y, t[p >= th], lag, len(y), wins)
                labs = np.array([z[0] for z in feats])
                cnt = np.array([z[1] for z in feats], float)
                pw = np.array([z[2] for z in feats], float)
                scl = np.array([x[a:b].mean() for a, b, _ in wins])
                rows.append({"sid": sid, "labels": labs, "count": cnt, "power": pw,
                             "scl": scl,
                             "auc_power": auc(pw[labs == 2], pw[labs == 1]),
                             "auc_count": auc(cnt[labs == 2], cnt[labs == 1]),
                             "auc_scl": auc(scl[labs == 2], scl[labs == 1])})
            per_subject[(label, site)] = rows
    summary = []
    for (label, site), rows in per_subject.items():
        ref = per_subject[(ref_name, site)]
        agree = [spearmanr(a["power"], b["power"])[0] for a, b in zip(rows, ref)]
        row = {"variant": label, "site": site,
               "n_subjects": len(rows),
               "auc_power_mean": np.mean([z["auc_power"] for z in rows]),
               "auc_power_sd": np.std([z["auc_power"] for z in rows]),
               "auc_count_mean": np.nanmean([z["auc_count"] for z in rows]),
               "auc_count_sd": np.nanstd([z["auc_count"] for z in rows]),
               "agreement_rho_vs_ref": np.nanmean(agree),
               "auc_scl_mean": np.mean([z["auc_scl"] for z in rows])}
        diff = np.array([a["auc_power"] - b["auc_power"] for a, b in zip(rows, ref)])
        row["auc_power_minus_ref"] = float(np.mean(diff))
        row["auc_power_minus_ref_pos"] = int(np.sum(diff > 0))
        row["auc_power_minus_ref_p"] = (float(wilcoxon(diff).pvalue)
                                        if np.any(np.abs(diff) > 1e-12) else float("nan"))
        summary.append({k: (round(v, 4) if isinstance(v, float) else v)
                        for k, v in row.items()})
    return summary, per_subject


def paired_wilcoxon(rows_a, rows_b, key):
    d = np.array([a[key] - b[key] for a, b in zip(rows_a, rows_b)], float)
    p = float(wilcoxon(d).pvalue) if np.any(np.abs(d) > 1e-12) else float("nan")
    return float(np.mean(d)), int(np.sum(d > 0)), len(d), p


# ----------------------------------------------------------------------------
# E4: Tier-2 drive sensitivity
# ----------------------------------------------------------------------------
def tier2_sensitivity(selected, sessions):
    rows = []
    cal, test = sessions["clean"]
    modes = [("linearised", 1.0)] + [(ro, u) for ro in ("dc", "ac") for u in TIER2_DRIVES]
    for vi, d in enumerate(selected):
        for readout, drive in modes:
            mk = lambda part, k: make_tier2_filter(  # noqa: E731
                d, drive, np.random.default_rng((SEED, 13, part, k, vi)), JITTER,
                readout=readout)
            lag, th, cal_f1 = calibrate([mk(0, k) for k in range(len(cal))], cal)
            filters = [mk(1, k) for k in range(len(test))]
            res = [evaluate_session(f, s, lag, th, linear=False)
                   for f, s in zip(filters, test)]
            sat = max(f.state["max_progress"] for f in filters)
            mode = readout if readout == "linearised" else f"{readout} read-out, drive {drive:g}"
            rows.append({"design": d.name, "tier2_mode": mode, "lag_s": lag,
                         "cal_f1": round(cal_f1, 4),
                         "f1_mean": round(float(np.mean([z["f1"] for z in res])), 4),
                         "f1_sd": round(float(np.std([z["f1"] for z in res])), 4),
                         "r_mean": round(float(np.mean([z["r"] for z in res])), 4),
                         "auc_power_mean": round(float(np.mean([z["auc_power"] for z in res])), 4),
                         "max_progress": round(sat, 4)})
    return rows


# ----------------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------------
def write_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path}")


def make_figure(freqs, designs_by_name, picks, sessions, calib, synth_rows, ds_rows,
                wesad_rows):
    import matplotlib.pyplot as plt
    import figstyle
    figstyle.apply()
    C = figstyle.COLORS
    fig, axes = plt.subplots(2, 2, figsize=(7.4, 5.9))

    # (a) design space
    ax = axes[0, 0]
    ax.axvspan(*EDASYMP_BAND, color=C["light"], zorder=0)
    ax.text(math.sqrt(EDASYMP_BAND[0] * EDASYMP_BAND[1]), 1.42, "EDASymp\nband",
            ha="center", va="top", fontsize=6.5, color=C["gray"])
    curves = [(picks["ref"], C["gray"], "-", "digital phasic"),
              (picks["dev_hp"], C["orange"], "-", "device HP (fastest cell)"),
              (picks["rc_hp"], C["blue"], (0, (2, 2)), "RC twin"),
              (picks["slow_hp"], C["purple"], ":", "device HP (lead cell)"),
              (picks["dev_bp"], C["green"], "-", "device BP")]
    for name, col, ls, lab in curves:
        ax.plot(freqs, frequency_response(designs_by_name[name], freqs), color=col,
                ls=ls, lw=1.3, label=lab)
    corners = [r["band_lo_hz"] for r in ds_rows
               if r["family"] == "device" and r["topology"] == "HP"]
    ax.plot(corners, np.full(len(corners), 1.53), "|", color=C["orange"], ms=6, mew=1.0)
    ax.text(min(corners) * 0.8, 1.53, "8 device HP\ncorners", ha="right", va="center",
            fontsize=6.3, color=C["orange"])
    ax.set_xscale("log")
    ax.set_xlim(1e-3, 2.0)
    ax.set_ylim(0, 1.62)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("|H(f)|")
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.88), fontsize=6.3)
    figstyle.panel(ax, "a", "Frequency response")

    # (b) example trace (direct labels)
    ax = axes[0, 1]
    sess = sessions["clean"][1][0]
    a, b = int(5 * 60 * FS), int(8 * 60 * FS)
    t = np.arange(a, b) / FS / 60.0
    ax.plot(t, sess.phasic[a:b] / sess.phasic[a:b].max(), color="k", lw=1.0)
    ax.text(t[-1] + 0.05, 0.1, "true\nphasic", fontsize=6.5, va="bottom")
    offset = 1.25
    for i, (name, col, lab) in enumerate([(picks["dev_hp"], C["orange"], "device\nHP"),
                                          (picks["rc_hp"], C["blue"], "RC\ntwin"),
                                          (picks["ref"], C["gray"], "digital\nphasic")]):
        lag = calib[(name, "clean")][0]
        f = make_filter(designs_by_name[name], np.random.default_rng((SEED, 99, i)),
                        JITTER if designs_by_name[name].family == "device" else 0.0)
        y = f(sess.x)
        sh = int(round(lag * FS))
        seg = y[a + sh:b + sh]
        seg = (seg - np.median(seg)) / (np.abs(seg).max() + 1e-12)
        ax.plot(t, seg - offset * (i + 1), color=col, lw=1.0)
        ax.text(t[-1] + 0.05, -offset * (i + 1), lab, color=col, fontsize=6.5, va="center")
    pk = sess.peak_t[(sess.peak_t >= a / FS) & (sess.peak_t < b / FS) & (sess.amp >= A_MIN)]
    ax.plot(pk / 60.0, np.full(len(pk), 1.12), "v", color="k", ms=3)
    ax.set_xlim(t[0], t[-1] + 0.45)
    ax.set_yticks([])
    ax.set_xlabel("time (min); traces peak-normalised, lag-aligned")
    ax.spines["left"].set_visible(False)
    figstyle.panel(ax, "b", "Synthetic aroused block")

    # (c) synthetic detection F1
    ax = axes[1, 0]
    bars = [("digital", picks["ref"], C["gray"]),
            ("device HP", picks["dev_hp"], C["orange"]), ("RC HP", picks["rc_hp"], C["blue"]),
            ("device BP", picks["dev_bp"], C["green"]), ("RC BP", picks["rc_bp"], C["blue"]),
            ("raw", "raw signal", C["gray"])]
    by = {(r["variant"], r["condition"]): r for r in synth_rows}
    width = 0.27
    shades = (1.0, 0.65, 0.35)
    for ci, cond in enumerate(CONDITIONS):
        xs = np.arange(len(bars)) + (ci - 1) * width
        ax.bar(xs, [by[(n, cond)]["f1_mean"] for _, n, _ in bars], width,
               yerr=[by[(n, cond)]["f1_sd"] for _, n, _ in bars], capsize=1.5,
               error_kw={"lw": 0.6}, color=[c for _, _, c in bars], alpha=shades[ci],
               label=cond, edgecolor="none")
    ax.set_xticks(np.arange(len(bars)))
    ax.set_xticklabels([b[0] for b in bars], rotation=30, ha="right")
    ax.set_ylim(0, 1)
    ax.set_ylabel("SCR detection F1 (30 test sessions)")
    ax.legend(loc="upper right", fontsize=6.5, ncol=3)
    figstyle.panel(ax, "c", "Synthetic ground truth")

    # (d) WESAD stress vs baseline
    ax = axes[1, 1]
    wb = {(r["variant"], r["site"]): r for r in wesad_rows}
    wbars = [("digital", picks["ref"], C["gray"]),
             ("EDASymp", picks["edasymp"], C["gray"]),
             ("device HP", picks["dev_hp"], C["orange"]), ("RC HP", picks["rc_hp"], C["blue"]),
             ("device BP", picks["dev_bp"], C["green"]), ("RC BP", picks["rc_bp"], C["blue"])]
    width = 0.38
    for si, site in enumerate(("chest", "wrist")):
        xs = np.arange(len(wbars)) + (si - 0.5) * width
        ax.bar(xs, [wb[(n, site)]["auc_power_mean"] for _, n, _ in wbars], width,
               yerr=[wb[(n, site)]["auc_power_sd"] for _, n, _ in wbars], capsize=1.5,
               error_kw={"lw": 0.6}, color=[c for _, _, c in wbars],
               alpha=1.0 if si == 0 else 0.45, label=f"{site} phasic power",
               edgecolor="none")
    for si, site in enumerate(("chest", "wrist")):
        ax.axhline(wb[(picks["ref"], site)]["auc_scl_mean"], color=C["red"], lw=0.8,
                   ls="--" if si == 0 else ":", label=f"{site} tonic SCL")
    ax.axhline(0.5, color=C["gray"], lw=0.6)
    ax.set_xticks(np.arange(len(wbars)))
    ax.set_xticklabels([b[0] for b in wbars], rotation=30, ha="right")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("stress vs baseline AUC (within subject)")
    leg = ax.legend(loc="lower center", fontsize=6.3, ncol=2, frameon=True)
    leg.get_frame().set_facecolor("white")
    leg.get_frame().set_edgecolor("none")
    leg.get_frame().set_alpha(0.92)
    figstyle.panel(ax, "d", "WESAD, 15 subjects")

    fig.tight_layout()
    figstyle.save(fig, FIG)


def device_vs_rc(cells, per_session, per_subject):
    """Per cell: does the measured stretched kernel differ from an RC filter at the
    same half-life? Nominal (unjittered) devices isolate kernel shape."""
    rows = []
    for c in sorted(cells, key=lambda z: z.t_half):
        dev = f"device HP {cell_label(c)} (nominal)"
        rc = f"rc HP {cell_label(c)}"
        row = {"cell": cell_label(c), "t_half_s": round(c.t_half, 2), "beta": round(c.beta, 2)}
        for cond in CONDITIONS:
            m, k, n = paired_signs(per_session[(dev, cond)], per_session[(rc, cond)])
            row[f"dF1_{cond}"] = round(m, 4)
            row[f"dF1_{cond}_pos"] = f"{k}/{n}"
        if per_subject:
            for site in ("chest", "wrist"):
                m, k, n, p = paired_wilcoxon(per_subject[(dev, site)], per_subject[(rc, site)],
                                             "auc_power")
                row[f"dAUC_{site}"] = round(m, 4)
                row[f"dAUC_{site}_pos"] = f"{k}/{n}"
                row[f"dAUC_{site}_p"] = round(p, 4) if p == p else p
        rows.append(row)
    return rows


def main():
    cells = _full(load_cards(li_only=True))
    designs = build_designs(cells)
    by_name = {d.name: d for d in designs}
    print(f"{len(cells)} composition cells -> {len(designs)} designs")

    # E1
    ds_rows, freqs = design_space(designs)
    write_csv(os.path.join(OUT, "ch5_filterbank_design.csv"), ds_rows)
    cards_rows = component_cards(cells)
    write_csv(os.path.join(OUT, "ch5_component_cards.csv"), cards_rows)
    for r in cards_rows:
        print(f"  {r['cell']:14s} t1/2 {r['t_half_s']:5.2f} s  beta {r['beta']:.2f}  "
              f"f_c device {r['f_corner_device_hz']:.4f} Hz  RC {r['f_corner_rc_hz']:.4f} Hz")

    # E2
    sessions = make_sessions()
    synth_rows, per_session, calib = synthetic_benchmark(designs, sessions)
    oracle = oracle_benchmark(sessions)

    def best(family, topology):
        """Design with the highest calibration F1 averaged over conditions."""
        rows = [r for r in synth_rows if r["family"] == family and r["topology"] == topology
                and not r["variant"].endswith("(nominal)")]
        score = {}
        for r in rows:
            score.setdefault(r["variant"], []).append(r["cal_f1"])
        return max(score, key=lambda v: np.mean(score[v]))

    dev_hp, dev_bp = best("device", "HP"), best("device", "BP")
    picks = {"ref": "digital phasic 0.05-1 Hz", "edasymp": "digital EDASymp 0.045-0.25 Hz",
             "dev_hp": dev_hp, "rc_hp": by_name[dev_hp].twin("rc").name,
             "dev_bp": dev_bp, "rc_bp": by_name[dev_bp].twin("rc").name,
             "best_rc_hp": best("rc", "HP"), "best_rc_bp": best("rc", "BP"),
             "slow_hp": "device HP PEO0.3/0.09"}
    for cond in CONDITIONS:
        orc = np.array([z["f1"] for z in oracle[cond]])
        print(f"\n[{cond}] noise-free phasic F1 {orc.mean():.3f} +/- {orc.std():.3f}")
        for key in ("ref", "dev_hp", "rc_hp", "dev_bp", "rc_bp", "best_rc_hp", "slow_hp"):
            name = picks[key]
            r = next(z for z in synth_rows if z["variant"] == name and z["condition"] == cond)
            print(f"  {key:10s} {name:42s} F1 {r['f1_mean']:.3f}+/-{r['f1_sd']:.3f} "
                  f"r {r['r_mean']:.3f} leak {r['tonic_leak_mean']:.3f} "
                  f"AUCcount {r['auc_count_mean']:.3f} AUCpow {r['auc_power_mean']:.3f} "
                  f"lag {r['lag_s']:.2f}s")
        for a, b in (("dev_hp", "rc_hp"), ("dev_hp", "ref"), ("dev_bp", "rc_bp")):
            m, k, n = paired_signs(per_session[(picks[a], cond)], per_session[(picks[b], cond)])
            print(f"  {a} - {b}: dF1 {m:+.3f} ({k}/{n} sessions positive)")
    for r in synth_rows:
        r["is_selected"] = r["variant"] in picks.values()
    for cond, res in oracle.items():
        row = {"variant": "noise-free phasic (no filter)", "family": "reference",
               "topology": "NONE", "jitter": 0.0, "condition": cond, "is_selected": False}
        for key in ("r", "f1", "precision", "recall", "auc_count", "auc_power"):
            vals = np.array([z[key] for z in res], float)
            row[f"{key}_mean"] = round(float(np.nanmean(vals)), 4)
            row[f"{key}_sd"] = round(float(np.nanstd(vals)), 4)
        synth_rows.append(row)
    write_csv(os.path.join(OUT, "ch5_filterbank_synthetic.csv"), synth_rows)

    # E4
    t2 = tier2_sensitivity([by_name[dev_hp], by_name[dev_bp]], sessions)
    write_csv(os.path.join(OUT, "ch5_filterbank_tier2.csv"), t2)
    print("\nTier 2 (composed node), clean synthetic:")
    for r in t2:
        print(f"  {r['design']:42s} {r['tier2_mode']:26s} F1 {r['f1_mean']:.3f} "
              f"r {r['r_mean']:.3f} AUCpow {r['auc_power_mean']:.3f} "
              f"max p {r['max_progress']:.3f}")

    # E3
    raw = load_wesad_eda()
    if not raw:
        print("\nWESAD not found under data/wesad/WESAD; skipping E3 and the figure.")
        write_csv(os.path.join(OUT, "ch5_filterbank_device_vs_rc.csv"),
                  device_vs_rc(cells, per_session, {}))
        return
    wesad_rows, per_subject = wesad_benchmark(designs, raw, calib)
    write_csv(os.path.join(OUT, "ch5_filterbank_wesad.csv"), wesad_rows)
    print("\nWESAD stress vs baseline (phasic power AUC, per-subject mean):")
    for site in ("chest", "wrist"):
        for key in ("ref", "edasymp", "dev_hp", "rc_hp", "dev_bp", "rc_bp", "slow_hp"):
            r = next(z for z in wesad_rows if z["variant"] == picks[key] and z["site"] == site)
            print(f"  {site:5s} {key:8s} AUCpow {r['auc_power_mean']:.3f}+/-{r['auc_power_sd']:.3f} "
                  f"AUCcount {r['auc_count_mean']:.3f} rho_ref {r['agreement_rho_vs_ref']:.3f} "
                  f"(SCL AUC {r['auc_scl_mean']:.3f})")
        for a, b in (("dev_hp", "rc_hp"), ("dev_bp", "rc_bp"), ("dev_hp", "ref")):
            m, k, n, p = paired_wilcoxon(per_subject[(picks[a], site)],
                                         per_subject[(picks[b], site)], "auc_power")
            print(f"  {site:5s} {a} - {b}: dAUC {m:+.3f} ({k}/{n} subjects) Wilcoxon p={p:.3g}")

    dvr = device_vs_rc(cells, per_session, per_subject)
    write_csv(os.path.join(OUT, "ch5_filterbank_device_vs_rc.csv"), dvr)
    print("\nMeasured stretched kernel vs RC at the same half-life (HP, nominal devices):")
    for r in dvr:
        print(f"  {r['cell']:14s} t1/2 {r['t_half_s']:5.2f} beta {r['beta']:.2f} | dF1 "
              + " ".join(f"{c} {r[f'dF1_{c}']:+.3f} ({r[f'dF1_{c}_pos']})" for c in CONDITIONS)
              + " | dAUC chest {:+.3f} ({}) p={} wrist {:+.3f} ({}) p={}".format(
                  r["dAUC_chest"], r["dAUC_chest_pos"], r["dAUC_chest_p"],
                  r["dAUC_wrist"], r["dAUC_wrist_pos"], r["dAUC_wrist_p"]))

    make_figure(freqs, by_name, picks, sessions, calib, synth_rows, ds_rows, wesad_rows)


if __name__ == "__main__":
    main()
