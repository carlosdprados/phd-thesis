#!/usr/bin/env python3
"""
bridge_hybrane_peo_reproducibility.py

Evidence audit for the proposed standalone "bridge" chapter (Hybrane -> PEO).
Tests, against the regenerated DATABASE (May 2025), exactly which parts of the
reproducibility-crisis narrative are quantitatively supported and how.

CORRECTED FRAMING (per author, 2026-06-06):
  The degradation is a BATCH-over-CALENDAR-TIME collapse attributed to the
  physical Hybrane reagent stock aging -- NOT individual devices aging after
  fabrication. The signal in the DATABASE is therefore a *device-health /
  conductivity collapse* across successive batches, not a "smaller normalized
  loop area" on surviving devices (shorted devices are flagged out, so the
  area metric alone misses it).

Three questions, all on the silver-electrode corpus:

  Q1  Device-to-device reproducibility & switching-window strength,
      Hybrane (SY/Hy/LiTr) vs PEO (SY/PEO/LiTr), on valid (non-broken,
      non-saturated) devices.                                  <- SOLID
  Q2  Hybrane device-health collapse over calendar time: fraction of pixels
      flagged broken/saturated, and median current, by month.  <- THE SIGNAL
  Q3  Why the normalized-area metric alone does NOT show a clean decline.

CAVEAT carried into the chapter: the mid-2021 Hybrane corpus is enriched in
*deliberately stressed* controls (no-Hybrane, no-salt, air exposure, old-SY,
baby-chamber transport), so natural stock-aging is not cleanly separable from
intentional stress experiments in the DATABASE alone. The qualitative campaign
narrative lives in the Fabrication/Characterization Notes (see handout 22).

Source of truth:
  - material decode & TRUE dates : DATABASE/DEVICES_LIBRARY.csv ('Date' is full
    date here; UPDATED_DEVICES_LIBRARY.csv coarsens Date to month -- do not use
    it for the timeline).
  - components/metal             : DATABASE/UPDATED_DEVICES_LIBRARY.csv
  - HYST metrics                 : DATABASE/DEVICES_HYST_PIXEL_INFO.csv
  - red-flag exclusion           : DATABASE/FILTERED_DEVICES.csv

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
    libo = pd.read_csv(os.path.join(DB, "DEVICES_LIBRARY.csv"))
    libo["Date"] = pd.to_datetime(libo["Date"], errors="coerce")  # TRUE dates
    up = pd.read_csv(os.path.join(DB, "UPDATED_DEVICES_LIBRARY.csv"))
    lib = libo[["device_name", "Date"]].merge(
        up[["device_name", "Components Group", "Used Metal"]], on="device_name", how="left")
    hyst = pd.read_csv(os.path.join(DB, "DEVICES_HYST_PIXEL_INFO.csv"))
    filt = pd.read_csv(os.path.join(DB, "FILTERED_DEVICES.csv"))
    bad = set(zip(filt["device_name"], filt["day"], filt["pixel"]))
    return lib, hyst, bad


def corpus(lib, hyst, group):
    devs = lib[(lib["Components Group"] == group) & (lib["Used Metal"] == "Ag")]
    return devs, hyst.merge(devs[["device_name", "Date"]], on="device_name", how="inner")


def main():
    lib, hyst, bad = load()
    rows = []

    # ---- Q1: reproducibility & window on VALID devices --------------------
    print("=" * 72)
    print("Q1  Device-to-device reproducibility & window (Ag, valid devices)")
    print("=" * 72)
    for label, group in [("Hybrane SY/Hy/LiTr", "SY, Hy, LiTr"),
                         ("PEO SY/PEO/LiTr", "SY, PEO, LiTr")]:
        devs, m = corpus(lib, hyst, group)
        v = m[(m["is broken"] != "Y") & (m["is saturated"] != "Y")]
        v = v[~v.set_index(["device_name", "day", "pixel"]).index.isin(bad)]
        narea = v.groupby("device_name")["normalized area mean"].median().dropna()
        onoff = v.groupby("device_name")["on-off ratio mean"].median().dropna()
        print(f"\n{label}: library Ag={devs['device_name'].nunique()}, valid-HYST devices={len(narea)}")
        print(f"  normalized area : median={narea.median():.3f}  CV={narea.std()/narea.mean():.2f}")
        print(f"  on-off ratio    : median={onoff.median():.2f}  CV={onoff.std()/onoff.mean():.2f}")
        rows.append(dict(question="Q1_reproducibility", corpus=label, n_devices=len(narea),
                         narea_median=round(float(narea.median()), 3),
                         narea_cv=round(float(narea.std()/narea.mean()), 3),
                         onoff_median=round(float(onoff.median()), 3),
                         onoff_cv=round(float(onoff.std()/onoff.mean()), 3)))

    # ---- Q2: Hybrane device-health collapse over calendar time -----------
    print("\n" + "=" * 72)
    print("Q2  Hybrane device-health collapse over calendar time (THE signal)")
    print("=" * 72)
    _, m = corpus(lib, hyst, "SY, Hy, LiTr")
    m = m.copy()
    m["bad"] = (m["is broken"] == "Y") | (m["is saturated"] == "Y")
    m["ym"] = m["Date"].dt.to_period("M")
    g = m.groupby("ym").agg(devices=("device_name", "nunique"), pixels=("pixel", "size"),
                            frac_bad=("bad", "mean"),
                            current_uA_med=("mean current at max v (uA)", "median"))
    print(g.to_string(float_format=lambda x: f"{x:.2f}"))
    pre = m[m["Date"] < "2021-05-01"]
    post = m[(m["Date"] >= "2021-05-01") & (m["Date"] < "2022-01-01")]
    print(f"\n  Pre-inflection (<=Apr 2021): {pre['device_name'].nunique()} dev, "
          f"frac_bad={pre['bad'].mean():.2f}, median current={pre['mean current at max v (uA)'].median():.2f} uA")
    print(f"  Mid-decline (May-Dec 2021):  {post['device_name'].nunique()} dev, "
          f"frac_bad={post['bad'].mean():.2f}, median current={post['mean current at max v (uA)'].median():.2f} uA")
    print("  NOTE: mid-2021 corpus includes deliberately-stressed controls; "
          "natural stock-aging is not cleanly separable here (see handout 22).")
    for ym, r in g.iterrows():
        rows.append(dict(question="Q2_health_collapse", corpus=str(ym), n_devices=int(r["devices"]),
                         frac_broken_saturated=round(float(r["frac_bad"]), 3),
                         current_uA_median=round(float(r["current_uA_med"]), 2)))

    # ---- Q3: why normalized-area alone does not show the decline ---------
    print("\n" + "=" * 72)
    print("Q3  Normalized-area-only trend is NOT a clean decline (explained)")
    print("=" * 72)
    v = m[(m["is broken"] != "Y") & (m["is saturated"] != "Y")].dropna(subset=["normalized area mean"])
    fd = v.groupby("device_name")["day"].transform("min")
    dev = (v[v["day"] == fd].groupby("device_name")
           .agg(date=("Date", "first"), narea=("normalized area mean", "median")).dropna().sort_values("date"))
    x = (dev["date"] - dev["date"].min()).dt.days.values.astype(float)
    y = dev["narea"].values
    r, p = stats.pearsonr(x, y)
    print(f"\nValid-device freshest-day normalized area vs date: n={len(dev)}, Pearson r={r:+.3f} (p={p:.3f}).")
    print("Only ~20 Hybrane/Ag devices survive as non-saturated; the degraded majority")
    print("become high-conductivity shorts (Q2) and are flagged out, so the area metric")
    print("on survivors does NOT trend down. The reproducible degradation metric is Q2,")
    print("and the batch-by-batch timeline figure should be sourced from the contemporaneous")
    print("record (Common/2021-12-29_EVO.pptx, 2021-12-03_gold&degr.pptx) -- see handout 22.")
    rows.append(dict(question="Q3_area_only_trend", corpus="Hybrane valid freshest-day",
                     n_devices=len(dev), pearson_r=round(float(r), 3), pearson_p=round(float(p), 3)))

    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"\nSummary written to {OUT}")


if __name__ == "__main__":
    main()
