"""Shared chart theme and colour palette for the BC Crime analysis.

Thin wrapper around the kds shared module. BC-specific colour semantics
are preserved; theming, axes styling, and figure export delegate to kds.
"""

import sys
from pathlib import Path
import textwrap

import matplotlib.pyplot as plt

# Make the kds package importable from the project root's sibling directory
_KDS_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_KDS_ROOT) not in sys.path:
    sys.path.insert(0, str(_KDS_ROOT))

import kds.theme as _kds_theme  # noqa: E402
from kds.theme import (  # noqa: E402
    FIGSIZE_DOUBLE,
    FIGSIZE_SINGLE,
    FIGSIZE_SMALL,
    FIGSIZE_WIDE,
    smart_annotate as _kds_smart_annotate,
)

# ---------------------------------------------------------------------------
# BC-specific colour palette
# ---------------------------------------------------------------------------
PALETTE = {
    "bc_blue": "#1b4f72",
    "bc_red": "#c0392b",
    "bc_teal": _kds_theme.PALETTE.teal,
    "bc_amber": _kds_theme.PALETTE.amber,
    "bc_slate": _kds_theme.PALETTE.slate,
    "bc_orange": "#e67e22",
    "bc_purple": "#7d3c98",
    "light_grey": "#d5d8dc",
    "canada_grey": "#808b96",
}

ORDERED = [
    PALETTE["bc_blue"],
    PALETTE["bc_red"],
    PALETTE["bc_teal"],
    PALETTE["bc_amber"],
    PALETTE["bc_slate"],
    PALETTE["bc_orange"],
    PALETTE["bc_purple"],
]

PROVINCE_COLOURS = {
    "British Columbia": PALETTE["bc_blue"],
    "Canada": PALETTE["canada_grey"],
    "Alberta": PALETTE["bc_amber"],
    "Ontario": PALETTE["bc_teal"],
    "Saskatchewan": PALETTE["bc_orange"],
    "Manitoba": PALETTE["bc_purple"],
}


# ---------------------------------------------------------------------------
# Theme delegates
# ---------------------------------------------------------------------------

def apply_theme() -> None:
    """Apply the kds standard theme (300 DPI, whitegrid, JetBrains Mono)."""
    _kds_theme.apply_theme(font="JetBrains Mono")


def style_axes(ax: plt.Axes) -> None:
    """Apply standard spine/grid treatment via kds."""
    _kds_theme.style_axes(ax)


def save_fig(fig: plt.Figure, path: str) -> None:
    """Save figure via kds (300 DPI, tight layout) then close."""
    _kds_theme.save_fig(fig, path, show=False)
    plt.close(fig)


def add_source(fig: plt.Figure, text: str, fontsize: int = 8) -> None:
    """Add a source annotation below the figure."""
    fig.text(
        0.01, -0.02, text,
        fontsize=fontsize, color=PALETTE["bc_slate"],
        ha="left", va="top", style="italic",
    )


def add_subtitle(ax: plt.Axes, text: str, fontsize: int = 10) -> None:
    """Add an interpretive subtitle below the title."""
    ax.text(
        0, 1.06, text,
        transform=ax.transAxes,
        fontsize=fontsize,
        color=PALETTE["bc_slate"],
        style="italic",
        va="bottom",
    )


KEY_EVENTS = {
    2015: "Opioid crisis begins",
    2018: "Cannabis legalized",
    2020: "COVID-19 pandemic",
}


def add_fig_subtitle(fig: plt.Figure, text: str, fontsize: int = 10) -> None:
    """Add a figure-level subtitle for small multiples (below fig.suptitle)."""
    fig.text(
        0.5, 0.96, text,
        ha="center",
        fontsize=fontsize,
        color=PALETTE["bc_slate"],
        style="italic",
    )


def annotate_events(
    ax: plt.Axes,
    events: dict[int, str] | None = None,
    ypos: float = 0.85,
) -> None:
    """Add vertical dashed lines and labels for key events on temporal charts."""
    items = list((events or KEY_EVENTS).items())
    for idx, (yr, label) in enumerate(items):
        ax.axvline(yr, color=PALETTE["light_grey"], linewidth=0.8, linestyle="--", zorder=0)
        # Stagger alternating labels to prevent overlap
        stagger = 0.0 if idx % 2 == 0 else -0.10
        ax.text(
            yr, ax.get_ylim()[1] * (ypos + stagger), f" {label}",
            fontsize=7, color=PALETTE["bc_slate"],
            rotation=90, va="top",
            bbox={"boxstyle": "round,pad=0.15", "facecolor": "white", "alpha": 0.85, "edgecolor": "none"},
        )


def smart_annotate(
    ax: plt.Axes,
    texts: list[str],
    x,
    y,
    fontsize: int = 8,
    color: str | None = None,
    max_labels: int = 30,
    **kwargs,
) -> list:
    """Auto-position scatter/strip labels to avoid overlaps with dotted leader lines.

    Thin wrapper around kds.theme.smart_annotate using the BC palette default.
    """
    return _kds_theme.smart_annotate(
        ax, texts, x, y,
        fontsize=fontsize,
        color=color or PALETTE["bc_slate"],
        max_labels=max_labels,
        **kwargs,
    )


def wrap_bar_labels(labels: list[str], max_width: int = 20) -> list[str]:
    """Wrap long jurisdiction/category names for horizontal bar y-tick labels.

    Parameters
    ----------
    labels : list[str]
        The original label strings.
    max_width : int
        Maximum characters per line before wrapping.

    Returns
    -------
    list[str]
        Labels with newlines inserted at word boundaries.
    """
    return [textwrap.fill(str(lbl), width=max_width) for lbl in labels]


def smart_bar_value_labels(
    ax: plt.Axes,
    bars,
    values,
    fontsize: int = 8,
    min_gap_px: int = 12,
    fmt: str = "",
) -> None:
    """Add value labels to horizontal bars, staggering or omitting on overlap.

    Checks if consecutive value labels would overlap in pixel space
    (y-positions closer than min_gap_px) and staggers them by adding
    horizontal offset, or omits labels that still collide.

    Parameters
    ----------
    ax : plt.Axes
        The axes containing the bars.
    bars : BarContainer
        The bar patches from ax.barh().
    values : array-like
        The numeric values to display as labels.
    fontsize : int
        Font size for labels.
    min_gap_px : int
        Minimum vertical pixel gap between consecutive labels.
    fmt : str
        Format string for values (e.g., '+.1f' for signed floats).
        If empty, auto-detects: uses comma-separated integers for
        values > 100, one decimal otherwise.
    """
    fig = ax.get_figure()
    fig.canvas.draw()
    transform = ax.transData

    label_positions = []
    for bar, val in zip(bars, values):
        cx = bar.get_width()
        cy = bar.get_y() + bar.get_height() / 2
        _, py = transform.transform((cx, cy))
        label_positions.append((cx, cy, py, val))

    label_positions.sort(key=lambda t: t[2])

    last_py = -999
    for cx, cy, py, val in label_positions:
        if py - last_py < min_gap_px:
            continue
        if fmt:
            text = f"{val:{fmt}}"
        elif abs(val) >= 100:
            text = f"{val:,.0f}"
        else:
            text = f"{val:.1f}"
        offset = 2 if cx >= 0 else -2
        ha = "left" if cx >= 0 else "right"
        ax.text(cx + offset, cy, text, ha=ha, va="center", fontsize=fontsize)
        last_py = py
