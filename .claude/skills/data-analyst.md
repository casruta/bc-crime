# Data Analysis Skill

## What This Is

This skill documents everything learned from a real iterative improvement session
on a BC crime data analysis report (R Markdown). Over 19 iterations, the report
went from a quality score of 18/100 to 98/100. Every technique below was tested
empirically -- the ones that moved the needle are ranked first.

## What the Project Started As

The original `BC CRIME.Rmd` was a quick first project: 5 bar charts (3 of them
nearly identical copy-paste), zero narrative text, raw `print()` output, a bug
where 2018 data was labeled "2019", and an inconsistent title "Crime by Area 23".
No table of contents, no sections, no tables. Score: 18/100.

## What Actually Moved the Needle

### Tier 1: Massive Impact (got us from 18 to 72 in one iteration)

**1. Adding report structure was the single biggest win.**
A table of contents, numbered sections, and an introduction transformed a code
dump into something readable. This alone was worth more than any individual chart.
Use YAML front matter:
```yaml
output:
  html_document:
    toc: true
    toc_float: true
    theme: flatly
    code_folding: hide
    number_sections: true
```

**2. Fixing bugs before adding features.**
The title "Total Crimes by Neighbourhood in 2019" was on a chart showing 2018 data.
"Crime by Area 23" was meaningless. Fixing these two bugs added more credibility
than three new chart types combined. Always scan for title/data mismatches first.

**3. Replacing `print()` with `kable()` tables.**
```r
kable(data, caption = "Table 1: Annual crime counts",
      format.args = list(big.mark = ","))
```
This is cheap, fast, and transforms how professional the output looks.

**4. Creating a custom theme function.**
```r
theme_bc_crime <- function(base_size = 13) {
  theme_minimal(base_size = base_size) %+replace%
    theme(
      plot.title = element_text(face = "bold", size = rel(1.25)),
      plot.subtitle = element_text(color = "grey40"),
      plot.caption = element_text(color = "grey60"),
      panel.grid.minor = element_blank(),
      panel.grid.major.x = element_blank()
    )
}
```
Define once, use everywhere. Every chart instantly looks consistent.

**5. Adding narrative text between charts.**
Each section needs 2-3 sentences explaining *what* we're looking at and *why*.
A chart without context is decoration. A chart with context is analysis.

**6. Replacing 3 copy-paste bar charts with one faceted chart.**
The original had three nearly identical neighbourhood charts (2018, 2019, 2023).
One `facet_wrap(~ YEAR)` replaced all three and enabled direct visual comparison.

### Tier 2: Meaningful Impact (got us from 72 to 91)

**7. Diverse chart types (but stop at 7-8).**
The original only had bar charts. Adding line charts, heatmaps, area charts, bump
charts, and small multiples told different stories. But after ~8 types, each new
chart added less insight. The full set that worked well:
- Line chart (trends over time)
- Bar/column chart (comparisons)
- Stacked area (composition over time)
- Heatmap (two-dimensional patterns, e.g. crime type x year)
- Faceted small multiples (one panel per category)
- Bump chart (rank changes over time)
- Diverging bar (increase vs decrease)
- Lorenz/concentration curve (inequality analysis)

**8. Statistical context beyond raw counts.**
- Year-over-year percentage change with `safe_pct_change()` helper
- Reference lines showing averages on charts
- Severity-weighted index (not all crimes equal)
- Indexed comparison (base year = 100) for comparing different magnitudes
- Linear trend summary using `lm()`
- Correlation matrix between crime types
- Lorenz-style concentration curve for neighbourhood inequality

**9. Dynamic text generation with `glue`.**
```r
cat(glue::glue("Crime changed by **{change}%** from {year1} to {year2}."))
```
The executive summary, key findings, and "What to Watch" sections all auto-generate
from the data. The report updates itself when the data changes.

**10. An executive summary at the top.**
Key metrics in styled HTML cards so a reader can get the headline in 5 seconds
without scrolling. This was surprisingly high-impact for perceived quality.

### Tier 3: Polish (got us from 91 to 98)

**11. COVID-19 timeline annotation on the trend chart.**
A subtle shaded band and label on 2020 added historical context. Nice but only
worth about +1 point -- the reader can already see the dip.

**12. Custom CSS for HTML output.**
Styled table headers (blue background, white text), blockquote callout boxes,
print-friendly rules, and methodology section background. Makes the HTML output
look published.

**13. Data validation section.**
Automated PASS/WARNING checks for missing values, year continuity, and record
balance. Adds credibility that the analyst checked the data before analyzing it.

**14. Forward-looking "What to Watch" section.**
Auto-identifies the fastest-growing and fastest-declining crime types and
references the concentration analysis. Turns a retrospective report into
something actionable.

**15. Tabset panels for dense sections.**
```markdown
# Part 2: Crime Type Analysis {.tabset .tabset-fade}
## By Count
## Distribution
## Heatmap
```
Reduces scrolling and lets readers jump to what interests them.

**16. Spotlight deep-dive section.**
A worked example (Break-and-Enter: commercial vs residential) that shows how to
drill into one crime type. Serves as a template others can replicate.

**17. Dumbbell chart and correlation matrix.**
Novel chart types that tell specific stories (before/after comparison, which
crimes move together). Pushed visualization variety to near-maximum.

## What Did NOT Work (or was wasted effort)

1. **Adding charts past ~15** -- The report became overwhelming. More is not better.
2. **HTML stat cards** -- Looked great but didn't add analytical value. Pure decoration.
3. **Tabset panels** -- Improved UX but scored +0 on quality. They reorganize, not improve.
4. **Section numbering** -- Nice formatting touch but zero analytical impact.
5. **Over-annotating** -- Too many reference lines and labels made charts cluttered.

## The Critical Bug That Nearly Ruined Everything

In iteration 3, I added an Executive Summary section *before* the Setup/Data Loading
section. The summary used `crime_data`, `safe_pct_change()`, and `comma()` -- none
of which existed yet because packages hadn't been loaded and data hadn't been read.

**The report would have crashed on the very first chunk.** I didn't catch this until
iteration 13, when a code review pass finally checked execution order.

**Lesson: After ANY structural change in R Markdown, verify that chunks still
execute in dependency order.** This single bug was more impactful than 12 feature
iterations combined.

Checklist after restructuring:
- [ ] All `library()` calls before any function usage
- [ ] Data loading before any data reference
- [ ] Helper functions defined before use
- [ ] Cross-section variables (like `hood_change`) still defined before referenced

## The Improvement Curve

```
Score | What to do
------+-------------------------------------------------------------
0-30  | Fix bugs, add structure, format tables (30 min, huge gains)
30-70 | Narrative text, chart variety, custom theme (1 hour)
70-85 | Statistical depth, dynamic text, derived metrics (1 hour)
85-95 | Polish, CSS, project docs, deep-dives (1 hour)
95+   | Needs external data, interactivity, or new formats (unbounded)
```

The key insight: **80% of the value came from the first 3 iterations.** Structure,
bug fixes, and basic chart variety. Everything after that was incremental.

## Score Trajectory (All 19 Iterations)

| Iter | Score | Delta | What I Did |
|------|-------|-------|------------|
| 0    | 18    | --    | Baseline: 5 bar charts, bugs, no narrative |
| 1    | 72    | +54   | Structure, bug fixes, tables, chart variety |
| 2    | 82    | +10   | Severity index, bump chart, seasonal analysis |
| 3    | 88    | +6    | Executive summary, small multiples, Lorenz curve |
| 4    | 91    | +3    | COVID annotations, worksheet upgrade, README |
| 5    | 93    | +2    | Reusable helpers, indexed comparison |
| 6    | 94    | +1    | Custom CSS, severity weight table |
| 7    | 95    | +1    | Data validation section |
| 8    | 96    | +1    | Forward-looking "What to Watch" section |
| 9    | 96    | 0     | Tabset panels (UX only, no content gain) |
| 10   | 97    | +1    | Spotlight deep-dive on Break-and-Enter |
| 11   | 97    | 0     | Stale file cleanup |
| 12   | 97    | 0     | HTML stat cards (visual polish only) |
| 13   | 97    | --    | **Critical bug fix**: exec summary ordering |
| 14   | 97    | 0     | Dumbbell chart (diminishing returns) |
| 15   | 97    | 0     | Section numbering |
| 16   | 98    | +1    | Linear trend analysis |
| 17   | 98    | 0     | Correlation matrix |
| 18   | 98    | 0     | Auto-generated correlation interpretation |
| 19   | 98    | 0     | Dynamic report footer |

## Phase 2: Beyond the 100-Point Ceiling (Iterations 20-37)

After hitting 98/100, a new 150-point rubric was created adding: Project Organization,
Robustness, Contextual Depth, and Reproducibility dimensions.

### What Worked in Phase 2

**1. Folder restructuring was the single biggest Phase 2 win (+12 points).**
Moving from `BC Crime Data/Data Sets/` to `src/data/output/docs/` with a proper
`.gitignore` added instant professionalism and made the project navigable.

**2. Parameterization compounds (+5 points).**
Creating a config chunk with YAML params meant every subsequent change
was automatically flexible. One change propagated to 15+ locations.

**3. Statistical tests add credibility cheaply (+5 points).**
Adding p-values, confidence intervals, and a chi-squared test took ~20 lines
each but transformed the report from descriptive to analytical.

**4. Neighbourhood clustering was novel and high-impact (+3 points).**
Ward's hierarchical clustering on crime proportions revealed patterns
not visible in any single chart---genuine new insight from ~40 lines of code.

**5. Context sections turned analysis into intelligence (+3 points).**
Adding BC population context, national comparisons, and policy references
made the report useful for decision-makers, not just analysts.

**6. Comprehensive methodology equals reproducibility (+3 points).**
Expanding from 8 lines to a full section with variable definitions, methods table,
limitations, and session info made the report citable.

### Phase 2 Score Trajectory

| Iter | Score | Delta | What I Did |
|------|-------|-------|------------|
| 20   | 110   | +12   | Project restructure: src/data/output/docs layout |
| 21   | 112   | +2    | .gitignore for outputs, data, R session files |
| 22   | 116   | +4    | Robust data loading with file/column validation |
| 23   | 121   | +5    | Parameterize ~15 hardcoded values via config chunk |
| 24   | 124   | +3    | Reusable helpers (get_top_n, add_covid_band, format_change) |
| 25   | 128   | +4    | Expand data validation from 3 to 8 checks |
| 26   | 133   | +5    | Statistical tests (p-values, CI, chi-squared) |
| 27   | 137   | +4    | Trend projection (Part 6) with fan chart |
| 28   | 140   | +3    | Neighbourhood clustering (Ward's D2 hierarchical) |
| 29   | 143   | +3    | Broader context section |
| 30   | 145   | +2    | Abstract, inter-section transition callouts |
| 31   | 148   | +3    | Expanded methodology with methods table |
| 32   | 150   | +2    | Glossary, appendix tables, references |
| 33-37| 150   | 0     | Polish: CSS, accessibility, DT tables, YAML params, docs |

## Files Changed

| File | What Changed |
|------|-------------|
| `src/BC-CRIME.Rmd` | 156 → ~1700 lines. 6 analysis parts, 18+ chart types, statistical tests, clustering, projections, interactive tables, parameterized |
| `src/BC-CRIME-Worksheet.Rmd` | Exploration template with reusable code blocks |
| `src/custom.css` | Responsive, accessible, print-friendly styling |
| `README.md` | Full documentation with parameterized report instructions |
| `docs/improvement_log.md` | 37-iteration history across two rubrics |
| `.gitignore` | Excludes outputs, data, R session files |
