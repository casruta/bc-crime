# Exploring the Crime Landscape in British Columbia

**A data-driven analysis of crime severity, composition, justice system effectiveness, and geographic distribution across BC (2004--2024)**

*Kacper Ruta | Data sourced from Statistics Canada and the BC Ministry of Public Safety*

---

## Table of Contents

1. [Key Findings at a Glance](#key-findings-at-a-glance)
2. [Is Crime Rising?](#1-is-crime-rising)
3. [What Kinds of Crime Are Changing?](#2-what-kinds-of-crime-are-changing)
4. [How Effectively Is Crime Being Addressed?](#3-how-effectively-is-crime-being-addressed)
5. [Where Is Crime Concentrated?](#4-where-is-crime-concentrated)
6. [Why Does Crime Feel Like It's Rising?](#5-why-does-crime-feel-like-its-rising)
7. [Methodology](#methodology)
8. [Caveats](#caveats)
9. [Technical Details](#technical-details)

---

## Key Findings at a Glance

> 1. **BC's Crime Severity Index fell ~46%** from its 2004 peak to a trough of 90 in 2014. The 2024 reading of 92 reflects a **7.4% year-over-year decline**, but BC remains roughly **21% above the national average**.
> 2. **Violent and non-violent CSI have converged.** The violent-to-non-violent ratio rose from ~0.73 in the mid-2000s to approximately **1.0** -- violent and non-violent severity are now roughly equal.
> 3. **Property crime's share dropped from 64% to 51%** over two decades; violent crime's share **grew from 12% to 20%**, a compositional shift toward more serious offences.
> 4. **Child exploitation offences (+82/100k) and shoplifting (+79/100k)** are the sharpest rising categories, while theft from motor vehicles fell by **-772/100k** over five years.
> 5. **Drug offences are declining fastest** (CAGR of -8.3%); violent crime is declining slowest (CAGR of -0.8%), reinforcing the compositional shift.
> 6. **Interior CMAs have roughly double** the per-capita crime rate of coastal metros -- Chilliwack (11,352/100k) and Kamloops (10,546/100k) vs. Vancouver (5,438/100k) and Victoria (5,283/100k).
> 7. **Crime is extremely concentrated**: just **5% of jurisdictions account for 50%** of all Criminal Code offences; 19% account for 80%.
> 8. **Total and violent offences correlate at r = 0.99** across jurisdictions -- high-crime areas have proportionally more violent crime, not just more property crime.
> 9. **42% of BC residents believe crime increased** in their neighbourhood (GSS 2019), yet the Crime Severity Index was ~40% below its peak — a persistent perception-reality gap driven by media salience, visible disorder, and selective recall.

---

## 1. Is Crime Rising?

BC's Crime Severity Index traces a clear arc: sustained decline through 2014, partial rebound peaking around 2019, renewed decline through 2024. The latest data shows a 7.4% year-over-year drop to a CSI of 92.

The striking feature of the recent period is the divergence between violent and non-violent CSI. The non-violent index tracked the overall downward trend, but the violent CSI climbed more steeply since 2014 — evidence of a compositional shift toward more serious offences even as overall severity fell.

![BC Crime Severity Index, showing total, violent, and non-violent CSI trends](outputs/charts/q1_bc_csi_trend.png)
*Figure 1. BC's Crime Severity Index by component. The total CSI (dark blue) fell 46% from peak to trough before stabilizing. The violent CSI (red) rose relative to non-violent since 2014. Source: Statistics Canada, Table 35-10-0063-01.*

The violent-to-non-violent CSI ratio quantifies this shift. It bottomed at 0.73 in the mid-2000s and has since climbed to approximately 1.0 — violent and non-violent crime severity are now roughly equal, where two decades ago non-violent crime dominated.

![Violent vs non-violent CSI ratio over time](outputs/charts/q1_violent_nonviolent_gap.png)
*Figure 2. Ratio of violent to non-violent CSI. A rising ratio confirms the compositional shift toward more serious offences. When the ratio exceeds 1.0, violent crime severity surpasses non-violent. Source: Statistics Canada, Table 35-10-0063-01.*

Year-over-year changes reveal the rhythm more clearly. Declining years dominate from 2004 to 2014, while rising years cluster around 2015--2019 — coinciding with the opioid crisis and rising property crime in the Lower Mainland. The most recent year confirms the renewed downward trend.

![Year-over-year percentage change in BC's crime rate](outputs/charts/q1_bc_yoy_trend.png)
*Figure 3. Year-over-year percentage change in BC's Criminal Code offence rate. The 2004--2014 period shows near-continuous decline; the post-2019 trend is again downward. Source: Statistics Canada, Table 35-10-0177-01.*

Every major province experienced the same broad pattern — decline through the mid-2010s, a plateau or slight rise, then renewed decline. But absolute levels differ sharply. Saskatchewan's offence rate consistently runs roughly double Ontario's. BC sits above the national average, closer to Alberta and Manitoba.

![Criminal Code offence rates per 100,000 population for six provinces](outputs/charts/q1_provincial_comparison.png)
*Figure 4. Criminal Code offence rates (excluding traffic) per 100,000 population across six provinces, 2004--2024. Source: Statistics Canada, Table 35-10-0177-01.*

Indexing all provinces to their 2004 crime rate (= 100) makes trajectories directly comparable regardless of absolute level. BC shows the steepest decline among comparison provinces, reaching roughly 58 by 2014 — a 42% drop. The post-2014 rebound appears across all provinces but has since reversed.

![Provincial crime rate trajectories indexed to 2004 = 100](outputs/charts/q1_indexed_provincial_growth.png)
*Figure 5. Provincial crime rate trajectories indexed to 2004 = 100. BC (bold blue) declined the steepest, then rebounded before resuming decline. Source: Statistics Canada, Table 35-10-0177-01.*

BC's crime rate has persistently exceeded the national average. The gap narrowed from 2004 to 2014 as BC's decline outpaced the national trend, but has since stabilized at roughly 20% above. That persistent premium raises questions about structural factors specific to BC — housing costs, the opioid crisis, and policing models among them.

![BC vs Canada crime rate gap](outputs/charts/q1_bc_canada_gap.png)
*Figure 6. BC vs Canada crime rate with the excess gap shaded. BC remained above the national average for the entire period, though the gap narrowed through 2014. Source: Statistics Canada, Table 35-10-0177-01.*

The most recent year-over-year comparison across provinces shows BC's decline is among the steepest nationally, suggesting province-specific factors beyond the broader national pattern.

![Year-over-year change in crime rate by province, latest year](outputs/charts/q1_yoy_by_province.png)
*Figure 7. Year-over-year change in Criminal Code offence rate by province. BC highlighted in blue; grey bars show comparison provinces. Source: Statistics Canada, Table 35-10-0177-01.*

Decomposing the CSI into contributing offence categories reveals which crime types drive the aggregate index. Severity weighting means violent offences contribute disproportionately to the total despite lower volumes — a distinction the raw crime rate obscures.

![CSI contribution breakdown by offence category](outputs/charts/q1_csi_contribution.png)
*Figure 8. CSI contribution breakdown by offence category. Violent offences carry outsized weight relative to their volume because of severity-based weighting. Source: Statistics Canada, Table 35-10-0063-01.*

---

## 2. What Kinds of Crime Are Changing?

BC's crime mix shifted markedly over two decades. Total crime rates fell, but the composition changed in ways that reshape policing priorities: property crime still dominates by volume, yet its declining share pushed violent crime and administration of justice violations to a larger proportion of the total.

![Stacked area chart showing BC crime composition by category](outputs/charts/q2_stacked_composition.png)
*Figure 9. BC crime composition by category (rate per 100,000), 2004--2024. Property crime dominates but is declining; violent crime holds steady. Source: Statistics Canada, Table 35-10-0177-01.*

The 100% stacked view makes the shift explicit. Property crime's share fell from 64% in 2004 to 51% in 2024. Violent crime grew from roughly 12% to 20%. Administration of justice violations also expanded — consistent with stricter bail enforcement during this period.

![100% stacked area showing crime category shares over time](outputs/charts/q2_composition_shares.png)
*Figure 10. Crime composition as share of total (%), 2004--2024. Property crime's declining share and violent crime's rising share confirm the compositional shift. Source: Statistics Canada, Table 35-10-0177-01.*

The heatmap offers a year-by-year intensity view. Property crime cells show gradual cooling, while administration of justice violations warm from left to right — a pattern consistent with policy changes around breach and bail offences.

![Heatmap of offence rates by category and year](outputs/charts/q2_heatmap.png)
*Figure 11. Heatmap of BC crime rates by category and year. Warmer colours indicate higher rates per 100,000. Source: Statistics Canada, Table 35-10-0177-01.*

Absolute rate changes over the last five years identify the specific offences driving aggregate trends. Theft from motor vehicles saw the single largest decline at -772 per 100,000, followed by breaking and entering and theft under $5,000. On the rising side, child exploitation offences (+82/100k) and shoplifting (+79/100k) both increased — two categories that warrant targeted policy attention.

![Top 10 offences by absolute rate change](outputs/charts/q2_top_changes.png)
*Figure 12. Top 10 violations by absolute rate change over five years. Teal bars indicate declines; red bars indicate increases. Source: Statistics Canada, Table 35-10-0177-01.*

The slope chart ranks five main crime categories by rate in 2014 versus the latest year. Property crime remains dominant in absolute terms. The key movements: administration of justice rose in rank while drug offences fell — reflecting both decriminalization trends and stricter bail enforcement.

![Slope chart ranking crime categories](outputs/charts/q2_slope_ranking.png)
*Figure 13. Slope chart of crime category rankings, 2014 vs latest year. Source: Statistics Canada, Table 35-10-0177-01.*

Compound annual growth rate normalizes changes for both time and base rate. Over the most recent five years, all five categories declined, but at vastly different rates. Violent crime's CAGR of just -0.8% confirms it is declining the slowest — the crime mix is shifting toward more serious offences.

![CAGR by crime category](outputs/charts/q2_category_cagr.png)
*Figure 14. Compound annual growth rate by crime category. Drug offences declined fastest (-8.3%); violent crime declined slowest (-0.8%). Source: Statistics Canada, Table 35-10-0177-01.*

Drilling into individual violation types reveals trajectories that aggregate figures obscure. The small multiples show eight selected violations across different crime categories, each on its own path — some declining steadily, others surging or plateauing.

![2x4 small multiples of specific violation trends](outputs/charts/q2_specific_violation_trends.png)
*Figure 15. Trend lines for eight selected Criminal Code violations, showing the diversity of trajectories beneath aggregate numbers. Source: Statistics Canada, Table 35-10-0177-01.*

The fastest-rising violations, while sometimes small in absolute terms, represent emerging pressure points. These trends are not yet visible in aggregate statistics — the kind of signal that gets lost in a provincial average.

![Rising violations spotlight overlay](outputs/charts/q2_rising_violations_spotlight.png)
*Figure 16. Overlay of the fastest-rising Criminal Code violations in BC. Source: Statistics Canada, Table 35-10-0177-01.*

BC Government data adds a complementary lens on the most recent year. Comparing 2022 and 2023 incident counts across categories reveals a mixed picture: 17 categories rose while 14 declined, with the largest percentage increases in categories often underrepresented in aggregate statistics.

![Year-over-year change by crime category, 2022-2023](outputs/charts/q2_bcgov_yoy_2022_2023.png)
*Year-over-year percentage change in incident counts by crime category, 2022 vs 2023. Red bars indicate increases; teal bars indicate decreases. Source: BC Government, Crime Statistics in BC 2023 (Appendix F).*

---

## 3. How Effectively Is Crime Being Addressed?

Clearance rates provide the most direct measure of police effectiveness. Tracking them by crime category over time reveals whether the system's capacity kept pace with the changing crime mix.

![Clearance rate trends by crime category](outputs/charts/q3_clearance_rate_trends.png)
*Figure 17. Clearance rate trends by major crime category. Rates vary widely by offence type, and the trends reveal shifting enforcement priorities and capacity constraints. Source: Statistics Canada, Table 35-10-0063-01.*

Breaking clearance rates down by violation type shows where the system is most and least effective. Offences with identifiable victims and clear evidence clear at high rates; others present persistent investigative challenges.

![Clearance rates by violation type](outputs/charts/q3_clearance_by_violation.png)
*Figure 18. Clearance rates by specific violation type, ranging from <20% (theft) to >70% (assault). Source: Statistics Canada, Table 35-10-0063-01.*

Youth and adult crime follow different trajectories. The youth Crime Severity Index declined even as the overall CSI rose — a divergence that points to age-specific factors and has direct implications for prevention-oriented policy.

![Youth vs adult CSI trends](outputs/charts/q3_youth_vs_adult_csi.png)
*Figure 19. Youth vs adult Crime Severity Index. The youth CSI declined while the overall index rose, pointing to age-specific drivers that aggregate figures obscure. Source: Statistics Canada, Table 35-10-0063-01.*

BC's policing splits between RCMP detachments (most of the province by area) and independent municipal forces (the largest cities). Comparing outcomes across these two models tests whether organizational structure correlates with differences in crime patterns or clearance performance.

![RCMP vs municipal policing comparison](outputs/charts/q3_rcmp_vs_municipal.png)
*Figure 20. Crime metrics across RCMP-policed and municipally-policed jurisdictions. Municipal forces handle the largest share of offences by volume. Source: BC Government, Police Resources in British Columbia.*

The COVID-19 pandemic disrupted crime patterns across every category. Lockdowns, reduced mobility, economic support programs, and reporting changes all produced anomalous 2020--2021 data. Isolating the pandemic's impact helps distinguish genuine trends from temporary distortions — critical for interpreting the post-2019 decline (see Caveat 2).

![COVID-19 impact on crime patterns](outputs/charts/q3_covid_impact.png)
*Figure 21. COVID-19 impact analysis. Some offences dropped sharply during lockdowns; others were largely unaffected. Source: Statistics Canada, Table 35-10-0177-01.*

Not all reported incidents result in founded criminal cases. The unfounded rate — the share of reports police determine did not occur or did not constitute a criminal offence — varies by offence type, with implications for both victims and the accuracy of crime statistics.

![Unfounded rates by offence type](outputs/charts/q3_unfounded_rates.png)
*Figure 22. Unfounded rates across offence categories. Higher unfounded rates may reflect investigative complexity, reporting patterns, or systemic assessment differences. Source: Statistics Canada, Table 35-10-0063-01.*

### The Reporting Gap: Could Underreporting Explain the Decline?

The apparent decline in crime rates may partly reflect less crime being *reported* rather than less crime occurring. Statistics Canada's [General Social Survey on Canadians' Safety (2019)](https://www150.statcan.gc.ca/n1/pub/85-002-x/2021001/article/00014-eng.htm) found that only **29% of criminal victimizations** were reported to police (Cotter, 2021, *Juristat*, Catalogue no. 85-002-X). Reporting rates vary dramatically: property crime at roughly 35%, violent crime at 24%, sexual assault at just 6%.

Police-reported data therefore captures less than a third of actual criminal victimization. If reporting rates declined over time, falling police-reported rates could coexist with stable or rising actual crime. Three proxy indicators test this hypothesis:

1. **Unfounded rates** — If police classify more reports as "unfounded," crime counts are artificially suppressed. Panel 1 of Figure 23 tracks unfounded rates for specific violations over time.

2. **Clearance method shifts** — A growing share of cases "cleared otherwise" (rather than by charge) may indicate victims declining to proceed, consistent with reporting fatigue. Panel 2 tracks this ratio.

3. **Differential decline rates** — If underreporting drives the decline, the steepest drops should appear in categories with the lowest reporting rates. Panel 3 compares property crime (~35% reporting rate) and violent crime (~24%) trajectories.

![Underreporting proxy dashboard](outputs/charts/q3_underreporting_proxies.png)
*Figure 23. Underreporting proxy dashboard. Top-left: unfounded rates for specific violations. Top-right: share of cleared cases resolved by charge vs otherwise. Bottom-left: property vs violent crime indexed to 2004. Bottom-right: GSS victimization survey context. Sources: Statistics Canada Tables 35-10-0177-01 and 35-10-0063-01; GSS on Canadians' Safety, 2019.*

**Assessment.** The proxy data partly supports the underreporting hypothesis — but with a critical exception. Property crime, which has a *higher* reporting rate and is therefore less sensitive to reporting changes, declined more steeply than violent crime. That is the *opposite* of what a reporting-driven decline would produce. The GSS data confirms that the vast majority of crime goes unreported, making it impossible to fully separate genuine crime reduction from reporting changes using police data alone. The most defensible conclusion: underreporting likely contributes to some of the property crime decline (particularly low-value theft) but cannot explain the violent crime trends, which are shaped by distinct factors including the opioid crisis and changing enforcement priorities.

### Policing Costs and Cost-Effectiveness

BC's policing bill grew steadily — but did the spending produce results?

![BC policing expenditure trend](outputs/charts/q3_bc_expenditure_trend.png)
*Figure S1. BC policing expenditure in nominal and CPI-adjusted (real) dollars. Spending outpaced general inflation over the full period. Source: Statistics Canada, Table 35-10-0076-01.*

![Per-capita policing cost comparison across provinces](outputs/charts/q3_per_capita_comparison.png)
*Figure S2. Per-capita policing expenditure across Canadian provinces. BC consistently ranks above the national average. Source: Statistics Canada, Table 35-10-0076-01.*

![CSI overlaid with policing expenditure](outputs/charts/q3_csi_vs_expenditure.png)
*Figure S3. BC Crime Severity Index overlaid with policing expenditure. Spending rose while crime severity fell — then kept rising as crime plateaued, raising cost-effectiveness questions. Sources: Statistics Canada, Tables 35-10-0076-01 and 35-10-0063-01.*

![Policing expenditure breakdown by component](outputs/charts/q3_expenditure_breakdown.png)
*Figure S4. Policing expenditure breakdown. Personnel costs dominate, accounting for the majority of total spending. Source: Statistics Canada, Table 35-10-0076-01.*

Staffing levels add another dimension. The number of police officers per 100,000 measures whether the force kept pace with a growing province.

![Police officers per 100,000 population over time](outputs/charts/q3_staffing_trend.png)
*Figure S5. Police officers per 100,000 population in BC over time. Source: Statistics Canada, Table 35-10-0076-01.*

Combining staffing with crime data yields a workload measure: how many Criminal Code incidents does each officer handle? Overlaid with the Crime Severity Index, this reveals whether declining crime translated into reduced workload or whether other demands absorbed the capacity.

![Criminal Code incidents per police officer](outputs/charts/q3_crimes_per_officer.png)
*Figure S6. Criminal Code incidents per police officer in BC, with CSI trend overlay. Source: Statistics Canada, Tables 35-10-0076-01 and 35-10-0063-01.*

---

## 4. Where Is Crime Concentrated?

Provincial averages mask enormous variation at the local level.

Population drives raw offence counts — Vancouver and Surrey top the list simply because they are the most populous. The chart below ranks the top 20 jurisdictions by total Criminal Code offences, distinguishing municipal police forces from RCMP detachments.

![Top 20 jurisdictions by total crime count](outputs/charts/q4_top_jurisdictions.png)
*Figure 24. Top 20 BC policing jurisdictions by total Criminal Code offence count (latest year). Source: BC Government, Police Resources in British Columbia.*

The small multiples show how crime evolved in BC's eight largest jurisdictions. Trajectories diverge: some show clear declines, others plateaued, a few rose modestly. Local factors — economic conditions, policing models, demographics — matter as much as provincial trends.

![Crime trends for the 8 largest BC jurisdictions](outputs/charts/q4_jurisdiction_trends.png)
*Figure 25. Crime trends in BC's 8 largest policing jurisdictions. Divergent trajectories confirm that local conditions drive outcomes alongside province-wide forces. Source: BC Government, Police Resources in British Columbia.*

Among BC's Census Metropolitan Areas, the interior-coastal split is stark. Chilliwack leads at 11,352 offences per 100,000, followed by Kamloops (10,546), Nanaimo (9,365), and Kelowna (8,922). The large coastal metros — Vancouver (5,438) and Victoria (5,283) — sit at the bottom. Interior CMAs consistently record per-capita rates roughly double those of the major urban centres.

![Per-capita crime rates across BC CMAs](outputs/charts/q4_cma_comparison.png)
*Figure 26. Criminal Code offence rate per 100,000 across BC Census Metropolitan Areas (latest year). Interior CMAs report roughly double the rates of coastal metros. Source: Statistics Canada, Table 35-10-0177-01.*

CMA trend charts add temporal context. Abbotsford-Mission's rate roughly halved from its 2004 peak; Kelowna's held relatively flat. Chilliwack and Kamloops have shorter time series (they became CMAs more recently), showing elevated but declining rates. These divergent paths caution against treating "BC" as a single story (see Caveat 3 on CMA boundary changes).

![CMA crime rate trends over time](outputs/charts/q4_cma_trends.png)
*Figure 27. Crime rate trends across BC CMAs, 2004--2024. Abbotsford-Mission declined sharply; Kelowna held steady. Source: Statistics Canada, Table 35-10-0177-01.*

Aggregating by region reveals which parts of BC saw the sharpest increases. The small multiples below cover the top 12 regions by volume — some interior regions saw substantial increases while Metro Vancouver's counts declined.

![Region comparison small multiples](outputs/charts/q4_region_comparison.png)
*Crime count trends by BC region (top 12 by volume), 2014--2023. Strathcona, Central Okanagan, and Thompson Nicola grew the fastest; Metro Vancouver is the only declining region among the top 12. Source: BC Government, Police Resources in British Columbia.*

A scatter plot of total offences against violent offences reveals a near-perfect linear relationship (r = 0.99). High-crime jurisdictions do not just have more property crime — they have proportionally more violent crime. This undermines the narrative that high-crime areas are primarily a property-offence story.

![Scatter plot of total vs violent offences by jurisdiction](outputs/charts/q4_total_vs_violent.png)
*Figure 28. Total vs. violent Criminal Code offences by jurisdiction (r = 0.99). High-crime areas face proportionally elevated violence, not just more property crime. Source: BC Government, Police Resources in British Columbia.*

Crime concentration in BC is extreme. The Pareto curve shows 5% of jurisdictions account for 50% of all Criminal Code offences; 19% account for 80%. Provincial statistics are largely driven by a handful of high-volume jurisdictions — a fact with direct implications for resource allocation.

![Crime concentration Pareto curve](outputs/charts/q4_crime_concentration.png)
*Figure 29. Pareto curve of crime concentration across BC jurisdictions. The steep initial rise shows that a small number of jurisdictions dominate total crime volume. Source: BC Government, Police Resources in British Columbia.*

Violent crime's share varies widely across jurisdictions. The average sits at roughly 26%, but some jurisdictions exceed 50% while others fall below 15%. Jurisdictions with disproportionately high violent shares require different policing strategies than those dominated by property crime.

![Distribution of violent crime share across jurisdictions](outputs/charts/q4_violent_share_distribution.png)
*Figure 30. Distribution of violent crime share (%) across BC jurisdictions. The dashed line shows the average; red dots mark jurisdictions more than 10 percentage points above average. Source: BC Government, Police Resources in British Columbia.*

An [interactive version of the jurisdiction data](outputs/charts/q4_interactive_map.html) is available for exploring all 50 top jurisdictions with hover details for violent, property, and total offence breakdowns.

---

## 5. Why Does Crime Feel Like It's Rising?

Crime severity fell substantially from its early-2000s peak — yet 42% of BC residents told Statistics Canada they believe crime increased in their neighbourhood. That gap between perception and measurement has real policy consequences.

Statistics Canada's General Social Survey on Canadians' Safety (2019) asked respondents whether neighbourhood crime had increased, decreased, or stayed the same over five years. In BC, 42% said crime increased — up from 30% in 2014. Nationally, 39% held the same view. Both figures track poorly with the Crime Severity Index, which in 2019 sat roughly 40% below its 2003 peak.

![Perception vs reality: survey beliefs alongside actual CSI trend](outputs/charts/q5_perception_vs_reality.png)
*Figure 31. Top: proportion of BC and Canada respondents who said crime "increased" across GSS cycles. Bottom: actual BC Crime Severity Index. The perception-measurement gap is substantial and widening. Sources: Statistics Canada, GSS on Canadians' Safety; Table 35-10-0063-01.*

Confidence in local police varies across provinces and may feed into crime perceptions. In 2019, 30% of BC residents reported a "great deal of confidence" in their local police — below the national average of 32% and below prairie provinces. Residents who feel less protected tend to overestimate local crime trends.

![Confidence in police by province](outputs/charts/q5_confidence_by_province.png)
*Figure 32. Confidence in police by province (GSS 2019). BC's confidence levels are modestly below the national average. Source: Statistics Canada, GSS on Canadians' Safety (2019).*

Underreporting compounds the problem. Only 29% of criminal victimization is reported to police. Every chart in this analysis captures less than a third of actual crime. Reporting rates range from 60% for motor vehicle theft to just 6% for sexual assault — meaning the gap between lived experience and official statistics is wide enough for perception and data to tell different stories.

![Reporting rates by crime type](outputs/charts/q5_reporting_rates.png)
*Figure 33. Police reporting rates by crime type (GSS 2019). The overall victimization reporting rate is 29%. Source: Cotter (2021), Juristat, Catalogue no. 85-002-X.*

**Assessment.** The perception-reality gap has five identifiable drivers: (1) media coverage emphasizes dramatic incidents over statistical trends; (2) visible disorder — homelessness, open drug use — creates a sense of rising crime even as severity indices decline; (3) specific crime types affecting daily life (vehicle break-ins, retail theft) may have risen locally while aggregate indices fell; (4) the opioid crisis concentrated visible harm in urban centres; and (5) social media amplifies anecdotal reports at the expense of base rates. The policy implication: decisions driven by perceived rather than measured crime trends risk misallocating resources toward visible symptoms rather than underlying patterns.

---

## Methodology

### Data Sources

| Source | Table / Reference | Coverage | Used In |
|--------|-------------------|----------|---------|
| Statistics Canada | 35-10-0063-01 | Crime Severity Index by police service, including clearance and youth/adult breakdowns | Sections 1, 3 |
| Statistics Canada | 35-10-0177-01 | Incident-based crime statistics by province and CMA | Sections 1, 2, 3, 4 |
| BC Government | Appendix F--I (2014--2023) | Jurisdiction-level crime statistics, RCMP vs municipal | Sections 3, 4 |

### Key Metric Definitions

- **Crime Severity Index (CSI)**: A Statistics Canada composite measure that weights each offence type by its average sentence length (derived from five years of sentencing data), then divides by population. More serious crimes carry higher weight. Base year: 2006 = 100. Unlike simple crime rates, the CSI accounts for both the volume and severity of crime. See Figures 1--2, 8, 19.
- **Per-capita rate**: Criminal Code offences per 100,000 population, excluding traffic violations. This normalizes for population size, enabling fair comparisons across jurisdictions of different sizes. See Figures 4--7, 26--27.
- **Compound Annual Growth Rate (CAGR)**: The constant annual rate that would produce the observed cumulative change over a given period. Calculated as (end value / start value)^(1/n) - 1, where n is the number of years. CAGR smooths out year-to-year volatility, making it useful for comparing categories with different time spans. See Figure 14.
- **Indexed growth (base = 100)**: Each province's crime rate is divided by its 2004 value and multiplied by 100, so all series start at the same point. Changes are then expressed in percentage-point terms relative to 2004, enabling trajectory comparisons across provinces with very different absolute levels. See Figure 5.
- **Clearance rate**: The share of police-reported incidents that are "cleared" -- either by charge (a suspect is identified and charged) or by other means (e.g., the suspect dies, the victim declines to proceed). Clearance rates vary by offence type and are not equivalent to conviction rates. See Figures 17--18.
- **Unfounded rate**: The share of reported incidents that police determine did not occur or did not constitute a criminal offence. A high unfounded rate does not necessarily mean false reporting -- it may reflect evidentiary thresholds or investigative practices. See Figures 22--23.

---

## Caveats

These limitations are material to interpreting the analysis. They are referenced in specific figure captions where most relevant.

1. **Police-reported data only** -- These statistics reflect crimes reported to and recorded by police. They do not capture unreported crime, which varies significantly by offence type (e.g., sexual assault is heavily underreported). This affects all sections but is most consequential for Figures 9--16 (compositional analysis), where offences with low reporting rates may be systematically underrepresented. Figure 23 explores proxy indicators for underreporting using police data and GSS victimization survey context.

2. **COVID-19 disruption** -- The 2020--2021 period shows anomalous patterns due to lockdowns, reduced mobility, and changes in reporting behaviour. Trends spanning this period should be interpreted with caution. Figure 21 isolates the pandemic's impact; Figures 3 and 5 are also affected. Any year-over-year comparison involving 2020 or 2021 data should be treated as potentially distorted.

3. **CMA boundary changes** -- Census Metropolitan Area definitions shift between census cycles, which can affect per-capita rate comparisons over long periods. This is most relevant to Figures 26--27 (CMA comparisons). Chilliwack and Kamloops, which became CMAs more recently, have shorter time series.

4. **Most-serious-offence counting rule** -- Statistics Canada counts only the most serious offence when multiple offences occur in a single incident. This systematically undercounts less serious offences and inflates the apparent severity share. Figures 9--14 (compositional analysis) are affected.

5. **Jurisdiction coverage** -- BC Government appendix data covers the largest municipal police services and RCMP detachments but may not include all smaller jurisdictions. Figures 24--25 and 28--30 should be interpreted as covering the majority -- but not the entirety -- of BC policing jurisdictions.

6. **Clearance rates are not conviction rates** -- A "cleared" case means police have identified a suspect, not that a conviction was obtained. Figures 17--18 reflect police investigative outcomes, not judicial outcomes.

7. **Unfounded determinations are subjective** -- The threshold for classifying a report as "unfounded" involves police judgment and may vary across jurisdictions and over time. Figure 22 should be interpreted with this in mind.

---

<details>
<summary><strong>Technical Details</strong></summary>

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
python -m src.analysis.q3_justice
python -m src.analysis.q3_costs
python -m src.analysis.q4_geography
python -m src.analysis.q5_perception
```

Charts are saved to `outputs/charts/`. Open `notebooks/bc_crime_report.ipynb` for the full interactive narrative report.

### Project Structure

```
src/
  paths.py                    # Centralized path constants
  download.py                 # Fetch all raw data from StatCan and BC Gov
  clean.py                    # Parse, normalize, save to parquet
  analysis/
    theme.py                  # Shared chart theme and palette (kds wrapper)
    q1_is_crime_rising.py     # CSI trends, provincial comparison (8 charts)
    q2_what_kinds.py          # Crime type breakdown (9 charts)
    q3_justice.py             # Justice system effectiveness (7 charts)
    q3_costs.py               # Policing expenditure and staffing analysis (6 charts)
    q4_geography.py           # Jurisdiction and CMA analysis (8 charts + 1 HTML)
    q5_perception.py          # Perception vs reality (3 charts)
data/
  README.md                   # Data dictionary — full citations and schemas
  raw/
    statscan/                 # Statistics Canada CSVs (gitignored)
    bcgov/                    # BC Government XLSX files (gitignored)
  processed/                  # Cleaned parquet files (gitignored)
notebooks/
  bc_crime_report.ipynb       # Full narrative report
outputs/
  charts/                     # Generated charts (41 PNG + 1 HTML)
    README.md                 # Chart index with figure numbers and sources
tests/
  test_download.py            # Download verification tests
  test_clean.py               # Data quality tests
```

See [`data/README.md`](data/README.md) for full data source citations, column schemas, and data lineage.

### Chart Count

| Script | PNG | HTML | Figures |
|--------|-----|------|---------|
| q1_is_crime_rising.py | 8 | 0 | 1--8 |
| q2_what_kinds.py | 9 | 0 | 9--16 + BC Gov YoY |
| q3_justice.py | 7 | 0 | 17--23 |
| q3_costs.py | 6 | 0 | S1--S6 (supplementary) |
| q4_geography.py | 8 | 1 | 24--30 + region + interactive |
| q5_perception.py | 3 | 0 | 31--33 |
| **Total** | **41** | **1** | **41 + 1** |

### Processed Data

Cleaned parquet files are stored in `data/processed/` (gitignored). Regenerate them with `python -m src.clean` after downloading raw data. The processed files include:
- `crime_severity_bc.parquet` -- BC Crime Severity Index by component
- `crime_incidents_national.parquet` -- incident-based crime statistics by province and CMA
- `bc_gov_jurisdiction_trends.parquet` -- jurisdiction-level counts from BC Government appendices

### Requirements

- Python 3.12+, see `requirements.txt`

</details>

---

*Data: Statistics Canada (Tables 35-10-0063-01 and 35-10-0177-01) and BC Ministry of Public Safety. Analysis and visualizations by Kacper Ruta, 2024--2026.*
