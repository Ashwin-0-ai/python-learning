USE ROLE ACCOUNTADMIN;
USE WAREHOUSE BLITZKREIG_WH;
USE DATABASE MISSION_BLITZKREIG;
USE SCHEMA STAGING;

SELECT 
      state_name                               AS       state_name,
      
      CAST(population_total AS BIGINT)         AS       population_total, 
      
      CAST(population_female AS BIGINT)        AS       population_female,
      CAST(population_density AS DECIMAL(10,2))AS       population_density,
ROUND((population_female :: FLOAT / population_total:: FLOAT)*100,2)AS pct_female,
CASE 
    WHEN TRIM(state_name) IN (
        'Brandenburg',
        'Mecklenburg-Vorpommern',
        'Sachsen',
        'Sachsen-Anhalt',
        'Thüringen',
        'Berlin'
    ) THEN 'East'
    ELSE 'West'
END AS region

FROM MISSION_BLITZKREIG.STAGING.GERMAN_STATE_POPULATION
ORDER BY population_density DESC

--CREATE TABLE 
USE WAREHOUSE BLITZKREIG_WH;
USE DATABASE MISSION_BLITZKREIG;
USE SCHEMA ANALYTICS;
CREATE OR REPLACE TABLE ANALYTICS.GERMAN_CONSULTANCY_FIRM (
   state_name            VARCHAR,
   population_density    DECIMAL (10,2),
   population_female     BIGINT,
   population_total      BIGINT,
   pct_female            DECIMAL(5,2),
   region              VARCHAR
);

--INSERT TABLE 
INSERT INTO ANALYTICS.GERMAN_CONSULTANCY_FIRM
  (state_name, population_total, population_female, population_density, pct_female, region)
SELECT 
                        state_name,
                       CAST(population_total          AS BIGINT),
                       CAST(population_female         AS BIGINT),
                       CAST(population_density        AS DECIMAL(10,2)),
                       ROUND((population_female::FLOAT / population_total::FLOAT) * 100,2),
CASE 

    WHEN TRIM(state_name) IN (

        'Brandenburg',
        'Mecklenburg-Vorpommern',
        'Sachsen',
        'Sachsen-Anhalt',
        'Thüringen',
        'Berlin'
 ) THEN 'East'
   ELSE 'West'
END AS region
FROM MISSION_BLITZKREIG.STAGING.GERMAN_STATE_POPULATION;

-- VERIFY  
SELECT * FROM ANALYTICS.GERMAN_CONSULTANCY_FIRM
ORDER BY population_density DESC;