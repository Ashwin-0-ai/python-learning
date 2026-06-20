{{ config( 
    schema='ANALYTICS',
    )}}

WITH fuel_history AS (
    SELECT * FROM {{ ref('stg_fuel_history')}}
),
exchange_rates AS (
    SELECT * FROM {{ ref('stg_exchange_rates')}}
)
     SELECT 
          f.year AS year,
          f.month AS month,
          f.petrol_price_inr AS petrol_price_inr,
          f.diesel_price_inr AS diesel_price_inr,
          f.crude_oil_prices_usd AS crude_oil_prices_usd,
          f.inr_per_usd AS inr_per_usd,
            f.event_description AS event_description,
            f.event_flag AS event_flag,
            f.usd_inr_exchange_rate AS usd_inr_exchange_rate,
            e.inr_per_gbp AS inr_per_gbp,
            e.inr_per_aed AS inr_per_aed,
            CURRENT_TIMESTAMP()::TIMESTAMP_NTZ AS loaded_at 
        FROM fuel_history f
        LEFT JOIN exchange_rates e
        ON f.year = e.year  
