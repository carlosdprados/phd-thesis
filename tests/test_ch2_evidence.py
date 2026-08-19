import sys
from pathlib import Path

import numpy as np


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from ch2_figures import fit_stdp_branch  # noqa: E402


def test_stdp_branches_are_fitted_independently_from_the_measured_mean():
    delay = np.arange(-0.6, 0.65, 0.05)
    response = np.zeros_like(delay)
    left = delay < 0
    right = delay > 0
    response[left] = 32.0 * np.exp(-np.abs(delay[left]) / 0.09) + 0.4
    response[right] = -15.0 * np.exp(-delay[right] / 0.15) + 0.8

    potentiation, _ = fit_stdp_branch(delay, response, "potentiation")
    depression, _ = fit_stdp_branch(delay, response, "depression")

    assert np.isclose(potentiation[1], 0.09, atol=1e-6)
    assert np.isclose(depression[1], 0.15, atol=1e-6)
    assert potentiation[0] > 0
    assert depression[0] < 0


def test_stdp_fit_excludes_the_zero_delay_point():
    delay = np.arange(-0.6, 0.65, 0.05)
    response = 24.0 * np.exp(-np.abs(delay) / 0.11)
    response[delay > 0] *= -1
    response[np.isclose(delay, 0.0)] = 10_000.0

    potentiation, _ = fit_stdp_branch(delay, response, "potentiation")
    depression, _ = fit_stdp_branch(delay, response, "depression")

    assert np.isclose(potentiation[1], 0.11, atol=1e-6)
    assert np.isclose(depression[1], 0.11, atol=1e-6)
