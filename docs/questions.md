# Expert Review Questions & Answers

> Each iteration, Claude adopts expert personas and generates hard questions
> about the codebase, then investigates to answer them. Grouped by date and
> iteration number. Reference specific files, functions, and line numbers.

---

## 2026-03-16 — Iteration 1 (Data Pipeline)

### Senior Developer
**Q: What encoding does StatCan use for CSV exports?**
A: UTF-8 with BOM (`\ufeff`). Pandas handles this with `encoding="utf-8-sig"`. Confirmed by inspecting raw files — all have the BOM byte prefix.

**Q: How do BC Gov XLSX files structure multi-panel data?**
A: Horizontally — Row 0 has panel headers ("Number of Offences", "Offences Cleared", etc.), separated by NaN columns. Year headers are in Row 2 for the trends file. The jurisdiction file uses Row 1 as headers with columns REGION, TYPE OF POLICING, POLICING JURISDICTION, then year columns as strings.

### Security Engineer
**Q: Are we downloading from HTTPS endpoints?**
A: Yes. All StatCan URLs use `https://www150.statcan.gc.ca/` and BC Gov uses `https://www2.gov.bc.ca/`. No authentication required — public data.

### Product Manager
**Q: What is the minimum viable dataset to answer all four questions?**
A: The national table (35-10-0177-01) alone can answer Q1 and Q2 for BC at the province level. Q4 geography requires the BC Gov jurisdiction files. Q3 costs requires the expenditure tables. The 6 GB BC-specific table (35-10-0184-01) provides granularity but is not strictly required for province-level analysis.

## 2026-03-16 — Iteration 2 (Analysis)

### Code Reviewer
**Q: Is the chart generation pattern consistent across modules?**
A: Yes. Every chart function follows the pattern: `def chart_xxx(save_path=None) -> tuple[plt.Figure, str]`. Each calls `apply_theme()` first, generates the chart, produces a narrative string from the data, and optionally saves via `save_fig()`. The `run_all()` function orchestrates all charts in each module.

### DevOps Engineer
**Q: How reproducible is the pipeline end-to-end?**
A: Fully reproducible from a clean state: `python -m src.download && python -m src.clean && python -m src.analysis.q1_is_crime_rising` etc. Data downloads are deterministic (same StatCan tables, versioned by table ID). The 6 GB file is skipped by default in clean.py (`skip_large=True` in `__main__`).

### End User
**Q: Can the charts be regenerated without re-downloading data?**
A: Yes. Downloads go to `data/raw/`, cleaning produces `data/processed/` parquet files, and analysis reads only from `data/processed/`. Each stage is independent. You only need to re-download if you want updated data.
