
#Block B (20-80 min): Modeling SQL Practice (timed)
#1. Create modeled tables:
#Create a date dimension from invoice dates.
#Expected columns:
#date_key (YYYYMMDD integer), calendar_date, year, month, month_name, quarter
#Table name: training_dim_date

import sqlite3
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

#Q2 (10 min)
#-- Create a customer dimension from customers.
#-- Expected columns:
#-- customer_key, customer_id, full_name, country, city, company
#-- Table name: training_dim_customer

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

#Q3 (15 min)
#-- Create a track/product dimension by joining tracks + albums + artists + genres + media_types.
#-- Expected columns:
#--   track_key, track_id, track_name, album_title, artist_name, genre_name, media_type_name, unit_price
#-- Table name: training_dim_track


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

#Q4 (20 min)
#-- Create a sales fact table at invoice line grain.
#-- Expected columns:
#--   sales_key, invoice_line_id, invoice_id, customer_id, track_id, date_key,
#--   quantity, unit_price, gross_amount
#-- Table name: training_fct_sales
#-- Note: gross_amount = quantity * unit_price
       
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


#- Q5 (15 min)
#-- Write 3 validation queries:
#-- V1) Row count of training_fct_sales
#-- V2) Sum(gross_amount) vs original invoice_items total (should be very close)
#-- V3) Distinct customer_id in fact vs customers table

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


#Block C (80-110 min): Analysis Checks (write query + short note)
#-- ==================================================
#-- C1) Top 10 countries by gross_amount from your fact model.
#-- C2) Top 5 genres by gross_amount.
#-- C3) Monthly revenue trend using date dimension.

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


