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


def main():
    # chemistry + manifest candidates
    man = list(csv.DictReader(open(os.path.join(OUT, "ch4_device_manifest_DRAFT.csv"))))
    cell = {}  # device_id -> (cation, peo, salt, stratum)
    for r in man:
        if r["manifest_candidate"] == "1":
            cell[r["device_id"]] = (r["cation"], r["peo_mass_fraction"], r["salt_mass_fraction"], r["stratum"])

    flags = set()
    for r in load("FILTERED_DEVICES.csv"):
        flags.add((G(r, "device_name"), G(r, "day"), G(r, "pixel"), G(r, "measurement_type")))

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
        if (dn, G(r, "day"), G(r, "pixel"), "DELAYTIME") in flags:
            continue
        t, y = fnum(G(r, "delay time (s)")), fnum(G(r, "ratio"))
        if t and t > 0 and y is not None:
            grp[(dn, G(r, "pixel"))].append((t, y))

    decay_rows = []
    for (dn, px), pts in grp.items():
        pts = sorted(set(pts))
        t = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
        if len(t) < 6:
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
        identified = int(np.isfinite(tau) and 0.5 <= tau <= 1000 and r2 >= 0.95)
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
        if (dn, G(r, "day"), G(r, "pixel"), "PULSES") in flags:
            continue
        N, y = fnum(G(r, "number of pulses")), fnum(G(r, "ratio"))
        if N and N > 0 and y is not None:
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
    for k in sorted(cells):
        rows = cells[k]; ndev = len({r["device_id"] for r in rows})
        idrows = [r for r in rows if r["identified"]]; nb = len({r["device_id"] for r in idrows})
        tau = dmed(idrows, "tau_s") if idrows else float("nan")
        print(f"  {k[0]:2s} PEO{k[1]:>4}/salt{k[2]:<5} n_dev={ndev:2d} | t_half med={dmed(rows,'t_half_s'):6.1f}s | "
              f"ret@60s={dmed(rows,'retention60'):.2f} | tau(id n={nb})={tau:6.1f}s")

    print("\n== PULSES potentiation descriptors per cell ==")
    pcells = collections.defaultdict(list)
    for dn in {r["device_id"] for r in pulse_rows}:
        c, peo, salt, _ = cell[dn]; pcells[(c, peo, salt)].append(dn)
    onsetd = by_dev(pulse_rows, "onset_N"); peakd = by_dev(pulse_rows, "peak_ratio"); npeakd = by_dev(pulse_rows, "N_peak")
    gexpd = by_dev(pulse_rows, "growth_exp")
    turn = collections.defaultdict(list)
    for r in pulse_rows: turn[r["device_id"]].append(r["turnover"])
    for k in sorted(pcells):
        ds = pcells[k]
        to = 100 * med([med(turn[d]) for d in ds])
        print(f"  {k[0]:2s} PEO{k[1]:>4}/salt{k[2]:<5} n_dev={len(ds):2d} | onsetN med={med([onsetd[d] for d in ds]):5.1f} | growth_exp={med([gexpd[d] for d in ds]):.2f} | peak={med([peakd[d] for d in ds]):6.1f} @N={med([npeakd[d] for d in ds]):5.0f} | turnover~{to:.0f}%")


if __name__ == "__main__":
    main()
