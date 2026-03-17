"""Priority 6 — Where Is Crime Happening? Geographic Analysis.

Ranks BC police jurisdictions by crime volume, growth, and violence.
Compares BC Census Metropolitan Areas. Produces static charts and an
interactive Plotly HTML visualisation.
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
    FIGSIZE_WIDE,
    ORDERED,
    PALETTE,
    add_fig_subtitle,
    add_source,
    add_subtitle,
    annotate_events,
    apply_theme,
    save_fig,
    style_axes,
)

from src.paths import CHARTS_DIR, PROCESSED_DIR

logger = logging.getLogger(__name__)

# Jurisdiction-level categories in the BC Gov data
CAT_TOTAL = "Criminal Code Offences"
CAT_VIOLENT = "Violent Offences"
CAT_PROPERTY = "Property Offences"

# The BC-wide aggregate row uses this jurisdiction name
BC_AGGREGATE = " BRITISH COLUMBIA"

# CMA labels shown on charts (mapped from raw geo strings)
CMA_GEO_MAP = {
    "Vancouver, British Columbia": "Vancouver",
    "Victoria, British Columbia": "Victoria",
    "Kelowna, British Columbia": "Kelowna",
    "Abbotsford-Mission, British Columbia": "Abbotsford-Mission",
    "Kamloops, British Columbia": "Kamloops",
    "Nanaimo, British Columbia": "Nanaimo",
    "Chilliwack, British Columbia": "Chilliwack",
}

# Top-N constants
TOP_N_BAR = 20
TOP_N_TREND = 8
FIVE_YEAR_WINDOW = 5


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def _load_jurisdiction() -> pd.DataFrame:
    """Load the BC Gov jurisdiction trends parquet, excluding the province-wide aggregate."""
    df = pd.read_parquet(PROCESSED_DIR / "bc_gov_jurisdiction_trends.parquet")
    # Strip leading/trailing whitespace from string columns
    for col in ("region", "type_of_policing", "policing_jurisdiction", "category"):
        df[col] = df[col].str.strip()
    # Drop the province-wide aggregate row so it does not dominate rankings
    df = df[df["policing_jurisdiction"] != "BRITISH COLUMBIA"].copy()
    df = df.reset_index(drop=True)
    return df


def _load_cma_rates() -> pd.DataFrame:
    """Load CMA-level crime rates for BC metro areas from the national table.

    Returns a DataFrame with columns: year, geo, cma_label, crime_rate.
    """
    df = pd.read_parquet(PROCESSED_DIR / "crime_incidents_national.parquet")

    mask = (
        df["geo"].isin(CMA_GEO_MAP.keys())
        & (df["violation"] == "Total, all Criminal Code violations (excluding traffic) [50]")
        & (df["statistic"] == "Rate per 100,000 population")
    )
    result = df[mask][["year", "geo", "value"]].copy()
    result = result.rename(columns={"value": "crime_rate"})
    result["cma_label"] = result["geo"].map(CMA_GEO_MAP)
    result = result.dropna(subset=["crime_rate"]).sort_values(["geo", "year"])
    result = result.reset_index(drop=True)
    return result


# ---------------------------------------------------------------------------
# Ranking helpers
# ---------------------------------------------------------------------------

def _rank_latest_total(jur: pd.DataFrame) -> pd.DataFrame:
    """Rank jurisdictions by total Criminal Code Offences count in the latest year."""
    latest_year = int(jur["year"].max())
    latest = jur[(jur["year"] == latest_year) & (jur["category"] == CAT_TOTAL)].copy()
    latest = latest.dropna(subset=["count"])
    latest = latest.sort_values("count", ascending=False).reset_index(drop=True)
    latest["rank"] = range(1, len(latest) + 1)
    return latest


def _rank_five_year_change(jur: pd.DataFrame) -> pd.DataFrame:
    """Rank jurisdictions by 5-year % change in total Criminal Code Offences."""
    latest_year = int(jur["year"].max())
    start_year = latest_year - FIVE_YEAR_WINDOW

    start = (
        jur[(jur["year"] == start_year) & (jur["category"] == CAT_TOTAL)]
        [["policing_jurisdiction", "count"]]
        .rename(columns={"count": "count_start"})
    )
    end = (
        jur[(jur["year"] == latest_year) & (jur["category"] == CAT_TOTAL)]
        [["policing_jurisdiction", "count"]]
        .rename(columns={"count": "count_end"})
    )

    merged = start.merge(end, on="policing_jurisdiction")
    merged = merged.dropna(subset=["count_start", "count_end"])
    # Exclude tiny jurisdictions (< 50 offences in the start year) to avoid misleading % swings
    merged = merged[merged["count_start"] >= 50].copy()
    merged["pct_change"] = ((merged["count_end"] - merged["count_start"]) / merged["count_start"]) * 100
    merged["start_year"] = start_year
    merged["end_year"] = latest_year
    merged = merged.sort_values("pct_change", ascending=False).reset_index(drop=True)
    merged["rank"] = range(1, len(merged) + 1)
    return merged


def _rank_violent(jur: pd.DataFrame) -> pd.DataFrame:
    """Rank jurisdictions by violent offence count in the latest year."""
    latest_year = int(jur["year"].max())
    violent = jur[(jur["year"] == latest_year) & (jur["category"] == CAT_VIOLENT)].copy()
    violent = violent.dropna(subset=["count"])
    violent = violent.sort_values("count", ascending=False).reset_index(drop=True)
    violent["rank"] = range(1, len(violent) + 1)
    return violent


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------

def chart_top_jurisdictions(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Horizontal bar chart: top 20 jurisdictions by total crime count (latest year)."""
    apply_theme()
    jur = _load_jurisdiction()
    ranked = _rank_latest_total(jur)
    latest_year = int(jur["year"].max())

    top = ranked.head(TOP_N_BAR).sort_values("count", ascending=True)

    fig, ax = plt.subplots(figsize=FIGSIZE_DOUBLE)

    # Colour the bars: Metro Vancouver jurisdictions in blue, others in teal
    colors = [
        PALETTE["bc_blue"] if "Mun" in j else PALETTE["bc_teal"]
        for j in top["policing_jurisdiction"]
    ]
    bars = ax.barh(top["policing_jurisdiction"], top["count"], color=colors, edgecolor="white")

    # Value labels
    for bar, val in zip(bars, top["count"]):
        ax.text(
            bar.get_width() + 200,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,.0f}",
            ha="left",
            va="center",
            fontsize=8,
        )

    ax.set_title(f"Top {TOP_N_BAR} BC Policing Jurisdictions by Total Crime Count ({latest_year})")
    ax.set_xlabel("Criminal Code Offences (count)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    style_axes(ax)
    ax.grid(axis="y", visible=False)
    fig.subplots_adjust(left=0.18)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=PALETTE["bc_blue"], label="Municipal police"),
        Patch(facecolor=PALETTE["bc_teal"], label="RCMP / Provincial"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=9)

    # Narrative
    top1 = ranked.iloc[0]
    add_subtitle(ax, f"Municipal police forces dominate — {top1['policing_jurisdiction']} leads with {top1['count']:,.0f} offences")
    top3_names = ", ".join(ranked["policing_jurisdiction"].head(3).tolist())
    narrative = (
        f"In {latest_year}, {top1['policing_jurisdiction']} recorded the highest crime count at "
        f"{top1['count']:,.0f} Criminal Code offences. The top three jurisdictions — {top3_names} — "
        f"together account for a large share of BC's total crime volume. Municipal police forces in "
        f"Metro Vancouver dominate the rankings, reflecting the region's population concentration. "
        f"Source: BC Government Police Resources in British Columbia."
    )

    add_source(fig, "Source: BC Government, Police Resources in British Columbia")
    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_jurisdiction_trends(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Small multiples: crime trends for the 8 largest jurisdictions (2014-2023)."""
    apply_theme()
    jur = _load_jurisdiction()
    ranked = _rank_latest_total(jur)

    # Get the top N jurisdictions by latest-year total
    top_jurisdictions = ranked.head(TOP_N_TREND)["policing_jurisdiction"].tolist()

    fig, axes = plt.subplots(2, 4, figsize=FIGSIZE_WIDE, sharex=True)
    axes = axes.flatten()

    for i, jurisdiction in enumerate(top_jurisdictions):
        ax = axes[i]
        j_data = jur[
            (jur["policing_jurisdiction"] == jurisdiction) & (jur["category"] == CAT_TOTAL)
        ].sort_values("year")

        color = ORDERED[i % len(ORDERED)]
        ax.plot(j_data["year"], j_data["count"], color=color, linewidth=2, marker="o", markersize=3)
        ax.fill_between(j_data["year"], j_data["count"], alpha=0.1, color=color)

        ax.set_title(jurisdiction, fontsize=10, fontweight="bold")
        ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax.tick_params(axis="x", rotation=45, labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        style_axes(ax)

    min_yr = int(jur["year"].min())
    max_yr = int(jur["year"].max())
    fig.suptitle(
        f"Crime Trends in BC's 8 Largest Policing Jurisdictions ({min_yr}–{max_yr})",
        fontsize=14, fontweight="bold", y=1.04,
    )
    add_fig_subtitle(fig, "Tracking the 8 highest-volume jurisdictions over a decade")
    fig.supylabel("Criminal Code Offences (count)")
    fig.tight_layout(pad=2.0)

    # Narrative — identify which jurisdictions are trending up vs down
    trends = []
    for jurisdiction in top_jurisdictions:
        j_data = jur[
            (jur["policing_jurisdiction"] == jurisdiction) & (jur["category"] == CAT_TOTAL)
        ].sort_values("year")
        if len(j_data) >= 2:
            first = j_data.iloc[0]["count"]
            last = j_data.iloc[-1]["count"]
            if pd.notna(first) and pd.notna(last) and first > 0:
                pct = ((last - first) / first) * 100
                trends.append((jurisdiction, pct))

    rising = [(j, p) for j, p in trends if p > 0]
    falling = [(j, p) for j, p in trends if p <= 0]

    rising_str = ", ".join(f"{j} (+{p:.0f}%)" for j, p in sorted(rising, key=lambda x: -x[1])[:3])
    falling_str = ", ".join(f"{j} ({p:.0f}%)" for j, p in sorted(falling, key=lambda x: x[1])[:3])

    narrative = (
        f"Among BC's {TOP_N_TREND} highest-volume jurisdictions, those with the largest 10-year "
        f"increases include {rising_str or 'none'}. "
    )
    if falling_str:
        narrative += f"Jurisdictions with declining or stable counts include {falling_str}. "
    narrative += "Source: BC Government Police Resources in British Columbia."

    add_source(fig, "Source: BC Government, Police Resources in British Columbia")
    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_total_vs_violent(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Scatter plot: total crime count vs violent crime count per jurisdiction (latest year)."""
    apply_theme()
    jur = _load_jurisdiction()
    latest_year = int(jur["year"].max())

    total = (
        jur[(jur["year"] == latest_year) & (jur["category"] == CAT_TOTAL)]
        [["policing_jurisdiction", "region", "count"]]
        .rename(columns={"count": "total_count"})
    )
    violent = (
        jur[(jur["year"] == latest_year) & (jur["category"] == CAT_VIOLENT)]
        [["policing_jurisdiction", "count"]]
        .rename(columns={"count": "violent_count"})
    )

    merged = total.merge(violent, on="policing_jurisdiction")
    merged = merged.dropna(subset=["total_count", "violent_count"])
    merged["violent_share"] = (merged["violent_count"] / merged["total_count"]) * 100

    fig, ax = plt.subplots(figsize=FIGSIZE_DOUBLE)

    ax.scatter(
        merged["total_count"],
        merged["violent_count"],
        c=merged["violent_share"],
        cmap="YlOrRd",
        s=40,
        alpha=0.7,
        edgecolors="white",
        linewidth=0.5,
    )

    # Add colorbar
    sm = plt.cm.ScalarMappable(
        cmap="YlOrRd",
        norm=plt.Normalize(vmin=merged["violent_share"].min(), vmax=merged["violent_share"].max()),
    )
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, shrink=0.8)
    cbar.set_label("Violent Share (%)", fontsize=10)

    # Label the top jurisdictions
    top_total = merged.nlargest(8, "total_count")
    top_violent_share = merged.nlargest(5, "violent_share")
    to_label = pd.concat([top_total, top_violent_share]).drop_duplicates("policing_jurisdiction")

    for _, row in to_label.iterrows():
        ax.annotate(
            row["policing_jurisdiction"].replace(" Mun", "").replace(" Prov", ""),
            xy=(row["total_count"], row["violent_count"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
            color=PALETTE["bc_slate"],
            bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "alpha": 0.7, "edgecolor": "none"},
        )

    # Trend line
    valid = merged[["total_count", "violent_count"]].dropna()
    if len(valid) > 2:
        z = np.polyfit(valid["total_count"], valid["violent_count"], 1)
        p = np.poly1d(z)
        x_line = np.linspace(valid["total_count"].min(), valid["total_count"].max(), 100)
        ax.plot(x_line, p(x_line), "--", color=PALETTE["bc_slate"], linewidth=1, alpha=0.5)
        corr = valid["total_count"].corr(valid["violent_count"])
        ax.text(
            0.02, 0.95,
            f"r = {corr:.2f}",
            transform=ax.transAxes,
            fontsize=10,
            color=PALETTE["bc_slate"],
        )
        add_subtitle(ax, f"Strong correlation (r = {corr:.2f}) — high-crime jurisdictions are also high-violence")

    ax.set_title(f"Total Crime vs Violent Crime by Jurisdiction ({latest_year})")
    ax.set_xlabel("Total Criminal Code Offences")
    ax.set_ylabel("Violent Offences")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    style_axes(ax)

    # Narrative
    avg_share = merged["violent_share"].mean()
    high_violence = merged[merged["violent_share"] > avg_share + 10]
    high_violence_names = ", ".join(
        high_violence.nlargest(5, "violent_share")["policing_jurisdiction"]
        .str.replace(" Mun", "").str.replace(" Prov", "").tolist()
    )

    narrative = (
        f"The scatter plot reveals a strong positive correlation (r = {corr:.2f}) between total "
        f"and violent crime — jurisdictions with higher overall crime also tend to have more "
        f"violent offences. The average violent share across jurisdictions is {avg_share:.1f}%. "
    )
    if high_violence_names:
        narrative += (
            f"Jurisdictions with a disproportionately high violent share (>10pp above average) "
            f"include {high_violence_names}. "
        )
    narrative += "Source: BC Government Police Resources in British Columbia."

    add_source(fig, "Source: BC Government, Police Resources in British Columbia")
    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_cma_comparison(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Bar chart: CMA crime rate per 100,000 for BC's main metro areas (latest year)."""
    apply_theme()
    cma = _load_cma_rates()
    latest_year = int(cma["year"].max())

    latest = cma[cma["year"] == latest_year].copy()
    latest = latest.sort_values("crime_rate", ascending=True)

    fig, ax = plt.subplots(figsize=FIGSIZE_SMALL)

    # Colour palette: highlight the 4 original CMAs differently
    highlight_cmas = {"Vancouver", "Victoria", "Kelowna", "Abbotsford-Mission"}
    colors = [
        PALETTE["bc_blue"] if label in highlight_cmas else PALETTE["bc_teal"]
        for label in latest["cma_label"]
    ]

    bars = ax.barh(latest["cma_label"], latest["crime_rate"], color=colors, edgecolor="white")

    for bar, val in zip(bars, latest["crime_rate"]):
        ax.text(
            bar.get_width() + 80,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,.0f}",
            ha="left",
            va="center",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_title(f"Criminal Code Offence Rate per 100,000 — BC Census Metropolitan Areas ({latest_year})")
    ax.set_xlabel("Rate per 100,000 Population")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    style_axes(ax)
    ax.grid(axis="y", visible=False)

    # Narrative
    highest = latest.iloc[-1]
    lowest = latest.iloc[0]
    ratio = highest["crime_rate"] / lowest["crime_rate"] if lowest["crime_rate"] > 0 else 0
    add_subtitle(ax, f"Interior CMAs report up to {ratio:.1f}x higher per-capita crime than coastal metros")

    narrative = (
        f"In {latest_year}, {highest['cma_label']} had the highest criminal offence rate at "
        f"{highest['crime_rate']:,.0f} per 100,000, while {lowest['cma_label']} had the lowest at "
        f"{lowest['crime_rate']:,.0f} — a {ratio:.1f}x difference. Smaller interior CMAs "
        f"(Kamloops, Chilliwack, Nanaimo, Kelowna) report substantially higher per-capita crime "
        f"than the large coastal metros (Vancouver, Victoria). "
        f"Source: Statistics Canada Table 35-10-0177-01."
    )

    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")
    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_interactive_jurisdiction(save_path: Path | None = None) -> str:
    """Plotly interactive bar chart of jurisdiction crime data, saved as HTML.

    Returns the narrative string.
    """
    try:
        import plotly.express as px
    except ImportError:
        logger.warning("Plotly not installed — skipping interactive chart.")
        return "Interactive chart skipped (plotly not available)."

    jur = _load_jurisdiction()
    latest_year = int(jur["year"].max())

    # Build a wide table: jurisdiction × (total, violent, property) for the latest year
    pivot = jur[jur["year"] == latest_year].pivot_table(
        index=["policing_jurisdiction", "region"],
        columns="category",
        values="count",
        aggfunc="first",
    ).reset_index()
    pivot.columns.name = None

    # Clean up column names
    col_map = {
        CAT_TOTAL: "total_offences",
        CAT_VIOLENT: "violent_offences",
        CAT_PROPERTY: "property_offences",
    }
    pivot = pivot.rename(columns=col_map)
    pivot = pivot.dropna(subset=["total_offences"])

    # Compute violent share
    pivot["violent_share_pct"] = (
        pivot["violent_offences"].fillna(0) / pivot["total_offences"] * 100
    ).round(1)

    pivot = pivot.sort_values("total_offences", ascending=False).head(50)

    fig = px.bar(
        pivot,
        x="policing_jurisdiction",
        y="total_offences",
        color="region",
        hover_data=["violent_offences", "property_offences", "violent_share_pct"],
        title=f"Top 50 BC Policing Jurisdictions by Total Crime Count ({latest_year})",
        labels={
            "policing_jurisdiction": "Jurisdiction",
            "total_offences": "Criminal Code Offences",
            "region": "Region",
            "violent_offences": "Violent Offences",
            "property_offences": "Property Offences",
            "violent_share_pct": "Violent Share (%)",
        },
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        template="plotly_white",
        height=600,
        width=1200,
        font={"size": 11},
    )

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(save_path))
        logger.info("  Saved interactive chart: %s", save_path)

    narrative = (
        f"The interactive chart shows the top 50 BC policing jurisdictions by total crime count "
        f"in {latest_year}, colour-coded by region. Hover for violent/property breakdowns. "
        f"Metro Vancouver jurisdictions dominate, but several interior and northern jurisdictions "
        f"appear in the top 50 despite smaller populations, indicating higher per-capita crime. "
        f"Source: BC Government Police Resources in British Columbia."
    )
    return narrative


# ---------------------------------------------------------------------------
# Run all
# ---------------------------------------------------------------------------

def chart_cma_trends(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Small multiples: crime rate trends over time for each BC CMA."""
    apply_theme()
    cma = _load_cma_rates()
    cma = cma[cma["year"] >= 2004]

    cma_labels = sorted(cma["cma_label"].dropna().unique())
    n_cmas = len(cma_labels)
    if n_cmas == 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, "No CMA data available", ha="center", va="center", transform=ax.transAxes)
        return fig, "No CMA trend data available."

    ncols = min(4, n_cmas)
    nrows = (n_cmas + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(16, 4 * nrows), sharex=True, sharey=True)
    if nrows == 1 and ncols == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    for i, label in enumerate(cma_labels):
        ax = axes[i]
        c_data = cma[cma["cma_label"] == label].sort_values("year")
        color = ORDERED[i % len(ORDERED)]
        ax.plot(c_data["year"], c_data["crime_rate"], color=color, linewidth=2, marker="o", markersize=3)
        ax.fill_between(c_data["year"], c_data["crime_rate"], alpha=0.1, color=color)
        ax.set_title(label, fontsize=10, fontweight="bold")
        ax.xaxis.set_major_locator(mticker.MultipleLocator(4))
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax.tick_params(axis="x", rotation=45, labelsize=8)
        style_axes(ax)
        annotate_events(ax)

    for j in range(n_cmas, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("Crime Rate Trends Across BC Census Metropolitan Areas",
                 fontsize=14, fontweight="bold", y=1.04)
    add_fig_subtitle(fig, "Interior CMAs have consistently higher rates than coastal metros")
    fig.supylabel("Rate per 100,000")
    fig.tight_layout(pad=2.0)

    narrative = (
        "The CMA trend charts reveal whether high-crime metro areas have always been high "
        "or recently surged. This temporal context complements the single-year snapshot. "
        "Source: Statistics Canada Table 35-10-0177-01."
    )

    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_crime_concentration(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Pareto curve: cumulative share of total crime by jurisdiction."""
    apply_theme()
    jur = _load_jurisdiction()
    ranked = _rank_latest_total(jur)
    latest_year = int(jur["year"].max())

    total_crime = ranked["count"].sum()
    ranked["cumulative_share"] = ranked["count"].cumsum() / total_crime * 100
    ranked["jurisdiction_pct"] = np.arange(1, len(ranked) + 1) / len(ranked) * 100

    fig, ax = plt.subplots(figsize=FIGSIZE_SMALL)
    ax.plot(ranked["jurisdiction_pct"], ranked["cumulative_share"],
            color=PALETTE["bc_blue"], linewidth=2.5)
    ax.plot([0, 100], [0, 100], "--", color=PALETTE["light_grey"], linewidth=1, label="Perfect equality")
    ax.fill_between(ranked["jurisdiction_pct"], ranked["cumulative_share"],
                     ranked["jurisdiction_pct"], alpha=0.1, color=PALETTE["bc_blue"])

    # Annotate the 50% and 80% thresholds
    for threshold in [50, 80]:
        idx = (ranked["cumulative_share"] >= threshold).idxmax()
        x_val = ranked.loc[idx, "jurisdiction_pct"]
        ax.axhline(threshold, color=PALETTE["bc_slate"], linewidth=0.5, linestyle=":")
        ax.axvline(x_val, color=PALETTE["bc_slate"], linewidth=0.5, linestyle=":")
        ax.annotate(
            f"{threshold}% of crime\n← {x_val:.0f}% of jurisdictions",
            xy=(x_val, threshold), xytext=(x_val + 10, threshold - 8),
            fontsize=9, color=PALETTE["bc_slate"],
            arrowprops={"arrowstyle": "->", "color": PALETTE["bc_slate"], "lw": 0.8},
        )

    ax.set_title(f"Crime Concentration Across BC Jurisdictions ({latest_year})")
    ax.set_xlabel("Cumulative % of Jurisdictions (ranked by crime volume)")
    ax.set_ylabel("Cumulative % of Total Crime")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 105)
    ax.legend(loc="lower right", fontsize=9)
    style_axes(ax)

    # Find the jurisdiction % that accounts for 50% of crime
    idx_50 = (ranked["cumulative_share"] >= 50).idxmax()
    pct_50 = ranked.loc[idx_50, "jurisdiction_pct"]
    add_subtitle(ax, f"Just {pct_50:.0f}% of jurisdictions account for 50% of all crime")

    narrative = (
        f"Crime in BC is highly concentrated: just {pct_50:.0f}% of jurisdictions account for "
        f"50% of all Criminal Code offences. The Pareto curve shows a steep initial rise, "
        f"meaning a small number of high-volume jurisdictions dominate provincial crime statistics. "
        f"Source: BC Government Police Resources in British Columbia."
    )

    add_source(fig, "Source: BC Government, Police Resources in British Columbia")

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_violent_share_distribution(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Strip plot: distribution of violent crime share across jurisdictions."""
    apply_theme()
    jur = _load_jurisdiction()
    latest_year = int(jur["year"].max())

    total = (
        jur[(jur["year"] == latest_year) & (jur["category"] == CAT_TOTAL)]
        [["policing_jurisdiction", "count"]]
        .rename(columns={"count": "total_count"})
    )
    violent = (
        jur[(jur["year"] == latest_year) & (jur["category"] == CAT_VIOLENT)]
        [["policing_jurisdiction", "count"]]
        .rename(columns={"count": "violent_count"})
    )

    merged = total.merge(violent, on="policing_jurisdiction")
    merged = merged.dropna(subset=["total_count", "violent_count"])
    merged = merged[merged["total_count"] >= 100]  # Exclude tiny jurisdictions
    merged["violent_share"] = (merged["violent_count"] / merged["total_count"]) * 100
    merged = merged.sort_values("violent_share", ascending=True).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=FIGSIZE_SMALL)
    avg_share = merged["violent_share"].mean()

    colors = [
        PALETTE["bc_red"] if v > avg_share + 10 else
        PALETTE["bc_teal"] if v < avg_share - 10 else
        PALETTE["bc_slate"]
        for v in merged["violent_share"]
    ]
    ax.scatter(merged["violent_share"], range(len(merged)), c=colors, s=40, zorder=5)
    ax.axvline(avg_share, color=PALETTE["bc_blue"], linewidth=1.5, linestyle="--",
               label=f"Average: {avg_share:.1f}%")

    # Label outliers (top 5 and bottom 5)
    for idx in list(merged.index[:3]) + list(merged.index[-3:]):
        row = merged.loc[idx]
        ax.annotate(
            row["policing_jurisdiction"].replace(" Mun", "").replace(" Prov", ""),
            xy=(row["violent_share"], idx),
            xytext=(5, 0), textcoords="offset points",
            fontsize=9, color=PALETTE["bc_slate"],
        )

    ax.set_title(f"Distribution of Violent Crime Share Across BC Jurisdictions ({latest_year})")
    ax.set_xlabel("Violent Offences as % of Total Crime")
    ax.set_yticks([])
    ax.legend(loc="upper right", fontsize=9)
    style_axes(ax)
    add_subtitle(ax, f"Average violent share: {avg_share:.1f}% — red dots are 10+ pp above average")

    std_share = merged["violent_share"].std()
    narrative = (
        f"Across {len(merged)} jurisdictions (with 100+ offences), the violent crime share "
        f"averages {avg_share:.1f}% with a standard deviation of {std_share:.1f}pp. "
        f"Red dots indicate jurisdictions with disproportionately high violence (>10pp above average). "
        f"Source: BC Government Police Resources in British Columbia."
    )

    add_source(fig, "Source: BC Government, Police Resources in British Columbia")

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def run_all() -> dict[str, str]:
    """Generate all Priority 6 charts and return narratives."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    narratives: dict[str, str] = {}

    # Static matplotlib charts
    charts = [
        ("q4_top_jurisdictions", chart_top_jurisdictions),
        ("q4_jurisdiction_trends", chart_jurisdiction_trends),
        ("q4_total_vs_violent", chart_total_vs_violent),
        ("q4_cma_comparison", chart_cma_comparison),
        ("q4_cma_trends", chart_cma_trends),
        ("q4_crime_concentration", chart_crime_concentration),
        ("q4_violent_share_distribution", chart_violent_share_distribution),
    ]

    for name, fn in charts:
        path = CHARTS_DIR / f"{name}.png"
        logger.info("Generating %s ...", name)
        _, narrative = fn(save_path=path)
        narratives[name] = narrative
        logger.info("  Saved %s", path)

    # Interactive Plotly chart
    interactive_path = CHARTS_DIR / "q4_interactive_map.html"
    logger.info("Generating interactive chart ...")
    interactive_narrative = chart_interactive_jurisdiction(save_path=interactive_path)
    narratives["q4_interactive"] = interactive_narrative

    # Log jurisdiction rankings summary
    jur = _load_jurisdiction()
    ranked_total = _rank_latest_total(jur)
    ranked_change = _rank_five_year_change(jur)
    ranked_violent = _rank_violent(jur)

    logger.info("\nTop 10 jurisdictions by total crime count (%d):", int(jur["year"].max()))
    for _, row in ranked_total.head(10).iterrows():
        logger.info("  #%d  %s: %s", row["rank"], row["policing_jurisdiction"], f"{row['count']:,.0f}")

    logger.info("\nTop 10 jurisdictions by 5-year crime increase:")
    for _, row in ranked_change.head(10).iterrows():
        logger.info(
            "  #%d  %s: %+.1f%% (%d→%d)",
            row["rank"], row["policing_jurisdiction"], row["pct_change"],
            row["start_year"], row["end_year"],
        )

    logger.info("\nTop 10 jurisdictions by violent offence count (%d):", int(jur["year"].max()))
    for _, row in ranked_violent.head(10).iterrows():
        logger.info("  #%d  %s: %s", row["rank"], row["policing_jurisdiction"], f"{row['count']:,.0f}")

    return narratives


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    narratives = run_all()
    print("\n" + "=" * 70)
    print("NARRATIVES")
    print("=" * 70)
    for name, text in narratives.items():
        print(f"\n### {name}\n{text}")
