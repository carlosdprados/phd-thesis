#!/usr/bin/env python3
"""Chapter 5 -- from in-silico model to a worn device: (i) sensor site (chest vs the
consumer wrist), and (ii) the energy / latency / training-cost envelope, grounded in
the measured Chapter 2 device numbers.

Two questions a jury asks of an "affective-computing application":

  (1) Would it survive a real wearable? WESAD records the same sessions from a chest
      strap (clean ECG + respiration) AND an Empatica E4 wrist band (PPG, EDA, skin
      temperature -- fewer channels, much noisier). We re-run the continuous binary
      stress detector of ch5_onset.py on the wrist signals and compare to the chest.

  (2) What would it cost to run? The reservoir's dynamics are physical and untrained;
      only the linear read-out is fitted, by one closed-form ridge solve. We report
      the exact trainable-parameter and MAC counts. A deliberately labelled reference
      calculation then charges each simulated node one measured Chapter 2 Hybrane
      write event per update. This is neither a PEO-device prediction nor a complete
      system-power estimate; it only makes the scale implied by that source train
      auditable.

Run from the repo root:  python scripts/ch5_deployment.py
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch5_model import load_cards                                  # noqa: E402
import ch5_onset as O                                             # noqa: E402
from ch5_wesad import load_raw, load_raw_wrist, CHANNELS, WRIST_CHANNELS  # noqa: E402

# ---- measured Hybrane source-train constants (Chapter 2; source of truth) ----
# Recomputed from the 50 positive active dwells in D1_T/D1_V/D1_I.  The values
# are intentionally explicit here so that the deployment table can be checked
# without rerunning the Chapter 2 raw-data extractor.
E_EVENT_MIN_J = 84.26355719446866e-9
E_EVENT_MEDIAN_J = 1079.6075481059008e-9
E_EVENT_MAX_J = 1550.7477745649264e-9


# ----------------------------------------------------------------------------
# (1) Sensor site: chest vs wrist
# ----------------------------------------------------------------------------
def site_comparison(cards):
    """Continuous binary stress detection (ch5_onset) on the chest vs the wrist
    signals, clean and under sensor noise, SEED-AVERAGED via the noise sweep so the
    numbers match the rest of the chapter. Returns {site: dict} with per-bank F1 at
    sigma 0 and 0.4, clean false-alarm rates, and the per-subject paired het-inst
    test at sigma=0.4."""
    sites = {"chest (ECG+Resp+EDA+Temp)": load_raw(),
             "wrist (Empatica E4: EDA+Temp+PPG)": load_raw_wrist()}
    out = {}
    for name, raw in sites.items():
        sw = O.noise_sweep(raw, cards)
        i0, i4 = sw["sigmas"].index(0.0), sw["sigmas"].index(0.4)
        rN = O.evaluate(raw, cards, sigma=0.4)             # per-subject scores @ sigma 0.4
        out[name] = dict(
            f1_0={b: sw["banks"][b]["f1"][i0][0] for b in ("inst", "mem0", "hom", "het")},
            f1_4={b: sw["banks"][b]["f1"][i4][0] for b in ("inst", "mem0", "hom", "het")},
            far0={b: sw["banks"][b]["far"][i0][0] for b in ("inst", "hom", "het")},
            paired=O._paired(rN["het"]["subj_f1"], rN["inst"]["subj_f1"]),
        )
    return out


# ----------------------------------------------------------------------------
# (2) Energy / latency / training-cost envelope
# ----------------------------------------------------------------------------
def envelope(N=48, n_classes=3, dt=1.0):
    """Exact read-out size plus a labelled Hybrane write-energy reference.

    - Trainable parameters: reservoir dynamics are fixed physical devices (0 trained);
      the read-out is a single (N+1)x n_classes weight matrix, fitted by one ridge
      solve (closed form -- no backpropagation, no GPU).
    - Energy: charge each node one median positive event from the measured Chapter 2
      Hybrane source train. The min--max interval propagates the event-level range.
      This reference is not a prediction for a fabricated PEO reservoir and excludes
      reads, conversion, sensing, communication, control, and leakage.
    - Read-out compute: N*n_classes multiply-accumulates per step. No energy per MAC
      is assumed because implementation technology is unspecified.
    """
    train_params = (N + 1) * n_classes
    e_step = N * E_EVENT_MEDIAN_J
    e_step_range = (N * E_EVENT_MIN_J, N * E_EVENT_MAX_J)
    p_avg = e_step / dt
    return dict(
        N=N, n_classes=n_classes, dt=dt,
        train_params=train_params,
        e_step_J=e_step, p_avg_W=p_avg,
        e_step_range_J=e_step_range,
        readout_macs=N * n_classes,
    )


def _fmt_si(x, unit):
    for p, s in [(1e-12, "p"), (1e-9, "n"), (1e-6, "u"), (1e-3, "m"), (1, "")]:
        if abs(x) < p * 1000:
            return f"{x / p:.2f} {s}{unit}"
    return f"{x:.2e} {unit}"


def main():
    cards = load_cards(li_only=True)
    if not os.path.isdir("data/wesad/WESAD"):
        print("WESAD not present; run scripts/ch5_wesad.py for download instructions.")
    else:
        print("(1) SENSOR SITE -- continuous binary stress-detection macro-F1 "
              "(seed-averaged)\n")
        cmp = site_comparison(cards)
        for name, d in cmp.items():
            print(f"  {name}")
            print(f"      {'bank':5s} {'F1 sig0':>8} {'F1 sig0.4':>10} {'FAR sig0':>9}")
            for b in ("inst", "mem0", "hom", "het"):
                far = d["far0"].get(b)
                fars = f"{far:9.3f}" if far is not None else f"{'--':>9}"
                print(f"      {b:5s} {d['f1_0'][b]:8.3f} {d['f1_4'][b]:10.3f} {fars}")
            p = d["paired"]
            print(f"      paired het-inst F1@sig0.4: {p['mean']:+.3f}, "
                  f"{int(p['frac_pos']*p['n'])}/{p['n']}, p={p['p']:.1e}\n")

    print("(2) DEPLOYMENT COUNTS AND HYBRANE WRITE-ENERGY REFERENCE\n")
    for N in (24, 48):
        e = envelope(N=N)
        print(f"  N={N} nodes, {e['n_classes']} classes, dt={e['dt']:g}s:")
        print(f"    trainable params: reservoir 0 + read-out {e['train_params']} "
              f"(one ridge solve, no backprop)")
        print(f"    read-out operations: {e['readout_macs']} MACs per step")
        print(f"    reference energy/update {_fmt_si(e['e_step_J'],'J')} "
              f"({_fmt_si(e['e_step_range_J'][0],'J')}--"
              f"{_fmt_si(e['e_step_range_J'][1],'J')}) -> reference power "
              f"{_fmt_si(e['p_avg_W'],'W')} (always-on, 1 update/s)")
    print("\n  Reference only: one Chapter 2 Hybrane write per node per update; "
          "not a PEO-device prediction or full-system budget.")


if __name__ == "__main__":
    main()
