--Preparing Raw Data 

USE WAREHOUSE BLITZKREIG_WH;
USE DATABASE MISSION_BLITZKREIG;
USE SCHEMA STAGING;

SELECT 
      state_name                               AS       state_name,
      CAST(area_km2 AS DECIMAL(10,2))          AS       area_km2,
      CAST(population_total AS BIGINT)         AS       population_total, 
      CAST(population_male AS BIGINT)          AS       population_male,
      CAST(population_female AS BIGINT)        AS       population_female,
      CAST(population_density AS DECIMAL(10,2))AS       population_density,
      CURRENT_TIMESTAMP()                      AS       loaded_at,
      ROUND((population_female :: FLOAT / population_total :: FLOAT)*100,2) AS  pct_female
FROM MISSION_BLITZKREIG.RAW.GERMAN_STATE_POPULATION

-- Create table 
USE ROLE ACCOUNTADMIN;
USE WAREHOUSE BLITZKREIG_WH;
USE DATABASE MISSION_BLITZKREIG;
USE SCHEMA STAGING;
CREATE OR REPLACE TABLE STAGING.GERMAN_STATE_POPULATION ( 
    state_name            VARCHAR,
    area_km2              DECIMAL(10,2),
    population_density    DECIMAL (10,2),
    population_female     BIGINT, 
    population_male       BIGINT,
    population_total      BIGINT,
    pct_female            DECIMAL(5,2),
    loaded_at             TIMESTAMP_NTZ
);
-- Insert the above table 

INSERT INTO STAGING.GERMAN_STATE_POPULATION
SELECT 
         state_name,
         CAST(area_km2                  AS DECIMAL(10,2)),
         CAST(population_total          AS BIGINT),
         CAST(population_male           AS BIGINT),
         CAST(population_female         AS BIGINT),
         CAST(population_density        AS DECIMAL(10,2)),
         ROUND((population_female::FLOAT / population_total::FLOAT) * 100,2),
         CURRENT_TIMESTAMP()
FROM MISSION_BLITZKREIG.RAW.GERMAN_STATE_POPULATION;

SELECT * FROM STAGING.GERMAN_STATE_POPULATION;