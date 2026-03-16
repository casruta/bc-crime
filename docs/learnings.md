# Project Learnings

> Accumulated knowledge discovered through the learning loop. Read at the
> start of every iteration so knowledge persists across context windows.
> Tag entries with [CLAUDE.MD-CANDIDATE] if they should be promoted to
> CLAUDE.md by the human.

---

## Patterns Discovered

- StatCan CSVs have a BOM (`\ufeff`) — use `encoding="utf-8-sig"` when reading with pandas
- StatCan GEO columns include bracket codes like `"British Columbia [59]"` — strip with regex `r"\s*\[.*?\]"`
- StatCan suppression codes: `..`, `x`, `F`, `...`, empty string — all should become NaN
- BC Gov XLSX files have multi-panel layouts with NaN columns separating panels horizontally; stop at the first NaN gap after years start to extract just the first panel
- BC Gov jurisdiction XLSX has year columns as strings (`"2014"`) not integers — use flexible type checking
- Table 35-10-0184-01 is ~6 GB — must use chunked reading (`chunksize=500_000`)
- The national crime table (35-10-0177-01) uses violation codes in brackets like `[100]` — these are useful for programmatic filtering
- Province-level entries in national data have no comma in the GEO name (CMAs have commas)

## Gotchas & Pitfalls

- `openpyxl` version matters: pandas requires >= 3.1.5 for `read_excel()`. The system had 3.1.2 installed, causing silent failures in BC Gov XLSX parsing
- StatCan table `18-10-0005-01` is annual CPI, `18-10-0004-01` is monthly — the plan specified 0005 which is correct for this analysis
- The CPI table has multiple base-year series (1992=100, 2002=100) — must filter to `2002=100` for consistency
- **Policing expenditure data gap:** Table 35-10-0076-01 only has provincial expenditure through 2009. Post-2009 requires alternative sources. Table 35-10-0059-01 (2018-2023) is Canada-only, no provincial splits
- BC Gov jurisdiction data has `'-'` for suppressed values — these are already handled by the NaN conversion in the cleaner

## Architecture Decisions

- Used parquet for processed data: faster reads, type preservation, smaller files than CSV
- Separated download, clean, and analysis into distinct modules — allows re-running analysis without re-downloading
- Each analysis module (q1–q4) returns `(fig, narrative)` tuples — enables both standalone chart generation and notebook embedding
- Shared theme module (`theme.py`) ensures visual consistency across all 16+ charts
- Province colour assignments are fixed in `PROVINCE_COLOURS` dict — BC always blue, Canada always grey

## Missing Documentation

- The BC Gov XLSX files have ReadMe sheets with endnotes and data qualifiers that we don't parse — these contain important caveats about data collection changes
- [CLAUDE.MD-CANDIDATE] StatCan table numbers and their contents should be documented in CLAUDE.md for quick reference

## Dependencies & Relationships

- `src/clean.py` depends on `src/download.py` having been run first (reads from `data/raw/`)
- All `src/analysis/q*.py` modules depend on `src/clean.py` having been run (reads from `data/processed/`)
- `q3_costs.py` additionally depends on two StatCan tables (35100076, 35100059) that are not downloaded by the default `download.py` — the agent downloaded them separately
- The notebook (`bc_crime_report.ipynb`) imports from all four analysis modules
