# British Columbia Crime Analysis

> **Bottom line:** BC crime fell 46% from 2003 to 2014 and dropped another 7.4% in 2024, but violent crime's share has been rising since 2014 — the headline decline masks a compositional shift toward more serious offences. Interior communities face per-capita rates 2x the Lower Mainland's, and 42% of residents believe crime is getting worse. The priorities are clear: track the violent crossover, rebalance resources toward the interior, and close the growing gap between public perception and statistical reality.

---

**Crime in BC is falling in volume but shifting in character.** The Crime Severity Index dropped 46% from its 2003 peak of 166.9 to 90.2 in 2014, then fell another 7.4% in 2024. Yet violent crime's share has been climbing since 2014 while property crime collapses beneath it. Interior communities like Chilliwack (11,352 per 100,000) face crime rates double Vancouver's (5,438). And 42% of BC residents believe crime is rising despite two decades of decline. This summary distils five research questions, 42 charts, and 20 years of Statistics Canada data into the findings that matter most.

### Contents

| Section | Question | Charts |
|---|---|---|
| [1. Crime Trends](#1-crime-is-falling--but-the-mix-is-getting-worse) | Is crime rising? | Figures 1-8 |
| [2. Crime Types](#2-property-crime-is-collapsing-two-categories-are-surging) | What kinds of crime are changing? | Figures 9-16 |
| [3. Justice System](#3-the-justice-system-clears-violent-crime-but-loses-property-crime) | How effectively is crime addressed? | Figures 17-23, S1-S6 |
| [4. Geography](#4-crime-concentrates-in-the-interior-not-the-lower-mainland) | Where is crime concentrated? | Figures 24-30 + map |
| [5. Perception](#5-the-public-thinks-crime-is-rising--the-data-disagrees) | Why does crime feel like it's rising? | Figures 31-33 |
| [Implications](#what-these-findings-mean--and-what-to-do-about-them) | What should be done? | -- |
| [Methodology](#methodology--limitations) | Data sources and methods | -- |

---

## 1. Crime Is Falling — but the Mix Is Getting Worse

BC's Crime Severity Index peaked at 166.9 in 2003, fell 46% to 90.2 by 2014, and dropped a further 7.4% in 2024 — the second-largest provincial decline after Alberta (-8.5%). Over the full series, BC recorded 18 years of declining crime rates against 8 years of increases. Linear regression confirms the decline is statistically significant (p < 0.05), though the model doesn't capture the non-linear COVID-19 disruption that created an artificial dip in 2020 and partial rebound through 2022.

![Figure 1: BC Crime Severity Index — peak of 166.9 in 2003, 46% decline to 90.2 by 2014, continued decline in 2024](outputs/charts/q1_bc_csi_trend.png)

The composition tells a different story. Violent CSI has risen more steeply than non-violent CSI since 2014: the overall index stabilized because property crime's decline masked a violent-crime crossover (Figure 2). BC still sits roughly 21% above the national average, a gap that has persisted across the entire 20-year series regardless of whether crime was rising or falling.

![Figure 2: Violent CSI rising while non-violent CSI falls — the crossover that the headline number hides](outputs/charts/q1_violent_nonviolent_gap.png)

The year-over-year pattern reinforces this: BC recorded 18 years of decline against 8 years of increase, with the most recent year (2024) showing a 7.4% drop (Figure 3).

![Figure 3: BC year-over-year crime rate changes — 18 declining years vs. 8 increasing](outputs/charts/q1_bc_yoy_trend.png)

Saskatchewan runs at roughly 2x Ontario's rate, but all provinces share the same arc. Indexed to 2004 = 100, every comparison province shows a converging downward trajectory, with BC tracking the middle of the pack (Figures 4-5). The decline is structural, not provincial — driven by demographics, urbanization, and enforcement philosophy more than any single jurisdiction's policy.

![Figure 4: Provincial crime rate comparison — BC consistently above the national average](outputs/charts/q1_provincial_comparison.png)

![Figure 5: Indexed provincial growth (2004 = 100) — all provinces converge downward](outputs/charts/q1_indexed_provincial_growth.png)

The BC-Canada gap (Figure 6) has persisted across the entire series, and BC's 7.4% year-over-year decline ranks second among provinces after Alberta's 8.5% (Figure 7).

![Figure 6: BC-Canada crime rate gap — persistent across two decades](outputs/charts/q1_bc_canada_gap.png)

![Figure 7: Year-over-year change by province — BC's 7.4% drop is second-largest](outputs/charts/q1_yoy_by_province.png)

A breakdown of which offences contribute most to BC's overall CSI (Figure 8) reveals the violations that carry the most weight in the index — and therefore the most leverage for policy intervention.

![Figure 8: CSI contribution by violation type — which offences drive BC's overall severity index](outputs/charts/q1_csi_contribution.png)

BC Government data confirms the pattern at the most recent granularity (Figure below).

![BC Government year-over-year comparison, 2022-2023](outputs/charts/q2_bcgov_yoy_2022_2023.png)

**What the data can't tell us:** Whether the violent-crime increase reflects genuine behavioural change, reclassification of offences under revised Criminal Code provisions (particularly post-2019 amendments), or improved reporting mechanisms for domestic violence and sexual assault. The CSI weights offences by average sentence severity, so reclassification of a given act to a more serious category inflates the index even if the underlying behaviour is unchanged.

## 2. Property Crime Is Collapsing; Two Categories Are Surging

Property crime accounts for 51% of the total rate but has been declining steadily since the early 2000s (Figures 9-10). The five-year absolute drops are steep:

| Violation | 5-Year Change (per 100,000) |
|---|---|
| Theft from vehicles | -772 |
| Breaking and entering | -270 |
| Theft under $5,000 | -221 |
| Disturb the peace | -165 |

![Figure 9: Crime composition over time — property crime's share shrinking as violent crime's share grows](outputs/charts/q2_stacked_composition.png)

![Figure 10: Current composition shares — property crime still dominates at 51% but is declining](outputs/charts/q2_composition_shares.png)

The violation-level heatmap (Figure 11) shows the intensity pattern across all crime types and years, while Figure 12 ranks the largest absolute changes — theft from vehicles (-772/100k) leads all declines.

![Figure 11: Property violations cool from red to blue over time while violent types hold steady](outputs/charts/q2_heatmap.png)

![Figure 12: Largest absolute changes in crime rate — theft from vehicles leads all declines at -772/100k](outputs/charts/q2_top_changes.png)

The theft-from-vehicles decline is the single largest absolute drop of any violation. Multiple factors likely contribute: improved vehicle security, fewer valuables left visible, contactless payment reducing cash-carrying, and pandemic-era work-from-home patterns.

Two categories bucked the trend. Child pornography offences rose by 82 per 100,000 and shoplifting by 79. The child exploitation increase almost certainly reflects expanded digital investigation capacity (ICAC task forces, automated hash-matching, mandatory platform reporting) rather than a prevalence increase. The shoplifting rise is more ambiguous: genuine behavioural change, reduced in-store security staffing, and lower prosecution thresholds could each play a role.

![Figure 13: Violation trajectories diverge — property types slope down while exploitation and shoplifting climb](outputs/charts/q2_slope_ranking.png)

![Figure 14: Property crime's CAGR is negative while other categories are flat or positive](outputs/charts/q2_category_cagr.png)

Figures 15-16 spotlight the specific violations driving these trends. The rising violations spotlight (Figure 16) isolates the fastest-growing crime types for closer examination.

![Figure 15: Theft from vehicles plunges while shoplifting and exploitation climb — individual violation trajectories](outputs/charts/q2_specific_violation_trends.png)

![Figure 16: The fastest-growing violations — child exploitation and shoplifting lead absolute increases](outputs/charts/q2_rising_violations_spotlight.png)

Violent crime's absolute rate remains relatively flat, but its share of total crime is growing as property crime falls away beneath it. A Pareto analysis shows a small cluster of crime types accounts for roughly 80% of total volume. The chi-squared test for crime-type composition across years is statistically significant (p < 0.05), confirming the shift is real, not noise.

![BC Government year-over-year comparison by crime type, 2022-2023](outputs/charts/q2_bcgov_yoy_2022_2023.png)

## 3. The Justice System Clears Violent Crime but Loses Property Crime

Clearance rates split sharply by type. Violent crime clears above 50%; property crime clears below 30% — 7 in 10 property crimes go unresolved (Figures 17-18). These rates have held steady over the 2004-2024 period. The stability itself is the finding: two decades of reforms, technology investment, and budget growth haven't moved the needle on property-crime resolution. This points to a structural constraint — the sheer volume and low individual value of property offences making investigation uneconomical — rather than a fixable capacity gap.

![Figure 17: Clearance rate trends — violent crime stays above 50%, property crime stuck below 30%](outputs/charts/q3_clearance_rate_trends.png)

![Figure 18: Wide clearance variation — some violations clear above 70% while others languish below 20%](outputs/charts/q3_clearance_by_violation.png)

Youth crime severity has diverged from the adult trend (Figure 19), continuing to decline since 2014 while adult CSI rose or stabilized. Three candidate explanations: declining youth population share, diversion programs keeping cases out of the formal system, and generational behavioural shifts. The data supports the divergence but can't isolate the cause.

![Figure 19: Youth vs. adult CSI divergence — youth crime continues declining while adult crime stabilizes](outputs/charts/q3_youth_vs_adult_csi.png)

Policing model matters. Figure 20 compares RCMP and municipal force jurisdictions, while Figure 21 isolates the COVID-19 impact — the 2020 dip and subsequent rebound visible across categories.

![Figure 20: RCMP detachments and municipal forces show different crime trajectories](outputs/charts/q3_rcmp_vs_municipal.png)

![Figure 21: COVID-19 impact — the 2020 dip and post-pandemic rebound across crime categories](outputs/charts/q3_covid_impact.png)

The data rules out two alternative explanations for the overall decline. Unfounded rates have remained stable (Figure 22), so the drop isn't police reclassifying incidents. And the underreporting pattern runs the wrong way (Figure 23): property crime (~35% reported) declined more steeply than violent crime (~24% reported). If the decline were driven by people simply reporting less, the more-reported category would decline more slowly — the opposite of what we observe.

![Figure 22: Unfounded rates stable over time — ruling out reclassification as a driver of decline](outputs/charts/q3_unfounded_rates.png)

![Figure 23: Underreporting proxy analysis — the pattern contradicts a reporting-driven decline](outputs/charts/q3_underreporting_proxies.png)

### Policing costs are rising faster than crime is falling

BC police spending grew in both nominal and inflation-adjusted (constant 2020 dollar) terms even as crime severity dropped (Figures S1-S3). Salary and benefits growth outpaced operating and capital spending. BC's population grew 10.4% from 5,000,879 (2018) to 5,519,913 (2023), raising the question of whether staffing kept pace.

![Figure S1: BC policing expenditure — nominal vs. inflation-adjusted, both rising](outputs/charts/q3_bc_expenditure_trend.png)

![Figure S2: Per-capita policing cost comparison across provinces](outputs/charts/q3_per_capita_comparison.png)

![Figure S3: CSI vs. expenditure — spending rises while crime severity falls](outputs/charts/q3_csi_vs_expenditure.png)

The crimes-per-officer workload metric (Figure S6), overlaid with CSI, suggests declining crime volume was absorbed by expanding non-crime demands. Police increasingly respond to mental health crises, overdose calls, welfare checks, and social disorder — work that doesn't generate Criminal Code incidents but consumes patrol hours.

![Figure S4: Expenditure breakdown — salaries and benefits outpace operating and capital](outputs/charts/q3_expenditure_breakdown.png)

![Figure S5: Police staffing trend — officers per 100,000 population](outputs/charts/q3_staffing_trend.png)

![Figure S6: Crimes per officer with CSI overlay — declining crime hasn't reduced workload](outputs/charts/q3_crimes_per_officer.png)

## 4. Crime Concentrates in the Interior, Not the Lower Mainland

Vancouver (~48,812 offences) and Surrey (~41,275) lead in absolute volume (Figure 24), but per-capita rates reverse the map:

| Community | Rate per 100,000 | vs. Vancouver |
|---|---|---|
| Chilliwack | 11,352 | 2.1x |
| Kamloops | 10,546 | 1.9x |
| Vancouver | 5,438 | 1.0x |
| Victoria | 5,283 | 0.97x |

![Figure 24: Top 20 jurisdictions by total crime count — Vancouver and Surrey dominate volume](outputs/charts/q4_top_jurisdictions.png)

![Figure 25: The 8 largest jurisdictions follow different trajectories — some declining, others flat](outputs/charts/q4_jurisdiction_trends.png)

The per-capita comparison (Figure 26) is where the interior-coastal divide becomes stark. Interior CMAs face rates roughly 2x those of Vancouver and Victoria.

![Figure 26: CMA per-capita crime rate — interior communities at 2x the rate of coastal metros](outputs/charts/q4_cma_comparison.png)

![Figure 27: Interior CMA rates diverge upward from coastal CMAs over time](outputs/charts/q4_cma_trends.png)

The interior-coastal divide isn't random. Interior communities share a cluster of compounding risk factors: higher rates of homelessness and visible poverty, acute opioid-crisis exposure, seasonal tourism economies with transient populations, and reliance on RCMP detachments rather than dedicated municipal forces.

![Figure 28: Some jurisdictions have disproportionately violent profiles relative to their total crime](outputs/charts/q4_total_vs_violent.png)

![Figure 29: Crime is highly concentrated — a small number of jurisdictions account for most of BC's total](outputs/charts/q4_crime_concentration.png)

![Figure 30: Violent crime's share varies widely — some jurisdictions are 3x more violent than others](outputs/charts/q4_violent_share_distribution.png)

![Regional crime rate comparison across BC](outputs/charts/q4_region_comparison.png)

A composite neighbourhood ranking (60% standardized volume, 40% trend direction) classifies areas as high, moderate, or lower concern — identifying the intersections where intervention has the highest expected return. An ANOVA variance decomposition partitions total crime variation across year, crime type, and neighbourhood. The dimension that explains the most variance determines whether policy should prioritize place-based interventions, category-targeted programs, or time-sensitive responses.

[Interactive jurisdiction map (HTML)](outputs/charts/q4_interactive_map.html)

## 5. The Public Thinks Crime Is Rising — the Data Disagrees

The perception-reality gap widened between 2014 and 2019:

| Year | "Crime increased" | "About the same" |
|---|---|---|
| 2009 | 38% | 43% |
| 2014 | 30% | 48% |
| 2019 | 42% | 41% |

Figure 31 overlays the perception data against actual CSI, making the divergence visible.

![Figure 31: Perception vs. reality — 42% believe crime is rising while CSI remains below its peak](outputs/charts/q5_perception_vs_reality.png)

From 2009 to 2014, perception tracked reality: crime fell and fewer people believed it was rising. From 2014 to 2019, crime stabilized or rose slightly while perceived increase jumped 12 percentage points. The gap isn't a simple case of public ignorance — five concrete mechanisms explain why reasonable people reach the wrong conclusion from accurate observations.

### Why the gap exists

**1. The visibility paradox.** The crimes people witness are rising. Shoplifting (+79 per 100,000) happens in plain sight — in grocery stores, pharmacies, transit stations. The crimes driving the aggregate decline are invisible non-events: a car that wasn't broken into (theft from vehicles: -772/100k, Figure 12), a house that wasn't burglarized. People form perceptions from what they see, not from Statistics Canada tables. A resident who watches someone walk out of a store with unpaid goods every week has a rational basis for believing crime is getting worse. Their observation is accurate. The aggregate trend they infer from it is not.

**2. The compositional paradox.** People sensing "crime is getting worse" are partially right. Violent CSI has been climbing since 2014 (Figure 2) — assaults, threats, and weapons offences are genuinely increasing. The headline CSI falls only because property crime's massive decline masks the violent crossover. The public's intuition picks up the shift toward more serious offences; the aggregate statistic buries it under a falling total. When someone says "crime feels worse," they may be responding to the violent trend that the headline number conceals.

**3. The resolution gap.** Seven in ten property crimes go unresolved — clearance rates sit below 30% (Figures 17-18). When a resident reports a bike theft, a car break-in, or a package stolen from their porch and nothing happens, they conclude the system isn't working. That conclusion is accurate. From there, inferring that crime must be worsening is a short step. Low clearance doesn't just fail victims — it erodes the credibility of the statistics that claim crime is falling. Why trust the numbers from a system that can't solve your case?

**4. Locally rational perception.** Residents of Chilliwack (11,352/100k) and Kamloops (10,546/100k) live with crime rates roughly 2x Vancouver's (5,438/100k) (Figure 26). For them, crime IS high — their daily experience matches a genuinely elevated local reality, even if the provincial aggregate is declining. The General Social Survey is provincial, so these voices get averaged into a misleading provincial mean. A Kamloops resident who says "crime is rising" may be reporting their environment accurately; the statistic that says otherwise reflects a provincial average dominated by lower-crime coastal populations.

**5. Signal crimes and visible disorder.** Certain crimes reshape perception far beyond their statistical weight. A single violent assault in a neighbourhood communicates more threat than 100 fewer car break-ins. Visible social disorder — open drug use, encampments, aggressive panhandling — functions as a signal that "things are getting worse" even when these aren't Criminal Code offences captured in the CSI. BC's interior communities sit at the intersection of the opioid crisis, housing precarity, and concentrated homelessness. Residents in these areas experience a daily environment of disorder that the crime statistics don't measure but their perception registers. In criminology, these are called "signal crimes" (Innes, 2004) — events or conditions that communicate risk disproportionately to their actual prevalence.

### Confidence and reporting compound the gap

![Figure 32: Confidence in police by province — BC's middling confidence mirrors the national pattern](outputs/charts/q5_confidence_by_province.png)

Confidence in police is middling. In 2019, 30% of BC residents reported "a great deal of confidence," 47% "some confidence," 17% "not very much," and 5% "none at all" — closely mirroring the national distribution (32%/46%/15%/5%). Middling confidence reinforces the perception gap: residents who don't trust police also don't trust police-reported statistics.

The reporting rate gap (Figure 33) adds a structural layer. When only 6% of sexual assaults reach police but 60% of motor vehicle thefts do, the statistical record reflects a heavily filtered version of reality. A victim of unreported assault knows their experience is real regardless of whether it appears in the data. Multiply this across the 71% of victimizations that go unreported nationally, and the gap between lived experience and official statistics becomes not just explainable but inevitable.

![Figure 33: Reporting rates by crime type — from 6% (sexual assault) to 60% (motor vehicle theft)](outputs/charts/q5_reporting_rates.png)

The perception-reality gap is not a communication failure to be solved with better dashboards alone. It reflects a genuine disconnect between what the statistics measure (police-reported Criminal Code offences, severity-weighted) and what people experience (visible disorder, unsolved cases, rising violence in their community, unreported victimization). Bridging the gap requires not just publishing data, but addressing the underlying conditions — clearance rates, visible disorder, local crime concentration — that make the public's distrust rational.

---

## What These Findings Mean — and What to Do About Them

### Priority 1: Track the violent-crime crossover before it becomes a crisis

**Why now:** Violent CSI has climbed since 2014 while property-crime decline drives the headline 7.4% drop. Every year this compositional shift goes unmonitored, resources stay allocated to a property-crime problem that's solving itself.

**Next steps:** Report violent and non-violent CSI separately in quarterly dashboards. Flag any quarter where the violent-to-total ratio exceeds the previous year's annual average. Tie new investigative resource allocation to the violent-crime share trend, not the total-crime level.

### Priority 2: Rebalance resources toward interior communities

**Why now:** Chilliwack (11,352/100k) and Kamloops (10,546/100k) face per-capita rates 2x Vancouver's (5,438/100k), and the composite ranking shows several interior areas are both high-crime and worsening. Provincial funding formulas that weight absolute volume over per-capita intensity systematically underfund these communities.

**Next steps:** Adopt the composite ranking (volume 60% + trend 40%) as an input to allocation formulas. Conduct root-cause assessments in the top-5 ranked communities targeting housing, substance use, and economic precarity. Policing alone won't close this gap — cross-ministry coordination is the minimum viable intervention.

### Priority 3: Redeploy property-crime investigation capacity

**Why now:** Property crime clears below 30% (7 in 10 cases unresolved) and is declining steeply (theft from vehicles: -772/100k over five years). Violent crime clears above 50% — each additional detective-hour has higher expected clearance yield.

**Next steps:** Audit detective assignment by crime category. Model the clearance-rate gain from shifting one FTE from property to violent-crime investigation. Pilot in one high-composite-rank interior jurisdiction; measure clearance outcomes over 12 months before scaling.

### Priority 4: Close the perception-reality gap

**Why now:** The 12-point jump in perceived crime increase (30% to 42%, 2014-2019) occurred while CSI remained below its historical peak. Left unchecked, this gap creates political pressure to respond to perceptions rather than evidence — driving reactive policy that wastes resources.

**Next steps:** Publish a quarterly plain-language CSI dashboard at the provincial level, covering total and violent/non-violent breakdowns with per-capita rates by community. Pair with visible community policing in the 10 highest-rate jurisdictions. Target: reduce the "crime increased" perception by at least 5 points in the next GSS cycle.

### Priority 5: Separate detection increases from prevalence increases

**Why now:** Child exploitation offences (+82/100k) and shoplifting (+79/100k) lead absolute increases but for opposite reasons. Misdiagnosing expanded detection as a crime wave (or a genuine behavioural shift as a reporting artefact) leads to misallocation in both directions.

**Next steps:** For child exploitation, track case-initiation source (proactive tip vs. victim report) to test the detection-gain hypothesis. For shoplifting, compare incident reports against retail loss surveys and enforcement-hour data to isolate the primary driver.

### Monitoring cadence

| Metric | Frequency | Source | Trigger |
|---|---|---|---|
| Total + violent/non-violent CSI | Quarterly | StatsCan 35-10-0063-01 | Violent ratio exceeds prior annual average |
| Top-5 interior jurisdiction rates | Quarterly | BC Gov Appendix F | Any community exceeds 2x provincial average |
| Property vs. violent clearance | Annually | StatsCan 35-10-0177-01 | Property clearance below 25% or violent below 45% |
| Public perception (GSS) | Per cycle (~5 years) | StatsCan 35-10-0066-01 | "Crime increased" exceeds 45% |
| Child exploitation case source | Annually | Internal police data | Proactive share drops below 60% |

---

## What This Analysis Cannot Answer

This analysis measures what the system records, not what occurs. Three questions remain structurally out of reach:

1. **The true prevalence of crime.** With only 29% of victimizations reported nationally (2019 GSS), and reporting rates varying from 6% (sexual assault) to 60% (motor vehicle theft), the dark figure is large and unevenly distributed. Trends in reported crime may reflect trends in reporting behaviour as much as trends in criminal behaviour.

2. **Causal drivers of the decline.** The 46% CSI drop from 2003 to 2014 is well-documented but its causes are debated: demographic ageing, rising incarceration through the 2000s, improved security technology, economic conditions, and cultural shifts all contribute to varying degrees. This analysis measures the "what" precisely but cannot isolate the "why."

3. **The effectiveness of specific interventions.** Clearance rates, cost trends, and staffing ratios describe system performance at the aggregate level. They can't attribute outcomes to specific programs, policies, or leadership decisions. Answering those questions requires randomized or quasi-experimental evaluation designs that fall outside the scope of observational crime data.

---

## Methodology & Limitations

**Data sources:** Six Statistics Canada tables (35-10-0063-01, 35-10-0177-01, 18-10-0005-01, 35-10-0076-01, 35-10-0059-01, 35-10-0066/0068-01) and four BC Government justice appendices (F-I). BC population estimates from BC Stats (2018: 5,000,879 to 2023: 5,519,913).

**Key metrics:** Crime Severity Index (sentence-severity weighted, base 2006), crime rate per 100,000, clearance rate, unfounded rate, CAGR, chi-squared composition test, ANOVA variance decomposition.

**Statistical methods:** Linear regression with 95% confidence intervals on slope, chi-squared test for compositional independence, Ward's hierarchical clustering for neighbourhood grouping, ANOVA for variance partitioning, 2-year trend projections with fan-chart uncertainty bands.

**Limitations:** Police-reported data only — the "dark figure" of unreported crime (71% nationally per 2019 GSS) is not captured. COVID-19 distorts 2020-2021. Clearance does not equal conviction. Per-capita rates use mid-year population estimates revised post-census. Reporting rates range from 6% (sexual assault) to 60% (motor vehicle theft), creating structural blind spots that no methodology can fully resolve.

---

## Repository Structure

```
bc-crime/
├── src/
│   ├── __init__.py
│   ├── paths.py                       # Centralized path constants
│   ├── download.py                    # Fetch raw CSVs from StatsCan / BC Gov
│   ├── clean.py                       # Normalize, rename columns, write parquet
│   └── analysis/
│       ├── __init__.py
│       ├── theme.py                   # Palette, styling helpers (kds wrapper)
│       ├── q1_is_crime_rising.py      # Section 1 charts (8 PNG)
│       ├── q2_what_kinds.py           # Section 2 charts (9 PNG)
│       ├── q3_justice.py              # Section 3 charts (7 PNG)
│       ├── q3_costs.py                # Policing costs charts (6 PNG)
│       ├── q4_geography.py            # Section 4 charts (8 PNG + 1 HTML map)
│       └── q5_perception.py           # Section 5 charts (3 PNG)
├── data/
│   ├── README.md                      # Data dictionary with full lineage
│   ├── raw/                           # Downloaded source files (gitignored)
│   └── processed/                     # Cleaned parquet files (gitignored)
├── outputs/
│   └── charts/
│       ├── README.md                  # Chart index mapping filenames to figures
│       ├── q1_*.png ... q5_*.png      # 41 publication-ready charts
│       └── q4_interactive_map.html    # Plotly interactive map
├── tests/
├── notebooks/
│   └── bc_crime_report.ipynb          # Exploratory Jupyter notebook
├── generate_report.py                 # Convert README → Word .docx
├── requirements.txt
└── CLAUDE.md
```

See [`data/README.md`](data/README.md) for the full data dictionary and [`outputs/charts/README.md`](outputs/charts/README.md) for the complete chart index.

## How to Run

```bash
pip install -r requirements.txt            # Install dependencies
python -m src.download                     # Download all datasets (~8 GB)
python -m src.clean                        # Clean and normalize to parquet
python -m src.analysis.q1_is_crime_rising  # Section 1: Is crime rising? (8 charts)
python -m src.analysis.q2_what_kinds       # Section 2: What kinds? (9 charts)
python -m src.analysis.q3_justice          # Section 3: Justice system (7 charts)
python -m src.analysis.q3_costs            # Section 3: Policing costs (6 charts)
python -m src.analysis.q4_geography        # Section 4: Geography (8 charts + map)
python -m src.analysis.q5_perception       # Section 5: Perception (3 charts)
pytest                                     # Run tests
python generate_report.py                  # Generate Word report from this README
```

## Data Sources

| Table ID | Description | Coverage |
|----------|-------------|----------|
| 35-10-0063-01 | Crime Severity Index by police service | 1998-2024 |
| 35-10-0177-01 | Incident-based crime statistics (national) | 1998-2024 |
| 18-10-0005-01 | Consumer Price Index | 1914-2024 |
| 35-10-0076-01 | Police personnel and selected crime stats | 1986-2023 |
| 35-10-0059-01 | Police services expenditures (Canada) | 2018-2023 |
| 35-10-0066-01 | Perception of crime (GSS) | 2004-2019 |
| 35-10-0068-01 | Confidence in police (GSS) | 2004-2019 |
| BC Gov Appendix F | Crime Statistics in BC, 2023 | 2022-2023 |
| BC Gov Appendix G | BC Crime Trends | 2014-2023 |
| BC Gov Appendix H | BC Regional District Crime Trends | 2014-2023 |
| BC Gov Appendix I | BC Policing Jurisdiction Crime Trends | 2014-2023 |

## Author

Kacper Ruta (2024-2026)
