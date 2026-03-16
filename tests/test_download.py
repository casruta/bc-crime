"""Tests for src/download.py — verifies downloads succeed and produce non-empty files."""

import tempfile
from pathlib import Path

import pytest

from src.download import (
    BCGOV_FILES,
    STATCAN_TABLES,
    download_all,
    download_bcgov_file,
    download_statcan_table,
)

NETWORK_MARK = pytest.mark.network


@NETWORK_MARK
class TestStatCanDownloads:
    """Each StatCan table should download, unzip, and produce non-empty CSVs."""

    @pytest.fixture()
    def tmp_dest(self, tmp_path: Path) -> Path:
        return tmp_path / "raw"

    @pytest.mark.parametrize("table", STATCAN_TABLES, ids=lambda t: t.table_id)
    def test_download_produces_nonempty_csv(self, table, tmp_dest):
        paths = download_statcan_table(table, tmp_dest)
        assert len(paths) >= 1, f"Expected at least 1 CSV from {table.table_id}"
        for p in paths:
            assert p.exists(), f"{p} does not exist"
            assert p.stat().st_size > 0, f"{p} is empty"
            assert p.suffix == ".csv"


@NETWORK_MARK
class TestBCGovDownloads:
    """Each BC Gov file should download and be a non-empty XLSX."""

    @pytest.fixture()
    def tmp_dest(self, tmp_path: Path) -> Path:
        return tmp_path / "raw"

    @pytest.mark.parametrize("bcfile", BCGOV_FILES, ids=lambda f: f.name)
    def test_download_produces_nonempty_xlsx(self, bcfile, tmp_dest):
        path = download_bcgov_file(bcfile, tmp_dest)
        assert path.exists(), f"{path} does not exist"
        assert path.stat().st_size > 0, f"{path} is empty"
        assert path.suffix == ".xlsx"


@NETWORK_MARK
class TestDownloadAll:
    """Integration test: download_all should retrieve every dataset."""

    def test_all_sources_succeed(self, tmp_path):
        dest = tmp_path / "raw"
        results = download_all(dest)
        expected_sources = len(STATCAN_TABLES) + len(BCGOV_FILES)
        assert len(results) == expected_sources
        for name, paths in results.items():
            assert len(paths) >= 1, f"Source '{name}' produced no files"
            for p in paths:
                assert p.stat().st_size > 0, f"{p} is empty"
