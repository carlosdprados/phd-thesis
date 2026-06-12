#!/usr/bin/env python3
"""Findings extraction for the Au/TMPE lock-in frequency-sweep corpus.

Consumes handouts/lockin_metrics.csv (written by lockin_au_tmpe_audit.py)
plus targeted re-reads of the raw exports, and quantifies:

  L1  capacitive-divider validation: H(C_ext) on unkK2-L5 day 3 follows
      H = C_dev/(C_dev+C_ext) with a single C_dev
  L2  passive-band linearity: |H| at 1/10 kHz is amplitude-independent
      (0.5-2.4 Vpk) at zero offset
  L3  bias-controlled low-frequency gain: |H| at 1-2 Hz vs DC offset
      (day-23 11-point series + day-4/9/10 matched +/- pairs), with
      range-boundary repeats (200 Hz, 5 kHz) as repeatability QC
  L4  aging: passive plateau and zero-offset low-f transmission within pixel
      (offset-gain protocols differ across days -> descriptive only)
  L5  rectified DC at the output node (demod 3) vs offset

The 110 "500k-1Hz_400p-1s" files are *derived*: they are the output of the
corpus' own combine_freq.py (frequency-sorted merge of the three piecewise
ranges; capture count 400 = 101+98+201, timer runs backwards). They are
excluded from all statistics here to avoid double counting.

Writes handouts/lockin_findings_{divider,linearity,gain,aging}.csv and a
console summary. Run from the repo root after the audit script.
"""
import os
import math
import csv

import numpy as np
import pandas as pd

RAW = ("../Nanomem_Devices_Library/Common/"
       "Au_TMPE_Li-Na-K_Lock-in-Amplifier_Freq_Sweeps/raw_data")
OUT = "handouts"

MET = pd.read_csv(os.path.join(OUT, "lockin_metrics.csv"))
MET["dev"] = MET.chem + "-" + MET.pixel
DERIVED = MET.frange == "500k-1Hz"   # combine_freq.py merges, not measurements
MET = MET[~DERIVED].copy()


def load_cols(fn, *wanted):
    with open(os.path.join(RAW, fn)) as fh:
        lines = fh.readlines()
    header = next(l.lstrip("# ").strip() for l in lines if l.startswith("#"))
    cols = [c.strip() for c in header.split("\t") if c.strip()]
    data = [[float(x) for x in ln.split()]
            for ln in lines if not ln.startswith("#") and ln.strip()
            and len(ln.split()) == len(cols)]
    arr = np.array(data)
    out = []
    for w in wanted:
        idx = next(i for i, c in enumerate(cols) if all(k in c for k in w))
        out.append(arr[:, idx])
    return out


def near(f, target):
    i = int(np.argmin(np.abs(f - target)))
    return i if 0.8 * target <= f[i] <= 1.25 * target else None


# ------------------------------------------------- L1 divider validation --
def divider():
    rows = []
    sel = MET[(MET.dev == "unkK2-L5") & (MET.day == 3) & (MET.offset_v == 0)
              & (MET.amp_v == 0.5) & (MET.frange == "500k-5kHz")
              & MET.config.str.contains("nF")]
    for _, r in sel.iterrows():
        h = r.H_10k
        if pd.isna(h) or not 0 < h < 1:
            continue
        rows.append(dict(c_ext_nf=r.c_ext_nf, H_10k=h,
                         c_dev_nf=round(r.c_ext_nf * h / (1 - h), 3)))
    df = pd.DataFrame(rows).sort_values("c_ext_nf")
    df.to_csv(os.path.join(OUT, "lockin_findings_divider.csv"), index=False)
    print("\n== L1 divider validation (unkK2-L5 d3, 0.5 Vpk, H at 10 kHz) ==")
    print(df.to_string(index=False))
    c = df.c_dev_nf
    print(f"implied C_dev across C_ext {df.c_ext_nf.min()}-{df.c_ext_nf.max()} nF: "
          f"median {c.median():.2f} nF, rel. spread (IQR/med) "
          f"{(c.quantile(.75)-c.quantile(.25))/c.median()*100:.0f}%")


# ------------------------------------------------- L2 passive linearity --
def linearity():
    rows = []
    sel = MET[(MET.offset_v == 0) & (MET.config == "LP-4nF-noR")]
    for (dev, day), g in sel.groupby(["dev", "day"]):
        for fcol in ("H_1k", "H_10k"):
            vals = g.dropna(subset=[fcol])
            amps = vals.groupby("amp_v")[fcol].median()
            if len(amps) < 3:
                continue
            spread = (amps.max() - amps.min()) / amps.mean() * 100
            rows.append(dict(dev=dev, day=day, fband=fcol,
                             n_amp=len(amps), amp_min=amps.index.min(),
                             amp_max=amps.index.max(),
                             H_mean=round(amps.mean(), 4),
                             rel_spread_pct=round(spread, 2)))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "lockin_findings_linearity.csv"), index=False)
    print("\n== L2 passive-band linearity (0 offset, amplitude series) ==")
    for fb, g in df.groupby("fband"):
        print(f"{fb}: {len(g)} device-days, median |H| spread across "
              f"amplitudes {g.rel_spread_pct.median():.2f}% "
              f"(max {g.rel_spread_pct.max():.2f}%)")
    # effective capacitance by chemistry (1 kHz, all 4nF 0-offset files)
    cd = sel.dropna(subset=["c_dev_nf"])
    print("\nC_dev at 1 kHz by chemistry (4 nF config, 0 offset):")
    print(cd.groupby("chem").c_dev_nf.describe()[["count", "50%", "25%", "75%"]]
          .round(2).to_string())
    print("\nC_dev by device and day:")
    print(cd.groupby(["dev", "day"]).c_dev_nf.median().round(2).to_string())


# --------------------------------------------------------- L3 gain table --
def gain():
    rows = []
    sel = MET[MET.config == "LP-4nF-noR"]
    for _, r in sel.iterrows():
        if pd.isna(r.get("H_2")) and pd.isna(r.get("H_1")):
            continue
        rows.append(dict(dev=r.dev, chem=r.chem, day=r.day, frange=r.frange,
                         offset_v=r.offset_v, amp_v=r.amp_v,
                         file=r["file"],
                         H_1=r.get("H_1"), H_2=r.get("H_2"),
                         H_5=r.get("H_5"), H_10=r.get("H_10"),
                         H_1k=r.get("H_1k"),
                         ph_2=r.get("ph_2"), dc_2=r.get("dc_2")))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "lockin_findings_gain.csv"), index=False)

    print("\n== L3 bias-controlled low-frequency gain ==")
    d23 = df[(df.dev == "unkLi2-L3") & (df.day == 23)
             & (df.frange == "200-1Hz")].sort_values("offset_v")
    print("\nday-23 offset series (unkLi2-L3, 0.25 Vpk, 200-1Hz capture):")
    print(d23[["offset_v", "H_1", "H_2", "H_5", "H_10",
               "dc_2"]].to_string(index=False))
    # gain corner: highest frequency at which |H| still exceeds 1
    print("\nday-23 gain corner (max f with |H|>1, stitched 200-1Hz curve):")
    for _, r in d23.iterrows():
        f, h = load_cols(r.file, ("Oscilator_frequency",), ("Demod_4", "_R_"))
        H = h / (r.amp_v / math.sqrt(2))
        above = f[H > 1]
        fx = above.max() if len(above) else float("nan")
        print(f"  offset {r.offset_v:+.1f} V: f_gain<1x at {fx:5.1f} Hz")

    # repeatability: the 200 Hz boundary point is measured in both the
    # 5k-200Hz and 200-1Hz captures of a condition, minutes apart
    reps = []
    for (dev, day, off, amp), g in MET[MET.config == "LP-4nF-noR"].groupby(
            ["dev", "day", "offset_v", "amp_v"]):
        h200 = {}
        for _, r in g.iterrows():
            if r.frange not in ("5k-200Hz", "200-1Hz"):
                continue
            f, h = load_cols(r.file, ("Oscilator_frequency",),
                             ("Demod_4", "_R_"))
            i = int(np.argmin(np.abs(f - 200)))
            if 180 <= f[i] <= 220:
                h200[r.frange] = h[i] / (amp / math.sqrt(2))
        if len(h200) == 2:
            reps.append(abs(h200["5k-200Hz"] - h200["200-1Hz"])
                        / np.mean(list(h200.values())))
    if reps:
        reps = np.array(reps)
        print(f"\n200 Hz boundary repeatability, n={len(reps)} conditions: "
              f"median |dH|/H = {np.median(reps)*100:.1f}%, "
              f"90th pct {np.percentile(reps, 90)*100:.1f}%")

    # population: gain>1 prevalence vs offset (200-1Hz captures only)
    df["absoff"] = df.offset_v.abs()
    pop = df[df.frange == "200-1Hz"].dropna(subset=["H_2"])
    print("\nH_2 by |offset| (200-1Hz captures):")
    print(pop.groupby("absoff").H_2.agg(["count", "median",
                                         lambda s: (s > 1).mean()])
          .rename(columns={"<lambda_0>": "frac>1"}).round(2).to_string())

    # polarity symmetry on matched pairs
    pairs = pop[pop.absoff > 0].pivot_table(
        index=["dev", "day", "absoff", "amp_v"],
        columns=pop.offset_v.gt(0).map({True: "pos", False: "neg"}),
        values="H_2", aggfunc="median")
    pairs = pairs.dropna()
    if len(pairs):
        lr = np.log(pairs.pos / pairs.neg)
        from scipy import stats
        w = stats.wilcoxon(lr)
        print(f"\nmatched +/- pairs n={len(pairs)}: median H2(+)/H2(-) = "
              f"{np.exp(np.median(lr)):.2f}, Wilcoxon p={w.pvalue:.4f}")
        pairs.reset_index().to_csv(
            os.path.join(OUT, "lockin_findings_gain_pairs.csv"), index=False)


# ------------------------------------------------------------- L4 aging --
def aging():
    rows = []
    sel = MET[MET.config == "LP-4nF-noR"].copy()
    # passive plateau vs day (H_1k is offset-insensitive; verify first)
    chk = sel.dropna(subset=["H_1k"])
    by_off = chk.groupby(chk.offset_v.abs() > 0).H_1k.median()
    print("\n== L4 aging ==")
    print(f"plateau H_1k median, 0-offset vs offset files: "
          f"{by_off.get(False, float('nan')):.3f} vs "
          f"{by_off.get(True, float('nan')):.3f}")
    plat = chk.groupby(["dev", "day"]).H_1k.median().reset_index()
    plat.to_csv(os.path.join(OUT, "lockin_findings_aging.csv"), index=False)
    print("\nplateau H_1k by device/day:")
    print(plat.pivot_table(index="dev", columns="day", values="H_1k")
          .round(3).to_string())

    # zero-offset low-f transmission vs day (smallest common amplitude);
    # offset-gain protocols differ across days, so no matched comparison
    z = MET[(MET.config == "LP-4nF-noR") & (MET.offset_v == 0)
            & (MET.frange == "200-1Hz")].dropna(subset=["H_2"])
    z = z[z.amp_v == 0.5]
    if len(z):
        print("\nzero-offset H_2 (0.5 Vpk) by device/day:")
        print(z.groupby(["dev", "day"]).H_2.median().round(3).to_string())


# -------------------------------------------------------- L5 rectified DC --
def rectdc():
    g = pd.read_csv(os.path.join(OUT, "lockin_findings_gain.csv"))
    g = g[g.frange == "200-1Hz"].dropna(subset=["dc_2"])
    print("\n== L5 rectified DC at output node (demod 3, 2 Hz point) ==")
    d23 = g[(g.dev == "unkLi2-L3") & (g.day == 23)].sort_values("offset_v")
    if len(d23):
        print("day-23 series offset -> dc_2 (V):",
              ", ".join(f"{o:+.1f}:{d:+.2f}" for o, d in
                        zip(d23.offset_v, d23.dc_2)))
    z = g[g.offset_v == 0]
    if len(z):
        from scipy import stats
        bt = stats.binomtest((z.dc_2 < 0).sum(), len(z))
        print(f"zero-offset files n={len(z)}: median dc_2 = "
              f"{z.dc_2.median():+.3f} V, frac negative = "
              f"{(z.dc_2 < 0).mean():.2f} (binomial p={bt.pvalue:.3f})")


if __name__ == "__main__":
    divider()
    linearity()
    gain()
    aging()
    rectdc()
