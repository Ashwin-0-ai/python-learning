-- Day 36: Cloud Warehouse Foundations (Question Sheet Only)
-- Timebox: 120 minutes total
-- Mode: No answer key today. You write every query from scratch.
-- Data source: chinook.db

-- ==================================================
-- Study First (Required)
-- ==================================================
-- Read: 36_pre_study_material.md (30-40 min max)
-- Start timed block only after finishing the Start Rule section.

-- ==================================================
-- Session Outcome (today)
-- ==================================================
-- 1) You can explain OLTP vs OLAP in practical terms.
-- 2) You can draft a simple star schema for analytics.
-- 3) You can build staging -> dimensions -> fact using SQL.
-- 4) You can run sanity checks on the modeled output.


-- ==================================================
-- Block A (0-20 min): Architecture Notes (write in comments)
-- ==================================================
-- A1) In 3-5 lines, define OLTP and OLAP with one real example each.
OLTP (Online Transaction Processing) refers to systems that manage transactional data and support day-to-day operations. They are optimized for fast query processing and maintaining data integrity in multi-access environments. An example of an OLTP system is a retail point-of-sale system that records customer purchases in real-time.
-- A2) Why star schema for BI dashboards? List 3 reasons.
1. Simplicity: Star schemas are straightforward and easy to understand, making it easier for analysts and business users to navigate the data and create reports without needing complex SQL knowledge.
2. Performance: Star schemas are optimized for query performance, especially in OLAP systems, as    
they allow for efficient querying and aggregation of data, which is essential for BI dashboards that require fast response times.
3. Scalability: Star schemas can handle large volumes of data and can be easily extended by adding new dimensions or facts without affecting existing queries, making them ideal for evolving business needs and growing datasets in BI environments.

-- A3) Identify grain for the fact table you will build today.
The grain for the fact table I will build today is at the invoice line level, meaning that each record in the fact table will represent a single line item from an invoice, including details such as the quantity, unit price, and gross amount for each track sold to a customer on a specific date.
-- A4) Write one sentence each for: dimension table, fact table, surrogate key.
A dimension table is a structure that categorizes and describes data in a fact table, providing context for analysis (e.g., customer, date, product). A fact table is a central table in a star schema that contains quantitative data for analysis, typically including foreign keys to dimension tables and measures (e.g., sales amount). A surrogate key is an artificial identifier used in dimension tables to uniquely identify each record, often implemented as an auto-incrementing integer, which helps maintain data integrity and simplifies joins with fact tables.


-- ==================================================
-- Block B (20-80 min): Modeling SQL Practice (timed)
-- ==================================================
-- Rule: Use CREATE TABLE ... AS SELECT for your training models.
-- Prefix all tables with training_ to keep them separate.

-- Q1 (10 min)
-- Create a date dimension from invoice dates.
-- Expected columns:
--   date_key (YYYYMMDD integer), calendar_date, year, month, month_name, quarter
-- Table name: training_dim_date

-- TODO:import sqlite3
import pandas as pd

conn = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS training_dim_date")
conn.commit()

cursor.execute("""
CREATE TABLE training_dim_date AS
 SELECT DISTINCT
  CAST(strftime('%Y%m%d', InvoiceDate) AS INTEGER) AS date_key,
  date(InvoiceDate)                                AS calendar_date,
  CAST(strftime('%Y', InvoiceDate) AS INTEGER)     AS year,
  CAST(strftime('%m', InvoiceDate) AS INTEGER)     AS month,
  strftime('%m', InvoiceDate)                      AS month_name,
 CASE
    WHEN CAST(strftime('%m',InvoiceDate) AS INTEGER) <=3 THEN 1
    WHEN CAST(strftime('%m',InvoiceDate) AS INTEGER) <=6 THEN 2 
    WHEN CAST(strftime('%m',InvoiceDate) AS INTEGER) <=9 THEN 3
    ELSE 4
    END AS quarter
    FROM invoices
        
""")
conn.commit()

df2 = pd.read_sql_query("SELECT * FROM training_dim_date LIMIT 5 ", conn)
print("\n ============ training_dim_date===========")
print(df2)


-- Q2 (10 min)
-- Create a customer dimension from customers.
-- Expected columns:
--   customer_key, customer_id, full_name, country, city, company
-- Table name: training_dim_customer

-- TODO: Write your SQL here
df = pd.read_sql_query("PRAGMA table_info(customers)", conn)
print(df)

cursor.execute("DROP TABLE IF EXISTS training_dim_customer")
conn.commit()

cursor.execute("""
    CREATE TABLE training_dim_customer AS 
        SELECT
            CustomerId AS customer_key,
            CustomerId AS customer_id,
               FirstName || ' ' || LastName AS full_name,
               Country AS country,
                City AS city,
                Company AS company
        FROM customers
               """)

df3 = pd.read_sql_query("SELECT * FROM training_dim_customer LIMIT 5 ", conn)
print("\n ============ training_dim_customer===========")
print(df3)


-- Q3 (15 min)
-- Create a track/product dimension by joining tracks + albums + artists + genres + media_types.
-- Expected columns:
--   track_key, track_id, track_name, album_title, artist_name, genre_name, media_type_name, unit_price
-- Table name: training_dim_track

-- TODO: Write your SQL here
cursor.execute("DROP TABLE IF EXISTS training_dim_track")
conn.commit()

cursor.execute("""
               CREATE TABLE training_dim_track AS 
               SELECT 
               t.TrackId             AS track_key,
               t.TrackId             AS track_id,
               t.Name                AS track_name,
               al.Title              AS album_title,
               ar.Name               AS artist_name,
               g.Name                AS genre_name,
               mt.Name               AS media_type_name,
               t.UnitPrice           AS unit_price
               FROM tracks t 
               JOIN albums al on t.AlbumID = al.AlbumId
               JOIN artists ar on al.ArtistId = ar.ArtistId
               JOIN genres g on t.GenreId = g.genreId
               JOIN media_types mt on t.MediaTypeId = mt.MediaTypeId 
               """)
df4 = pd.read_sql_query("SELECT * FROM training_dim_track LIMIT 5 ", conn) 
print("\n=============training_dim_track================")
print(df4)


-- Q4 (20 min)
-- Create a sales fact table at invoice line grain.
-- Expected columns:
--   sales_key, invoice_line_id, invoice_id, customer_id, track_id, date_key,
--   quantity, unit_price, gross_amount
-- Table name: training_fct_sales
-- Note: gross_amount = quantity * unit_price

-- TODO: Write your SQL here
cursor.execute("DROP TABLE IF EXISTS training_fct_sales")
conn.commit()

cursor.execute("""
CREATE TABLE training_fct_sales AS
SELECT
    ii.InvoiceLineId                                    AS sales_key,
    ii.InvoiceLineId                                    AS invoice_line_id,
    ii.InvoiceId                                        AS invoice_id,
    i.CustomerId                                        AS customer_id,
    ii.TrackId                                          AS track_id,
    CAST(strftime('%Y%m%d', i.InvoiceDate) AS INTEGER)  AS date_key,
    ii.Quantity                                         AS quantity,
    ii.UnitPrice                                        AS unit_price,
    ROUND(ii.Quantity * ii.UnitPrice, 2)                AS gross_amount
FROM invoice_items ii
JOIN invoices i ON ii.InvoiceId = i.InvoiceId
""")
conn.commit()

# Step 2: View result
df_fct = pd.read_sql_query("SELECT * FROM training_fct_sales LIMIT 5", conn)
print("\n=========== training_fct_sales ===========")
print(df_fct)



-- Q5 (15 min)
-- Write 3 validation queries:
-- V1) Row count of training_fct_sales
-- V2) Sum(gross_amount) vs original invoice_items total (should be very close)
-- V3) Distinct customer_id in fact vs customers table

-- TODO: Write your SQL here
# V1: Row count
v1 = pd.read_sql_query("SELECT COUNT(*) AS total_rows FROM training_fct_sales", conn)
print("V1 - Row Count:")
print(v1)

# V2: Revenue reconciliation
v2 = pd.read_sql_query("""
SELECT
    ROUND((SELECT SUM(gross_amount)  FROM training_fct_sales), 2) AS fact_revenue,
    ROUND((SELECT SUM(UnitPrice * Quantity) FROM invoice_items), 2) AS raw_revenue
""", conn)
print("\nV2 - Revenue Reconciliation:")
print(v2)
print("Match?", v2['fact_revenue'][0] == v2['raw_revenue'][0])

# V3: Customer coverage
v3 = pd.read_sql_query("""
SELECT
    (SELECT COUNT(DISTINCT customer_id) FROM training_fct_sales) AS fact_customers,
    (SELECT COUNT(DISTINCT CustomerId)  FROM customers)          AS source_customers
""", conn)
print("\nV3 - Customer Coverage:")
print(v3)


-- ==================================================
-- Block C (80-110 min): Analysis Checks (write query + short note)
-- ==================================================
-- C1) Top 10 countries by gross_amount from your fact model.
-- C2) Top 5 genres by gross_amount.
-- C3) Monthly revenue trend using date dimension.

c1 = pd.read_sql_query("""
SELECT
    dc.country,
    ROUND(SUM(fs.gross_amount), 2) AS total_revenue
FROM training_fct_sales fs
JOIN training_dim_customer dc ON fs.customer_id = dc.customer_id
GROUP BY dc.country
ORDER BY total_revenue DESC
LIMIT 10
""", conn)
print("C1 - Top 10 Countries by Revenue:")
print(c1)

c2 = pd.read_sql_query(""" 
                       SELECT 
                       dt.genre_name,
                       ROUND(SUM(fs.gross_amount),2) AS total_revenue
                       FROM training_fct_sales fs 
                       JOIN training_dim_track dt ON fs.track_id = dt.track_id
                       GROUP BY dt.genre_name
                       ORDER BY total_revenue DESC
                       LIMIT 5
                       """,conn)

print("\nC2 - Top 5 Genres by Revenue:")
print(c2)


c3 = pd.read_sql_query("""
SELECT
    dd.year,
    dd.month,
    ROUND(SUM(fs.gross_amount), 2) AS monthly_revenue
FROM training_fct_sales fs
JOIN training_dim_date dd ON fs.date_key = dd.date_key
GROUP BY dd.year, dd.month
ORDER BY dd.year, dd.month
""", conn)
print("\nC3 - Monthly Revenue Trend:")
print(c3)



-- ==================================================
-- Block D (110-120 min): Commit Notes
-- ==================================================
-- D1) What broke first? (naming, joins, grain, or date_key)
-- D2) What did you fix?
-- D3) One thing to improve on Day 37.


-- ==================================================
-- End-Of-Session Recap Questionnaire (Previous Day: Day 35)
-- ==================================================
-- Answer without opening Day 35 answer key.
-- 1) When do you prefer ROW_NUMBER over RANK?
ROW_NUMBER is preferred when you want to assign a unique sequential integer to rows within a partition of a result set, regardless of duplicates. RANK, on the other hand, assigns the same rank to identical values and skips subsequent ranks, which can lead to gaps in the ranking sequence. Therefore, if you need a distinct order without ties, ROW_NUMBER is the better choice.
-- 2) In one sentence, what does a 3-row moving average smooth out?
A 3-row moving average smooths out short-term fluctuations in data by averaging each data point with its two immediate neighbors, providing a clearer view of the underlying trend.
-- 3) Why use NULLIF in division expressions?
NULLIF is used in division expressions to prevent division by zero errors. It returns NULL if the second argument is zero, allowing the entire expression to return NULL instead of causing an error, which can be handled gracefully in SQL queries.
-- 4) How do you define query grain before writing joins?
To define query grain before writing joins, you first identify the level of detail you want in your final output (e.g., customer-level, transaction-level, daily-level) and then determine which tables and columns are necessary to achieve that level of detail. This helps ensure that your joins are structured correctly to produce the desired granularity in your results.
-- 5) Write the exact order of clauses in a typical SQL query.
The typical order of clauses in a SQL query is:
1. SELECT
2. FROM
3. JOIN (if applicable)
4. WHERE
5. GROUP BY (if applicable)
6. HAVING (if applicable)
7. ORDER BY (if applicable)
8. LIMIT (if applicable)

-- 6) Give one example where LEFT JOIN is safer than INNER JOIN for KPI reporting.
LEFT JOIN is safer than INNER JOIN for KPI reporting when you want to include all records from the left table, even if there are no matching records in the right table. For example, if you're reporting on total sales by customer and some customers have not made any purchases, using a LEFT JOIN will ensure that those customers are still included in the report with a sales total of zero, whereas an INNER JOIN would exclude them entirely, potentially skewing the analysis.

-- 7) What is one mistake you made in Day 35 and how will you avoid it?
One mistake I made in Day 35 was not clearly defining the grain of my fact table before starting to write the SQL queries, which led to confusion and multiple revisions. To avoid this in the future, I will take a moment at the beginning of the modeling process to explicitly state the grain of the fact table and ensure that all subsequent joins and aggregations align with that defined grain.
-- 8) Score your Day 35 confidence (1-10) for interview speed under time pressure.  
I would score my Day 35 confidence as a 6 for interview speed under time pressure. While I was able to complete the tasks, I found myself second-guessing some of my decisions and had to make several adjustments along the way, which slowed me down. With more practice and a clearer initial plan, I believe I can improve my speed and efficiency in future sessions.



-- ==================================================
-- Self-Scoring
-- ==================================================
-- [5] Finished all blocks within 120 min
-- [10] Built at least 3 training_* tables
-- [8] Ran all 3 validation checks
-- [8] Completed previous-day recap questionnaire
