"""Priority 7 -- Why Does Crime Feel Like It's Rising? Perception vs. Reality.

Explores the gap between public perception of crime trends and actual
crime statistics. Uses GSS victimization survey data, CSI actuals,
and Justice Canada citations.

Data sources:
    - 35-10-0066-01  Perception of crime in neighbourhood (GSS)
    - 35-10-0068-01  Confidence in police (GSS)
    - Crime severity BC parquet (CSI actuals)
    - Cotter (2021), GSS on Canadians' Safety, Juristat
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

from src.analysis.theme import (
    FIGSIZE_DOUBLE,
    FIGSIZE_SINGLE,
    FIGSIZE_SMALL,
    ORDERED,
    PALETTE,
    add_fig_subtitle,
    add_source,
    add_subtitle,
    apply_theme,
    save_fig,
    style_axes,
)

from src.paths import CHARTS_DIR, PROCESSED_DIR

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Fallback data from real sources
# ---------------------------------------------------------------------------

# GSS Victimization Survey, 2014 and 2019 (StatCan catalogue 85-002-X)
# "Perception of crime in neighbourhood compared to 5 years ago"
FALLBACK_PERCEPTION = pd.DataFrame([
    {"year": 2009, "geo": "British Columbia", "response": "Increased", "value": 38.0},
    {"year": 2009, "geo": "British Columbia", "response": "About the same", "value": 43.0},
    {"year": 2009, "geo": "British Columbia", "response": "Decreased", "value": 13.0},
    {"year": 2009, "geo": "Canada", "response": "Increased", "value": 33.0},
    {"year": 2009, "geo": "Canada", "response": "About the same", "value": 48.0},
    {"year": 2009, "geo": "Canada", "response": "Decreased", "value": 14.0},
    {"year": 2014, "geo": "British Columbia", "response": "Increased", "value": 30.0},
    {"year": 2014, "geo": "British Columbia", "response": "About the same", "value": 48.0},
    {"year": 2014, "geo": "British Columbia", "response": "Decreased", "value": 17.0},
    {"year": 2014, "geo": "Canada", "response": "Increased", "value": 27.0},
    {"year": 2014, "geo": "Canada", "response": "About the same", "value": 52.0},
    {"year": 2014, "geo": "Canada", "response": "Decreased", "value": 16.0},
    {"year": 2019, "geo": "British Columbia", "response": "Increased", "value": 42.0},
    {"year": 2019, "geo": "British Columbia", "response": "About the same", "value": 41.0},
    {"year": 2019, "geo": "British Columbia", "response": "Decreased", "value": 10.0},
    {"year": 2019, "geo": "Canada", "response": "Increased", "value": 39.0},
    {"year": 2019, "geo": "Canada", "response": "About the same", "value": 44.0},
    {"year": 2019, "geo": "Canada", "response": "Decreased", "value": 12.0},
])

# GSS confidence in police (StatCan catalogue 85-002-X)
FALLBACK_CONFIDENCE = pd.DataFrame([
    {"year": 2019, "geo": "British Columbia", "confidence_level": "Great deal of confidence", "value": 30.0},
    {"year": 2019, "geo": "British Columbia", "confidence_level": "Some confidence", "value": 47.0},
    {"year": 2019, "geo": "British Columbia", "confidence_level": "Not very much confidence", "value": 17.0},
    {"year": 2019, "geo": "British Columbia", "confidence_level": "No confidence at all", "value": 5.0},
    {"year": 2019, "geo": "Canada", "confidence_level": "Great deal of confidence", "value": 32.0},
    {"year": 2019, "geo": "Canada", "confidence_level": "Some confidence", "value": 46.0},
    {"year": 2019, "geo": "Canada", "confidence_level": "Not very much confidence", "value": 15.0},
    {"year": 2019, "geo": "Canada", "confidence_level": "No confidence at all", "value": 5.0},
    {"year": 2019, "geo": "Alberta", "confidence_level": "Great deal of confidence", "value": 34.0},
    {"year": 2019, "geo": "Alberta", "confidence_level": "Some confidence", "value": 44.0},
    {"year": 2019, "geo": "Alberta", "confidence_level": "Not very much confidence", "value": 16.0},
    {"year": 2019, "geo": "Alberta", "confidence_level": "No confidence at all", "value": 5.0},
    {"year": 2019, "geo": "Ontario", "confidence_level": "Great deal of confidence", "value": 33.0},
    {"year": 2019, "geo": "Ontario", "confidence_level": "Some confidence", "value": 47.0},
    {"year": 2019, "geo": "Ontario", "confidence_level": "Not very much confidence", "value": 14.0},
    {"year": 2019, "geo": "Ontario", "confidence_level": "No confidence at all", "value": 4.0},
    {"year": 2019, "geo": "Saskatchewan", "confidence_level": "Great deal of confidence", "value": 35.0},
    {"year": 2019, "geo": "Saskatchewan", "confidence_level": "Some confidence", "value": 43.0},
    {"year": 2019, "geo": "Saskatchewan", "confidence_level": "Not very much confidence", "value": 16.0},
    {"year": 2019, "geo": "Saskatchewan", "confidence_level": "No confidence at all", "value": 5.0},
    {"year": 2019, "geo": "Manitoba", "confidence_level": "Great deal of confidence", "value": 29.0},
    {"year": 2019, "geo": "Manitoba", "confidence_level": "Some confidence", "value": 45.0},
    {"year": 2019, "geo": "Manitoba", "confidence_level": "Not very much confidence", "value": 19.0},
    {"year": 2019, "geo": "Manitoba", "confidence_level": "No confidence at all", "value": 6.0},
])

# Reporting rates by crime type (GSS 2019, Cotter 2021, Juristat)
REPORTING_RATES = pd.DataFrame([
    {"crime_type": "Total criminal victimization", "reporting_rate": 29.0},
    {"crime_type": "Theft of personal property", "reporting_rate": 35.0},
    {"crime_type": "Break and enter", "reporting_rate": 54.0},
    {"crime_type": "Motor vehicle theft", "reporting_rate": 60.0},
    {"crime_type": "Assault", "reporting_rate": 31.0},
    {"crime_type": "Robbery", "reporting_rate": 43.0},
    {"crime_type": "Sexual assault", "reporting_rate": 6.0},
    {"crime_type": "Vandalism", "reporting_rate": 32.0},
])

# Colour thresholds for reporting rate bars
REPORTING_RATE_LOW = 20.0
REPORTING_RATE_MID = 50.0


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def _load_gss_perception() -> pd.DataFrame | None:
    """Load GSS perception data if available."""
    path = PROCESSED_DIR / "gss_perception.parquet"
    if not path.exists():
        logger.warning("GSS perception data not found: %s -- using fallback data", path)
        return None
    return pd.read_parquet(path)


def _load_gss_confidence() -> pd.DataFrame | None:
    """Load GSS confidence data if available."""
    path = PROCESSED_DIR / "gss_confidence.parquet"
    if not path.exists():
        logger.warning("GSS confidence data not found: %s -- using fallback data", path)
        return None
    return pd.read_parquet(path)


def _load_csi_bc() -> pd.DataFrame:
    """Load BC CSI for overlay."""
    df = pd.read_parquet(PROCESSED_DIR / "crime_severity_bc.parquet")
    bc = df[
        (df["geo"] == "British Columbia")
        & (df["statistic"] == "Crime severity index")
    ][["year", "value"]].copy()
    bc = bc.rename(columns={"value": "csi"})
    return bc.dropna(subset=["csi"]).sort_values("year").reset_index(drop=True)


def _get_perception_data() -> tuple[pd.DataFrame, bool]:
    """Return GSS perception data and whether fallback was used."""
    loaded = _load_gss_perception()
    if loaded is not None:
        return loaded, False
    logger.warning("Using hardcoded fallback GSS data — parquet files not found")
    return FALLBACK_PERCEPTION.copy(), True


def _get_confidence_data() -> tuple[pd.DataFrame, bool]:
    """Return GSS confidence data and whether fallback was used."""
    loaded = _load_gss_confidence()
    if loaded is not None:
        return loaded, False
    logger.warning("Using hardcoded fallback GSS data — parquet files not found")
    return FALLBACK_CONFIDENCE.copy(), True


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------

def chart_perception_vs_reality(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Dual-panel: grouped bar (GSS 'crime increased' %) + line (actual CSI).

    Top panel shows the percentage of respondents who believe crime has
    increased in their neighbourhood, for BC and Canada across GSS cycles.
    Bottom panel overlays the actual BC Crime Severity Index over the same
    period, revealing the gap between perception and reality.
    """
    apply_theme()
    perception, _perception_fallback = _get_perception_data()
    csi = _load_csi_bc()

    # Filter perception to "Increased" responses only
    increased = perception[perception["response"] == "Increased"].copy()
    gss_years = sorted(increased["year"].unique())

    fig, (ax_top, ax_bot) = plt.subplots(
        2, 1, figsize=FIGSIZE_DOUBLE, gridspec_kw={"height_ratios": [1.2, 1]},
    )

    # --- Top panel: grouped bar chart ---
    bar_width = 0.35
    x_positions = np.arange(len(gss_years))

    bc_vals = []
    ca_vals = []
    for yr in gss_years:
        bc_row = increased[(increased["year"] == yr) & (increased["geo"] == "British Columbia")]
        ca_row = increased[(increased["year"] == yr) & (increased["geo"] == "Canada")]
        bc_vals.append(bc_row["value"].values[0] if len(bc_row) else 0)
        ca_vals.append(ca_row["value"].values[0] if len(ca_row) else 0)

    bars_bc = ax_top.bar(
        x_positions - bar_width / 2, bc_vals, bar_width,
        color=PALETTE["bc_blue"], label="British Columbia", edgecolor="white",
    )
    bars_ca = ax_top.bar(
        x_positions + bar_width / 2, ca_vals, bar_width,
        color=PALETTE["canada_grey"], label="Canada", edgecolor="white",
    )

    # Value labels on bars
    for bars in (bars_bc, bars_ca):
        for bar in bars:
            height = bar.get_height()
            ax_top.text(
                bar.get_x() + bar.get_width() / 2, height + 0.8,
                f"{height:.0f}%", ha="center", va="bottom", fontsize=9, fontweight="bold",
            )

    ax_top.set_xticks(x_positions)
    ax_top.set_xticklabels([str(yr) for yr in gss_years])
    ax_top.set_ylabel('% Who Say Crime "Increased"')
    ax_top.set_title("Public Perception: Crime Is Increasing in My Neighbourhood")
    ax_top.legend(loc="upper left", fontsize=9)
    ax_top.set_ylim(0, max(max(bc_vals), max(ca_vals)) * 1.25)
    style_axes(ax_top)

    # --- Bottom panel: actual CSI line ---
    # Filter CSI to the range spanning the GSS years
    min_gss = min(gss_years)
    max_gss = max(gss_years)
    csi_range = csi[(csi["year"] >= min_gss - 2) & (csi["year"] <= max_gss + 2)]

    ax_bot.plot(
        csi_range["year"], csi_range["csi"],
        color=PALETTE["bc_blue"], linewidth=2.5, marker="o", markersize=4,
    )
    ax_bot.fill_between(csi_range["year"], csi_range["csi"], alpha=0.1, color=PALETTE["bc_blue"])

    # Highlight GSS survey years on the CSI line
    for yr in gss_years:
        csi_yr = csi_range[csi_range["year"] == yr]
        if not csi_yr.empty:
            val = csi_yr["csi"].values[0]
            ax_bot.plot(yr, val, "o", color=PALETTE["bc_red"], markersize=8, zorder=5)
            ax_bot.annotate(
                f"CSI: {val:.0f}",
                xy=(yr, val), xytext=(yr, val + 6),
                ha="center", fontsize=9, color=PALETTE["bc_red"],
                arrowprops={"arrowstyle": "->", "color": PALETTE["bc_red"], "lw": 0.8},
            )

    ax_bot.set_ylabel("Crime Severity Index")
    ax_bot.set_xlabel("Year")
    ax_bot.set_title("Reality: BC Crime Severity Index (Actual Trend)")
    ax_bot.xaxis.set_major_locator(mticker.MultipleLocator(2))
    style_axes(ax_bot)

    fig.suptitle(
        "Perception vs. Reality: Is Crime Actually Rising?",
        fontsize=14, fontweight="bold", y=1.02,
    )

    # Compute the peak CSI for narrative
    csi_peak = csi["csi"].max()
    csi_peak_year = int(csi.loc[csi["csi"].idxmax(), "year"])
    latest_bc_pct = bc_vals[-1]
    latest_gss_year = gss_years[-1]
    csi_at_latest = csi[csi["year"] == latest_gss_year]
    csi_latest_val = csi_at_latest["csi"].values[0] if not csi_at_latest.empty else None

    if csi_latest_val is not None:
        decline_pct = ((csi_peak - csi_latest_val) / csi_peak) * 100 if csi_peak != 0 else 0.0
        add_fig_subtitle(
            fig,
            f"{latest_bc_pct:.0f}% of BC residents said crime increased in {latest_gss_year}, "
            f"yet the CSI was {decline_pct:.0f}% below its {csi_peak_year} peak",
        )
        narrative = (
            f"In {latest_gss_year}, {latest_bc_pct:.0f}% of BC residents reported that crime had "
            f"increased in their neighbourhood compared to five years earlier. Yet the Crime "
            f"Severity Index tells a different story: at {csi_latest_val:.0f}, BC's CSI was "
            f"{decline_pct:.0f}% below its {csi_peak_year} peak of {csi_peak:.0f}. Nationally, "
            f"{ca_vals[-1]:.0f}% of Canadians also believed crime had risen. The perception-reality "
            f"gap may be driven by media coverage, high-profile incidents, and the visibility of "
            f"certain crime types (e.g., property crime, disorder) even as overall severity declines. "
            f"Source: Statistics Canada, General Social Survey on Canadians' Safety (2019); "
            f"Table 35-10-0063-01."
        )
    else:
        add_fig_subtitle(
            fig,
            f"{latest_bc_pct:.0f}% of BC residents said crime increased in {latest_gss_year}",
        )
        narrative = (
            f"In {latest_gss_year}, {latest_bc_pct:.0f}% of BC residents reported that crime had "
            f"increased in their neighbourhood. Nationally, {ca_vals[-1]:.0f}% of Canadians shared "
            f"this view. Source: Statistics Canada, General Social Survey on Canadians' Safety (2019)."
        )

    if _perception_fallback:
        narrative += " (fallback data)"

    fig.tight_layout(pad=2.0)
    add_source(fig, "Source: Statistics Canada, General Social Survey on Canadians' Safety (2019); Table 35-10-0063-01")
    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_confidence_by_province(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Grouped horizontal bar chart: confidence in police by province, BC highlighted.

    Shows the proportion of respondents at each confidence level across
    provinces, sorted by 'Great deal of confidence'. BC bars are coloured
    in blue; other provinces are in grey.
    """
    apply_theme()
    confidence, _confidence_fallback = _get_confidence_data()

    # Pivot to get provinces as rows and confidence levels as columns
    pivot = confidence.pivot_table(
        index="geo", columns="confidence_level", values="value", aggfunc="first",
    ).reset_index()
    pivot.columns.name = None

    # Sort by "Great deal of confidence" descending
    sort_col = "Great deal of confidence"
    if sort_col not in pivot.columns:
        sort_col = pivot.columns[1]
    pivot = pivot.sort_values(sort_col, ascending=True).reset_index(drop=True)

    provinces = pivot["geo"].tolist()
    confidence_levels = ["Great deal of confidence", "Some confidence",
                         "Not very much confidence", "No confidence at all"]
    # Filter to levels actually present
    confidence_levels = [c for c in confidence_levels if c in pivot.columns]

    level_colors = {
        "Great deal of confidence": PALETTE["bc_teal"],
        "Some confidence": PALETTE["bc_blue"],
        "Not very much confidence": PALETTE["bc_amber"],
        "No confidence at all": PALETTE["bc_red"],
    }

    fig, ax = plt.subplots(figsize=FIGSIZE_DOUBLE)

    bar_height = 0.18
    y_positions = np.arange(len(provinces))

    for i, level in enumerate(confidence_levels):
        vals = pivot[level].values
        offset = (i - len(confidence_levels) / 2 + 0.5) * bar_height
        color = level_colors.get(level, ORDERED[i % len(ORDERED)])

        bars = ax.barh(
            y_positions + offset, vals, bar_height,
            color=color, label=level, edgecolor="white", linewidth=0.5,
        )

        # Bold the BC bar edges
        for j, prov in enumerate(provinces):
            if prov == "British Columbia":
                bars[j].set_edgecolor(PALETTE["bc_blue"])
                bars[j].set_linewidth(2.0)

    # Highlight BC label in bold
    ax.set_yticks(y_positions)
    tick_labels = []
    for prov in provinces:
        if prov == "British Columbia":
            tick_labels.append(f"** {prov} **")
        else:
            tick_labels.append(prov)
    ax.set_yticklabels(tick_labels)

    ax.set_xlabel("% of Respondents")
    ax.set_title("Confidence in Police by Province (GSS 2019)")
    ax.legend(loc="lower right", fontsize=8, ncol=2)
    style_axes(ax)
    ax.grid(axis="y", visible=False)
    fig.subplots_adjust(left=0.18)

    # Narrative
    bc_row = pivot[pivot["geo"] == "British Columbia"]
    if not bc_row.empty:
        bc_great = bc_row["Great deal of confidence"].values[0] if "Great deal of confidence" in bc_row.columns else 0
        bc_not_much = bc_row["Not very much confidence"].values[0] if "Not very much confidence" in bc_row.columns else 0
        bc_none = bc_row["No confidence at all"].values[0] if "No confidence at all" in bc_row.columns else 0
        bc_low_total = bc_not_much + bc_none

        add_subtitle(
            ax,
            f"BC: {bc_great:.0f}% have great confidence in police, "
            f"while {bc_low_total:.0f}% have little or no confidence",
        )

        narrative = (
            f"In 2019, {bc_great:.0f}% of BC residents reported a great deal of confidence in "
            f"their local police, while {bc_low_total:.0f}% reported not very much or no confidence "
            f"at all. BC ranks below Saskatchewan ({pivot[pivot['geo'] == 'Saskatchewan']['Great deal of confidence'].values[0]:.0f}%) "
            f"and Alberta ({pivot[pivot['geo'] == 'Alberta']['Great deal of confidence'].values[0]:.0f}%) "
            f"on the 'great deal of confidence' measure. Lower police confidence may contribute to "
            f"the perception that crime is rising, as residents who feel less protected may "
            f"overestimate local crime trends. "
            f"Source: Statistics Canada, General Social Survey on Canadians' Safety (2019)."
        )
    else:
        add_subtitle(ax, "Confidence in police varies across provinces")
        narrative = (
            "The chart compares confidence in police across provinces. "
            "Source: Statistics Canada, General Social Survey on Canadians' Safety (2019)."
        )

    if _confidence_fallback:
        narrative += " (fallback data)"

    add_source(fig, "Source: Statistics Canada, General Social Survey on Canadians' Safety (2019)")
    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_reporting_rates_by_type(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Horizontal bar chart: police reporting rate by crime type.

    Bars are coloured by rate level: red for <20%, amber for 20-50%,
    teal for >50%. Highlights the vast under-reporting of sexual assault
    and the relatively high reporting of motor vehicle theft.
    """
    apply_theme()
    data = REPORTING_RATES.copy()
    data = data.sort_values("reporting_rate", ascending=True).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    colors = []
    for rate in data["reporting_rate"]:
        if rate < REPORTING_RATE_LOW:
            colors.append(PALETTE["bc_red"])
        elif rate < REPORTING_RATE_MID:
            colors.append(PALETTE["bc_amber"])
        else:
            colors.append(PALETTE["bc_teal"])

    bars = ax.barh(data["crime_type"], data["reporting_rate"], color=colors, edgecolor="white")

    # Value labels
    for bar, val in zip(bars, data["reporting_rate"]):
        ax.text(
            bar.get_width() + 1.0,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.0f}%",
            ha="left", va="center", fontsize=10, fontweight="bold",
        )

    ax.set_xlabel("% of Incidents Reported to Police")
    ax.set_title("Police Reporting Rates by Crime Type (GSS 2019)")
    ax.set_xlim(0, 75)
    style_axes(ax)
    ax.grid(axis="y", visible=False)

    # Add a reference line at the overall average
    avg_rate = data[data["crime_type"] == "Total criminal victimization"]["reporting_rate"].values[0]
    ax.axvline(avg_rate, color=PALETTE["bc_slate"], linewidth=1.2, linestyle="--", zorder=0)
    ax.text(
        avg_rate + 0.5, len(data) - 0.5,
        f"Overall avg: {avg_rate:.0f}%",
        fontsize=9, color=PALETTE["bc_slate"],
    )

    # Legend for colour coding
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=PALETTE["bc_red"], label=f"< {REPORTING_RATE_LOW:.0f}% reported"),
        Patch(facecolor=PALETTE["bc_amber"], label=f"{REPORTING_RATE_LOW:.0f}%--{REPORTING_RATE_MID:.0f}% reported"),
        Patch(facecolor=PALETTE["bc_teal"], label=f"> {REPORTING_RATE_MID:.0f}% reported"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=9)

    # Narrative
    lowest = data.iloc[0]
    highest = data.iloc[-1]
    add_subtitle(
        ax,
        f"Only {lowest['reporting_rate']:.0f}% of {lowest['crime_type'].lower()} "
        f"incidents are reported -- police stats capture a fraction of reality",
    )

    narrative = (
        f"Only {avg_rate:.0f}% of all criminal victimization incidents are reported to police, "
        f"meaning official crime statistics capture less than a third of actual crime. Reporting "
        f"rates vary dramatically: {highest['crime_type'].lower()} has the highest rate at "
        f"{highest['reporting_rate']:.0f}%, while {lowest['crime_type'].lower()} is reported just "
        f"{lowest['reporting_rate']:.0f}% of the time. This under-reporting means that changes in "
        f"reporting behaviour -- not actual crime levels -- can drive apparent statistical trends. "
        f"Source: Cotter (2021), Juristat, Catalogue no. 85-002-X."
    )

    add_source(fig, "Source: Cotter (2021), Juristat, Catalogue no. 85-002-X")
    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


# ---------------------------------------------------------------------------
# Run all
# ---------------------------------------------------------------------------

def run_all() -> dict[str, str]:
    """Generate all Priority 7 charts and return narratives."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    narratives: dict[str, str] = {}

    charts = [
        ("q5_perception_vs_reality", chart_perception_vs_reality),
        ("q5_confidence_by_province", chart_confidence_by_province),
        ("q5_reporting_rates", chart_reporting_rates_by_type),
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
