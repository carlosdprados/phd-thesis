#!/usr/bin/env python3
"""
bridge_hybrane_peo_reproducibility.py

Evidence audit for the proposed standalone "bridge" chapter (Hybrane -> PEO).
Establishes, against the regenerated DATABASE (May 2025), only the claims that
survive a protocol confound that dominates ionic memristors.

THE CONFOUND (author, 2026-06-06): hysteresis is a 0 -> +X -> 0 loop. A larger
sweep amplitude X drives more ionic redistribution, so the device is "more
excited" and conducts more (and shows a different loop area) even when read back
at the same voltage. The Hybrane corpus was swept mostly at ~1.2 V, PEO mostly
at ~2-3 V, and the Hybrane sweep grew from ~1.2 V (early 2021) to ~3 V (later).
Therefore EVERY feature-vs-time or Hybrane-vs-PEO comparison must be done WITHIN
a matched sweep-amplitude stratum (binned from 'max voltage (V)'). Reading at a
fixed voltage from raw does NOT fix this, because the device *state* at that read
still depends on X -- so the earlier fixed-1V reconstruction was dropped.

What survives stratification (the chapter's quantitative spine):
  Q1  PEO has a wider switching window than Hybrane at MATCHED ~3 V
      (normalized area, on-off; Mann-Whitney).            <- resolution, holds
  Q2  Within Hybrane, normalized area at fixed ~1.2 V sweep DECLINES over the
      campaign (Spearman vs fabrication date).            <- degradation, holds

What does NOT survive (report honestly as confounded / inconclusive):
  Q3  on-off-vs-time and conductance-vs-time within strata; PEO-vs-Hybrane CV.

Qualitative only (carry the deliberate-stress caveat):
  Q4  device-health collapse (fraction broken/saturated rises to ~1.0).

Source of truth: DATABASE/{DEVICES_LIBRARY.csv (TRUE dates), UPDATED_DEVICES_LIBRARY.csv
(components/metal), DEVICES_HYST_PIXEL_INFO.csv}. v061/v064 multi-day stability is a
Hybrane *positive* -> Chapter-2 SI, not here (only their fresh-day points enter Q2).

Run from repo root:  python scripts/bridge_hybrane_peo_reproducibility.py
Writes handouts/bridge_hybrane_peo_summary.csv
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

DB = "../Nanomem_Devices_Library/DATABASE"
OUT = "handouts/bridge_hybrane_peo_summary.csv"


def load():
    libo = pd.read_csv(os.path.join(DB, "DEVICES_LIBRARY.csv"))
    libo["Date"] = pd.to_datetime(libo["Date"], errors="coerce")
    up = pd.read_csv(os.path.join(DB, "UPDATED_DEVICES_LIBRARY.csv"))
    lib = libo[["device_name", "Date"]].merge(
        up[["device_name", "Components Group", "Used Metal"]], on="device_name", how="left")
    m = pd.read_csv(os.path.join(DB, "DEVICES_HYST_PIXEL_INFO.csv"))
    m = m.merge(lib, on="device_name", how="inner")
    # sweep-amplitude stratum from the per-pixel max voltage
    v = m["max voltage (V)"]
    m["vbin"] = np.where(v < 1.6, "~1.2V", np.where(v < 2.6, "~2V", "~3V"))
    return m


def corpus(m, group):
    return m[(m["Components Group"] == group) & (m["Used Metal"] == "Ag")]


def valid(df):
    return df[(df["is broken"] != "Y") & (df["is saturated"] != "Y")]


def dev_median(df, col):
    return df.groupby("device_name")[col].median().dropna()


def freshest(df, col):
    g = df.dropna(subset=["Date", col])
    fd = g.groupby("device_name")["day"].transform("min")
    return (g[g["day"] == fd].groupby("device_name")
            .agg(date=("Date", "first"), y=(col, "median")).dropna())


def main():
    m = load()
    H = corpus(m, "SY, Hy, LiTr")
    P = corpus(m, "SY, PEO, LiTr")
    rows = []

    # ---- Q1: matched-amplitude window contrast (resolution) --------------
    print("=" * 72)
    print("Q1  PEO vs Hybrane switching window at MATCHED ~3 V (valid devices)")
    print("=" * 72)
    out = {}
    for label, d in [("Hybrane", H), ("PEO", P)]:
        v = valid(d[d["vbin"] == "~3V"])
        na = dev_median(v, "normalized area mean")
        oo = dev_median(v, "on-off ratio mean")
        out[label] = na
        cv = na.std() / na.mean() if len(na) > 1 else float("nan")
        print(f"  {label:8s}: n={len(na):2d} dev | narea median={na.median():.3f} CV={cv:.2f} "
              f"| on-off median={oo.median():.2f}")
        rows.append(dict(question="Q1_window_matched3V", corpus=label, n_devices=len(na),
                         narea_median=round(float(na.median()), 3), narea_cv=round(float(cv), 3),
                         onoff_median=round(float(oo.median()), 3)))
    u, p = stats.mannwhitneyu(out["Hybrane"], out["PEO"], alternative="two-sided")
    print(f"  Mann-Whitney normalized area (Hy vs PEO): U={u:.0f}, p={p:.4f}  "
          f"-> PEO wider window {'(significant)' if p < 0.05 else '(n.s.)'}")
    print("  NOTE: at matched 3 V the CVs are comparable -> the pooled 'PEO more")
    print("        reproducible (CV 0.54->0.34)' claim was a protocol artifact; dropped.")
    rows.append(dict(question="Q1_window_matched3V_test", corpus="Hy_vs_PEO",
                     mannwhitney_U=float(u), mannwhitney_p=round(float(p), 4)))

    # ---- Q2: within-Hybrane area decline, stratified --------------------
    print("\n" + "=" * 72)
    print("Q2  Within-Hybrane normalized area vs fabrication date, by sweep bin")
    print("=" * 72)
    for tag, df in [("ALL (confounded)", H), ("~1.2V stratum", H[H["vbin"] == "~1.2V"]),
                    ("~3V stratum", H[H["vbin"] == "~3V"])]:
        d = freshest(df, "normalized area mean")
        x = (d["date"] - d["date"].min()).dt.days.values.astype(float)
        rho, pv = stats.spearmanr(x, d["y"].values)
        flag = "  <- survives" if (tag == "~1.2V stratum" and pv < 0.05) else ""
        print(f"  {tag:18s}: n={len(d):2d}  Spearman rho={rho:+.3f}  p={pv:.4f}{flag}")
        rows.append(dict(question="Q2_area_decline", corpus=tag, n_devices=len(d),
                         spearman_rho=round(float(rho), 3), spearman_p=round(float(pv), 4)))

    # ---- Q3: confounded / non-surviving trends (honest negatives) -------
    print("\n" + "=" * 72)
    print("Q3  Trends that do NOT survive stratification (reported as confounded)")
    print("=" * 72)
    for col in ["on-off ratio mean", "mean conductance at max v (uS)"]:
        line = []
        for b in ["~1.2V", "~3V"]:
            d = freshest(H[H["vbin"] == b], col)
            x = (d["date"] - d["date"].min()).dt.days.values.astype(float)
            rho, pv = stats.spearmanr(x, d["y"].values)
            line.append(f"{b}: rho={rho:+.3f} p={pv:.3f} (n={len(d)})")
            rows.append(dict(question="Q3_nonsurviving", corpus=f"{col} @ {b}", n_devices=len(d),
                             spearman_rho=round(float(rho), 3), spearman_p=round(float(pv), 3)))
        print(f"  {col:32s}: " + " | ".join(line))

    # ---- Q4: device-health collapse (qualitative) -----------------------
    print("\n" + "=" * 72)
    print("Q4  Hybrane device-health collapse over time (qualitative; stress-confounded)")
    print("=" * 72)
    h = H.copy()
    h["bad"] = (h["is broken"] == "Y") | (h["is saturated"] == "Y")
    g = h.groupby(h["Date"].dt.to_period("M")).agg(devices=("device_name", "nunique"),
                                                    frac_bad=("bad", "mean"))
    print(g.to_string(float_format=lambda x: f"{x:.2f}"))
    print("  CAVEAT: mid-2021 corpus enriched in deliberately-stressed controls; "
          "use as narrative, not as a clean stock-aging rate.")
    for ym, r in g.iterrows():
        rows.append(dict(question="Q4_health", corpus=str(ym), n_devices=int(r["devices"]),
                         frac_broken_saturated=round(float(r["frac_bad"]), 3)))

    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"\nSummary written to {OUT}")


if __name__ == "__main__":
    main()
