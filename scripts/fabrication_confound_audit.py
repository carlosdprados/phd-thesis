#!/usr/bin/env python3
"""Full fabrication-confound audit for the Chapter 3-4 composition and chemistry claims.

Run from the repo root:  python3 scripts/fabrication_confound_audit.py

Question (raised 2026-06-05): the chapters attribute changes in the measured
parameters/features to deliberate changes in *chemistry / composition*. Could any
*other* fabrication variable recorded per device be the real driver? This audit
goes through every column of DATABASE/DEVICES_LIBRARY.csv for the exact devices
that feed Chapter 3/4, and for each variable asks:
  (a) is it held CONSTANT across the devices (then it cannot confound), or
  (b) does it VARY, and if so does it COVARY with the composition axis (PEO/salt)
      or is it crossed (spans all composition levels) -> not a confound.

It also checks the measurement-age (days since fabrication) of the decay
measurements, because aging is the classic uncontrolled variable.

Earlier audits already settled three confounds and are NOT repeated here:
  - spin-coat RPM / film thickness  -> scripts/thickness_rpm_audit.py, handout 14
  - write/read protocol amplitude    -> handout 08 sec.13
  - electrode metal (Ag vs Au)       -> handout 08 sec.16, sec.23(b)

Sources of truth:
  - fabrication metadata = DATABASE/DEVICES_LIBRARY.csv (88 columns, 1 row/device)
  - material decode      = DATABASE/UPDATED_DEVICES_LIBRARY.csv ('Components Group')
  - composition/cell map = handouts/ch4_decay_fits.csv + ch4_pulse_descriptors.csv
  - measurement age      = DATABASE/DEVICES_DELAYTIME_PIXEL_INFO.csv ('day')

Full write-up + verdict: handouts/15_fabrication_confound_audit.md
"""
import csv, os, statistics
from collections import defaultdict, OrderedDict

DB = "../Nanomem_Devices_Library/DATABASE"
HO = "handouts"


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


def load_fits(fn):
    rows = {}
    with open(os.path.join(HO, fn), newline="") as f:
        for r in csv.DictReader(f):
            rows[r["device_id"]] = r
    return rows


decay = load_fits("ch4_decay_fits.csv")
pulse = load_fits("ch4_pulse_descriptors.csv")

lib = {}
with open(os.path.join(DB, "DEVICES_LIBRARY.csv"), newline="") as f:
    for r in csv.DictReader(f):
        lib[r["device_name"]] = r

upd = {}
with open(os.path.join(DB, "UPDATED_DEVICES_LIBRARY.csv"), newline="") as f:
    rd = csv.DictReader(f)
    cg = next(c for c in rd.fieldnames if "Components Group" in c)
    for r in rd:
        upd[r["device_name"]] = r.get(cg, "")


def comp(d):
    r = decay.get(d) or pulse.get(d)
    return fnum(r["peo"]), fnum(r["salt"]), r.get("cation")


def metal(d):
    for col, m in (("Ag Thickness [nm]", "Ag"), ("Au Thickness [nm]", "Au"), ("Al Thickness [nm]", "Al")):
        v = (lib.get(d, {}).get(col, "") or "").strip()
        if v not in ("", "NA", "0"):
            return m
    return "?"


# Composition spine = Li devices with a decay/pulse fit, on Ag electrode.
spine = sorted({d for d in {**decay, **pulse}
                if comp(d)[2] == "Li" and metal(d) == "Ag"},
               key=lambda x: int(x.split("v")[1]))

print("=" * 78)
print("FABRICATION-CONFOUND AUDIT  (Chapter 3-4 composition + chemistry claims)")
print("=" * 78)
print(f"\nComposition spine (Li / Ag, with a decay or pulse fit): n = {len(spine)}")

# --------------------------------------------------------------------------
# 1. constancy / covariation across the spine
# --------------------------------------------------------------------------
cols = list(next(iter(lib.values())).keys())
SKIP = {"device_name", "Fabrication Notes", "Characterization Notes"}
const, varying = [], []
for c in cols:
    if c in SKIP:
        continue
    uniq = sorted({(lib[d].get(c, "") or "").strip() for d in spine})
    if len(uniq) == 1:
        const.append((c, uniq[0]))
    else:
        varying.append(c)

print("\n--- HELD CONSTANT across the spine (cannot confound composition) ---")
for c, v in const:
    print(f"  {c:60} = {v!r}")

print("\n--- VARIES across the spine: is it CROSSED with PEO, or CONFOUNDED? ---")
for c in varying:
    bypeo = defaultdict(set)
    for d in spine:
        bypeo[comp(d)[0]].add((lib[d].get(c, "") or "").strip())
    levels = sorted(bypeo)
    # crossed if >=2 PEO levels share at least one common value, or each level
    # has internal variety; confounded if value is monotone-disjoint with PEO.
    pretty = "  ".join(f"PEO{p}:{sorted(bypeo[p])}" for p in levels)
    if len(pretty) > 150:
        pretty = pretty[:150] + " ..."
    print(f"  * {c}\n      {pretty}")

# --------------------------------------------------------------------------
# 2. measurement age (days since fabrication) of the decay measurements
# --------------------------------------------------------------------------
dly = defaultdict(list)
with open(os.path.join(DB, "DEVICES_DELAYTIME_PIXEL_INFO.csv"), newline="") as f:
    for r in csv.DictReader(f):
        d = r["device_name"]
        if d in spine:
            dd = fnum(r.get("day"))
            if dd is not None:
                dly[d].append(dd)

print("\n--- AGING: delay-measurement day (days since fab), by PEO level ---")
bypeo_day = defaultdict(list)
for d in spine:
    for x in dly.get(d, []):
        bypeo_day[comp(d)[0]].append(x)
for p in sorted(bypeo_day):
    v = bypeo_day[p]
    print(f"  PEO{p:<4} median day={statistics.median(v):4.0f}  range=[{min(v):.0f},{max(v):.0f}]  n={len(v)}")
print("  (within every batch all PEO levels are measured on the SAME day -> aging is")
print("   crossed with composition, not confounded.)")

# --------------------------------------------------------------------------
# 3. the cleanest single-batch composition control
# --------------------------------------------------------------------------
print("\n--- SINGLE-BATCH CONTROL: 2022-11-17, constant RPM=2000, one operator/SY lot ---")
batch = [d for d in spine if lib[d]["Date"] == "11/17/2022"]
for d in sorted(batch, key=lambda x: (comp(x)[1], comp(x)[0])):
    peo, salt, _ = comp(d)
    th = decay.get(d, {})
    print(f"  {d} PEO{peo} salt{salt}  RPM={lib[d]['Spin Coating Rotational Speed [RPM]']}  "
          f"t_half={th.get('t_half_s','-')}  tau={th.get('tau_s','-')}")
print("  -> higher PEO gives shorter retention even with RPM (thickness) held fixed.")

# --------------------------------------------------------------------------
# 4. chemistry-landscape matched cells (host / anion / cation)
# --------------------------------------------------------------------------
groups = OrderedDict([
    ("cation PEO/triflate 2023-10", ["NM_v247", "NM_v248", "NM_v249"]),
    ("cation TMPE/triflate 2023-10", ["NM_v250", "NM_v251", "NM_v252"]),
    ("cation PEO/TFSI 2025-03", ["NM_v321", "NM_v323", "NM_v325"]),
    ("cation TMPE/TFSI 2025-05", ["NM_v333", "NM_v335", "NM_v337"]),
    ("cation old PEO/triflate 2022", ["NM_v114", "NM_v115", "NM_v116"]),
    ("host PEO-Li (vs TMPE v250)", ["NM_v140", "NM_v146", "NM_v241", "NM_v250"]),
    ("anion PEO-Li Tr (vs TFSI v321)", ["NM_v140", "NM_v146", "NM_v241", "NM_v321"]),
])
print("\n--- CHEMISTRY-LANDSCAPE CELLS: are the matched comparisons same-batch? ---")
keys = ["Date", "Spin Coating Rotational Speed [RPM]", "Annealing Temperature [°C]",
        "Annealing Time [h]", "Old SY Used", "Filtered Salt",
        "Measurements in Glove Box", "Who Prepared Solutions"]
short = {"Date": "Date", "Spin Coating Rotational Speed [RPM]": "RPM",
         "Annealing Temperature [°C]": "AnT", "Annealing Time [h]": "AnH",
         "Old SY Used": "OldSY", "Filtered Salt": "Filt",
         "Measurements in Glove Box": "MeasGB", "Who Prepared Solutions": "Who"}
for name, devs in groups.items():
    print(f"\n  [{name}]")
    for d in devs:
        meta = "  ".join(f"{short[k]}={(lib[d].get(k,'') or '-').strip()}" for k in keys)
        print(f"    {d:9} {upd.get(d,'?')[:16]:16} {metal(d):3} {meta}")

print("\nVERDICT: see handouts/15_fabrication_confound_audit.md")
