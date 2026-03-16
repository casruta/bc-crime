# BC Crime Analysis — Feature Plan

> Source of truth for tasks. Claude reads this every iteration and picks
> the highest-priority incomplete task. Use `- [ ]` for incomplete,
> `- [x]` for done, `- [!]` for blocked.

---

## Priority 1: Project Scaffolding & Data Acquisition

> Set up the project structure, dependencies, and download all official
> datasets so subsequent tasks can focus on analysis.

- [ ] Create project directory structure (`src/`, `data/raw/`, `data/processed/`, `notebooks/`, `outputs/charts/`, `tests/`, `docs/`)
- [ ] Create `requirements.txt` with pinned versions: pandas, matplotlib, seaborn, plotly, geopandas, requests, openpyxl, jupyter, pytest, kaleido (for plotly image export)
- [ ] Create `.gitignore` (exclude `data/raw/`, `data/processed/`, `venv/`, `__pycache__/`, `.ipynb_checkpoints/`)
- [ ] Build `src/download.py` — fetch all StatCan CSVs and BC Gov XLSX files to `data/raw/`:
  - StatCan 35-10-0184-01 (incident-based crime by police service in BC)
  - StatCan 35-10-0063-01 (Crime Severity Index by police service in BC)
  - StatCan 35-10-0177-01 (incident-based crime by province/CMA — national)
  - StatCan 18-10-0005-01 (CPI for inflation adjustment)
  - BC Gov Crime Statistics 2023 XLSX
  - BC Gov Crime Trends 2014–2023 XLSX
  - BC Gov Policing Jurisdiction Crime Trends 2014–2023 XLSX
- [ ] Write a test that verifies `download.py` retrieves files and they are non-empty

---

## Priority 2: Data Cleaning & Normalization

> Parse StatCan's idiosyncratic CSV format, handle metadata rows, normalize
> column names, merge datasets where needed.

- [ ] Build `src/clean.py` — StatCan CSV parser that handles:
  - Metadata header rows (StatCan CSVs have extra rows before the data)
  - Bilingual column names and value labels
  - REF_DATE parsing into proper datetime/year columns
  - GEO column normalization (jurisdiction name standardization)
  - VALUE column type coercion (handle `..`, `x`, `F` suppression codes)
- [ ] Clean and save each dataset to `data/processed/` as parquet or clean CSV:
  - `crime_incidents_bc.parquet` (from 35-10-0184-01)
  - `crime_severity_bc.parquet` (from 35-10-0063-01)
  - `crime_incidents_national.parquet` (from 35-10-0177-01)
  - `cpi.parquet` (from 18-10-0005-01)
  - `bc_gov_trends.parquet` (from BC Gov XLSX files)
- [ ] Build a jurisdiction name mapping table that reconciles StatCan names with BC Gov names (e.g., "Vancouver, City, Municipal" ↔ "Vancouver Police Department")
- [ ] Write tests that verify row counts, expected columns, no unexpected nulls in key fields, and year range coverage

---

## Priority 3: Question 1 — Is Crime Rising in BC?

> Trend analysis using Crime Severity Index and total crime rates.
> The CSI is the gold standard metric — it weights offences by severity.

- [ ] Analyze BC's overall Crime Severity Index trend (1998–latest):
  - Total CSI
  - Violent CSI vs Non-Violent CSI
  - Youth CSI
  - Identify inflection points (2014 trough, post-2014 rise, COVID anomaly)
- [ ] Compare BC's CSI trend to the national average and to other provinces (AB, ON, SK, MB) using Table 35-10-0177-01
- [ ] Calculate year-over-year % change in total crime rate for BC
- [ ] Generate charts:
  - Line chart: BC CSI over time (total, violent, non-violent) with key events annotated
  - Small multiples: BC vs Canada vs 3 other provinces, CSI over time
  - Bar chart: most recent year-over-year change in CSI by province (BC highlighted)
- [ ] Write a narrative summary paragraph for each chart citing specific numbers and table sources

---

## Priority 4: Question 2 — What Kinds of Crime Are Rising?

> Breakdown by violation category to identify which crime types drive
> the overall trend.

- [ ] Group violations into meaningful categories:
  - Violent crime (homicide, assault, sexual assault, robbery)
  - Property crime (break & enter, theft, motor vehicle theft, fraud, mischief)
  - Drug offences
  - Administration of justice (bail violations, failure to appear)
  - Other Criminal Code
- [ ] For each category: calculate rate per 100,000 trend line (2014–latest)
- [ ] Identify the top 5 fastest-rising specific violations in BC (by % change in rate over 5 years)
- [ ] Identify the top 5 fastest-declining specific violations
- [ ] Generate charts:
  - Stacked area chart: crime composition over time (how the mix has shifted)
  - Heatmap: year × violation category, color = rate per 100,000 (highlights which cells are getting hotter)
  - Horizontal bar chart: top 10 violations by absolute rate change (last 5 years)
  - Slope chart or bump chart: ranking of violation categories, 2014 vs latest year
- [ ] Write narrative for each chart with specific numbers and caveats about reporting changes

---

## Priority 5: Question 3 — How Have Costs Increased?

> Policing expenditure analysis — total, per-capita, inflation-adjusted.

- [ ] Extract BC policing expenditure data from StatCan tables (35-10-0059-01 and/or 35-10-0076-01)
- [ ] Adjust all dollar figures to constant dollars using CPI (pick a base year, e.g., 2015 or 2020)
- [ ] Calculate for BC over time:
  - Total operating expenditures (nominal and real)
  - Per-capita operating expenditures (real)
  - Expenditure breakdown (salaries vs benefits vs other operating vs capital)
- [ ] Compare BC per-capita policing costs to national average and other provinces
- [ ] Calculate the "cost per crime" metric: total expenditure / total incidents
- [ ] Overlay: CSI trend vs per-capita expenditure trend (dual-axis or indexed to base year)
- [ ] Generate charts:
  - Line chart: BC total policing expenditure (nominal vs inflation-adjusted)
  - Bar chart: BC per-capita policing cost vs other provinces (latest year)
  - Dual-axis line: CSI vs per-capita expenditure over time (indexed to 100)
  - Stacked bar: expenditure breakdown by category over time
- [ ] Write narrative with specific dollar figures, always noting "constant [base year] dollars"

---

## Priority 6: Question 4 — Where Is Crime Happening?

> Geographic analysis by police jurisdiction and regional district.

- [ ] Extract jurisdiction-level data from Table 35-10-0184-01 and/or BC Gov Jurisdiction Trends XLSX
- [ ] Rank BC police jurisdictions by:
  - Highest overall crime rate (latest year)
  - Highest CSI (latest year)
  - Largest increase in crime rate (5-year and 10-year % change)
  - Highest violent crime rate
- [ ] Attempt to source GeoJSON boundaries for BC police jurisdictions or regional districts from DataBC catalogue (https://catalogue.data.gov.bc.ca/) — if unavailable, fall back to a bar chart by jurisdiction
- [ ] Generate charts:
  - Choropleth map: crime rate by jurisdiction (if GeoJSON found)
  - Interactive plotly map with hover tooltips showing jurisdiction name, rate, CSI, top crime type
  - Horizontal bar chart: top 20 jurisdictions by crime rate
  - Small multiples: CSI trend for the 8 largest jurisdictions (Vancouver, Surrey, Burnaby, etc.)
  - Scatter plot: jurisdiction population vs crime rate (are larger cities safer or more dangerous?)
- [ ] CMA-level analysis using Table 35-10-0177-01:
  - Compare Vancouver CMA, Victoria CMA, Kelowna CMA, Abbotsford CMA
- [ ] Write narrative with jurisdiction-specific findings

---

## Priority 7: Final Report Assembly

> Combine all analysis into a cohesive narrative report.

- [ ] Create `notebooks/bc_crime_report.ipynb` that tells the full story:
  - Executive summary (key findings in 3–4 bullet points)
  - Section 1: Is crime rising? (with embedded charts)
  - Section 2: What kinds of crime? (with embedded charts)
  - Section 3: What does it cost? (with embedded charts)
  - Section 4: Where is it happening? (with maps and charts)
  - Methodology notes and data source citations
  - Caveats and limitations section
- [ ] Export notebook to standalone HTML: `outputs/report.html`
- [ ] Ensure all charts are also saved as high-res PNGs in `outputs/charts/`
- [ ] Final review: run all code end-to-end from clean state to verify reproducibility
- [ ] Update README.md with project description, setup instructions, and sample outputs

---

## Blocked

<!-- Move items here with a note about what's blocking them -->

## Completed

<!-- Claude moves completed items here with a date -->
