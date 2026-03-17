"""Download all StatCan CSV and BC Gov XLSX datasets to data/raw/."""

import io
import logging
import zipfile
from dataclasses import dataclass
from pathlib import Path

import requests

from src.paths import RAW_BCGOV_DIR, RAW_STATSCAN_DIR

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 120
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "BC-Crime-Analysis/1.0 (academic research)"
)


@dataclass
class StatCanTable:
    """A Statistics Canada table to download."""

    table_id: str
    name: str
    description: str

    @property
    def pid(self) -> str:
        return self.table_id.replace("-", "")[:8]

    @property
    def url(self) -> str:
        return f"https://www150.statcan.gc.ca/n1/tbl/csv/{self.pid}-eng.zip"

    @property
    def csv_filename(self) -> str:
        return f"{self.pid}.csv"

    @property
    def metadata_filename(self) -> str:
        return f"{self.pid}_MetaData.csv"


@dataclass
class BCGovFile:
    """A BC Government XLSX file to download."""

    name: str
    url: str
    description: str

    @property
    def filename(self) -> str:
        return self.url.rsplit("/", 1)[-1]


STATCAN_TABLES = [
    StatCanTable(
        table_id="35-10-0063-01",
        name="crime_severity_bc",
        description="Crime Severity Index by police service in BC",
    ),
    StatCanTable(
        table_id="35-10-0177-01",
        name="crime_incidents_national",
        description="Incident-based crime statistics by province/CMA (national)",
    ),
    StatCanTable(
        table_id="18-10-0005-01",
        name="cpi_annual",
        description="Consumer Price Index, annual averages",
    ),
    StatCanTable(
        table_id="35-10-0066-01",
        name="gss_perception_neighbourhood",
        description="Perception of crime in neighbourhood, by province (GSS)",
    ),
    StatCanTable(
        table_id="35-10-0068-01",
        name="gss_confidence_police",
        description="Confidence in police, by province (GSS)",
    ),
    StatCanTable(
        table_id="35-10-0076-01",
        name="police_personnel",
        description="Police personnel and selected crime statistics",
    ),
    StatCanTable(
        table_id="35-10-0059-01",
        name="police_expenditure",
        description="Police services expenditures, municipal, provincial/territorial",
    ),
]

BCGOV_FILES = [
    BCGovFile(
        name="bc_crime_stats_2023",
        url=(
            "https://www2.gov.bc.ca/assets/gov/law-crime-and-justice/"
            "criminal-justice/police/publications/statistics/"
            "appendix_f_-_crime_statistics_in_bc_2023.xlsx"
        ),
        description="Crime Statistics in BC, 2023",
    ),
    BCGovFile(
        name="bc_crime_trends",
        url=(
            "https://www2.gov.bc.ca/assets/gov/law-crime-and-justice/"
            "criminal-justice/police/publications/statistics/"
            "appendix_g_-_bc_crime_trends_2014-2023.xlsx"
        ),
        description="BC Crime Trends, 2014-2023",
    ),
    BCGovFile(
        name="bc_jurisdiction_trends",
        url=(
            "https://www2.gov.bc.ca/assets/gov/law-crime-and-justice/"
            "criminal-justice/police/publications/statistics/"
            "appendix_i_-_bc_policing_jurisdiction_crime_trends_2014-2023.xlsx"
        ),
        description="BC Policing Jurisdiction Crime Trends, 2014-2023",
    ),
    BCGovFile(
        name="bc_regional_district_trends",
        url=(
            "https://www2.gov.bc.ca/assets/gov/law-crime-and-justice/"
            "criminal-justice/police/publications/statistics/"
            "appendix_h_-_bc_regional_district_crime_trends_2014-2023.xlsx"
        ),
        description="BC Regional District Crime Trends, 2014-2023",
    ),
]


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def download_statcan_table(table: StatCanTable, dest: Path) -> list[Path]:
    """Download a StatCan ZIP, extract CSV + metadata to *dest*. Return paths."""
    dest.mkdir(parents=True, exist_ok=True)
    logger.info("Downloading StatCan %s (%s) ...", table.table_id, table.description)

    session = _session()
    resp = session.get(table.url, timeout=TIMEOUT_SECONDS)
    resp.raise_for_status()

    extracted: list[Path] = []
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for member in zf.namelist():
            if member.endswith(".csv"):
                target = dest / member
                target.write_bytes(zf.read(member))
                extracted.append(target)
                logger.info("  Extracted %s (%s bytes)", member, target.stat().st_size)

    return extracted


def download_bcgov_file(bcfile: BCGovFile, dest: Path) -> Path:
    """Download a BC Gov XLSX to *dest*. Return the path."""
    dest.mkdir(parents=True, exist_ok=True)
    logger.info("Downloading BC Gov %s (%s) ...", bcfile.name, bcfile.description)

    session = _session()
    resp = session.get(bcfile.url, timeout=TIMEOUT_SECONDS)
    resp.raise_for_status()

    target = dest / bcfile.filename
    target.write_bytes(resp.content)
    logger.info("  Saved %s (%s bytes)", bcfile.filename, target.stat().st_size)
    return target


def download_all(dest: Path | None = None) -> dict[str, list[Path]]:
    """Download every dataset. Return a dict mapping name -> list of paths.

    When *dest* is provided (e.g. by tests), all files go to that single
    directory.  When *dest* is None (production), StatCan files go to
    ``data/raw/statscan/`` and BC Gov files to ``data/raw/bcgov/``.
    """
    statcan_dest = dest or RAW_STATSCAN_DIR
    bcgov_dest = dest or RAW_BCGOV_DIR
    results: dict[str, list[Path]] = {}

    for table in STATCAN_TABLES:
        try:
            paths = download_statcan_table(table, statcan_dest)
            results[table.name] = paths
        except Exception:
            logger.exception("Failed to download StatCan %s", table.table_id)
            results[table.name] = []

    for bcfile in BCGOV_FILES:
        try:
            path = download_bcgov_file(bcfile, bcgov_dest)
            results[bcfile.name] = [path]
        except Exception:
            logger.exception("Failed to download BC Gov %s", bcfile.name)
            results[bcfile.name] = []

    return results


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )
    results = download_all()
    total = sum(len(v) for v in results.values())
    failed = sum(1 for v in results.values() if not v)
    logger.info("Done. %d files downloaded, %d sources failed.", total, failed)
