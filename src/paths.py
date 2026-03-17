"""Centralized path constants for the BC Crime analysis pipeline."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_STATSCAN_DIR = RAW_DIR / "statscan"
RAW_BCGOV_DIR = RAW_DIR / "bcgov"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"
