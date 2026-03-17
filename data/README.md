# BC Crime Analysis -- Data Dictionary

Comprehensive data codebook for the BC Crime Analysis project. This document describes every raw and processed dataset, the cleaning pipeline, jurisdiction mappings, and data lineage.

**To regenerate all data from scratch:**

```bash
python -m src.download
python -m src.clean
```

---

## Raw Data Sources -- Statistics Canada

| Table ID | Filename | Description | Coverage | Approx Size |
|----------|----------|-------------|----------|-------------|
| 35-10-0063-01 | `statscan/35100063.csv` | Crime Severity Index by police service in BC | 1998--2024 | ~21 MB |
| 35-10-0177-01 | `statscan/35100177.csv` | Incident-based crime statistics by province/CMA (national) | 1998--2024 | ~1.5 GB |
| 18-10-0005-01 | `statscan/18100005.csv` | Consumer Price Index, annual averages | 1914--2024 | ~13 MB |
| 35-10-0076-01 | `statscan/35100076.csv` | Police personnel and selected crime statistics | 1986--2023 | ~1.1 MB |
| 35-10-0059-01 | `statscan/35100059.csv` | Police services expenditures (Canada) | 2018--2023 | ~16 KB |
| 35-10-0066-01 | `statscan/35100066.csv` | Perception of crime in neighbourhood, by province (GSS) | 2004--2019 | ~500 KB |
| 35-10-0068-01 | `statscan/35100068.csv` | Confidence in police, by province (GSS) | 2004--2019 | ~500 KB |

Each table has a companion `*_MetaData.csv` file containing variable descriptions, footnotes, and correction notices.

**URLs** follow this pattern:

```
https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=XXXXXXXX01
```

Replace dashes in the Table ID to form the `pid`. For example, `35-10-0063-01` becomes `pid=3510006301`.

**Citation format:**

> Statistics Canada. Table [ID]: [Description]. [URL]. Accessed 2025.

---

## Raw Data Sources -- BC Government

| Appendix | Filename | Description | Coverage |
|----------|----------|-------------|----------|
| F | `bcgov/appendix_f_-_crime_statistics_in_bc_2023.xlsx` | Crime Statistics in BC, 2023 | 2022--2023 |
| G | `bcgov/appendix_g_-_bc_crime_trends_2014-2023.xlsx` | BC Crime Trends | 2014--2023 |
| H | `bcgov/appendix_h_-_bc_regional_district_crime_trends_2014-2023.xlsx` | BC Regional District Crime Trends | 2014--2023 |
| I | `bcgov/appendix_i_-_bc_policing_jurisdiction_crime_trends_2014-2023.xlsx` | BC Policing Jurisdiction Crime Trends | 2014--2023 |

**URLs** follow this pattern:

```
https://www2.gov.bc.ca/assets/gov/law-crime-and-justice/criminal-justice/police/publications/statistics/[filename]
```

**Citation format:**

> BC Ministry of Public Safety and Solicitor General. *Police Resources in British Columbia, 2023*. [URL]. Accessed 2025.

---

## Cleaning Pipeline (`src/clean.py`)

The cleaning pipeline transforms raw CSV and XLSX files into analysis-ready parquet files. Each step is described below.

1. **Column normalization** -- All column names are lowercased and spaces are replaced with underscores.

2. **GEO code stripping** -- Bracketed numeric codes appended by Statistics Canada are removed from geographic names. For example, `British Columbia [59]` becomes `British Columbia`.

3. **Suppression code handling** -- Statistics Canada uses several codes for suppressed, confidential, or unavailable values. The following are all replaced with `NaN`: `..`, `x`, `F`, `...`, and empty strings.

4. **VALUE coercion** -- The `value` column is cast to float using `pd.to_numeric(errors='coerce')`. Any remaining non-numeric values become `NaN`.

5. **Metadata column drops** -- The following columns are dropped as they carry no analytical value after cleaning: `DGUID`, `UOM_ID`, `SCALAR_FACTOR`, `SCALAR_ID`, `VECTOR`, `COORDINATE`, `SYMBOL`, `TERMINATED`, `DECIMALS`.

6. **ref_date parsing** -- The `REF_DATE` column is converted to an integer `year` column.

7. **BC Gov XLSX extraction** -- The multi-panel Excel layout used by BC Government appendices requires special handling:
   - Header row detection to locate the start of each data panel
   - Year column identification from the header row
   - Wide-to-long melt for jurisdiction-level data (Appendix I)
   - Panel extraction for trends data (Appendix G)

8. **Suppression markers in BC Gov data** -- The `-` character and empty strings in BC Government spreadsheets are replaced with `NaN`.

---

## Processed Files Schema

All processed files are written to `data/processed/` in Apache Parquet format.

### crime_severity_bc.parquet

**Source:** 35-10-0063-01 | **Rows:** ~50K+

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| year | Int64 | Reference year | 2024 |
| geo | string | Geographic area (BC province or police service) | British Columbia |
| statistic | string | Measure type | Crime severity index |
| value | float64 | Numeric value | 92.3 |
| uom | string | Unit of measure | Index |

### crime_incidents_national.parquet

**Source:** 35-10-0177-01 | **Rows:** ~1M+

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| year | Int64 | Reference year | 2024 |
| geo | string | Province, territory, or CMA | British Columbia |
| violation | string | Criminal Code violation category | Total, all Criminal Code violations (excluding traffic) [50] |
| statistic | string | Measure type | Rate per 100,000 population |
| value | float64 | Numeric value | 7234.5 |
| uom | string | Unit of measure | Rate |

### cpi.parquet

**Source:** 18-10-0005-01

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| year | Int64 | Reference year | 2024 |
| geo | string | Geography (Canada or British Columbia) | Canada |
| cpi | float64 | Consumer Price Index (2002=100) | 163.2 |

### bc_gov_trends.parquet

**Source:** Appendix G

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| offence | string | Offence category name | Total Criminal Code |
| year | int | Year | 2023 |
| count | float64 | Number of offences | 45123.0 |
| sheet | string | Source Excel sheet name | Criminal Code Offences |

### bc_gov_jurisdiction_trends.parquet

**Source:** Appendix I

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| region | string | BC region | Lower Mainland |
| type_of_policing | string | Policing model | Independent Municipal |
| policing_jurisdiction | string | Jurisdiction name | Vancouver Mun |
| year | Int64 | Year | 2023 |
| count | float64 | Number of offences | 53421.0 |
| category | string | Offence category | Criminal Code Offences |

### bc_gov_stats_2023.parquet

**Source:** Appendix F

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| crime_category | string | Crime category | Total Criminal Code |
| count_2022 | float64 | Offence count, 2022 | 41234.0 |
| count_2023 | float64 | Offence count, 2023 | 39876.0 |
| rate_2022 | float64 | Rate per 100k, 2022 | 7890.2 |
| rate_2023 | float64 | Rate per 100k, 2023 | 7654.1 |

### jurisdiction_mapping.parquet

**Source:** `clean.py` JURISDICTION_MAP

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| bcgov_name | string | BC Government jurisdiction name | Vancouver Mun |
| statcan_name | string | Statistics Canada GEO name | Vancouver, City, Municipal |

### gss_perception.parquet

**Source:** 35-10-0066-01

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| year | Int64 | GSS survey reference year | 2019 |
| geo | string | Province or Canada | British Columbia |
| response | string | Perception response | Increased |
| value | float64 | Percentage of respondents | 42.0 |

### gss_confidence.parquet

**Source:** 35-10-0068-01

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| year | Int64 | GSS survey reference year | 2019 |
| geo | string | Province | British Columbia |
| confidence_level | string | Level of confidence in police | Great deal of confidence |
| value | float64 | Percentage of respondents | 30.0 |

---

## Jurisdiction Mapping

The following 23-entry mapping links BC Government jurisdiction names to their Statistics Canada GEO equivalents. This mapping is defined in `JURISDICTION_MAP` inside `src/clean.py` and exported as `jurisdiction_mapping.parquet`.

| BC Gov Name | StatCan GEO Name |
|-------------|------------------|
| Abbotsford Mun | Abbotsford, City, Municipal |
| Burnaby Mun | Burnaby, City, Municipal |
| Central Saanich Mun | Central Saanich, District, Municipal |
| Delta Mun | Delta, City, Municipal |
| Esquimalt Mun | Esquimalt, Township, Municipal |
| Kamloops Mun | Kamloops, City, Municipal |
| Langley Mun | Langley, Township, Municipal |
| Nanaimo Mun | Nanaimo, City, Municipal |
| Nelson Mun | Nelson, City, Municipal |
| New Westminster Mun | New Westminster, City, Municipal |
| North Vancouver RCMP Mun | North Vancouver, District, Municipal |
| Oak Bay Mun | Oak Bay, District, Municipal |
| Penticton Mun | Penticton, City, Municipal |
| Port Moody Mun | Port Moody, City, Municipal |
| Prince George Mun | Prince George, City, Municipal |
| Richmond Mun | Richmond, City, Municipal |
| Saanich Mun | Saanich, District, Municipal |
| Surrey Mun | Surrey, City, Municipal |
| Vancouver Mun | Vancouver, City, Municipal |
| Vernon Mun | Vernon, City, Municipal |
| Victoria Mun | Victoria, City, Municipal |
| West Vancouver Mun | West Vancouver, District, Municipal |
| White Rock Mun | White Rock, City, Municipal |

---

## Data Lineage

### Statistics Canada Pipeline

```
                        ┌─────────────────┐
                        │  Statistics      │
                        │  Canada API      │
                        └────────┬────────┘
                                 │ download_statcan_table()
                                 ▼
┌──────────────────────────────────────────────────┐
│  data/raw/statscan/                              │
│  ├── 35100063.csv + _MetaData.csv                │
│  ├── 35100177.csv + _MetaData.csv                │
│  ├── 18100005.csv + _MetaData.csv                │
│  ├── 35100076.csv + _MetaData.csv                │
│  ├── 35100059.csv + _MetaData.csv                │
│  ├── 35100066.csv + _MetaData.csv                │
│  └── 35100068.csv + _MetaData.csv                │
└───────────────────────┬──────────────────────────┘
                        │ clean_crime_severity_bc()
                        │ clean_crime_incidents_national()
                        │ clean_cpi()
                        ▼
┌──────────────────────────────────────────────────┐
│  data/processed/                                 │
│  ├── crime_severity_bc.parquet                   │
│  ├── crime_incidents_national.parquet            │
│  ├── cpi.parquet                                 │
│  ├── bc_gov_trends.parquet                       │
│  ├── bc_gov_jurisdiction_trends.parquet          │
│  ├── bc_gov_stats_2023.parquet                   │
│  ├── jurisdiction_mapping.parquet                │
│  ├── gss_perception.parquet                      │
│  └── gss_confidence.parquet                      │
└───────────────────────┬──────────────────────────┘
                        │ q1_is_crime_rising.run_all()
                        │ q2_what_kinds.run_all()
                        │ q3_justice.run_all()
                        │ q3_costs.run_all()
                        │ q5_perception.run_all()
                        │ q4_geography.run_all()
                        ▼
┌──────────────────────────────────────────────────┐
│  outputs/charts/                                 │
│  ├── q1_*.png  (8 charts)                        │
│  ├── q2_*.png  (8 charts)                        │
│  ├── q3_*.png  (11 charts)                       │
│  ├── q4_*.png  (7 charts)                        │
│  ├── q4_interactive_map.html                     │
│  └── q5_*.png  (3 charts)                        │
└──────────────────────────────────────────────────┘
```

### BC Government Pipeline

```
┌─────────────────┐
│  BC Gov website  │
└────────┬────────┘
         │ download_bcgov_file()
         ▼
┌──────────────────────────────────┐
│  data/raw/bcgov/                 │
│  ├── appendix_f_*.xlsx           │
│  ├── appendix_g_*.xlsx           │
│  ├── appendix_h_*.xlsx           │
│  └── appendix_i_*.xlsx           │
└────────────────┬─────────────────┘
                 │ clean_bc_gov_trends()
                 │ clean_bc_gov_jurisdiction_trends()
                 │ clean_bc_gov_stats_2023()
                 │ get_jurisdiction_mapping()
                 ▼
         (merges into data/processed/ above)
```

---

## External References

> Cotter, A. (2021). *Criminal victimization in Canada, 2019*. Statistics Canada, *Juristat*, Catalogue no. 85-002-X. https://www150.statcan.gc.ca/n1/pub/85-002-x/2021001/article/00014-eng.htm

This source is used in the underreporting analysis (Figure 23, `q3_justice.py`) for GSS victimization survey context showing that only 29% of criminal victimizations are reported to police.

> Statistics Canada. Table 35-10-0066-01: Perception of neighbourhood crime. https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3510006601

> Statistics Canada. Table 35-10-0068-01: Confidence in the police. https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3510006801
