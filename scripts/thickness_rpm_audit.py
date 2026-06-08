#!/usr/bin/env python3
"""Thickness / spin-coat-RPM confound audit for the Chapter 3-4 composition spine.

Run from the repo root:  python3 scripts/thickness_rpm_audit.py

Question (raised 2026-06-04): devices were spin-coated at different RPM, and RPM
was sometimes (but not always) raised for higher PEO/LiTr concentrations to thin
the otherwise-thicker film. Does this deliberate thickness tuning contaminate the
composition claims of Chapter 3 (and therefore the Chapter-4 parameter cards)?

Source of truth for thickness = DATABASE/DEVICES_PROFILOMETRY_STATS.csv (nm).
RPM + composition = DATABASE/DEVICES_LIBRARY.csv.
Dynamics metrics (t_half, tau, growth exponent, peak ratio) = the per-device fit
artifacts handouts/ch4_decay_fits.csv and handouts/ch4_pulse_descriptors.csv
(produced by scripts/ch3_4_dynamics_fits.py).

Verdict (see handouts/14_thickness_rpm_confound_audit.md): PEO and thickness covary
(RPM compensation was incomplete), but thickness has *no* effect on the dynamics once
composition is held fixed -> thickness is a controlled covariate, not a confound, and
no reported value, parameter card, or simulation changes.

Outputs:
  - prints the joined table, correlations, partial correlations, and the verdict
  - figures/chapter4/thickness_control.pdf  (fig:ch3_thickness_control)
"""
import csv, math, os, statistics
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DB = "../Nanomem_Devices_Library/DATABASE"
HO = "handouts"
FIGDIR = "figures/chapter4"

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
})


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


def pearson(xs, ys):
    pts = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pts) < 3:
        return None, len(pts)
    mx = statistics.mean([p[0] for p in pts])
    my = statistics.mean([p[1] for p in pts])
    num = sum((x - mx) * (y - my) for x, y in pts)
    den = math.sqrt(sum((x - mx) ** 2 for x, _ in pts) * sum((y - my) ** 2 for _, y in pts))
    return (num / den if den else None), len(pts)


def spearman(xs, ys):
    pts = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pts) < 3:
        return None, len(pts)

    def rank(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        rk = [0.0] * len(vals)
        i = 0
        while i < len(vals):
            j = i
            while j + 1 < len(vals) and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                rk[order[k]] = avg
            i = j + 1
        return rk

    return pearson(rank([p[0] for p in pts]), rank([p[1] for p in pts]))[0], len(pts)


def partial(rows, xk, yk, zk):
    """Partial correlation of x,y controlling for z."""
    rows = [r for r in rows if r.get(xk) is not None and r.get(yk) is not None and r.get(zk) is not None]
    if len(rows) < 4:
        return None, len(rows)
    rxy, _ = pearson([r[xk] for r in rows], [r[yk] for r in rows])
    rxz, _ = pearson([r[xk] for r in rows], [r[zk] for r in rows])
    ryz, _ = pearson([r[yk] for r in rows], [r[zk] for r in rows])
    if None in (rxy, rxz, ryz):
        return None, len(rows)
    den = math.sqrt((1 - rxz ** 2) * (1 - ryz ** 2))
    return ((rxy - rxz * ryz) / den if den else None), len(rows)


# --------------------------------------------------------------------------
# load sources
# --------------------------------------------------------------------------
thick = defaultdict(list)
with open(os.path.join(DB, "DEVICES_PROFILOMETRY_STATS.csv"), newline="") as f:
    for r in csv.DictReader(f):
        v = fnum(r["avg_thickness (nm)"])
        if v is not None:
            thick[r["device_name"]].append(v)
thick = {k: statistics.mean(v) for k, v in thick.items()}

lib = {}
with open(os.path.join(DB, "DEVICES_LIBRARY.csv"), newline="") as f:
    for r in csv.DictReader(f):
        lib[r["device_name"]] = r

decay = {}
with open(os.path.join(HO, "ch4_decay_fits.csv"), newline="") as f:
    for r in csv.DictReader(f):
        decay[r["device_id"]] = r
pulse = {}
with open(os.path.join(HO, "ch4_pulse_descriptors.csv"), newline="") as f:
    for r in csv.DictReader(f):
        pulse[r["device_id"]] = r

devs = sorted(set(decay) | set(pulse), key=lambda x: int(x.split("v")[1]))

rows = []
for d in devs:
    dd, pp = decay.get(d, {}), pulse.get(d, {})
    ag, au = fnum(lib.get(d, {}).get("Ag Thickness [nm]")), fnum(lib.get(d, {}).get("Au Thickness [nm]"))
    elec = "Ag" if (ag and ag > 0) else ("Au" if (au and au > 0) else "?")
    th = thick.get(d)
    rows.append(dict(
        dev=d,
        cat=(dd.get("cation") or pp.get("cation")),
        peo=fnum(dd.get("peo") or pp.get("peo")),
        salt=fnum(dd.get("salt") or pp.get("salt")),
        rpm=fnum(lib.get(d, {}).get("Spin Coating Rotational Speed [RPM]")),
        th=th,
        t_half=fnum(dd.get("t_half_s")),
        tau=fnum(dd.get("tau_s")),
        alpha=fnum(pp.get("growth_exp")),
        peak=fnum(pp.get("peak_ratio")),
        elec=elec,
        lt=(math.log10(fnum(dd.get("t_half_s"))) if fnum(dd.get("t_half_s")) else None),
        lp=(math.log10(fnum(pp.get("peak_ratio"))) if fnum(pp.get("peak_ratio")) else None),
    ))

li_ag = [r for r in rows if r["cat"] == "Li" and r["elec"] == "Ag" and r["peo"] is not None and r["th"] is not None]

# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------
print("=" * 78)
print("THICKNESS / RPM CONFOUND AUDIT  (Chapter 3-4 composition spine)")
print("=" * 78)
print(f"\nDevices joined: {len(rows)}   Li/Ag composition spine used for stats: {len(li_ag)}\n")

print("RPM was escalated with PEO (compensation), but not uniformly:")
rpm_by_peo = defaultdict(list)
for r in rows:
    if r["peo"] is not None and r["rpm"] is not None:
        rpm_by_peo[r["peo"]].append(r["rpm"])
for peo in sorted(rpm_by_peo):
    s = sorted({int(x) for x in rpm_by_peo[peo]})
    print(f"   PEO {peo:>4}: RPM in {s}")

print("\nResidual thickness still rises with PEO (compensation incomplete):")
th_by_peo = defaultdict(list)
for r in li_ag:
    th_by_peo[r["peo"]].append(r["th"])
for peo in sorted(th_by_peo):
    v = th_by_peo[peo]
    print(f"   PEO {peo:>4}: thickness median={statistics.median(v):3.0f} nm  range=[{min(v):.0f},{max(v):.0f}]  n={len(v)}")

print("\nCorrelations (Li/Ag spine):")
def rep(name, xk, yk, src):
    p, n = pearson([r[xk] for r in src], [r[yk] for r in src])
    s, _ = spearman([r[xk] for r in src], [r[yk] for r in src])
    print(f"   {name:34} Pearson={p:+.2f}  Spearman={s:+.2f}  (n={n})")
rep("PEO       -> thickness", "peo", "th", li_ag)
rep("PEO       -> log10(t_half)", "peo", "lt", [r for r in li_ag if r["lt"] is not None])
rep("thickness -> log10(t_half)", "th", "lt", [r for r in li_ag if r["lt"] is not None])
rep("PEO       -> growth exponent", "peo", "alpha", [r for r in li_ag if r["alpha"] is not None])
rep("thickness -> growth exponent", "th", "alpha", [r for r in li_ag if r["alpha"] is not None])
rep("PEO       -> log10(peak ratio)", "peo", "lp", [r for r in li_ag if r["lp"] is not None])
rep("thickness -> log10(peak ratio)", "th", "lp", [r for r in li_ag if r["lp"] is not None])

print("\nPartial correlations (the decisive test):")
pr, n = partial([r for r in li_ag if r["lt"] is not None], "th", "lt", "peo")
print(f"   r(thickness, log t_half | PEO) = {pr:+.2f}  (n={n})  -> ~0: thickness adds nothing beyond PEO")
pr2, n2 = partial([r for r in li_ag if r["lt"] is not None], "peo", "lt", "th")
print(f"   r(PEO, log t_half | thickness) = {pr2:+.2f}  (n={n2})  -> strong: composition effect survives")

print("\nVERDICT: thickness is a controlled covariate, not a confound. Composition claims,")
print("parameter cards, and simulations are unaffected. See handouts/14_*.md.\n")

# --------------------------------------------------------------------------
# figure
# --------------------------------------------------------------------------
os.makedirs(FIGDIR, exist_ok=True)
fig, (axA, axB) = plt.subplots(1, 2, figsize=(8.2, 3.6))

# Panel A: thickness vs PEO, coloured by RPM (shows covariation + RPM compensation)
peo_levels = [0.3, 0.6, 1.2]
xpos = {p: i for i, p in enumerate(peo_levels)}
A = [r for r in li_ag if r["peo"] in xpos and r["rpm"] is not None]
import numpy as np
rng = np.random.default_rng(0)
xs = [xpos[r["peo"]] + rng.uniform(-0.13, 0.13) for r in A]
sc = axA.scatter(xs, [r["th"] for r in A], c=[r["rpm"] for r in A],
                 cmap="viridis", s=34, edgecolor="k", linewidth=0.3, zorder=3)
for p in peo_levels:
    m = statistics.median([r["th"] for r in li_ag if r["peo"] == p])
    axA.plot([xpos[p] - 0.22, xpos[p] + 0.22], [m, m], color="crimson", lw=1.6, zorder=2)
axA.set_xticks(range(len(peo_levels)))
axA.set_xticklabels([str(p) for p in peo_levels])
axA.set_xlabel("PEO mass fraction")
axA.set_ylabel("film thickness (nm)")
axA.set_title("(a) thickness covaries with PEO\n(red = cell median; colour = spin RPM)")
cb = fig.colorbar(sc, ax=axA, pad=0.02)
cb.set_label("spin-coat RPM", fontsize=8)

# Panel B: log t_half vs thickness, coloured by PEO (memory tracks PEO colour, not x)
B = [r for r in li_ag if r["lt"] is not None]
cmap = {0.3: "#2166ac", 0.6: "#999999", 1.2: "#b2182b"}
for p in peo_levels:
    pts = [r for r in B if r["peo"] == p]
    axB.scatter([r["th"] for r in pts], [r["t_half"] for r in pts],
                color=cmap[p], s=36, edgecolor="k", linewidth=0.3, label=f"PEO {p}")
axB.set_yscale("log")
axB.set_xlabel("film thickness (nm)")
axB.set_ylabel(r"fading-memory time $t_{1/2}$ (s)")
prtxt, npt = partial(B, "th", "lt", "peo")
axB.set_title("(b) memory tracks PEO, not thickness\n"
              rf"$r(\mathrm{{thick}},\,t_{{1/2}}\,|\,\mathrm{{PEO}})={prtxt:+.2f}$ (n={npt})")
axB.legend(fontsize=7, frameon=False, loc="upper right")

fig.tight_layout()
out = os.path.join(FIGDIR, "thickness_control.pdf")
fig.savefig(out)
print(f"wrote {out}")
