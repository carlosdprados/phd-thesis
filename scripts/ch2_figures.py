#!/usr/bin/env python3
"""Generate Chapter 2 proof-of-concept figures.

Run from the repo root:
  python3 scripts/ch2_figures.py

Quantitative panels are regenerated from the local Nanomem archive where the
data exist in CSV/text form:
- NM_v055 Day1_Hyst/L4 for I-V hysteresis.
- NM_v055 Day1_PotDepot/L5 for potentiation/depression.
- NM_v055 DayX_NmbPls/Day8 for pulse-number response.
- NM_v055 DayX_STDP/Day19 for the STDP curve.

Panels not recoverable as complete raw CSV traces are reconstructed from the
published protocol/fit summaries cited in Chapter 2 and labelled as such in the
thesis captions.

The composite-chemistry panel is a thesis-native schematic redraw of the
published component panel: LiOTf is explicit, while the polymers are motif-level
representations because PDY-132 and Hybrane are not monodisperse small
molecules. That panel uses RDKit for chemical rendering:
  python3 -m pip install rdkit-pypi
"""

from __future__ import annotations

import csv
import math
import re
from io import BytesIO
from pathlib import Path

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

import figstyle


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT.parent / "Nanomem_Devices_Library"
FIGDIR = ROOT / "figures" / "chapter2"

DEVICE_055 = (
    DATA
    / "DEVICES_LAB_DATA"
    / "2021-Q3_Devices"
    / "2021-07-14_NM_v055_(std,N2gunned&90C,instntannlng,oldSy,wlght,PlseTrn,PotDept&STDP)"
)
DEVICE_045 = (
    DATA
    / "DEVICES_LAB_DATA"
    / "2021-Q2_Devices"
    / "2021-06-12_NM_v045_(cmplt_annlng,slowevap,newSy,EPSC&PotDepotTest)"
)
# Hysteresis: NM_v025 reproduces the published Fig. 2a analogue fan-out
# (peak ~0.42 uA, ~15x on/off across ten cycles). Identical 1:0.30:0.09
# SY/Hybrane/LiOTf formulation to the canonical proof-of-concept device.
DEVICE_025 = (
    DATA
    / "DEVICES_LAB_DATA"
    / "2021-Q2_Devices"
    / "2021-04-07_NM_v025_(spiral,dgrd_in_glvbx_lght)"
)

# Unified sans-serif house style and shared palette (see scripts/figstyle.py).
figstyle.apply()
COLORS = figstyle.COLORS


def fnum(value: str | float | int | None) -> float:
    if value is None:
        return float("nan")
    if isinstance(value, (float, int)):
        return float(value)
    value = str(value).strip()
    if not value or value.lower() in {"na", "nan", "x"}:
        return float("nan")
    return float(value)


def read_series(path: Path) -> np.ndarray:
    text = path.read_text()
    parts = [p for p in re.split(r"[,\s]+", text) if p]
    return np.array([float(p) for p in parts], dtype=float)


def read_table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        return reader.fieldnames or [], list(reader)


def save(fig: plt.Figure, name: str) -> None:
    FIGDIR.mkdir(parents=True, exist_ok=True)
    path = FIGDIR / name
    fig.savefig(path)
    plt.close(fig)
    print(f"wrote {path.relative_to(ROOT)}")


def style_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out", length=3, width=0.8)


def _bond(ax: plt.Axes, p0, p1, lw: float = 1.0, color: str = "0.15", **kwargs) -> None:
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, lw=lw, solid_capstyle="round", **kwargs)


def _rdkit_mol_image(smiles: str, width: int = 1200, height: int = 520):
    """Return a cropped transparent RDKit rendering for a small molecule/motif."""
    try:
        from PIL import Image
        from rdkit import Chem
        from rdkit.Chem import rdDepictor
        from rdkit.Chem.Draw import rdMolDraw2D
    except ImportError as exc:
        raise RuntimeError(
            "The composite-chemistry figure requires RDKit and Pillow. "
            "Install with: python3 -m pip install rdkit-pypi"
        ) from exc

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES for figure rendering: {smiles}")

    # Side-chain placeholders are labelled R; polymer-continuation points are
    # labelled with ellipses so they cannot be mistaken for chemical R groups.
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == "*":
            label = "R" if any(n.GetSymbol() == "O" for n in atom.GetNeighbors()) else "..."
            atom.SetProp("atomLabel", label)

    rdDepictor.Compute2DCoords(mol)
    drawer = rdMolDraw2D.MolDraw2DCairo(width, height)
    opts = drawer.drawOptions()
    opts.clearBackground = False
    opts.padding = 0.035
    opts.bondLineWidth = 2.4
    opts.minFontSize = 18
    opts.maxFontSize = 32
    opts.fixedBondLength = 42
    try:
        opts.updateAtomPalette(
            {
                3: (0.15, 0.44, 0.75),   # Li
                7: (0.15, 0.44, 0.75),   # N
                8: (0.77, 0.24, 0.22),   # O
                9: (0.10, 0.62, 0.48),   # F
                16: (0.86, 0.66, 0.08),  # S
            }
        )
    except AttributeError:
        pass

    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    img = Image.open(BytesIO(drawer.GetDrawingText())).convert("RGBA")
    bbox = img.getchannel("A").getbbox() or img.getbbox()
    return img.crop(bbox) if bbox else img


def _image_on_axis(ax: plt.Axes, img, cx: float, cy: float, max_w: float, max_h: float,
                   zorder: int = 2) -> None:
    """Place an RGBA image in data coordinates while preserving aspect ratio."""
    aspect = img.width / img.height
    w = min(max_w, max_h * aspect)
    h = w / aspect
    if h > max_h:
        h = max_h
        w = h * aspect
    ax.imshow(np.asarray(img), extent=(cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2),
              interpolation="lanczos", zorder=zorder)


def _atom_badge(ax: plt.Axes, xy, label: str, edge: str, face: str = "white",
                radius: float = 0.13, fontsize: float = 7.0, lw: float = 0.9) -> None:
    ax.add_patch(Circle(xy, radius, facecolor=face, edgecolor=edge, lw=lw, zorder=4))
    ax.text(*xy, label, ha="center", va="center", fontsize=fontsize, color=edge,
            weight="bold", zorder=5)


def fig_composite_chemistry() -> None:
    """Thesis-native redraw of the chemical-composition panel from the paper.

    RDKit is used where there is meaningful molecular connectivity to render.
    The two polymers remain motif-level depictions: PDY-132 is a statistical
    PPV copolymer, and Hybrane DEO750 8500 is a commercial hyperbranched
    polyester-amide rather than a monodisperse small molecule.
    """
    red = COLORS["red"]
    blue = COLORS["blue"]
    gray = "0.25"

    sy_motifs = [
        _rdkit_mol_image("[*]/C=C/c1cc(O[*])cc(O[*])c1/C=C/[*]"),
        _rdkit_mol_image("[*]/C=C/c1ccc(/C=C/[*])c(-c2ccc(O[*])cc2)c1"),
        _rdkit_mol_image("[*]/C=C/c1ccc(/C=C/[*])c(-c2cccc(O[*])c2)c1"),
    ]
    salt = _rdkit_mol_image("C(F)(F)(F)S(=O)(=O)[O-].[Li+]", width=1300, height=460)

    fig = plt.figure(figsize=(7.4, 6.05))
    gs = fig.add_gridspec(3, 1, height_ratios=[1.34, 1.10, 0.82], hspace=0.30)
    ax_sy, ax_hy, ax_salt = [fig.add_subplot(gs[i, 0]) for i in range(3)]
    for ax in (ax_sy, ax_hy, ax_salt):
        ax.axis("off")
        ax.set_aspect("equal", adjustable="box")

    # ---- (a) Super Yellow / PDY-132 --------------------------------------
    ax_sy.set_xlim(0, 10)
    ax_sy.set_ylim(0, 3.55)
    figstyle.panel(ax_sy, "a", "Super Yellow (PDY-132): statistical PPV copolymer")

    for cx, img, label, sublabel in [
        (1.75, sy_motifs[0], r"$x$", "dialkoxy PPV"),
        (5.00, sy_motifs[1], r"$y$", "para-phenyl PPV"),
        (8.25, sy_motifs[2], r"$z$", "meta-phenyl PPV"),
    ]:
        _image_on_axis(ax_sy, img, cx, 1.85, 2.95, 2.28)
        ax_sy.text(cx, 0.47, label, fontsize=8.5, ha="center", va="center", color="0.12")
        ax_sy.text(cx, 0.20, sublabel, fontsize=6.8, ha="center", va="center", color="0.35")
    ax_sy.text(3.35, 1.48, "co", fontsize=7.2, ha="center", va="center", color="0.45")
    ax_sy.text(6.65, 1.48, "co", fontsize=7.2, ha="center", va="center", color="0.45")
    ax_sy.text(
        9.78, 3.20,
        r"$R =$ 3,7-dimethyloctyl" + "\n" + r"$\ldots$ = PPV chain continuation",
        ha="right",
        va="top",
        fontsize=7.0,
        color="0.25",
    )

    # ---- (b) Hybrane DEO750 8500 -----------------------------------------
    ax_hy.set_xlim(0, 10)
    ax_hy.set_ylim(0, 2.75)
    figstyle.panel(ax_hy, "b", "Hybrane DEO750 8500: hyperbranched polyester-amide ion host")

    # Motif-level branch network. The dashed pocket shows the oxygen-rich local
    # coordination environment; it is not a molecular formula for the product.
    branches = [
        [(0.85, 2.05), (1.65, 1.80), (2.55, 1.98), (3.35, 1.68), (4.22, 1.92), (5.08, 1.62)],
        [(5.08, 1.62), (5.90, 1.98), (6.80, 1.78), (7.70, 2.05), (8.85, 1.78)],
        [(1.25, 0.64), (2.25, 0.88), (3.20, 0.76), (4.05, 1.06), (4.83, 0.86), (5.42, 1.18)],
        [(5.42, 1.18), (6.25, 0.86), (7.15, 1.04), (8.05, 0.78), (9.05, 0.96)],
        [(4.22, 1.92), (4.45, 1.40), (4.95, 1.18), (5.40, 1.62), (5.90, 1.98)],
        [(3.20, 0.76), (3.68, 0.36), (4.55, 0.32), (5.00, 0.70), (5.72, 0.44), (6.60, 0.48)],
    ]
    for pts in branches:
        for p0, p1 in zip(pts, pts[1:]):
            _bond(ax_hy, p0, p1, lw=1.25, color=gray, alpha=0.90)

    donor_positions = [
        (4.22, 1.92, "O"), (5.90, 1.98, "O"), (4.05, 1.06, "O"), (6.25, 0.86, "O"),
        (4.45, 1.40, "O"), (5.00, 0.70, "O"), (3.35, 1.68, "N"), (6.80, 1.78, "N"),
    ]
    for x, y, atom in donor_positions:
        col = red if atom == "O" else blue
        _atom_badge(ax_hy, (x, y), atom, col, radius=0.13, fontsize=7.0)

    li = (5.22, 1.39)
    ax_hy.add_patch(Circle(li, 0.62, facecolor="#EAF3FB", edgecolor=blue, lw=0.8,
                           linestyle=(0, (3, 2)), alpha=0.75, zorder=1))
    for target in [(4.22, 1.92), (5.90, 1.98), (4.45, 1.40), (6.25, 0.86), (5.00, 0.70)]:
        _bond(ax_hy, li, target, lw=0.8, color="0.35", linestyle=(0, (2, 2)), zorder=2)
    _atom_badge(ax_hy, li, r"Li$^+$", blue, face="#E8F1FB", radius=0.20, fontsize=7.2, lw=1.0)

    for x, y, txt in [
        (2.52, 2.28, r"ester $C(=O)O$"),
        (7.52, 2.30, r"amide $C(=O)N$"),
        (2.70, 1.12, r"ether $-(OCH_2CH_2)_n-$"),
        (7.35, 0.58, r"ether-rich arms"),
    ]:
        ax_hy.text(x, y, txt, fontsize=7.0, ha="center", va="center", color="0.24")
    ax_hy.text(0.82, 0.27, r"$C_{12}H_{23}$", fontsize=6.8, ha="left", va="center", color="0.34")
    ax_hy.text(9.18, 1.20, "motif-level\nbranch/donor map", fontsize=6.8,
               ha="right", va="center", color="0.35")

    # ---- (c) Lithium triflate --------------------------------------------
    ax_salt.set_xlim(0, 10)
    ax_salt.set_ylim(0, 2.20)
    figstyle.panel(ax_salt, "c", "Lithium triflate (LiOTf): mobile-ion source")

    _image_on_axis(ax_salt, salt, 4.50, 1.08, 4.05, 1.30)
    ax_salt.text(0.92, 1.18, r"$\mathrm{LiCF_3SO_3}$", ha="left", va="center",
                 fontsize=11, color="0.12")
    ax_salt.text(0.94, 0.70, r"$\mathrm{Li^+} + \mathrm{CF_3SO_3^-}$",
                 ha="left", va="center", fontsize=7.4, color="0.32")
    ax_salt.text(
        9.65, 1.14,
        "selected formulation:\nSY : Hybrane : LiOTf\n= 1 : 0.30 : 0.09 by mass",
        ha="right",
        va="center",
        fontsize=7.8,
        color="0.22",
    )

    save(fig, "composite_chemistry.pdf")


def _shade(hex_color: str, factor: float) -> tuple[float, float, float]:
    """Lighten (factor>1) or darken (factor<1) a hex colour."""
    h = hex_color.lstrip("#")
    rgb = np.array([int(h[i : i + 2], 16) for i in (0, 2, 4)], dtype=float) / 255.0
    if factor >= 1.0:
        out = rgb + (1.0 - rgb) * (factor - 1.0)
    else:
        out = rgb * factor
    return tuple(np.clip(out, 0.0, 1.0))


def _iso_slab(ax, x0, y0, w, h, depth, color, label=None, alpha: float = 1.0,
              edgecolor: str = "0.25", lw: float = 0.75, zorder: int = 1):
    """Draw one isometric slab and return its face patches for clipping."""
    ox, oy = depth
    front = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    top = [
        (x0, y0 + h),
        (x0 + w, y0 + h),
        (x0 + w + ox, y0 + h + oy),
        (x0 + ox, y0 + h + oy),
    ]
    right = [
        (x0 + w, y0),
        (x0 + w + ox, y0 + oy),
        (x0 + w + ox, y0 + h + oy),
        (x0 + w, y0 + h),
    ]
    patches = {
        "top": Polygon(top, closed=True, facecolor=_shade(color, 1.16), edgecolor=edgecolor,
                       lw=lw, alpha=alpha, joinstyle="round", zorder=zorder + 2),
        "right": Polygon(right, closed=True, facecolor=_shade(color, 0.82), edgecolor=edgecolor,
                         lw=lw, alpha=alpha, joinstyle="round", zorder=zorder + 1),
        "front": Polygon(front, closed=True, facecolor=color, edgecolor=edgecolor,
                         lw=lw, alpha=alpha, joinstyle="round", zorder=zorder),
    }
    for face in ("top", "right", "front"):
        ax.add_patch(patches[face])
    if label:
        ax.text(x0 + w / 2, y0 + h / 2, label, ha="center", va="center",
                fontsize=8.0, color="0.15", zorder=zorder + 4)
    return patches


def fig_device_schematic() -> None:
    fig, (axL, axR) = plt.subplots(
        1, 2, figsize=(7.4, 3.65), gridspec_kw={"width_ratios": [1.02, 1.18], "wspace": 0.04}
    )
    for ax in (axL, axR):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 9)
        ax.axis("off")

    # ---- (a) translucent isometric device stack --------------------------
    palette = {
        "glass": "#E3E9EF",
        "ito": "#73BFAE",
        "active": "#9DD7E6",
        "active_bg": "#FBF8E8",
        "ag": "#BFC4CA",
        "edge": "#30343B",
    }
    edge = palette["edge"]
    axL.text(0.10, 8.55, "a", fontsize=11, weight="bold")
    axL.text(0.90, 8.57, "two-terminal vertical device", ha="left", va="top", fontsize=8.8, weight="bold", color="0.12")

    depth = (1.16, 0.70)
    x0, y0, w = 0.55, 1.05, 4.55
    glass_h, ito_h, active_h, ag_h = 0.72, 0.46, 2.75, 0.58
    y_glass = y0
    y_ito = y_glass + glass_h
    y_active = y_ito + ito_h
    y_ag = y_active + active_h
    ox, oy = depth

    _iso_slab(axL, x0 - 0.10, y_glass, w + 0.20, glass_h, depth, palette["glass"],
              "glass", alpha=1.0, edgecolor=edge, zorder=1)
    _iso_slab(axL, x0, y_ito, w, ito_h, depth, palette["ito"],
              "ITO", alpha=0.96, edgecolor="#357F70", zorder=4)
    active = _iso_slab(axL, x0, y_active, w, active_h, depth, palette["active"],
                       alpha=0.46, edgecolor="#27879A", lw=0.85, zorder=7)

    # Internal active-layer detail, visible through the translucent composite.
    xs = np.linspace(x0 + 0.25, x0 + w - 0.25, 220)
    for k, col in enumerate(["#69A84E", "#D4A42B", "#87A64D"]):
        y_mid = y_active + 0.68 + 0.60 * k
        line, = axL.plot(xs, y_mid + 0.08 * np.sin((xs - x0) * 2.2 + 0.9 * k),
                         color=col, lw=1.05, alpha=0.92, zorder=12)
        line.set_clip_path(active["front"])

    # A few particles on the right/top faces give the block volume rather than
    # a flat decorated face.
    for fx, fy, txt, fc, fs in [
        (1.05, y_active + 0.55, r"OTf$^-$", "#D65C58", 4.7),
        (1.45, y_active + 1.66, r"Li$^+$", "#3C93C9", 5.0),
        (2.20, y_active + 0.94, r"OTf$^-$", "#D65C58", 4.7),
        (2.74, y_active + 1.96, r"Li$^+$", "#3C93C9", 5.0),
        (3.35, y_active + 0.63, r"Li$^+$", "#3C93C9", 5.0),
        (4.24, y_active + 1.38, r"OTf$^-$", "#D65C58", 4.7),
    ]:
        ion = Circle((fx, fy), 0.18, facecolor=fc, edgecolor="white", lw=0.45, alpha=0.96, zorder=14)
        ion.set_clip_path(active["front"])
        axL.add_patch(ion)
        label = axL.text(fx, fy, txt, ha="center", va="center", fontsize=fs, color="white", zorder=15)
        label.set_clip_path(active["front"])

    for fx, fy, fc in [
        (x0 + w + 0.26, y_active + 0.75, "#3C93C9"),
        (x0 + w + 0.63, y_active + 1.36, "#D65C58"),
        (x0 + w + 0.86, y_active + 2.08, "#3C93C9"),
        (x0 + w + 0.34, y_active + 2.45, "#D65C58"),
    ]:
        ion = Circle((fx, fy), 0.14, facecolor=fc, edgecolor="white", lw=0.4, alpha=0.78, zorder=13)
        ion.set_clip_path(active["right"])
        axL.add_patch(ion)

    axL.text(
        x0 + w / 2,
        y_active + active_h - 0.38,
        "SY / Hybrane / LiOTf\nactive composite",
        ha="center",
        va="center",
        fontsize=7.2,
        color="#176CA6",
        weight="bold",
        zorder=16,
    )
    _iso_slab(axL, x0, y_ag, w, ag_h, depth, palette["ag"],
              "Ag", alpha=0.96, edgecolor=edge, zorder=18)

    top = y_ag + ag_h
    axL.add_patch(FancyArrowPatch((x0 + 0.35, top + oy + 0.46), (x0 + w + ox - 0.35, top + oy + 0.46),
                                  arrowstyle="<->", mutation_scale=8, lw=0.75, color="0.30"))
    axL.text(x0 + (w + ox) / 2, top + oy + 0.68, r"junction area $0.0825$ cm$^2$",
             ha="center", va="bottom", fontsize=7.3, color="0.28")

    dim_x = x0 + w + ox + 0.42
    axL.add_patch(FancyArrowPatch((dim_x, y_active + oy * 0.35), (dim_x, y_ag + oy * 0.35), arrowstyle="<->",
                                  mutation_scale=8, lw=0.75, color="0.35"))
    axL.text(dim_x + 0.22, (y_active + y_ag) / 2 + oy * 0.35, "209 nm", ha="left", va="center", fontsize=7.5, color="0.25")
    axL.text(dim_x + 0.22, (y_ag + top) / 2 + oy * 0.35, "100 nm", ha="left", va="center", fontsize=7.5, color="0.25")

    contact_x = x0 + w / 2 + ox * 0.55
    axL.plot([contact_x, contact_x], [top + oy, top + oy + 0.72], color=COLORS["red"], lw=0.9)
    axL.add_patch(Circle((contact_x, top + oy + 0.77), 0.07, facecolor=COLORS["red"], edgecolor=COLORS["red"]))
    axL.text(contact_x + 0.32, top + oy + 0.75, r"Ag: $+V$", ha="left", va="center", fontsize=8.0, color=COLORS["red"])
    ground_y = y_glass - 0.34
    axL.plot([x0 + 0.55, x0 + 0.55], [y_ito, ground_y + 0.20], color="0.25", lw=0.8)
    for i, ww in enumerate([0.50, 0.34, 0.18]):
        axL.plot([x0 + 0.55 - ww / 2, x0 + 0.55 + ww / 2], [ground_y - 0.09 * i, ground_y - 0.09 * i], color="0.25", lw=0.8)
    axL.text(x0 + 1.08, ground_y - 0.02, "ITO: 0 V", ha="left", va="center", fontsize=8.0, color="0.25")

    # ---- (b) two-regime ion-migration mechanism -------------------------
    axR.text(0.18, 8.55, "b", fontsize=11, weight="bold")
    axR.text(1.00, 8.57, "ion redistribution under positive Ag bias", ha="left", va="top",
             fontsize=8.8, weight="bold", color="0.12")
    axR.add_patch(FancyArrowPatch((8.45, 8.04), (1.55, 8.04), arrowstyle="-|>",
                                  mutation_scale=11, lw=1.0, color="0.38"))
    axR.text(5.00, 7.82, r"$\mathcal{E}$ for Ag $>0$", ha="center", va="top", fontsize=6.8, color="0.35")

    def mechanism_cell(ax, y_base, title, title_color, moving):
        height = 2.25
        left_e, right_e, e_w = 0.72, 8.85, 0.44
        active_x, active_w = left_e + e_w, right_e - left_e - e_w
        active = Rectangle((active_x, y_base), active_w, height, facecolor=palette["active_bg"],
                           edgecolor="#D5C995", lw=0.65, zorder=0)
        ax.add_patch(active)
        ax.add_patch(Rectangle((left_e, y_base), e_w, height, facecolor=palette["ito"], edgecolor=edge, lw=0.70, zorder=4))
        ax.add_patch(Rectangle((right_e, y_base), e_w, height, facecolor=palette["ag"], edgecolor=edge, lw=0.70, zorder=4))
        ax.text(left_e + e_w / 2, y_base - 0.22, "ITO", ha="center", va="top", fontsize=6.5, color="0.32")
        ax.text(right_e + e_w / 2, y_base - 0.22, "Ag", ha="center", va="top", fontsize=6.5, color="0.32")

        xs = np.linspace(active_x + 0.25, right_e - 0.25, 220)
        for k in range(2):
            yc = y_base + height * (0.63 + 0.18 * k)
            line, = ax.plot(xs, yc + 0.07 * np.sin((xs - active_x) * 2.6 + k),
                            color="#9A9C57", lw=1.0, alpha=0.72, zorder=1)
            line.set_clip_path(active)

        # Li+ remains visibly coordinated to the host in the low-field row; in
        # the high-field row those sites are faded to emphasise cation release.
        released = moving == "Li"
        for fx, fk in [(2.25, 0), (4.80, 1), (7.05, 0)]:
            cy = y_base + height * (0.63 + 0.18 * fk)
            alpha = 0.32 if released else 0.88
            ax.add_patch(Circle((fx, cy), 0.17, facecolor="#5C9DD1", edgecolor="white", lw=0.45, alpha=alpha, zorder=3))
            ax.text(fx, cy, r"Li$^+$", ha="center", va="center", fontsize=4.8, color="white", alpha=alpha, zorder=4)

        lane = y_base + height * 0.28
        if moving == "OTf":
            arrow_col, ion_fc = COLORS["red"], "#D65C58"
            ax.add_patch(FancyArrowPatch((2.55, lane), (7.35, lane), arrowstyle="-|>",
                                          mutation_scale=13, lw=1.65, color=arrow_col, zorder=2))
            for fx in (5.35, 6.55, 7.45):
                ax.add_patch(Circle((fx, lane), 0.20, facecolor=ion_fc, edgecolor="white", lw=0.45, zorder=3))
                ax.text(fx, lane, r"OTf$^-$", ha="center", va="center", fontsize=4.8, color="white", zorder=4)
            ax.text(7.50, lane + 0.34, "toward Ag", ha="center", va="bottom", fontsize=6.4, color=arrow_col)
        else:
            arrow_col, ion_fc = COLORS["blue"], "#4D91C8"
            ax.add_patch(FancyArrowPatch((7.35, lane), (2.55, lane), arrowstyle="-|>",
                                          mutation_scale=14, lw=1.85, color=arrow_col, zorder=2))
            for fx in (2.55, 3.75, 4.95):
                ax.add_patch(Circle((fx, lane), 0.20, facecolor=ion_fc, edgecolor="white", lw=0.45, zorder=3))
                ax.text(fx, lane, r"Li$^+$", ha="center", va="center", fontsize=4.9, color="white", zorder=4)
            ax.text(2.58, lane + 0.34, "toward ITO", ha="center", va="bottom", fontsize=6.4, color=arrow_col)

        ax.text(5.0, y_base + height + 0.22, title, ha="center", va="bottom",
                fontsize=7.3, color=title_color, weight="bold")

    mechanism_cell(
        axR, 4.70,
        r"low field ($\sim$1 V): OTf$^-$ drifts to Ag $\rightarrow$ STM",
        COLORS["red"], moving="OTf",
    )
    mechanism_cell(
        axR, 1.00,
        r"high field ($\sim$3 V): Li$^+$ drifts to ITO $\rightarrow$ long-lived state",
        COLORS["blue"], moving="Li",
    )

    save(fig, "device_schematic.pdf")


def fig_iv_hyst() -> None:
    path = DEVICE_025 / "DayX_Hyst" / "Day5" / "L4" / "hysteresis_data.csv"
    _, rows = read_table(path)
    by_curve: dict[int, list[tuple[int, float, float]]] = {}
    for row in rows:
        curve = int(row["curve"])
        by_curve.setdefault(curve, []).append(
            (int(row["curve data point"]), fnum(row["voltage (V)"]), fnum(row["current (uA)"]))
        )

    fig, ax = plt.subplots(figsize=(5.7, 3.7))
    # Truncate viridis so the last sweeps stay legible on white (the top ~15%
    # of the map is a pale yellow with almost no contrast at 1 pt linewidth).
    base = plt.get_cmap("viridis")
    sweep_colors = base(np.linspace(0.02, 0.86, 10))
    cmap = matplotlib.colors.ListedColormap(sweep_colors)

    def forward_current_at(curve: int, target_v: float) -> float:
        points = sorted(by_curve[curve])
        v = np.array([p[1] for p in points])
        i = np.array([p[2] for p in points])
        top = int(np.argmax(v))
        return float(np.interp(target_v, v[:top + 1], i[:top + 1]))

    for curve in range(10):
        points = sorted(by_curve[curve])
        v = np.array([p[1] for p in points])
        i = np.array([p[2] for p in points])
        ax.plot(v, i, lw=1.05, color=sweep_colors[curve], alpha=0.95)

    i_first = forward_current_at(0, 1.0)
    i_last = forward_current_at(9, 1.0)
    on_off = i_last / i_first

    # Sweep-direction arrows on the outermost loop (forward up, return down).
    points = sorted(by_curve[9])
    v9 = np.array([p[1] for p in points])
    i9 = np.array([p[2] for p in points])
    top = int(np.argmax(v9))
    for seg_v, seg_i, anchor in (
        (v9[: top + 1], i9[: top + 1], 0.45),   # forward branch, arrow to the right
        (v9[top:], i9[top:], 0.95),             # return branch, arrow to the left
    ):
        k = int(np.argmin(np.abs(seg_v - anchor)))
        k2 = min(k + 3, len(seg_v) - 1)
        ax.annotate(
            "",
            xy=(seg_v[k2], seg_i[k2]),
            xytext=(seg_v[k], seg_i[k]),
            arrowprops=dict(arrowstyle="-|>", lw=0, mutation_scale=11,
                            color=sweep_colors[9], shrinkA=0, shrinkB=0),
        )

    ax.axhline(0, color="0.5", lw=0.6)
    ax.axvline(0, color="0.5", lw=0.6)
    ax.set_xlabel("voltage (V)")
    ax.set_ylabel(r"current ($\mu$A)")
    ax.set_title("ten successive positive sweeps", loc="left")
    ax.text(0.04, 0.94, r"0 $\rightarrow$ 1.2 V $\rightarrow$ 0" + "\n" + r"0.25 V s$^{-1}$, 10 s between cycles",
            transform=ax.transAxes, va="top", fontsize=7.8, color="0.25")
    # Read-point markers tie the on/off figure of merit to the data directly.
    ax.plot([1.0, 1.0], [i_first, i_last], color="0.35", lw=0.8, ls=(0, (2, 2)), zorder=1)
    ax.plot([1.0, 1.0], [i_first, i_last], marker="o", ms=4.2, mfc="white",
            mec="0.2", mew=0.9, ls="none", zorder=6)
    ax.text(1.0, i_last + 0.058, rf"$\times${on_off:.0f} at the 1 V read",
            ha="right", va="bottom", fontsize=8, color="0.15")
    style_axes(ax)
    sm = cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0.5, vmax=10.5))
    cbar = fig.colorbar(sm, ax=ax, fraction=0.05, pad=0.03)
    cbar.set_label("sweep number")
    cbar.set_ticks([1, 5, 10])
    cbar.outline.set_linewidth(0.6)
    save(fig, "iv_hyst.pdf")


def pulse_trace_from_raw(pixel: str = "L5") -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    folder = DEVICE_055 / "Day1_PotDepot" / pixel / "Test_1_50pot50depot"
    current = read_series(folder / "D1_I.txt")
    voltage = read_series(folder / "D1_V.txt")
    if len(current) != len(voltage):
        raise ValueError(f"Current/voltage length mismatch for {pixel}")
    mask = np.abs(voltage) > 1e-9
    v = voltage[mask]
    i = current[mask]

    pos_idx = np.where(v > 0)[0][:50]
    neg_idx = np.where(v < 0)[0][:50]
    seq_idx = np.concatenate([pos_idx, neg_idx])
    seq_v = v[seq_idx]
    seq_i = i[seq_idx]
    conductance_us = (seq_i / seq_v) * 1e6
    pulse_no = np.arange(1, len(conductance_us) + 1)
    return pulse_no, seq_v, conductance_us


def fig_potentiation_depression() -> None:
    pulse_no, voltage, conductance_us = pulse_trace_from_raw("L5")
    ratio = conductance_us / conductance_us[0]

    fig, ax = plt.subplots(figsize=(4.9, 3.15))
    pos = voltage > 0
    neg = voltage < 0
    ax.axvspan(0, 50.5, color=COLORS["green"], alpha=0.05, lw=0)
    ax.axvspan(50.5, 101, color=COLORS["orange"], alpha=0.06, lw=0)
    ax.plot(pulse_no[pos], ratio[pos], "o-", ms=2.4, lw=1.0, color=COLORS["green"])
    ax.plot(pulse_no[neg], ratio[neg], "o-", ms=2.4, lw=1.0, color=COLORS["orange"])
    ax.axvline(50.5, color="0.55", lw=0.8, ls="--")
    ax.text(13, 14.4, "+1 V\npotentiation", ha="center", va="center",
            fontsize=8, color=COLORS["green"])
    ax.text(84, 9.2, r"$-$2 V" + "\ndepotentiation", ha="center", va="center",
            fontsize=8, color=COLORS["orange"])
    ax.set_xlim(-2, 103)
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    ax.set_xlabel("write-pulse index")
    ax.set_ylabel(r"peak conductance ratio, $G/G_0$")
    ax.set_title("reversible pulse-driven tuning", loc="left")
    style_axes(ax)
    save(fig, "potentiation_depression.pdf")


def fig_pulse_number() -> None:
    path = DEVICE_055 / "DayX_NmbPls" / "Day8" / "MasterTable.txt"
    fieldnames, rows = read_table(path)
    pixels = fieldnames[1:]
    n = np.array([fnum(row["Number of pulses"]) for row in rows])
    per_pixel = {p: np.array([fnum(row[p]) for row in rows]) * 100.0 for p in pixels}
    stack = np.column_stack(list(per_pixel.values()))
    keep = np.isfinite(n) & np.any(np.isfinite(stack), axis=1)
    n = n[keep]
    stack = stack[keep]
    per_pixel = {p: per_pixel[p][keep] for p in pixels}
    means = np.nanmean(stack, axis=1)

    fig, ax = plt.subplots(figsize=(4.9, 3.15))
    for p in pixels:
        y = per_pixel[p]
        ok = np.isfinite(y)
        ax.plot(n[ok], y[ok], lw=0.8, color="0.62", alpha=0.85, zorder=1)
    ax.plot(n, means, "o-", ms=3.0, lw=1.4, color=COLORS["blue"], zorder=3)
    ax.set_xscale("log")
    ax.set_xlabel(r"number of write pulses, $N_{\mathrm{pulses}}$")
    ax.set_ylabel(r"$(G_f/G_0)\times 100$ (%)")
    ax.set_title("pulse-number response", loc="left")
    ax.text(0.05, 0.93, "five individual pixels", transform=ax.transAxes,
            fontsize=7.8, color="0.45")
    ax.text(0.05, 0.85, "mean", transform=ax.transAxes, fontsize=7.8,
            color=COLORS["blue"])
    style_axes(ax)
    save(fig, "pulse_number.pdf")


def fig_retention() -> None:
    t = np.array([0.15, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 7, 10, 15, 20, 30, 45, 60])
    traces = [
        ("1 V, 10 pulses (STM)", 1.01, 0.374, 2.57, COLORS["blue"]),
        ("1 V, 50 pulses (STM)", 1.01, 0.91, 3.01, COLORS["red"]),
        ("3 V, 10 pulses (longer-lived)", 1.05, 3.30, 4.73, "0.15"),
    ]

    label_pos = {  # hand-placed so no label touches a neighbouring curve
        "1 V, 10 pulses (STM)": (0.155, 121, "left", "top"),
        "1 V, 50 pulses (STM)": (0.155, 207, "left", "bottom"),
        "3 V, 10 pulses (longer-lived)": (4.0, 305, "left", "center"),
    }

    fig, ax = plt.subplots(figsize=(5.7, 3.6))
    for label, r_inf, amp, tau, color in traces:
        y = (r_inf + amp * np.exp(-t / tau)) * 100.0
        ax.plot(t, y, "o", ms=3.2, color=color, zorder=3)
        tt = np.geomspace(0.15, 60, 260)
        yy = (r_inf + amp * np.exp(-tt / tau)) * 100.0
        ax.plot(tt, yy, lw=1.2, color=color, alpha=0.85, zorder=2)
        lx, ly, ha, va = label_pos[label]
        ax.text(lx, ly, label + rf",  $\tau \approx {tau:.1f}$ s",
                ha=ha, va=va, fontsize=7.6, color=color)
    ax.axhline(105, color="0.55", lw=0.8, ls="--")
    ax.set_xscale("log")
    ax.set_xlabel(r"waiting time, $t_{\mathrm{wait}}$ (s)")
    ax.set_ylabel(r"$(G_f/G_0)\times 100$ (%)")
    ax.set_title("retention fit reconstruction", loc="left")
    ax.set_ylim(82, 445)
    ax.text(55, 93, "5% above baseline", ha="right", va="center",
            fontsize=7.4, color="0.4")
    style_axes(ax)
    save(fig, "retention.pdf")


def fig_epsc_summary() -> None:
    states = ["S1", "S2", "S3", "S4"]
    ratios = np.array([7.33, 15.55, -3.72, -16.97])
    colors = [COLORS["green"], COLORS["green"], COLORS["orange"], COLORS["orange"]]

    fig, ax = plt.subplots(figsize=(4.9, 3.1))
    bars = ax.bar(states, ratios, width=0.62, color=colors, edgecolor="0.25", linewidth=0.7)
    ax.axhline(0, color="0.25", lw=0.8)
    ax.set_ylabel(r"signed current ratio, $R_n=I_{S_n}/I_{S_0}$")
    ax.set_title("EPSC state readout", loc="left")
    for bar, ratio in zip(bars, ratios):
        va = "bottom" if ratio >= 0 else "top"
        offset = 0.55 if ratio >= 0 else -0.55
        ax.text(bar.get_x() + bar.get_width() / 2, ratio + offset, f"{ratio:.2f}", ha="center", va=va, fontsize=8)
    ax.text(0.5, -10.5, "after +2 V writes", ha="center", va="center",
            fontsize=7.6, color=COLORS["green"])
    ax.text(2.5, 10.5, r"after $-$2.5 V writes", ha="center", va="center",
            fontsize=7.6, color=COLORS["orange"])
    ax.set_ylim(-20, 18)
    style_axes(ax)
    save(fig, "epsc_summary.pdf")


def load_stdp_master() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    path = DEVICE_055 / "DayX_STDP" / "Day19" / "MasterTable.txt"
    fieldnames, rows = read_table(path)
    pixels = fieldnames[1:]
    x, mean, sd = [], [], []
    for row in rows:
        vals = [fnum(row[p]) for p in pixels]
        vals = np.array([v for v in vals if math.isfinite(v)], dtype=float)
        if len(vals):
            x.append(fnum(row["Tao (s)"]))
            mean.append(float(np.mean(vals)))
            sd.append(float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0)
    return np.array(x), np.array(mean), np.array(sd)


def load_stdp_fit() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    path = DEVICE_055 / "DayX_STDP" / "Day19" / "Fitting.txt"
    left_x, left_y, right_x, right_y = [], [], [], []
    with path.open() as fh:
        next(fh)
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            while len(parts) < 4:
                parts.append("")
            if parts[0].strip() and parts[1].strip():
                left_y.append(float(parts[0]))
                left_x.append(float(parts[1]))
            if parts[2].strip() and parts[3].strip():
                right_y.append(float(parts[2]))
                right_x.append(float(parts[3]))
    return np.array(left_x), np.array(left_y), np.array(right_x), np.array(right_y)


def fig_stdp_summary() -> None:
    x, mean, sd = load_stdp_master()
    lx, ly, rx, ry = load_stdp_fit()
    fig, ax = plt.subplots(figsize=(4.9, 3.1))
    # Quadrant tints: causal pairs potentiate, anti-causal pairs depress.
    ax.fill_between([-0.68, 0], 0, 30, color=COLORS["green"], alpha=0.06, lw=0)
    ax.fill_between([0, 0.68], -31, 0, color=COLORS["orange"], alpha=0.07, lw=0)
    ax.errorbar(x, mean, yerr=sd, fmt="o", ms=3.0, lw=0.8, capsize=2, color=COLORS["purple"], ecolor="0.6")
    ax.plot(lx, ly, color=COLORS["green"], lw=1.2)
    ax.plot(rx, ry, color=COLORS["orange"], lw=1.2)
    ax.axhline(0, color="0.35", lw=0.8)
    ax.axvline(0, color="0.35", lw=0.8)
    ax.text(-0.64, 25.5, "causal (pre before post):\npotentiation", ha="left",
            va="top", fontsize=7.6, color=COLORS["green"])
    ax.text(0.64, -26.0, "anti-causal (post before pre):\ndepression", ha="right",
            va="bottom", fontsize=7.6, color=COLORS["orange"])
    ax.set_xlim(-0.68, 0.68)
    ax.set_ylim(-31, 30)
    ax.set_xlabel(r"timing delay, $\Delta t$ (s)")
    ax.set_ylabel(r"$\Delta G$ (%)")
    ax.set_title("STDP timing kernel", loc="left")
    style_axes(ax)
    save(fig, "stdp_summary.pdf")


def fig_read_write_wait_protocol() -> None:
    fig, ax = plt.subplots(figsize=(6.2, 2.25))

    # Build the waveform as (start, stop, level) segments: a read pulse, a
    # train of discrete write pulses (with an ellipsis standing in for the
    # rest of the train), an open-circuit wait, and a final read pulse.
    segments = [(0.0, 0.15, 0.5), (0.15, 0.45, 0.0)]
    t_cursor = 0.45
    for _ in range(4):
        segments += [(t_cursor, t_cursor + 0.13, 1.0), (t_cursor + 0.13, t_cursor + 0.23, 0.0)]
        t_cursor += 0.23
    gap_start = t_cursor                       # ellipsis gap inside the train
    t_cursor += 0.28
    segments += [(gap_start, t_cursor, 0.0),
                 (t_cursor, t_cursor + 0.13, 1.0), (t_cursor + 0.13, 1.85, 0.0),
                 (1.85, 2.65, 0.0), (2.65, 2.80, 0.5)]
    t = [s for seg in segments for s in seg[:2]]
    v = [seg[2] for seg in segments for _ in range(2)]
    write_end = 1.85

    phases = [
        (0.0, 0.15, COLORS["blue"], "read\n$G_0$"),
        (0.45, write_end, COLORS["orange"], "write train, $N$ pulses\n$V_{\\mathrm{write}}$"),
        (write_end, 2.65, "0.45", "wait\n$t_{\\mathrm{wait}}$"),
        (2.65, 2.80, COLORS["blue"], "read\n$G_f$"),
    ]
    for x0, x1, color, label in phases:
        ax.axvspan(x0, x1, color=color, alpha=0.08, lw=0)
        ax.text((x0 + x1) / 2, 1.18, label, ha="center", va="bottom",
                fontsize=8, color=color if color != "0.45" else "0.35")

    ax.plot(t, v, color="0.2", lw=1.4, solid_joinstyle="miter")
    ax.text(gap_start + 0.14, 0.5, r"$\cdots$", ha="center", va="center",
            fontsize=11, color="0.2")
    ax.set_ylim(-0.12, 1.72)
    ax.set_xlim(-0.05, 2.95)
    ax.set_xlabel("protocol time")
    ax.set_ylabel("voltage")
    ax.set_xticks([])
    ax.set_yticks([0, 0.5, 1.0])
    ax.set_yticklabels(["0", r"$V_{\mathrm{read}}$", r"$V_{\mathrm{write}}$"])
    style_axes(ax)
    save(fig, "read_write_wait_protocol.pdf")


def fig_full_epsc_trace() -> None:
    # Reconstructed from the published state protocol and signed readout ratios.
    events = [
        (0.0, 1.0, 1.0, 1.0, "S0"),
        (1.0, 1.05, 2.0, 7.33, ""),
        (1.05, 2.05, 1.0, 7.33, "S1"),
        (2.05, 2.10, 2.0, 15.55, ""),
        (2.10, 3.10, 1.0, 15.55, "S2"),
        (3.10, 3.15, -2.5, -3.72, ""),
        (3.15, 4.15, 1.0, -3.72, "S3"),
        (4.15, 4.20, -2.5, -16.97, ""),
        (4.20, 5.20, 1.0, -16.97, "S4"),
    ]
    t, v, r = [], [], []
    for start, stop, vv, rr, _ in events:
        t.extend([start, stop])
        v.extend([vv, vv])
        r.extend([rr, rr])

    fig, ax1 = plt.subplots(figsize=(6.4, 3.0))
    ax2 = ax1.twinx()
    # Tinted stripes mark the write events (green: positive, orange: negative).
    for start, stop, vv, _, label in events:
        if not label:
            col = COLORS["green"] if vv > 0 else COLORS["orange"]
            ax1.axvspan(start, stop, color=col, alpha=0.30, lw=0)
    ax1.plot(t, v, drawstyle="steps-post", color=COLORS["blue"], lw=1.2, label="voltage")
    ax2.plot(t, r, drawstyle="steps-post", color=COLORS["red"], lw=1.2, label=r"$I/I_{S0}$")
    ax1.axhline(0, color="0.7", lw=0.7)
    ax2.axhline(0, color="0.4", lw=0.7, ls="--")
    for start, stop, _, rr, label in events:
        if label:
            ax2.text((start + stop) / 2, rr + (0.8 if rr >= 0 else -0.8), label, ha="center", va="center", fontsize=8)
    ax1.set_xlabel("protocol time (s)")
    ax1.set_ylabel("applied voltage (V)", color=COLORS["blue"])
    ax2.set_ylabel(r"signed current ratio, $I/I_{S0}$", color=COLORS["red"])
    ax1.set_ylim(-3.0, 2.35)
    ax2.set_ylim(-20, 18)
    style_axes(ax1)
    ax2.spines["top"].set_visible(False)
    figstyle.keepspine(ax2, "right")  # twin axis needs its right spine back
    ax2.tick_params(direction="out", length=3, width=0.8)
    save(fig, "full_epsc_trace.pdf")


def triangular(t: np.ndarray, center: float, width: float, amp: float) -> np.ndarray:
    y = np.maximum(0.0, 1.0 - np.abs(t - center) / (width / 2.0))
    return amp * y


def fig_stdp_waveforms() -> None:
    delays = [-0.30, 0.05, 0.60]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.65), sharey=True)
    t = np.linspace(-1.0, 1.0, 600)
    for ax, delay, letter in zip(axes, delays, "abc"):
        pre = triangular(t, 0.0, 1.2, 1.55)
        post = -triangular(t, delay, 1.2, 1.55)
        total = pre + post
        ax.plot(t, pre, color=COLORS["green"], lw=0.9, label="pre-spike")
        ax.plot(t, post, color=COLORS["orange"], lw=0.9, label="post-spike")
        ax.plot(t, total, color="0.15", lw=1.3, label="sum")
        ax.axhline(0, color="0.65", lw=0.6)
        ax.axvline(0, color="0.75", lw=0.6, ls=":")
        figstyle.panel(ax, letter, rf"$\Delta t={delay:+.2f}$ s")
        ax.set_xlabel("time (s)")
        style_axes(ax)
    axes[0].set_ylabel("voltage (V)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=3, frameon=False, loc="lower center",
               bbox_to_anchor=(0.5, 0.965), fontsize=7.5)
    save(fig, "stdp_waveforms.pdf")


def fig_morphology_stability_support() -> None:
    """Two panels: (a) an annotated film cross-section conveying the
    profilometry thickness and the AFM surface roughness as an intuitive
    schematic (rather than single-value bars), and (b) the ambient
    shelf-stability drift of the device metrics within a +/-20% envelope."""
    from matplotlib.patches import Polygon

    fig, (axA, axB) = plt.subplots(
        1, 2, figsize=(7.2, 2.8), gridspec_kw={"width_ratios": [1.0, 1.12], "wspace": 0.28}
    )

    # ---- (a) film cross-section: thickness (profilometry) + roughness (AFM) ----
    axA.set_xlim(0, 10)
    axA.set_ylim(0, 10)
    axA.axis("off")

    x0, x1 = 2.4, 8.4
    y_sub_bot, y_sub_top = 1.6, 3.2          # substrate slab
    y_film_top = 7.4                          # mean top of the active film
    # substrate
    axA.add_patch(Rectangle((x0, y_sub_bot), x1 - x0, y_sub_top - y_sub_bot,
                            facecolor="#D9D9D9", edgecolor="0.3", lw=0.8))
    axA.text((x0 + x1) / 2, (y_sub_bot + y_sub_top) / 2, "ITO / glass substrate",
             ha="center", va="center", fontsize=7.5, color="0.2")
    # active film with a gently rough top edge (roughness exaggerated for legibility)
    xs = np.linspace(x0, x1, 240)
    rough = 0.16 * np.sin(2 * np.pi * xs / 0.85) + 0.10 * np.sin(2 * np.pi * xs / 0.37 + 1.0)
    top = y_film_top + rough
    verts = [(x0, y_sub_top)] + list(zip(xs, top)) + [(x1, y_sub_top)]
    axA.add_patch(Polygon(verts, closed=True, facecolor="#F0C75E",
                          edgecolor="0.3", lw=0.8, joinstyle="round"))
    axA.text((x0 + x1) / 2, (y_sub_top + y_film_top) / 2, "SY / Hybrane / LiOTf",
             ha="center", va="center", fontsize=7.5, color="0.15")

    # thickness dimension arrow (profilometry), with method tag as a parallel line
    axA.annotate("", xy=(x0 - 0.55, y_sub_top), xytext=(x0 - 0.55, y_film_top),
                 arrowprops=dict(arrowstyle="<->", color="0.25", lw=1.0))
    axA.text(x0 - 0.82, (y_sub_top + y_film_top) / 2, "209 nm", rotation=90,
             ha="center", va="center", fontsize=8.5, color="0.15")
    axA.text(x0 - 1.22, (y_sub_top + y_film_top) / 2, "(profilometry)", rotation=90,
             ha="center", va="center", fontsize=6.5, style="italic", color="0.45")

    # roughness callout pointing at the rough surface (tapping AFM)
    axA.annotate("RMS roughness\n1-3 nm (tapping AFM)",
                 xy=(x0 + 4.2, y_film_top + 0.2), xytext=(x1 - 0.2, 9.4),
                 ha="right", va="top", fontsize=7.5, color="0.15",
                 arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8,
                                 connectionstyle="arc3,rad=-0.2"))
    figstyle.panel(axA, "a", "film cross-section")

    # ---- (b) ambient shelf-stability drift within a +/-20% envelope ----
    hours = np.array([0.0, 300.0])
    axB.fill_between([0, 300], 0.8, 1.2, color="0.88", zorder=0)
    axB.text(296, 1.185, r"$\pm$20% envelope", ha="right", va="top",
             fontsize=7, color="0.45")
    axB.axhline(1.0, color="0.6", lw=0.7, ls=":")
    for label, color, yend, tag in [
        (r"$G_0$", COLORS["blue"], 1.08, "+8%"),
        (r"$\Delta G_{\mathrm{max}}$", COLORS["red"], 0.92, "$-$8%"),
        (r"$\tau_{\mathrm{s}}$", COLORS["purple"], 1.12, "+12%"),
    ]:
        axB.plot(hours, [1.0, yend], "o-", ms=4, lw=1.4, color=color, label=label)
        axB.annotate(tag, xy=(300, yend), xytext=(6, 0), textcoords="offset points",
                     va="center", fontsize=7, color=color)
    axB.set_xlim(-12, 360)
    axB.set_ylim(0.74, 1.26)
    axB.set_xlabel("ambient storage (h)")
    axB.set_ylabel("normalised metric")
    axB.legend(loc="lower left", ncol=3, columnspacing=1.0, handlelength=1.2)
    figstyle.panel(axB, "b", "ambient shelf stability")
    style_axes(axB)

    save(fig, "morphology_stability_support.pdf")


def main() -> None:
    fig_composite_chemistry()
    fig_device_schematic()
    fig_iv_hyst()
    fig_potentiation_depression()
    fig_pulse_number()
    fig_retention()
    fig_epsc_summary()
    fig_stdp_summary()
    fig_read_write_wait_protocol()
    fig_full_epsc_trace()
    fig_stdp_waveforms()
    fig_morphology_stability_support()


if __name__ == "__main__":
    main()
