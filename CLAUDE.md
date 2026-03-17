# BC Crime Analysis

## Overview

Python-based analytical pipeline examining crime trends across British Columbia
(2004-2024). Data sourced from Statistics Canada open tables and BC Government
justice appendices. Outputs are publication-ready PNG charts and one interactive
HTML map, organized into four research questions.

## Commands

```bash
pip install -r requirements.txt          # Install dependencies
python -m src.download                   # Download all datasets (~8 GB)
python -m src.clean                      # Clean and normalize to parquet
python -m src.analysis.q1_is_crime_rising  # Section 1 charts (8 PNG)
python -m src.analysis.q2_what_kinds       # Section 2 charts (8 PNG)
python -m src.analysis.q3_justice          # Section 3 charts (7 PNG)
python -m src.analysis.q4_geography        # Section 4 charts (7 PNG + 1 HTML)
pytest                                     # Run tests
```

## Architecture

```
BC-CRIME-/
  src/
    __init__.py
    paths.py               # Centralized path constants (single source of truth)
    download.py            # Fetch raw CSVs from StatsCan / BC Gov
    clean.py               # Normalize, rename columns, write parquet
    analysis/
      __init__.py
      theme.py             # PALETTE, ORDERED, styling helpers
      q1_is_crime_rising.py
      q2_what_kinds.py
      q3_justice.py
      q3_costs.py
      q4_geography.py
  data/
    README.md              # Comprehensive data dictionary with citations
    raw/
      statscan/            # Statistics Canada CSVs + metadata (gitignored)
      bcgov/               # BC Government XLSX files (gitignored)
    processed/             # Cleaned parquet files (gitignored)
  outputs/
    charts/                # Generated PNGs and HTML
      README.md            # Chart index mapping filenames to figure numbers
  tests/
  notebooks/               # Exploratory Jupyter notebooks
  requirements.txt
  CLAUDE.md
  README.md
```

## Data Sources

| Key             | StatsCan Table / Source        | Content                          |
|-----------------|-------------------------------|----------------------------------|
| CSI             | Table 35-10-0063-01           | Crime Severity Index, 1998-2024  |
| National        | Table 35-10-0177-01           | Incident-based national stats    |
| Jurisdiction    | BC Gov Appendix F-I           | Municipal / detachment-level data|

## Conventions

- Every chart function follows the signature:
  `chart_xyz(save_path) -> tuple[plt.Figure, str]`
  returning the figure object and a narrative string.
- All styling goes through `src/analysis/theme.py`, which wraps the shared
  `kds` module and re-exports: `PALETTE`, `ORDERED`, `add_subtitle`,
  `add_fig_subtitle`, `annotate_events`, `add_source`, `save_fig`,
  `style_axes`.
- Each `q*` module exposes a `run_all()` entry point that generates every
  chart for that section.
- Charts are saved to `outputs/charts/`.
- Processed data lives in `data/processed/` as parquet files (gitignored).

## File Boundaries

**Safe to edit:**
- `src/analysis/*.py`
- `src/paths.py`
- `tests/`
- `notebooks/`
- `data/README.md`
- `outputs/charts/README.md`
- `README.md`
- `CLAUDE.md`

**Never touch:**
- `data/raw/` (downloaded source data)
- `.env`

## Quality Gates

All gates must pass before committing:

1. `pytest` passes with zero failures
2. No lint errors
3. All charts regenerate without error (`python -m src.analysis.q1_is_crime_rising` through `q4`)
