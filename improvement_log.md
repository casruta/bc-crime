# Visualization & Report Quality Improvement Log

## Scoring Rubric (0-100)

| Dimension | Max | Description |
|---|---|---|
| Visualization Variety | 15 | Diversity of chart types (line, bar, heatmap, area, etc.) |
| Title/Label Accuracy | 10 | Correct, consistent, descriptive titles and labels |
| Narrative/Analysis | 15 | Explanatory text, context, interpretation |
| Code Quality (DRY) | 10 | No copy-paste, reusable functions, clean structure |
| Theme/Styling Consistency | 10 | Unified visual identity, coherent color palette |
| Statistical Depth | 15 | Rates, trends, comparisons, derived metrics |
| Report Structure | 10 | TOC, sections, logical flow, navigation |
| Data Presentation | 10 | Formatted tables, summaries, column descriptions |
| Accessibility | 5 | Labels, annotations, colorblind-safe palettes |

## Score Trajectory

| Iteration | Score | Delta | Approach |
|-----------|-------|-------|----------|
| Baseline  | 18    | --    | Original code |
| 1         | 72    | +54   | Structure, narrative, bug fixes, tables, new chart types |
| 2         | 82    | +10   | Statistical depth, severity index, bump chart |
| 3         | 88    | +6    | Executive summary, small multiples, Lorenz curve |
| 4         | 91    | +3    | Interpretive depth, COVID annotations, project polish |
| 5         | 93    | +2    | Reusable helpers, indexed comparison, proportional bar |
| 6         | 94    | +1    | Custom CSS, severity weight table |
| 7         | 95    | +1    | Data validation section, data-analyst skill |
| 8         | 96    | +1    | Forward-looking analysis, cross-references |

## Iteration History

### Baseline (Original) - Score: 18/100
- 5 bar charts only (3 near-identical copy-paste)
- Bug: 2018 data labeled "2019"
- Inconsistent title: "Crime by Area 23"
- Zero narrative text
- Raw print() output
- No sections, TOC, or structure

### Iteration 1 - Score: 72/100 (+54)
**What worked:**
- Adding report structure with TOC, sections -> huge readability gain
- Replacing raw print() with kable tables -> professional feel
- Line chart for trends -> better storytelling than bars alone
- YoY change chart with red/green -> instant insight
- Custom theme function -> visual consistency
- Faceted neighbourhood comparison -> eliminated 3 copy-paste charts

**What didn't work as well:**
- Heatmap text labels too small at lower proportions
- Area chart hard to read with many overlapping types
- No statistical context (averages, reference lines)

### Iteration 2 - Score: 82/100 (+10)
**What worked:**
- Severity index -> adds analytical depth beyond counts
- Bump chart for rank changes -> novel, compelling
- Dynamic key takeaways -> report feels alive
- Methodology notes -> adds credibility
- Average line on homicide chart -> context for interpretation
- Conditional monthly analysis -> graceful degradation

**What didn't work as well:**
- Severity weights are arbitrary - acknowledged more clearly
- Too many charts could overwhelm reader
- Still missing executive summary

### Iteration 3 - Score: 88/100 (+6)
**What worked:**
- Executive summary table at top -> immediate value for skimmers
- Small multiples -> every crime type visible independently
- Lorenz curve -> novel statistical insight
- Heatmap contrast fix -> genuinely improved readability

**What didn't work as well:**
- Diminishing returns on adding more chart types
- Scoring plateau approaching
- Decision: switch approach from "more charts" to "deeper interpretation"

### Iteration 4 - Score: 91/100 (+3)
**New approach: interpretive depth + project polish**

**What worked:**
- COVID-19 annotation -> adds historical context that pure data can't show
- Neighbourhood crime profiles heatmap -> genuinely new analytical insight
- Worksheet upgrade -> makes project usable for others
- README rewrite -> project is now self-documenting

**What didn't work as well:**
- Smaller delta (+3) suggests we're near the ceiling for this project
- Further improvements need external data (population for per-capita rates)
- Interactive elements (plotly) would help but adds dependency complexity

## Lessons Learned

### High-Impact Patterns (apply first)
1. **Structure > individual chart quality** - The biggest single improvement (+54)
   came from organizing content with headers, TOC, and narrative text
2. **Fix bugs before adding features** - Correcting the 2018/2019 title mislabel
   was higher-value than adding a new chart
3. **Replace raw output with formatted tables** - print() -> kable() is always
   worth doing; it's a cheap, high-impact change
4. **Custom theme function** - Define once, apply everywhere. This compounds over
   every subsequent chart added

### Medium-Impact Patterns (apply second)
5. **Context beats decoration** - Reference lines, averages, % labels add more
   value than fancy color schemes or animations
6. **Dynamic text generation** - Using glue/inline R to auto-generate findings
   makes reports feel alive and reduces maintenance
7. **DRY code compounds** - Helper functions + shared theme = every new chart
   starts at higher quality automatically
8. **Conditional execution** - eval=has_column patterns handle missing data
   gracefully without crashing

### Low-Impact / Diminishing Returns
9. **Adding more chart types** - After 6-7 diverse types, each additional one
   yields diminishing insight per visual
10. **Over-annotation** - Too many labels and reference lines can clutter
11. **Interpretive annotations** - COVID bands are nice but only +1 point;
    the reader can see the dip themselves

### Key Insight: The Improvement Curve
- **Phase 1 (0-70):** Structure, bug fixes, and basic chart variety yield
  massive gains. This is where 80% of the value lives.
- **Phase 2 (70-85):** Statistical depth and novel analyses (severity, Lorenz)
  add meaningful analytical value.
- **Phase 3 (85-92):** Interpretive polish, project-level documentation, and
  cross-cutting analyses provide small but real improvements.
- **Phase 4 (92+):** Requires external data, interactivity, or fundamentally
  different output formats to push further.

## Final Detailed Score Breakdown (Iteration 8)

| Dimension | Baseline | Final | Max | Notes |
|---|---|---|---|---|
| Visualization Variety | 3 | 14 | 15 | 11 chart types: line, bar, area, heatmap x3, facet, bump, small mult, Lorenz, indexed, proportional |
| Title/Label Accuracy | 3 | 10 | 10 | All titles correct, consistent, dynamic |
| Narrative/Analysis | 0 | 14 | 15 | Exec summary, section intros, cross-refs, what-to-watch, methodology |
| Code Quality (DRY) | 2 | 9 | 10 | Custom theme, helpers, named palette, no copy-paste |
| Theme/Styling Consistency | 4 | 9 | 10 | Unified theme, custom CSS, consistent colors |
| Statistical Depth | 2 | 14 | 15 | YoY%, severity, concentration, indexed, data validation |
| Report Structure | 1 | 10 | 10 | TOC, 5 parts, exec summary, methodology, what-to-watch |
| Data Presentation | 1 | 9 | 10 | 8+ tables, column summary, quality checks, dynamic text |
| Accessibility | 2 | 5 | 5 | Viridis + Set2, heatmap contrast, labeled annotations |
| **TOTAL** | **18** | **96** | **100** | **+78 points over 8 iterations** |
