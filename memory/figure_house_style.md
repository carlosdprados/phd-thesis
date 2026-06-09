---
name: figure-house-style
description: Unified sans-serif figure house style (scripts/figstyle.py) applied to Ch2-5; Ch1 raster gap
metadata:
  type: project
---

2026-06-09 figures pass: introduced **`scripts/figstyle.py`**, a shared house
style every figure script now imports (`import figstyle; figstyle.apply()`).
It sets a Nature-like sans-serif look: **Helvetica → Arial → DejaVu Sans** text
with **`mathtext.fontset="stixsans"`** for matching sans-serif maths, de-spined
axes (`axes.spines.top/right=False`), frameless legends, outward ticks, embedded
TrueType (`pdf.fonttype=42`), and the shared `COLORS` palette (blue `#276FBF`,
green `#1B9E77`, orange `#D95F02`, red `#C43C39`, purple `#6A4C93`, grays).

Helpers: `panel(ax, "a", "title")` renders a **bold lower-case letter + title as
a single LEFT-aligned title** (mathtext-bold letter — collision-proof on narrow
panels; do NOT go back to centred dual-title, it collided); `box(ax)` restores
all four spines for heatmaps/imshow; `keepspine(ax2,"right")` re-adds a twin/
secondary axis spine after the global de-spine (needed for EPSC trace, EIS t½,
UV-Vis energy axis).

Applied to **all matplotlib figures in Ch2, Ch3 (bridge), Ch4, Ch5**. Bugs fixed
along the way (were rendering literally — scripts don't use usetex): `(\%)`→`(%)`,
`NM\_v114`→`NM_v114`, `on--off`→`on/off`, ATR `\&`; ASCII `->` arrows. Redrawn:
Ch2 SI morphology (two single-value bars → annotated film cross-section) and Ch4
`design_space` (legends moved to right margin off the data). Label declutter:
Ch5 `tau_coverage` (leader lines fan labels off clustered τ dots), `physio_context`
panel a (rotated x labels).

**Gap:** Chapter 1's 14 figures are raster **PNGs with no generating script in
the repo** (`figures/chapter1/ch1_fig*.png`) — they are still the old serif look
and were NOT restyled. Chapter 6 has no figures. If full-thesis font consistency
is wanted, Ch1 needs its source pipeline located/rebuilt — a separate effort.
Orphan (generated but never `\includegraphics`'d) Ch4 figures: `iratr_fingerprint`,
`iratr_triflate_nsSO3`, `iratr_host_crystallinity` (the used composite is
`iratr_chemistry`). See [[thesis_jury_audit_polish]], [[chapter4_wesad_results]].
