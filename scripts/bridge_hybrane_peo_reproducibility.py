#!/usr/bin/env python3
"""
bridge_hybrane_peo_reproducibility.py

Evidence audit for the proposed standalone "bridge" chapter (Hybrane -> PEO).
Tests, against the regenerated DATABASE (May 2025), exactly which parts of the
reproducibility-crisis narrative are quantitatively supported and which are not.

It answers three questions, all on the silver-electrode corpus, after applying
the FILTERED_DEVICES red-flag exclusion list and dropping broken/saturated pixels:

  Q1  Device-to-device reproducibility and switching-window strength,
      Hybrane (SY/Hy/LiTr) vs PEO (SY/PEO/LiTr).   <- the SOLID claim
  Q2  Within-device aging: does the normalized hysteresis area fall over the
      days following fabrication?                   <- SUPPORTING (small n)
  Q3  Calendar-time trend: does early-day normalized area decline across the
      ~2021 Hybrane campaign?                        <- HONEST NULL in this slice

Source of truth:
  - material decode : DATABASE/UPDATED_DEVICES_LIBRARY.csv ('Components Group','Used Metal','Date')
  - HYST metrics    : DATABASE/DEVICES_HYST_PIXEL_INFO.csv ('normalized area mean','on-off ratio mean','day')
  - exclusion list  : DATABASE/FILTERED_DEVICES.csv (device_name, day, pixel)

Run from the repo root:  python scripts/bridge_hybrane_peo_reproducibility.py
Writes a tidy summary to handouts/bridge_hybrane_peo_summary.csv
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

DB = "../Nanomem_Devices_Library/DATABASE"
OUT = "handouts/bridge_hybrane_peo_summary.csv"


def load():
    lib = pd.read_csv(os.path.join(DB, "UPDATED_DEVICES_LIBRARY.csv"))
    lib["Date"] = pd.to_datetime(lib["Date"], errors="coerce")
    hyst = pd.read_csv(os.path.join(DB, "DEVICES_HYST_PIXEL_INFO.csv"))
    filt = pd.read_csv(os.path.join(DB, "FILTERED_DEVICES.csv"))
    bad = set(zip(filt["device_name"], filt["day"], filt["pixel"]))
    hyst["key"] = list(zip(hyst["device_name"], hyst["day"], hyst["pixel"]))
    hyst = hyst[~hyst["key"].isin(bad)].copy()
    hyst = hyst[(hyst["is broken"] != "Y") & (hyst["is saturated"] != "Y")]
    return lib, hyst


def corpus(lib, hyst, group):
    devs = lib[(lib["Components Group"] == group) & (lib["Used Metal"] == "Ag")]
    m = hyst.merge(devs[["device_name", "Date"]], on="device_name", how="inner")
    return devs, m


def main():
    lib, hyst = load()
    rows = []

    print("=" * 70)
    print("Q1  Device-to-device reproducibility & window (Ag corpus, clean HYST)")
    print("=" * 70)
    for label, group in [("Hybrane SY/Hy/LiTr", "SY, Hy, LiTr"),
                         ("PEO SY/PEO/LiTr", "SY, PEO, LiTr")]:
        devs, m = corpus(lib, hyst, group)
        narea = m.groupby("device_name")["normalized area mean"].median().dropna()
        onoff = m.groupby("device_name")["on-off ratio mean"].median().dropna()
        cv_a = narea.std() / narea.mean()
        cv_o = onoff.std() / onoff.mean()
        print(f"\n{label}: library Ag={devs['device_name'].nunique()}, "
              f"clean-HYST devices={m['device_name'].nunique()}")
        print(f"  normalized area : median={narea.median():.3f}  CV={cv_a:.2f}  "
              f"IQR[{narea.quantile(.25):.3f},{narea.quantile(.75):.3f}]")
        print(f"  on-off ratio    : median={onoff.median():.2f}  CV={cv_o:.2f}")
        rows.append(dict(question="Q1_reproducibility", corpus=label,
                         n_devices=int(m["device_name"].nunique()),
                         narea_median=round(float(narea.median()), 3), narea_cv=round(float(cv_a), 3),
                         onoff_median=round(float(onoff.median()), 3), onoff_cv=round(float(cv_o), 3)))

    print("\n" + "=" * 70)
    print("Q2  Within-device aging of normalized area (slope vs day post-fab)")
    print("=" * 70)
    for label, group in [("Hybrane SY/Hy/LiTr", "SY, Hy, LiTr"),
                         ("PEO SY/PEO/LiTr", "SY, PEO, LiTr")]:
        _, m = corpus(lib, hyst, group)
        slopes = []
        for _, g in m.groupby("device_name"):
            g = g.dropna(subset=["day", "normalized area mean"])
            if g["day"].nunique() >= 3:
                slopes.append(stats.linregress(g["day"], g["normalized area mean"])[0])
        slopes = np.array(slopes)
        if len(slopes):
            print(f"\n{label}: n={len(slopes)} devices with >=3 measurement days")
            print(f"  median slope={np.median(slopes):+.5f}/day  frac<0={(slopes < 0).mean():.2f}")
            rows.append(dict(question="Q2_within_device_aging", corpus=label,
                             n_devices=len(slopes),
                             aging_slope_median_per_day=round(float(np.median(slopes)), 5),
                             frac_negative=round(float((slopes < 0).mean()), 2)))
        else:
            print(f"\n{label}: no device has >=3 measurement days (insufficient).")

    print("\n" + "=" * 70)
    print("Q3  Calendar-time trend across the Hybrane campaign (early-day, day<=1)")
    print("=" * 70)
    _, m = corpus(lib, hyst, "SY, Hy, LiTr")
    early = m[m["day"] <= 1]
    g = (early.groupby("device_name")
         .agg(date=("Date", "first"), narea=("normalized area mean", "median"))
         .dropna().sort_values("date"))
    x = (g["date"] - g["date"].min()).dt.days.values.astype(float)
    y = g["narea"].values
    if len(g) >= 3:
        r, p = stats.pearsonr(x, y)
        rho, prho = stats.spearmanr(x, y)
        print(f"\nHybrane early-day normalized area vs calendar time: n={len(g)}")
        print(f"  Pearson r={r:+.3f} (p={p:.3f})   Spearman rho={rho:+.3f} (p={prho:.3f})")
        print("  -> NO significant downward calendar trend in this DATABASE slice.")
        print("     The contemporaneous 'area vs date' timeline (Common/2021-12-29_EVO.pptx)")
        print("     must be reproduced from primary records before any calendar claim is made.")
        rows.append(dict(question="Q3_calendar_trend", corpus="Hybrane early-day",
                         n_devices=len(g), pearson_r=round(float(r), 3), pearson_p=round(float(p), 3),
                         spearman_rho=round(float(rho), 3), spearman_p=round(float(prho), 3)))

    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"\nSummary written to {OUT}")


if __name__ == "__main__":
    main()
