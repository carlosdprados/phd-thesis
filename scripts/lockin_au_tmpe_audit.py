#!/usr/bin/env python3
"""Audit of the Au/TMPE/(Li,Na,K)OTf lock-in frequency-sweep corpus (Mar 2025).

`Nanomem_Devices_Library/Common/Au_TMPE_Li-Na-K_Lock-in-Amplifier_Freq_Sweeps/`
holds 549 Zurich MFLI sweeper exports (.txt + .hdf5 siblings) taken on a
single Au/TMPE batch fabricated 2025-03-03 (the `Ndaydeg` filename field
equals date - 2025-03-03 for every file) and tracked to day 23. This is the
sibling dataset of the DC corpus audited in handout 28 (same chemistry and
generation, fresh substrates, device IDs unkLi2/unkNa2/unkK2).

Circuit (from the included dataviz script + MFLI channel map): the sweeper
drives offset + amp*sin(2*pi*f*t) through the device into a series capacitor
C_ext to ground ("LP-<C>-noR" config); the MFLI voltage input (10 Mohm) reads
the node across C_ext. Demod 4 = output at the drive frequency (Demod 2 is a
unit-mislabelled duplicate); Demod 3 behaves as a DC monitor of the output
node (|R| = magnitude, sign of theta = sign of the DC); Demod 1 is an
auxiliary current channel not used here. |H| = Demod4_R / (amp/sqrt(2)),
the normalisation used by the corpus' own dataviz script.

Writes:
  handouts/lockin_manifest.csv   one row per .txt file (metadata + QC)
  handouts/lockin_metrics.csv    per-file |H|/phase/DC at probe frequencies
  figures/lockin_qa/             per device-day overlay of |H|(f)

Run from the repo root:  python3 scripts/lockin_au_tmpe_audit.py
"""
import os
import re
import csv
import math

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAW = ("../Nanomem_Devices_Library/Common/"
       "Au_TMPE_Li-Na-K_Lock-in-Amplifier_Freq_Sweeps/raw_data")
OUT = "handouts"
QADIR = "figures/lockin_qa"
os.makedirs(QADIR, exist_ok=True)

FAB_DATE = "2025-03-03"

PAT = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2})_"
    r"(?P<chem>[^-]+)-"
    r"(?P<pixel>[^_]+)_"
    r"(?P<config>.+?)-config_"
    r"(?P<deg>[^_]+)_"
    r"(?P<frange>[^_]+)_"
    r"(?P<capture>[^_]+)_"
    r"(?P<offset>[^_]+)_"
    r"(?P<amp>[^V]+)Vpk\.txt$")

CAP_PAT = re.compile(r"LP-([\d.]+)([pn])F", re.I)

# probe frequencies (Hz) at which |H|, phase and the DC monitor are sampled
PROBES = [1, 2, 5, 10, 20, 50, 100, 1000, 1e4, 1e5, 5e5]


def parse_name(fn):
    m = PAT.match(fn)
    if not m:
        return None
    d = m.groupdict()
    d["day"] = int(re.search(r"(\d+)", d["deg"]).group(1))
    d["offset_v"] = float(d["offset"].replace("offset", ""))
    d["amp_v"] = float(d["amp"])
    cm = CAP_PAT.search(d["config"])
    if cm:
        val = float(cm.group(1))
        d["c_ext_nf"] = val / 1000.0 if cm.group(2).lower() == "p" else val
    else:
        d["c_ext_nf"] = math.nan
    return d


def load_txt(path):
    """Return dict of column -> np.array for one sweeper export."""
    with open(path) as fh:
        lines = fh.readlines()
    header = next(l.lstrip("# ").strip() for l in lines if l.startswith("#"))
    cols = [c.strip() for c in header.split("\t") if c.strip()]
    data = []
    for ln in lines:
        if ln.startswith("#") or not ln.strip():
            continue
        parts = ln.split()
        if len(parts) == len(cols):
            data.append([float(x) for x in parts])
    arr = np.array(data)
    return {c: arr[:, i] for i, c in enumerate(cols)}


def col(d, *keys):
    for c in d:
        if all(k in c for k in keys):
            return d[c]
    return None


def sample_at(f, y, target):
    """Value of y at the frequency point nearest target (None if >20% off)."""
    i = int(np.argmin(np.abs(f - target)))
    if not (0.8 * target <= f[i] <= 1.25 * target):
        return None
    return y[i]


def main():
    files = sorted(f for f in os.listdir(RAW) if f.endswith(".txt"))
    manifest, metrics = [], []
    curves = {}  # (chem,pixel,day) -> list of (label, f, H, offset, amp)

    for fn in files:
        meta = parse_name(fn)
        row = {"file": fn}
        if meta is None:
            row["parsed"] = 0
            manifest.append(row)
            continue
        row.update({k: meta[k] for k in
                    ("date", "chem", "pixel", "config", "day", "frange",
                     "capture", "offset_v", "amp_v", "c_ext_nf")})
        row["parsed"] = 1
        d = load_txt(os.path.join(RAW, fn))
        f = col(d, "Oscilator_frequency")
        v4r = col(d, "Demod_4", "_R_")
        v4t = col(d, "Demod_4", "Theta")
        v2r = col(d, "Demod_2", "_R_")
        v3r = col(d, "Demod_3", "_R_")
        v3t = col(d, "Demod_3", "Theta")
        timer = col(d, "Timer")

        vrms = meta["amp_v"] / math.sqrt(2.0)
        H = v4r / vrms
        row["n_pts"] = len(f)
        row["f_min"] = float(f.min())
        row["f_max"] = float(f.max())
        row["descending"] = int(f[0] > f[-1])
        row["sweep_dur_s"] = float(timer[-1] - timer[0]) if timer is not None else None
        # QC: Demod_2 duplicates Demod_4 (unit mislabel)
        row["demod2_dup"] = int(v2r is not None and
                                np.allclose(v2r, v4r, rtol=1e-3, atol=1e-6))
        row["h_nan"] = int(np.isnan(H).any())
        manifest.append(row)

        met = {k: row[k] for k in ("file", "chem", "pixel", "config", "day",
                                   "frange", "offset_v", "amp_v", "c_ext_nf")}
        for p in PROBES:
            tag = (f"{p:g}" if p < 1000 else f"{p/1000:g}k").replace(".", "p")
            h = sample_at(f, H, p)
            th = sample_at(f, v4t, p)
            met[f"H_{tag}"] = round(h, 5) if h is not None else None
            met[f"ph_{tag}"] = round(th, 2) if th is not None else None
            if v3r is not None:
                dc = sample_at(f, v3r, p)
                dct = sample_at(f, v3t, p)
                if dc is not None and dct is not None:
                    met[f"dc_{tag}"] = round(math.copysign(dc, dct), 4)
                else:
                    met[f"dc_{tag}"] = None
        # capacitive-divider plateau -> effective device capacitance at 1 kHz
        h1k, ph1k = met.get("H_1k"), met.get("ph_1k")
        if (h1k is not None and ph1k is not None and 0 < h1k < 1
                and abs(ph1k) < 15 and not math.isnan(meta["c_ext_nf"])):
            met["c_dev_nf"] = round(meta["c_ext_nf"] * h1k / (1 - h1k), 3)
        else:
            met["c_dev_nf"] = None
        metrics.append(met)

        key = (meta["chem"], meta["pixel"], meta["day"])
        curves.setdefault(key, []).append(
            (meta["offset_v"], meta["amp_v"], f, H))

    wcsv(os.path.join(OUT, "lockin_manifest.csv"), manifest)
    wcsv(os.path.join(OUT, "lockin_metrics.csv"), metrics)

    # ---- QA figures: one panel per device-day, |H|(f) coloured by offset --
    for (chem, pixel, day), items in sorted(curves.items()):
        fig, ax = plt.subplots(figsize=(7, 4.5))
        offsets = sorted({o for o, a, _, _ in items})
        cmap = plt.cm.coolwarm
        for o, a, f, H in sorted(items, key=lambda x: (x[0], x[1])):
            if len(offsets) > 1 and (max(offsets) - min(offsets)) > 0:
                c = cmap((o - min(offsets)) / (max(offsets) - min(offsets)))
            else:
                c = "k"
            ax.plot(f, H, lw=0.8, color=c, alpha=0.7,
                    label=f"{o:+.1f} V / {a:g} Vpk")
        ax.set_xscale("log")
        ax.set_xlabel("frequency (Hz)")
        ax.set_ylabel("|H| = Vout/Vin,rms")
        ax.set_title(f"{chem}-{pixel} day {day}")
        ax.axhline(1.0, color="grey", lw=0.5, ls=":")
        handles, labels = ax.get_legend_handles_labels()
        seen, hh, ll = set(), [], []
        for h, l in zip(handles, labels):
            if l not in seen:
                seen.add(l)
                hh.append(h)
                ll.append(l)
        ax.legend(hh, ll, fontsize=5, ncol=2, frameon=False)
        fig.tight_layout()
        fig.savefig(os.path.join(QADIR, f"{chem}-{pixel}_d{day:02d}.png"),
                    dpi=130)
        plt.close(fig)

    n_ok = sum(r.get("parsed", 0) for r in manifest)
    print(f"files: {len(manifest)}  parsed: {n_ok}")
    print(f"demod2 duplicate of demod4: "
          f"{sum(r.get('demod2_dup', 0) for r in manifest)}/{n_ok}")
    print(f"descending sweeps: {sum(r.get('descending', 0) for r in manifest)}/{n_ok}")
    print(f"wrote {OUT}/lockin_manifest.csv, {OUT}/lockin_metrics.csv, "
          f"{len(curves)} QA panels in {QADIR}/")


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


if __name__ == "__main__":
    main()
