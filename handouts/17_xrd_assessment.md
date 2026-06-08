# Handout 17 — XRD dataset: assessment for Chapter 4 (and a correction to the ATR host claim)

**Date:** 2026-06-05
**Script:** `scripts/ch4_xrd.py` · **Figure:** `figures/chapter4/xrd_amorphous.pdf`

## 1. What the data is

PANalytical Empyrean XRD (Cu-Kα) on the **same v126–v133 host×cation samples** as the
IR-ATR set (SY/polyether/metal-triflate blend on ITO, no top electrode, lead cell 0.3/0.09).
Clean data = 2-col `.xy` (2θ, counts); also `.xrdml`, `.csv` (header+data), and PANalytical
`.rd/.udf/.x00`. **Every folder carries a shared `ITO_Test/` blank** (bare ITO substrate) —
essential, because the films are thin and the substrate dominates.

Matrix (n=1 each): PEO/Li v126, PEO/Na v127, PEO/K v128, TMPE/Li v129, TMPE/Na v130,
TMPE/K v131; plus batch-2 PEO/Li v132 & TMPE/Li v133. (Humidity set v134–139 has **no** XRD.)

## 2. Finding — the composite films are X-ray amorphous

The prominent peaks in **all** samples — 21.5°, 30.6°, 35.5° — are the crystalline **ITO
substrate** (In₂O₃ bixbyite): they appear identically in the **ITO_Test blank**. After
scaling the blank to the substrate peak and subtracting, the film residuals are weak
(PEO-doublet residual ≈ 55–120 counts vs residual RMS ≈ 30–35, i.e. ≲2–3× noise) and **not
PEO-specific** (PEO and TMPE samples give comparable residuals).

- **No sharp PEO crystalline doublet** (~19.1° / 23.3°): bulk PEO crystallisation is
  **suppressed** in the SY/salt composite.
- **No crystalline metal-triflate salt phase**: the salt is dissolved/amorphous, not
  segregated as crystallites (no sharp Li/Na/K-triflate peaks in any sample).
- Holds across host and cation → a **homogeneous, X-ray-amorphous composite** in every cell.

**Caveat:** thin films on a crystalline substrate → XRD is near its sensitivity floor here;
"no long-range crystallinity detected" cannot exclude small/few crystallites below detection.
n=1 per chemistry, illustrative tier.

## 3. Bearing on the IR-ATR host claim (a correction)

Handout 16 / §3.5 currently reads the ATR C–O–C multiplet as PEO being **"semicrystalline"**.
XRD shows that is **too strong at the long-range-order level**: PEO does **not** form bulk
crystallites in the composite. The two probes are reconciled if framed by length scale:

- **ATR** (local, ~nm conformational order): PEO retains resolved C–O–C multiplet →
  **short-range / conformational order** (helical PEO sequences); TMPE amorphous.
- **XRD** (long-range, crystallites): **neither** host is crystalline in the composite.

→ **Recommended wording fix:** replace "semicrystalline PEO" with "PEO retains *local/
conformational* order (ATR) without forming long-range crystallites (XRD)". The host→mobility
→relaxation argument is unaffected (it only needs PEO's local order/lower segmental freedom
vs amorphous TMPE), and the chapter becomes *more* rigorous, not less.

## 4. Recommendation

**Include briefly**, as the third microscopic probe on the chemistry axis (with EIS on the
composition axis), value being:
1. **Positive:** the polymer-electrolyte composite is a **homogeneous amorphous medium** — no
   crystalline salt segregation, no bulk PEO crystallites — the expected matrix for ion
   transport. The `ITO_Test` blank makes this rigorous (substrate-resolved).
2. **Corrective:** disciplines the ATR host reading from "semicrystalline" to "locally
   ordered", which is the honest, defensible statement.

Slot: one figure (`fig:ch4_iratr`, panel c) + 2–3 sentences folded into the host paragraph of §4.5,
right after the ATR crystallinity sentence; update the §4.7 discussion clause likewise.
Do **not** over-claim; this is a null/amorphous + corrective result, not a new positive lever.
