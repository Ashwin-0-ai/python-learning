# German State Population Analysis — Snowflake Data Pipeline

## What This Project Does
End-to-end data pipeline built on Snowflake that loads, transforms 
and analyses official German state population data from Destatis (2022 Census).

## Business Questions Answered
- Which German states need urgent housing infrastructure? (population density)
- How does East Germany compare to West Germany demographically?
- What does the gender distribution look like across states for 
  political campaign targeting?

## Pipeline Architecture
Destatis Excel → Python (Pandas clean) → CSV → Snowflake Stage→ COPY INTO RAW → STAGING (typed, transformed) → ANALYTICS (business layer)

## Tech Stack
- **Snowflake** — cloud data warehouse (Azure region)
- **Python / Pandas** — data cleaning and preparation
- **SQL** — transformation and analysis
- **Snowflake Features Used** — Internal Stages, COPY INTO, 
  Time Travel, Streams, Tasks

## Key Findings
- Berlin is the most densely populated state (4,136 people/km²)
- East German states average significantly lower population density than West
- Female population is consistent across all states (50.4% — 51.1%)

## Project Structure
SnowFlake/
├── data/ # Source data files
├── day3_load_data.sql # Stage creation and COPY INTO
├── day4_staging_transformation.sql # RAW to STAGING transformation
├── day5_analytics_layer.sql # ANALYTICS layer with East/West region
├── day6_time_travel_streams_tasks.sql # Time Travel, Streams, Tasks
└── day_3_prepare_bundeslaender.py # Python data cleaning script

## Data Source
Statistisches Bundesamt (Destatis) — [destatis.de](https://www.destatis.de)
Official German Federal Statistical Office, 2022 Census data