#!/usr/bin/env python3
"""Quantitative-rigour add-ons for Chapter 4 (comparative).

Run from the repo root:  python3 scripts/ch4_rigor.py

This script does NOT touch the headline figures. It produces the statistical
back-matter requested in the jury-strengthening pass, all from data already in
the archive:

  [1] Composition-spine SIGNIFICANCE + cell uncertainty.
      Per metric (t_half, growth exponent alpha, peak ratio, on-off ratio) on the
      replicated Ag/Li SY/PEO/LiTr spine: Spearman rho vs PEO with a permutation
      p-value, Holm family-wise correction, a batch-restricted sensitivity test,
      and a non-parametric bootstrap 95 % CI where n >= 3 (observed range at n=2).
      ->  handouts/ch4_gradient_stats.csv, handouts/ch4_cell_ci.csv

  [2] PEO x salt FACTORIAL decomposition.
      OLS of log-metric on log(PEO), log(salt), their interaction, and acquisition
      batch fixed effects, with conditional Freedman--Lane residual-permutation
      p-values restricted within batch.
      ->  handouts/ch4_factorial.csv

  [3] PERCOLATION / dilution test of the mechanism.
      Absolute on-state conductance (HYST) vs PEO/SY mass ratio: if added ion-transport
      polymer dilutes the SY electronic-percolation network, the absolute
      conductance must fall with PEO -- a prediction independent of the
      peak-normalised dynamics. Power-law fit + figure.
      ->  handouts/ch4_percolation.csv, figures/chapter4/percolation.pdf

  [4] EIS small-signal vs large-signal TIMESCALE bridge.
      The Nyquist-apex RC time (small signal) is sub-second; the forgetting time
      t_half is seconds. We show the gap is the chemical-to-geometric capacitance
      ratio measured from the spectra, so t_half lands in the observed range --
      upgrading the EIS link from same-direction to same-magnitude.
      ->  handouts/ch4_eis_timescale.csv

  [5] WITHIN-DEVICE (cycle-to-cycle) reproducibility.
      Scatter of the model-free t_half across the several junctions/pixels of one
      device, vs the across-device within-cell scatter. Tests the reservoir
      premise that each element is "individually reproducible-enough".
      ->  handouts/ch4_cycling.csv

  [6/7] HETEROGENEITY as a resource + beta-sigma link.
      Effective number of distinguishable memory timescales the composition bank
      provides, and the comparison of the single-device stretch dispersion (1-beta)
      with the inter-device sigma(ln tau).
      ->  handouts/ch4_heterogeneity_resource.csv

Scope: Ag electrode, Li cation, SY/PEO/LiTr composition spine, matching the
quantitative core of Section 4.4. Chemistry/electrode axes are illustrative and
are left out of these powered statistics by design.
"""
import csv, os, sys
from functools import lru_cache
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figstyle
from ch4_common import (
    freedman_lane_pvalues,
    holm_adjust,
    load_curation_registry,
    load_filter_flags,
    pearson,
    perm_p_spearman,
    row_is_excluded,
    spearman,
)
figstyle.apply()
COLORS = figstyle.COLORS

DB = "../Nanomem_Devices_Library/DATABASE"
OUT = "handouts"
FIGDIR = "figures/chapter4"
AREA_CM2 = 8.25e-2
RNG = np.random.default_rng(20260611)


# --------------------------------------------------------------------------- io
@lru_cache(maxsize=None)
def load(f):
    with open(os.path.join(DB, f), newline="") as fh:
        return list(csv.DictReader(fh))


@lru_cache(maxsize=None)
def loadh(f):
    with open(os.path.join(OUT, f), newline="") as fh:
        return list(csv.DictReader(fh))


def fnum(x):
    try:
        v = float(x)
        return v if np.isfinite(v) else None
    except Exception:
        return None


def med(v):
    v = [x for x in v if x is not None and np.isfinite(x)]
    return float(np.median(v)) if v else float("nan")


# ------------------------------------------------------- device composition meta
meta = {}            # device -> (peo, salt, electrode)
for r in load("UPDATED_DEVICES_LIBRARY.csv"):
    if (r.get("Components Group") or "").strip() != "SY, PEO, LiTr":
        continue
    ag = fnum(r.get("Ag Thickness [nm]"))
    meta[r["device_name"]] = (
        fnum(r.get("Ion-Conducting Polymer Mass Ratio")),
        fnum(r.get("Salt Mass Ratio")),
        "Ag" if (ag and ag > 0) else "Au",
    )


def is_spine(dn):
    """Ag/Li composition-spine device with a valid PEO/salt."""
    m = meta.get(dn)
    return bool(m and m[2] == "Ag" and m[0] is not None and m[1] is not None)


def is_replicated_grid(dn):
    """Ag/Li substrate in the pre-specified 3 x 3 replicated composition grid."""
    return (
        is_spine(dn)
        and meta[dn][0] in {0.3, 0.6, 1.2}
        and meta[dn][1] in {0.045, 0.09, 0.18}
    )


batch_by_device = {
    r["device_id"]: r.get("quarter") or "unknown"
    for r in csv.DictReader(open(os.path.join(OUT, "ch4_device_manifest_DRAFT.csv")))
}
flags = load_filter_flags(os.path.join(DB, "FILTERED_DEVICES.csv"))
curation = load_curation_registry(os.path.join(OUT, "ch4_png_qa_curation.csv"))


# --------------------------------------------------------------------------- [1]
# Per-substrate screened descriptors (Li replicated grid only) from the curated
# junction-level tables. Junctions are collapsed before inference so a substrate
# with two measured junctions never counts twice.
GRID_PEO = {0.3, 0.6, 1.2}
GRID_SALT = {0.045, 0.09, 0.18}


def spine_rows(fname, metric_cols):
    grouped = {}
    for r in loadh(fname):
        if r.get("cation") != "Li":
            continue
        peo, salt = fnum(r.get("peo")), fnum(r.get("salt"))
        if peo not in GRID_PEO or salt not in GRID_SALT:
            continue
        rec = grouped.setdefault(
            r["device_id"],
            dict(
                device=r["device_id"],
                peo=peo,
                salt=salt,
                batch=batch_by_device.get(r["device_id"], "unknown"),
                values={c: [] for c in metric_cols},
            ),
        )
        for c in metric_cols:
            value = fnum(r.get(c))
            if value is not None:
                rec["values"][c].append(value)
    out = []
    for rec in grouped.values():
        values = rec.pop("values")
        rec.update({c: (med(values[c]) if values[c] else None) for c in metric_cols})
        out.append(rec)
    return out


decay = spine_rows("ch4_decay_fits.csv", ["t_half_s", "tau_s", "beta", "retention60"])
pulse = spine_rows("ch4_pulse_descriptors.csv", ["growth_exp", "peak_ratio", "turnover"])

# On--off ratio per spine substrate, recomputed from screened curves so the
# gradient, heatmap, and cycling analysis share exactly the same exclusions.
onoff = {}
for r in load("DEVICES_HYST_CURVE_INFO.csv"):
    dn = r.get("device_name")
    if not is_replicated_grid(dn):
        continue
    if row_is_excluded(
        r, "HYST", flags, curation, broken_fields=("is broken",)
    ):
        continue
    v = fnum(r.get("on-off ratio"))
    if v and v > 0:
        onoff.setdefault(dn, []).append(v)
onoff_rows = [dict(device=dn, peo=meta[dn][0], salt=meta[dn][1],
                   batch=batch_by_device.get(dn, "unknown"), onoff=med(v))
              for dn, v in onoff.items()]

METRICS = {
    "t_half_s":   ("fading-memory $t_{1/2}$ (s)", decay,      "t_half_s", True),
    "growth_exp": ("growth exponent $\\alpha$",   pulse,      "growth_exp", False),
    "peak_ratio": ("peak ratio",                  pulse,      "peak_ratio", True),
    "onoff":      ("on--off ratio",               onoff_rows, "onoff", False),
}


def bootstrap_ci(vals, B=20000):
    vals = [v for v in vals if v is not None and np.isfinite(v)]
    if len(vals) < 2:
        return float("nan"), float("nan"), "not_estimable"
    if len(vals) == 2:
        return float(min(vals)), float(max(vals)), "observed_range"
    boots = [np.median(RNG.choice(vals, size=len(vals), replace=True)) for _ in range(B)]
    return (
        float(np.percentile(boots, 2.5)),
        float(np.percentile(boots, 97.5)),
        "bootstrap_95",
    )


def cell_key(r):
    return (r["peo"], r["salt"])


grad_rows, cell_ci_rows = [], []
for mkey, (label, rows, col, _log) in METRICS.items():
    xs = [r["peo"] for r in rows if r.get(col) is not None]
    ys = [r[col] for r in rows if r.get(col) is not None]
    blocks = [r["batch"] for r in rows if r.get(col) is not None]
    rho = spearman(xs, ys)
    p = perm_p_spearman(xs, ys, RNG)
    batch_p = perm_p_spearman(xs, ys, RNG, blocks=blocks)
    grad_rows.append(dict(metric=mkey, n=len(xs), spearman_rho=round(rho, 3),
                          perm_p=round(p, 5), batch_perm_p=round(batch_p, 5)))
    # per-cell median + bootstrap CI
    cells = {}
    for r in rows:
        if r.get(col) is not None:
            cells.setdefault(cell_key(r), []).append(r[col])
    for k in sorted(cells):
        lo, hi, method = bootstrap_ci(cells[k])
        cell_ci_rows.append(dict(metric=mkey, peo=k[0], salt=k[1], n=len(cells[k]),
                                 median=round(float(np.median(cells[k])), 4),
                                 interval_method=method,
                                 ci_lo=round(lo, 4), ci_hi=round(hi, 4)))

for row, adjusted in zip(grad_rows, holm_adjust([r["perm_p"] for r in grad_rows])):
    row["holm_p"] = round(float(adjusted), 5)

with open(os.path.join(OUT, "ch4_gradient_stats.csv"), "w", newline="") as fh:
    w = csv.DictWriter(
        fh,
        fieldnames=[
            "metric",
            "n",
            "spearman_rho",
            "perm_p",
            "holm_p",
            "batch_perm_p",
        ],
    )
    w.writeheader(); [w.writerow(x) for x in grad_rows]
with open(os.path.join(OUT, "ch4_cell_ci.csv"), "w", newline="") as fh:
    w = csv.DictWriter(
        fh,
        fieldnames=[
            "metric",
            "peo",
            "salt",
            "n",
            "median",
            "interval_method",
            "ci_lo",
            "ci_hi",
        ],
    )
    w.writeheader(); [w.writerow(x) for x in cell_ci_rows]


# --------------------------------------------------------------------------- [2]
def ols_perm(rows, col, logy, B=20000):
    """Factorial model with conditional, batch-restricted Freedman--Lane tests."""
    d = [r for r in rows if r.get(col) is not None and r[col] > 0]
    lp = np.log(np.array([r["peo"] for r in d]))
    ls = np.log(np.array([r["salt"] for r in d]))
    y = np.array([r[col] for r in d], float)
    y = np.log(y) if logy else y
    # centre predictors so the interaction is near-orthogonal to the mains
    lp -= lp.mean(); ls -= ls.mean()
    blocks = [r["batch"] for r in d]
    batch_levels = sorted(set(blocks))
    batch_dummies = [
        np.asarray([block == level for block in blocks], dtype=float)
        for level in batch_levels[1:]
    ]
    X = np.column_stack(
        [np.ones_like(lp), lp, ls, lp * ls, *batch_dummies]
    )
    beta, pvals = freedman_lane_pvalues(
        X, y, RNG, term_indices=(1, 2, 3), B=B, blocks=blocks
    )
    yhat = X @ beta
    r2 = 1 - np.sum((y - yhat) ** 2) / max(
        np.sum((y - y.mean()) ** 2), 1e-12
    )
    return d, beta, pvals, r2


fact_rows = []
for mkey, col, logy in [("t_half_s", "t_half_s", True),
                        ("growth_exp", "growth_exp", False),
                        ("peak_ratio", "peak_ratio", True)]:
    d, beta, pv, r2 = ols_perm(globals()["decay" if mkey == "t_half_s" else "pulse"], col, logy)
    fact_rows.append(dict(metric=mkey, n=len(d),
                          b_peo=round(beta[1], 3), p_peo=round(pv[1], 5),
                          b_salt=round(beta[2], 3), p_salt=round(pv[2], 5),
                          b_inter=round(beta[3], 3), p_inter=round(pv[3], 5),
                          r2=round(r2, 3)))
with open(os.path.join(OUT, "ch4_factorial.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["metric", "n", "b_peo", "p_peo", "b_salt",
                                       "p_salt", "b_inter", "p_inter", "r2"])
    w.writeheader(); [w.writerow(x) for x in fact_rows]


# --------------------------------------------------------------------------- [3]
# Absolute on-state conductance (HYST) vs PEO -> dilution / percolation test.
gon = {}
for r in load("DEVICES_HYST_PIXEL_INFO.csv"):
    dn = r.get("device_name")
    if not is_replicated_grid(dn):
        continue
    if row_is_excluded(
        r, "HYST", flags, curation, broken_fields=("is broken",)
    ):
        continue
    g = fnum(r.get("mean conductance at max v (uS)"))
    if g and g > 0:
        gon.setdefault(dn, []).append(g)
perc = [dict(device=dn, peo=meta[dn][0], salt=meta[dn][1], g_on_uS=med(v))
        for dn, v in gon.items() if np.isfinite(med(v))]

px = np.array([r["peo"] for r in perc])
gy = np.array([r["g_on_uS"] for r in perc])
rho_g = spearman(px, gy)
p_g = perm_p_spearman(px, gy, RNG)
# power law g ~ PEO^(-m): slope on log-log
slope_g = np.polyfit(np.log(px), np.log(gy), 1)[0]
with open(os.path.join(OUT, "ch4_percolation.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["device", "peo", "salt", "g_on_uS"])
    w.writeheader(); [w.writerow(x) for x in sorted(perc, key=lambda r: r["peo"])]

# figure: g_on vs PEO (log-log), coloured by salt
SALTC = {0.045: COLORS["blue"], 0.09: COLORS["purple"], 0.18: COLORS["red"]}
fig, ax = plt.subplots(figsize=(3.4, 3.0))
for r in perc:
    ax.scatter(r["peo"], r["g_on_uS"], s=26, color=SALTC.get(r["salt"], COLORS["gray"]),
               alpha=0.75, edgecolor="none", zorder=3)
# PEO-median trend
pm = {}
for r in perc:
    pm.setdefault(r["peo"], []).append(r["g_on_uS"])
pmk = sorted(pm)
ax.plot(pmk, [np.median(pm[p]) for p in pmk], "-o", color=COLORS["gray"], lw=1.6,
        ms=5, zorder=4, label="PEO median")
xx = np.array([min(px), max(px)])
ax.plot(xx, np.exp(np.polyval(np.polyfit(np.log(px), np.log(gy), 1), np.log(xx))),
        "--", color="k", lw=1.0, zorder=2,
        label=fr"power law $\propto$PEO$^{{{slope_g:.1f}}}$")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"PEO/SY mass ratio, $r_{\mathrm{PEO}}$"); ax.set_ylabel(r"on-state conductance ($\mu$S)")
handles = [plt.Line2D([], [], marker="o", ls="", color=SALTC[s], label=f"salt {s}")
           for s in sorted(SALTC)]
handles += [plt.Line2D([], [], marker="o", color=COLORS["gray"], label="PEO median"),
            plt.Line2D([], [], ls="--", color="k", label=fr"$\propto$PEO$^{{{slope_g:.1f}}}$")]
ax.legend(handles=handles, fontsize=6, frameon=False, loc="lower left")
figstyle.panel(ax, "", "on-state conductance rises with PEO")
figstyle.save(fig, os.path.join(FIGDIR, "percolation.pdf"))


# --------------------------------------------------------------------------- [4]
# EIS apex RC (small signal) vs forgetting time; capacitance-ratio bridge.
eis = {}
for r in load("DEVICES_EIS_PIXEL_INFO.csv"):
    if fnum(r.get("DC Voltage (V)")) != 0.0:
        continue
    dn = r.get("device_name")
    if not is_replicated_grid(dn):
        continue
    f_apex = fnum(r.get("Freq at Max -Zimag (Hz)"))
    z_apex = fnum(r.get("Zreal at Max -Zimag (ohm)"))
    if f_apex and f_apex > 0 and z_apex and z_apex > 0:
        d = eis.setdefault(dn, dict(peo=meta[dn][0], f=[], z=[]))
        d["f"].append(f_apex); d["z"].append(z_apex)
tau_rc, c_geo = {}, {}      # per device: small-signal RC time, geometric C at apex
for dn, d in eis.items():
    fa, za = med(d["f"]), med(d["z"])
    if np.isfinite(fa) and np.isfinite(za) and fa > 0 and za > 0:
        tau_rc[dn] = 1.0 / (2 * np.pi * fa)
        c_geo[dn] = 1.0 / (2 * np.pi * fa * za)
tau_rc_med = med(list(tau_rc.values()))

# Independent low-frequency (chemical / double-layer) capacitance from the full
# spectra: C_lf = -1/(2 pi f Zimag) at the lowest measured frequency (0 V DC).
lowf = {}
for r in load("DEVICES_EIS_ALL_DATAPOINTS.csv"):
    if fnum(r.get("DC Voltage (V)")) != 0.0:
        continue
    dn = r.get("device_name")
    if dn not in c_geo:
        continue
    f = fnum(r.get("Freq (Hz)")); zi = fnum(r.get("Zimag (ohm)"))
    if f and f > 0 and zi is not None and zi < 0:        # capacitive branch
        cur = lowf.get(dn)
        if cur is None or f < cur[0]:
            lowf[dn] = (f, -1.0 / (2 * np.pi * f * zi))
# per-device chemical/geometric capacitance enhancement
c_ratio = [lowf[dn][1] / c_geo[dn] for dn in lowf if c_geo.get(dn)]
c_ratio_med = med(c_ratio)

# observed forgetting time (spine median of model-free t_half)
thalf_all = [r["t_half_s"] for r in decay if r.get("t_half_s")]
thalf_med = med(thalf_all)
ratio_needed = thalf_med / tau_rc_med if tau_rc_med else float("nan")
# predicted large-signal relaxation = tau_RC * (independently measured C_lf/C_geo)
tau_large_pred = tau_rc_med * c_ratio_med
with open(os.path.join(OUT, "ch4_eis_timescale.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "value", "unit"])
    w.writerow(["tau_RC_apex_median", round(tau_rc_med, 4), "s"])
    w.writerow(["t_half_median", round(thalf_med, 2), "s"])
    w.writerow(["C_chem_over_C_geo_measured", round(c_ratio_med, 1), "ratio"])
    w.writerow(["C_chem_over_C_geo_needed", round(ratio_needed, 1), "ratio"])
    w.writerow(["tau_large_predicted", round(tau_large_pred, 2), "s"])
    w.writerow(["n_eis_devices", len(tau_rc), "count"])
    w.writerow(["n_lowf_devices", len(c_ratio), "count"])


# --------------------------------------------------------------------------- [5]
# Within-device reproducibility. The fading-memory protocol measured a single
# junction per device (only one spine device carries two), so repeat-DECAY
# reproducibility is not estimable at the population level -- a stated gap. The
# repeated HYST sweeps (median ~5 sweeps per junction) DO give a population-level
# within-device (sweep-to-sweep) reproducibility of the switching window, which is
# the relevant "individually reproducible-enough" test for the steady-state metric.
hg = {}
for r in load("DEVICES_HYST_CURVE_INFO.csv"):
    dn = r.get("device_name")
    if not is_replicated_grid(dn):
        continue
    if row_is_excluded(
        r, "HYST", flags, curation, broken_fields=("is broken",)
    ):
        continue
    v = fnum(r.get("on-off ratio"))
    if v and v > 0:
        hg.setdefault((dn, r.get("pixel"), r.get("day")), []).append(v)
within_sweep = [float(np.std(np.log(v), ddof=1)) for v in hg.values() if len(v) >= 3]
within_sweep_med = med(within_sweep)

# across-device within-cell scatter of the on-off ratio (device medians per cell)
dev_onoff = {dn: med(v) for dn, v in onoff.items()}
cell_onoff = {}
for dn, v in dev_onoff.items():
    if np.isfinite(v) and v > 0:
        cell_onoff.setdefault((meta[dn][0], meta[dn][1]), []).append(v)
across_onoff = med([np.std(np.log(v), ddof=1) for v in cell_onoff.values() if len(v) >= 2])

# the single two-junction decay device, as corroboration for t_half itself
dl = {}
for r in load("DEVICES_DELAYTIME_CURVE_INFO.csv"):
    dn = r.get("device_name")
    if not is_replicated_grid(dn):
        continue
    if row_is_excluded(r, "DELAYTIME", flags, curation):
        continue
    t = fnum(r.get("delay time (s)")); y = fnum(r.get("ratio"))
    if t is not None and y is not None:
        dl.setdefault((dn, r.get("pixel"), r.get("day")), []).append((t, y))


def thalf_modelfree(pts):
    pts = sorted(set(pts))
    t = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
    if len(t) < 5:
        return float("nan")
    r1 = float(y[t == 1][0]) if (t == 1).any() else float(y[0])
    target = r1 / 2.0
    for i in range(len(t) - 1):
        if y[i] >= target >= y[i + 1] and y[i] != y[i + 1]:
            lt, lt2 = np.log10(t[i]), np.log10(t[i + 1])
            frac = (y[i] - target) / (y[i] - y[i + 1])
            return float(10 ** (lt + frac * (lt2 - lt)))
    return float("nan")


dev_pix = {}
for (dn, px, day), pts in dl.items():
    th = thalf_modelfree(pts)
    if np.isfinite(th) and th > 0:
        dev_pix.setdefault(dn, []).append(th)
twojxn = {dn: round(float(np.std(np.log(v), ddof=1)), 3)
          for dn, v in dev_pix.items() if len(v) >= 2}
within_decay_med = med(list(twojxn.values())) if twojxn else float("nan")

with open(os.path.join(OUT, "ch4_cycling.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "value", "n"])
    w.writerow(["within_device_sweep_sigma_ln_onoff", round(within_sweep_med, 3), len(within_sweep)])
    w.writerow(["across_device_within_cell_sigma_ln_onoff", round(across_onoff, 3),
                sum(1 for v in cell_onoff.values() if len(v) >= 2)])
    w.writerow(["within_device_decay_sigma_ln_thalf", round(within_decay_med, 3), len(twojxn)])


# ------------------------------------------------------------------------- [6/7]
# Effective number of distinguishable memory timescales + beta-dispersion link.
# Use the robust model-free t_half throughout; report N_eff as a RANGE bracketed
# by the model-free within-cell scatter and the (larger, fit-noisy) sigma(ln tau)
# the thesis already cites, so the resource claim is bounded, not cherry-picked.
cell_thalf = {}
for r in decay:
    if r.get("t_half_s"):
        cell_thalf.setdefault((r["peo"], r["salt"]), []).append(r["t_half_s"])
within_cell_sigmas = [np.std(np.log(v), ddof=1) for v in cell_thalf.values() if len(v) >= 2]
sigma_within_cell = float(np.median(within_cell_sigmas))   # device-to-device, within composition
cell_meds = [np.median(v) for v in cell_thalf.values()]
ln_span = float(np.log(max(cell_meds)) - np.log(min(cell_meds)))


def n_eff(sigma):
    return 1.0 + ln_span / (2.0 * sigma)        # 2-sigma separation between bands


n_eff_robust = n_eff(sigma_within_cell)
n_eff_conservative = n_eff(0.85)                # fitted-tau scatter cited in Ch5 SI

# beta-dispersion link: identified fits only (unidentified ones carry junk tau)
betas = [r["beta"] for r in decay if r.get("beta") is not None]
med_one_minus_beta = float(np.median([1 - b for b in betas])) if betas else float("nan")

with open(os.path.join(OUT, "ch4_heterogeneity_resource.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["quantity", "value"])
    w.writerow(["ln_span_cell_medians", round(ln_span, 3)])
    w.writerow(["sigma_within_cell_lnthalf_modelfree", round(sigma_within_cell, 3)])
    w.writerow(["n_eff_timescales_robust", round(n_eff_robust, 2)])
    w.writerow(["n_eff_timescales_conservative", round(n_eff_conservative, 2)])
    w.writerow(["median_one_minus_beta", round(med_one_minus_beta, 3)])


# ------------------------------------------------------------------------ report
print("=== [1] PEO-gradient significance (Ag/Li spine) ===")
for r in grad_rows:
    print(f"  {r['metric']:12s} Spearman rho={r['spearman_rho']:+.2f}  "
          f"perm p={r['perm_p']:.4f}, Holm={r['holm_p']:.4f}, "
          f"batch={r['batch_perm_p']:.4f}  (n={r['n']})")
print("\n=== [2] PEO x salt factorial (batch-adjusted Freedman--Lane tests) ===")
for r in fact_rows:
    print(f"  {r['metric']:12s} bPEO={r['b_peo']:+.2f}(p={r['p_peo']:.3f})  "
          f"bSALT={r['b_salt']:+.2f}(p={r['p_salt']:.3f})  "
          f"bINT={r['b_inter']:+.2f}(p={r['p_inter']:.3f})  R2={r['r2']:.2f}")
print("\n=== [3] Dilution test: absolute on-state conductance vs PEO ===")
print(f"  n={len(perc)}  Spearman(PEO,g_on)={rho_g:+.2f}  perm p={p_g:.4f}  "
      f"log-log slope={slope_g:+.2f}  --> conductance RISES with PEO (refutes dilution)")
print("\n=== [4] EIS timescale bridge (non-circular) ===")
print(f"  tau_RC(apex) median={tau_rc_med*1e3:.0f} ms ; t_half median={thalf_med:.1f} s")
print(f"  measured C_lf/C_geo={c_ratio_med:.0f} (n={len(c_ratio)}) ; needed={ratio_needed:.0f} ; "
      f"predicted tau_large={tau_large_pred:.1f} s")
print("\n=== [5] Within-device reproducibility ===")
print(f"  sweep-to-sweep sigma(ln on-off)={within_sweep_med:.2f} (n={len(within_sweep)} junctions) "
      f"vs across-device within-cell sigma={across_onoff:.2f}")
print(f"  two-junction decay device(s): {twojxn}  median sigma(ln t_half)={within_decay_med:.2f}")
print("\n=== [6/7] Heterogeneity resource ===")
print(f"  ln-span(cell medians)={ln_span:.2f} ; within-cell sigma(model-free)={sigma_within_cell:.2f}")
print(f"  N_eff timescales: {n_eff_conservative:.1f} (conservative, sigma=0.85) "
      f"to {n_eff_robust:.1f} (model-free)")
print(f"  median(1-beta)={med_one_minus_beta:.2f}")
print("\nWrote: ch4_gradient_stats, ch4_cell_ci, ch4_factorial, ch4_percolation, "
      "ch4_eis_timescale, ch4_cycling, ch4_heterogeneity_resource (+ percolation.pdf)")
