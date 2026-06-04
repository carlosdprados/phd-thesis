#!/usr/bin/env python3
"""Chapter 3/4 dynamics fits: stretched-exponential fading-memory decay (DELAYTIME)
and pulse-potentiation descriptors (PULSES), per composition/cation cell.

Run from the repo root:  python3 scripts/ch3_4_dynamics_fits.py
Reads the (un-versioned) experimental DATABASE in the sibling Nanomem_Devices_Library/.
Writes per-device fit tables to handouts/ and prints a per-cell summary.

Honesty notes baked in:
- FILTERED flags are applied per (device, day, pixel, measurement_type).
- FILTERED barely covers PULSES/DELAYTIME, so we add our own quality screen (R^2,
  monotonicity) instead of trusting FILTERED for these two measurements.
- DELAYTIME restricted to the common 2.0 V read protocol.
- PNG-derived human curation (verdict + hand-picked points per device/measurement)
  is read from handouts/ch3_png_qa_curation.csv and applied: 'discard' drops the
  curve, 'clean' keeps only the listed points, 'use'/absent keeps all points.
  This is the single source of truth for the hand-picked points.
"""
import csv, os, collections
import numpy as np
from scipy.optimize import curve_fit

DB = "../Nanomem_Devices_Library/DATABASE"
OUT = "handouts"


def load(f):
    with open(os.path.join(DB, f), newline="") as fh:
        return list(csv.DictReader(fh))


def G(r, k):
    return (r.get(k) or "").strip()


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


def med(v):
    v = [x for x in v if x is not None and np.isfinite(x)]
    return float(np.median(v)) if v else float("nan")


def load_curation():
    """PNG-derived human QA: (device, measurement_type) -> (verdict, kept_points_set_or_None)."""
    cur = {}
    path = os.path.join(OUT, "ch3_png_qa_curation.csv")
    if not os.path.exists(path):
        return cur
    for r in csv.DictReader(open(path)):
        dn, mt = G(r, "device_name"), G(r, "measurement_type")
        v, kp = G(r, "verdict"), G(r, "kept_points")
        if not dn or not mt:
            continue
        kept = None
        if v == "clean" and kp and kp != "all":
            kept = set(float(x) for x in kp.split(";") if x.strip())
        cur[(dn, mt)] = (v, kept)
    return cur


def main():
    # Composition spine + chemistry landscape.
    #   - chemistry landscape (other cations/hosts/anions): manifest candidates only;
    #   - composition spine (PEO/LiTr/Ag): ALL such devices, not just manifest
    #     candidates, so the curation-salvaged low-concentration row (e.g. v151,
    #     PEO mass-fraction 0.15) enriches the PEO axis. Devices without PULSES/
    #     DELAYTIME data, FILTERED-flagged curves, and curation 'discard' verdicts
    #     are filtered downstream, so broadening here is safe.
    man = list(csv.DictReader(open(os.path.join(OUT, "ch4_device_manifest_DRAFT.csv"))))
    cell = {}  # device_id -> (cation, peo, salt, stratum)
    for r in man:
        is_cand = r["manifest_candidate"] == "1"
        is_peo_litr_ag = (r["host"] == "PEO" and r["cation"] == "Li" and r["electrode"] == "Ag")
        if is_cand or is_peo_litr_ag:
            cell[r["device_id"]] = (r["cation"], r["peo_mass_fraction"], r["salt_mass_fraction"], r["stratum"])

    flags = set()
    for r in load("FILTERED_DEVICES.csv"):
        flags.add((G(r, "device_name"), G(r, "day"), G(r, "pixel"), G(r, "measurement_type")))

    curation = load_curation()  # PNG-derived per-device verdicts + hand-picked points

    # DELAYTIME read-voltage screen: keep only devices measured at 2.0 V
    rv2 = set()
    for r in load("DEVICES_DELAYTIME_PIXEL_INFO.csv"):
        if G(r, "reading voltage (V)") == "2.0":
            rv2.add(G(r, "device_name"))

    # ---------- DELAYTIME: stretched-exponential fit per (device,pixel) ----------
    def stretched(t, A, tau, beta, C):
        return A * np.exp(-((t / tau) ** beta)) + C

    dly = load("DEVICES_DELAYTIME_CURVE_INFO.csv")
    grp = collections.defaultdict(list)  # (dev,pixel) -> [(t,ratio)]
    for r in dly:
        dn = G(r, "device_name")
        if dn not in cell or dn not in rv2:
            continue
        cur = curation.get((dn, "DELAYTIME"))
        if cur and cur[0] == "discard":
            continue
        if (dn, G(r, "day"), G(r, "pixel"), "DELAYTIME") in flags:
            continue
        t, y = fnum(G(r, "delay time (s)")), fnum(G(r, "ratio"))
        if t and t > 0 and y is not None:
            if cur and cur[0] == "clean" and cur[1] is not None and t not in cur[1]:
                continue  # keep only hand-picked points
            grp[(dn, G(r, "pixel"))].append((t, y))

    decay_rows = []
    for (dn, px), pts in grp.items():
        pts = sorted(set(pts))
        t = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
        # Hand-curated 'clean' curves are trusted down to 5 points (the reviewer
        # already vetted them); uncurated curves still need >=6 to fit. Either way
        # the stretched-exp tau is only *reported* when 'identified' (R2>=0.95),
        # so sparse curves contribute the model-free t_half but not a fitted tau.
        ccur = curation.get((dn, "DELAYTIME"))
        min_n = 5 if (ccur and ccur[0] == "clean") else 6
        if len(t) < min_n:
            continue
        # --- model-free metrics (robust; primary) ---
        r1 = float(y[t == 1][0]) if (t == 1).any() else float(y[0])
        def at(tt):
            return float(y[t == tt][0]) if (t == tt).any() else float("nan")
        r60, r300 = at(60), at(300)
        target = r1 / 2.0; thalf = float("nan")   # half-enhancement time, log-t interp
        for i in range(len(t) - 1):
            if y[i] >= target >= y[i + 1] and y[i] != y[i + 1]:
                lt, lt2 = np.log10(t[i]), np.log10(t[i + 1])
                frac = (y[i] - target) / (y[i] - y[i + 1])
                thalf = float(10 ** (lt + frac * (lt2 - lt))); break
        # --- stretched-exp fit (secondary; weakly identified at 8 pts) ---
        A0 = max(y.max() - y.min(), 1e-3); C0 = max(y.min(), 0.0)
        tau = beta = floor = r2 = float("nan")
        try:
            p, _ = curve_fit(stretched, t, y, p0=[A0, float(np.median(t)), 0.7, C0],
                             bounds=([0, 1e-2, 0.1, 0], [np.inf, 1e5, 2.0, np.inf]), maxfev=40000)
            yhat = stretched(t, *p); r2 = float(1 - np.sum((y - yhat) ** 2) / max(np.sum((y - y.mean()) ** 2), 1e-12))
            tau, beta, floor = float(p[1]), float(p[2]), float(p[3])
        except Exception:
            pass
        # Require >=6 points so the 4-parameter stretched fit keeps >=2 dof; a fit
        # on 5 points (e.g. the curated v151 curve) would hit R2>=0.95 trivially by
        # overfitting, so such curves report the model-free t_half only.
        identified = int(np.isfinite(tau) and 0.5 <= tau <= 1000 and r2 >= 0.95 and len(t) >= 6)
        c, peo, salt, strat = cell[dn]
        decay_rows.append(dict(device_id=dn, pixel=px, cation=c, peo=peo, salt=salt, stratum=strat,
                               r1=round(r1, 2), r60=(round(r60, 2) if np.isfinite(r60) else ""),
                               retention60=(round(r60 / r1, 3) if np.isfinite(r60) and r1 else ""),
                               t_half_s=(round(thalf, 2) if np.isfinite(thalf) else ""),
                               tau_s=(round(tau, 2) if np.isfinite(tau) else ""),
                               beta=(round(beta, 3) if np.isfinite(beta) else ""),
                               r2=(round(r2, 4) if np.isfinite(r2) else ""), identified=identified, n=len(t)))

    with open(os.path.join(OUT, "ch4_decay_fits.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["device_id", "pixel", "cation", "peo", "salt", "stratum",
                                           "r1", "r60", "retention60", "t_half_s", "tau_s", "beta", "r2", "identified", "n"])
        w.writeheader(); [w.writerow(x) for x in decay_rows]

    # ---------- PULSES: descriptors per (device,pixel) ----------
    pul = load("DEVICES_PULSES_CURVE_INFO.csv")
    pg = collections.defaultdict(list)
    for r in pul:
        dn = G(r, "device_name")
        if dn not in cell:
            continue
        cur = curation.get((dn, "PULSES"))
        if cur and cur[0] == "discard":
            continue
        if (dn, G(r, "day"), G(r, "pixel"), "PULSES") in flags:
            continue
        N, y = fnum(G(r, "number of pulses")), fnum(G(r, "ratio"))
        if N and N > 0 and y is not None:
            if cur and cur[0] == "clean" and cur[1] is not None and N not in cur[1]:
                continue
            pg[(dn, G(r, "pixel"))].append((N, y))

    pulse_rows = []
    for (dn, px), pts in pg.items():
        pts = sorted(set(pts))
        N = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
        if len(N) < 5:
            continue
        pk = int(np.argmax(y)); peak = float(y[pk]); npeak = float(N[pk])
        turnover = int(pk < len(y) - 1)
        onset = next((float(n) for n, rr in zip(N, y) if rr > 2), float("nan"))
        mask = (N <= npeak) & (y > 0)
        gexp = float(np.polyfit(np.log10(N[mask]), np.log10(y[mask]), 1)[0]) if mask.sum() >= 3 else float("nan")
        c, peo, salt, strat = cell[dn]
        pulse_rows.append(dict(device_id=dn, pixel=px, cation=c, peo=peo, salt=salt, stratum=strat,
                               onset_N=onset, peak_ratio=round(peak, 2), N_peak=npeak,
                               turnover=turnover, growth_exp=round(gexp, 3) if np.isfinite(gexp) else "", n=len(N)))

    with open(os.path.join(OUT, "ch4_pulse_descriptors.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["device_id", "pixel", "cation", "peo", "salt", "stratum",
                                           "onset_N", "peak_ratio", "N_peak", "turnover", "growth_exp", "n"])
        w.writeheader(); [w.writerow(x) for x in pulse_rows]

    # ---------- per-cell summaries ----------
    def by_dev(rows, key):
        d = collections.defaultdict(list)
        for r in rows:
            d[r["device_id"]].append(r[key])
        return {k: med(v) for k, v in d.items()}

    def dmed(rows, key):
        """device-median then cell-median of a possibly-blank numeric column"""
        d = collections.defaultdict(list)
        for r in rows:
            v = r.get(key, "")
            if v != "" and v is not None:
                d[r["device_id"]].append(float(v))
        return med([med(v) for v in d.values()])

    nid = sum(r["identified"] for r in decay_rows)
    print(f"DELAYTIME: {len(decay_rows)} clean (device,pixel) curves; stretched-exp identified "
          f"(0.5<=tau<=1000s & R2>=0.95): {nid}/{len(decay_rows)}")
    print("\n== DELAYTIME fading memory per cell  [model-free t_half & retention@60s primary; tau only if identified] ==")
    cells = collections.defaultdict(list)
    for r in decay_rows:
        cells[(r["cation"], r["peo"], r["salt"])].append(r)
    decay_cell_rows = []
    for k in sorted(cells):
        rows = cells[k]; ndev = len({r["device_id"] for r in rows})
        idrows = [r for r in rows if r["identified"]]; nb = len({r["device_id"] for r in idrows})
        tau = dmed(idrows, "tau_s") if idrows else float("nan")
        beta = dmed(idrows, "beta") if idrows else float("nan")
        print(f"  {k[0]:2s} PEO{k[1]:>4}/salt{k[2]:<5} n_dev={ndev:2d} | t_half med={dmed(rows,'t_half_s'):6.1f}s | "
              f"ret@60s={dmed(rows,'retention60'):.2f} | tau(id n={nb})={tau:6.1f}s")
        decay_cell_rows.append(dict(
            cation=k[0], peo=k[1], salt=k[2], n_dev=ndev,
            t_half_med=(round(dmed(rows, "t_half_s"), 2) if np.isfinite(dmed(rows, "t_half_s")) else ""),
            retention60_med=(round(dmed(rows, "retention60"), 3) if np.isfinite(dmed(rows, "retention60")) else ""),
            n_identified=nb,
            tau_med=(round(tau, 2) if np.isfinite(tau) else ""),
            beta_med=(round(beta, 3) if np.isfinite(beta) else "")))
    with open(os.path.join(OUT, "ch3_decay_by_cell.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["cation", "peo", "salt", "n_dev", "t_half_med",
                                           "retention60_med", "n_identified", "tau_med", "beta_med"])
        w.writeheader(); [w.writerow(x) for x in decay_cell_rows]

    print("\n== PULSES potentiation descriptors per cell ==")
    pcells = collections.defaultdict(list)
    for dn in {r["device_id"] for r in pulse_rows}:
        c, peo, salt, _ = cell[dn]; pcells[(c, peo, salt)].append(dn)
    onsetd = by_dev(pulse_rows, "onset_N"); peakd = by_dev(pulse_rows, "peak_ratio"); npeakd = by_dev(pulse_rows, "N_peak")
    gexpd = by_dev(pulse_rows, "growth_exp")
    turn = collections.defaultdict(list)
    for r in pulse_rows: turn[r["device_id"]].append(r["turnover"])
    pulse_cell_rows = []
    for k in sorted(pcells):
        ds = pcells[k]
        to = 100 * med([med(turn[d]) for d in ds])
        onset = med([onsetd[d] for d in ds]); gexp = med([gexpd[d] for d in ds])
        peak = med([peakd[d] for d in ds]); npeak = med([npeakd[d] for d in ds])
        print(f"  {k[0]:2s} PEO{k[1]:>4}/salt{k[2]:<5} n_dev={len(ds):2d} | onsetN med={onset:5.1f} | growth_exp={gexp:.2f} | peak={peak:6.1f} @N={npeak:5.0f} | turnover~{to:.0f}%")
        pulse_cell_rows.append(dict(
            cation=k[0], peo=k[1], salt=k[2], n_dev=len(ds),
            onset_N_med=(round(onset, 1) if np.isfinite(onset) else ""),
            growth_exp_med=(round(gexp, 3) if np.isfinite(gexp) else ""),
            peak_ratio_med=(round(peak, 2) if np.isfinite(peak) else ""),
            N_peak_med=(round(npeak) if np.isfinite(npeak) else ""),
            turnover_pct=round(to)))
    with open(os.path.join(OUT, "ch3_pulses_by_cell.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["cation", "peo", "salt", "n_dev", "onset_N_med",
                                           "growth_exp_med", "peak_ratio_med", "N_peak_med", "turnover_pct"])
        w.writeheader(); [w.writerow(x) for x in pulse_cell_rows]


if __name__ == "__main__":
    main()
