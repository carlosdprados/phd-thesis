import math
import sys
from pathlib import Path

import numpy as np


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from ch5_filterbank import (  # noqa: E402
    A_MIN,
    EDASYMP_BAND,
    FS,
    NOISE_SD,
    RATES,
    build_designs,
    causal_filter,
    composed_progress,
    design_space,
    make_filter,
    make_tier2_filter,
    match_counts,
    relaxation_kernel,
    synth_session,
)
from ch5_model import load_cards  # noqa: E402
from ch5_reservoir import ReservoirNode, _full, run_states  # noqa: E402


def _cells():
    return _full(load_cards(li_only=True))


def test_relaxation_kernels_reproduce_measured_half_time_for_stretched_cells():
    for card in _cells():
        k = relaxation_kernel(card.tau, card.beta, normalise=False)
        t = np.arange(len(k)) / FS
        t_half = float(np.interp(0.5, k[::-1], t[::-1]))
        assert abs(t_half - card.t_half) < 1.0 / FS


def test_filters_are_causal_and_reject_a_constant_input():
    designs = build_designs(_cells())
    x = np.full(800, 7.5)
    for d in designs:
        if d.topology in {"HP", "BP", "BAND"}:
            assert np.allclose(make_filter(d)(x), 0.0, atol=1e-9), d.name
    k = relaxation_kernel(4.0, 0.8)
    impulse = np.zeros(400)
    impulse[200] = 1.0
    y = causal_filter(impulse, k)
    assert np.allclose(y[:200], 0.0)
    assert np.isclose(y[200], k[0])


def test_composed_node_reduces_to_bounded_chapter5_node_for_simple_exponential():
    tau, alpha, peak, n_peak = 6.0, 0.6, 20.0, 300.0
    rng = np.random.default_rng(4)
    u = np.r_[0.0, rng.uniform(0.0, 0.6, 600)]
    node = ReservoirNode(decay=math.exp(-1.0 / (FS * tau)), alpha=alpha, w=1.0,
                         peak_ratio=peak, n_peak=n_peak)
    reference = run_states([node], u)[:, 0]
    p, x = composed_progress(u, tau, 1.0, alpha, n_peak)
    assert p.max() < 1.0
    assert np.allclose(1.0 + (peak - 1.0) * x, reference, rtol=1e-3, atol=1e-6)


def test_composed_single_write_decays_as_the_measured_relaxation():
    card = next(c for c in _cells() if c.beta < 0.7)
    u = np.zeros(int(200 * FS))
    u[1] = 1.0
    _, x = composed_progress(u, card.tau, card.beta, card.alpha, card.n_peak)
    t = (np.arange(len(u)) - 1) / FS
    decay = x[1:] / x[1]
    t_half = float(np.interp(0.5, decay[::-1], t[1:][::-1]))
    assert abs(t_half - card.t_half) < 1.0 / FS


def test_synthetic_session_has_consistent_ground_truth():
    s = synth_session(np.random.default_rng(11), minutes=20.0)
    assert np.all(s.phasic >= 0)
    assert np.all((s.peak_t >= 0) & (s.peak_t < len(s.x) / FS))
    resid = s.x - s.tonic - s.phasic
    assert abs(resid.std() - NOISE_SD) < 0.2 * NOISE_SD
    idx = np.clip((s.peak_t * FS).astype(int), 0, len(s.x) - 1)
    aroused = s.aroused[idx]
    # aroused blocks carry the higher nominal rate (equal block time in 20 min)
    assert aroused.sum() > (~aroused).sum()
    assert RATES[1] > RATES[0]
    assert np.any(s.amp >= A_MIN)


def test_match_counts_scores_hits_misses_and_neutral_detections():
    true_t = np.array([10.0, 30.0, 50.0])
    target = np.array([True, True, False])
    assert match_counts(true_t + 0.5, true_t, target, lag=0.0) == (2, 0, 0)
    assert match_counts(true_t + 5.0, true_t, target, lag=0.0) == (0, 3, 2)
    assert match_counts(true_t + 5.0, true_t, target, lag=5.0) == (2, 0, 0)


def test_tier2_ac_readout_is_drive_invariant_below_saturation():
    card = _cells()[0]
    design = next(d for d in build_designs([card]) if d.family == "device")
    x = synth_session(np.random.default_rng(5), minutes=10.0).x
    lo = make_tier2_filter(design, 0.05, readout="ac")
    hi = make_tier2_filter(design, 0.5, readout="ac")
    y_lo, y_hi = lo(x), hi(x)
    assert hi.state["max_progress"] < 1.0
    assert np.allclose(y_lo, y_hi, rtol=1e-6, atol=1e-9)


def test_every_device_highpass_corner_lies_below_the_edasymp_band():
    rows, _ = design_space(build_designs(_cells()))
    corners = [r["band_lo_hz"] for r in rows
               if r["family"] == "device" and r["topology"] == "HP"]
    assert len(corners) == len(_cells())
    assert max(corners) < EDASYMP_BAND[0]
