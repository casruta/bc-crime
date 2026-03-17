"""Tests for src/clean.py — verify cleaned datasets have expected shape and content."""

import pandas as pd
import pytest

from src.paths import PROCESSED_DIR


def _load(name: str) -> pd.DataFrame:
    path = PROCESSED_DIR / name
    assert path.exists(), f"Missing {name} — run `python -m src.clean` first"
    return pd.read_parquet(path)


class TestCrimeSeverityBC:
    def test_columns(self):
        df = _load("crime_severity_bc.parquet")
        assert "year" in df.columns
        assert "geo" in df.columns
        assert "statistic" in df.columns
        assert "value" in df.columns

    def test_row_count(self):
        df = _load("crime_severity_bc.parquet")
        assert len(df) > 50_000

    def test_year_range(self):
        df = _load("crime_severity_bc.parquet")
        years = df["year"].dropna()
        assert years.min() <= 1998
        assert years.max() >= 2022

    def test_no_bracket_codes_in_geo(self):
        df = _load("crime_severity_bc.parquet")
        assert not df["geo"].str.contains(r"\[", regex=True, na=False).any()


class TestCrimeIncidentsNational:
    def test_columns(self):
        df = _load("crime_incidents_national.parquet")
        assert "year" in df.columns
        assert "geo" in df.columns
        assert "violation" in df.columns
        assert "value" in df.columns

    def test_row_count(self):
        df = _load("crime_incidents_national.parquet")
        assert len(df) > 1_000_000

    def test_has_bc_and_canada(self):
        df = _load("crime_incidents_national.parquet")
        geos = df["geo"].unique()
        assert "British Columbia" in geos
        assert "Canada" in geos

    def test_year_range(self):
        df = _load("crime_incidents_national.parquet")
        years = df["year"].dropna()
        assert years.min() <= 1998
        assert years.max() >= 2022


class TestCPI:
    def test_columns(self):
        df = _load("cpi.parquet")
        assert set(df.columns) == {"year", "geo", "cpi"}

    def test_has_canada_and_bc(self):
        df = _load("cpi.parquet")
        assert "Canada" in df["geo"].values
        assert "British Columbia" in df["geo"].values

    def test_cpi_values_reasonable(self):
        df = _load("cpi.parquet")
        # CPI (2002=100) should be between ~10 and ~200
        assert df["cpi"].min() > 5
        assert df["cpi"].max() < 250


class TestBCGovTrends:
    def test_not_empty(self):
        df = _load("bc_gov_trends.parquet")
        assert len(df) > 100

    def test_columns(self):
        df = _load("bc_gov_trends.parquet")
        assert "offence" in df.columns
        assert "year" in df.columns
        assert "count" in df.columns

    def test_year_range(self):
        df = _load("bc_gov_trends.parquet")
        assert df["year"].min() == 2014
        assert df["year"].max() == 2023


class TestBCGovJurisdictionTrends:
    def test_not_empty(self):
        df = _load("bc_gov_jurisdiction_trends.parquet")
        assert len(df) > 1000

    def test_columns(self):
        df = _load("bc_gov_jurisdiction_trends.parquet")
        assert "policing_jurisdiction" in df.columns
        assert "year" in df.columns
        assert "count" in df.columns


class TestBCGovStats2023:
    def test_not_empty(self):
        df = _load("bc_gov_stats_2023.parquet")
        assert len(df) > 10

    def test_has_both_years(self):
        df = _load("bc_gov_stats_2023.parquet")
        assert "count_2022" in df.columns
        assert "count_2023" in df.columns


class TestJurisdictionMapping:
    def test_not_empty(self):
        df = _load("jurisdiction_mapping.parquet")
        assert len(df) >= 20

    def test_columns(self):
        df = _load("jurisdiction_mapping.parquet")
        assert "bcgov_name" in df.columns
        assert "statcan_name" in df.columns
