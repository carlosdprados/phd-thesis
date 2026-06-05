#!/usr/bin/env python3
"""Chapter 3 --- electrode (Ag vs Au) contrast at the lead composition cell.

The quantitative spine of Chapter 3 (the SY/PEO/LiOTf composition grid) and the
chemistry landscape are reported on the *silver* electrode; gold-electrode
devices were held out as a confound. This script audits what the gold corpus
actually contains and what it can and cannot say, so that the electrode can be
reported honestly rather than merely excluded.

Three things are established here, all reproduced from the same DATABASE the
rest of Chapter 3 uses:

  (1) Coverage. Every Au device is SY-based and sits at the single lead
      composition (ion-polymer mass ratio 0.3, salt 0.09). The Au corpus is
      therefore a *chemistry-axis* dataset at fixed composition; it cannot test
      the composition spine at all.

  (2) Electrode contrast at matched chemistry (0.3/0.09). Across hysteresis,
      potentiation and fading-memory decay, the inert Au electrode gives a
      narrower switching window, weaker potentiation and a *longer* fading-
      memory time than the electrochemically active Ag electrode --- the
      direction expected for an active (Ag+) vs noble (Au) electrode. Reported
      illustratively: small n per cell, no human PNG curation of Au curves, and
      the Au generation (2024-2025) post-dates the Ag chemistry generation, so
      electrode and fabrication generation are partly confounded.

  (3) Independent-electrode replication of the chemistry claims. The host effect
      (PEO > TMPE retention) and the cation null (no clean Li/Na/K ordering)
      both reproduce on Au, and the salt-free / host-free Au controls show no
      potentiation --- strengthening the Chapter 3 chemistry landscape on a
      second electrode.

Run from the repo root:  python3 scripts/ch3_electrode.py
Writes handouts/ch3_electrode_by_cell.csv and prints the tables used in the text.
"""
import csv
import collections
import os

import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DB = "../Nanomem_Devices_Library/DATABASE"
OUT = "handouts"
FIGDIR = "figures/chapter3"

plt.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.titlesize": 9,
    "axes.labelsize": 9, "figure.dpi": 150, "savefig.bbox": "tight",
})
AG_C, AU_C = "#1f4e79", "#b8860b"  # silver-blue, gold


def L(f):
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


# ----------------------------------------------------------------------
# Composition / chemistry / electrode decode.
#  - species identity (which host / salt) lives in the per-species columns of
#    DEVICES_LIBRARY.csv;
#  - the collapsed mass-ratio values live in UPDATED_DEVICES_LIBRARY.csv;
#  - electrode is read from the evaporated-thickness columns of the UPDATED lib.
# ----------------------------------------------------------------------
ORIG = {r["device_name"]: r for r in L("DEVICES_LIBRARY.csv")}
UPD = {r["device_name"]: r for r in L("UPDATED_DEVICES_LIBRARY.csv")}


def electrode(dn):
    r = UPD.get(dn)
    if not r:
        return "?"
    au = fnum(r.get("Au Thickness [nm]")) or 0
    ag = fnum(r.get("Ag Thickness [nm]")) or 0
    if au > 0:
        return "Au"
    if ag > 0:
        return "Ag"
    return "?"


def host(dn):
    for c in ["PEO", "TMPE", "Hy"]:
        v = fnum(ORIG[dn].get(f"Ion-Conducting Polymer Mass Ratio - {c}"))
        if v and v > 0:
            return c
    return "none"


def salt(dn):
    table = [("LiTr", "Li", "OTf"), ("NaTr", "Na", "OTf"), ("KTr", "K", "OTf"),
             ("LiTFSI", "Li", "TFSI"), ("NaTFSI", "Na", "TFSI"), ("KTFSI", "K", "TFSI")]
    for col, cat, an in table:
        v = fnum(ORIG[dn].get(f"Salt Mass Ratio - {col}"))
        if v and v > 0:
            return cat, an
    return "none", "none"


def chem(dn):
    cat, an = salt(dn)
    return f"{host(dn)}/{cat}/{an}"


def comp(dn):
    return UPD[dn].get("Ion-Conducting Polymer Mass Ratio", ""), UPD[dn].get("Salt Mass Ratio", "")


def is_sy(dn):
    return (fnum(ORIG[dn].get("Semiconductive Polymer Mass Ratio - SY")) or 0) > 0


FLAGS = set((r["device_name"], r["day"], r["pixel"], r["measurement_type"])
            for r in L("FILTERED_DEVICES.csv"))
RV2 = set(r["device_name"] for r in L("DEVICES_DELAYTIME_PIXEL_INFO.csv")
          if (r.get("reading voltage (V)") or "").strip() == "2.0")

AU = sorted(dn for dn in UPD if electrode(dn) == "Au")


def survey():
    print(f"=== Au corpus: {len(AU)} devices ===")
    cells = collections.Counter()
    for dn in AU:
        pm, sm = comp(dn)
        cells[(chem(dn), pm, sm)] += 1
    for k, v in sorted(cells.items(), key=lambda x: str(x)):
        print(f"  chem={k[0]:16s} PEO={k[1]:4s} salt={k[2]:5s}  n={v}")
    offspine = [dn for dn in AU if comp(dn) not in (("0.3", "0.09"), ("0.3", ""), ("", "0.09"), ("", ""))]
    print(f"\nAu devices off the 0.3/0.09 lead composition: {len(offspine)}  "
          f"(the Au corpus is a chemistry-axis set at fixed composition)")


# ----------------------------------------------------------------------
# Hysteresis: per-device median on-off ratio / normalised area / activation V
# ----------------------------------------------------------------------
def hyst_by_device():
    h = collections.defaultdict(list)
    for r in L("DEVICES_HYST_CURVE_INFO.csv"):
        dn = r["device_name"]
        if (dn, r["day"], r["pixel"], "HYST") in FLAGS:
            continue
        if (r.get("is broken") or "") == "True":
            continue
        h[dn].append((fnum(r.get("on-off ratio")), fnum(r.get("normalized area")),
                      fnum(r.get("activation voltage (V)"))))
    return h


# ----------------------------------------------------------------------
# Potentiation: per-device peak ratio / log-log growth exponent / turnover
# ----------------------------------------------------------------------
def pulses_by_device():
    pg = collections.defaultdict(list)
    for r in L("DEVICES_PULSES_CURVE_INFO.csv"):
        dn = r["device_name"]
        if (dn, r["day"], r["pixel"], "PULSES") in FLAGS:
            continue
        N, y = fnum(r.get("number of pulses")), fnum(r.get("ratio"))
        if N and N > 0 and y is not None:
            pg[(dn, r["pixel"])].append((N, y))
    d = collections.defaultdict(list)
    for (dn, px), pts in pg.items():
        pts = sorted(set(pts))
        N = np.array([p[0] for p in pts])
        y = np.array([p[1] for p in pts])
        if len(N) < 5:
            continue
        pk = int(np.argmax(y))
        mask = (N <= N[pk]) & (y > 0)
        gexp = float(np.polyfit(np.log10(N[mask]), np.log10(y[mask]), 1)[0]) if mask.sum() >= 3 else float("nan")
        d[dn].append((float(y[pk]), gexp, int(pk < len(y) - 1)))
    return d


# ----------------------------------------------------------------------
# Fading memory: model-free t_half + stretched-exp fit, 2.0 V read only.
# No human PNG curation exists for the Au curves -> automated screen only.
# ----------------------------------------------------------------------
def stretched(t, A, tau, beta, C):
    return A * np.exp(-((t / tau) ** beta)) + C


def delaytime_fits(restrict=None):
    grp = collections.defaultdict(list)
    for r in L("DEVICES_DELAYTIME_CURVE_INFO.csv"):
        dn = r["device_name"]
        if restrict is not None and dn not in restrict:
            continue
        if dn not in RV2:
            continue
        if (dn, r["day"], r["pixel"], "DELAYTIME") in FLAGS:
            continue
        t, y = fnum(r.get("delay time (s)")), fnum(r.get("ratio"))
        if t and t > 0 and y is not None:
            grp[(dn, r["pixel"])].append((t, y))
    rows = []
    for (dn, px), pts in grp.items():
        pts = sorted(set(pts))
        t = np.array([p[0] for p in pts])
        y = np.array([p[1] for p in pts])
        if len(t) < 6:
            continue
        r1 = float(y[t == 1][0]) if (t == 1).any() else float(y[0])
        target = r1 / 2.0
        thalf = float("nan")
        for i in range(len(t) - 1):
            if y[i] >= target >= y[i + 1] and y[i] != y[i + 1]:
                lt, lt2 = np.log10(t[i]), np.log10(t[i + 1])
                frac = (y[i] - target) / (y[i] - y[i + 1])
                thalf = float(10 ** (lt + frac * (lt2 - lt)))
                break
        tau = beta = r2 = float("nan")
        try:
            p, _ = curve_fit(stretched, t, y, p0=[max(y.max() - y.min(), 1e-3), float(np.median(t)), 0.7, max(y.min(), 0.0)],
                             bounds=([0, 1e-2, 0.1, 0], [np.inf, 1e5, 2.0, np.inf]), maxfev=40000)
            yhat = stretched(t, *p)
            r2 = float(1 - np.sum((y - yhat) ** 2) / max(np.sum((y - y.mean()) ** 2), 1e-12))
            tau, beta = float(p[1]), float(p[2])
        except Exception:
            pass
        # "clean" decay = identified stretched fit, not a degenerate bound-hit
        clean = bool(np.isfinite(r2) and r2 >= 0.90 and 0.1 < beta < 1.9 and np.isfinite(thalf))
        rows.append(dict(device=dn, pixel=px, chem=chem(dn), n=len(t),
                         t_half=thalf, tau=tau, beta=beta, r2=r2, clean=clean))
    return rows


def raw_decays(dns):
    """Per-device delay-time curves (t, ratio) at 2.0 V read, FILTERED applied."""
    grp = collections.defaultdict(list)
    for r in L("DEVICES_DELAYTIME_CURVE_INFO.csv"):
        dn = r["device_name"]
        if dn not in dns or dn not in RV2:
            continue
        if (dn, r["day"], r["pixel"], "DELAYTIME") in FLAGS:
            continue
        t, y = fnum(r.get("delay time (s)")), fnum(r.get("ratio"))
        if t and t > 0 and y is not None:
            grp[(dn, r["pixel"])].append((t, y))
    return grp


def make_figure(hyst, pul, decay_all):
    """Electrode contrast at the lead 0.3/0.09 cell: retention up, window down
    (and cation-flat), potentiation down, for inert Au vs active Ag."""
    fig, ax = plt.subplots(1, 3, figsize=(9.2, 3.0))

    # (a) PEO/Li/OTf fading-memory decays, Ag vs Au (clean curves only)
    for el, col in [("Ag", AG_C), ("Au", AU_C)]:
        dns = set(d for d in cell_devs(el, "PEO/Li/OTf")
                  if d in decay_all and decay_all[d]["clean"])
        lab = True
        for (dn, px), pts in raw_decays(dns).items():
            pts = sorted(set(pts))
            t = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
            y0 = y[t == 1][0] if (t == 1).any() else y[0]
            ax[0].semilogx(t, y / y0, "-o", ms=3, lw=1.1, color=col, alpha=0.85,
                           label=(el if lab else None)); lab = False
    ax[0].axhline(0.5, ls=":", c="0.6", lw=0.8)
    ax[0].set_xlabel("delay (s)"); ax[0].set_ylabel("norm. enhancement")
    ax[0].set_title("(a) fading memory (PEO/Li)"); ax[0].legend(frameon=False, fontsize=8)

    # (b) switching window across chemistry, Ag vs Au (cation series flat on Au)
    cells_b = ["PEO/Li/OTf", "TMPE/Li/OTf", "TMPE/Na/OTf", "TMPE/K/OTf"]
    labs = ["PEO/Li", "TMPE/Li", "TMPE/Na", "TMPE/K"]
    x = np.arange(len(cells_b)); w = 0.38
    for k, (el, col) in enumerate([("Ag", AG_C), ("Au", AU_C)]):
        vals = [med([med([t[0] for t in hyst.get(dn, [])]) for dn in cell_devs(el, ce) if dn in hyst])
                for ce in cells_b]
        ax[1].bar(x + (k - 0.5) * w, vals, w, color=col, label=el)
    ax[1].set_xticks(x); ax[1].set_xticklabels(labs, rotation=30, ha="right")
    ax[1].set_ylabel("on-off ratio"); ax[1].set_title("(b) switching window")
    ax[1].legend(frameon=False, fontsize=8)

    # (c) potentiation peak ratio, Ag vs Au (log)
    cells_c = ["PEO/Li/OTf", "TMPE/Li/OTf"]
    labs_c = ["PEO/Li", "TMPE/Li"]
    x = np.arange(len(cells_c))
    for k, (el, col) in enumerate([("Ag", AG_C), ("Au", AU_C)]):
        vals = [med([med([t[0] for t in pul.get(dn, [])]) for dn in cell_devs(el, ce) if dn in pul])
                for ce in cells_c]
        ax[2].bar(x + (k - 0.5) * w, vals, w, color=col, label=el)
    ax[2].set_yscale("log"); ax[2].set_xticks(x); ax[2].set_xticklabels(labs_c)
    ax[2].set_ylabel("potentiation peak ratio"); ax[2].set_title("(c) potentiation")
    ax[2].legend(frameon=False, fontsize=8)

    fig.tight_layout()
    os.makedirs(FIGDIR, exist_ok=True)
    fig.savefig(os.path.join(FIGDIR, "electrode_contrast.pdf"))
    print(f"\nwrote {FIGDIR}/electrode_contrast.pdf")


def cell_devs(electr, chemstr):
    return [dn for dn in ORIG if is_sy(dn) and electrode(dn) == electr and chem(dn) == chemstr
            and comp(dn)[0] in ("0.3", "") and comp(dn)[1] in ("0.09", "")]


def main():
    survey()

    hyst = hyst_by_device()
    pul = pulses_by_device()

    def hmed(dns, idx):
        return med([med([t[idx] for t in hyst.get(dn, [])]) for dn in dns if dn in hyst])

    def pmed(dns, idx):
        return med([med([t[idx] for t in pul.get(dn, [])]) for dn in dns if dn in pul])

    decay_all = {r["device"]: r for r in delaytime_fits()}

    def dmed(dns):
        vals = [decay_all[dn]["t_half"] for dn in dns if dn in decay_all and decay_all[dn]["clean"]]
        return med(vals), len(vals)

    cells = ["PEO/Li/OTf", "TMPE/Li/OTf", "TMPE/Na/OTf", "TMPE/K/OTf",
             "TMPE/Na/TFSI", "Hy/Li/OTf", "none/Li/OTf", "TMPE/none/none", "none/none/none"]
    print("\n=== Electrode x chemistry at 0.3/0.09 (per-device medians) ===")
    hdr = (f"{'chem':15s} {'el':3s} {'nH':>3s} {'onoff':>6s} {'normA':>6s} {'Vact':>5s} "
           f"{'nP':>3s} {'peak':>7s} {'gexp':>5s} {'nDok':>4s} {'t_half':>7s}")
    print(hdr)
    out = []
    for ce in cells:
        for el in ["Ag", "Au"]:
            dns = cell_devs(el, ce)
            if not dns:
                continue
            nH = sum(dn in hyst for dn in dns)
            nP = sum(dn in pul for dn in dns)
            th, nD = dmed(dns)
            row = dict(chem=ce, electrode=el, n_hyst=nH,
                       onoff=hmed(dns, 0), normA=hmed(dns, 1), Vact=hmed(dns, 2),
                       n_pulse=nP, peak_ratio=pmed(dns, 0), growth_exp=pmed(dns, 1),
                       n_decay_clean=nD, t_half=th)
            out.append(row)
            print(f"{ce:15s} {el:3s} {nH:3d} {row['onoff']:6.2f} {row['normA']:6.3f} {row['Vact']:5.2f} "
                  f"{nP:3d} {row['peak_ratio']:7.1f} {row['growth_exp']:5.2f} {nD:4d} {th:7.1f}")

    with open(os.path.join(OUT, "ch3_electrode_by_cell.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["chem", "electrode", "n_hyst", "onoff", "normA", "Vact",
                                           "n_pulse", "peak_ratio", "growth_exp", "n_decay_clean", "t_half"])
        w.writeheader()
        for r in out:
            w.writerow({k: (round(v, 3) if isinstance(v, float) and np.isfinite(v) else
                            ("" if isinstance(v, float) else v)) for k, v in r.items()})

    print("\n=== Au PEO/Li/OTf fading-memory decays (2.0 V read; automated screen only) ===")
    for dn in sorted(cell_devs("Au", "PEO/Li/OTf")):
        r = decay_all.get(dn)
        if r:
            print(f"  {dn}: n={r['n']} t_half={r['t_half']:6.1f}s tau={r['tau']:6.1f} "
                  f"beta={r['beta']:.2f} R2={r['r2']:.2f} clean={r['clean']}")
    print("\nReference (Ag, from ch3_decay_by_cell.csv): PEO/Li 0.3/0.09 t_half_med ~ 19.2 s (n=3).")

    make_figure(hyst, pul, decay_all)


if __name__ == "__main__":
    main()
