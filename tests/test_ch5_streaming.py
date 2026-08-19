import sys
from pathlib import Path

import numpy as np


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import ch5_case as case  # noqa: E402
import ch5_onset as onset  # noqa: E402
import ch5_wesad as wesad  # noqa: E402
from ch5_model import load_cards  # noqa: E402
from ch5_reservoir import ReservoirNode  # noqa: E402


def test_prefix_scaling_is_unchanged_by_future_samples():
    prefix = np.linspace(0.0, 1.0, 20)[:, None]
    future_a = np.full((20, 1), 2.0)
    future_b = np.full((20, 1), 2000.0)
    a = wesad._scale_subject(np.vstack([prefix, future_a]), fs=1.0, calibration_s=20)
    b = wesad._scale_subject(np.vstack([prefix, future_b]), fs=1.0, calibration_s=20)
    assert np.allclose(a[:20], b[:20])
    assert np.all((b > 0.0) & (b < 1.0))
    assert b[-1, 0] > a[-1, 0]


def test_versioned_cache_rejects_wrong_source_signature(tmp_path):
    path = tmp_path / "streams.npz"
    raw = {"S1": (np.ones((3, 1)), np.array([1, 2, 1]))}
    wesad._save_stream_cache(str(path), "source-a", raw)
    assert wesad._load_stream_cache(str(path), "source-a") is not None
    assert wesad._load_stream_cache(str(path), "source-b") is None


def test_causal_hold_does_not_use_the_next_rr_interval():
    grid = np.array([0.0, 1.0, 2.0, 3.0])
    held = wesad._causal_hold(grid, [1.5, 2.5], [80.0, 120.0], default=70.0)
    assert np.array_equal(held, [70.0, 70.0, 80.0, 120.0])


def test_stream_resampling_keeps_feature_and_label_lengths_equal():
    U = np.arange(31 * 2, dtype=float).reshape(31, 2)
    labels = np.ones(31, dtype=int)
    for dt in (0.5, 1.0, 2.0, 4.0):
        Us, ls = wesad.stream_subject(U, labels, dt)
        assert len(Us) == len(ls)


def test_binary_loso_retains_unlabelled_timeline_gaps():
    labels = np.array([1, 1, 0, 0, 2, 2, 1, 1])
    score = labels != 0
    x = (labels == 2).astype(float)[:, None]
    feats = {f"S{i}": (x + i * 1e-4, labels, score) for i in range(3)}
    _, per = onset.loso_binary(feats, smooth=3)
    for full_labels, pred, full_score in per.values():
        assert len(full_labels) == len(labels)
        assert len(pred) == len(labels)
        assert np.array_equal(full_score, score)


def test_classification_ridge_is_invariant_to_dataset_duplication():
    F = np.array([[0.0], [0.2], [0.8], [1.0]])
    y = np.array([0, 0, 1, 1])
    W1 = wesad._ridge_onehot_fit(F, y, [0, 1])
    W2 = wesad._ridge_onehot_fit(np.tile(F, (3, 1)), np.tile(y, 3), [0, 1])
    assert np.allclose(W1, W2)


def test_onset_metric_counts_stress_segments_separated_by_unlabelled_time():
    labels = np.array([1, 2, 2, 0, 0, 2, 2, 1])
    score = labels != 0
    pred = (labels == 2).astype(int)
    latency, n_onsets = onset.onset_latency(
        {"S1": (labels, pred, score)}, dt=1.0, stable_s=2.0
    )
    assert n_onsets == 2
    assert latency == 0.0


def test_case_per_channel_bank_uses_bounded_nodes_and_one_hot_masks():
    nodes = case._build_nodes("heterogeneous_perchan", load_cards(li_only=True), seed=3)
    assert all(isinstance(node, ReservoirNode) for node in nodes)
    assert all(np.count_nonzero(node.w) == 1 for node in nodes)
