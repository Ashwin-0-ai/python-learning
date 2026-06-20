WITH sources AS (

SELECT * FROM {{ ref('india_fuel_history_1947_2026')}}
),
  STAGED AS (
           SELECT
                CAST (year AS INTEGER)                        AS year,  
                CAST (month AS INTEGER)                       AS month,
                CAST (petrol_price_inr AS FLOAT)              AS petrol_price_inr,
                CAST (diesel_price_inr AS FLOAT)              AS diesel_price_inr,
                CAST (crude_oil_price_usd AS FLOAT)           AS crude_oil_prices_usd,
                TRIM (event_description)                      AS event_description,
                CAST (event_flag AS BOOLEAN)                  AS event_flag,
                CAST (usd_inr_exchange_rate AS FLOAT)          AS usd_inr_exchange_rate,
                CURRENT_TIMESTAMP()::TIMESTAMP_NTZ            AS loaded_at
        FROM sources
                 )
        SELECT * FROM staged