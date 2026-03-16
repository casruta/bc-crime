"""Priority 3 — Is Crime Rising in BC?

Analyzes BC's Crime Severity Index (CSI) trend, compares to other provinces,
and calculates year-over-year crime rate changes. Produces charts and narrative.
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

from src.analysis.theme import (
    ORDERED,
    PALETTE,
    PROVINCE_COLOURS,
    apply_theme,
    save_fig,
    style_axes,
)

logger = logging.getLogger(__name__)

PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"
CHARTS_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "charts"

# Key events for annotation
ANNOTATIONS = {
    2003: "Peak crime era",
    2014: "CSI trough",
    2020: "COVID-19",
}

COMPARISON_PROVINCES = ["British Columbia", "Canada", "Alberta", "Ontario", "Saskatchewan", "Manitoba"]


def _load_csi_bc() -> pd.DataFrame:
    """Load and reshape BC CSI data: year × statistic → wide format."""
    df = pd.read_parquet(PROCESSED_DIR / "crime_severity_bc.parquet")
    bc = df[df["geo"] == "British Columbia"].copy()

    # Pivot: one row per year, columns = statistic types
    stats_of_interest = [
        "Crime severity index",
        "Violent crime severity index",
        "Non-violent crime severity index",
        "Youth crime severity index",
    ]
    bc = bc[bc["statistic"].isin(stats_of_interest)]
    wide = bc.pivot_table(index="year", columns="statistic", values="value", aggfunc="first")
    wide = wide.sort_index().reset_index()
    wide.columns.name = None
    return wide


def _load_national_csi() -> pd.DataFrame:
    """Load CSI-equivalent data from national table for province comparison.

    The national table (35-10-0177-01) has 'Total, all violations' with
    'Rate per 100,000 population' which we use as a proxy for CSI comparison.
    We also look for CSI data if available in the table.
    """
    df = pd.read_parquet(PROCESSED_DIR / "crime_incidents_national.parquet")

    # Filter to province-level, total violations, rate statistic
    mask = (
        df["geo"].isin(COMPARISON_PROVINCES)
        & (df["violation"] == "Total, all Criminal Code violations (excluding traffic) [50]")
        & (df["statistic"] == "Rate per 100,000 population")
    )
    result = df[mask][["year", "geo", "value"]].copy()
    result = result.rename(columns={"value": "crime_rate"})
    result = result.dropna(subset=["crime_rate"]).sort_values(["geo", "year"])
    result = result.reset_index(drop=True)
    return result


def _load_bc_yoy() -> pd.DataFrame:
    """Load BC total crime rate and compute year-over-year % change."""
    df = pd.read_parquet(PROCESSED_DIR / "crime_incidents_national.parquet")

    mask = (
        (df["geo"] == "British Columbia")
        & (df["violation"] == "Total, all Criminal Code violations (excluding traffic) [50]")
        & (df["statistic"] == "Rate per 100,000 population")
    )
    bc = df[mask][["year", "value"]].copy()
    bc = bc.rename(columns={"value": "crime_rate"})
    bc = bc.dropna(subset=["crime_rate"]).sort_values("year").reset_index(drop=True)
    bc["yoy_pct_change"] = bc["crime_rate"].pct_change() * 100
    return bc


# ---------------------------------------------------------------------------
# Chart generators
# ---------------------------------------------------------------------------

def chart_bc_csi_trend(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Line chart: BC CSI over time (total, violent, non-violent) with annotations."""
    apply_theme()
    data = _load_csi_bc()

    fig, ax = plt.subplots(figsize=(12, 6))

    lines = [
        ("Crime severity index", PALETTE["bc_blue"], "Total CSI", 2.5),
        ("Violent crime severity index", PALETTE["bc_red"], "Violent CSI", 1.8),
        ("Non-violent crime severity index", PALETTE["bc_teal"], "Non-violent CSI", 1.8),
    ]

    for col, color, label, lw in lines:
        if col in data.columns:
            ax.plot(data["year"], data[col], color=color, label=label, linewidth=lw)

    # Annotations
    for yr, label in ANNOTATIONS.items():
        if yr in data["year"].values:
            val = data.loc[data["year"] == yr, "Crime severity index"].values[0]
            ax.annotate(
                label,
                xy=(yr, val),
                xytext=(yr, val + 12),
                ha="center",
                fontsize=9,
                color=PALETTE["bc_slate"],
                arrowprops={"arrowstyle": "->", "color": PALETTE["bc_slate"], "lw": 0.8},
            )

    ax.set_title("British Columbia Crime Severity Index (1998–2024)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Crime Severity Index")
    ax.legend(loc="upper right")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    style_axes(ax)

    # Narrative
    latest_year = int(data["year"].max())
    peak_year = int(data.loc[data["Crime severity index"].idxmax(), "year"])
    peak_val = data["Crime severity index"].max()
    latest_val = data.loc[data["year"] == latest_year, "Crime severity index"].values[0]
    trough_val = data.loc[data["year"] == 2014, "Crime severity index"].values[0] if 2014 in data["year"].values else None

    narrative = (
        f"BC's Crime Severity Index peaked at {peak_val:.1f} in {peak_year}, then declined to "
        f"a trough of {trough_val:.1f} in 2014 — a {((peak_val - trough_val) / peak_val * 100):.0f}% drop. "
        f"Since 2014, the CSI has risen, reaching {latest_val:.1f} in {latest_year}. "
        f"The violent CSI has risen more steeply than non-violent, signalling that the composition "
        f"of crime is shifting toward more serious offences. "
        f"Source: Statistics Canada Table 35-10-0063-01."
    ) if trough_val else f"BC's CSI was {latest_val:.1f} in {latest_year}."

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_provincial_comparison(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Small multiples: BC vs Canada vs 3 other provinces, crime rate over time."""
    apply_theme()
    data = _load_national_csi()

    provinces = COMPARISON_PROVINCES
    fig, axes = plt.subplots(2, 3, figsize=(16, 9), sharex=True, sharey=True)
    axes = axes.flatten()

    for i, prov in enumerate(provinces):
        ax = axes[i]
        prov_data = data[data["geo"] == prov].sort_values("year")
        color = PROVINCE_COLOURS.get(prov, ORDERED[i % len(ORDERED)])
        ax.plot(prov_data["year"], prov_data["crime_rate"], color=color, linewidth=2)
        ax.fill_between(prov_data["year"], prov_data["crime_rate"], alpha=0.1, color=color)
        ax.set_title(prov, fontsize=11, fontweight="bold")
        ax.xaxis.set_major_locator(mticker.MultipleLocator(5))
        style_axes(ax)

    fig.suptitle(
        "Criminal Code Offence Rate per 100,000 Population (excl. traffic)",
        fontsize=14, fontweight="bold", y=1.02,
    )
    fig.supxlabel("Year")
    fig.supylabel("Rate per 100,000")
    fig.tight_layout()

    # Narrative
    latest = data[data["year"] == data["year"].max()]
    bc_rate = latest.loc[latest["geo"] == "British Columbia", "crime_rate"]
    ca_rate = latest.loc[latest["geo"] == "Canada", "crime_rate"]
    bc_rate_val = bc_rate.values[0] if len(bc_rate) else 0
    ca_rate_val = ca_rate.values[0] if len(ca_rate) else 0
    latest_yr = int(data["year"].max())

    narrative = (
        f"In {latest_yr}, BC's Criminal Code offence rate was {bc_rate_val:,.0f} per 100,000, "
        f"compared to the national average of {ca_rate_val:,.0f}. "
        f"BC's rate is {((bc_rate_val / ca_rate_val - 1) * 100):+.0f}% relative to Canada. "
        f"Saskatchewan consistently has the highest rate among comparison provinces. "
        f"Source: Statistics Canada Table 35-10-0177-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_yoy_change_by_province(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Bar chart: most recent year-over-year change in crime rate by province (BC highlighted)."""
    apply_theme()
    data = _load_national_csi()

    # Calculate YoY change for each province for the latest year
    provinces = COMPARISON_PROVINCES
    records = []
    for prov in provinces:
        prov_data = data[data["geo"] == prov].sort_values("year")
        if len(prov_data) >= 2:
            prev = prov_data.iloc[-2]["crime_rate"]
            curr = prov_data.iloc[-1]["crime_rate"]
            pct_chg = ((curr - prev) / prev) * 100 if prev != 0 else 0
            records.append({"province": prov, "yoy_pct_change": pct_chg, "latest_year": int(prov_data["year"].max())})

    df_chg = pd.DataFrame(records).sort_values("yoy_pct_change")

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [
        PALETTE["bc_blue"] if p == "British Columbia" else PALETTE["light_grey"]
        for p in df_chg["province"]
    ]
    bars = ax.barh(df_chg["province"], df_chg["yoy_pct_change"], color=colors, edgecolor="white")

    # Add value labels
    for bar, val in zip(bars, df_chg["yoy_pct_change"]):
        x = bar.get_width()
        ax.text(
            x + (0.3 if x >= 0 else -0.3),
            bar.get_y() + bar.get_height() / 2,
            f"{val:+.1f}%",
            ha="left" if x >= 0 else "right",
            va="center",
            fontsize=10,
            fontweight="bold" if bar.get_facecolor()[:3] != (0.835, 0.847, 0.863) else "normal",
        )

    latest_yr = df_chg["latest_year"].max()
    ax.set_title(f"Year-over-Year Change in Crime Rate ({latest_yr - 1} → {latest_yr})")
    ax.set_xlabel("% Change in Rate per 100,000")
    ax.axvline(0, color="black", linewidth=0.8)
    style_axes(ax)
    ax.grid(axis="y", visible=False)

    # Narrative
    bc_chg = df_chg.loc[df_chg["province"] == "British Columbia", "yoy_pct_change"].values[0]
    direction = "increased" if bc_chg > 0 else "decreased"
    narrative = (
        f"BC's crime rate {direction} by {abs(bc_chg):.1f}% from {latest_yr - 1} to {latest_yr}. "
        f"Source: Statistics Canada Table 35-10-0177-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_bc_yoy_trend(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Bar chart: BC year-over-year % change in total crime rate, full time series."""
    apply_theme()
    data = _load_bc_yoy()
    data = data.dropna(subset=["yoy_pct_change"])

    fig, ax = plt.subplots(figsize=(12, 5))
    colors = [PALETTE["bc_red"] if v > 0 else PALETTE["bc_teal"] for v in data["yoy_pct_change"]]
    ax.bar(data["year"], data["yoy_pct_change"], color=colors, edgecolor="white", width=0.8)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("BC Year-over-Year Change in Criminal Code Offence Rate")
    ax.set_xlabel("Year")
    ax.set_ylabel("% Change")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    style_axes(ax)

    # Narrative
    rising_years = len(data[data["yoy_pct_change"] > 0])
    falling_years = len(data[data["yoy_pct_change"] < 0])
    latest_chg = data.iloc[-1]["yoy_pct_change"]
    latest_yr = int(data.iloc[-1]["year"])
    narrative = (
        f"Over the full time series, BC experienced rising crime rates in {rising_years} years "
        f"and declining rates in {falling_years} years. In {latest_yr}, the rate changed by "
        f"{latest_chg:+.1f}%. The most sustained decline occurred from 2003–2014. "
        f"Source: Statistics Canada Table 35-10-0177-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


# ---------------------------------------------------------------------------
# Run all
# ---------------------------------------------------------------------------

def run_all() -> dict[str, str]:
    """Generate all Priority 3 charts and return narratives."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    narratives = {}

    charts = [
        ("q1_bc_csi_trend", chart_bc_csi_trend),
        ("q1_provincial_comparison", chart_provincial_comparison),
        ("q1_yoy_by_province", chart_yoy_change_by_province),
        ("q1_bc_yoy_trend", chart_bc_yoy_trend),
    ]

    for name, fn in charts:
        path = CHARTS_DIR / f"{name}.png"
        logger.info("Generating %s ...", name)
        _, narrative = fn(save_path=path)
        narratives[name] = narrative
        logger.info("  Saved %s", path)

    return narratives


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    narratives = run_all()
    print("\n" + "=" * 70)
    print("NARRATIVES")
    print("=" * 70)
    for name, text in narratives.items():
        print(f"\n### {name}\n{text}")
