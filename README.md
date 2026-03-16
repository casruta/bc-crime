# BC Crime Data Analysis

A comprehensive analysis of crime trends across British Columbia, Canada, using official Statistics Canada and BC Government data.

## Two analysis tracks

### 1. R Markdown Report (original)

An R-based analysis covering 2018–2023 using a local `bc_crime.csv` dataset.

| File | Description |
|------|-------------|
| `BC Crime Data/Data Sets/BC CRIME.Rmd` | Main analysis report (HTML + PDF output) |
| `BC Crime Data/Data Sets/BC CRIME Worksheet.Rmd` | Exploration worksheet |

**To run:** Open `BC CRIME.Rmd` in RStudio → Click **Knit**

### 2. Python Analysis Pipeline (new)

A full data pipeline that downloads official StatCan and BC Government datasets, cleans them, and produces 16 publication-quality charts answering four policy questions.

#### Questions answered

1. **Is crime rising?** CSI trend analysis, provincial comparison, year-over-year changes
2. **What kinds of crime?** Category composition, heatmap, fastest-rising/declining offences
3. **What does policing cost?** Expenditure trends (nominal vs CPI-adjusted), per-capita comparison
4. **Where is crime happening?** Jurisdiction rankings, CMA comparison, interactive map

#### Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Download all datasets (~8 GB)
python -m src.download

# Clean and normalize to parquet
python -m src.clean

# Generate all charts
python -m src.analysis.q1_is_crime_rising
python -m src.analysis.q2_what_kinds
python -m src.analysis.q3_costs
python -m src.analysis.q4_geography
```

Charts are saved to `outputs/charts/`. Open `notebooks/bc_crime_report.ipynb` for the full narrative report.

#### Data sources

| Source | Table | Description |
|--------|-------|-------------|
| Statistics Canada | 35-10-0063-01 | Crime Severity Index by police service, BC |
| Statistics Canada | 35-10-0177-01 | Incident-based crime stats by province/CMA |
| Statistics Canada | 35-10-0076-01 | Police personnel and expenditures |
| Statistics Canada | 35-10-0059-01 | Police services expenditures |
| Statistics Canada | 18-10-0005-01 | Consumer Price Index |
| BC Government | Appendix F–I | Crime stats, trends, jurisdiction data (2014–2023) |

#### Project structure

```
src/
  download.py          # Fetch all raw data from StatCan and BC Gov
  clean.py             # Parse, normalize, save to parquet
  analysis/
    theme.py           # Shared chart theme and palette
    q1_is_crime_rising.py   # CSI trends, provincial comparison
    q2_what_kinds.py        # Crime type breakdown
    q3_costs.py             # Policing expenditure analysis
    q4_geography.py         # Jurisdiction and CMA analysis
data/
  raw/                 # Downloaded files (gitignored)
  processed/           # Cleaned parquet files (gitignored)
notebooks/
  bc_crime_report.ipynb  # Full narrative report
outputs/
  charts/              # Generated PNG charts
tests/
  test_download.py     # Download verification tests
  test_clean.py        # Data quality tests
```

## Requirements

- **R track:** R >= 4.0, ggplot2, dplyr, tidyr, scales, knitr, rmarkdown, glue
- **Python track:** Python 3.12+, see `requirements.txt`

## Author

Casper Kacper Ruta (2024–2026)
