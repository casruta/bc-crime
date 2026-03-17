"""Clean and normalize all raw datasets into analysis-ready parquet files."""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from src.paths import PROCESSED_DIR, RAW_BCGOV_DIR, RAW_STATSCAN_DIR

logger = logging.getLogger(__name__)

# StatCan suppression codes that should become NaN
SUPPRESSION_CODES = frozenset({"..", "x", "F", "...", ""})

# Columns we keep from StatCan CSVs (rest is metadata)
STATCAN_DROP_COLS = [
    "DGUID", "UOM_ID", "SCALAR_FACTOR", "SCALAR_ID",
    "VECTOR", "COORDINATE", "SYMBOL", "TERMINATED", "DECIMALS",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _strip_geo_code(geo: pd.Series) -> pd.Series:
    """Remove StatCan bracketed codes from GEO, e.g. 'British Columbia [59]' -> 'British Columbia'."""
    return geo.str.replace(r"\s*\[.*?\]", "", regex=True).str.strip()


def _coerce_value(series: pd.Series) -> pd.Series:
    """Convert VALUE column: replace suppression codes with NaN, then to float."""
    cleaned = series.replace({code: np.nan for code in SUPPRESSION_CODES})
    return pd.to_numeric(cleaned, errors="coerce")


def _clean_statcan_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase column names, strip GEO codes, coerce VALUE, drop metadata cols."""
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    if "geo" in df.columns:
        df["geo"] = _strip_geo_code(df["geo"])
    if "value" in df.columns:
        df["value"] = _coerce_value(df["value"])
    drop = [c.lower() for c in STATCAN_DROP_COLS]
    df = df.drop(columns=[c for c in drop if c in df.columns], errors="ignore")
    return df


def _parse_ref_date(df: pd.DataFrame) -> pd.DataFrame:
    """Parse ref_date to integer year. StatCan uses 'YYYY' format for annual tables."""
    if "ref_date" in df.columns:
        df["year"] = pd.to_numeric(df["ref_date"], errors="coerce").astype("Int64")
        df = df.drop(columns=["ref_date"])
    return df


# ---------------------------------------------------------------------------
# StatCan table cleaners
# ---------------------------------------------------------------------------

def clean_crime_severity_bc() -> pd.DataFrame:
    """Clean 35100063 — Crime Severity Index by police service in BC."""
    path = RAW_STATSCAN_DIR / "35100063.csv"
    logger.info("Cleaning %s ...", path.name)
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig")
    df = _clean_statcan_columns(df)
    df = _parse_ref_date(df)
    df = df.rename(columns={"statistics": "statistic"})
    logger.info("  %d rows, %d cols", len(df), len(df.columns))
    return df


def clean_crime_incidents_national() -> pd.DataFrame:
    """Clean 35100177 — incident-based crime by province/CMA (national)."""
    path = RAW_STATSCAN_DIR / "35100177.csv"
    logger.info("Cleaning %s ...", path.name)
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig")
    df = _clean_statcan_columns(df)
    df = _parse_ref_date(df)
    df = df.rename(columns={"violations": "violation", "statistics": "statistic"})
    logger.info("  %d rows, %d cols", len(df), len(df.columns))
    return df


def clean_cpi() -> pd.DataFrame:
    """Clean 18100005 — CPI annual averages.

    We extract the All-items, 2002=100 series for Canada and BC.
    """
    path = RAW_STATSCAN_DIR / "18100005.csv"
    logger.info("Cleaning %s ...", path.name)
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig")
    df = _clean_statcan_columns(df)
    df = _parse_ref_date(df)
    df = df.rename(columns={"products_and_product_groups": "product_group"})

    # Keep only All-items with 2002=100 base
    mask = (
        df["product_group"].str.strip().str.lower() == "all-items"
    ) & (
        df["uom"].str.contains("2002=100", na=False)
    )
    df = df[mask].copy()

    # Keep Canada and BC
    df = df[df["geo"].isin(["Canada", "British Columbia"])].copy()
    df = df[["year", "geo", "value"]].rename(columns={"value": "cpi"})
    df = df.dropna(subset=["cpi"]).reset_index(drop=True)
    logger.info("  %d rows after filtering", len(df))
    return df


def clean_gss_perception() -> pd.DataFrame:
    """Clean 35100066 — Perception of crime in neighbourhood, by province (GSS).

    Extracts the 'increased/decreased/about the same' responses for
    BC and Canada from the General Social Survey data.
    Output columns: year, geo, response, value.
    """
    path = RAW_STATSCAN_DIR / "35100066.csv"
    if not path.exists():
        logger.warning("GSS perception file not found: %s", path)
        return pd.DataFrame(columns=["year", "geo", "response", "value"])
    logger.info("Cleaning %s ...", path.name)
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig")
    logger.info("  Raw columns: %s", list(df.columns))
    df = _clean_statcan_columns(df)
    df = _parse_ref_date(df)

    # Keep BC and Canada
    geos = {"British Columbia", "Canada"}
    if "geo" in df.columns:
        df = df[df["geo"].isin(geos)].copy()

    # Identify the response/perception column
    # StatCan GSS tables use various column names for the perception dimension
    response_col = None
    for candidate in ("perceptions", "perception_of_crime_in_the_neighbourhood",
                       "perception", "indicators"):
        if candidate in df.columns:
            response_col = candidate
            break

    if response_col is None:
        # Fall back: use any column that contains perception-like values
        for col in df.columns:
            sample = df[col].dropna().head(20).str.lower()
            if sample.str.contains("increased|decreased|about the same", regex=True).any():
                response_col = col
                break

    if response_col is None:
        logger.warning("Could not identify perception/response column in GSS data")
        return pd.DataFrame(columns=["year", "geo", "response", "value"])

    # Filter to key responses
    response_keywords = ["increased", "decreased", "about the same"]
    mask = df[response_col].str.lower().str.contains("|".join(response_keywords), na=False, regex=True)
    df = df[mask].copy()

    df = df.rename(columns={response_col: "response"})
    result = df[["year", "geo", "response", "value"]].copy()
    result = result.dropna(subset=["value"]).reset_index(drop=True)
    logger.info("  %d rows after filtering", len(result))
    return result


def clean_gss_confidence() -> pd.DataFrame:
    """Clean 35100068 — Confidence in police, by province (GSS).

    Extracts confidence levels for all provinces from the General Social Survey.
    Output columns: year, geo, confidence_level, value.
    """
    path = RAW_STATSCAN_DIR / "35100068.csv"
    if not path.exists():
        logger.warning("GSS confidence file not found: %s", path)
        return pd.DataFrame(columns=["year", "geo", "confidence_level", "value"])
    logger.info("Cleaning %s ...", path.name)
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig")
    logger.info("  Raw columns: %s", list(df.columns))
    df = _clean_statcan_columns(df)
    df = _parse_ref_date(df)

    # Identify the confidence level column
    confidence_col = None
    for candidate in ("confidence_in_police", "confidence", "level_of_confidence",
                       "indicators", "responses"):
        if candidate in df.columns:
            confidence_col = candidate
            break

    if confidence_col is None:
        for col in df.columns:
            sample = df[col].dropna().head(20).str.lower()
            if sample.str.contains("great deal|some confidence|not very much", regex=True).any():
                confidence_col = col
                break

    if confidence_col is None:
        logger.warning("Could not identify confidence column in GSS data")
        return pd.DataFrame(columns=["year", "geo", "confidence_level", "value"])

    df = df.rename(columns={confidence_col: "confidence_level"})
    result = df[["year", "geo", "confidence_level", "value"]].copy()
    result = result.dropna(subset=["value"]).reset_index(drop=True)
    logger.info("  %d rows after filtering", len(result))
    return result


# ---------------------------------------------------------------------------
# BC Gov XLSX cleaners
# ---------------------------------------------------------------------------

def _read_bcgov_trends_sheet(path: Path, sheet_name: str, year_cols: list[int]) -> pd.DataFrame:
    """Read a BC Gov trends sheet and extract the 'Number of Offences' panel.

    These sheets have a complex layout: Row 0 = panel header, Row 2 = year columns,
    Row 3+ = data. Multiple panels side-by-side. We extract only the first panel
    (Number of Offences) plus the Crime Rates panel if available.
    """
    df_raw = pd.read_excel(path, sheet_name=sheet_name, header=None)

    # Find the header row with year numbers
    header_row_idx = None
    for i in range(min(5, len(df_raw))):
        row_vals = df_raw.iloc[i].dropna().tolist()
        if any(isinstance(v, (int, float)) and 2014 <= v <= 2030 for v in row_vals):
            header_row_idx = i
            break

    if header_row_idx is None:
        logger.warning("Could not find year header in sheet '%s' of %s", sheet_name, path.name)
        return pd.DataFrame()

    # Extract offence name column (col 0) and year data columns
    offence_col = 0
    # Find year columns in the first panel only (stop at first NaN gap after years start)
    header = df_raw.iloc[header_row_idx]
    year_col_indices: list[int] = []
    started = False
    for col_idx in range(1, len(header)):
        val = header.iloc[col_idx]
        if isinstance(val, (int, float)) and not pd.isna(val) and 2014 <= val <= 2030:
            year_col_indices.append(col_idx)
            started = True
        elif started:
            break  # Hit the NaN gap between panels — stop

    if not year_col_indices:
        return pd.DataFrame()

    # Build the dataframe
    data_start = header_row_idx + 1
    years = [int(header.iloc[c]) for c in year_col_indices]

    records = []
    for row_idx in range(data_start, len(df_raw)):
        offence = df_raw.iloc[row_idx, offence_col]
        if pd.isna(offence) or str(offence).strip() == "":
            continue
        offence = str(offence).strip()
        for j, yr in enumerate(years):
            val = df_raw.iloc[row_idx, year_col_indices[j]]
            records.append({"offence": offence, "year": yr, "count": val})

    result = pd.DataFrame(records)
    result["count"] = pd.to_numeric(result["count"], errors="coerce")
    return result


def clean_bc_gov_trends() -> pd.DataFrame:
    """Clean appendix_g — BC Crime Trends 2014-2023.

    Extracts the 'Criminal Code Offences' sheet as the primary dataset.
    """
    path = RAW_BCGOV_DIR / "appendix_g_-_bc_crime_trends_2014-2023.xlsx"
    logger.info("Cleaning %s ...", path.name)

    sheets_to_extract = ["Criminal Code Offences", "Drug Offences", "Crime Severity Index"]
    frames = []
    for sheet in sheets_to_extract:
        try:
            df = _read_bcgov_trends_sheet(path, sheet, list(range(2014, 2024)))
            if not df.empty:
                df["sheet"] = sheet
                frames.append(df)
        except Exception:
            logger.exception("Failed to parse sheet '%s'", sheet)

    if not frames:
        logger.warning("No data extracted from %s", path.name)
        return pd.DataFrame()

    result = pd.concat(frames, ignore_index=True)
    logger.info("  %d rows from %d sheets", len(result), len(frames))
    return result


def clean_bc_gov_jurisdiction_trends() -> pd.DataFrame:
    """Clean appendix_i — BC Policing Jurisdiction Crime Trends 2014-2023.

    Row 1 = headers: REGION, TYPE OF POLICING, POLICING JURISDICTION, 2014...2023, ENDNOTE
    """
    path = RAW_BCGOV_DIR / "appendix_i_-_bc_policing_jurisdiction_crime_trends_2014-2023.xlsx"
    logger.info("Cleaning %s ...", path.name)

    sheets = ["Criminal Code Offences", "Violent Offences", "Property Offences"]
    frames = []

    for sheet in sheets:
        try:
            df_raw = pd.read_excel(path, sheet_name=sheet, header=1)
            # Columns: REGION, TYPE OF POLICING, POLICING JURISDICTION, 2014...2023, ENDNOTE
            # Year columns may be int, float, or string depending on openpyxl version
            year_cols = []
            for c in df_raw.columns:
                try:
                    yr = int(float(c)) if not isinstance(c, (int, float)) else int(c)
                    if 2014 <= yr <= 2030:
                        year_cols.append(c)
                except (ValueError, TypeError):
                    pass
            meta_cols = ["REGION", "TYPE OF POLICING", "POLICING JURISDICTION"]
            meta_cols = [c for c in meta_cols if c in df_raw.columns]

            if not year_cols or not meta_cols:
                continue

            # Melt from wide to long
            id_vars = meta_cols
            df_long = df_raw[meta_cols + year_cols].melt(
                id_vars=id_vars, var_name="year", value_name="count"
            )
            df_long.columns = [c.lower().replace(" ", "_") for c in df_long.columns]
            df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce").astype("Int64")
            df_long["count"] = pd.to_numeric(
                df_long["count"].replace({"-": np.nan, "": np.nan}), errors="coerce"
            )
            df_long["category"] = sheet
            df_long = df_long.dropna(subset=["policing_jurisdiction"])
            frames.append(df_long)
        except Exception:
            logger.exception("Failed to parse jurisdiction sheet '%s'", sheet)

    if not frames:
        return pd.DataFrame()

    result = pd.concat(frames, ignore_index=True)
    result = result.reset_index(drop=True)
    logger.info("  %d rows from %d sheets", len(result), len(frames))
    return result


def clean_bc_gov_stats_2023() -> pd.DataFrame:
    """Clean appendix_f — Crime Statistics in BC 2023.

    Complex layout with sub-headers. Extract Table 1 sheet.
    """
    path = RAW_BCGOV_DIR / "appendix_f_-_crime_statistics_in_bc_2023.xlsx"
    logger.info("Cleaning %s ...", path.name)

    df_raw = pd.read_excel(path, sheet_name="Table 1", header=None)
    # Row 3 has column headers: Crime Category, 2022, 2023, % Chg, ...
    # Data starts at row 4+
    # Columns: Crime Category | Num2022 | Num2023 | %Chg | Rate2022 | Rate2023 | %Chg | ...

    data_start = 4  # row index
    records = []
    for row_idx in range(data_start, len(df_raw)):
        category = df_raw.iloc[row_idx, 0]
        if pd.isna(category) or str(category).strip() == "":
            continue
        category = str(category).strip()
        num_2022 = pd.to_numeric(df_raw.iloc[row_idx, 1], errors="coerce")
        num_2023 = pd.to_numeric(df_raw.iloc[row_idx, 2], errors="coerce")
        rate_2022 = pd.to_numeric(df_raw.iloc[row_idx, 4], errors="coerce")
        rate_2023 = pd.to_numeric(df_raw.iloc[row_idx, 5], errors="coerce")
        records.append({
            "crime_category": category,
            "count_2022": num_2022,
            "count_2023": num_2023,
            "rate_2022": rate_2022,
            "rate_2023": rate_2023,
        })

    result = pd.DataFrame(records)
    logger.info("  %d rows", len(result))
    return result


# ---------------------------------------------------------------------------
# Jurisdiction name mapping
# ---------------------------------------------------------------------------

JURISDICTION_MAP = {
    # BC Gov name -> StatCan GEO name
    "Abbotsford Mun": "Abbotsford, City, Municipal",
    "Burnaby Mun": "Burnaby, City, Municipal",
    "Central Saanich Mun": "Central Saanich, District, Municipal",
    "Delta Mun": "Delta, City, Municipal",
    "Esquimalt Mun": "Esquimalt, Township, Municipal",
    "Kamloops Mun": "Kamloops, City, Municipal",
    "Langley Mun": "Langley, Township, Municipal",
    "Nanaimo Mun": "Nanaimo, City, Municipal",
    "Nelson Mun": "Nelson, City, Municipal",
    "New Westminster Mun": "New Westminster, City, Municipal",
    "North Vancouver RCMP Mun": "North Vancouver, District, Municipal",
    "Oak Bay Mun": "Oak Bay, District, Municipal",
    "Penticton Mun": "Penticton, City, Municipal",
    "Port Moody Mun": "Port Moody, City, Municipal",
    "Prince George Mun": "Prince George, City, Municipal",
    "Richmond Mun": "Richmond, City, Municipal",
    "Saanich Mun": "Saanich, District, Municipal",
    "Surrey Mun": "Surrey, City, Municipal",
    "Vancouver Mun": "Vancouver, City, Municipal",
    "Vernon Mun": "Vernon, City, Municipal",
    "Victoria Mun": "Victoria, City, Municipal",
    "West Vancouver Mun": "West Vancouver, District, Municipal",
    "White Rock Mun": "White Rock, City, Municipal",
}


def get_jurisdiction_mapping() -> pd.DataFrame:
    """Return a DataFrame mapping BC Gov jurisdiction names to StatCan GEO names."""
    records = [
        {"bcgov_name": k, "statcan_name": v}
        for k, v in JURISDICTION_MAP.items()
    ]
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def clean_all() -> dict[str, pd.DataFrame]:
    """Clean all datasets and save to data/processed/. Return dict of DataFrames."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    results: dict[str, pd.DataFrame] = {}

    # StatCan tables
    cleaners = {
        "crime_severity_bc": (clean_crime_severity_bc, "crime_severity_bc.parquet"),
        "crime_incidents_national": (clean_crime_incidents_national, "crime_incidents_national.parquet"),
        "cpi": (clean_cpi, "cpi.parquet"),
        "gss_perception": (clean_gss_perception, "gss_perception.parquet"),
        "gss_confidence": (clean_gss_confidence, "gss_confidence.parquet"),
    }

    for name, (fn, filename) in cleaners.items():
        try:
            df = fn()
            outpath = PROCESSED_DIR / filename
            df.to_parquet(outpath, index=False)
            results[name] = df
            logger.info("Saved %s (%d rows)", outpath.name, len(df))
        except Exception:
            logger.exception("Failed to clean %s", name)

    # BC Gov files
    bcgov_cleaners = {
        "bc_gov_trends": (clean_bc_gov_trends, "bc_gov_trends.parquet"),
        "bc_gov_jurisdiction_trends": (
            clean_bc_gov_jurisdiction_trends,
            "bc_gov_jurisdiction_trends.parquet",
        ),
        "bc_gov_stats_2023": (clean_bc_gov_stats_2023, "bc_gov_stats_2023.parquet"),
    }

    for name, (fn, filename) in bcgov_cleaners.items():
        try:
            df = fn()
            outpath = PROCESSED_DIR / filename
            df.to_parquet(outpath, index=False)
            results[name] = df
            logger.info("Saved %s (%d rows)", outpath.name, len(df))
        except Exception:
            logger.exception("Failed to clean %s", name)

    # Jurisdiction mapping
    mapping = get_jurisdiction_mapping()
    mapping.to_parquet(PROCESSED_DIR / "jurisdiction_mapping.parquet", index=False)
    results["jurisdiction_mapping"] = mapping
    logger.info("Saved jurisdiction_mapping.parquet (%d mappings)", len(mapping))

    return results


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )
    results = clean_all()
    logger.info("Cleaned %d datasets.", len(results))
    for name, df in results.items():
        logger.info("  %-35s  %d rows  x  %d cols", name, len(df), len(df.columns))
