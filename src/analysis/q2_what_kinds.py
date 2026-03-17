"""Priority 4 — What Kinds of Crime Are Rising in BC?

Breakdown by violation category: composition trends, fastest-rising and
fastest-declining offences, heatmap, and slope chart.
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

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

logger = logging.getLogger(__name__)

PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"
CHARTS_DIR = Path(__file__).resolve().parent.parent.parent / "outputs" / "charts"

# Category groupings using StatCan aggregate violation codes
CATEGORIES = {
    "Violent crime": "Total violent Criminal Code violations [100]",
    "Property crime": "Total property crime violations [200]",
    "Administration of justice": "Total administration of justice violations [330]",
    "Other Criminal Code": "Total other Criminal Code violations [300]",
    "Drug offences": "Total drug violations [401]",
}

# Specific violations to track for fastest-rising/declining analysis
SPECIFIC_VIOLATIONS = [
    "Homicide [110]",
    "Attempted murder [1210]",
    "Assault, level 1 [1430]",
    "Assault, level 2, weapon or bodily harm [1420]",
    "Assault, level 3, aggravated [1410]",
    "Total sexual violations against children [130]",
    "Sexual assault, level 1 [1610]",
    "Robbery [1610]",
    "Total robbery [160]",
    "Breaking and entering [2120]",
    "Total theft of motor vehicle [220]",
    "Total theft under $5,000 (non-motor vehicle) [240]",
    "Total theft over $5,000 (non-motor vehicle) [230]",
    "Total mischief [250]",
    "Fraud [2160]",
    "Total possession of stolen property [211]",
    "Arson [2110]",
    "Breach of probation [3520]",
    "Total weapons violations [310]",
    "Total offences in relation to sexual services [190]",
    "Impaired driving (alcohol) [9110]",
    "Identity theft [2162]",
    "Identity fraud [2163]",
    "Extortion [3410]",
]


def _load_bc_rates() -> pd.DataFrame:
    """Load BC crime rates per 100,000 from the national table."""
    df = pd.read_parquet(PROCESSED_DIR / "crime_incidents_national.parquet")
    mask = (
        (df["geo"] == "British Columbia")
        & (df["statistic"] == "Rate per 100,000 population")
    )
    result = df[mask][["year", "violation", "value"]].copy()
    result = result.rename(columns={"value": "rate"})
    result = result.dropna(subset=["rate"]).sort_values(["violation", "year"])
    return result.reset_index(drop=True)


def _category_rates(bc: pd.DataFrame) -> pd.DataFrame:
    """Extract rates for the 5 main crime categories."""
    records = []
    for label, violation in CATEGORIES.items():
        cat = bc[bc["violation"] == violation][["year", "rate"]].copy()
        cat["category"] = label
        records.append(cat)
    return pd.concat(records, ignore_index=True)


def _fastest_changing(bc: pd.DataFrame, n: int = 5, window_years: int = 5) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Find the top N fastest-rising and fastest-declining specific violations.

    Compares the latest year to (latest - window_years).
    """
    latest = int(bc["year"].max())
    start = latest - window_years

    changes = []
    for viol in bc["violation"].unique():
        v = bc[bc["violation"] == viol]
        start_row = v[v["year"] == start]
        end_row = v[v["year"] == latest]
        if start_row.empty or end_row.empty:
            continue
        rate_start = start_row["rate"].values[0]
        rate_end = end_row["rate"].values[0]
        if rate_start == 0:
            continue
        pct_chg = ((rate_end - rate_start) / rate_start) * 100
        abs_chg = rate_end - rate_start
        changes.append({
            "violation": viol,
            "rate_start": rate_start,
            "rate_end": rate_end,
            "pct_change": pct_chg,
            "abs_change": abs_chg,
            "start_year": start,
            "end_year": latest,
        })

    df_chg = pd.DataFrame(changes)
    # Filter out aggregate/total categories for specific analysis
    specific = df_chg[~df_chg["violation"].str.startswith("Total")]
    rising = specific.nlargest(n, "pct_change")
    declining = specific.nsmallest(n, "pct_change")
    return rising, declining


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------

def chart_stacked_area(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Stacked area chart: crime composition over time."""
    apply_theme()
    bc = _load_bc_rates()
    cats = _category_rates(bc)

    # Pivot to wide format: year × category
    wide = cats.pivot_table(index="year", columns="category", values="rate", aggfunc="first")
    wide = wide.sort_index()
    # Keep only years >= 2000 for cleaner visual
    wide = wide[wide.index >= 2004]

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
    order = ["Violent crime", "Property crime", "Administration of justice", "Other Criminal Code", "Drug offences"]
    cols = [c for c in order if c in wide.columns]
    colors = ORDERED[:len(cols)]

    ax.stackplot(wide.index, [wide[c].values for c in cols], labels=cols, colors=colors, alpha=0.85)
    ax.set_title("BC Crime Composition by Category (rate per 100,000)")
    add_subtitle(ax, f"Total crime rate peaked near {int(wide.loc[wide.sum(axis=1).idxmax()].name)} and has declined {((wide.iloc[0].sum() - wide.iloc[-1].sum()) / wide.iloc[0].sum() * 100):.0f}% since")
    ax.set_xlabel("Year")
    ax.set_ylabel("Rate per 100,000")
    ax.legend(loc="upper left", fontsize=9)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    style_axes(ax)
    annotate_events(ax)

    # Narrative
    latest_yr = int(wide.index.max())
    latest_total = wide.loc[latest_yr].sum()
    property_share = wide.loc[latest_yr, "Property crime"] / latest_total * 100 if "Property crime" in wide.columns else 0
    narrative = (
        f"In {latest_yr}, BC's combined crime rate across the five categories was "
        f"{latest_total:,.0f} per 100,000. Property crime accounts for {property_share:.0f}% of "
        f"the total. The stacked chart shows a broad decline from 2003–2014 followed by "
        f"a plateau, with the composition shifting slightly toward violent crime. "
        f"Source: Statistics Canada Table 35-10-0177-01."
    )

    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_heatmap(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Heatmap: year × violation category, color = rate per 100,000."""
    apply_theme()
    bc = _load_bc_rates()
    cats = _category_rates(bc)
    cats = cats[cats["year"] >= 2014]

    wide = cats.pivot_table(index="category", columns="year", values="rate", aggfunc="first")
    wide = wide.reindex(list(CATEGORIES.keys()))

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
    sns.heatmap(
        wide,
        annot=True,
        fmt=".0f",
        cmap="YlOrRd",
        linewidths=0.5,
        ax=ax,
        cbar_kws={"label": "Rate per 100,000"},
    )
    ax.set_title(f"BC Crime Rate Heatmap by Category (2014–{int(wide.columns.max())})")
    add_subtitle(ax, "Property crime dominates by rate; violent crime shows gradual warming")
    ax.set_ylabel("")
    ax.set_xlabel("Year")

    # Narrative
    narrative = (
        "The heatmap reveals that property crime dominates by rate but has been relatively stable "
        "since 2014. Violent crime shows a gradual warming trend. Administration of justice violations "
        "have increased notably, reflecting more charges for bail violations and failure to appear. "
        "Source: Statistics Canada Table 35-10-0177-01."
    )

    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_top_changes(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Horizontal bar chart: top 10 violations by absolute rate change (last 5 years)."""
    apply_theme()
    bc = _load_bc_rates()

    # Get all violations' absolute changes over 5 years
    latest = int(bc["year"].max())
    start = latest - 5

    changes = []
    for viol in bc["violation"].unique():
        v = bc[bc["violation"] == viol]
        s = v[v["year"] == start]
        e = v[v["year"] == latest]
        if s.empty or e.empty:
            continue
        abs_chg = e["rate"].values[0] - s["rate"].values[0]
        # Skip totals/aggregates
        if viol.startswith("Total") or viol.startswith("Total,"):
            continue
        changes.append({"violation": viol, "abs_change": abs_chg})

    df_chg = pd.DataFrame(changes)
    # Top 10 by absolute value of change
    df_top = df_chg.reindex(df_chg["abs_change"].abs().nlargest(10).index).sort_values("abs_change")

    # Clean violation labels (remove codes)
    df_top["label"] = df_top["violation"].str.replace(r"\s*\[\d+\]", "", regex=True)

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
    colors = [PALETTE["bc_red"] if v > 0 else PALETTE["bc_teal"] for v in df_top["abs_change"]]
    ax.barh(df_top["label"], df_top["abs_change"], color=colors, edgecolor="white")

    for i, (val, label) in enumerate(zip(df_top["abs_change"], df_top["label"])):
        ax.text(
            val + (2 if val >= 0 else -2),
            i,
            f"{val:+.0f}",
            ha="left" if val >= 0 else "right",
            va="center",
            fontsize=9,
        )

    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title(f"Top 10 Violations by Absolute Rate Change ({start}–{latest})")
    add_subtitle(ax, f"Property theft drives declines; child exploitation and shoplifting are largest increases")
    ax.set_xlabel("Change in Rate per 100,000")
    style_axes(ax)
    ax.grid(axis="y", visible=False)
    fig.subplots_adjust(left=0.30)

    # Narrative
    biggest_rise = df_top.iloc[-1]
    biggest_drop = df_top.iloc[0]
    narrative = (
        f"The largest absolute increase was in {biggest_rise['label']} "
        f"({biggest_rise['abs_change']:+.0f} per 100,000), while the largest decrease was in "
        f"{biggest_drop['label']} ({biggest_drop['abs_change']:+.0f} per 100,000) over "
        f"{start}–{latest}. Source: Statistics Canada Table 35-10-0177-01."
    )

    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_slope(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Slope chart: ranking of violation categories, 2014 vs latest year."""
    apply_theme()
    bc = _load_bc_rates()
    cats = _category_rates(bc)

    latest_yr = int(cats["year"].max())
    start_yr = 2014

    start = cats[cats["year"] == start_yr].set_index("category")["rate"]
    end = cats[cats["year"] == latest_yr].set_index("category")["rate"]

    # Rank (highest rate = rank 1)
    start_rank = start.rank(ascending=False)
    end_rank = end.rank(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 6))

    categories = list(CATEGORIES.keys())
    for i, cat in enumerate(categories):
        if cat in start_rank.index and cat in end_rank.index:
            color = ORDERED[i % len(ORDERED)]
            ax.plot(
                [0, 1],
                [start_rank[cat], end_rank[cat]],
                color=color,
                linewidth=2.5,
                marker="o",
                markersize=8,
            )
            ax.text(-0.05, start_rank[cat], cat, ha="right", va="center", fontsize=10, color=color)
            ax.text(1.05, end_rank[cat], cat, ha="left", va="center", fontsize=10, color=color)

    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(len(categories) + 0.5, 0.5)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([str(start_yr), str(latest_yr)], fontsize=12, fontweight="bold")
    ax.set_yticks(range(1, len(categories) + 1))
    ax.set_yticklabels([""] * len(categories))
    ax.set_title(f"Crime Category Ranking: {start_yr} vs {latest_yr}")
    add_subtitle(ax, "Property crime remains #1 by rate in both years")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.grid(False)

    narrative = (
        f"The slope chart shows how crime category rankings have shifted from {start_yr} to {latest_yr}. "
        f"Property crime remains the highest-rate category in both years. "
        f"Source: Statistics Canada Table 35-10-0177-01."
    )

    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_composition_shares(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """100% stacked area: crime category shares over time."""
    apply_theme()
    bc = _load_bc_rates()
    cats = _category_rates(bc)

    wide = cats.pivot_table(index="year", columns="category", values="rate", aggfunc="first")
    wide = wide.sort_index()
    wide = wide[wide.index >= 2004]

    order = ["Violent crime", "Property crime", "Administration of justice", "Other Criminal Code", "Drug offences"]
    cols = [c for c in order if c in wide.columns]

    # Normalize each year to 100%
    row_totals = wide[cols].sum(axis=1)
    pct = wide[cols].div(row_totals, axis=0) * 100

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
    colors = ORDERED[:len(cols)]
    ax.stackplot(pct.index, [pct[c].values for c in cols], labels=cols, colors=colors, alpha=0.85)
    ax.set_ylim(0, 100)
    ax.set_title("BC Crime Composition — Share of Total by Category")
    ax.set_xlabel("Year")
    ax.set_ylabel("Share of Total (%)")
    ax.legend(loc="upper left", fontsize=9)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    style_axes(ax)
    annotate_events(ax)

    first_yr = int(pct.index.min())
    last_yr = int(pct.index.max())
    prop_first = pct.loc[first_yr, "Property crime"] if "Property crime" in pct.columns else 0
    prop_last = pct.loc[last_yr, "Property crime"] if "Property crime" in pct.columns else 0
    viol_first = pct.loc[first_yr, "Violent crime"] if "Violent crime" in pct.columns else 0
    viol_last = pct.loc[last_yr, "Violent crime"] if "Violent crime" in pct.columns else 0
    add_subtitle(ax, f"Property share fell from {prop_first:.0f}% to {prop_last:.0f}%; violent grew from {viol_first:.0f}% to {viol_last:.0f}%")

    narrative = (
        f"Property crime's share of total offences declined from {prop_first:.0f}% in {first_yr} "
        f"to {prop_last:.0f}% in {last_yr}, while violent crime grew from {viol_first:.0f}% to "
        f"{viol_last:.0f}%. This 100% stacked view reveals the compositional shift that absolute "
        f"rates obscure. Source: Statistics Canada Table 35-10-0177-01."
    )

    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_category_cagr(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Lollipop chart: 5-year CAGR by crime category."""
    apply_theme()
    bc = _load_bc_rates()
    cats = _category_rates(bc)

    latest_yr = int(cats["year"].max())
    start_yr = latest_yr - 5

    records = []
    for label in CATEGORIES:
        cat = cats[(cats["category"] == label)]
        s = cat[cat["year"] == start_yr]["rate"]
        e = cat[cat["year"] == latest_yr]["rate"]
        if s.empty or e.empty or s.values[0] == 0:
            continue
        cagr = ((e.values[0] / s.values[0]) ** (1 / 5) - 1) * 100
        records.append({"category": label, "cagr": cagr})

    df = pd.DataFrame(records).sort_values("cagr")

    fig, ax = plt.subplots(figsize=FIGSIZE_SMALL)
    colors = [PALETTE["bc_red"] if v > 0 else PALETTE["bc_teal"] for v in df["cagr"]]
    ax.hlines(y=df["category"], xmin=0, xmax=df["cagr"], color=colors, linewidth=2)
    ax.scatter(df["cagr"], df["category"], color=colors, s=80, zorder=5)

    for _, row in df.iterrows():
        offset = 0.3 if row["cagr"] >= 0 else -0.3
        ax.text(
            row["cagr"] + offset,
            row["category"],
            f"{row['cagr']:+.1f}%",
            ha="left" if row["cagr"] >= 0 else "right",
            va="center", fontsize=9,
            bbox={"boxstyle": "round,pad=0.15", "facecolor": "white", "alpha": 0.8, "edgecolor": "none"},
        )

    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title(f"Compound Annual Growth Rate by Crime Category ({start_yr}–{latest_yr})")
    add_subtitle(ax, f"Highest growth: {df.iloc[-1]['category']} at {df.iloc[-1]['cagr']:+.1f}% per year")
    ax.set_xlabel("CAGR (%)")
    style_axes(ax)
    ax.grid(axis="y", visible=False)

    narrative = (
        f"The 5-year CAGR reveals which crime categories are growing on a compounding basis. "
        f"Unlike absolute rate changes, CAGR normalizes for different base rates. "
        f"Source: Statistics Canada Table 35-10-0177-01."
    )

    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def find_fastest_changing() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return DataFrames of top 5 fastest-rising and top 5 fastest-declining violations."""
    bc = _load_bc_rates()
    rising, declining = _fastest_changing(bc, n=5, window_years=5)
    return rising, declining


def chart_specific_violation_trends(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Small multiples (2x4): top 8 specific violations by rate, trend over time."""
    apply_theme()
    bc = _load_bc_rates()

    # Exclude aggregate/total violations
    specific = bc[
        ~bc["violation"].str.startswith("Total")
        & ~bc["violation"].str.contains("all Criminal Code", case=False, na=False)
        & ~bc["violation"].str.contains("all violations", case=False, na=False)
    ].copy()

    if specific.empty:
        fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
        ax.text(0.5, 0.5, "Data unavailable", ha="center", va="center", transform=ax.transAxes)
        return fig, "Specific violation trend data unavailable."

    latest_year = int(specific["year"].max())
    latest_rates = specific[specific["year"] == latest_year].nlargest(8, "rate")
    top_violations = latest_rates["violation"].tolist()

    # Filter to year >= 2004 for the panels
    panel_data = specific[(specific["violation"].isin(top_violations)) & (specific["year"] >= 2004)]

    fig, axes = plt.subplots(2, 4, figsize=(16, 10), sharex=True)
    axes = axes.flatten()

    for i, viol in enumerate(top_violations):
        ax = axes[i]
        viol_data = panel_data[panel_data["violation"] == viol].sort_values("year")
        color = ORDERED[i % len(ORDERED)]
        ax.plot(viol_data["year"], viol_data["rate"], color=color, linewidth=2)
        ax.fill_between(viol_data["year"], viol_data["rate"], alpha=0.1, color=color)

        # Strip bracket codes from title
        clean_label = viol.split(" [")[0] if " [" in viol else viol
        ax.set_title(clean_label, fontsize=9, fontweight="bold")
        ax.xaxis.set_major_locator(mticker.MultipleLocator(5))
        style_axes(ax)
        annotate_events(ax)

    # Hide unused axes if fewer than 8
    for j in range(len(top_violations), len(axes)):
        axes[j].set_visible(False)

    fig.suptitle(
        f"Top 8 Specific Violations by Rate — Trend Over Time (2004–{latest_year})",
        fontsize=14, fontweight="bold", y=1.04,
    )
    add_fig_subtitle(fig, "Deep-dive into the 8 highest-rate specific violations")
    fig.supxlabel("Year")
    fig.supylabel("Rate per 100,000")
    fig.tight_layout(pad=2.0)
    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    top_names = [v.split(" [")[0] for v in top_violations[:3]]
    narrative = (
        f"The 8 highest-rate specific violations in {latest_year} are shown as individual panels. "
        f"{top_names[0]}, {top_names[1]}, and {top_names[2]} lead by rate. Each panel reveals "
        f"distinct trajectories — some declining steadily, others rebounding after 2014. "
        f"Source: Statistics Canada Table 35-10-0177-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_rising_violations_spotlight(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Multi-line chart: 5 fastest-growing specific violations, 2010–latest."""
    apply_theme()
    bc = _load_bc_rates()

    latest_year = int(bc["year"].max())
    start_year = latest_year - 5

    # Exclude aggregate/total violations
    specific = bc[
        ~bc["violation"].str.startswith("Total")
        & ~bc["violation"].str.contains("all Criminal Code", case=False, na=False)
        & ~bc["violation"].str.contains("all violations", case=False, na=False)
    ].copy()

    if specific.empty:
        fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
        ax.text(0.5, 0.5, "Data unavailable", ha="center", va="center", transform=ax.transAxes)
        return fig, "Rising violations data unavailable."

    # Compute 5-year growth rate for each specific violation
    growth_records = []
    for viol in specific["violation"].unique():
        v = specific[specific["violation"] == viol]
        s = v[v["year"] == start_year]
        e = v[v["year"] == latest_year]
        if s.empty or e.empty:
            continue
        rate_start = s["rate"].values[0]
        rate_end = e["rate"].values[0]
        if rate_start == 0:
            continue
        pct_chg = ((rate_end - rate_start) / rate_start) * 100
        growth_records.append({"violation": viol, "pct_change": pct_chg})

    if not growth_records:
        fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
        ax.text(0.5, 0.5, "Insufficient data for growth calculation",
                ha="center", va="center", transform=ax.transAxes)
        return fig, "Insufficient data to compute 5-year growth rates."

    df_growth = pd.DataFrame(growth_records)
    top5 = df_growth.nlargest(5, "pct_change")
    top5_violations = top5["violation"].tolist()

    # Chart data from 2010 onward
    chart_data = specific[
        (specific["violation"].isin(top5_violations)) & (specific["year"] >= 2010)
    ]

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    legend_labels = []
    for i, viol in enumerate(top5_violations):
        viol_data = chart_data[chart_data["violation"] == viol].sort_values("year")
        color = ORDERED[i % len(ORDERED)]
        clean_label = viol.split(" [")[0] if " [" in viol else viol
        ax.plot(viol_data["year"], viol_data["rate"], color=color, linewidth=2, label=clean_label)
        legend_labels.append(clean_label)

    annotate_events(ax)

    ax.set_title(f"Fastest-Rising Specific Violations in BC ({start_year}–{latest_year})")

    # Build data-driven subtitle from top 3 names
    subtitle_names = legend_labels[:3]
    subtitle_text = ", ".join(subtitle_names[:2]) + f", and {subtitle_names[2]} lead recent increases"
    add_subtitle(ax, subtitle_text)

    ax.set_xlabel("Year")
    ax.set_ylabel("Rate per 100,000")
    ax.legend(loc="upper left", fontsize=8)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    style_axes(ax)
    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    top_name = legend_labels[0]
    top_pct = top5.iloc[0]["pct_change"]
    narrative = (
        f"The 5 fastest-growing specific violations over {start_year}–{latest_year} are spotlighted. "
        f"{top_name} leads with a {top_pct:+.0f}% increase. These rising violations signal "
        f"emerging crime trends that may warrant targeted policy responses. "
        f"Source: Statistics Canada Table 35-10-0177-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


# ---------------------------------------------------------------------------
# Run all
# ---------------------------------------------------------------------------

def run_all() -> dict[str, str]:
    """Generate all Priority 4 charts and return narratives."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    narratives = {}

    charts = [
        ("q2_stacked_composition", chart_stacked_area),
        ("q2_heatmap", chart_heatmap),
        ("q2_top_changes", chart_top_changes),
        ("q2_slope_ranking", chart_slope),
        ("q2_composition_shares", chart_composition_shares),
        ("q2_category_cagr", chart_category_cagr),
        ("q2_specific_violation_trends", chart_specific_violation_trends),
        ("q2_rising_violations_spotlight", chart_rising_violations_spotlight),
    ]

    for name, fn in charts:
        path = CHARTS_DIR / f"{name}.png"
        logger.info("Generating %s ...", name)
        _, narrative = fn(save_path=path)
        narratives[name] = narrative
        logger.info("  Saved %s", path)

    # Top 5 rising / declining
    rising, declining = find_fastest_changing()
    logger.info("\nTop 5 fastest-rising violations (5-year % change):")
    for _, row in rising.iterrows():
        logger.info("  %s: %+.1f%%", row["violation"], row["pct_change"])
    logger.info("\nTop 5 fastest-declining violations (5-year % change):")
    for _, row in declining.iterrows():
        logger.info("  %s: %+.1f%%", row["violation"], row["pct_change"])

    narratives["fastest_rising"] = "\n".join(
        f"- {r['violation'].split(' [')[0]}: {r['pct_change']:+.1f}% ({r['start_year']}–{r['end_year']})"
        for _, r in rising.iterrows()
    )
    narratives["fastest_declining"] = "\n".join(
        f"- {r['violation'].split(' [')[0]}: {r['pct_change']:+.1f}% ({r['start_year']}–{r['end_year']})"
        for _, r in declining.iterrows()
    )

    return narratives


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
    narratives = run_all()
    print("\n" + "=" * 70)
    print("NARRATIVES")
    print("=" * 70)
    for name, text in narratives.items():
        print(f"\n### {name}\n{text}")
