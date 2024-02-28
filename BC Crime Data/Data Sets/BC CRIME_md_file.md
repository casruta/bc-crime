---
title: "Exploring the Crime Landscape in British Colombia, Canada"
author: "Casper Kacper Ruta"
date: "2024-02-25"
output:
  pdf_document: default
  html_document: default
---
```{r}
# Loading and Installing the Necessary Documents. 
packages <- c("here",
              "readr",
              "stringr", 
              "clock",
              "dplyr",
              "ggplot2",
              "rmarkdown",
              "knitr", 
              "magrittr",
              "glue",
              "xfun",
              "fs",
              "tidyr") 

installed_packages <- packages %in% rownames(installed.packages())

if (any(installed_packages == FALSE)) {
  install.packages(packages[!installed_packages])
}

library(ggplot2)
library(dplyr)
```

```{r}
# Basic Summary of the Data
crime_data  <- read.csv("bc_crime.csv")
summary(crime_data)
head(crime_data)
```

```{r}
# Creating a basic dataframe. 
crime_counts <- crime_data %>%
  filter(YEAR >= 2019) %>%
  group_by(YEAR, TYPE) %>%
  summarise(Count = n(), .groups = 'drop') %>% 
  arrange(YEAR, desc(Count))

print(crime_counts)
```

```{r}
# Creating a basic dataframe. 
crime_counts <- crime_data %>%
  filter(YEAR >= 2020) %>%
  group_by(YEAR, TYPE) %>%
  summarise(Count = n(), .groups = 'drop') %>% 
  arrange(YEAR, desc(Count))

print(crime_counts)
```

```{r}
# Creating a basic dataframe. 
crime_counts <- crime_data %>%
  filter(YEAR >= 2021) %>%
  group_by(YEAR, TYPE) %>%
  summarise(Count = n(), .groups = 'drop') %>% 
  arrange(YEAR, desc(Count))

print(crime_counts)
```

```{r}
homicide_count <- crime_data %>%
  filter(YEAR %in% c(2019, 2020, 2021, 2022, 2023) & TYPE == "Homicide") %>%
  group_by(YEAR) %>% 
  summarise(Count = n())

print(homicide_count)
```

```{r}
crime_data_selected_years <- crime_data %>%
  filter(YEAR %in% c(2020, 2021, 2022, 2023)) %>%
  count(YEAR)

ggplot(crime_data_selected_years, aes(x = YEAR, y = n, fill = as.factor(YEAR))) + 
  geom_bar(stat = "identity", width = 0.8) + 
  scale_fill_brewer(palette = "Blues") + 
  labs(title = "Crime Count per Year", x = "Year", y = "Count of Crimes") +
  theme_minimal()
```

```{r}
# Selecting for Homicides in Each Year Post Covid-19
homicide_data_years <- crime_data %>%
  filter(YEAR %in% c(2020, 2021, 2022, 2023) & TYPE == "Homicide") %>%
  count(YEAR)

# Creating the Bar Chart
ggplot(homicide_data_years, aes(x = YEAR, y = n, fill = as.factor(YEAR))) +
  geom_bar(stat = "identity", width = 0.8) + 
  scale_fill_brewer(palette = "Blues") +
  labs(title = "Homicide Count per Year", x = "Year", y = "Count of Homicides") +
  theme_minimal()
```

```{r}
# Filter and aggregate data for 2018 excluding Central Business District.
crime_data_2018_total <- crime_data %>%
  filter(YEAR == 2018, NEIGHBOURHOOD != "Central Business District") %>%
  count(NEIGHBOURHOOD)

# Create a colorful bar chart for 2018
ggplot(crime_data_2018_total, aes(x = NEIGHBOURHOOD, y = n, fill = NEIGHBOURHOOD)) +
  geom_bar(stat = "identity") +
  labs(title = "Total Crimes by Neighbourhood in 2019", x = "Neighbourhood", y = "Total Crimes") +
  theme_minimal() +
  theme(legend.key.size = unit(0.1, "cm"),
        axis.text.x = element_text(angle = 90, hjust = 1)) +
  scale_fill_viridis_d()
```

```{r}
# Filter and aggregate data for 2019 excluding Central Business District.
crime_data_2019_total <- crime_data %>%
  filter(YEAR == 2019, NEIGHBOURHOOD != "Central Business District") %>%
  count(NEIGHBOURHOOD)

# Create a colorful bar chart for 2019
ggplot(crime_data_2019_total, aes(x = NEIGHBOURHOOD, y = n, fill = NEIGHBOURHOOD)) +
  geom_bar(stat = "identity") +
  labs(title = "Total Crimes by Neighbourhood in 2019", x = "Neighbourhood", y = "Total Crimes") +
  theme_minimal() +
  theme(legend.key.size = unit(0.1, "cm"),
        axis.text.x = element_text(angle = 90, hjust = 1)) +
  scale_fill_viridis_d()
```

```{r}
# Filter and aggregate data for 2023 excluding Central Business District.
crime_data_2023_total <- crime_data %>%
  filter(YEAR == 2023, NEIGHBOURHOOD != "Central Business District") %>%
  count(NEIGHBOURHOOD)

# Create a colorful bar chart for 2023
ggplot(crime_data_2023_total, aes(x = NEIGHBOURHOOD, y = n, fill = NEIGHBOURHOOD)) +
  geom_bar(stat = "identity") +
  labs(title = "Crime by Area 23", x = "Neighbourhood", y = "Total Crimes Committed") +
  theme_minimal() +
  theme(legend.key.size = unit(0.1, "cm"),
        axis.text.x = element_text(angle = 90, hjust = 1)) +
  scale_fill_viridis_d()
```