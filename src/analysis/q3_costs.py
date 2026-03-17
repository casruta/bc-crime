"""Priority 5 — Policing Expenditure and Costs.

Analyzes BC policing expenditure trends (nominal and CPI-adjusted),
compares per-capita policing costs across provinces, overlays CSI
against per-capita spending, and shows Canada-level expenditure
breakdown by category. Produces four charts with narratives.

Data sources:
    - 35-10-0076-01  Police personnel and selected crime statistics
    - 35-10-0059-01  Police services expenditures (Canada only)
    - CPI parquet     Consumer Price Index (2002=100 base)
    - CSI parquet     Crime Severity Index for overlay
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

from src.paths import CHARTS_DIR, PROCESSED_DIR, RAW_STATSCAN_DIR

logger = logging.getLogger(__name__)

CPI_BASE_YEAR = 2020
COMPARISON_PROVINCES = [
    "British Columbia",
    "Canada",
    "Alberta",
    "Ontario",
    "Saskatchewan",
    "Manitoba",
    "Quebec",
    "Nova Scotia",
    "New Brunswick",
    "Newfoundland and Labrador",
]

# Top-level expenditure categories for stacked bar
EXPENDITURE_CATEGORIES = [
    "Total salaries, wages and benefits",
    "Total non-salary operating expenditures",
    "Total capital expenditures",
]

EXPENDITURE_LABELS = {
    "Total salaries, wages and benefits": "Salaries & Benefits",
    "Total non-salary operating expenditures": "Operating (non-salary)",
    "Total capital expenditures": "Capital",
}


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------


def _load_cpi() -> pd.DataFrame:
    """Load Canada CPI and compute a deflator to constant 2020 dollars.

    Returns a DataFrame with columns: year, cpi, deflator.
    Multiply a nominal value by ``deflator`` to get constant 2020 dollars.
    """
    cpi = pd.read_parquet(PROCESSED_DIR / "cpi.parquet")
    cpi_canada = cpi[cpi["geo"] == "Canada"][["year", "cpi"]].copy()
    cpi_canada = cpi_canada.sort_values("year").reset_index(drop=True)

    base_cpi = cpi_canada.loc[cpi_canada["year"] == CPI_BASE_YEAR, "cpi"]
    if base_cpi.empty:
        logger.warning("CPI for base year %d not found; deflation disabled", CPI_BASE_YEAR)
        cpi_canada["deflator"] = 1.0
    else:
        cpi_canada["deflator"] = base_cpi.values[0] / cpi_canada["cpi"]

    return cpi_canada


def _load_police_personnel() -> pd.DataFrame:
    """Load and clean the 35-10-0076-01 police personnel table.

    Returns long-form DataFrame with columns:
        year, geo, statistic, value, uom, scalar_factor
    """
    path = RAW_STATSCAN_DIR / "35100076.csv"
    df = pd.read_csv(path, dtype=str, encoding="utf-8")

    df = df.rename(columns={
        "REF_DATE": "year",
        "GEO": "geo",
        "Statistics": "statistic",
        "VALUE": "value",
        "UOM": "uom",
        "SCALAR_FACTOR": "scalar_factor",
    })

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["year", "value"])
    df["year"] = df["year"].astype(int)

    # Strip geographic codes from GEO names
    df["geo"] = df["geo"].str.replace(r"\s*\[\d+\]", "", regex=True).str.strip()

    return df[["year", "geo", "statistic", "value", "uom", "scalar_factor"]].reset_index(drop=True)


def _load_expenditure_breakdown() -> pd.DataFrame:
    """Load the 35-10-0059-01 police expenditure breakdown (Canada only).

    Returns DataFrame with columns: year, category, value_thousands.
    Values are in thousands of current dollars.
    """
    path = RAW_STATSCAN_DIR / "35100059.csv"
    df = pd.read_csv(path, dtype=str, encoding="utf-8")

    df = df.rename(columns={
        "REF_DATE": "year",
        "Expenditures": "category",
        "VALUE": "value",
    })

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["year", "value"])
    df["year"] = df["year"].astype(int)

    return df[["year", "category", "value"]].reset_index(drop=True)


def _bc_expenditure_with_cpi() -> pd.DataFrame:
    """BC total policing expenditure in nominal and constant 2020 dollars.

    The 35-10-0076 table stores expenditures in thousands of dollars.
    Returns DataFrame: year, nominal_millions, real_millions.
    """
    pp = _load_police_personnel()
    cpi = _load_cpi()

    bc_exp = pp[
        (pp["geo"] == "British Columbia")
        & (pp["statistic"] == "Total expenditures on policing")
    ][["year", "value"]].copy()

    # value is in thousands of dollars; convert to millions
    bc_exp["nominal_millions"] = bc_exp["value"] / 1000.0
    bc_exp = bc_exp.merge(cpi[["year", "deflator"]], on="year", how="left")
    bc_exp["real_millions"] = bc_exp["nominal_millions"] * bc_exp["deflator"]
    bc_exp = bc_exp.sort_values("year").reset_index(drop=True)

    return bc_exp[["year", "nominal_millions", "real_millions"]]


def _per_capita_by_province() -> pd.DataFrame:
    """Per-capita policing cost for all provinces from the personnel table.

    Returns DataFrame: year, geo, per_capita (nominal dollars).
    """
    pp = _load_police_personnel()
    pc = pp[pp["statistic"] == "Per capita cost"][["year", "geo", "value"]].copy()
    pc = pc.rename(columns={"value": "per_capita"})
    pc = pc.sort_values(["geo", "year"]).reset_index(drop=True)
    return pc


def _csi_for_overlay() -> pd.DataFrame:
    """Load province-level Crime Severity Index for BC from the CSI parquet.

    Returns DataFrame: year, csi.
    """
    df = pd.read_parquet(PROCESSED_DIR / "crime_severity_bc.parquet")
    bc = df[
        (df["geo"] == "British Columbia")
        & (df["statistic"] == "Crime severity index")
    ][["year", "value"]].copy()
    bc = bc.rename(columns={"value": "csi"})
    bc = bc.dropna(subset=["csi"]).sort_values("year").reset_index(drop=True)
    return bc


# ---------------------------------------------------------------------------
# Chart generators
# ---------------------------------------------------------------------------


def chart_bc_expenditure_trend(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Line chart: BC total policing expenditure — nominal vs inflation-adjusted."""
    apply_theme()
    data = _bc_expenditure_with_cpi()

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        data["year"], data["nominal_millions"],
        color=PALETTE["bc_slate"], linewidth=2, linestyle="--",
        label="Nominal dollars",
    )
    ax.plot(
        data["year"], data["real_millions"],
        color=PALETTE["bc_blue"], linewidth=2.5,
        label=f"Constant {CPI_BASE_YEAR} dollars",
    )

    ax.fill_between(
        data["year"], data["real_millions"], data["nominal_millions"],
        alpha=0.12, color=PALETTE["bc_amber"], label="Inflation gap",
    )

    ax.set_title(f"BC Total Policing Expenditure ({int(data['year'].min())}–{int(data['year'].max())})")
    ax.set_xlabel("Year")
    ax.set_ylabel("Expenditure ($ millions)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}M"))
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.legend(loc="upper left")
    style_axes(ax)

    # Narrative
    first_yr = int(data["year"].iloc[0])
    last_yr = int(data["year"].iloc[-1])
    nom_start = data["nominal_millions"].iloc[0]
    nom_end = data["nominal_millions"].iloc[-1]
    real_start = data["real_millions"].iloc[0]
    real_end = data["real_millions"].iloc[-1]
    nom_growth = ((nom_end / nom_start) - 1) * 100
    real_growth = ((real_end / real_start) - 1) * 100

    narrative = (
        f"BC's policing expenditure grew from ${nom_start:,.0f}M to ${nom_end:,.0f}M "
        f"in nominal terms ({nom_growth:+.0f}%) between {first_yr} and {last_yr}. "
        f"Adjusted to constant {CPI_BASE_YEAR} dollars, spending rose from "
        f"${real_start:,.0f}M to ${real_end:,.0f}M ({real_growth:+.0f}%), showing that "
        f"real policing costs roughly {'doubled' if real_growth > 80 else 'increased substantially'} "
        f"even after removing inflation. "
        f"Source: Statistics Canada Table 35-10-0076-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_per_capita_comparison(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Bar chart: per-capita policing cost by province (latest available year)."""
    apply_theme()
    data = _per_capita_by_province()

    # Filter to comparison provinces and latest year
    data = data[data["geo"].isin(COMPARISON_PROVINCES)]
    latest_yr = int(data["year"].max())
    latest = data[data["year"] == latest_yr].copy()

    # Exclude territories and RCMP HQ for cleaner comparison
    latest = latest[latest["geo"].isin(COMPARISON_PROVINCES)]
    latest = latest.sort_values("per_capita", ascending=True).reset_index(drop=True)

    if latest.empty:
        logger.warning("No per-capita data found for comparison provinces")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, "No data available", ha="center", va="center", transform=ax.transAxes)
        return fig, "No per-capita comparison data available."

    fig, ax = plt.subplots(figsize=(11, 6))

    colors = [
        PROVINCE_COLOURS.get(g, PALETTE["light_grey"]) if g in PROVINCE_COLOURS
        else PALETTE["light_grey"]
        for g in latest["geo"]
    ]
    bars = ax.barh(latest["geo"], latest["per_capita"], color=colors, edgecolor="white")

    # Value labels
    for bar, val in zip(bars, latest["per_capita"]):
        ax.text(
            bar.get_width() + 3,
            bar.get_y() + bar.get_height() / 2,
            f"${val:,.0f}",
            ha="left", va="center", fontsize=10,
            fontweight="bold" if bar.get_facecolor()[:3] == tuple(
                int(PALETTE["bc_blue"][i:i + 2], 16) / 255 for i in (1, 3, 5)
            ) else "normal",
        )

    ax.set_title(f"Per-Capita Policing Cost by Province ({latest_yr})")
    ax.set_xlabel("Per-Capita Cost (nominal dollars)")
    style_axes(ax)
    ax.grid(axis="y", visible=False)

    # Narrative
    bc_cost = latest.loc[latest["geo"] == "British Columbia", "per_capita"]
    ca_cost = latest.loc[latest["geo"] == "Canada", "per_capita"]
    bc_val = bc_cost.values[0] if len(bc_cost) else 0
    ca_val = ca_cost.values[0] if len(ca_cost) else 0

    # Find highest province (excluding Canada aggregate)
    prov_only = latest[latest["geo"] != "Canada"]
    highest_prov = prov_only.iloc[-1]["geo"] if len(prov_only) else "N/A"
    highest_val = prov_only.iloc[-1]["per_capita"] if len(prov_only) else 0

    narrative = (
        f"In {latest_yr}, BC's per-capita policing cost was ${bc_val:,.0f}, "
        f"compared to the national average of ${ca_val:,.0f} "
        f"({((bc_val / ca_val - 1) * 100):+.0f}% vs Canada). "
        f"The Canada-wide figure is higher because it includes RCMP headquarters "
        f"and federal policing costs distributed nationally. "
        f"Among provinces, {highest_prov} had the highest per-capita cost at ${highest_val:,.0f}. "
        f"Source: Statistics Canada Table 35-10-0076-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_csi_vs_expenditure(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Indexed line chart: CSI trend vs per-capita expenditure over time.

    Both series are indexed to 100 at their first overlapping year for
    comparison of relative trajectories.
    """
    apply_theme()
    csi = _csi_for_overlay()
    pc = _per_capita_by_province()
    cpi = _load_cpi()

    # BC per-capita cost, adjusted to real dollars
    bc_pc = pc[pc["geo"] == "British Columbia"][["year", "per_capita"]].copy()
    bc_pc = bc_pc.merge(cpi[["year", "deflator"]], on="year", how="left")
    bc_pc["per_capita_real"] = bc_pc["per_capita"] * bc_pc["deflator"]

    # Merge on overlapping years
    merged = csi.merge(bc_pc[["year", "per_capita_real"]], on="year", how="inner")
    merged = merged.sort_values("year").reset_index(drop=True)

    if merged.empty:
        logger.warning("No overlapping years between CSI and per-capita data")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, "No overlapping data", ha="center", va="center", transform=ax.transAxes)
        return fig, "No overlapping years between CSI and per-capita expenditure data."

    # Index to 100 at the first year
    base_csi = merged["csi"].iloc[0]
    base_pc = merged["per_capita_real"].iloc[0]
    merged["csi_indexed"] = (merged["csi"] / base_csi) * 100
    merged["pc_indexed"] = (merged["per_capita_real"] / base_pc) * 100

    base_year = int(merged["year"].iloc[0])
    last_year = int(merged["year"].iloc[-1])

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        merged["year"], merged["csi_indexed"],
        color=PALETTE["bc_red"], linewidth=2.5,
        label="Crime Severity Index",
        marker="o", markersize=4,
    )
    ax.plot(
        merged["year"], merged["pc_indexed"],
        color=PALETTE["bc_blue"], linewidth=2.5,
        label=f"Per-capita policing cost (constant {CPI_BASE_YEAR} $)",
        marker="s", markersize=4,
    )

    ax.axhline(100, color=PALETTE["light_grey"], linewidth=1, linestyle=":")
    ax.set_title(f"CSI vs Per-Capita Policing Cost — Indexed to {base_year} = 100")
    ax.set_xlabel("Year")
    ax.set_ylabel(f"Index ({base_year} = 100)")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
    ax.legend(loc="best")
    style_axes(ax)

    # Narrative
    csi_end = merged["csi_indexed"].iloc[-1]
    pc_end = merged["pc_indexed"].iloc[-1]
    csi_direction = "risen" if csi_end > 100 else "fallen"
    pc_direction = "risen" if pc_end > 100 else "fallen"

    narrative = (
        f"Indexed to {base_year} = 100, BC's Crime Severity Index had {csi_direction} to "
        f"{csi_end:.0f} by {last_year}, while real per-capita policing cost had {pc_direction} "
        f"to {pc_end:.0f}. "
    )

    if pc_end > csi_end:
        narrative += (
            "Per-capita policing expenditure grew faster than crime severity, suggesting "
            "rising unit costs or expanded policing scope beyond crime response. "
        )
    else:
        narrative += (
            "Crime severity grew faster than per-capita policing expenditure, suggesting "
            "policing budgets may not have kept pace with rising crime complexity. "
        )

    narrative += "Source: Statistics Canada Tables 35-10-0076-01, 35-10-0063-01."

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_expenditure_breakdown(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Stacked bar chart: Canada policing expenditure breakdown by category over time.

    Uses the 35-10-0059 table (Canada only, 2018-2023). Values are adjusted
    to constant 2020 dollars.
    """
    apply_theme()
    raw = _load_expenditure_breakdown()
    cpi = _load_cpi()

    # Filter to top-level categories
    cats = raw[raw["category"].isin(EXPENDITURE_CATEGORIES)].copy()

    # Value in the table is already in thousands; convert to billions
    cats = cats.merge(cpi[["year", "deflator"]], on="year", how="left")
    cats["real_billions"] = (cats["value"] * cats["deflator"]) / 1_000_000

    # Pivot: year × category
    wide = cats.pivot_table(index="year", columns="category", values="real_billions", aggfunc="first")
    wide = wide.sort_index()

    if wide.empty:
        logger.warning("No expenditure breakdown data available")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, "No data available", ha="center", va="center", transform=ax.transAxes)
        return fig, "No expenditure breakdown data available."

    fig, ax = plt.subplots(figsize=(12, 6))

    years = wide.index.values
    bar_width = 0.6
    bottom = np.zeros(len(years))

    colors = [PALETTE["bc_blue"], PALETTE["bc_amber"], PALETTE["bc_teal"]]
    for i, cat in enumerate(EXPENDITURE_CATEGORIES):
        if cat not in wide.columns:
            continue
        vals = wide[cat].fillna(0).values
        label = EXPENDITURE_LABELS.get(cat, cat)
        ax.bar(years, vals, bar_width, bottom=bottom, label=label, color=colors[i], edgecolor="white")

        # Add value labels inside bars if segment is tall enough
        for j, (y, v, b) in enumerate(zip(years, vals, bottom)):
            # Only label if the segment is tall enough (> 1.5× fontsize in data units)
            if v > 0.8:
                ax.text(
                    y, b + v / 2, f"${v:.1f}B",
                    ha="center", va="center", fontsize=8, color="white", fontweight="bold",
                )

        bottom += vals

    # Total labels on top
    totals = bottom
    for y, t in zip(years, totals):
        ax.text(y, t + 0.5, f"${t:.1f}B", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_title(f"Canada Policing Expenditure Breakdown (constant {CPI_BASE_YEAR} dollars)")
    ax.set_xlabel("Year")
    ax.set_ylabel(f"Expenditure ($ billions, constant {CPI_BASE_YEAR})")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}B"))
    ax.set_xticks(years)
    ax.set_xticklabels([str(int(y)) for y in years])
    ax.legend(loc="upper left")
    style_axes(ax)

    # Narrative
    first_yr = int(years[0])
    last_yr = int(years[-1])
    first_total = totals[0]
    last_total = totals[-1]
    growth_pct = ((last_total / first_total) - 1) * 100
    salary_share = wide[EXPENDITURE_CATEGORIES[0]].iloc[-1] / last_total * 100

    narrative = (
        f"Canada's total policing expenditure (in constant {CPI_BASE_YEAR} dollars) grew from "
        f"${first_total:.1f}B to ${last_total:.1f}B between {first_yr} and {last_yr} "
        f"({growth_pct:+.0f}% real growth). "
        f"Salaries and benefits account for {salary_share:.0f}% of total spending, "
        f"dominating the cost structure. Capital expenditure is a small share at "
        f"roughly {(100 - salary_share - (wide[EXPENDITURE_CATEGORIES[1]].iloc[-1] / last_total * 100)):.0f}% "
        f"of the total. Note: 2020 data is unavailable in the source table. "
        f"Source: Statistics Canada Table 35-10-0059-01."
    )

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_staffing_trend(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Line chart: BC police officers per 100,000 population over time."""
    apply_theme()
    pp = _load_police_personnel()

    bc = pp[
        (pp["geo"] == "British Columbia")
        & (pp["statistic"] == "Police officers per 100,000 population")
    ][["year", "value"]].copy()
    bc = bc.sort_values("year").reset_index(drop=True)

    if bc.empty:
        logger.warning("No staffing data found for BC")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, "No data available", ha="center", va="center", transform=ax.transAxes)
        return fig, "No BC staffing data available."

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        bc["year"], bc["value"],
        color=PALETTE["bc_blue"], linewidth=2.5,
        marker="o", markersize=4,
        label="Officers per 100,000",
    )

    first_yr = int(bc["year"].iloc[0])
    last_yr = int(bc["year"].iloc[-1])

    ax.set_title(f"BC Police Officers per 100,000 Population ({first_yr}–{last_yr})")
    ax.set_xlabel("Year")
    ax.set_ylabel("Officers per 100,000 population")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.legend(loc="best")
    style_axes(ax)

    # Narrative
    val_start = bc["value"].iloc[0]
    val_end = bc["value"].iloc[-1]
    val_peak = bc["value"].max()
    peak_yr = int(bc.loc[bc["value"].idxmax(), "year"])
    pct_change = ((val_end / val_start) - 1) * 100

    narrative = (
        f"BC had {val_start:.0f} police officers per 100,000 population in {first_yr}, "
        f"reaching a peak of {val_peak:.0f} in {peak_yr} before settling at {val_end:.0f} "
        f"by {last_yr} ({pct_change:+.0f}% overall). "
    )
    if val_end < val_peak:
        narrative += (
            f"The decline from peak staffing suggests that officer counts have not kept "
            f"pace with population growth. "
        )
    narrative += "Source: Statistics Canada Table 35-10-0076-01."

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


def chart_crimes_per_officer(save_path: Path | None = None) -> tuple[plt.Figure, str]:
    """Line chart: BC Criminal Code incidents per police officer, with CSI overlay."""
    apply_theme()
    pp = _load_police_personnel()

    bc = pp[
        (pp["geo"] == "British Columbia")
        & (pp["statistic"] == "Criminal Code incidents per police officer")
    ][["year", "value"]].copy()
    bc = bc.rename(columns={"value": "crimes_per_officer"})
    bc = bc.sort_values("year").reset_index(drop=True)

    if bc.empty:
        logger.warning("No crimes-per-officer data found for BC")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, "No data available", ha="center", va="center", transform=ax.transAxes)
        return fig, "No BC crimes-per-officer data available."

    first_yr = int(bc["year"].iloc[0])
    last_yr = int(bc["year"].iloc[-1])

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        bc["year"], bc["crimes_per_officer"],
        color=PALETTE["bc_blue"], linewidth=2.5,
        marker="o", markersize=4,
        label="Criminal Code incidents per officer",
    )

    # Overlay CSI on secondary axis for context
    ax2 = None
    try:
        csi = _csi_for_overlay()
        merged = bc.merge(csi, on="year", how="inner")
        if not merged.empty:
            ax2 = ax.twinx()
            ax2.plot(
                merged["year"], merged["csi"],
                color=PALETTE["bc_red"], linewidth=2, linestyle="--",
                marker="s", markersize=3,
                label="Crime Severity Index",
            )
            ax2.set_ylabel("Crime Severity Index", color=PALETTE["bc_red"])
            ax2.tick_params(axis="y", labelcolor=PALETTE["bc_red"])
            ax2.spines["right"].set_visible(True)
            ax2.spines["right"].set_color(PALETTE["bc_red"])
    except Exception:
        logger.debug("CSI overlay unavailable; plotting crimes-per-officer alone")

    ax.set_title(f"BC Criminal Code Incidents per Police Officer ({first_yr}–{last_yr})")
    ax.set_xlabel("Year")
    ax.set_ylabel("Incidents per officer")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    style_axes(ax)

    # Combined legend
    lines, labels = ax.get_legend_handles_labels()
    if ax2 is not None:
        lines2, labels2 = ax2.get_legend_handles_labels()
        lines += lines2
        labels += labels2
    ax.legend(lines, labels, loc="best")

    # Narrative
    val_start = bc["crimes_per_officer"].iloc[0]
    val_end = bc["crimes_per_officer"].iloc[-1]
    val_peak = bc["crimes_per_officer"].max()
    peak_yr = int(bc.loc[bc["crimes_per_officer"].idxmax(), "year"])
    pct_change = ((val_end / val_start) - 1) * 100

    narrative = (
        f"Each BC police officer handled an average of {val_start:.0f} Criminal Code incidents "
        f"in {first_yr}, peaking at {val_peak:.0f} in {peak_yr} and declining to {val_end:.0f} "
        f"by {last_yr} ({pct_change:+.0f}% overall). "
    )
    if val_end < val_peak:
        narrative += (
            "The post-peak decline in workload per officer may reflect both falling crime rates "
            "and incremental staffing improvements. "
        )
    narrative += "Source: Statistics Canada Table 35-10-0076-01."

    if save_path:
        save_fig(fig, str(save_path))
    return fig, narrative


# ---------------------------------------------------------------------------
# Run all
# ---------------------------------------------------------------------------


def run_all() -> dict[str, str]:
    """Generate all Priority 5 charts and return narratives."""
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    narratives = {}

    charts = [
        ("q3_bc_expenditure_trend", chart_bc_expenditure_trend),
        ("q3_per_capita_comparison", chart_per_capita_comparison),
        ("q3_csi_vs_expenditure", chart_csi_vs_expenditure),
        ("q3_expenditure_breakdown", chart_expenditure_breakdown),
        ("q3_staffing_trend", chart_staffing_trend),
        ("q3_crimes_per_officer", chart_crimes_per_officer),
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
