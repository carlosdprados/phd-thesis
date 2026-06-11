#!/usr/bin/env python3
"""Findings pass over the uncategorized Au/TMPE/(Li,Na,K)OTf corpus.

Builds on the inventory written by uncat_au_tmpe_audit.py and re-parses raw
files where cycle- or tail-level detail is needed. Five analyses:

  F1  Polarity asymmetry: positive vs negative drive on the same substrate
      (NM_v316 Day-1 threshold test; bipolar dual sweeps; catalogued
      Hyst-vs-NegaHyst reference sweeps of the same Au/TMPE generation).
  F2  Sweep-rate dependence of the switching window (step-count series).
  F3  Constant-bias activation: current growth vs hold voltage.
  F4  Pulse-train potentiation (negative pulses) and depression (positive
      pulses) at negative read.
  F5  Fading memory after potentiation: Kohlrausch fits of the sparse-read
      relaxation tails -> tau, beta, t_half per salt on Au/TMPE.

Writes handouts/uncat_findings_{rate,pulse,relax,vconst,polarity}.csv and
figures/uncat_qa/F*.png. Run from repo root after the audit script.
"""
import os
import re
import csv
import math
import collections

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uncat_au_tmpe_audit as ua

OUT = "handouts"
FIG = "figures/uncat_qa"
SALT_C = {"LiTr": "#1f77b4", "NaTr": "#d62728", "KTr": "#2ca02c"}


def load_inventory():
    rows = list(csv.DictReader(open(os.path.join(OUT, "uncat_inventory.csv"))))
    for r in rows:
        for k, v in list(r.items()):
            if v in ("", None):
                r[k] = None
                continue
            try:
                r[k] = float(v)
            except (TypeError, ValueError):
                if v == "True":
                    r[k] = True
                elif v == "False":
                    r[k] = False
    return rows


def reparse(rel):
    return ua.parse_raw(os.path.join(ua.UNCAT, rel))


# ----------------------------------------------------------------- F1 ------
def f1_polarity(inv):
    print("\n" + "=" * 78)
    print("F1  POLARITY ASYMMETRY")
    print("=" * 78)
    # --- v316 day-1 threshold test (uncategorized copy) ---
    rows = [r for r in inv if "TestVthreshold" in str(r["file"]) and r["cls"] == "SWEEP"]
    print("\nNM_v316 Day 1 threshold sweeps (10 cycles each; pixel differs by sign):")
    print(f"{'branch':22s}{'amp':>5s}{'Ipk (A)':>11s}{'onoff_med':>10s}{'narea':>8s}")
    tab = []
    for r in sorted(rows, key=lambda r: (r["polarity"], abs(r["amp"]))):
        b = f"{r['polarity']} ({r['pixel']})"
        print(f"{b:22s}{r['amp']:5.1f}{r['i_peak_max']:11.2e}{r['onoff_med']:10.2f}{r['narea_med']:8.3f}")
        tab.append(dict(set="v316_threshold", branch=r["polarity"], pixel=r["pixel"],
                        amp=r["amp"], i_peak=r["i_peak_max"], onoff=r["onoff_med"]))
    # --- bipolar dual sweeps: per-cycle branch asymmetry ---
    print("\nBipolar dual sweeps, |I(-A)| / |I(+A)| (per file, median over cycles):")
    print(f"{'campaign':18s}{'pixel':6s}{'amp':>5s}{'rate':>8s}{'asym med':>10s}{'n_cyc':>6s}")
    for r in inv:
        if r["cls"] != "SWEEP" or r.get("polarity") != "BIPOLAR":
            continue
        try:
            I, V, T = reparse(r["file"])
        except Exception:
            continue
        amp = r["amp"]
        # split into cycles by sign structure: measure peak |I| near +amp and -amp
        near_p = np.abs(V - amp) < 0.05 * amp
        near_n = np.abs(V + amp) < 0.05 * amp
        if near_p.sum() < 2 or near_n.sum() < 2:
            continue
        asym = np.median(np.abs(I[near_n])) / max(np.median(np.abs(I[near_p])), 1e-13)
        print(f"{r['campaign']:18s}{str(r['pixel']):6s}{amp:5.1f}{r['rate_Vps']:8.3f}{asym:10.2f}{int(r['n_cycles_used'] or 0):6d}")
        tab.append(dict(set="dual", campaign=r["campaign"], pixel=r["pixel"], amp=amp,
                        asym_neg_over_pos=float(asym)))
    # --- catalogued reference: POS vs NEG sweeps of same generation ---
    ref = list(csv.DictReader(open(os.path.join(OUT, "uncat_reference_sweeps.csv"))))
    grp = collections.defaultdict(list)
    for r in ref:
        try:
            grp[(r["chem"], r["polarity"])].append(
                (float(r["onoff_med"]), float(r["narea_med"]), float(r["i_peak_max"])))
        except (ValueError, KeyError):
            continue
    print("\nCatalogued same-generation reference sweeps (v296-v316), medians:")
    print(f"{'chem':12s}{'pol':8s}{'n':>3s}{'onoff':>7s}{'narea':>8s}{'Ipk (A)':>11s}")
    for (chem, pol), v in sorted(grp.items()):
        a = np.median([x[0] for x in v]); b = np.median([x[1] for x in v])
        c = np.median([x[2] for x in v])
        print(f"{chem:12s}{pol:8s}{len(v):3d}{a:7.2f}{b:8.3f}{c:11.2e}")
        tab.append(dict(set="reference", chem=chem, branch=pol, n=len(v),
                        onoff=float(a), narea=float(b), i_peak=float(c)))
    ua.wcsv(os.path.join(OUT, "uncat_findings_polarity.csv"), tab)


# ----------------------------------------------------------------- F2 ------
def f2_rate(inv):
    print("\n" + "=" * 78)
    print("F2  SWEEP-RATE DEPENDENCE OF THE SWITCHING WINDOW")
    print("=" * 78)
    from scipy.stats import spearmanr
    series = collections.defaultdict(list)
    for r in inv:
        if r["cls"] != "SWEEP" or r.get("polarity") not in ("NEG", "POS"):
            continue
        if r.get("rate_Vps") is None or r.get("onoff_med") is None:
            continue
        key = (r["salt"], r["campaign"], str(r["pixel"]), r["amp"])
        series[key].append((r["rate_Vps"], r["onoff_med"], r["narea_med"]))
    tab = []
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    print(f"\n{'series (salt camp pix amp)':42s}{'n':>3s}{'rho(onoff,rate)':>16s}{'oo_slow':>8s}{'oo_fast':>8s}")
    for key, pts in sorted(series.items()):
        if len(pts) < 5:
            continue
        pts.sort()
        rates = np.array([p[0] for p in pts]); oo = np.array([p[1] for p in pts])
        rho, p = spearmanr(rates, oo)
        slow = float(np.median(oo[:2])); fast = float(np.median(oo[-2:]))
        lab = f"{key[0]} {key[1][-5:]} {key[2]} -{key[3]:.1f}V"
        print(f"{lab:42s}{len(pts):3d}{rho:10.2f} (p={p:.3f}){slow:8.2f}{fast:8.2f}")
        tab.append(dict(salt=key[0], campaign=key[1], pixel=key[2], amp=key[3],
                        n=len(pts), rho=float(rho), p=float(p),
                        onoff_slow=slow, onoff_fast=fast))
        ax = axes[0] if key[3] <= 2.0 else axes[1]
        ax.plot(rates, oo, "o-", ms=3, lw=0.8, color=SALT_C.get(key[0], "k"), alpha=0.7,
                label=lab)
    for ax, t in zip(axes, ("amp <= 2 V", "amp = 3 V")):
        ax.set_xscale("log"); ax.set_xlabel("sweep rate (V/s)")
        ax.set_ylabel("on/off at half-amplitude"); ax.set_title(t, fontsize=9)
        ax.axhline(1, color="0.6", lw=0.6)
        ax.legend(fontsize=4.5)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "F2_rate_dependence.png"), dpi=130)
    plt.close(fig)
    ua.wcsv(os.path.join(OUT, "uncat_findings_rate.csv"), tab)


# ----------------------------------------------------------------- F3 ------
def f3_vconst(inv):
    print("\n" + "=" * 78)
    print("F3  CONSTANT-BIAS ACTIVATION (drift of |I| during holds)")
    print("=" * 78)
    tab = []
    fig, ax = plt.subplots(figsize=(5, 3.4))
    print(f"\n{'campaign':18s}{'pixel':6s}{'Vhold':>7s}{'I_start':>10s}{'I_end':>10s}{'ratio':>8s}{'t63 s':>7s}")
    for r in sorted([r for r in inv if r["cls"] == "VCONST" and r.get("v_hold") is not None],
                    key=lambda r: (r["campaign"], str(r["pixel"]), r["v_hold"])):
        if r.get("drift_ratio") is None:
            continue
        print(f"{r['campaign']:18s}{str(r['pixel']):6s}{r['v_hold']:7.2f}{r['i_start']:10.1e}"
              f"{r['i_end']:10.1e}{r['drift_ratio']:8.2f}{r['t63']:7.0f}")
        tab.append(dict(campaign=r["campaign"], salt=r["salt"], pixel=r["pixel"],
                        v_hold=r["v_hold"], i_start=r["i_start"], i_end=r["i_end"],
                        drift=r["drift_ratio"], t63=r["t63"], dur=r["dur"]))
        ax.semilogy(abs(r["v_hold"]), r["drift_ratio"], "o", ms=4,
                    color=SALT_C.get(r["salt"], "k"), alpha=0.7)
    ax.set_xlabel("|V hold| (V)"); ax.set_ylabel("I_end / I_start")
    ax.axhline(1, color="0.6", lw=0.6)
    for s, c in SALT_C.items():
        ax.plot([], [], "o", color=c, label=s)
    ax.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "F3_vconst_activation.png"), dpi=130)
    plt.close(fig)
    ua.wcsv(os.path.join(OUT, "uncat_findings_vconst.csv"), tab)


# ----------------------------------------------------------------- F4 ------
def f4_pulses(inv):
    print("\n" + "=" * 78)
    print("F4  PULSE POTENTIATION / DEPRESSION (read at negative bias)")
    print("=" * 78)
    tab = []
    print(f"\n{'campaign':18s}{'pixel':6s}{'read':>6s}{'pulses':>14s}{'n_pul':>7s}"
          f"{'pot_ratio':>10s}{'grow':>6s}{'depot':>7s}{'sat':>4s}")
    for r in sorted([r for r in inv if r["cls"] == "PULSE"],
                    key=lambda r: (r["campaign"], str(r["pixel"]))):
        if r.get("pot_ratio") is None or r.get("floor_suspect"):
            continue
        depot = ""
        if r.get("pot_depot"):
            # re-parse to get depression ratio: last reads vs peak
            try:
                I, V, T = reparse(r["file"])
                info = ua.classify(I, V, T)
                base = info["v_read"]
                vr = np.round(V, 2)
                on_read = np.abs(vr - base) <= 0.05
                reads = np.abs(I[on_read])
                k = max(1, reads.size // 50)
                sm = np.convolve(reads, np.ones(k) / k, mode="same")
                depot = f"{float(sm[-max(2, reads.size//100):].mean() / max(sm.max(), 1e-13)):.3f}"
            except Exception:
                depot = "?"
        sat = "Y" if (r.get("read_sat") or r.get("any_sat")) else ""
        print(f"{r['campaign']:18s}{str(r['pixel']):6s}{r['v_read']:6.2f}"
              f"{str(r['pulse_levels']):>14s}{int(r['n_pulses']):7d}"
              f"{r['pot_ratio']:10.2f}{(r.get('growth_exp') or float('nan')):6.2f}{depot:>7s}{sat:>4s}")
        tab.append(dict(campaign=r["campaign"], salt=r["salt"], pixel=r["pixel"],
                        v_read=r["v_read"], pulse_levels=r["pulse_levels"],
                        n_pulses=int(r["n_pulses"]), period_s=r.get("period_s"),
                        pot_ratio=r["pot_ratio"],
                        growth_exp=r.get("growth_exp"), depot_ratio=depot or None,
                        sat=bool(r.get("read_sat") or r.get("any_sat")),
                        file=r["file"]))
    by_salt = collections.defaultdict(list)
    for t in tab:
        if not t["sat"]:
            by_salt[t["salt"]].append(t["pot_ratio"])
    print("\nper-salt potentiation ratio (unsaturated files): median [IQR] (n)")
    for s, v in sorted(by_salt.items()):
        q = np.percentile(v, [25, 50, 75])
        print(f"  {s}: {q[1]:.1f}  [{q[0]:.1f}-{q[2]:.1f}]  (n={len(v)})")
    print("\nprotocol-matched subset (pulses include -5 V, read -2.25 V, unsaturated):")
    for s in ("LiTr", "NaTr", "KTr"):
        v = [t["pot_ratio"] for t in tab
             if t["salt"] == s and not t["sat"] and t["v_read"] == -2.25
             and "-5" in str(t["pulse_levels"])]
        if v:
            q = np.percentile(v, [25, 50, 75])
            print(f"  {s}: {q[1]:.1f}  [{q[0]:.1f}-{q[2]:.1f}]  (n={len(v)})")
    ua.wcsv(os.path.join(OUT, "uncat_findings_pulse.csv"), tab)

    # ---- F6: pulse-interval (frequency) series --------------------------
    print("\nF6  PULSE-INTERVAL DEPENDENCE (matched level/count series)")
    from scipy.stats import spearmanr
    grp = collections.defaultdict(list)
    for t in tab:
        key = (t["campaign"], str(t["pixel"]), t["pulse_levels"], t["n_pulses"], t["v_read"])
        grp[key].append(t)
    print(f"{'series':52s}{'n':>3s}{'rho(pot,period)':>17s}")
    for key, ts in sorted(grp.items(), key=lambda kv: str(kv[0])):
        pers = sorted({round(x.get('period_s') or 0, 3) for x in ts})
        if len(ts) < 4 or len(pers) < 4:
            continue
        x = [t2["period_s"] for t2 in ts]
        y = [t2["pot_ratio"] for t2 in ts]
        rho, p = spearmanr(x, y)
        lab = f"{key[0][-9:]} {key[1]} {key[2]} x{int(key[3])} rd{key[4]}"
        print(f"{lab:52s}{len(ts):3d}{rho:9.2f} (p={p:.3f})")


# ----------------------------------------------------------------- F5 ------
def f5_relax(inv):
    print("\n" + "=" * 78)
    print("F5  FADING MEMORY AFTER POTENTIATION (Kohlrausch fits of tails)")
    print("=" * 78)
    tab = []
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.2), sharey=False)
    axmap = {"LiTr": 0, "NaTr": 1, "KTr": 2}
    print(f"\n{'campaign':18s}{'pixel':6s}{'read':>6s}{'tail s':>8s}{'drop':>6s}"
          f"{'tau s':>8s}{'beta':>6s}{'t1/2 s':>8s}{'t50 s':>8s}{'ok':>3s}")
    for r in sorted([r for r in inv if r["cls"] == "PULSE" and (r.get("tail_s") or 0) > 10],
                    key=lambda r: (r["salt"], r["campaign"])):
        try:
            I, V, T = reparse(r["file"])
        except Exception:
            continue
        info = ua.classify(I, V, T)
        base = info["v_read"]
        vr = np.round(V, 2)
        lv = ua.runs(list(np.abs(vr - base) <= 0.05))
        val, s, ln = lv[-1]
        if not val or ln < 8:
            continue
        seg = slice(s + 1, s + ln)
        y = np.abs(I[seg]); t = T[seg]
        tau, beta, th, ok = ua.kohlrausch_fit(t, y)
        t50 = ua.t50_model_free(t, y)
        drop = 1 - y[-max(2, y.size // 20):].mean() / max(y[: max(2, y.size // 20)].mean(), 1e-30)
        print(f"{r['campaign']:18s}{str(r['pixel']):6s}{base:6.2f}{r['tail_s']:8.0f}{drop:6.2f}"
              f"{tau:8.1f}{beta:6.2f}{th:8.1f}{t50:8.1f}{'Y' if ok else 'n':>3s}")
        tab.append(dict(campaign=r["campaign"], salt=r["salt"], pixel=r["pixel"],
                        v_read=base, tail_s=r["tail_s"], drop=float(drop), tau=tau,
                        beta=beta, t_half=th, t50=t50, fit_ok=ok, file=r["file"]))
        if r["salt"] in axmap and np.isfinite(tau):
            ax = axes[axmap[r["salt"]]]
            ax.semilogy(t - t[0], y / y[0], ".-", ms=2, lw=0.6, alpha=0.7,
                        label=f"{r['campaign'][-5:]} {r['pixel']} t½={th:.0f}s")
    for s, i in axmap.items():
        axes[i].set_title(s, fontsize=9); axes[i].set_xlabel("t after last pulse (s)")
        axes[i].legend(fontsize=4.5)
    axes[0].set_ylabel("|I_read| / first")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "F5_relaxation_tails.png"), dpi=130)
    plt.close(fig)
    by_salt = collections.defaultdict(list)
    for t in tab:
        if t["drop"] > 0.3 and abs(t["v_read"]) > 0.1 and np.isfinite(t["t50"]):
            by_salt[t["salt"]].append((t["t50"], t["t_half"] if t["fit_ok"] else np.nan))
    print("\nper-salt decay (nonzero read, drop>0.3): model-free t50 / Kohlrausch t1/2")
    for s, v in sorted(by_salt.items()):
        t50s = [x[0] for x in v]
        ths = [x[1] for x in v if np.isfinite(x[1])]
        print(f"  {s}: t50 med {np.median(t50s):7.1f} s (n={len(t50s)}: "
              f"{sorted(round(x,1) for x in t50s)})")
        if ths:
            print(f"        Kohlrausch t1/2 med {np.median(ths):7.1f} s (n={len(ths)})")
    ua.wcsv(os.path.join(OUT, "uncat_findings_relax.csv"), tab)

    # ---- drive-history -> decay-time lever: join with pulse table -------
    try:
        pul = {p["file"]: p for p in csv.DictReader(
            open(os.path.join(OUT, "uncat_findings_pulse.csv")))}
        pts = []
        for t in tab:
            p = pul.get(t["file"])
            if p and t["drop"] > 0.3 and abs(t["v_read"]) > 0.1 and np.isfinite(t["t50"]):
                try:
                    pts.append((float(p["pot_ratio"]), t["t50"], t["salt"]))
                except ValueError:
                    pass
        if len(pts) >= 8:
            from scipy.stats import spearmanr
            rho, p = spearmanr([x[0] for x in pts], [x[1] for x in pts])
            print(f"\ndrive-history lever: Spearman(pot_ratio, t50) = {rho:.2f} "
                  f"(p={p:.4f}, n={len(pts)})")
    except FileNotFoundError:
        pass


def main():
    inv = load_inventory()
    f1_polarity(inv)
    f2_rate(inv)
    f3_vconst(inv)
    f4_pulses(inv)
    f5_relax(inv)


if __name__ == "__main__":
    main()
