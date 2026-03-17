"""Priority 5 — Justice System Effectiveness in BC

Analyzes clearance rates, youth vs adult crime severity, policing jurisdiction
trends, COVID impact, and unfounded rates. Produces charts and narrative.
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

from src.analysis.theme import (
    FIGSIZE_SINGLE,
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

# Five main crime categories used across charts
CATEGORIES = {
    "Violent crime": "Total violent Criminal Code violations [100]",
    "Property crime": "Total property crime violations [200]",
    "Administration of justice": "Total administration of justice violations [330]",
    "Other Criminal Code": "Total other Criminal Code violations [300]",
    "Drug offences": "Total drug violations [401]",
}


# ---------------------------------------------------------------------------
# Private data loaders
# ---------------------------------------------------------------------------

def _load_national_bc() -> pd.DataFrame:
    """Load BC rows from the national crime incidents parquet."""
    df = pd.read_parquet(PROCESSED_DIR / "crime_incidents_national.parquet")
    bc = df[df["geo"] == "British Columbia"].copy()
    return bc.reset_index(drop=True)


def _load_csi_bc() -> pd.DataFrame:
    """Load BC province-level rows from the crime severity parquet."""
    df = pd.read_parquet(PROCESSED_DIR / "crime_severity_bc.parquet")
    bc = df[df["geo"] == "British Columbia"].copy()
    return bc.reset_index(drop=True)


def _load_jurisdiction_trends() -> pd.DataFrame:
    """Load BC government jurisdiction trends parquet."""
    df = pd.read_parquet(PROCESSED_DIR / "bc_gov_jurisdiction_trends.parquet")
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Chart generators
# ---------------------------------------------------------------------------

def chart_clearance_rate_trends(
    save_path: Path | None = None,
) -> tuple[plt.Figure, str]:
    """Multi-line chart: clearance rate (%) by category over time, 2004-2024."""
    apply_theme()
    bc = _load_national_bc()

    # Compute clearance rate = Total cleared / Actual incidents * 100
    records = []
    for label, violation in CATEGORIES.items():
        cleared = bc[
            (bc["violation"] == violation) & (bc["statistic"] == "Total cleared")
        ][["year", "value"]].rename(columns={"value": "cleared"})
        actual = bc[
            (bc["violation"] == violation) & (bc["statistic"] == "Actual incidents")
        ][["year", "value"]].rename(columns={"value": "actual"})

        merged = cleared.merge(actual, on="year", how="inner")
        merged["clearance_rate"] = np.where(
            merged["actual"] > 0,
            merged["cleared"] / merged["actual"] * 100,
            np.nan,
        )
        merged["category"] = label
        records.append(merged[["year", "category", "clearance_rate"]])

    df = pd.concat(records, ignore_index=True)
    df = df[df["year"] >= 2004].sort_values(["category", "year"])

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    for i, label in enumerate(CATEGORIES):
        cat = df[df["category"] == label]
        ax.plot(
            cat["year"],
            cat["clearance_rate"],
            color=ORDERED[i],
            linewidth=2,
            label=label,
        )

    annotate_events(ax)

    # Data-driven subtitle
    latest_yr = int(df["year"].max())
    prop_rate = df.loc[
        (df["category"] == "Property crime") & (df["year"] == latest_yr),
        "clearance_rate",
    ]
    viol_rate = df.loc[
        (df["category"] == "Violent crime") & (df["year"] == latest_yr),
        "clearance_rate",
    ]
    prop_val = prop_rate.values[0] if len(prop_rate) else 0
    viol_val = viol_rate.values[0] if len(viol_rate) else 0
    subtitle = (
        f"Property crime clearance is {prop_val:.0f}% while "
        f"violent crime exceeds {viol_val:.0f}% ({latest_yr})"
    )
    add_subtitle(ax, subtitle)

    ax.set_title(
        f"BC Clearance Rate by Crime Category (2004–{latest_yr})",
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Clearance Rate (%)")
    ax.legend(loc="upper right", fontsize=9)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    style_axes(ax)
    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    # Narrative
    overall_rates = (
        df[df["year"] == latest_yr]
        .set_index("category")["clearance_rate"]
    )
    highest_cat = overall_rates.idxmax()
    highest_val = overall_rates.max()
    lowest_cat = overall_rates.idxmin()
    lowest_val = overall_rates.min()

    narrative = (
        f"In {latest_yr}, {highest_cat.lower()} had the highest clearance rate at "
        f"{highest_val:.1f}%, while {lowest_cat.lower()} had the lowest at "
        f"{lowest_val:.1f}%. Clearance rates measure the proportion of reported crimes "
        f"that police resolve through charges or other means. "
        f"Source: Statistics Canada Table 35-10-0177-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_clearance_by_violation(
    save_path: Path | None = None,
) -> tuple[plt.Figure, str]:
    """Horizontal bar chart: clearance rate for top 10 violations by incident count."""
    apply_theme()
    bc = _load_national_bc()

    latest_yr = int(bc["year"].max())
    latest = bc[bc["year"] == latest_yr]

    # Get actual incidents for all violations in the latest year
    actual = latest[latest["statistic"] == "Actual incidents"][
        ["violation", "value"]
    ].rename(columns={"value": "actual"})
    cleared = latest[latest["statistic"] == "Total cleared"][
        ["violation", "value"]
    ].rename(columns={"value": "cleared"})

    merged = actual.merge(cleared, on="violation", how="inner")
    # Drop aggregate totals
    merged = merged[
        ~merged["violation"].str.startswith("Total,")
        & ~merged["violation"].str.startswith("Total ")
    ]
    merged = merged[merged["actual"] > 0]

    # Top 10 by incident count
    top10 = merged.nlargest(10, "actual").copy()
    top10["clearance_rate"] = top10["cleared"] / top10["actual"] * 100
    top10["label"] = top10["violation"].str.replace(
        r"\s*\[\d+\]", "", regex=True,
    )
    top10 = top10.sort_values("clearance_rate")

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    # Color gradient: green (high clearance) to red (low clearance)
    max_rate = top10["clearance_rate"].max()
    min_rate = top10["clearance_rate"].min()
    rate_range = max_rate - min_rate if max_rate != min_rate else 1
    colors = []
    for rate in top10["clearance_rate"]:
        fraction = (rate - min_rate) / rate_range
        # Interpolate between bc_red (low) and bc_teal (high)
        r_low = int(PALETTE["bc_red"][1:3], 16)
        g_low = int(PALETTE["bc_red"][3:5], 16)
        b_low = int(PALETTE["bc_red"][5:7], 16)
        r_high = int(PALETTE["bc_teal"][1:3], 16)
        g_high = int(PALETTE["bc_teal"][3:5], 16)
        b_high = int(PALETTE["bc_teal"][5:7], 16)
        r = int(r_low + (r_high - r_low) * fraction)
        g = int(g_low + (g_high - g_low) * fraction)
        b = int(b_low + (b_high - b_low) * fraction)
        colors.append(f"#{r:02x}{g:02x}{b:02x}")

    bars = ax.barh(top10["label"], top10["clearance_rate"], color=colors, edgecolor="white")

    for bar, val in zip(bars, top10["clearance_rate"]):
        ax.text(
            bar.get_width() + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.0f}%",
            ha="left",
            va="center",
            fontsize=9,
        )

    median_rate = top10["clearance_rate"].median()
    add_subtitle(ax, f"Median clearance rate among top 10 violations: {median_rate:.0f}%")

    ax.set_title(f"Clearance Rate by Violation Type — Top 10 by Volume ({latest_yr})")
    ax.set_xlabel("Clearance Rate (%)")
    style_axes(ax)
    ax.grid(axis="y", visible=False)
    fig.subplots_adjust(left=0.30)
    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    # Narrative
    highest = top10.iloc[-1]
    lowest = top10.iloc[0]
    narrative = (
        f"Among the 10 highest-volume violations in {latest_yr}, "
        f"{highest['label']} had the highest clearance rate at {highest['clearance_rate']:.0f}%, "
        f"while {lowest['label']} had the lowest at {lowest['clearance_rate']:.0f}%. "
        f"The median clearance rate across these violations was {median_rate:.0f}%. "
        f"Source: Statistics Canada Table 35-10-0177-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_youth_vs_adult_csi(
    save_path: Path | None = None,
) -> tuple[plt.Figure, str]:
    """Dual-line chart: youth vs adult Crime Severity Index, 2004-2024."""
    apply_theme()
    csi = _load_csi_bc()

    adult = csi[csi["statistic"] == "Crime severity index"][
        ["year", "value"]
    ].rename(columns={"value": "adult_csi"})
    youth = csi[csi["statistic"] == "Youth crime severity index"][
        ["year", "value"]
    ].rename(columns={"value": "youth_csi"})

    merged = adult.merge(youth, on="year", how="inner")
    merged = merged[merged["year"] >= 2004].sort_values("year").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    ax.plot(
        merged["year"],
        merged["adult_csi"],
        color=PALETTE["bc_blue"],
        linewidth=2.5,
        label="Overall CSI",
        marker="o",
        markersize=4,
    )
    ax.plot(
        merged["year"],
        merged["youth_csi"],
        color=PALETTE["bc_amber"],
        linewidth=2.5,
        label="Youth CSI",
        marker="s",
        markersize=4,
    )

    annotate_events(ax)

    # Data-driven subtitle
    latest_yr = int(merged["year"].max())
    latest_adult = merged.loc[merged["year"] == latest_yr, "adult_csi"].values[0]
    latest_youth = merged.loc[merged["year"] == latest_yr, "youth_csi"].values[0]
    gap = latest_adult - latest_youth
    add_subtitle(
        ax,
        f"Overall CSI is {gap:.0f} points above youth CSI in {latest_yr}",
    )

    ax.set_title(f"Youth vs Overall Crime Severity Index — BC (2004–{latest_yr})")
    ax.set_xlabel("Year")
    ax.set_ylabel("Crime Severity Index")
    ax.legend(loc="upper right", fontsize=10)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    style_axes(ax)
    add_source(fig, "Source: Statistics Canada, Table 35-10-0063-01")

    # Narrative
    peak_youth_yr = int(merged.loc[merged["youth_csi"].idxmax(), "year"])
    peak_youth_val = merged["youth_csi"].max()
    narrative = (
        f"Youth CSI peaked at {peak_youth_val:.1f} in {peak_youth_yr} and has since declined to "
        f"{latest_youth:.1f} in {latest_yr}, while the overall CSI sits at {latest_adult:.1f}. "
        f"The divergence suggests youth crime severity is falling even as overall severity rises. "
        f"Source: Statistics Canada Table 35-10-0063-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_rcmp_vs_municipal(
    save_path: Path | None = None,
) -> tuple[plt.Figure, str]:
    """Multi-line chart: total crime count by policing type, 2014-2023."""
    apply_theme()
    jur = _load_jurisdiction_trends()

    # Filter to Criminal Code Offences and the 3 main policing types
    target_types = ["Independent Municipal", "RCMP Provincial", "RCMP Municipal"]
    mask = (
        (jur["category"] == "Criminal Code Offences")
        & (jur["type_of_policing"].isin(target_types))
    )
    subset = jur[mask].copy()

    # Group by type and year, sum counts across jurisdictions
    grouped = (
        subset.groupby(["type_of_policing", "year"], as_index=False)["count"]
        .sum()
        .sort_values(["type_of_policing", "year"])
    )

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    color_map = {
        "Independent Municipal": PALETTE["bc_blue"],
        "RCMP Provincial": PALETTE["bc_red"],
        "RCMP Municipal": PALETTE["bc_teal"],
    }

    for ptype in target_types:
        pdata = grouped[grouped["type_of_policing"] == ptype]
        ax.plot(
            pdata["year"],
            pdata["count"],
            color=color_map[ptype],
            linewidth=2,
            label=ptype,
            marker="o",
            markersize=4,
        )

    # Data-driven subtitle
    latest_yr = int(grouped["year"].max())
    latest_totals = grouped[grouped["year"] == latest_yr].set_index("type_of_policing")["count"]
    largest_type = latest_totals.idxmax()
    largest_count = latest_totals.max()
    add_subtitle(
        ax,
        f"{largest_type} jurisdictions recorded the most offences "
        f"({largest_count:,.0f}) in {latest_yr}",
    )

    ax.set_title(
        f"Criminal Code Offences by Policing Type — BC ({int(grouped['year'].min())}–{latest_yr})",
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Criminal Code Offences")
    ax.legend(loc="upper right", fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
    style_axes(ax)
    add_source(fig, "Source: BC Government, Police Resources in British Columbia")

    # Narrative
    first_yr = int(grouped["year"].min())
    first_totals = grouped[grouped["year"] == first_yr].set_index("type_of_policing")["count"]
    total_first = first_totals.sum()
    total_latest = latest_totals.sum()
    overall_change = ((total_latest - total_first) / total_first) * 100 if total_first > 0 else 0

    narrative = (
        f"From {first_yr} to {latest_yr}, total Criminal Code offences across BC's three "
        f"main policing types changed by {overall_change:+.1f}%. "
        f"In {latest_yr}, {largest_type} jurisdictions handled {largest_count:,.0f} offences, "
        f"the highest among the three types. "
        f"Source: BC Government, Police Resources in British Columbia."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_covid_impact(
    save_path: Path | None = None,
) -> tuple[plt.Figure, str]:
    """Grouped bar chart: crime rate per 100k for 5 categories across 2019, 2021, 2024."""
    apply_theme()
    bc = _load_national_bc()

    comparison_years = [2019, 2021, 2024]
    year_colors = {
        2019: PALETTE["bc_blue"],
        2021: PALETTE["bc_red"],
        2024: PALETTE["bc_teal"],
    }

    # Collect rates for each category and year
    records = []
    for label, violation in CATEGORIES.items():
        for yr in comparison_years:
            row = bc[
                (bc["violation"] == violation)
                & (bc["statistic"] == "Rate per 100,000 population")
                & (bc["year"] == yr)
            ]
            rate = row["value"].values[0] if len(row) else np.nan
            records.append({"category": label, "year": yr, "rate": rate})

    df = pd.DataFrame(records)

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    category_labels = list(CATEGORIES.keys())
    n_years = len(comparison_years)
    bar_height = 0.25
    y_positions = np.arange(len(category_labels))

    for i, yr in enumerate(comparison_years):
        yr_data = df[df["year"] == yr].set_index("category").reindex(category_labels)
        offset = (i - n_years / 2 + 0.5) * bar_height
        bars = ax.barh(
            y_positions + offset,
            yr_data["rate"],
            height=bar_height,
            color=year_colors[yr],
            label=str(yr),
            edgecolor="white",
        )
        for bar, val in zip(bars, yr_data["rate"]):
            if not np.isnan(val):
                ax.text(
                    bar.get_width() + 5,
                    bar.get_y() + bar.get_height() / 2,
                    f"{val:,.0f}",
                    ha="left",
                    va="center",
                    fontsize=8,
                )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(category_labels)
    ax.set_xlabel("Rate per 100,000 Population")
    ax.set_title("COVID Impact on BC Crime Rates — 2019 vs 2021 vs 2024")
    ax.legend(loc="lower right", fontsize=10)
    style_axes(ax)
    ax.grid(axis="y", visible=False)
    fig.subplots_adjust(left=0.22)

    # Data-driven subtitle
    prop_2019 = df.loc[
        (df["category"] == "Property crime") & (df["year"] == 2019), "rate"
    ]
    prop_2024 = df.loc[
        (df["category"] == "Property crime") & (df["year"] == 2024), "rate"
    ]
    p19 = prop_2019.values[0] if len(prop_2019) else 0
    p24 = prop_2024.values[0] if len(prop_2024) else 0
    prop_chg = ((p24 - p19) / p19 * 100) if p19 > 0 else 0
    add_subtitle(
        ax,
        f"Property crime rate changed {prop_chg:+.0f}% from pre-COVID 2019 to 2024",
    )

    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    # Narrative
    narrative_parts = []
    for label in category_labels:
        r19 = df.loc[(df["category"] == label) & (df["year"] == 2019), "rate"]
        r24 = df.loc[(df["category"] == label) & (df["year"] == 2024), "rate"]
        if len(r19) and len(r24) and r19.values[0] > 0:
            chg = ((r24.values[0] - r19.values[0]) / r19.values[0]) * 100
            narrative_parts.append(f"{label.lower()} {chg:+.0f}%")

    changes_str = ", ".join(narrative_parts) if narrative_parts else "no data"
    narrative = (
        f"Comparing pre-COVID 2019 to post-pandemic 2024, BC crime rate changes by category: "
        f"{changes_str}. The mid-pandemic year 2021 shows the initial shock, with some categories "
        f"dipping before rebounding. Source: Statistics Canada Table 35-10-0177-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_unfounded_rates(
    save_path: Path | None = None,
) -> tuple[plt.Figure, str]:
    """Multi-line chart: percent unfounded by category, 2004-2024."""
    apply_theme()
    bc = _load_national_bc()

    records = []
    for label, violation in CATEGORIES.items():
        unfounded = bc[
            (bc["violation"] == violation)
            & (bc["statistic"] == "Percent unfounded")
        ][["year", "value"]].copy()
        unfounded = unfounded.rename(columns={"value": "pct_unfounded"})
        unfounded["category"] = label
        records.append(unfounded)

    df = pd.concat(records, ignore_index=True)
    df = df[df["year"] >= 2004].sort_values(["category", "year"])

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    for i, label in enumerate(CATEGORIES):
        cat = df[df["category"] == label]
        ax.plot(
            cat["year"],
            cat["pct_unfounded"],
            color=ORDERED[i],
            linewidth=2,
            label=label,
        )

    annotate_events(ax)

    # Data-driven subtitle
    latest_yr = int(df["year"].max())
    latest_rates = df[df["year"] == latest_yr].set_index("category")["pct_unfounded"]
    highest_cat = latest_rates.idxmax() if not latest_rates.empty else "N/A"
    highest_val = latest_rates.max() if not latest_rates.empty else 0
    add_subtitle(
        ax,
        f"{highest_cat} has the highest unfounded rate at {highest_val:.1f}% in {latest_yr}",
    )

    ax.set_title(f"Percent Unfounded by Crime Category — BC (2004–{latest_yr})")
    ax.set_xlabel("Year")
    ax.set_ylabel("Percent Unfounded (%)")
    ax.legend(loc="upper right", fontsize=9)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    style_axes(ax)
    add_source(fig, "Source: Statistics Canada, Table 35-10-0177-01")

    # Narrative
    mean_unfounded = latest_rates.mean() if not latest_rates.empty else 0
    narrative = (
        f"In {latest_yr}, the average unfounded rate across the five categories was "
        f"{mean_unfounded:.1f}%. {highest_cat} had the highest unfounded rate at "
        f"{highest_val:.1f}%, meaning that proportion of reports were determined to have "
        f"not occurred or did not constitute a criminal offence. "
        f"Source: Statistics Canada Table 35-10-0177-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


# ---------------------------------------------------------------------------
# Underreporting hypothesis
# ---------------------------------------------------------------------------

# Specific violations to track in underreporting proxy analysis
_PROXY_VIOLATIONS = {
    "Sexual assault": "Sexual assault, level 1 [1330]",
    "Assault": "Assault, level 1 [1430]",
    "Theft under $5k": "Total theft under $5,000 (non-motor vehicle) [240]",
    "Breaking & entering": "Total breaking and entering [210]",
    "Mischief": "Total mischief [250]",
}


def chart_underreporting_proxies(
    save_path: Path | None = None,
) -> tuple[plt.Figure, str]:
    """2x2 dashboard exploring whether underreporting explains crime declines.

    Panels:
    1. Unfounded rates for specific violations over time
    2. Clearance method shift (charge vs otherwise) over time
    3. Property vs violent rate trajectories indexed to 2004=100
    4. Text panel with GSS victimization context
    """
    apply_theme()
    bc = _load_national_bc()
    bc = bc[bc["year"] >= 2004]

    fig, axes = plt.subplots(2, 2, figsize=FIGSIZE_WIDE)

    # --- Panel 1: Unfounded rates for specific violations ---
    ax1 = axes[0, 0]
    for i, (label, violation) in enumerate(_PROXY_VIOLATIONS.items()):
        unfounded = bc[
            (bc["violation"] == violation)
            & (bc["statistic"] == "Percent unfounded")
        ][["year", "value"]].sort_values("year")
        if not unfounded.empty:
            ax1.plot(
                unfounded["year"], unfounded["value"],
                color=ORDERED[i], linewidth=1.8, label=label,
            )

    ax1.set_title("Unfounded Rates by Violation Type", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Percent Unfounded (%)")
    ax1.legend(fontsize=7, loc="upper right")
    ax1.xaxis.set_major_locator(mticker.MultipleLocator(4))
    style_axes(ax1)

    # --- Panel 2: Clearance method shift ---
    ax2 = axes[0, 1]
    total_violation = "Total, all Criminal Code violations (excluding traffic) [50]"
    charged = bc[
        (bc["violation"] == total_violation)
        & (bc["statistic"] == "Cleared by charge")
    ][["year", "value"]].rename(columns={"value": "by_charge"}).sort_values("year")
    otherwise = bc[
        (bc["violation"] == total_violation)
        & (bc["statistic"] == "Cleared otherwise")
    ][["year", "value"]].rename(columns={"value": "otherwise"}).sort_values("year")

    if not charged.empty and not otherwise.empty:
        merged = charged.merge(otherwise, on="year", how="inner")
        merged["total_cleared"] = merged["by_charge"] + merged["otherwise"]
        merged["charge_share"] = np.where(
            merged["total_cleared"] > 0,
            merged["by_charge"] / merged["total_cleared"] * 100,
            np.nan,
        )
        merged["otherwise_share"] = np.where(
            merged["total_cleared"] > 0,
            merged["otherwise"] / merged["total_cleared"] * 100,
            np.nan,
        )
        ax2.stackplot(
            merged["year"],
            [merged["charge_share"].values, merged["otherwise_share"].values],
            labels=["Cleared by charge", "Cleared otherwise"],
            colors=[PALETTE["bc_blue"], PALETTE["bc_amber"]],
            alpha=0.8,
        )
        ax2.set_ylim(0, 100)
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))

    ax2.set_title("Clearance Method: Charge vs Otherwise", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Share of Cleared Cases (%)")
    ax2.legend(fontsize=8, loc="lower right")
    ax2.xaxis.set_major_locator(mticker.MultipleLocator(4))
    style_axes(ax2)

    # --- Panel 3: Property vs violent indexed to 2004 = 100 ---
    ax3 = axes[1, 0]
    cat_violations = {
        "Property crime": "Total property crime violations [200]",
        "Violent crime": "Total violent Criminal Code violations [100]",
    }
    cat_colors = {
        "Property crime": PALETTE["bc_teal"],
        "Violent crime": PALETTE["bc_red"],
    }
    for label, violation in cat_violations.items():
        rates = bc[
            (bc["violation"] == violation)
            & (bc["statistic"] == "Rate per 100,000 population")
        ][["year", "value"]].sort_values("year")
        if not rates.empty:
            base_val = rates["value"].iloc[0]
            if base_val > 0:
                indexed = rates["value"] / base_val * 100
                ax3.plot(
                    rates["year"], indexed,
                    color=cat_colors[label], linewidth=2, label=label,
                )

    ax3.axhline(100, color=PALETTE["light_grey"], linewidth=1, linestyle=":")
    ax3.set_title("Property vs Violent Rate (indexed 2004 = 100)", fontsize=11, fontweight="bold")
    ax3.set_xlabel("Year")
    ax3.set_ylabel("Index (2004 = 100)")
    ax3.legend(fontsize=9, loc="upper right")
    ax3.xaxis.set_major_locator(mticker.MultipleLocator(4))
    style_axes(ax3)
    ax3.annotate(
        "Real decline\nor reporting\ndecline?",
        xy=(2018, 60), fontsize=9, color=PALETTE["bc_slate"],
        style="italic", ha="center",
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "#f9f9f9", "edgecolor": PALETTE["bc_slate"], "alpha": 0.9},
    )

    # --- Panel 4: GSS context text ---
    ax4 = axes[1, 1]
    ax4.axis("off")

    gss_text = (
        "The Reporting Gap\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Statistics Canada's General Social\n"
        "Survey on Victimization (2019) found:\n\n"
        "  Overall:  only 29% of criminal\n"
        "            victimizations reported\n\n"
        "  Property crime:      ~35%\n"
        "  Violent crime:       ~24%\n"
        "  Sexual assault:       ~6%\n\n"
        "If reporting rates are declining,\n"
        "police-reported crime falls even\n"
        "when actual crime is stable.\n\n"
        "Source: Statistics Canada, GSS on\n"
        "Canadians' Safety, 2019 (Catalogue\n"
        "no. 85-002-X)"
    )

    ax4.text(
        0.08, 0.95, gss_text,
        transform=ax4.transAxes,
        fontsize=9, fontfamily="monospace",
        color=PALETTE["bc_blue"],
        va="top", ha="left",
        bbox={"boxstyle": "round,pad=0.6", "facecolor": "#f0f4f8", "edgecolor": PALETTE["bc_blue"], "alpha": 0.3},
    )

    fig.suptitle(
        "Could Underreporting Explain the Crime Decline?",
        fontsize=14, fontweight="bold", y=1.04,
    )
    add_fig_subtitle(
        fig,
        "Proxy indicators from police data, alongside victimization survey context",
    )
    fig.tight_layout(pad=2.0)
    add_source(fig, "Source: Statistics Canada, Tables 35-10-0177-01 and 35-10-0063-01; GSS 2019")

    # Narrative
    narrative = (
        "This dashboard explores whether declining crime rates may partly reflect "
        "changes in reporting behaviour rather than genuine crime reduction. "
        "Panel 1 shows unfounded rates for specific violations — if police are "
        "dismissing more reports, it inflates the apparent decline. "
        "Panel 2 tracks whether cases are increasingly 'cleared otherwise' "
        "(e.g., victim declines to proceed) rather than cleared by charge. "
        "Panel 3 contrasts property and violent crime trajectories — property "
        "crime (higher reporting sensitivity) has declined more steeply. "
        "The GSS context (Panel 4) reveals that only 29% of victimizations are "
        "reported to police, with sexual assault at just 6%. These proxy indicators "
        "suggest underreporting likely explains some of the property crime decline "
        "but cannot account for violent crime trends, which are less sensitive to "
        "reporting behaviour. "
        "Source: Statistics Canada Tables 35-10-0177-01, 35-10-0063-01; GSS 2019."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


# ---------------------------------------------------------------------------
# Run all
# ---------------------------------------------------------------------------

def run_all() -> dict[str, str]:
    """Generate all Justice System Effectiveness charts and return narratives."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    narratives = {}

    charts = [
        ("q3_clearance_rate_trends", chart_clearance_rate_trends),
        ("q3_clearance_by_violation", chart_clearance_by_violation),
        ("q3_youth_vs_adult_csi", chart_youth_vs_adult_csi),
        ("q3_rcmp_vs_municipal", chart_rcmp_vs_municipal),
        ("q3_covid_impact", chart_covid_impact),
        ("q3_unfounded_rates", chart_unfounded_rates),
        ("q3_underreporting_proxies", chart_underreporting_proxies),
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
