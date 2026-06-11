#!/usr/bin/env python3
"""Audit of the uncategorized Au/TMPE/(Li,Na,K)OTf raw corpus (Jan-Feb 2025).

`DEVICES_LAB_DATA/uncategorized/` holds eight dated campaign folders
(2025-01-23-LiTr ... 2025-02-21-NaTr) that never went through the
feature-extraction pipeline: folder/file naming is free-form (protocol encoded
in Spanish/English filenames), so `global_navigation.py` skips them. The
2025-01-23-LiTr campaign is a reorganised copy of NM_v316's device folder
(plus ~18 files unique to this copy); the February campaigns exist *only*
here and, by date and chemistry, sit on the 2024-Q4/2025-Q1 Au generation
(TMPE 0.3 / salt 0.09, Au top electrode, 3000 rpm, 90 C 3 h, glovebox).

This script parses every raw file directly (Keithley TSB dump: line 1 =
current, line 2 = voltage, line 3 = time; comma-separated; occasional 'TSP>'
prefixes), classifies the programmed waveform from the voltage trace (not the
filename), extracts per-class features, and writes:

  handouts/uncat_inventory.csv    one row per raw file (id, class, protocol)
  handouts/uncat_features.csv     per-file physics features
  figures/uncat_qa/               per-file QA thumbnails (V(t), I(t) / I-V)

It also ingests, with the same code path, the *catalogued but never
pipeline-processed* NegaHyst/DualHyst D1_all.txt sweeps of the same Au/TMPE
generation (v296-v316) as a cross-check corpus, so the uncategorized sweeps
can be validated against canonical-archive measurements of the same devices.

Run from the repo root:  python3 scripts/uncat_au_tmpe_audit.py
"""
import os
import re
import csv
import math
import collections

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LAB = "../Nanomem_Devices_Library/DEVICES_LAB_DATA"
UNCAT = os.path.join(LAB, "uncategorized")
OUT = "handouts"
QADIR = "figures/uncat_qa"
os.makedirs(QADIR, exist_ok=True)

I_SAT = 1.0e-3          # Keithley range ceiling seen in the data (A)
SAT_FRAC = 0.97         # |I| above SAT_FRAC*I_SAT counts as saturated


# ---------------------------------------------------------------- parsing --
def parse_raw(path):
    """Return (I, V, T) arrays or raise ValueError. Robust to TSP> prefixes,
    duplicated trailing time lines, and isolated source-value glitches."""
    if os.path.getsize(path) == 0:
        raise ValueError("EMPTY")
    text = open(path, errors="replace").read()
    if "smu." in text and "--" in text:
        raise ValueError("TSP_SCRIPT")
    arrs = []
    for ln in text.splitlines():
        ln = ln.replace("TSP>", " ").strip().strip(",")
        if not ln:
            continue
        try:
            a = np.array([float(x) for x in ln.split(",") if x.strip()])
        except ValueError:
            continue
        if a.size >= 2:
            arrs.append(a)
    # one extra duplicated line (e.g. time printed twice) -> drop the duplicate
    if len(arrs) == 4 and arrs[2].size == arrs[3].size and np.allclose(arrs[2], arrs[3]):
        arrs = arrs[:3]
    if len(arrs) != 3:
        raise ValueError(f"{len(arrs)} numeric lines (expected 3)")
    n = min(a.size for a in arrs)
    I, V, T = (a[:n] for a in arrs)
    # drop isolated glitch samples (|V| beyond any programmed level)
    ok = np.abs(V) <= 20
    if (~ok).sum() > 0.01 * n:
        raise ValueError("implausible V trace")
    I, V, T = I[ok], V[ok], T[ok]
    if not (np.diff(T) > 0).all():
        bad = int((np.diff(T) <= 0).sum())
        if bad > 2:
            raise ValueError(f"time not monotonic ({bad} reversals)")
    if np.nanmax(np.abs(I)) > 0.1:
        raise ValueError("implausible I range")
    return I, V, T


# ----------------------------------------------------------- classification --
def runs(levels):
    """Run-length encode an integer/level array -> list of (value, start, len)."""
    out = []
    s = 0
    for i in range(1, len(levels) + 1):
        if i == len(levels) or levels[i] != levels[s]:
            out.append((levels[s], s, i - s))
            s = i
    return out


def classify(I, V, T):
    """Classify waveform from V(t). Returns dict with class + protocol params."""
    n = V.size
    vr = np.round(V, 2)
    uniq, cnt = np.unique(vr, return_counts=True)
    nuniq = uniq.size
    span = float(V.max() - V.min())
    d = dict(n_pts=n, dur=float(T[-1] - T[0]), dt_med=float(np.median(np.diff(T))),
             v_min=float(V.min()), v_max=float(V.max()))

    # --- constant voltage ---------------------------------------------------
    if nuniq == 1 or span < 0.05:
        d.update(cls="VCONST", v_hold=float(np.median(V)))
        return d

    # --- few discrete levels -> pulse-type waveform --------------------------
    if nuniq <= 6:
        base = float(uniq[np.argmax(cnt)])           # most-occupied level = read/base
        lv = runs(list(vr))
        pulse_lv = [r for r in lv if abs(r[0] - base) > 0.05]
        plevels = sorted({float(r[0]) for r in pulse_lv})
        n_pulses = len(pulse_lv)
        # trailing baseline run = relaxation tail
        tail_pts = lv[-1][2] if abs(lv[-1][0] - base) <= 0.05 else 0
        tail_s = float(T[-1] - T[-tail_pts]) if tail_pts > 1 else 0.0
        per = (T[-1] - T[0]) / max(n_pulses, 1)
        two_pol = len(plevels) >= 2 and min(plevels) < base < max(plevels)
        d.update(cls="PULSE", v_read=base, pulse_levels=";".join(f"{p:g}" for p in plevels),
                 n_pulses=n_pulses, period_s=float(per), tail_s=tail_s,
                 pot_depot=bool(two_pol))
        return d

    # --- many levels -> staircase sweep --------------------------------------
    # count direction reversals on the (rounded) trace
    dv = np.diff(vr)
    dv = dv[dv != 0]
    if dv.size == 0:
        d.update(cls="OTHER")
        return d
    sign = np.sign(dv)
    revs = int((sign[1:] != sign[:-1]).sum())
    amp = float(max(abs(V.min()), abs(V.max())))
    bipolar = V.min() < -0.3 and V.max() > 0.3
    n_cycles = max(1, int(round(revs / 2 if not bipolar else revs / 2)))
    steps = nuniq - 1
    # half-sweep rate in V/s: one limb spans `span` volts in (pts per limb)*dt
    pts_per_rev = n / max(revs, 1)
    rate = span / (pts_per_rev * d["dt_med"]) if revs else float("nan")
    d.update(cls="SWEEP", polarity=("BIPOLAR" if bipolar else
                                    ("NEG" if abs(V.min()) > abs(V.max()) else "POS")),
             amp=amp, n_cycles=n_cycles, steps=steps, rate_Vps=float(rate))
    return d


# ------------------------------------------------------------- features ----
def t50_model_free(t, y):
    """Time at which y first falls halfway from its initial to its final level
    (linear interpolation between samples). Model-free decay descriptor."""
    t = t - t[0]
    y0 = float(np.median(y[: max(2, y.size // 20)]))
    y1 = float(np.median(y[-max(2, y.size // 10):]))
    if y0 <= y1:
        return np.nan
    target = y0 - 0.5 * (y0 - y1)
    below = np.where(y <= target)[0]
    if below.size == 0:
        return np.nan
    k = below[0]
    if k == 0:
        return float(t[0])
    f = (y[k - 1] - target) / max(y[k - 1] - y[k], 1e-30)
    return float(t[k - 1] + f * (t[k] - t[k - 1]))


def kohlrausch_fit(t, y):
    """Fit y(t) = y_inf + (y0-y_inf)*exp(-(t/tau)^beta), beta in (0,1].
    Fitted on y normalised by its initial level, in log space (the decays span
    decades and the absolute scale is 1e-7..1e-4 A, which otherwise stalls the
    optimiser at p0). Returns (tau, beta, t_half, ok)."""
    from scipy.optimize import curve_fit
    t = t - t[0]
    y0 = float(np.median(y[: max(3, y.size // 50)]))
    if not np.isfinite(y0) or y0 <= 0 or (y <= 0).any():
        return (np.nan, np.nan, np.nan, False)
    z = y / y0
    zinf0 = float(np.clip(np.median(z[-max(3, z.size // 20):]), 1e-6, 2.0))

    def logf(t, tau, beta, zinf):
        m = zinf + (1.0 - zinf) * np.exp(-((t / max(tau, 1e-6)) ** beta))
        return np.log(np.clip(m, 1e-12, None))

    try:
        p, _ = curve_fit(logf, t, np.log(z), p0=[max(t[-1] / 5, 1.0), 0.7, zinf0],
                         bounds=([1e-3, 0.05, 0.0], [1e5, 1.0, 2.0]),
                         x_scale="jac", maxfev=20000)
        tau, beta, zinf = (float(x) for x in p)
        resid = float(np.sqrt(np.mean((logf(t, *p) - np.log(z)) ** 2)))
        t_half = tau * (math.log(2.0)) ** (1.0 / beta)
        return (tau, beta, t_half, resid < 0.25)
    except Exception:
        return (np.nan, np.nan, np.nan, False)


def sweep_features(I, V, T, info):
    """Per-cycle loop features for staircase sweeps; returns dict + cycle table."""
    vr = np.round(V, 2)
    amp = info["amp"]
    # split into limbs at direction reversals
    dv = np.diff(vr)
    idx = np.where(dv != 0)[0]
    sign = np.sign(dv[idx])
    rev_pts = [int(idx[k] + 1) for k in range(1, len(idx)) if sign[k] != sign[k - 1]]
    limbs = np.split(np.arange(V.size), rev_pts)
    # pair limbs into half-cycles: out (0->peak) and back (peak->0)
    cyc = []
    for a, b in zip(limbs[:-1:2], limbs[1::2]):
        seg = np.concatenate([a, b])
        Vc, Ic = V[seg], I[seg]
        vh = (V[a[0]] + V[a[-1]]) / 2.0        # mid-limb voltage (signed half-amplitude)
        # nearest samples on each limb to vh
        ia = a[np.argmin(np.abs(V[a] - vh))]
        ib = b[np.argmin(np.abs(V[b] - vh))]
        i_fwd, i_ret = I[ia], I[ib]
        onoff = abs(i_ret) / max(abs(i_fwd), 1e-13)
        area = float(np.trapz(Ic, Vc))
        norm = abs(area) / max(np.abs(Ic).max() * (Vc.max() - Vc.min()), 1e-30)
        cyc.append(dict(onoff=float(onoff), narea=float(norm),
                        i_peak=float(Ic[np.argmax(np.abs(Ic))]),
                        sat=bool(np.abs(Ic).max() >= SAT_FRAC * I_SAT)))
    if not cyc:
        return {}
    return dict(n_cycles_used=len(cyc),
                onoff_first=cyc[0]["onoff"], onoff_med=float(np.median([c["onoff"] for c in cyc])),
                narea_med=float(np.median([c["narea"] for c in cyc])),
                i_peak_max=float(max(abs(c["i_peak"]) for c in cyc)),
                cycle_gain=float(abs(cyc[-1]["i_peak"]) / max(abs(cyc[0]["i_peak"]), 1e-13)),
                any_sat=any(c["sat"] for c in cyc))


def pulse_features(I, V, T, info):
    """Read-phase potentiation/depression features for pulse trains."""
    base = info["v_read"]
    vr = np.round(V, 2)
    on_read = np.abs(vr - base) <= 0.05
    lv = runs(list(on_read))
    # current at each read segment (median of segment), in time order
    reads, t_reads = [], []
    for val, s, ln in lv:
        if val:  # read run
            seg = slice(s, s + ln)
            reads.append(float(np.median(np.abs(I[seg]))))
            t_reads.append(float(np.median(T[seg])))
    reads = np.array(reads)
    t_reads = np.array(t_reads)
    if reads.size < 5:
        return {}
    # potentiation phase = up to global max of a 5-read moving median
    k = max(1, min(5, reads.size // 10))
    smooth = np.convolve(reads, np.ones(k) / k, mode="same")
    ipk = int(np.argmax(smooth))
    r0 = float(np.median(reads[: max(2, reads.size // 100)]))
    rpk = float(smooth[ipk])
    feats = dict(n_reads=int(reads.size), i_read0=r0, i_read_peak=rpk,
                 pot_ratio=rpk / max(r0, 1e-13),
                 frac_to_peak=float(ipk / reads.size),
                 read_sat=bool(reads.max() >= SAT_FRAC * I_SAT),
                 any_sat=bool(np.abs(I).max() >= SAT_FRAC * I_SAT),
                 floor_suspect=bool(np.median(reads) < 1e-9))
    # growth exponent on the rising branch (log-log slope), if enough points
    rise = reads[: max(ipk, 5)]
    nn = np.arange(1, rise.size + 1)
    good = rise > 0
    if good.sum() > 5 and rpk / max(r0, 1e-13) > 1.5:
        b = np.polyfit(np.log(nn[good]), np.log(rise[good]), 1)[0]
        feats["growth_exp"] = float(b)
    # relaxation tail after last pulse
    if info.get("tail_s", 0) > 10:
        val, s, ln = runs(list(on_read))[-1]
        seg = slice(s + max(2, ln // 200), s + ln)        # drop first samples (transient)
        y = np.abs(I[seg]); t = T[seg]
        # decimate ultra-long tails for fit stability
        if y.size > 4000:
            step = y.size // 4000
            y, t = y[::step], t[::step]
        tau, beta, t_half, ok = kohlrausch_fit(t, y)
        feats.update(tail_s=float(info["tail_s"]), tau=tau, beta=beta,
                     t_half=t_half, fit_ok=ok,
                     tail_drop=float(1 - y[-max(2, y.size // 20):].mean()
                                     / max(y[: max(2, y.size // 20)].mean(), 1e-30)))
    return feats


def vconst_features(I, V, T, info):
    a = np.abs(I)
    n = a.size
    i0 = float(np.median(a[: max(3, n // 100)]))
    i1 = float(np.median(a[-max(3, n // 20):]))
    drift = i1 / max(i0, 1e-13)
    # time to reach 63% of total change
    target = i0 + 0.63 * (i1 - i0)
    rel = (a - target) * np.sign(i1 - i0)
    k = np.argmax(rel > 0) if (rel > 0).any() else n - 1
    return dict(i_start=i0, i_end=i1, drift_ratio=float(drift),
                t63=float(T[k] - T[0]), v_hold=info["v_hold"],
                any_sat=bool(a.max() >= SAT_FRAC * I_SAT))


# ------------------------------------------------------------------ walk ----
PIX_RE = re.compile(r"(?:^|[\\/_ (])([LR][1-8])(?=[\\/_ ,.)]|$)")
PIXN_RE = re.compile(r"Pixel ?(\d)", re.I)


def meta_from_path(rel):
    camp = rel.split(os.sep)[0]
    salt = re.search(r"(LiTr|NaTr|KTr)", camp).group(1)
    pm = PIX_RE.search(rel.replace(camp, "", 1))
    pix = pm.group(1) if pm else None
    if pix is None:
        pn = PIXN_RE.search(rel)
        pix = f"P{pn.group(1)}" if pn else "unk"
    dm = re.search(r"Day ?(\d+)", rel, re.I)
    day = int(dm.group(1)) if dm else None
    return camp, salt, pix, day


def qa_plot(I, V, T, info, rel, tag):
    fig, ax = plt.subplots(1, 2, figsize=(7.5, 2.6))
    if info["cls"] == "SWEEP":
        ax[0].plot(V, I * 1e6, lw=0.6)
        ax[0].set_xlabel("V (V)"); ax[0].set_ylabel("I (uA)")
    else:
        ax[0].plot(T - T[0], V, lw=0.5)
        ax[0].set_xlabel("t (s)"); ax[0].set_ylabel("V (V)")
    ax[1].plot(T - T[0], np.abs(I), lw=0.5)
    ax[1].set_yscale("log"); ax[1].set_xlabel("t (s)"); ax[1].set_ylabel("|I| (A)")
    fig.suptitle(f"[{info['cls']}] {rel}", fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(QADIR, tag + ".png"), dpi=80)
    plt.close(fig)


def walk_uncategorized():
    rows = []
    for root, _dirs, files in os.walk(UNCAT):
        for f in sorted(files):
            if not f.lower().endswith(".txt"):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, UNCAT)
            camp, salt, pix, day = meta_from_path(rel)
            row = dict(file=rel, campaign=camp, salt=salt, pixel=pix, day=day)
            try:
                I, V, T = parse_raw(p)
            except ValueError as e:
                row.update(cls="PARSE_FAIL", err=str(e))
                rows.append(row)
                continue
            info = classify(I, V, T)
            row.update(info)
            try:
                if info["cls"] == "SWEEP":
                    row.update(sweep_features(I, V, T, info))
                elif info["cls"] == "PULSE":
                    row.update(pulse_features(I, V, T, info))
                elif info["cls"] == "VCONST":
                    row.update(vconst_features(I, V, T, info))
            except Exception as e:           # keep the inventory row regardless
                row["err"] = f"feat: {e}"
            tag = re.sub(r"[^A-Za-z0-9]+", "_", rel)[:120]
            try:
                qa_plot(I, V, T, info, rel, tag)
            except Exception:
                pass
            rows.append(row)
    return rows


# ------------------------------------------- catalogued NegaHyst reference --
def walk_reference():
    """Same-generation catalogued Au/TMPE sweeps (NegaHyst/DualHyst/Hyst)."""
    pat = re.compile(r"NM_v(29[6-9]|3[01][0-9]|316)_")
    rows = []
    for q in ("2024-Q4_Devices", "2025-Q1_Devices"):
        qd = os.path.join(LAB, q)
        if not os.path.isdir(qd):
            continue
        for dev in sorted(os.listdir(qd)):
            if not pat.search(dev or ""):
                continue
            m = re.search(r"NM_v\d+", dev)
            chem = re.search(r"\((TMPE(?:LiTr|NaTr|KTr))", dev)
            for root, _d, files in os.walk(os.path.join(qd, dev)):
                if "_Prof" in root:
                    continue
                mtm = re.search(r"Day(\d+)_(\w+)", root)
                for f in files:
                    if f != "D1_all.txt" and not f.lower().endswith(".txt"):
                        continue
                    if f.lower().endswith(".py"):
                        continue
                    p = os.path.join(root, f)
                    try:
                        I, V, T = parse_raw(p)
                    except Exception:
                        continue
                    info = classify(I, V, T)
                    if info["cls"] != "SWEEP":
                        continue
                    feats = sweep_features(I, V, T, info)
                    pixm = PIX_RE.search(p.replace(qd, ""))
                    rows.append(dict(device=m.group(0),
                                     chem=(chem.group(1) if chem else "?"),
                                     day=(int(mtm.group(1)) if mtm else None),
                                     mtype=(mtm.group(2) if mtm else "?"),
                                     pixel=(pixm.group(1) if pixm else "?"),
                                     **info, **feats))
    return rows


def wcsv(path, rows):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path}  ({len(rows)} rows)")


def main():
    rows = walk_uncategorized()
    wcsv(os.path.join(OUT, "uncat_inventory.csv"), rows)

    ref = walk_reference()
    wcsv(os.path.join(OUT, "uncat_reference_sweeps.csv"), ref)

    # ------------------------------------------------------------- summary --
    print("\n=== class counts by campaign ===")
    tab = collections.Counter((r["campaign"], r["cls"]) for r in rows)
    camps = sorted({r["campaign"] for r in rows})
    classes = sorted({r["cls"] for r in rows})
    print(f"{'campaign':28s}" + "".join(f"{c:>12s}" for c in classes))
    for c in camps:
        print(f"{c:28s}" + "".join(f"{tab.get((c, k), 0):12d}" for k in classes))

    nfail = sum(1 for r in rows if r["cls"] == "PARSE_FAIL")
    print(f"\nparse failures: {nfail}")
    for r in rows:
        if r["cls"] == "PARSE_FAIL":
            print("  !", r["file"], "->", r.get("err"))

    print("\n=== saturation flags ===")
    nsat = sum(1 for r in rows if r.get("any_sat") or r.get("read_sat"))
    print(f"files touching the 1 mA ceiling: {nsat}")


if __name__ == "__main__":
    main()
