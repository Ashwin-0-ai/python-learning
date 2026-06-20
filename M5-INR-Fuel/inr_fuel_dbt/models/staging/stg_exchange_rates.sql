WITH sources AS (

    SELECT * FROM {{ref('india_inr_exchange_rates_wide')}}
),
    STAGED AS (
           SELECT 
                CAST (Year AS INTEGER)                      AS year, 
                CAST (INR_per_GBP AS FLOAT)                 AS inr_per_gbp,
                CAST (INR_per_AED AS FLOAT)                 AS inr_per_aed,
                CAST (INR_per_USD AS FLOAT)                 AS inr_per_usd,
                CURRENT_TIMESTAMP()::TIMESTAMP_NTZ           AS loaded_at
            FROM sources
)
SELECT * FROM staged 