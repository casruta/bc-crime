# BC Crime Analysis — Feature Plan

> Source of truth for tasks. Claude reads this every iteration and picks
> the highest-priority incomplete task. Use `- [ ]` for incomplete,
> `- [x]` for done, `- [!]` for blocked.

---

## Blocked

- [!] **Policing expenditure (post-2009):** StatCan Table 35-10-0076-01 only has provincial-level expenditure data through 2009. Post-2009 data requires alternative sources (BC Public Accounts, FOI requests, or individual police board reports). Table 35-10-0059-01 has 2018-2023 data but only at the Canada national level.

## Completed

### Priority 1: Project Scaffolding & Data Acquisition (2026-03-16)

- [x] Create project directory structure
- [x] Create `requirements.txt` with pinned versions
- [x] Create `.gitignore`
- [x] Build `src/download.py` — fetches 4 StatCan tables + 4 BC Gov XLSX files (12 files total, 0 failures)
- [x] Write download verification tests (test_download.py)

### Priority 2: Data Cleaning & Normalization (2026-03-16)

- [x] Build `src/clean.py` — StatCan CSV parser + BC Gov XLSX parser
- [x] Clean and save 7 parquet files to `data/processed/`
- [x] Build jurisdiction name mapping table (23 entries)
- [x] Write 20 data quality tests (test_clean.py) — all pass

### Priority 3: Question 1 — Is Crime Rising in BC? (2026-03-16)

- [x] BC CSI trend analysis (1998-2024): peaked 166.9 in 1998, troughed 90.2 in 2014, at 93.0 in 2024
- [x] Provincial comparison (BC, Canada, AB, ON, SK, MB): BC is +21% vs national average
- [x] Year-over-year % change: BC fell 7.4% in 2024
- [x] Generated 4 charts with narratives (q1_bc_csi_trend, q1_provincial_comparison, q1_yoy_by_province, q1_bc_yoy_trend)

### Priority 4: Question 2 — What Kinds of Crime Are Rising? (2026-03-16)

- [x] Crime category composition analysis (5 categories, stacked area chart)
- [x] Heatmap: year × category (2014-2024)
- [x] Top 10 violations by absolute rate change (theft from vehicles -772, child exploitation +82)
- [x] Slope chart: category ranking 2014 vs 2024
- [x] Top 5 fastest-rising and fastest-declining specific violations identified

### Priority 5: Question 3 — How Have Costs Increased? (2026-03-16)

- [x] Downloaded StatCan 35-10-0076-01 and 35-10-0059-01
- [x] CPI adjustment to constant 2020 dollars
- [x] BC expenditure trend (1986-2009): real spending grew +145%
- [x] Per-capita provincial comparison (2009): BC at $253, 31% below national
- [x] CSI vs expenditure indexed overlay: CSI fell to 67 while spending rose to 151
- [x] Canada-level expenditure breakdown (2018-2023): salaries = 80%
- [x] Generated 4 charts with narratives

### Priority 6: Question 4 — Where Is Crime Happening? (2026-03-16)

- [x] Jurisdiction-level rankings (top 20 by count, by change, by violent)
- [x] 8-jurisdiction trend small multiples
- [x] Total vs violent scatter plot (r=0.99)
- [x] CMA comparison (7 BC CMAs): Chilliwack highest (11,352), Victoria lowest (5,283)
- [x] Interactive plotly chart (q4_interactive_map.html)
- [x] Generated 5 charts with narratives

### Priority 7: Final Report Assembly (2026-03-16)

- [x] Created `notebooks/bc_crime_report.ipynb` with full narrative
- [x] Executive summary, 4 analysis sections, methodology, caveats
- [x] All 16 charts saved as PNGs in `outputs/charts/`
- [x] Updated README.md with project description and setup instructions
