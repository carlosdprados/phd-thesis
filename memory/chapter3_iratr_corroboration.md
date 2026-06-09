---
name: chapter3-iratr-corroboration
description: Ch3 §3.5 IR-ATR + XRD microscopic corroboration of the chemistry axis — added 2026-06-05
metadata: 
  node_type: memory
  type: project
  originSessionId: 2f5bb10c-6ede-4cf3-9fae-b28a5e76f6c3
---

Ch3 §3.5 folded in IR-ATR (ATR-FTIR) corroboration on the **chemistry** axis (2026-06-05),
complementing the EIS corroboration of the **composition** axis ([[chapter3_eis_corroboration]]).

Source: electrode-free spectroscopy samples v126–v139 (films/scratched powders of the
SY/polyether/metal-triflate blend, all at lead cell 0.3/0.09) in `DEVICES_LAB_DATA`, folders
`*IRATR*`, data in `Day1_ATR/` as 2-col .csv(comma)/.dpt(tab) transmittance + raw OPUS binary;
`ITO/` = substrate blank, blank-named .txt = film/powder note. `corr`/`corrfin` = OPUS
atmos+baseline corrected (inconsistent in batch 3).

ATR findings (illustrative, n=1/chemistry, mixed film/powder): (1) triflate+polyether bands
confirm constituents in all chemistries; (2) **headline** — triflate ν_s(SO₃) at ~1029–1032
cm⁻¹ in all six host×cation samples, no cation-resolved shift → microscopically corroborates
"cation is not a clean lever"; (3) PEO resolved C–O–C multiplet vs TMPE broad band → host
structural correlate; (4) humidity glovebox-vs-ambient sub-series is an **honest null**
(contact-dominated), excluded.

**XRD added (same v126–v133 samples, `Day1_XRD/`, .xy = 2θ/counts, shared `ITO_Test/` blank):**
all patterns are dominated by crystalline ITO substrate (21.5/30.6/35.5°, in the blank); after
subtraction film residuals are weak & not PEO-specific → **composite is X-ray amorphous** (no
PEO crystallites at 19.1/23.3°, no crystalline salt phase, every chemistry). This **CORRECTED**
ATR finding (3): host order is *local/conformational* (ATR), NOT bulk crystallinity (XRD) —
chapter wording changed from "semicrystalline PEO" to "locally ordered, globally amorphous".
Plus: salt is dissolved → homogeneous composite. Humidity set has no XRD.

**UV-Vis added (third leg, 2026-06-05):** JASCO UV-Vis on 2025 TMPE-host blends v317–v320
(`2025-Q1_Devices`, `Day1_UV-Vis/`, SY/TMPE/salt cation series Li/Na/K + salt-free v320, **Au**
generation; `<ion>_View*.csv`=abs vs nm, `<ion>_conv*.csv`=Kubelka-Munk vs eV; `;`-delim comma
decimal). **SY π–π* peak ~446 nm, onset ~2.50 eV IDENTICAL across Li/Na/K** (salt-free matches
at band edge) → cation does not shift SY optical gap → electronic-structure leg, underwrites
"vary ion transport, hold SY electronic backbone fixed". Illustrative (n=1, separate
Au/2025/TMPE generation, positions-only, deep-UV unreliable). fig:ch3_uvvis,
`scripts/ch3_uvvis.py`, handout 18.

The three microscopic probes now in §3.5/§3.7: ATR=ion association+local order, XRD=morphology
(amorphous), UV-Vis=electronic structure — all reinforce "cation not a clean lever".

Artifacts: `scripts/ch3_iratr.py` (3-panel fig:ch3_iratr a=νsSO₃, b=ATR C–O–C, c=XRD),
`scripts/ch3_xrd.py`, `scripts/ch3_uvvis.py`, figs `iratr_chemistry.pdf` + `uvvis_bandedge.pdf`
(+ standalone `xrd_amorphous.pdf`), handouts 16 (ATR), 17 (XRD), 18 (UV-Vis), `ch3_iratr_bands.csv`.
Commits a54d2bb + 70fc22d (ATR), XRD analysis+integration, UV-Vis analysis+integration (2026-06-05).
