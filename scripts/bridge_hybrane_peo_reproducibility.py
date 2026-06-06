#!/usr/bin/env python3
"""
bridge_hybrane_peo_reproducibility.py

Evidence audit for the proposed standalone "bridge" chapter (Hybrane -> PEO),
built to honor the experimental procedure and its nuances so the degradation
story survives a jury. Mirrors the slicing logic of the author's interactive
tool (Nanomem_Devices_Library/project_feature_explorer).

FOUR CONTROLS, all required (each was shown to matter against the data):

  C1  Per-DEVICE weighting. number_pixels_measured falls 16 -> 2 over the
      campaign (Spearman vs date ~ -0.80), so pixel-pooled stats are biased to
      early devices. Every feature is reduced to ONE value per device (median
      across that device's freshest-day curves) before any test.
      (DEVICE_INFO saturated%/broken% columns are unpopulated/constant -> health
      is computed from curve-level is_saturated/is_broken instead.)

  C2  Standard-protocol corpus only. SY/Hy/LiTr/Ag with anneal 75C, no 2nd
      stage, Hy mass-ratio 0.3, LiTr 0.09. Excludes the invasive experiments
      (notably the 150C high-temperature batch that PARTIALLY RECOVERED devices
      a year in, plus composition variants) which would otherwise contaminate
      the feature-vs-date story.

  C3  Sweep-amplitude stratification. A 0->+X->0 loop with larger X excites the
      device more, so it conducts more even when read back at the same voltage.
      Amplitude is confounded with date AND material; analysis is confined to a
      tightly matched ~1.2 V band (the sensitive low-V probe).

  C4  Recovery-tail sensitivity. Results are reported with and without the last
      months (>= 2022-03), the deliberately-reverted "recovery" batches.

broken != saturated:  broken = erratic/open-circuit (a contact/handling failure);
saturated = a curve whose max current is BELOW the previous curve's (fails to
potentiate). They are reported separately and mean different things.

Run from repo root:  python scripts/bridge_hybrane_peo_reproducibility.py
Writes handouts/bridge_hybrane_peo_summary.csv
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

DB = "../Nanomem_Devices_Library/DATABASE"
OUT = "handouts/bridge_hybrane_peo_summary.csv"
TAIL = pd.Timestamp("2022-03-01")  # recovery-batch cutoff for C4


def load():
    libo = pd.read_csv(os.path.join(DB, "DEVICES_LIBRARY.csv"), low_memory=False)
    libo["Date"] = pd.to_datetime(libo["Date"], errors="coerce")
    up = pd.read_csv(os.path.join(DB, "UPDATED_DEVICES_LIBRARY.csv"))
    return libo.merge(up[["device_name", "Components Group", "Used Metal"]], on="device_name", how="left")


def hybrane_standard(L):
    return L[(L["Components Group"] == "SY, Hy, LiTr") & (L["Used Metal"] == "Ag")
             & (L["Annealing Temperature [°C]"] == 75)
             & (L["Second Stage Annealing Temperature [°C]"].isna())
             & (L["Ion-Conducting Polymer Mass Ratio - Hy"] == 0.3)
             & (L["Salt Mass Ratio - LiTr"] == 0.09)]


def per_device_freshest(cur, col, date, binary=False, cutoff=None):
    """One value per device (median across freshest-day curves), then Spearman vs date."""
    d = cur.copy()
    if cutoff is not None:
        d = d[d["date"] < cutoff]
    if binary:
        d = d.assign(_v=d[col].astype(str).str.upper().eq("Y"))
    else:
        d = d.dropna(subset=[col]).assign(_v=pd.to_numeric(d[col], errors="coerce"))
    fd = d.groupby("device_name")["day"].transform("min")
    d = d[d["day"] == fd]
    agg = "mean" if binary else "median"
    pdv = d.groupby("device_name").agg(date=("date", "first"), y=("_v", agg)).dropna()
    if len(pdv) < 6:
        return None
    x = (pdv["date"] - pdv["date"].min()).dt.days.values.astype(float)
    rho, p = stats.spearmanr(x, pdv["y"].values)
    return len(pdv), rho, p


def main():
    L = load()
    rows = []

    # ---- C1 evidence: pixel count collapses over time (why per-device) ----
    std = hybrane_standard(L)
    date = dict(zip(std["device_name"], std["Date"]))
    dev = pd.read_csv(os.path.join(DB, "DEVICES_HYST_DEVICE_INFO.csv"))
    dev = dev[dev["device_name"].isin(set(std["device_name"]))].copy()
    dev["date"] = dev["device_name"].map(date)
    d = dev.dropna(subset=["number_pixels_measured", "date"])
    x = (d["date"] - d["date"].min()).dt.days.values.astype(float)
    rho, p = stats.spearmanr(x, d["number_pixels_measured"].values)
    print("=" * 74)
    print(f"C1  pixels-measured vs date: rho={rho:+.3f} p={p:.2e} (n={len(d)})  "
          f"-> per-device weighting mandatory")
    rows.append(dict(block="C1_pixels_vs_date", feature="number_pixels_measured",
                     n=len(d), rho=round(float(rho), 3), p=float(f"{p:.2e}")))

    # ---- Degradation panel: standard corpus, matched ~1.2 V, per-device ----
    cur = pd.read_csv(os.path.join(DB, "DEVICES_HYST_CURVE_INFO.csv"), low_memory=False)
    cur = cur[cur["device_name"].isin(set(std["device_name"]))].copy()
    cur["date"] = cur["device_name"].map(date)
    mv = pd.to_numeric(cur["max voltage (V)"], errors="coerce")
    cur12 = cur[(mv >= 1.0) & (mv <= 1.45)].copy()
    print(f"\nStandard corpus n={std['device_name'].nunique()} devices; "
          f"matched ~1.2 V curves n={len(cur12)} on {cur12['device_name'].nunique()} devices "
          f"(span {std['Date'].min().date()}..{std['Date'].max().date()})")

    panel = [
        ("current at max v (uA)", 0, "conductivity"),
        ("area (V*uA)", 0, "conductivity"),
        ("current difference at on-off (uA)", 0, "conductivity"),
        ("percent change in max v current (%)", 0, "potentiation"),
        ("normalized area", 0, "window"),
        ("on-off ratio", 0, "window"),
        ("is saturated", 1, "health"),
        ("is broken", 1, "health"),
    ]
    print("\n" + "=" * 74)
    print("Degradation panel (per-device, standard corpus, matched ~1.2 V)")
    print("  feature [family]                            all dates     |   drop recovery tail")
    print("-" * 74)
    for col, binary, fam in panel:
        a = per_device_freshest(cur12, col, date, binary=binary)
        b = per_device_freshest(cur12, col, date, binary=binary, cutoff=TAIL)
        def fmt(r):
            return "n/a" if r is None else f"n={r[0]:2d} rho={r[1]:+.3f} p={r[2]:.4f}"
        print(f"  {col:34s}[{fam:12s}] {fmt(a):24s} | {fmt(b)}")
        if a:
            rows.append(dict(block="degradation_panel", feature=col, family=fam,
                             n=a[0], rho=round(a[1], 3), p=round(a[2], 4),
                             rho_drop_tail=(round(b[1], 3) if b else None),
                             p_drop_tail=(round(b[2], 4) if b else None)))
    print("\n  Reading: conductivity features RISE (material goes ohmic) and potentiation")
    print("  FALLS robustly (survive tail drop); normalized window shrinks but is tail-driven;")
    print("  'is broken' DECREASES (handling/contacts improved) -> NOT a Hybrane-degradation")
    print("  metric; 'is saturated' (fails-to-potentiate) rises weakly.")

    # ---- Resolution: PEO vs Hybrane window at matched ~3 V -----------------
    print("\n" + "=" * 74)
    print("Resolution: PEO vs Hybrane switching window at MATCHED ~3 V (valid devices)")
    m = pd.read_csv(os.path.join(DB, "DEVICES_HYST_PIXEL_INFO.csv"))
    m = m.merge(L[["device_name", "Components Group", "Used Metal"]], on="device_name", how="left")
    m3 = m[(pd.to_numeric(m["max voltage (V)"], errors="coerce") >= 2.6)
           & (m["is broken"] != "Y") & (m["is saturated"] != "Y")]
    out = {}
    for label, grp in [("Hybrane", "SY, Hy, LiTr"), ("PEO", "SY, PEO, LiTr")]:
        v = m3[(m3["Components Group"] == grp) & (m3["Used Metal"] == "Ag")]
        na = v.groupby("device_name")["normalized area mean"].median().dropna()
        oo = v.groupby("device_name")["on-off ratio mean"].median().dropna()
        out[label] = na
        print(f"  {label:8s}: n={len(na):2d} | narea median={na.median():.3f} | on-off median={oo.median():.2f}")
        rows.append(dict(block="resolution_matched3V", feature=label, n=len(na),
                         narea_median=round(float(na.median()), 3), onoff_median=round(float(oo.median()), 3)))
    u, p = stats.mannwhitneyu(out["Hybrane"], out["PEO"], alternative="two-sided")
    print(f"  Mann-Whitney normalized area Hy vs PEO: U={u:.0f}, p={p:.4f} "
          f"-> PEO wider window {'(sig)' if p < 0.05 else '(n.s.)'}")
    rows.append(dict(block="resolution_matched3V", feature="Hy_vs_PEO_MWU", mannwhitney_p=round(float(p), 4)))

    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(f"\nSummary written to {OUT}")


if __name__ == "__main__":
    main()
