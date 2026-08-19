import sys
from pathlib import Path

import numpy as np


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from ch5_model import lead_card, load_cards  # noqa: E402
from ch5_reservoir import (  # noqa: E402
    DEFAULT_JITTER,
    ReservoirNode,
    _full,
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
