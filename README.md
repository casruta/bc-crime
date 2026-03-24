# BC Crime Data Analysis

An R Markdown analysis of crime trends across British Columbia, Canada, covering 2018--2023.

## Repository Structure

```
BC-CRIME-/
├── src/                 Source R Markdown files and stylesheets
│   ├── BC-CRIME.Rmd           Main analysis report
│   ├── BC-CRIME-Worksheet.Rmd Exploration worksheet with reusable templates
│   └── custom.css             Custom HTML styling
├── data/                Place bc_crime.csv here (not tracked in git)
├── output/              Generated HTML/PDF reports (not tracked in git)
├── docs/                Project documentation
│   └── improvement_log.md     Iteration history and scoring
└── README.md
```

## Analysis Highlights

- **Overall trends**: Year-over-year crime volume with COVID-19 context
- **Crime type breakdown**: Composition analysis, heatmap, rank changes, small multiples
- **Neighbourhood analysis**: Top areas, concentration (Lorenz) curve, change over time, crime profiles
- **Seasonal patterns**: Monthly trends and heatmaps (when data available)
- **Severity index**: Weighted crime scoring beyond raw counts
- **Statistical depth**: Correlation matrix, indexed comparisons, linear trend analysis

## Requirements

- R >= 4.0
- Key packages: `ggplot2`, `dplyr`, `tidyr`, `scales`, `knitr`, `rmarkdown`, `glue`
- All packages are auto-installed when the Rmd is knitted

## How to Run

1. Place `bc_crime.csv` in the `data/` directory
2. Open `src/BC-CRIME.Rmd` in RStudio
3. Click **Knit** to generate the HTML or PDF report
4. Output will be saved in `output/`

## Data Format

The analysis expects a CSV file with these columns:

| Column | Description |
|--------|-------------|
| `YEAR` | Year of the crime record (e.g., 2018--2023) |
| `TYPE` | Crime type category (e.g., "Homicide", "Theft from Vehicle") |
| `NEIGHBOURHOOD` | Geographic area where the crime occurred |
| `MONTH` | Month of the crime (optional; seasonal analysis is skipped if absent) |

## Author

Casper Kacper Ruta (2024)
