#Excercise
#Checking the table called Track 
# Setting up the db connection 

import sqlite3
import pandas as pd

conn = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')

# Test 1 — confirm connection works
print("Connected!")

# Test 2 — confirm Track table exists
df_tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(df_tables)

# Test 3 — see Track structure
df_info = pd.read_sql("PRAGMA table_info(Track);", conn)
print(df_info)

df_info_1 = pd.read_sql("PRAGMA table_info(invoices);", conn)
print(df_info_1)

# -- Q1 (Easy, 10 min)
#-- Top 10 tracks by total revenue.
#-- Expected columns: TrackId, Name, total_revenue
#-- Sort: total_revenue DESC

q1 = """
SELECT 
    t.TrackId,
    t.Name,
    (SUM(ii.UnitPrice * ii.Quantity)) AS total_revenue
FROM invoice_items ii
JOIN tracks t ON ii.TrackId = t.TrackId
GROUP BY t.TrackId
ORDER BY total_revenue DESC
LIMIT 10;
"""

df1 = pd.read_sql_query(q1,conn)
print ("\n========== Q1: Top 10 Tracks by Revenue==========")
print (df1)


#-- Q2 (Easy-Medium, 15 min)
#-- Country-level KPIs: customers, invoices, revenue.
#-- Expected columns: Country, customer_count, invoice_count, total_revenue, avg_revenue_per_customer
#-- Sort: total_revenue DESC

df_info_2 = pd.read_sql("PRAGMA table_info(customers);", conn)
print(df_info_2)

df_info_3 = pd.read_sql("PRAGMA table_info(invoices);", conn)
print(df_info_3)

q2 = """
SELECT 
  c.CustomerId,
  c.Country,
  COUNT(DISTINCT c.CustomerId) AS customer_count ,
  COUNT(DISTINCT i.InvoiceId) AS  invoice_count,
  SUM(i.Total) AS total_revenue,
  (SUM(i.Total) / COUNT(DISTINCT c.CustomerId)) AS avg_revenue_per_customer
FROM customers c
JOIN invoices i ON c.CustomerId = i.CustomerId
GROUP BY c.Country
ORDER BY total_revenue DESC;
  """

df2 = pd.read_sql_query(q2,conn)
print ("\n========== Q2: Country-level KPIs==========")
print (df2)


#-- Q3 (Medium, 20 min)
#-- Monthly revenue with running total and 3-month moving average.
#-- Expected columns: month, revenue, running_revenue, moving_avg_3m
#-- Sort: month ASC

q3 = """
WITH monthly_revenue AS (
    SELECT
        strftime('%Y-%m', InvoiceDate) AS month,
        SUM(Total) AS revenue
    FROM invoices
    GROUP BY month
)
SELECT
    month,
    revenue,
    SUM(revenue) OVER (ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_revenue,
    ROUND(AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3m
FROM monthly_revenue
ORDER BY month ASC;
"""

df3 = pd.read_sql_query(q3, conn)
print("\n========== Q3: Monthly Revenue with Running Total and Moving Average ==========")
print(df3)


#-- Q4 (Medium, 20 min)
#-- For each genre, return top 2 customers by spend.
#-- Expected columns: GenreId, GenreName, CustomerId, CustomerName, genre_spend, rn
#-- Sort: GenreName ASC, rn ASC

# See the genre table structure
df_info_4 = pd.read_sql("PRAGMA table_info(genres);",conn)
print(df_info_4)

q4 = """
WITH genre_customer_spend AS (
    SELECT
        g.GenreId,
        g.Name AS GenreName,
        c.CustomerId,
        c.FirstName || ' ' || c.LastName AS CustomerName,
        ROUND(SUM(il.UnitPrice * il.Quantity), 2) AS genre_spend
    FROM invoice_items il
JOIN invoices i
    ON il.InvoiceId = i.InvoiceId
JOIN customers c
    ON i.CustomerId = c.CustomerId
JOIN tracks t
    ON il.TrackId = t.TrackId
JOIN genres g
    ON t.GenreId = g.GenreId
    GROUP BY g.GenreId, g.Name, c.CustomerId, CustomerName
), ranked AS (
    SELECT
        GenreId,
        GenreName,
        CustomerId,
        CustomerName,
        genre_spend,
        ROW_NUMBER() OVER (
            PARTITION BY GenreId
            ORDER BY genre_spend DESC, CustomerId ASC
        ) AS rn
    FROM genre_customer_spend
)
SELECT
    GenreId,
    GenreName,
    CustomerId,
    CustomerName,
    genre_spend,
    rn
FROM ranked
WHERE rn <= 2
ORDER BY GenreName, rn;

"""
df4 = pd.read_sql_query(q4, conn)
print("\n========== Q4: Top 2 Customers by Genre ==========")
print(df4)


#-- Q5 (Hard, 25 min)
#-- Customer retention proxy:
#-- Mark each invoice as NEW if first invoice month for that customer, else RETURNING.
#-- Then aggregate by month and customer_type.
#-- Expected columns: month, customer_type, customer_count, revenue
#-- Sort: month ASC, customer_type ASC

q5="""
WITH invoice_months AS (
    SELECT
        i.InvoiceId,
        i.CustomerId,
        strftime('%Y-%m', i.InvoiceDate) AS month,
        i.Total,
        MIN(strftime('%Y-%m', i.InvoiceDate)) OVER (
            PARTITION BY i.CustomerId
        ) AS first_month
    FROM invoices i
), typed AS (
    SELECT
        month,
        CustomerId,
        Total,
        CASE
            WHEN month = first_month THEN 'NEW'
            ELSE 'RETURNING'
        END AS customer_type
    FROM invoice_months
)
SELECT
    month,
    customer_type,
    COUNT(DISTINCT CustomerId) AS customer_count,
    ROUND(SUM(Total), 2) AS revenue
FROM typed
GROUP BY month, customer_type
ORDER BY month, customer_type;
"""
df5 = pd.read_sql_query(q5, conn)
print("\n========== Q5: Customer Retention Proxy ==========")
print(df5)
    