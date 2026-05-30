USE WAREHOUSE BLITZKREIG_WH;
USE DATABASE MISSION_BLITZKREIG;
USE SCHEMA RAW;

CREATE OR REPLACE STAGE german_population_stage
  COMMENT = 'Stage for loading German State Population data';

  --block 1 : creating the table :
USE WAREHOUSE BLITZKREIG_WH;
USE DATABASE MISSION_BLITZKREIG;
USE SCHEMA RAW;

CREATE OR REPLACE TABLE RAW.GERMAN_STATE_POPULATION( 
    state_name           VARCHAR,
    area_km2             FLOAT,
    population_total     NUMBER,
    population_male      NUMBER,
    population_female    NUMBER,
    population_density   FLOAT
);

  --block 2: load from stage into the table created above 
  COPY INTO RAW.GERMAN_STATE_POPULATION
  FROM @german_population_stage/02-bundeslaender.csv
  FILE_FORMAT = (
             TYPE = 'CSV'
             FIELD_OPTIONALLY_ENCLOSED_BY = '"'
             SKIP_HEADER = 1 
  );

    --Verify the uploaded data 
    SELECT * FROM RAW.GERMAN_STATE_POPULATION;

    --Calculates population density yourself and compares it to the official figure from Destatis.
    SELECT 
           STATE_NAME,
           AREA_KM2,
           POPULATION_TOTAL,
           ROUND(POPULATION_TOTAL/AREA_KM2,1) AS MY_DENSITY_CHECK,
           POPULATION_DENSITY
    FROM RAW.GERMAN_STATE_POPULATION
    ORDER BY POPULATION_TOTAL DESC;
    
           