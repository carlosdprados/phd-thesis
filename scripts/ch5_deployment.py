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
      only the linear read-out is fitted, by one closed-form ridge solve. We size the
      trainable-parameter count and an order-of-magnitude energy/latency budget from
      the MEASURED proof-of-concept device (Chapter 2):
        - energy per synaptic (write) event ~ 50 nJ  (1 V, 0.1 s pulse)
        - areal energy density ~ 6 fJ/um^2 over the 0.0825 cm^2 junction
        - sub-threshold, state-preserving read at 0.5 V
        - sub-kHz operating regime (affective signals are sub-Hz -> natively in band)
      These are unoptimised, large-area proof-of-concept figures; the point is the
      order of magnitude and the qualitative contrast with a gradient-trained model.

Run from the repo root:  python3 scripts/ch5_deployment.py
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch5_model import load_cards                                  # noqa: E402
import ch5_onset as O                                             # noqa: E402
from ch5_wesad import load_raw, load_raw_wrist, CHANNELS, WRIST_CHANNELS  # noqa: E402

# ---- measured device constants (Chapter 2 / appendix A; source of truth) ----
E_EVENT_J = 50e-9          # energy per synaptic event (1 V, 0.1 s write pulse) [J]
E_AREAL_J_UM2 = 6e-15      # areal switching-energy density [J/um^2]
AREA_UM2 = 0.0825 * 1e8    # 0.0825 cm^2 junction in um^2  (1 cm^2 = 1e8 um^2)
V_READ = 0.5               # sub-threshold read bias [V]


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
def envelope(N=48, n_classes=3, dt=1.0, mac_energy_J=1e-12, deep_params=(1e4, 1e6)):
    """Order-of-magnitude deployment budget for an N-node reservoir read out by a
    linear classifier, from the measured device constants.

    - Trainable parameters: reservoir dynamics are fixed physical devices (0 trained);
      the read-out is a single (N+1)x n_classes weight matrix, fitted by one ridge
      solve (closed form -- no backpropagation, no GPU).
    - Energy: conservatively charge each node one measured write event per update;
      reads are sub-threshold and cheaper. Average power = N * E_event / dt.
    - Read-out compute: N*n_classes multiply-accumulates per step -> negligible.
    - Latency: the device responds in the sub-kHz regime; affect is sub-Hz, so the
      substrate is not the bottleneck, and the read-out is one matrix-vector product.
    """
    train_params = (N + 1) * n_classes
    e_step = N * E_EVENT_J                       # J per reservoir update (write proxy)
    p_avg = e_step / dt                          # average power [W]
    e_readout_step = N * n_classes * mac_energy_J
    return dict(
        N=N, n_classes=n_classes, dt=dt,
        train_params=train_params,
        deep_params=deep_params,
        param_ratio=(deep_params[0] / train_params, deep_params[1] / train_params),
        e_step_J=e_step, p_avg_W=p_avg,
        e_readout_step_J=e_readout_step,
        areal_check_J=E_AREAL_J_UM2 * AREA_UM2,  # should ~ E_EVENT_J (consistency)
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

    print("(2) DEPLOYMENT ENVELOPE (from measured Chapter 2 device constants)\n")
    for N in (24, 48):
        e = envelope(N=N)
        print(f"  N={N} nodes, {e['n_classes']} classes, dt={e['dt']:g}s:")
        print(f"    trainable params: reservoir 0 + read-out {e['train_params']} "
              f"(one ridge solve, no backprop)")
        print(f"    vs deep model {e['deep_params'][0]:.0e}-{e['deep_params'][1]:.0e} "
              f"params -> {e['param_ratio'][0]:.0f}x-{e['param_ratio'][1]:.0f}x fewer trained")
        print(f"    energy/update {_fmt_si(e['e_step_J'],'J')}  ->  avg power "
              f"{_fmt_si(e['p_avg_W'],'W')} (always-on, 1 update/s)")
        print(f"    read-out compute {_fmt_si(e['e_readout_step_J'],'J')}/step (negligible)\n")
    e = envelope()
    print(f"  consistency: areal density x area = {_fmt_si(e['areal_check_J'],'J')} "
          f"~ measured {_fmt_si(E_EVENT_J,'J')}/event")


if __name__ == "__main__":
    main()
