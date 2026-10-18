import sys
from pathlib import Path

import numpy as np


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from ch5_model import lead_card, load_cards  # noqa: E402
from ch5_deployment import E_EVENT_MEDIAN_J, envelope  # noqa: E402
from ch5_reservoir import (  # noqa: E402
    DEFAULT_JITTER,
    ReservoirNode,
    _bounded_progress,
    _full,
    kww_modes,
    node_modes,
    memoryless_nodes,
    nodes_from,
    run_states,
)


def test_parameter_cards_reproduce_model_free_half_time():
    cards = load_cards(li_only=True)
    for card in cards:
        assert np.isclose(card.decay_factor(card.t_half), 0.5, atol=1e-10)


def test_quantitative_bank_excludes_exploratory_low_peo_card():
    cards = _full(load_cards(li_only=True))
    assert cards
    assert {card.peo for card in cards} <= {"0.3", "0.6", "1.2"}
    assert all(card.peo != "0.15" for card in cards)


def test_bounded_node_hits_measured_peak_without_leakage():
    node = ReservoirNode(
        decay=1.0, alpha=0.5, w=1.0, peak_ratio=10.0, n_peak=4.0
    )
    states = run_states([node], np.ones(12))[:, 0]
    assert np.isclose(states[3], 10.0)
    assert np.all(states >= 1.0)
    assert np.all(states <= 10.0)
    assert np.all(np.diff(states) >= -1e-12)


def test_zero_input_leaks_a_written_state():
    node = ReservoirNode(
        decay=0.5, alpha=1.0, w=1.0, peak_ratio=5.0, n_peak=1.0
    )
    states = run_states([node], np.array([1.0, 0.0, 0.0]))[:, 0]
    assert np.allclose(states, [5.0, 3.0, 2.0])


def test_default_variability_jitters_timescale_only():
    card = lead_card(load_cards(li_only=True))
    nodes = nodes_from([card], 8, np.random.default_rng(3))
    assert DEFAULT_JITTER == 0.264
    assert {node.alpha for node in nodes} == {card.alpha}
    assert {node.peak_ratio for node in nodes} == {card.peak_ratio}
    assert {node.n_peak for node in nodes} == {card.n_peak}
    assert len({round(node.decay, 12) for node in nodes}) > 1


def test_memoryless_control_preserves_write_parameters():
    card = lead_card(load_cards(li_only=True))
    node = nodes_from([card], 1, np.random.default_rng(4))[0]
    control = memoryless_nodes([node])[0]
    assert control.decay == 0.0
    assert control.alpha == node.alpha
    assert control.w == node.w
    assert control.peak_ratio == node.peak_ratio
    assert control.n_peak == node.n_peak


def test_deployment_counts_and_reference_energy_are_exact():
    result = envelope(N=24, n_classes=3)

    assert result["train_params"] == 75
    assert result["readout_macs"] == 72
    assert np.isclose(result["e_step_J"], 24 * E_EVENT_MEDIAN_J)
    assert result["e_step_range_J"][0] < result["e_step_J"]
    assert result["e_step_J"] < result["e_step_range_J"][1]


def test_relaxation_modes_reproduce_the_stretched_exponential():
    t = np.linspace(0.0, 40.0, 2001)
    for beta in (0.61, 0.64, 0.83, 0.97, 1.0):
        c, theta = kww_modes(beta)
        approx = (c[None, :] * np.exp(-t[:, None] / theta[None, :])).sum(axis=1)
        assert np.isclose(c.sum(), 1.0)
        assert np.max(np.abs(approx - np.exp(-t ** beta))) < 2e-3


def test_node_free_decay_follows_the_measured_kernel_at_any_step():
    for card in _full(load_cards(li_only=True)):
        for dt in (1.0, 5.0):
            node = nodes_from([card], 1, np.random.default_rng(0), jitter=0.0, dt=dt)[0]
            n = int(20 * card.t_half / dt) + 5
            u = np.zeros(n)
            u[0] = 1.0
            g = run_states([node], u)[:, 0] - 1.0
            t = np.arange(n) * dt
            assert np.allclose(g / g[0], card.decay_factor(t), atol=2e-3), (card.cell, dt)


def test_fast_bank_update_matches_the_bounded_recursion():
    rng = np.random.default_rng(12)
    nodes = nodes_from(_full(load_cards(li_only=True)), 16, rng, dt=1.0)
    nodes.append(ReservoirNode(decay=0.99, alpha=0.5, w=1.0, peak_ratio=10.0, n_peak=3.0))
    u = rng.uniform(0.0, 1.0, 400)
    states = run_states(nodes, u)
    for i, node in enumerate(nodes):
        c, a = node_modes(node)
        d = np.clip(np.atleast_1d(node.w)[0] * u, 0.0, 1.0) / node.n_peak
        p = _bounded_progress(c, a, d)
        ref = 1.0 + (node.peak_ratio - 1.0) * np.power(p, node.alpha)
        assert np.allclose(states[:, i], ref, rtol=1e-3, atol=1e-9)
