# Session Log

> Timestamped record of each iteration. Helps the human see what happened
> and helps Claude pick up where it left off if context resets.

---

## Session 1 — 2026-03-16

### Iteration 1: Project Setup + Data Pipeline (P1 & P2)

**Task:** Scaffold project, download all datasets, build cleaning pipeline

**Discovered:**
- StatCan CSV download pattern: `https://www150.statcan.gc.ca/n1/tbl/csv/{PID}-eng.zip`
- BC Gov XLSX files hosted at `www2.gov.bc.ca/assets/gov/law-crime-and-justice/...`
- 4 StatCan tables + 4 BC Gov XLSX files = 12 raw files total
- The crime incidents BC table (35-10-0184-01) is 6.2 GB
- BC Gov XLSX files have complex multi-panel layouts requiring custom parsing

**Implemented:**
- Created project structure, requirements.txt, .gitignore, pytest.ini
- Built `src/download.py` — all 12 files download successfully
- Built `src/clean.py` — produces 7 parquet files
- Fixed openpyxl version issue (3.1.2 → 3.1.5)
- Fixed BC Gov XLSX parser (NaN gaps between panels, string vs int year columns)
- Wrote 20 data quality tests — all pass

**Outcome:** Done

---

### Iteration 2: Crime Analysis (P3 & P4)

**Task:** Answer "Is Crime Rising?" and "What Kinds of Crime?"

**Discovered:**
- BC CSI data covers 1998–2024 with 18 statistic types
- National table has 314 unique violation types for BC
- Aggregate categories available via "Total" prefix violations

**Implemented:**
- `src/analysis/theme.py` — shared palette and chart styling
- `src/analysis/q1_is_crime_rising.py` — 4 charts: CSI trend, provincial comparison, YoY bars
- `src/analysis/q2_what_kinds.py` — 4 charts: stacked area, heatmap, top changes, slope chart
- Key findings: CSI peaked 1998 (166.9), troughed 2014 (90.2), BC +21% vs national, fell 7.4% in 2024
- Theft from vehicles dropped 772/100k; child exploitation up 82/100k

**Outcome:** Done

---

### Iteration 3: Costs + Geography (P5 & P6) — Parallel

**Task:** Policing expenditure analysis + geographic crime analysis

**Discovered:**
- Provincial expenditure data ends at 2009 — significant limitation
- Interior CMAs have 2x the per-capita crime rate of coastal metros
- Correlation between total and violent crime across jurisdictions is r=0.99

**Implemented:**
- Downloaded additional StatCan tables (35-10-0076, 35-10-0059)
- `src/analysis/q3_costs.py` — 4 charts: expenditure trend, per-capita comparison, CSI overlay, breakdown
- `src/analysis/q4_geography.py` — 5 outputs: top jurisdictions, trend multiples, scatter, CMA bars, interactive plotly
- Total: 16 PNG charts + 1 interactive HTML

**Outcome:** Done (P5 partially blocked on post-2009 expenditure data)

---

### Iteration 4: Final Report (P7)

**Task:** Assemble narrative report, update README and docs

**Implemented:**
- `notebooks/bc_crime_report.ipynb` — full report with executive summary, 4 sections, methodology, caveats
- Updated README.md with complete project description, quick start, data sources table
- Updated docs/plan.md — all tasks marked complete
- Updated docs/learnings.md with accumulated knowledge

**Outcome:** Done
