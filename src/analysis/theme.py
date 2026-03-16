"""Shared chart theme and colour palette for the BC Crime analysis."""

import matplotlib.pyplot as plt
import matplotlib as mpl

# Colour palette — accessible, consistent across all charts
PALETTE = {
    "bc_blue": "#1b4f72",
    "bc_red": "#c0392b",
    "bc_teal": "#148f77",
    "bc_amber": "#d4ac0d",
    "bc_slate": "#5d6d7e",
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

# Province colour assignments — consistent across all charts
PROVINCE_COLOURS = {
    "British Columbia": PALETTE["bc_blue"],
    "Canada": PALETTE["canada_grey"],
    "Alberta": PALETTE["bc_amber"],
    "Ontario": PALETTE["bc_teal"],
    "Saskatchewan": PALETTE["bc_orange"],
    "Manitoba": PALETTE["bc_purple"],
}


def apply_theme() -> None:
    """Apply the project-wide matplotlib style."""
    mpl.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.grid": True,
        "axes.grid.which": "major",
        "grid.alpha": 0.3,
        "grid.color": "#cccccc",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "legend.frameon": False,
        "figure.dpi": 150,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "font.family": "sans-serif",
    })


def style_axes(ax: plt.Axes) -> None:
    """Standard axes cleanup: remove top/right spines, light grid."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3)


def save_fig(fig: plt.Figure, path: str) -> None:
    """Save figure with tight layout and standard DPI."""
    fig.savefig(path, bbox_inches="tight", dpi=200, facecolor="white")
    plt.close(fig)
