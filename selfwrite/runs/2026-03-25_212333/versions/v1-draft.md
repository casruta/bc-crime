# British Columbia Crime Analysis (2004-2024)

British Columbia's Crime Severity Index (CSI) declined 46% from its 1998 peak of 166.9 to 90.2 in 2014, with a further 7.4% decrease in 2024. This analysis examines 20 years of Statistics Canada and BC Government data across five research questions, producing 42 charts and one interactive map.

> **Key findings:** Crime severity fell substantially over two decades, but the composition shifted toward violent offences after 2014. Interior communities record per-capita rates 1.9-2.1x those of coastal cities. Public perception of rising crime grew from 30% to 42% (2014-2019) despite declining aggregate statistics, driven by five identifiable measurement and communication gaps.

---

## Table of Contents

1. [Crime Severity Trends](#1-crime-severity-has-declined-but-the-composition-has-shifted)
2. [Property Crime and Emerging Categories](#2-property-crime-trends-and-emerging-offence-categories)
3. [Clearance Rates, Youth Crime, and Policing Costs](#3-clearance-rates-youth-crime-and-policing-costs)
4. [Geographic Distribution](#4-geographic-distribution-of-crime)
5. [Public Perception vs. Statistical Trends](#5-public-perception-and-statistical-trends)
6. [Implications](#implications)
7. [Limitations](#limitations)
8. [Methodology](#methodology)
9. [Reproducibility](#reproducibility)

---

## Key Terms

- **Crime Severity Index (CSI)**: A Statistics Canada measure weighting criminal incidents by the average sentence severity of each offence type (base year: 2006). Higher values indicate more severe crime profiles.
- **Crime rate**: The number of police-reported incidents per 100,000 population, unadjusted for severity.
- **Clearance rate**: The proportion of reported incidents where police identified a suspect, whether or not charges were laid.
- **Unfounded rate**: The proportion of incidents deemed, upon investigation, not to have occurred or not to constitute a criminal offence.

---

## 1. Crime Severity Has Declined, but the Composition Has Shifted

BC's Crime Severity Index fell from a peak of 166.9 in 1998 to 90.2 in 2014, a 46% reduction. The index decreased a further 7.4% in 2024, the second-largest year-over-year provincial decline after Alberta (-8.5%). Over the full 1998-2024 series, 18 years recorded declining crime rates against 8 years of increases. Linear regression confirms the downward trend is statistically significant (p < 0.05).

![BC Crime Severity Index: 46% decline from 1998 peak (166.9) to 2014 trough (90.2), continued decline through 2024](outputs/charts/q1_bc_csi_trend.png)

The compositional pattern diverged from the aggregate trend after 2014. The violent component of the CSI increased while the non-violent component continued to decline. The aggregate index continued to fall because property crime's absolute decline exceeded the upward movement in violent crime severity. BC's CSI remained approximately 21% above the national average throughout the 20-year series.

![Violent CSI trending upward since 2014 while non-violent CSI continues to decline](outputs/charts/q1_violent_nonviolent_gap.png)

Year-over-year data recorded 18 declining years against 8 increasing, with 2024 registering a 7.4% decrease.

![BC year-over-year crime rate changes: 18 declining years vs. 8 increasing](outputs/charts/q1_bc_yoy_trend.png)

The decline was not specific to British Columbia. All comparison provinces exhibited converging downward trajectories when indexed to 2004 = 100. Saskatchewan maintained rates approximately 2.8x Ontario's throughout the series, but the directional trend was consistent across jurisdictions. This convergence is consistent with structural factors -- demographic shifts, urbanization, changes in enforcement philosophy -- rather than jurisdiction-specific policy as the primary driver.

![Provincial crime rate comparison: BC consistently above the national average](outputs/charts/q1_provincial_comparison.png)

![Indexed provincial growth (2004 = 100): all provinces converge downward](outputs/charts/q1_indexed_provincial_growth.png)

The BC-Canada gap persisted across the full series. BC's 7.4% year-over-year decline in 2024 ranked second among provinces.

![BC-Canada crime rate gap: persistent across two decades](outputs/charts/q1_bc_canada_gap.png)

![Year-over-year change by province: BC's 7.4% drop ranks second-largest](outputs/charts/q1_yoy_by_province.png)

A small number of offence types accounted for the majority of CSI weight, identifying the categories with the greatest leverage for policy intervention.

![CSI contribution by violation type: a small number of offences account for most of the index weight](outputs/charts/q1_csi_contribution.png)

BC Government data confirm the pattern at the most recent available granularity.

![BC Government year-over-year comparison, 2022-2023](outputs/charts/q2_bcgov_yoy_2022_2023.png)

**Caveat:** The CSI weights offences by average sentence severity. Criminal Code revisions that reclassify an act to a more serious category increase the index even if the underlying behaviour is unchanged. Post-2019 amendments to domestic violence and sexual assault definitions may account for some of the observed increase in violent crime severity.

## 2. Property Crime Trends and Emerging Offence Categories

Property crime declined steadily from the early 2000s across all major violation types, accounting for 51% of the total crime rate as of the most recent data. The largest absolute changes over five years were as follows:

| Violation | 5-Year Change (per 100,000) |
|---|---|
| Theft from vehicles | -772 |
| Breaking and entering | -270 |
| Theft under $5,000 | -221 |
| Disturb the peace | -165 |

The 772 per 100,000 decline in theft from vehicles represented the largest absolute decrease of any violation type. Shoplifting increased by 79 per 100,000 over the same period.

![Crime composition over time: property crime's share contracting as violent crime's share grows](outputs/charts/q2_stacked_composition.png)

![Current composition shares: property crime accounts for 51% of total but is declining](outputs/charts/q2_composition_shares.png)

The violation-level heatmap displays intensity patterns across crime types and years. Property violations cooled over the study period while violent types remained relatively stable.

![Violation-level intensity heatmap: property violations cooling while violent types hold steady](outputs/charts/q2_heatmap.png)

![Largest absolute changes in crime rate: theft from vehicles leads all declines at -772/100k](outputs/charts/q2_top_changes.png)

Factors associated with the vehicle-theft decline include improved vehicle security technology, reduced visibility of valuables, increased contactless payment adoption, and pandemic-era remote work patterns.

Two violation categories increased against the overall trend. Child pornography offences rose by 82 per 100,000 and shoplifting by 79 per 100,000. The child exploitation increase is consistent with expanded digital investigation capacity (ICAC task forces, automated hash-matching, mandatory platform reporting) rather than a prevalence increase. The shoplifting increase has multiple potential explanations: behavioural change, reduced retail security staffing, and changes to prosecution thresholds have each been identified as contributing factors.

![Property violation trajectories declining while exploitation and shoplifting trend upward](outputs/charts/q2_slope_ranking.png)

![Property crime CAGR is negative; other categories are flat or positive](outputs/charts/q2_category_cagr.png)

Individual violation trajectories over the study period show divergent patterns, with child exploitation and shoplifting recording the largest absolute increases.

![Individual violation trajectories: theft from vehicles declining sharply, shoplifting and exploitation rising](outputs/charts/q2_specific_violation_trends.png)

![Fastest-growing violations: child exploitation and shoplifting lead absolute increases](outputs/charts/q2_rising_violations_spotlight.png)

Violent crime's absolute rate remained relatively stable, but its share of total crime increased as property crime declined. A chi-squared test for crime-type composition across years was statistically significant (p < 0.05), confirming the compositional shift.

![BC Government year-over-year comparison by crime type, 2022-2023](outputs/charts/q2_bcgov_yoy_2022_2023.png)

## 3. Clearance Rates, Youth Crime, and Policing Costs

Clearance rates differed substantially by crime type. Violent crime clearance, historically above 50%, declined to 37.4% in 2024 -- a 21-percentage-point reduction from its 2014 level. Property crime clearance remained in the 12-16% range throughout the study period, indicating that approximately 85% of reported property crimes went unresolved.

![Clearance rate trends: violent crime clearance declining from above 50% toward 37%; property crime stable at 12-16%](outputs/charts/q3_clearance_rate_trends.png)

![Clearance variation by violation: some types clear above 70% while others remain below 20%](outputs/charts/q3_clearance_by_violation.png)

The persistence of low property-crime clearance rates across two decades of reforms, technology investment, and budget increases is consistent with a structural constraint: the volume and low individual value of property offences may render case-by-case investigation uneconomical at current resource levels.

Youth crime severity diverged from the adult trend after 2014. Youth CSI continued to decline while adult CSI stabilized or increased. Of the candidate explanations, diversion programs are the most directly supported by the data: formal system contact for youth decreased concurrently with the expansion of extrajudicial measures. Declining youth population share may also contribute, though it does not fully account for the magnitude of the divergence.

![Youth vs. adult CSI divergence: youth crime continues declining while adult crime stabilizes](outputs/charts/q3_youth_vs_adult_csi.png)

RCMP detachments and municipal forces exhibited different crime trajectories. The COVID-19 pandemic produced a visible dip in 2020 followed by a partial rebound across categories.

![RCMP detachments and municipal forces show different crime trajectories](outputs/charts/q3_rcmp_vs_municipal.png)

![COVID-19 impact: 2020 dip and post-pandemic rebound across crime categories](outputs/charts/q3_covid_impact.png)

Two alternative explanations for the overall decline were not supported by the data. Unfounded rates remained stable, ruling out police reclassification as a driver. The underreporting pattern was inconsistent with a reporting-driven decline: property crime, reported at higher rates (~35%), declined more steeply than violent crime (~24% reported).

![Unfounded rates stable over time: reclassification did not drive the decline](outputs/charts/q3_unfounded_rates.png)

![Underreporting proxy analysis: the pattern is inconsistent with a reporting-driven decline](outputs/charts/q3_underreporting_proxies.png)

### Policing Expenditure Trends

Police spending in BC increased in both nominal and real (constant 2020 dollar) terms while crime severity declined. Salary and benefits growth outpaced operating and capital expenditure growth. BC's population increased 10.4% from 5,000,879 in 2018 to 5,519,913 in 2023.

![BC policing expenditure: nominal and inflation-adjusted, both rising](outputs/charts/q3_bc_expenditure_trend.png)

![Per-capita policing cost comparison across provinces](outputs/charts/q3_per_capita_comparison.png)

![CSI vs. expenditure: spending rises while crime severity falls](outputs/charts/q3_csi_vs_expenditure.png)

The crimes-per-officer metric indicates that declining crime volume did not produce a proportional reduction in officer workload. This pattern is consistent with expanding non-crime demands on police services, including mental health crisis response, overdose calls, welfare checks, and social disorder management.

![Expenditure breakdown: salaries and benefits outpace operating and capital](outputs/charts/q3_expenditure_breakdown.png)

![Police staffing trend: officers per 100,000 population](outputs/charts/q3_staffing_trend.png)

![Crimes per officer with CSI overlay: declining crime has not reduced workload](outputs/charts/q3_crimes_per_officer.png)

## 4. Geographic Distribution of Crime

Vancouver (~48,812 offences) and Surrey (~41,275) recorded the highest absolute crime volumes. Per-capita rates, however, were substantially higher in interior communities:

| Community | Rate per 100,000 | Ratio to Vancouver |
|---|---|---|
| Chilliwack | 11,352 | 2.1x |
| Kamloops | 10,546 | 1.9x |
| Vancouver | 5,438 | 1.0x |
| Victoria | 5,283 | 0.97x |

![Top 20 jurisdictions by total crime count: Vancouver and Surrey lead in volume](outputs/charts/q4_top_jurisdictions.png)

![The 8 largest jurisdictions follow different trajectories](outputs/charts/q4_jurisdiction_trends.png)

Interior Census Metropolitan Areas recorded per-capita rates 1.9-2.1x those of Vancouver (5,438/100k) and Victoria (5,283/100k), and this gap widened over the study period.

![CMA per-capita crime rate: interior communities at approximately 2x the rate of coastal metros](outputs/charts/q4_cma_comparison.png)

![Interior CMA rates diverging upward from coastal CMAs over time](outputs/charts/q4_cma_trends.png)

Several factors are associated with the interior-coastal divide: higher rates of homelessness and visible poverty, acute opioid-crisis exposure, seasonal tourism economies with transient populations, and reliance on RCMP detachments rather than dedicated municipal police services. The relative contribution of each factor cannot be isolated from the available data.

![Some jurisdictions have disproportionately violent profiles relative to their total crime](outputs/charts/q4_total_vs_violent.png)

![Crime concentration: a small number of jurisdictions account for most of BC's total](outputs/charts/q4_crime_concentration.png)

![Violent crime's share varies widely: some jurisdictions are 3x more violent than others](outputs/charts/q4_violent_share_distribution.png)

![Regional crime rate comparison across BC](outputs/charts/q4_region_comparison.png)

A composite ranking (60% standardized volume, 40% trend direction) classified areas as high, moderate, or lower concern, identifying communities where intervention would yield the highest expected return.

[Interactive jurisdiction map (HTML)](outputs/charts/q4_interactive_map.html)

## 5. Public Perception and Statistical Trends

Between 2014 and 2019, the share of BC residents who reported that crime had increased rose from 30% to 42% (General Social Survey), a 12-percentage-point increase occurring during a period of declining CSI.

| Year | "Crime increased" | "About the same" |
|---|---|---|
| 2009 | 38% | 43% |
| 2014 | 30% | 48% |
| 2019 | 42% | 41% |

![Perception vs. reality: 42% of residents believe crime is rising while CSI remains below its peak](outputs/charts/q5_perception_vs_reality.png)

Five data-traceable factors account for this divergence.

### Five Factors Contributing to the Perception Gap

**1. CSI aggregation conceals compositional shifts.** The violent component of the CSI increased after 2014 while the non-violent component declined. The aggregate index fell because property crime's absolute decline was larger, but residents may respond to the violent-crime component, which carries greater salience for personal safety.

*Corrective:* Report violent and non-violent CSI components separately.

**2. Increasing crime types are more visible than decreasing types.** Shoplifting increased by 79 per 100,000 and is directly observable in retail settings. Offsetting declines -- 772 fewer vehicle thefts and 270 fewer break-ins per 100,000 -- produce no observable signal. For every additional shoplifting incident per 100,000, approximately 10 vehicle thefts were prevented.

*Corrective:* Publish quarterly scorecards pairing increasing and decreasing crime categories.

**3. Low property-crime clearance rates may erode institutional credibility.** Property crime clearance remained in the 12-16% range throughout the study period. When the institution reporting crime statistics does not resolve the majority of reported cases, the public may discount its aggregate claims.

*Corrective:* Implement closed-loop case reporting with 30-day status updates for all filed reports.

**4. Provincial averages obscure jurisdiction-level variation.** Chilliwack (11,352/100k) and Kamloops (10,546/100k) recorded per-capita rates approximately 2x Vancouver's 5,438. For residents of these communities, provincial-level claims of declining crime may not correspond to local experience.

*Corrective:* Publish jurisdiction-level dashboards and allocate resources proportional to per-capita rates.

**5. Visible disorder is not captured by the CSI.** Open drug use, encampments, and aggressive panhandling are not Criminal Code offences and do not appear in the CSI. In communities with acute opioid-crisis exposure, these phenomena may dominate daily experience.

*Corrective:* Develop a community disorder index from police calls for service (wellness checks, trespass, mischief) and publish it alongside the CSI.

### Confidence and Reporting Rates

In the 2019 GSS, 30% of BC residents reported "a great deal of confidence" in police, with 47% reporting "some," 17% "not very much," and 5% "none." These figures tracked the national distribution (32%/46%/15%/5%).

![Confidence in police by province: BC's figures track the national pattern](outputs/charts/q5_confidence_by_province.png)

Reporting rates ranged from 6% (sexual assault) to 60% (motor vehicle theft). Nationally, 71% of victimizations went unreported (2019 GSS).

![Reporting rates by crime type: from 6% (sexual assault) to 60% (motor vehicle theft)](outputs/charts/q5_reporting_rates.png)

### Corrective Action Summary

| Factor | Action | Measure of Success |
|---|---|---|
| CSI aggregation conceals compositional shift | Report violent and non-violent CSI separately | Perception of violent trend aligns with data within 2 GSS cycles |
| Visible-crime sampling bias | Quarterly scorecard pairing increasing and decreasing categories | Media coverage references net change |
| Low clearance erodes credibility | 30-day closed-loop case updates for all filed reports | "Great deal of confidence" exceeds 35% |
| Provincial average obscures local rates | Jurisdiction-level dashboards; per-capita resource allocation | Interior per-capita rates decline toward provincial mean |
| Disorder outside CSI scope | Community disorder index from calls for service | Public discourse distinguishes disorder from Criminal Code crime |

---

## Implications

Five priorities emerge from the analysis.

**1. Monitor the violent-crime compositional shift.** Report violent and non-violent CSI separately in quarterly dashboards. The shift has been underway since 2014; resources remain allocated to declining property-crime categories.

**2. Rebalance resources toward interior communities.** Adopt the composite ranking (60% volume, 40% trend) as an input to funding formulas. Per-capita rates in interior CMAs (Chilliwack: 11,352/100k; Kamloops: 10,546/100k) are 1.9-2.1x coastal rates (Vancouver: 5,438/100k), and the gap widened over the study period.

**3. Redeploy investigation capacity from property to violent crime.** Each additional investigator-hour on violent crime yields a higher expected clearance rate than on property crime, which clears in the 12-16% range regardless of resource allocation.

**4. Address the perception-reality gap.** Publish quarterly plain-language dashboards with total and component breakdowns by community. The 12-percentage-point increase in perceived crime (30% to 42%, 2014-2019) occurred during a period of declining CSI.

**5. Distinguish detection increases from prevalence increases.** Child exploitation (+82/100k) and shoplifting (+79/100k) increased for distinct reasons. Misattribution leads to resource misallocation.

---

## Limitations

This analysis measures police-reported crime, not the true prevalence of criminal activity. Three questions remain structurally unaddressable:

1. **True crime prevalence.** With 71% of victimizations unreported nationally (2019 GSS) and reporting rates ranging from 6% (sexual assault) to 60% (motor vehicle theft), trends in reported crime may partially reflect trends in reporting behaviour.

2. **Causal drivers of the decline.** The 46% CSI reduction from 1998 to 2014 is documented but its causes remain debated: demographic ageing, incarceration trends, security technology, economic conditions, and cultural shifts all potentially contribute.

3. **Effectiveness of specific interventions.** Aggregate clearance rates, expenditure trends, and staffing ratios cannot attribute outcomes to specific programs or policies.

---

## Methodology

**Data sources:** Six Statistics Canada tables (35-10-0063-01, 35-10-0177-01, 18-10-0005-01, 35-10-0076-01, 35-10-0059-01) and four BC Government justice appendices (F-I). General Social Survey perception data (2004-2019) sourced from published Juristat reports.

**Key metrics:** Crime Severity Index (sentence-severity weighted, base 2006), crime rate per 100,000, clearance rate, unfounded rate, compound annual growth rate (CAGR).

**Statistical methods:** Linear regression for trend significance testing, chi-squared tests for compositional change, indexed growth analysis (base-100 normalization), year-over-year percentage change.

**Limitations:** Police-reported data only. COVID-19 distorted 2020-2021 data. Clearance does not equal conviction. Reporting rates range from 6% to 60% by crime type. GSS perception data most recently available from 2019.

---

## Reproducibility

```bash
pip install -r requirements.txt          # Install dependencies
python -m src.download                   # Download all datasets
python -m src.clean                      # Clean and normalize to parquet
python -m src.analysis.q1_is_crime_rising  # Section 1 charts
python -m src.analysis.q2_what_kinds       # Section 2 charts
python -m src.analysis.q3_justice          # Section 3 charts
python -m src.analysis.q3_costs            # Policing costs charts
python -m src.analysis.q4_geography        # Section 4 charts + interactive map
python -m src.analysis.q5_perception       # Section 5 charts
pytest                                     # Run tests
```

All charts regenerate from source data. Processed parquet files are stored in `data/processed/` (gitignored). Raw data is downloaded from Statistics Canada and BC Government open data portals.
