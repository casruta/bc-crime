# Exploring the Crime Landscape in British Columbia

**A data-driven analysis of crime severity, composition, policing costs, and geographic distribution across BC (1998–2024)**

*Kacper Ruta | Data sourced from Statistics Canada and the BC Ministry of Public Safety*

---

## Executive Summary

1. **Crime is down dramatically from its peak** — BC's Crime Severity Index fell from 178 in 1998 to a trough of 90 in 2014, a 49% decline. After a modest rebound, the 2024 reading of 92 shows a 7.4% year-over-year drop, but BC remains 21% above the national average.
2. **The composition of crime is shifting** — Property crime (51% of all offences) continues to decline, with theft from motor vehicles down 772 per 100,000 over five years. But child exploitation offences (+82/100k) and shoplifting (+79/100k) are rising sharply.
3. **Policing costs have diverged from crime rates** — Between 1998 and 2009, real per-capita policing expenditure rose to 149% of its starting level while the CSI fell to 67%. BC spent $253 per capita on policing in 2009 — below the national average of $365.
4. **Geography matters more than population** — Interior CMAs like Chilliwack (11,352/100k) and Kamloops (10,546/100k) have roughly double the per-capita crime rate of Vancouver (5,438/100k) and Victoria (5,283/100k).

---

## 1. Is Crime Rising?

BC's overall Crime Severity Index has followed a clear arc: a sustained decline from the late 1990s through 2014, a partial rebound peaking around 2019, and a renewed decline through 2024. The total CSI dropped from 178 in 1998 to 90 in 2014 — a 49% reduction — before climbing back above 100 in the late 2010s. The most recent data shows a 7.4% year-over-year decline to 92 in 2024.

What makes the recent period notable is the divergence between violent and non-violent CSI. While the non-violent index has tracked closely with the overall downward trend, the violent CSI has risen more steeply since 2014, suggesting a compositional shift toward more serious offences even as overall severity falls.

![BC Crime Severity Index 1998–2024, showing total, violent, and non-violent CSI trends](outputs/charts/q1_bc_csi_trend.png)
*Figure 1. BC's Crime Severity Index by component, 1998–2024. The total CSI (dark blue) fell 49% from peak to trough before stabilizing. The violent CSI (red) has risen relative to non-violent since 2014. Source: Statistics Canada, Table 35-10-0063-01.*

Placing BC in a national context, every major province experienced the same broad pattern — a peak around 2003, decline through the mid-2010s, and a plateau or slight rise since. However, the absolute levels differ substantially. Saskatchewan's offence rate consistently runs roughly double Ontario's. BC sits above the national average, closer to Alberta and Manitoba, with a 2024 rate around 7,000 per 100,000 population compared to the national figure of approximately 5,500.

![Criminal Code offence rates per 100,000 population for six provinces, 1998–2024](outputs/charts/q1_provincial_comparison.png)
*Figure 2. Criminal Code offence rates (excluding traffic) per 100,000 population across six provinces. BC's rate declined from 12,000+ in 1998 to roughly 7,000 by 2024 but remains above the national average. Source: Statistics Canada, Table 35-10-0177-01.*

---

## 2. What Kinds of Crime Are Changing?

The stacked composition chart reveals a story dominated by property crime, which accounts for roughly 51% of all Criminal Code offences in BC. Property crime rates have fallen steadily from over 10,000 per 100,000 in the early 2000s to under 4,000 by 2024. Violent crime, while lower in absolute terms, has held relatively stable — meaning its share of total crime has grown as property offences decline.

Administration of justice violations (bail breaches, failure to appear) represent a growing category, while drug offences have contracted significantly following federal policy changes.

![Stacked area chart showing BC crime composition by category from 2000 to 2024](outputs/charts/q2_stacked_composition.png)
*Figure 3. BC crime composition by category (rate per 100,000), 2000–2024. Property crime dominates but is declining, while violent crime holds steady and grows as a share of total offences. Source: Statistics Canada, Table 35-10-0177-01.*

The most revealing view is the absolute rate change over the last five years (2019–2024). Theft from motor vehicles saw the single largest decline at -772 per 100,000, followed by breaking and entering (-270) and theft under $5,000 (-221). On the other side, child pornography offences increased by 82 per 100,000 and shoplifting by 79 per 100,000 — both concerning trends that warrant targeted policy attention.

Other notable declines include disturbing the peace (-165), impaired driving (-108), mischief (-80), breach of probation (-67), and level 1 assault (-66).

![Horizontal bar chart showing the 10 offences with the largest absolute rate changes, 2019–2024](outputs/charts/q2_top_changes.png)
*Figure 4. Top 10 violations by absolute rate change, 2019–2024. Eight of the ten largest movers are declining offences (teal); the two increases — child exploitation and shoplifting — stand out in red. Source: Statistics Canada, Table 35-10-0177-01.*

---

## 3. What Does Policing Cost?

One of the most striking findings in this analysis is the divergence between crime severity and policing expenditure. When both metrics are indexed to 1998 = 100, the lines move in opposite directions: the CSI fell steadily to 67% of its 1998 level by 2009, while real per-capita policing costs climbed to 149%. Crime went down; costs went up.

This pattern raises important questions about policing efficiency and resource allocation. It may reflect rising labour costs, expanded mandates (cybercrime, mental health calls), or structural factors in police contracts — but the divergence is substantial and sustained.

![Indexed comparison of CSI and per-capita policing cost, both set to 1998 = 100](outputs/charts/q3_csi_vs_expenditure.png)
*Figure 5. Crime Severity Index vs. per-capita policing cost, indexed to 1998 = 100 (constant 2020 dollars). By 2009, crime severity had fallen to 67% of its 1998 level while policing costs rose to 149%. Source: Statistics Canada, Tables 35-10-0059-01 and 18-10-0005-01.*

Despite this growth, BC's per-capita policing cost remains below most peer provinces. At $253 per capita in 2009 (the most recent year with provincial-level data), BC ranked below the national average of $365 and well below Ontario ($303). Only Saskatchewan ($247), Alberta ($249), and the Atlantic provinces spent less per person on policing.

![Horizontal bar chart comparing per-capita policing costs across Canadian provinces, 2009](outputs/charts/q3_per_capita_comparison.png)
*Figure 6. Per-capita policing cost by province, 2009 (nominal dollars). BC's $253 sits below the national average of $365 and below Ontario's $303. Source: Statistics Canada, Table 35-10-0076-01.*

---

## 4. Where Is Crime Concentrated?

Raw offence counts are dominated by population — Vancouver (48,812 offences) and Surrey (41,275) account for the largest volumes simply because they are the most populous jurisdictions. But per-capita rates tell a fundamentally different story.

Among BC's Census Metropolitan Areas, Chilliwack leads at 11,352 offences per 100,000 population, followed by Kamloops (10,546), Nanaimo (9,365), and Kelowna (8,922). The large coastal metros that dominate headlines — Vancouver (5,438) and Victoria (5,283) — sit at the bottom of the ranking. Interior and smaller CMAs consistently record per-capita crime rates roughly double those of the major urban centres.

This pattern likely reflects a combination of economic conditions, homelessness concentration, substance use crises, and differences in policing models between RCMP-policed and municipally policed jurisdictions.

![Horizontal bar chart showing per-capita crime rates across BC CMAs, 2024](outputs/charts/q4_cma_comparison.png)
*Figure 7. Criminal Code offence rate per 100,000 population across BC Census Metropolitan Areas, 2024. Interior CMAs (Chilliwack, Kamloops) record rates more than double those of Vancouver and Victoria. Source: Statistics Canada, Table 35-10-0177-01.*

A scatter plot of total offences against violent offences across all BC jurisdictions reveals a near-perfect linear relationship (r = 0.99). Jurisdictions with more crime overall do not simply have more property crime — they have proportionally more violent crime as well. Vancouver and Surrey stand apart in the upper right, while the remaining jurisdictions cluster along the same trend line.

![Scatter plot of total vs. violent Criminal Code offences by BC jurisdiction, 2023](outputs/charts/q4_total_vs_violent.png)
*Figure 8. Total vs. violent Criminal Code offences by jurisdiction, 2023. The correlation coefficient of r = 0.99 indicates a near-perfect linear relationship — higher-crime jurisdictions experience proportionally more violent offences, not just more property crime. Source: BC Government, Appendix data.*

---

## Methodology

### Data Sources

| Source | Table / Reference | Coverage | Used In |
|--------|-------------------|----------|---------|
| Statistics Canada | 35-10-0063-01 | Crime Severity Index by police service | Section 1 |
| Statistics Canada | 35-10-0177-01 | Incident-based crime statistics by province and CMA | Sections 1, 2, 4 |
| Statistics Canada | 35-10-0076-01 | Police personnel and expenditures | Section 3 |
| Statistics Canada | 35-10-0059-01 | Police services expenditures | Section 3 |
| Statistics Canada | 18-10-0005-01 | Consumer Price Index (CPI) | Section 3 (inflation adjustment) |
| BC Government | Appendix F–I (2014–2023) | Jurisdiction-level crime statistics | Section 4 |

### Key Metrics

- **Crime Severity Index (CSI)**: A Statistics Canada measure that weights offences by their average sentence length, giving more serious crimes greater influence on the index. Base year: 2006 = 100.
- **Per-capita rate**: Criminal Code offences per 100,000 population, excluding traffic violations.
- **Real (CPI-adjusted) expenditure**: Policing costs converted to constant 2020 dollars using the all-items CPI to enable meaningful comparison across years.

---

## Caveats

1. **Police-reported data only** — These statistics reflect crimes reported to and recorded by police. They do not capture unreported crime, which varies significantly by offence type (e.g., sexual assault is heavily underreported).
2. **COVID-19 disruption** — The 2020–2021 period shows anomalous patterns due to lockdowns, reduced mobility, and changes in reporting behaviour. Trends spanning this period should be interpreted with caution.
3. **Expenditure data gap** — Statistics Canada's provincial-level policing expenditure data (Table 35-10-0059-01) ends at 2009. Post-2009 cost analysis relies on national aggregates only.
4. **CMA boundary changes** — Census Metropolitan Area definitions shift between census cycles, which can affect per-capita rate comparisons over long periods.
5. **Counting rules** — Statistics Canada uses the most-serious-offence rule: when multiple offences occur in a single incident, only the most serious is counted. This systematically undercounts less serious offences.
6. **Jurisdiction coverage** — BC Government appendix data covers the largest municipal police services and RCMP detachments but may not include all smaller jurisdictions.

---

<details>
<summary><strong>Technical Details</strong> (project structure, reproduction steps, additional charts)</summary>

### Quick Start

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

Charts are saved to `outputs/charts/`. Open `notebooks/bc_crime_report.ipynb` for the full interactive narrative report.

### Project Structure

```
src/
  download.py                 # Fetch all raw data from StatCan and BC Gov
  clean.py                    # Parse, normalize, save to parquet
  analysis/
    theme.py                  # Shared chart theme and palette
    q1_is_crime_rising.py     # CSI trends, provincial comparison
    q2_what_kinds.py          # Crime type breakdown
    q3_costs.py               # Policing expenditure analysis
    q4_geography.py           # Jurisdiction and CMA analysis
data/
  raw/                        # Downloaded files (gitignored)
  processed/                  # Cleaned parquet files (gitignored)
notebooks/
  bc_crime_report.ipynb       # Full narrative report
outputs/
  charts/                     # Generated PNG charts (16 files)
tests/
  test_download.py            # Download verification tests
  test_clean.py               # Data quality tests
```

### Additional Charts (not embedded above)

The analysis pipeline generates 16 charts in total. The 8 charts not shown above are:

| File | Description |
|------|-------------|
| `q1_bc_yoy_trend.png` | Year-over-year percentage change in BC's CSI |
| `q1_yoy_by_province.png` | YoY CSI changes compared across provinces |
| `q2_heatmap.png` | Heatmap of offence rates by category and year |
| `q2_slope_ranking.png` | Slope chart ranking crime categories by rate change |
| `q3_bc_expenditure_trend.png` | BC policing expenditure trend (nominal vs real dollars) |
| `q3_expenditure_breakdown.png` | Canada-wide policing expenditure by component |
| `q4_jurisdiction_trends.png` | Crime trends for top 8 BC jurisdictions (2014–2023) |
| `q4_top_jurisdictions.png` | Jurisdictions ranked by total offence volume |

### R Markdown Report (legacy)

An earlier R-based analysis covering 2018–2023 is available in `BC Crime Data/Data Sets/BC CRIME.Rmd`. Open in RStudio and click **Knit** to generate the HTML report.

### Requirements

- **Python track:** Python 3.12+, see `requirements.txt`
- **R track (legacy):** R >= 4.0, ggplot2, dplyr, tidyr, scales, knitr, rmarkdown, glue

</details>

---

*Data: Statistics Canada (Tables 35-10-0063-01, 35-10-0177-01, 35-10-0076-01, 35-10-0059-01, 18-10-0005-01) and BC Ministry of Public Safety. Analysis and visualizations by Kacper Ruta, 2024–2026.*
