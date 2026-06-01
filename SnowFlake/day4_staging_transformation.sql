-- Day 4: RAW to STAGING Transformation
-- Cleans types, trims state names, adds pct_female and loaded_at

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE BLITZKREIG_WH;
USE DATABASE MISSION_BLITZKREIG;
USE SCHEMA STAGING;

-- Preview before creating table
SELECT
    TRIM(state_name)                                                    AS state_name,
    CAST(area_km2 AS DECIMAL(10,2))                                     AS area_km2,
    CAST(population_total AS BIGINT)                                    AS population_total,
    CAST(population_male AS BIGINT)                                     AS population_male,
    CAST(population_female AS BIGINT)                                   AS population_female,
    CAST(population_density AS DECIMAL(10,2))                           AS population_density,
    ROUND((population_female::FLOAT / population_total::FLOAT)*100, 2)  AS pct_female,
    CURRENT_TIMESTAMP()::TIMESTAMP_NTZ                                  AS loaded_at
FROM MISSION_BLITZKREIG.RAW.GERMAN_STATE_POPULATION
ORDER BY population_density DESC;

-- Create STAGING table with correct data
CREATE OR REPLACE TABLE STAGING.GERMAN_STATE_POPULATION AS
SELECT
    TRIM(state_name)                                                    AS state_name,
    CAST(area_km2 AS DECIMAL(10,2))                                     AS area_km2,
    CAST(population_total AS BIGINT)                                    AS population_total,
    CAST(population_male AS BIGINT)                                     AS population_male,
    CAST(population_female AS BIGINT)                                   AS population_female,
    CAST(population_density AS DECIMAL(10,2))                           AS population_density,
    ROUND((population_female::FLOAT / population_total::FLOAT)*100, 2)  AS pct_female,
    CURRENT_TIMESTAMP()::TIMESTAMP_NTZ                                  AS loaded_at
FROM MISSION_BLITZKREIG.RAW.GERMAN_STATE_POPULATION;

-- Verify
SELECT state_name, population_total, population_density, pct_female
FROM STAGING.GERMAN_STATE_POPULATION
ORDER BY population_density DESC;