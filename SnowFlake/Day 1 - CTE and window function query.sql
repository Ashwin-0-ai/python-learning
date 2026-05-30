-- Query: Top 5 customers by total spend per market segment
-- Database: Snowflake sample data (TPCH_SF1)
-- Uses a chained CTE to calculate total spend per customer,
-- then ROW_NUMBER() window function to rank customers within
-- each market segment. Final filter keeps only top 5 per segment.

-- Top 5 customers by total order value per market segment
WITH customer_spend AS (
    SELECT
        c.c_custkey,
        c.c_name,
        c.c_mktsegment,
        SUM(o.o_totalprice) AS total_spend
    FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER c
    JOIN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS o
        ON c.c_custkey = o.o_custkey
    GROUP BY 1, 2, 3
),
ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY c_mktsegment
            ORDER BY total_spend DESC
        ) AS rank_in_segment
    FROM customer_spend
)
SELECT *
FROM ranked
WHERE rank_in_segment <= 5
ORDER BY c_mktsegment, rank_in_segment;