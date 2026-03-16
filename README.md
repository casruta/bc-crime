# BC Crime Data Analysis

An R Markdown analysis of crime trends across British Columbia, Canada, covering 2018--2023.

## What's in this repository

| File | Description |
|------|-------------|
| `BC Crime Data/Data Sets/BC CRIME.Rmd` | Main analysis report (HTML + PDF output) |
| `BC Crime Data/Data Sets/BC CRIME Worksheet.Rmd` | Exploration worksheet with reusable templates |
| `BC Crime Data/Data Sets/bc_crime.csv` | Source dataset (not included in repo) |

## Analysis highlights

- **Overall trends**: Year-over-year crime volume with COVID-19 context
- **Crime type breakdown**: Composition analysis, heatmap, rank changes, small multiples
- **Neighbourhood analysis**: Top areas, concentration (Lorenz) curve, change over time, crime profiles
- **Seasonal patterns**: Monthly trends and heatmaps (when data available)
- **Severity index**: Weighted crime scoring beyond raw counts

## Requirements

- R >= 4.0
- Key packages: `ggplot2`, `dplyr`, `tidyr`, `scales`, `knitr`, `rmarkdown`, `glue`
- All packages are auto-installed when the Rmd is knitted

## How to run

1. Place `bc_crime.csv` in the `BC Crime Data/Data Sets/` directory
2. Open `BC CRIME.Rmd` in RStudio
3. Click **Knit** to generate the HTML or PDF report

## Author

Casper Kacper Ruta (2024)
