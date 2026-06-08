#!/usr/bin/env python3
"""EIS corroboration of the composition -> ionic-transport mechanism (Chapter 4).

Run from the repo root:  python3 scripts/ch4_eis.py
Reads the (un-versioned) experimental DATABASE in ../Nanomem_Devices_Library/DATABASE
and the per-cell fading-memory ladder in handouts/ch4_decay_by_cell.csv
(written by scripts/ch4_dynamics_fits.py -- run that first).

What this does and why
----------------------
The chapter's mechanistic reading is that adding ion-transport polymer (PEO) lowers
the bulk ionic resistance, easing ionic redistribution and so shortening the
fading-memory time. EIS at 0 V DC tests that *independently* of the driven
pulse/decay measurements. We summarise each 0 V DC spectrum two ways:

  (1) MODEL-FREE  -- Zreal at the apex of the main Nyquist semicircle
      ('Zreal at Max -Zimag', from DEVICES_EIS_PIXEL_INFO). This is the headline:
      it commits to no circuit and is robust.
  (2) CIRCUIT     -- the fitted ionic resistance Rion of the MUNAR 0 V DC equivalent
      circuit. Of the two archived fits we use VARFREE (Gamry Echem Analyst, free fit
      with error estimates); the Python BOUNDS fit is over-constrained (Rion capped at
      10 MOhm, spectra smoothed, Nelder-Mead) and tracks composition more weakly.
      Per-pixel circuit fits are genuinely ill-conditioned, so the circuit Rion is
      reported only as corroboration of the model-free trend, not as a precise number.

Honesty notes
-------------
- Ag electrode only; 0 V DC only; PEO/LiTr composition spine only.
- The EIS *resistance* scale tracks composition and t_half; the EIS AC *relaxation
  time* (apex frequency) does NOT track the seconds-long fading-memory time -- EIS
  reports the small-signal ionic-transport bottleneck, not the slow relaxation clock.
- The resistance scale spans ~10^4x while film thickness spans only ~2.6x, and the
  PEO effect survives controlling for thickness (partial correlation), so this is a
  composition effect, not a geometric one (cf. the thickness-covariate argument in
  Section 4.2).
"""
import csv, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DB = "../Nanomem_Devices_Library/DATABASE"
OUT = "handouts"
FIGDIR = "figures/chapter4"

plt.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.titlesize": 9,
    "axes.labelsize": 9, "figure.dpi": 150, "savefig.bbox": "tight",
})


def load(f):
    with open(os.path.join(DB, f), newline="") as fh:
        return list(csv.DictReader(fh))


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


def med(v):
    v = [x for x in v if x is not None and np.isfinite(x)]
    return float(np.median(v)) if v else float("nan")


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return float(np.corrcoef(x, y)[0, 1])


def spearman(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return pearson(rx, ry)


def partial(x, y, z):
    """corr(x,y) controlling for z (all 1-D)."""
    def res(a, b):
        A = np.vstack([b, np.ones_like(b)]).T
        c, *_ = np.linalg.lstsq(A, a, rcond=None)
        return a - A @ c
    return pearson(res(np.asarray(x, float), np.asarray(z, float)),
                   res(np.asarray(y, float), np.asarray(z, float)))


# ---------------------------------------------------------------------------
# device -> (PEO, salt, electrode) for the SY/PEO/LiTr family
# ---------------------------------------------------------------------------
meta = {}
for r in load("UPDATED_DEVICES_LIBRARY.csv"):
    if (r.get("Components Group") or "").strip() != "SY, PEO, LiTr":
        continue
    ag = fnum(r.get("Ag Thickness [nm]"))
    meta[r["device_name"]] = (
        fnum(r.get("Ion-Conducting Polymer Mass Ratio")),
        fnum(r.get("Salt Mass Ratio")),
        "Ag" if (ag and ag > 0) else "Au",
    )

# fading-memory ladder (Li cells)
thalf = {}
with open(os.path.join(OUT, "ch4_decay_by_cell.csv"), newline="") as fh:
    for r in csv.DictReader(fh):
        if r["cation"] == "Li":
            thalf[(fnum(r["peo"]), fnum(r["salt"]))] = fnum(r["t_half_med"])

# ---------------------------------------------------------------------------
# (1) model-free: Zreal at Nyquist apex, 0 V DC, Ag
# ---------------------------------------------------------------------------
dev = {}  # device -> dict(peo,salt,zapex[list],thick[list])
for r in load("DEVICES_EIS_PIXEL_INFO.csv"):
    if fnum(r.get("DC Voltage (V)")) != 0.0:
        continue
    m = meta.get(r["device_name"])
    if not m or m[2] != "Ag" or m[0] is None:
        continue
    z = fnum(r.get("Zreal at Max -Zimag (ohm)"))
    if not z or z <= 0:
        continue
    d = dev.setdefault(r["device_name"], dict(peo=m[0], salt=m[1], z=[], t=[]))
    d["z"].append(z)
    d["t"].append(fnum(r.get("Average Thickness (nm)")))

devrows = []
for name, d in dev.items():
    devrows.append(dict(device=name, peo=d["peo"], salt=d["salt"],
                        zapex=med(d["z"]), thick=med(d["t"]),
                        thalf=thalf.get((d["peo"], d["salt"]))))

# (2) circuit Rion: VARFREE (primary) and BOUNDS (comparison)
def rion_by_dev(fname, col="Rion (ohm)", lo=1.0, hi=1e9):
    out = {}
    for r in load(fname):
        m = meta.get(r["device_name"])
        if not m or m[2] != "Ag":
            continue
        v = fnum(r.get(col))
        if v and lo < v < hi:
            out.setdefault(r["device_name"], []).append(v)
    return {k: med(v) for k, v in out.items()}

rion_vf = rion_by_dev("DEVICES_EIS_MUNAR0VDC_ECHEM_MODEL_VARFREE.csv")
rion_bd = rion_by_dev("DEVICES_EIS_MUNAR0VDC_PYTHON_MODEL_BOUNDS.csv", lo=0.2)
for row in devrows:
    row["rion_vf"] = rion_vf.get(row["device"])
    row["rion_bd"] = rion_bd.get(row["device"])

# ---------------------------------------------------------------------------
# per-cell medians + correlations
# ---------------------------------------------------------------------------
def cell_medians(key):
    cells = {}
    for row in devrows:
        v = row.get(key)
        if v is None or not np.isfinite(v) or v <= 0:
            continue
        cells.setdefault((row["peo"], row["salt"]), []).append(v)
    return {k: med(v) for k, v in cells.items()}


def report(key, label):
    cm = cell_medians(key)
    cells = [(k, v) for k, v in cm.items() if v > 0]
    rp = pearson([k[0] for k, _ in cells], [np.log10(v) for _, v in cells])
    pair = [(v, thalf[k]) for k, v in cells if k in thalf]
    rt = pearson([np.log10(a) for a, _ in pair], [np.log10(b) for _, b in pair]) if len(pair) > 2 else float("nan")
    print(f"  {label:24s} cells={len(cells):2d}  r(PEO,log)={rp:+.2f}  r(log,log t_half)={rt:+.2f}  [{len(pair)} paired]")
    return cm


def main():
    os.makedirs(FIGDIR, exist_ok=True)
    print(f"Model-free EIS devices (Ag, 0 V DC): {len(devrows)}")

    # per-device significance for the headline (model-free Zapex)
    md = [r for r in devrows if r["zapex"] and r["zapex"] > 0]
    rP = spearman([r["peo"] for r in md], [r["zapex"] for r in md])
    mt = [r for r in md if r["thalf"]]
    rT = pearson([np.log10(r["zapex"]) for r in mt], [np.log10(r["thalf"]) for r in mt])
    mh = [r for r in md if r["thick"] and np.isfinite(r["thick"])]
    pr = partial([np.log10(r["zapex"]) for r in mh], [r["peo"] for r in mh], [r["thick"] for r in mh])
    print(f"per-DEVICE  Spearman(PEO, Zapex)={rP:+.2f} (n={len(md)})  "
          f"r(log Zapex, log t_half)={rT:+.2f} (n={len(mt)})  "
          f"partial r(PEO,logZapex|thick)={pr:+.2f}")
    print("\nCell-level method comparison (correlation with PEO and independent t_half):")
    cm_z = report("zapex", "Zreal@apex (model-free)")
    report("rion_vf", "Rion VARFREE (Gamry)")
    report("rion_bd", "Rion BOUNDS (Python)")

    # write per-cell summary
    rows = []
    cm_vf = cell_medians("rion_vf")
    for k in sorted(set(cm_z) | set(cm_vf)):
        rows.append(dict(peo=k[0], salt=k[1],
                         zreal_apex_ohm=cm_z.get(k), rion_varfree_ohm=cm_vf.get(k),
                         t_half_s=thalf.get(k)))
    with open(os.path.join(OUT, "ch4_eis_by_cell.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"\nWrote {OUT}/ch4_eis_by_cell.csv")

    # ---- figure ----
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(7.4, 3.2))
    salt_levels = sorted({r["salt"] for r in md})
    cmap = {s: c for s, c in zip(salt_levels, ["#1f77b4", "#2ca02c", "#d62728", "#9467bd"])}

    # (a) Zapex vs PEO, per device coloured by salt, cell-median line
    for r in md:
        axA.scatter(r["peo"], r["zapex"], s=22, color=cmap.get(r["salt"], "gray"),
                    alpha=0.55, edgecolor="none", zorder=2)
    peos = sorted({k[0] for k in cm_z})
    cmed = [med([cm_z[k] for k in cm_z if k[0] == p]) for p in peos]
    axA.plot(peos, cmed, "k-o", lw=1.4, ms=4, zorder=3, label="PEO median")
    axA.set_yscale("log"); axA.set_xlabel("PEO mass fraction")
    axA.set_ylabel(r"$Z_{\mathrm{real}}$ at Nyquist apex ($\Omega$), 0 V DC")
    axA.set_title("(a) Ionic impedance vs composition")
    handles = [plt.Line2D([], [], marker="o", ls="", color=cmap[s], label=f"salt {s}") for s in salt_levels]
    handles.append(plt.Line2D([], [], marker="o", color="k", label="PEO median"))
    axA.legend(handles=handles, fontsize=6.5, frameon=False, loc="upper right")

    # (b) the EIS resistance scale and the (independently measured) fading-memory
    # time, both vs the shared PEO composition axis. Cell-level points + per-PEO
    # median trend for each: "one axis, two measurement types", no device-level
    # correlation coefficient to over-read; real cell spread is shown honestly.
    peo_levels = sorted({k[0] for k in cm_z} | {k[0] for k in thalf})
    z_by_peo = {p: med([cm_z[k] for k in cm_z if k[0] == p]) for p in peo_levels}
    t_by_peo = {p: med([thalf[k] for k in thalf if k[0] == p]) for p in peo_levels}

    c_eis, c_mem = "#1f4e79", "#b5651d"
    # EIS cells (left axis)
    for k, v in cm_z.items():
        axB.scatter(k[0], v, s=20, color=c_eis, alpha=0.4, edgecolor="none", zorder=2)
    pz = [p for p in peo_levels if np.isfinite(z_by_peo[p])]
    l1, = axB.plot(pz, [z_by_peo[p] for p in pz], "-o", color=c_eis, lw=1.6, ms=5, zorder=3)
    axB.set_yscale("log")
    axB.set_xlabel("PEO mass fraction")
    axB.set_ylabel(r"EIS $Z_{\mathrm{real}}$ at apex ($\Omega$)", color=c_eis)
    axB.tick_params(axis="y", labelcolor=c_eis)
    axB.set_title("(b) Two measurements, one composition axis")

    axB2 = axB.twinx()
    for k, v in thalf.items():
        if v and np.isfinite(v):
            axB2.scatter(k[0], v, s=20, marker="s", color=c_mem, alpha=0.4, edgecolor="none", zorder=2)
    pt = [p for p in peo_levels if np.isfinite(t_by_peo[p])]
    l2, = axB2.plot(pt, [t_by_peo[p] for p in pt], "--s", color=c_mem, lw=1.6, ms=5, zorder=3)
    axB2.set_yscale("log")
    axB2.set_ylabel(r"fading-memory time $t_{1/2}$ (s)", color=c_mem)
    axB2.tick_params(axis="y", labelcolor=c_mem)
    axB.legend([l1, l2], ["EIS ionic impedance", r"fading memory $t_{1/2}$"],
               fontsize=6.5, frameon=False, loc="lower left")

    fig.tight_layout()
    out = os.path.join(FIGDIR, "eis_ionic.pdf")
    fig.savefig(out); print(f"Wrote {out}")


if __name__ == "__main__":
    main()
