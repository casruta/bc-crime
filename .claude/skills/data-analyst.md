# Data Analyst Skill - Visualization & Report Quality Improvement

## When to Use
Use this skill when improving data analysis reports, R Markdown files, Jupyter
notebooks, or any data visualization project. The patterns below are ranked by
impact (highest first) based on empirical testing.

## Phase 1: High-Impact Fixes (Score +50 points typical)

These changes yield the most improvement per effort:

### 1. Add Report Structure
- Add YAML front matter with TOC, theme, code folding
- Organize into numbered sections with headers
- Add introduction and methodology sections
- **Why it works:** Structure is the #1 driver of perceived quality

### 2. Fix Bugs First
- Check all chart titles match their data (common: wrong year in title)
- Verify axis labels are descriptive and accurate
- Check for copy-paste errors in repeated chart blocks
- **Why it works:** Bugs destroy credibility faster than missing features

### 3. Replace Raw Output with Formatted Tables
- `print()` -> `kable()` with captions and number formatting
- Add `format.args = list(big.mark = ",")` for readability
- Number tables sequentially: "Table 1:", "Table 2:", etc.
- **Why it works:** Tables are the most-read part of reports

### 4. Create a Custom Theme Function
```r
theme_project <- function(base_size = 13) {
  theme_minimal(base_size = base_size) %+replace%
    theme(
      plot.title = element_text(face = "bold", size = rel(1.25)),
      plot.subtitle = element_text(color = "grey40"),
      # ... consistent across all charts
    )
}
```
- **Why it works:** Applies quality uniformly to every chart

### 5. Add Narrative Text Between Charts
- Each section needs 2-3 sentences explaining what we're looking at and why
- Charts without context are decoration; charts with context are analysis
- **Why it works:** Transforms a chart dump into an analytical report

## Phase 2: Medium-Impact Improvements (Score +15 points typical)

### 6. Diversify Visualization Types
Don't use only bar charts. Good variety for data analysis reports:
- Line charts for trends over time
- Heatmaps for two-dimensional patterns
- Faceted/small multiples for comparing categories
- Diverging bars for increase/decrease comparisons
- Area charts for composition over time
- **Stop at 7-8 types** - more is diminishing returns

### 7. Add Statistical Context
- Reference lines (averages, medians)
- Year-over-year percentage change calculations
- Indexed comparisons (base year = 100)
- Derived metrics (severity scores, concentration curves)
- **Why it works:** Moves from description to analysis

### 8. Dynamic Text Generation
```r
cat(glue::glue("Total crimes changed by **{change}%** from {year1} to {year2}."))
```
- Auto-generate key findings from the data
- Add an Executive Summary at the top
- **Why it works:** Report updates itself when data changes

### 9. Add Helper Functions
- `safe_pct_change()` to avoid Inf/NaN
- Reusable chart builders for repeated patterns
- Define color palettes as named constants
- **Why it works:** DRY code = fewer bugs + easier iteration

## Phase 3: Polish (Score +5 points typical)

### 10. Conditional Execution
```r
has_column <- "MONTH" %in% names(data)
# then use eval=has_column in chunk options
```

### 11. Accessibility
- Use colorblind-safe palettes (viridis, Set2)
- Add data labels on charts
- Ensure text contrast on heatmaps (dark on light, white on dark)

### 12. Custom CSS for HTML Output
- Style table headers, blockquotes, figure captions
- Add print-friendly rules
- Subtle background on methodology sections

## Critical: Execution Order Review

**ALWAYS verify chunk execution order after structural changes.** In R Markdown,
chunks execute top-to-bottom. If you move a section that uses `crime_data` before
the chunk that loads it, the entire report will fail to render. This is the single
most common critical bug in R Markdown refactoring.

Checklist after any restructuring:
- [ ] All `library()` calls before any function usage
- [ ] Data loading before any data reference
- [ ] Helper functions defined before use
- [ ] Cross-section variable dependencies still resolve

## Data Project Organization

### Path Constants
- **Always centralize path constants** in a single `src/paths.py` (or equivalent) file
- Never define `Path(__file__).resolve().parent...` in individual modules — import from the central file
- Standard constants: `PROJECT_ROOT`, `RAW_DIR`, `PROCESSED_DIR`, `CHARTS_DIR`
- All modules import from this single source of truth
- **Why it works:** Eliminates drift when directories change; one edit updates everything

### Raw Data Directory Structure
- **Organize raw data by source**, not by file type
- Pattern: `data/raw/<source>/` (e.g., `data/raw/statscan/`, `data/raw/bcgov/`)
- Keep metadata files alongside their data files in the same source directory
- Download scripts should route files to source-specific subdirectories by default
- Maintain backward compatibility: when a `dest` parameter is provided (e.g., in tests), route all files to that single directory
- **Why it works:** Prevents flat-directory sprawl; makes provenance obvious at a glance

### Data Dictionary (`data/README.md`)
Every data project must have a `data/README.md` with:
1. **Overview** — purpose, how to regenerate (download + clean commands)
2. **Raw Data Sources** — table per source with: ID, filename, description, coverage, size, URL, formal citation
3. **Cleaning Pipeline** — step-by-step transformations (column normalization, code stripping, coercion, drops)
4. **Processed Files Schema** — for each output file: column name, type, description, example value
5. **Data Lineage** — ASCII diagram showing raw source -> cleaning function -> processed output
6. **External References** — any external sources cited in analysis (e.g., survey data, reports)
- **Why it works:** New contributors can understand the data without reading code; citations prevent "where did this come from?" questions

### Chart Index (`outputs/charts/README.md`)
- Table mapping every output file to: figure number, section, generating function, primary data source
- Include both numbered figures (from the report) and supplementary/interactive outputs
- **Why it works:** Bridges the gap between filenames and the narrative report

### Naming & Jurisdiction Mappings
- When working with data from multiple sources that use different names for the same entities, create an explicit mapping table (e.g., `JURISDICTION_MAP` linking BC Gov names to StatCan GEO names)
- Export the mapping as a processed file for downstream use
- Document the full mapping in the data dictionary

## Anti-Patterns (What Doesn't Work)

1. **Adding more charts past 15** - Overwhelming, not insightful
2. **Over-annotating** - Too many reference lines and labels = clutter
3. **Pie charts** - Use proportional bars instead
4. **Interactive features in static reports** - Adds complexity without value
5. **Perfect before good** - Ship at 85/100, not 100/100

## The Improvement Curve

| Score Range | Focus | Typical Effort |
|-------------|-------|----------------|
| 0-30 | Fix bugs, add structure | 30 min |
| 30-70 | Tables, narrative, chart variety | 1 hour |
| 70-85 | Statistical depth, dynamic text | 1 hour |
| 85-95 | Polish, CSS, project docs | 1 hour |
| 95-100 | Needs external data or interactivity | Unbounded |
