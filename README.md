<p align="center">
  <img src="banner.png" alt="BC CRIME" width="100%">
</p>

# British Columbia Crime Analysis (1998-2024)

Crime in British Columbia has fallen steadily for more than two decades. The Crime Severity Index (CSI) dropped 46% from its 1998 peak of 166.9 to 90.2 by 2014, and continued to decline through 2024, when it posted a 7.4% year-over-year decrease (the second-largest provincial drop, after Alberta's 8.5%).

This analysis covers the full 1998-2024 CSI series alongside Statistics Canada and BC Government data, addressing five questions through its charts and one interactive map. The CSI series begins in 1998; other datasets, including provincial comparisons and General Social Survey (GSS) perception data, start in 2004. Data end dates vary by source: CSI through 2024, BC Government and policing expenditure data through 2023.

> **Key findings:** Crime severity fell 46% between 1998 and 2014, but the mix of crime types shifted toward violent offences after 2014. Interior communities like Chilliwack and Kamloops record per-capita crime rates 1.9 to 2.1 times Vancouver's. Meanwhile, public perception of rising crime grew from 30% to 42% between 2014 and 2019, even as the numbers declined. Section 5 identifies five factors in the data that help explain this gap.

---

## Table of Contents

1. [Crime Severity Trends](#1-crime-severity-has-declined-but-the-mix-has-shifted)
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

- **Crime Severity Index (CSI)**: A Statistics Canada measure that weights criminal incidents by the average sentence length and incarceration rate for each offence type (base year: 2006). Higher values mean more severe crime overall.
- **Crime rate**: The number of police-reported incidents per 100,000 population, without adjusting for severity.
- **Clearance rate**: The share of reported incidents where police identified a suspect, whether or not charges were laid.
- **Unfounded rate**: The share of incidents that police determined, after investigation, did not actually occur or did not amount to a criminal offence.
- **Indexed growth (base-100)**: A way of comparing change over time by setting a reference year to 100. A reading of 85 means a 15% decline from that reference year.
- **Census Metropolitan Area (CMA)**: A Statistics Canada geographic unit that groups a city with its surrounding commuter municipalities. CMA-level crime rates cover the broader metro area, not just the core city.
- **Compound annual growth rate (CAGR)**: The average annual rate of change over a multi-year period, smoothing out year-to-year fluctuations.

---

## 1. Crime Severity Has Declined, but the Mix Has Shifted

The trend is clear. BC's Crime Severity Index dropped from 166.9 in 1998 to 90.2 in 2014, a 46% reduction. It fell a further 7.4% in 2024. Of the 26 year-over-year changes between 1998 and 2024, 18 were declines and 8 were increases. A linear regression test confirms the downward trend is statistically significant (p < 0.05), meaning it is unlikely to reflect random year-to-year variation.

![BC Crime Severity Index: 46% decline from 1998 peak (166.9) to 2014 trough (90.2), continued decline through 2024](outputs/charts/q1_bc_csi_trend.png)

But the types of crime behind the index began moving in opposite directions after 2014. Violent crime severity rose. Non-violent severity kept falling. The overall index still declined because the drop in property crime was large enough to offset the rise in violent offences. On average across the full series, BC's CSI averaged about 21% above the national figure.

![Violent CSI trending upward since 2014 while non-violent CSI continues to decline](outputs/charts/q1_violent_nonviolent_gap.png)

BC was not alone in this. Every province saw crime fall over the same period. When each province's 2004 crime rate is set to a baseline of 100, all trajectories slope downward at similar rates. Saskatchewan's rate stayed roughly 2.8 times Ontario's in absolute terms, but both declined at comparable rates.

Every province moved in the same direction at the same time. Broad shared forces (an ageing population, urbanization, shifts in enforcement philosophy) are commonly proposed explanations. This analysis does not test them directly, but the cross-provincial uniformity is hard to reconcile with jurisdiction-specific policies.

![Provincial crime rate comparison: BC consistently above the national average](outputs/charts/q1_provincial_comparison.png)

![Indexed provincial growth (2004 = 100): all provinces converge downward](outputs/charts/q1_indexed_provincial_growth.png)

Despite the decline, BC's crime rate stayed above the national average for the entire period. The charts below show the persistent gap and how BC's 2024 drop compared to other provinces.

![BC-Canada crime rate gap throughout the series](outputs/charts/q1_bc_canada_gap.png)

![Year-over-year change by province: BC's 7.4% drop ranks second-largest](outputs/charts/q1_yoy_by_province.png)

A small number of offence types carry most of the CSI weight. These are the categories where policy changes would have the largest effect on the overall index.

![CSI contribution by violation type: a small number of offences account for most of the index weight](outputs/charts/q1_csi_contribution.png)

BC Government data at the jurisdiction level confirm the same pattern through 2023, with continued property crime contraction and stable or rising violent offence counts (see Section 2 for the detailed year-over-year comparison).

### Is the Decline Real?

Two pieces of evidence support the conclusion that crime genuinely fell, rather than being an artifact of changed reporting or police reclassification.

First, unfounded rates (the share of reports that police determine are not actual crimes) stayed stable over the full period. If police had been reclassifying more incidents as unfounded, the crime rate would drop without any real change in criminal activity. The stable unfounded rate rules this out.

![Unfounded rates stable over time: reclassification did not drive the decline](outputs/charts/q3_unfounded_rates.png)

Second, the underreporting data points in a different direction. If people were simply calling the police less often, the numbers would fall fastest for crime types that are already underreported, because even a small drop in reporting has a big proportional effect when few people report in the first place. Violent crime is reported less often (~24% of incidents) than property crime (~35%). So if reporting were declining, violent crime numbers should fall faster. The opposite happened: property crime dropped more steeply.

That pattern does not match a decline driven by fewer people calling the police, though it does not rule out reporting changes affecting specific crime types differently.

![Underreporting proxy analysis: the pattern is inconsistent with a reporting-driven decline](outputs/charts/q3_underreporting_proxies.png)

**Caveat:** The CSI weights offences by average sentence length and incarceration rate. When Criminal Code revisions reclassify an act to a more serious category, the index rises even if the underlying behaviour is unchanged. Post-2019 amendments to domestic violence and sexual assault definitions may account for some of the observed increase in violent crime severity.

## 2. Property Crime Trends and Emerging Offence Categories

Most property crime categories have been declining since the early 2000s, though shoplifting is a notable exception. Property offences as a group still made up 51% of total reported incidents as of 2023. Across all crime categories, the largest absolute changes over the most recent five-year window in the data were:

| Violation | 5-Year Change (per 100,000) |
|---|---|
| Theft from vehicles | -772 |
| Breaking and entering | -270 |
| Theft under $5,000 | -221 |
| Disturb the peace | -165 |

Theft from vehicles led all declines at 772 per 100,000. Shoplifting moved in the opposite direction, rising by 79 per 100,000 over the same period.

![Crime composition over time: property crime's share contracting as violent crime's share grows](outputs/charts/q2_stacked_composition.png)

![Current composition shares: property crime accounts for 51% of total but is declining](outputs/charts/q2_composition_shares.png)

The heatmap below shows property offence rates declining from elevated levels over the study period while violent types stayed comparatively steady.

![Violation-level intensity heatmap: property violations cooling while violent types hold steady](outputs/charts/q2_heatmap.png)

![Largest absolute changes in crime rate: theft from vehicles leads all declines at -772/100k](outputs/charts/q2_top_changes.png)

Factors plausibly behind the vehicle-theft decline include improved vehicle security, reduced visibility of valuables, and contactless payment adoption. The relative contribution of each has not been empirically isolated.

Two violation categories moved against the overall trend. The rate of police-reported sexual violations against children rose by 82 per 100,000 over five years, and shoplifting rose by 79 per 100,000. The child exploitation increase aligns with expanded digital investigation capacity (Internet Crimes Against Children task forces, automated hash-matching, mandatory platform reporting) rather than an actual increase in offending. If the increase is detection-driven, the policy response should differ from one targeting rising prevalence.

Shoplifting's rise has several candidate explanations: behavioural change, reduced retail security staffing, and shifts in prosecution thresholds have all been cited.

![Property violation trajectories declining while exploitation and shoplifting trend upward](outputs/charts/q2_slope_ranking.png)

![Property crime CAGR is negative; other categories are flat or positive](outputs/charts/q2_category_cagr.png)

The practical consequence of this divergence is important. The offences driving the aggregate decline (vehicle theft, break-ins) responded to technology and environmental changes. The offences driving the increase (child exploitation, shoplifting) require enforcement and regulatory responses. The two groups need different intervention models.

![Individual violation trajectories: theft from vehicles declining sharply, shoplifting and exploitation rising](outputs/charts/q2_specific_violation_trends.png)

![Fastest-growing violations: child exploitation and shoplifting lead absolute increases](outputs/charts/q2_rising_violations_spotlight.png)

While violent crime's absolute rate stayed relatively stable, its share of total crime grew as property offences fell. A chi-squared test (which measures whether the distribution of crime types changed more than random chance would predict) confirmed the shift was statistically significant (p < 0.05).

![BC Government year-over-year comparison by crime type, 2022-2023](outputs/charts/q2_bcgov_yoy_2022_2023.png)

## 3. Clearance Rates, Youth Crime, and Policing Costs

Clearance rates split sharply by crime type. Violent crime clearance stood at 58.4% in 2014 but fell to 37.4% by 2024, a 21-percentage-point drop. The causes of this decline are not established in the available data.

Property crime clearance barely moved. It stayed in the 12-16% range for the entire study period, meaning roughly 85% of reported property offences went unresolved across two decades.

![Clearance rate trends: violent crime clearance declining from above 50% toward 37%; property crime stable at 12-16%](outputs/charts/q3_clearance_rate_trends.png)

![Clearance variation by violation: some types clear above 70% while others remain below 20%](outputs/charts/q3_clearance_by_violation.png)

Despite two decades of reforms, technology investment, and budget growth, property-crime clearance rates barely budged. One proposed explanation is a structural ceiling: the volume and low individual value of property offences may make case-by-case investigation uneconomical at current resource levels. The data in this analysis cannot confirm or rule out this interpretation.

Youth crime severity split from the adult trend after 2014. Youth CSI continued to decline while adult CSI stabilized or edged upward. Among candidate explanations, diversion programs are the most commonly cited: formal system contact for youth decreased as extrajudicial measures expanded (programs that channel youth away from the court system into community-based interventions). Declining youth population share may also play a role, though it does not fully account for the size of the youth-adult gap.

![Youth vs. adult CSI divergence: youth crime continues declining while adult crime stabilizes](outputs/charts/q3_youth_vs_adult_csi.png)

RCMP detachments and municipal forces followed different crime trajectories. Interior communities, which are predominantly policed by RCMP detachments, post the highest per-capita rates. The data cannot determine whether the policing model or other local factors drive the difference.

COVID-19 produced a visible dip in 2020 followed by a partial rebound, though crime levels in most categories did not return to pre-pandemic baselines.

![RCMP detachments and municipal forces show different crime trajectories](outputs/charts/q3_rcmp_vs_municipal.png)

![COVID-19 impact: 2020 dip and post-pandemic rebound across crime categories](outputs/charts/q3_covid_impact.png)

### Policing Expenditure Trends

Spending rose as crime fell. Over the 2018-2023 period for which expenditure data is available, police budgets in BC expanded in both nominal and real (constant 2020 dollar) terms, with salary and benefits growing faster than operating and capital spending.

BC's population grew 10.4% over the same window (from 5,000,879 to 5,519,913), meaning per-capita policing costs rose even after accounting for population growth.

![BC policing expenditure: nominal and inflation-adjusted, both rising](outputs/charts/q3_bc_expenditure_trend.png)

![Per-capita policing cost comparison across provinces](outputs/charts/q3_per_capita_comparison.png)

![CSI vs. expenditure: spending rises while crime severity falls](outputs/charts/q3_csi_vs_expenditure.png)

Even with fewer crimes, officers are not less busy. The crimes-per-officer metric shows that declining crime volume did not lead to a proportional reduction in workload. Police services attribute this to expanding non-crime demands such as mental health crisis response, overdose calls, and welfare checks, though this analysis does not independently measure non-crime call volume.

![Expenditure breakdown: salaries and benefits outpace operating and capital](outputs/charts/q3_expenditure_breakdown.png)

![Police staffing trend: officers per 100,000 population](outputs/charts/q3_staffing_trend.png)

![Crimes per officer with CSI overlay: declining crime has not reduced workload](outputs/charts/q3_crimes_per_officer.png)

## 4. Geographic Distribution of Crime

In absolute terms, Vancouver (~48,812 offences) and Surrey (~41,275) led the province. Per-capita rates tell a different story: interior communities recorded substantially higher figures.

| Community | Rate per 100,000 | Ratio to Vancouver |
|---|---|---|
| Chilliwack | 11,352 | 2.1x |
| Kamloops | 10,546 | 1.9x |
| Vancouver | 5,438 | 1.0x |
| Victoria | 5,283 | 0.97x |

![Top 20 jurisdictions by total crime count: Vancouver and Surrey lead in volume](outputs/charts/q4_top_jurisdictions.png)

![The 8 largest jurisdictions follow different trajectories](outputs/charts/q4_jurisdiction_trends.png)

At the CMA level, interior per-capita rates ran 1.9 to 2.1 times those of Vancouver (5,438/100k) and Victoria (5,283/100k). The gap widened over the study period.

![CMA per-capita crime rate: interior communities at approximately 2x the rate of coastal metros](outputs/charts/q4_cma_comparison.png)

![Interior CMA rates diverging upward from coastal CMAs over time](outputs/charts/q4_cma_trends.png)

The opioid crisis and visible homelessness stand out as the most commonly cited factors behind the interior-coastal divide, followed by seasonal tourism economies and reliance on RCMP contract policing rather than dedicated municipal forces. The available data cannot rank these causes definitively.

![Some jurisdictions have disproportionately violent profiles relative to their total crime](outputs/charts/q4_total_vs_violent.png)

![Crime concentration: a small number of jurisdictions account for most of BC's total](outputs/charts/q4_crime_concentration.png)

![Violent crime's share varies widely: some jurisdictions are 3x more violent than others](outputs/charts/q4_violent_share_distribution.png)

![Regional crime rate comparison across BC](outputs/charts/q4_region_comparison.png)

Communities were ranked using a composite score: 60% based on current crime volume and 40% on whether the trend is worsening. Areas with both high absolute levels and rising trajectories scored highest. The ranking classified communities as high, moderate, or lower concern for resource allocation.

[Interactive jurisdiction map (HTML)](outputs/charts/q4_interactive_map.html)

## 5. Public Perception and Statistical Trends

Between 2014 and 2019, the share of BC residents who said crime had increased rose from 30% to 42% (General Social Survey), a 12-percentage-point swing during a period when the CSI was declining.

| Year | "Crime increased" | "About the same" |
|---|---|---|
| 2009 | 38% | 43% |
| 2014 | 30% | 48% |
| 2019 | 42% | 41% |

![Perception vs. reality: 42% of residents believe crime is rising while CSI remains below its peak](outputs/charts/q5_perception_vs_reality.png)

Five factors in the data help explain this gap. For each, a potential corrective action is proposed.

### Factor 1: The Headline Number Hides the Violent Crime Increase

The violent component of the CSI rose after 2014 while the non-violent component fell. Because property crime's absolute decline was larger, the aggregate index still dropped. But residents likely respond more to the violent-crime component, which matters more for personal safety. Reporting violent and non-violent CSI components separately would make this divergence visible.

### Factor 2: Visible vs. Invisible Crime

Shoplifting increased by 79 per 100,000 and is directly observable in retail settings. Offsetting declines (772 fewer vehicle thefts and 270 fewer break-ins per 100,000) produce no observable signal. The shoplifting increase was dwarfed by the vehicle theft decrease, but shoplifting is far more visible to the public. Publishing quarterly scorecards pairing increasing and decreasing categories would help balance the picture.

### Factor 3: Low Clearance Rates Erode Trust

Property crime clearance stayed in the 12-16% range for the entire study period. When the institution reporting crime statistics leaves most reported cases unresolved, the public may discount its claims about overall crime trends. Implementing closed-loop case reporting with 30-day status updates for all filed reports could help rebuild trust.

### Factor 4: Provincial Averages Mask Local Reality

Chilliwack (11,352/100k) and Kamloops (10,546/100k) posted per-capita rates roughly 2x Vancouver's 5,438. For residents of these communities, provincial claims of declining crime may not match their experience. Jurisdiction-level dashboards with per-capita resource allocation would ground the data in local reality.

### Factor 5: Disorder That the CSI Does Not Measure

Open drug use, encampments, and aggressive panhandling are not Criminal Code offences and do not appear in the CSI. In communities with acute opioid-crisis exposure, these phenomena may dominate daily experience. A community disorder index built from police calls for service (wellness checks, trespass, mischief), published alongside the CSI, would capture what the current metric misses.

### Confidence and Reporting Rates

In the 2019 GSS, 30% of BC residents reported "a great deal of confidence" in police, with 47% reporting "some," 17% "not very much," and 5% "none." These figures tracked the national distribution (32%/46%/15%/5%).

![Confidence in police by province: BC's figures track the national pattern](outputs/charts/q5_confidence_by_province.png)

Reporting rates ranged from 6% (sexual assault) to 60% (motor vehicle theft). Nationally, 71% of victimizations went unreported (2019 GSS).

![Reporting rates by crime type: from 6% (sexual assault) to 60% (motor vehicle theft)](outputs/charts/q5_reporting_rates.png)

---

## Implications

**1. Track violent and non-violent crime separately.** We recommend reporting the violent and non-violent CSI components in separate quarterly dashboards. The compositional shift has been underway since 2014, and the current aggregate number masks it.

**2. Rebalance resources toward interior communities.** The composite ranking (60% volume, 40% trend) could serve as an input to funding formulas. Per-capita rates in interior CMAs are 1.9 to 2.1 times coastal rates, and the gap has widened over the study period.

**3. Review the balance between property and violent crime investigation.** Property crime clears in the 12-16% range regardless of resource allocation, while violent crime clearance has dropped 21 points since 2014. The causes of the clearance decline are not established in this analysis, but the scale of the drop warrants a review of how investigation resources are allocated.

**4. Address the perception-reality gap.** Quarterly plain-language dashboards with total and component breakdowns by community would help. The 12-percentage-point increase in perceived crime (30% to 42%, 2014-2019) occurred during a period of declining CSI.

**5. Distinguish detection increases from prevalence increases.** Child exploitation (+82/100k) and shoplifting (+79/100k) rose for different reasons. Treating them the same leads to misallocated resources.

---

## Limitations

This analysis measures police-reported crime, not the true prevalence of criminal activity.

1. **True crime prevalence.** With 71% of victimizations unreported nationally (2019 GSS) and reporting rates ranging from 6% (sexual assault) to 60% (motor vehicle theft), trends in reported crime may partly reflect trends in reporting behaviour.

2. **Causal drivers of the decline.** The 46% CSI reduction from 1998 to 2014 is documented, but its causes remain contested. Demographic ageing and security technology are the most frequently cited drivers, with economic conditions and cultural shifts also in the mix.

3. **Effectiveness of specific interventions.** Aggregate clearance rates, expenditure trends, and staffing ratios cannot attribute outcomes to specific programs or policies.

---

## Methodology

**Data sources:** Five Statistics Canada tables (35-10-0063-01, 35-10-0177-01, 18-10-0005-01, 35-10-0076-01, 35-10-0059-01) and four BC Government justice appendices (F-I). General Social Survey perception data (2004-2019) sourced from published Juristat reports.

**Key metrics:** Crime Severity Index (sentence-severity weighted, base 2006), crime rate per 100,000, clearance rate, unfounded rate, compound annual growth rate (CAGR).

**Statistical methods:** Linear regression for trend significance testing, chi-squared tests for compositional change, indexed growth analysis (base-100 normalization), year-over-year percentage change.

**Limitations:** Police-reported data only. COVID-19 distorted 2020-2021 data. Clearance does not equal conviction. Reporting rates range from 6% to 60% by crime type. GSS perception data most recently available from 2019. Data end dates vary by source: CSI through 2024, BC Government data through 2023, policing expenditure through 2023.

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
