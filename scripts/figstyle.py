"""Shared figure house style for the thesis figure scripts (Chapters 2/4/5).

The goal is a single, consistent, journal-style look across every generated
figure: a sans-serif (Helvetica) text face with matching sans-serif maths
(STIX Sans), de-spined axes, frameless legends, and a uniform palette.

Usage (call once, right after importing matplotlib in each script):

    import figstyle
    figstyle.apply()

Helpers
-------
COLORS                       categorical palette (ColorBrewer Dark2 derived)
apply()                      install the rcParams house style
panel(ax, "a", "title")      Nature-style bold lower-case panel label, with an
                             optional centred descriptive title
despine(ax)                  hide top/right spines (also done globally; this is
                             for axes that need it re-applied, e.g. twins)
box(ax)                      restore all four spines (heatmaps / imshow panels)
keepspine(ax2, "right")      re-show one spine (secondary / twin axes)
save(fig, path)              savefig + close with a status print
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Categorical palette shared by every chapter. Derived from ColorBrewer Dark2
# (green/orange) with a balanced blue/red/purple and neutral grays so that
# line, bar and scatter colours stay consistent across figures.
COLORS = {
    "blue": "#276FBF",
    "green": "#1B9E77",
    "orange": "#D95F02",
    "red": "#C43C39",
    "purple": "#6A4C93",
    "gray": "#4D4D4D",
    "light": "#F4F4F4",
}


def apply() -> None:
    """Install the unified sans-serif house style into ``plt.rcParams``."""
    plt.rcParams.update(
        {
            # --- typography: Helvetica text + matching sans-serif maths -----
            "font.family": "sans-serif",
            "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
            "mathtext.fontset": "stixsans",
            "axes.unicode_minus": True,
            "font.size": 8.5,
            "axes.titlesize": 9,
            "axes.titleweight": "normal",
            "axes.labelsize": 8.5,
            "legend.fontsize": 7.5,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            # --- spines / ticks: clean, de-spined, outward ticks -----------
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.axisbelow": True,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "xtick.major.size": 3.0,
            "ytick.major.size": 3.0,
            # --- legends: frameless ----------------------------------------
            "legend.frameon": False,
            "legend.handlelength": 1.6,
            "legend.handletextpad": 0.5,
            "legend.labelspacing": 0.35,
            "legend.columnspacing": 1.2,
            # --- lines / markers -------------------------------------------
            "lines.linewidth": 1.6,
            "lines.markersize": 4.0,
            # --- output: vector PDF with embedded TrueType fonts -----------
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def panel(ax, letter: str, title: str | None = None) -> None:
    """Nature-style bold lower-case panel label at the top-left.

    Uses matplotlib's left/centre dual-title slots so the bold letter never
    overlaps the data or the (optional) centred descriptive title.
    """
    ax.set_title(letter, loc="left", fontweight="bold", fontsize=10)
    if title is not None:
        ax.set_title(title, loc="center")


def despine(ax, top: bool = True, right: bool = True,
            left: bool = False, bottom: bool = False) -> None:
    """Hide the requested spines and set outward ticks on ``ax``."""
    if top:
        ax.spines["top"].set_visible(False)
    if right:
        ax.spines["right"].set_visible(False)
    if left:
        ax.spines["left"].set_visible(False)
    if bottom:
        ax.spines["bottom"].set_visible(False)
    ax.tick_params(direction="out", length=3, width=0.8)


def box(ax) -> None:
    """Restore all four spines -- for heatmaps / imshow panels that need a box."""
    for spine in ax.spines.values():
        spine.set_visible(True)


def keepspine(ax, *which: str) -> None:
    """Re-show specific spines (e.g. the right spine of a twin/secondary axis)."""
    for w in which:
        ax.spines[w].set_visible(True)


def save(fig, path) -> None:
    """Write ``fig`` to ``path`` (creating parents) and close it."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    print(f"wrote {path}")
