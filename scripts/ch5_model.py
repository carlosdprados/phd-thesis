#!/usr/bin/env python3
"""Chapter 5 behavioural model — composition-indexed parameter cards + the
discrete-time phi (write nonlinearity) (x) lambda (fading memory) (x) f (read)
device model used by the reservoir-computing demonstrations.

Run from the repo root:  python3 scripts/ch5_model.py
Inputs (produced by scripts/ch4_dynamics_fits.py):
  handouts/ch4_decay_by_cell.csv   -> fading memory tau, beta, t_half, retention60
  handouts/ch4_pulses_by_cell.csv  -> write nonlinearity alpha, peak ratio, N_peak, turnover

This is the SHARED BACKBONE for both Chapter-5 demonstrations (handout 12):
  A) single-node time-multiplexed reservoir on the lead cell PEO 0.3 / salt 0.09
  B) heterogeneous multi-node reservoir over the composition bank.

Honesty notes baked in (handout 12 sec 3, sec 9):
- The write nonlinearity phi and the fading memory lambda were measured SEPARATELY
  (potentiation at one fixed inter-pulse cadence; decay after potentiation). This
  model COMPOSES them; that composition is an explicit assumption, not a measured
  fact. A varied-cadence pulse-train experiment is the test (future work).
- Fading memory uses the identified Kohlrausch (tau, beta) where available; for
  cells without an identified fit it falls back to a single exponential whose tau
  reproduces the model-free half-life (tau_eff = t_half / ln 2, beta = 1).
- Read is assumed sub-threshold (state-preserving), as in the Ch2 PoC device.

TODO (next session): leave-one-dataset-out validation against the raw curves;
per-device parameter spread for the variability envelope; pulse-encoding front end.
"""
import csv, os, math
from dataclasses import dataclass
import numpy as np

OUT = "handouts"
LN2 = math.log(2.0)


def _f(x):
    try:
        return float(x)
    except Exception:
        return None


@dataclass
class ParameterCard:
    """One composition cell's behavioural parameters (Li, Ag, 4 V/2 V)."""
    cation: str
    peo: str
    salt: str
    n_dev: int
    # fading memory (DELAYTIME)
    tau: float          # effective Kohlrausch relaxation time [s]
    beta: float         # stretch exponent (1.0 = simple exponential)
    t_half: float       # model-free half-enhancement time [s]
    retention60: float  # fraction of enhancement left at 60 s
    identified: bool    # True if tau/beta came from an identified stretched fit
    # write nonlinearity (PULSES)
    alpha: float        # log-log growth exponent of the conductance ratio vs N
    peak_ratio: float   # peak conductance enhancement (dynamic range)
    n_peak: float       # pulse count at the peak (turnover point; >= max tested if no turnover)
    turnover: bool      # whether the response turns over within the measured range
    onset_N: float      # pulses before the ratio exceeds ~2

    @property
    def cell(self):
        return f"{self.cation} PEO{self.peo}/salt{self.salt}"

    # ---- fading memory: residual fraction of an enhancement after a wait dt [s] ----
    def decay_factor(self, dt):
        dt = np.asarray(dt, dtype=float)
        return np.exp(-np.power(np.clip(dt, 0, None) / self.tau, self.beta))

    # ---- write nonlinearity: conductance enhancement ratio after N identical pulses ----
    def potentiation_ratio(self, N):
        """First-order behavioural model: a power-law build-up R ~ N^alpha that
        saturates/turns over near n_peak at peak_ratio. Calibrated so R(n_peak)=peak_ratio."""
        N = np.asarray(N, dtype=float)
        npk = max(self.n_peak, 1.0)
        # power-law rise normalised to hit peak_ratio at n_peak
        rise = self.peak_ratio * np.power(np.clip(N, 1e-9, None) / npk, self.alpha)
        r = np.minimum(rise, self.peak_ratio)
        if self.turnover:
            # gentle decline past the peak (decade-scale roll-off); behavioural only
            over = N > npk
            r = np.where(over, self.peak_ratio * np.power(npk / np.clip(N, 1e-9, None), 0.5), r)
        return np.maximum(r, 1.0)


def load_cards(li_only=True):
    """Assemble composition-cell parameter cards from the Ch3 per-cell artifacts."""
    decay = {}
    for r in csv.DictReader(open(os.path.join(OUT, "ch4_decay_by_cell.csv"))):
        decay[(r["cation"], r["peo"], r["salt"])] = r
    pulses = {}
    for r in csv.DictReader(open(os.path.join(OUT, "ch4_pulses_by_cell.csv"))):
        pulses[(r["cation"], r["peo"], r["salt"])] = r

    cards = []
    for key, d in decay.items():
        if li_only and d["cation"] != "Li":
            continue
        p = pulses.get(key, {})
        t_half = _f(d.get("t_half_med")) or float("nan")
        tau_id = _f(d.get("tau_med"))
        beta_id = _f(d.get("beta_med"))
        identified = tau_id is not None and beta_id is not None
        if identified:
            tau, beta = tau_id, beta_id
        elif t_half == t_half:  # not NaN
            tau, beta = t_half / LN2, 1.0   # single-exp reproducing the half-life
        else:
            continue
        cards.append(ParameterCard(
            cation=d["cation"], peo=d["peo"], salt=d["salt"], n_dev=int(d["n_dev"]),
            tau=tau, beta=beta, t_half=t_half,
            retention60=_f(d.get("retention60_med")) or float("nan"),
            identified=bool(identified),
            alpha=_f(p.get("growth_exp_med")) or float("nan"),
            peak_ratio=_f(p.get("peak_ratio_med")) or float("nan"),
            n_peak=_f(p.get("N_peak_med")) or float("nan"),
            turnover=(_f(p.get("turnover_pct")) or 0) >= 50,
            onset_N=_f(p.get("onset_N_med")) or float("nan"),
        ))
    return cards


def lead_card(cards):
    """The Demonstration-A lead node: PEO 0.3 / salt 0.09."""
    for c in cards:
        if c.peo == "0.3" and c.salt == "0.09":
            return c
    return None


def _self_test(cards):
    """Sanity demo: print the bank and check the lead node shows fading memory."""
    print(f"{'cell':22s} {'n':>3} {'tau[s]':>7} {'beta':>5} {'t12[s]':>7} "
          f"{'ret60':>6} {'alpha':>6} {'peak':>7} {'Npeak':>6} turn")
    for c in sorted(cards, key=lambda z: (float(z.peo), float(z.salt))):
        print(f"{c.cell:22s} {c.n_dev:3d} {c.tau:7.1f} {c.beta:5.2f} {c.t_half:7.1f} "
              f"{c.retention60:6.2f} {c.alpha:6.2f} {c.peak_ratio:7.1f} {c.n_peak:6.0f} "
              f"{'Y' if c.turnover else 'n'}")

    lead = lead_card(cards)
    assert lead is not None, "lead cell PEO0.3/salt0.09 missing"
    # fading-memory monotonicity + half-life check
    dts = np.array([1, 5, 10, 30, 60, 300], float)
    res = lead.decay_factor(dts)
    assert np.all(np.diff(res) <= 1e-9), "decay must be monotonic"
    half_t = lead.t_half
    assert abs(lead.decay_factor(half_t) - 0.5) < 0.12 or lead.identified, \
        "single-exp fallback should pass ~half at t_half"
    # write nonlinearity sanity: rises, hits peak_ratio near n_peak
    N = np.array([1, 3, 10, 30, 100, 300, 1000], float)
    R = lead.potentiation_ratio(N)
    assert R[0] <= R[3] and R.max() <= lead.peak_ratio + 1e-6, "potentiation should rise to peak"
    print(f"\nlead node = {lead.cell}: tau={lead.tau:.1f}s beta={lead.beta:.2f} "
          f"identified={lead.identified}")
    print("  decay_factor(dt=[1,5,10,30,60,300]s) =", np.round(res, 3).tolist())
    print("  potentiation_ratio(N=[1,3,10,30,100,300,1000]) =", np.round(R, 1).tolist())
    print("\nself-test: PASS")


if __name__ == "__main__":
    cards = load_cards(li_only=True)
    print(f"loaded {len(cards)} composition parameter cards (Li, Ag)\n")
    _self_test(cards)
