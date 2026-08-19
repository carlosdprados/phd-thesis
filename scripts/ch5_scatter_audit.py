#!/usr/bin/env python3
"""Measured between-substrate scatter of the fading-memory timescale.

Run from the repo root:  python scripts/ch5_scatter_audit.py
The primary estimate comes from the screened, substrate-level model-free
half-times in handouts/ch4_decay_fits.csv. A legacy instrument-fit tau audit is
retained only as an upper sensitivity reference.

Why this exists
---------------
The reservoir injects between-substrate variation as log-normal jitter on its
timescale. Because Chapter 4 defines the model-free t_half as the primary robust
timescale, the matching estimate is the typical within-cell SD of ln(t_half),
after junctions have been collapsed to one fabricated-substrate median.

The earlier 0.12 line was undocumented. A later 0.85 estimate used the noisier
instrument-side fitted tau and predated the corrected screening/aggregation.
Neither is the primary variability parameter for the revised node model.

Key honesty point baked in: a naive estimate that groups only by the qualitative
Components Group "SY, PEO, LiTr" CONFLATES the deliberate PEO x salt tuning sweep
(the comparative chapter's whole axis) with random scatter and over-states it.
The defensible number is the spread WITHIN each exact (PEO, salt) cell.
"""
import csv, os
import numpy as np

DB = "../Nanomem_Devices_Library/DATABASE"
OUT = "handouts"

# the reservoir spine: silver electrode, SY / PEO / LiOTf chemistry
COMP = "SY, PEO, LiTr"
METAL = "Ag"
MIN_DEV_PER_CELL = 3          # cells with enough devices to estimate a within-cell spread
OLD_CITED = 0.12


def load(fname):
    with open(os.path.join(DB, fname), newline="") as fh:
        return list(csv.DictReader(fh))


def fnum(x):
    try:
        v = float(x)
        return v if np.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def spearman(x, y):
    """Distribution-free monotonic correlation without a scipy dependency."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    if rx.std() == 0 or ry.std() == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def ols_resid_std(y, X):
    """Residual std after least-squares regression of y on design X (incl. const)."""
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = max(len(y) - X.shape[1], 1)
    return float(np.sqrt(np.sum(resid ** 2) / dof))


def robust_thalf_scatter():
    """Median within-cell SD of ln(t_half) on the replicated screened grid."""
    path = os.path.join(OUT, "ch4_decay_fits.csv")
    grouped = {}
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("cation") != "Li":
                continue
            if row.get("peo") not in {"0.3", "0.6", "1.2"}:
                continue
            if row.get("salt") not in {"0.045", "0.09", "0.18"}:
                continue
            value = fnum(row.get("t_half_s"))
            if value is not None and value > 0:
                grouped.setdefault((row["peo"], row["salt"]), []).append(value)
    cell_sigmas = [float(np.std(np.log(values), ddof=1))
                   for values in grouped.values() if len(values) >= 2]
    if not cell_sigmas:
        raise ValueError("no replicated t_half cells found")
    return (float(np.median(cell_sigmas)), sum(map(len, grouped.values())),
            len(cell_sigmas), min(cell_sigmas), max(cell_sigmas))


def main():
    sigma_thalf, n_thalf, n_cells, sigma_min, sigma_max = robust_thalf_scatter()
    lib = {r["device_name"]: r for r in load("UPDATED_DEVICES_LIBRARY.csv")}
    prof = {}
    for r in load("DEVICES_PROFILOMETRY_STATS.csv"):
        t = fnum(r.get("avg_thickness (nm)"))
        if t is not None:
            prof.setdefault(r["device_name"], []).append(t)
    prof = {k: float(np.median(v)) for k, v in prof.items()}

    # --- per-pixel tau on the Ag SY/PEO/LiTr spine, with fabrication covariates ---
    rows = []
    for r in load("DEVICES_DELAYTIME_PIXEL_INFO.csv"):
        dev = r["device_name"]
        L = lib.get(dev)
        if not L or L.get("Components Group") != COMP or L.get("Used Metal") != METAL:
            continue
        tau = fnum(r.get("exp decay: tau (s)"))
        if tau is None or tau <= 0:
            continue
        rows.append(dict(
            dev=dev, ln=np.log(tau), day=fnum(r.get("day")),
            peo=L.get("Ion-Conducting Polymer Mass Ratio"),
            salt=L.get("Salt Mass Ratio"),
            rpm=fnum(L.get("Spin Coating Rotational Speed [RPM]")),
            anneal=fnum(L.get("Annealing Temperature [°C]")),
            thick=prof.get(dev),
        ))

    # collapse to one ln(tau) per device (device-to-device, not pixel-to-pixel)
    dev_ln, meta = {}, {}
    for r in rows:
        dev_ln.setdefault(r["dev"], []).append(r["ln"])
        meta[r["dev"]] = r
    devs = sorted(dev_ln)
    ln = np.array([np.median(dev_ln[d]) for d in devs])
    cell = np.array([f"{meta[d]['peo']}|{meta[d]['salt']}" for d in devs])

    # --- variance decomposition -------------------------------------------------
    sigma_total = float(ln.std(ddof=1))   # pools the designed PEO x salt sweep -> inflated

    # within exact (PEO, salt) cell, for cells with >= MIN_DEV_PER_CELL devices
    within = []
    cell_sizes = {c: int((cell == c).sum()) for c in set(cell)}
    big = [c for c, n in cell_sizes.items() if n >= MIN_DEV_PER_CELL]
    for c in big:
        v = ln[cell == c]
        within.extend(v - np.median(v))
    sigma_within = float(np.std(within, ddof=1)) if len(within) > 1 else float("nan")
    n_within = len(within)

    # add RPM + anneal as further controls (composition cell fixed effects + covariates)
    ok = [i for i, d in enumerate(devs)
          if meta[d]["rpm"] is not None and meta[d]["anneal"] is not None
          and cell_sizes[cell[i]] >= MIN_DEV_PER_CELL]
    sigma_ctrl = float("nan")
    if len(ok) > 6:
        sub = [devs[i] for i in ok]
        y = ln[ok]
        cats = sorted(set(cell[ok]))
        D = np.zeros((len(ok), len(cats)))
        for j, i in enumerate(ok):
            D[j, cats.index(cell[i])] = 1.0
        rpm = np.array([meta[d]["rpm"] for d in sub]); rpm -= rpm.mean()
        ann = np.array([meta[d]["anneal"] for d in sub]); ann -= ann.mean()
        X = np.column_stack([D, rpm, ann])           # cell dummies already span the constant
        sigma_ctrl = ols_resid_std(y, X)

    # residual (within-cell) vs thickness and vs aging/day -- should be ~null
    cellmed = {c: np.median(ln[cell == c]) for c in set(cell)}
    resid = np.array([ln[i] - cellmed[cell[i]] for i in range(len(devs))])
    th = np.array([meta[d]["thick"] for d in devs], dtype=float)
    mth = np.isfinite(th)
    rho_thick = spearman(th[mth], resid[mth]) if mth.sum() > 5 else float("nan")
    n_thick = int(mth.sum()); n_dev_thick = int(np.isfinite(th).sum())
    # day at pixel level (more points than device medians)
    day = np.array([r["day"] for r in rows if r["day"] is not None], dtype=float)
    rday = np.array([r["ln"] - cellmed[f"{r['peo']}|{r['salt']}"]
                     for r in rows if r["day"] is not None], dtype=float)
    rho_day = spearman(day, rday) if len(day) > 5 else float("nan")

    headline = sigma_thalf

    # --- emit single source of truth -------------------------------------------
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, "ch5_scatter_audit.csv")
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["metric", "value", "n", "note"])
        w.writerow(["sigma_lnThalf_within_cell", round(headline, 4), n_thalf,
                    f"primary: median cell SD on screened substrate t_half; {n_cells} cells"])
        w.writerow(["sigma_lnThalf_cell_sd_min", round(sigma_min, 4), n_cells,
                    "minimum across replicated cells"])
        w.writerow(["sigma_lnThalf_cell_sd_max", round(sigma_max, 4), n_cells,
                    "maximum across replicated cells; sensitivity bound"])
        w.writerow(["sigma_lnTau_instrument_legacy", round(sigma_within, 4), n_within,
                    "secondary: unscreened instrument-fit tau; not primary jitter"])
        w.writerow(["sigma_lnTau_total_group", round(sigma_total, 4), len(devs),
                    "CONFLATED: pools designed PEO x salt sweep -- do not cite"])
        w.writerow(["sigma_lnTau_ctrl_rpm_anneal", round(sigma_ctrl, 4), len(ok),
                    "residual after cell + RPM + anneal"])
        w.writerow(["spearman_resid_thickness", round(rho_thick, 4), n_thick,
                    "within-cell residual vs film thickness (expect ~0)"])
        w.writerow(["spearman_resid_day", round(rho_day, 4), len(day),
                    "within-cell residual vs aging/day (expect ~0)"])
        w.writerow(["old_cited_value", OLD_CITED, "", "the undocumented number the figure used"])
        w.writerow(["thickness_coverage", f"{n_dev_thick}/{len(devs)}", "",
                    "devices with profilometry"])

    print("Between-substrate fading-memory scatter audit")
    print("-" * 64)
    print(f"  PRIMARY median cell SD ln(t_half) : {sigma_thalf:.3f}  "
          f"[n={n_thalf} substrates, {n_cells} cells]")
    print(f"  observed cell-SD range            : {sigma_min:.3f} to {sigma_max:.3f}")
    print("  legacy instrument-fit sensitivity:")
    print(f"  sigma(ln tau) total group         : {sigma_total:.2f}   <- CONFLATED (designed sweep)")
    print(f"  sigma(ln tau) WITHIN (PEO,salt)    : {sigma_within:.2f}   [n={n_within}]")
    print(f"  + control RPM & anneal (resid)     : {sigma_ctrl:.2f}")
    print(f"  resid vs thickness  rho={rho_thick:+.2f} (n={n_thick}); coverage {n_dev_thick}/{len(devs)}")
    print(f"  resid vs aging/day  rho={rho_day:+.2f} (n={len(day)})")
    print(f"  previously-cited undocumented value: {OLD_CITED}")
    print(f"\nwrote {out}")
    return headline


if __name__ == "__main__":
    main()
