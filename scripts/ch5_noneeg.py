#!/usr/bin/env python3
"""Chapter 5 -- cross-corpus replication on a SECOND, independent affective dataset.

The WESAD results rest on one corpus. This script repeats the continuous
stress-monitoring test of ch5_onset.py on the PhysioNet "Non-EEG Dataset for
Assessment of Neurological Status" (Birjandtalab et al., 2016): 20 subjects wearing
an Affectiva Q wrist sensor (electrodermal activity, skin temperature) and a Nonin
pulse oximeter (heart rate), cycling through relaxation and physical, cognitive, and
emotional stress phases annotated in the record. The channels (EDA, temperature,
heart rate) are the same set as the WESAD wrist demonstration, on a different wrist
sensor and a different study population -- a genuine out-of-corpus test of the
chapter's headline application claim: that fading memory yields a noise-robust
continuous stress detector that an instantaneous classifier cannot match.

Labels are mapped to the WESAD binary convention so the ch5_onset harness runs
unchanged: relaxation -> 1 (not-stress), any stress phase -> 2 (stress).

Get the data (~25 MB, open access):  python -c "import wfdb; wfdb.dl_database('noneeg','data/noneeg')"
Run from the repo root:              python scripts/ch5_noneeg.py
"""
import os, sys, glob
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch5_model import load_cards                                  # noqa: E402
import ch5_onset as O                                             # noqa: E402
from ch5_wesad import (CALIBRATION_S, SLOW_FS, _load_stream_cache,  # noqa: E402
                       _save_stream_cache, _scale_subject, _source_signature)

NONEEG_DIR = "data/noneeg"
RELAX, STRESS, DROP = 1, 2, 0       # WESAD-compatible label codes (0 = excluded)
# The closest analogue to WESAD's psychosocial stressor is PSYCHOLOGICAL stress
# (cognitive + emotional). Physical stress is bodily exertion (walking/jogging) that
# drives heart rate and EDA by a different mechanism, so it is excluded by default
# (its instantaneous signature is trivially separable and would flatter the static
# baseline); set PSYCH_ONLY = False to lump all stress phases together instead.
PSYCH_ONLY = True


def _interp_to(x, n_out):
    """Past-hold resampling to n_out samples, with causal forward NaN filling."""
    x = np.asarray(x, float).ravel()
    if np.isnan(x).any():
        idx = np.where(~np.isnan(x), np.arange(len(x)), -1)
        idx = np.maximum.accumulate(idx)
        x = np.where(idx >= 0, x[np.maximum(idx, 0)], 0.0)
    pos = np.minimum(np.floor(np.arange(n_out) * len(x) / n_out).astype(int), len(x) - 1)
    return x[pos]


def _load_subject(base):
    """Return (U (T,3) [EDA,Temp,HR] scaled @ SLOW_FS, lab (T,) in {1,2}) for one
    subject, or None on failure. Aligns the 8 Hz AccTempEDA and 1 Hz SpO2HR records
    onto a common SLOW_FS timeline and fills phase labels from the .atr annotation."""
    import wfdb
    ate = wfdb.rdrecord(f"{base}_AccTempEDA")          # ax,ay,az,temp,EDA @ 8 Hz
    sph = wfdb.rdrecord(f"{base}_SpO2HR")              # SpO2,hr @ 1 Hz
    ann = wfdb.rdann(f"{base}_AccTempEDA", "atr")      # phase boundaries (8 Hz idx)
    fs = ate.fs
    eda = ate.p_signal[:, ate.sig_name.index("EDA")]
    temp = ate.p_signal[:, ate.sig_name.index("temp")]
    hr = sph.p_signal[:, sph.sig_name.index("hr")]

    dur_s = min(len(eda) / fs, len(hr) / sph.fs)
    n = max(int(dur_s * SLOW_FS), 1)
    U = np.column_stack([_interp_to(eda, n), _interp_to(temp, n), _interp_to(hr, n)])

    # per-sample label at 8 Hz from annotation phases, then resample to SLOW_FS
    lab8 = np.full(len(eda), RELAX, int)
    bounds = list(ann.sample) + [len(eda)]
    for i, note in enumerate(ann.aux_note):
        a, b = int(bounds[i]), int(bounds[i + 1])
        nl = note.lower()
        if "physical" in nl:
            lab8[a:b] = DROP if PSYCH_ONLY else STRESS
        elif "stress" in nl:                           # cognitive / emotional
            lab8[a:b] = STRESS
        else:                                          # relaxation
            lab8[a:b] = RELAX
    li = np.minimum(np.floor(np.arange(n) * len(lab8) / n).astype(int), len(lab8) - 1)
    return _scale_subject(U, fs=SLOW_FS), lab8[li]


def load_raw_noneeg(cache=True):
    """{sid: (U (T,3) scaled @ SLOW_FS, lab in {1,2})} for the Non-EEG corpus."""
    tag = "psych" if PSYCH_ONLY else "allstress"
    paths = sorted(glob.glob(os.path.join(NONEEG_DIR, "Subject*")))
    signature = _source_signature([p for p in paths if os.path.isfile(p)])
    cache_path = os.path.join(os.path.dirname(NONEEG_DIR),
                              f"_cache_v4_causalcal{CALIBRATION_S:g}_noneeg_"
                              f"{tag}_EDA-Temp-HR_4hz.npz")
    raw = {}
    cached = _load_stream_cache(cache_path, signature) if cache else None
    if cached is not None:
        raw = cached
        print(f"  (loaded {len(raw)} subjects from cache {cache_path})")
        return raw
    for hea in sorted(glob.glob(os.path.join(NONEEG_DIR, "Subject*_AccTempEDA.hea"))):
        base = hea[:-len("_AccTempEDA.hea")]
        sid = os.path.basename(base)
        try:
            raw[sid] = _load_subject(base)
        except Exception as e:
            print(f"  ! skip {sid}: {e}")
    if cache and raw:
        _save_stream_cache(cache_path, signature, raw)
        print(f"  (cached {len(raw)} subjects -> {cache_path})")
    return raw


def main():
    cards = load_cards(li_only=True)
    if not glob.glob(os.path.join(NONEEG_DIR, "Subject*_AccTempEDA.hea")):
        print(f"Non-EEG dataset not found at {NONEEG_DIR}. Fetch it with:\n"
              f"  python -c \"import wfdb; wfdb.dl_database('noneeg','{NONEEG_DIR}')\"")
        return
    raw = load_raw_noneeg()
    secs = {"relax": 0, "stress": 0}
    for _, lab in raw.values():
        secs["stress"] += int(np.sum(lab == STRESS) / SLOW_FS)
        secs["relax"] += int(np.sum(lab == RELAX) / SLOW_FS)
    print(f"cross-corpus replication (PhysioNet Non-EEG) | {len(raw)} subjects | "
          f"channels EDA+Temp+HR | labelled seconds: {secs}\n")

    print("CLEAN streams (sigma=0):")
    r0 = O.evaluate(raw, cards, sigma=0.0)
    print(f"  {'bank':5s} {'binF1':>7} {'transF1':>8} {'falseAlarm':>11}")
    for b in ("inst", "mem0", "hom", "het"):
        m = r0[b]
        print(f"  {b:5s} {m['f1']:7.3f} {m['trans_f1']:8.3f} {m['far']:11.3f}")
    st = O._paired(r0["het"]["subj_f1"], r0["inst"]["subj_f1"])
    print(f"  het-inst binary-F1 = {st['mean']:+.3f} "
          f"({int(st['frac_pos']*st['n'])}/{st['n']} subjects, p={st['p']:.1e})")

    print("\nNOISE ROBUSTNESS (binary-F1 vs sigma; seed-averaged):")
    sw = O.noise_sweep(raw, cards)
    print(f"  {'bank':5s}  " + "  ".join(f"sig={s:g}" for s in sw["sigmas"]))
    for b in ("inst", "mem0", "hom", "het"):
        print(f"  {b:5s}  " + "  ".join(f"{m:.3f}" for m, _ in sw["banks"][b]["f1"]))
    hi = len(sw["sigmas"]) - 1
    rN = O.evaluate(raw, cards, sigma=sw["sigmas"][hi])
    stN = O._paired(rN["het"]["subj_f1"], rN["inst"]["subj_f1"])
    print(f"\n  at sigma={sw['sigmas'][hi]:g}: het {sw['banks']['het']['f1'][hi][0]:.3f} "
          f"vs inst {sw['banks']['inst']['f1'][hi][0]:.3f} "
          f"(advantage {sw['banks']['het']['f1'][hi][0]-sw['banks']['inst']['f1'][hi][0]:+.3f}; "
          f"{int(stN['frac_pos']*stN['n'])}/{stN['n']} subjects, p={stN['p']:.1e})")


if __name__ == "__main__":
    main()
