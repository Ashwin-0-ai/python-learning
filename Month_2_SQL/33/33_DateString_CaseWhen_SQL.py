#Exercise 1: Extract year, month, quarter, day-of-week from invoice dates.
#Exercise 2: Revenue by quarter across all years.
#Exercise 3: Bucket customers by spend tier using CASE WHEN.
#Exercise 4: Clean and standardise country names with string functions.
#Exercise 5: Combined — spend tier + quarter in one query.

import sqlite3 
import pandas as pd 

conn = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')
cursor = conn.cursor()

# Exercise 1: Extract year, month, quarter, day-of-week from invoice dates.
print("=== Exercise 1: Extract date parts ===")
query = """ 
SELECT 
    InvoiceDate,
    strftime('%Y', InvoiceDate) AS Year,
    strftime('%m',InvoiceDate) AS Month,
    strftime('%d', InvoiceDate) AS Day,
    CASE strftime('%m', InvoiceDate)
        WHEN '01' THEN 'Q1' WHEN '02' THEN 'Q1' WHEN '03' THEN 'Q1'
        WHEN '04' THEN 'Q2' WHEN '05' THEN 'Q2' WHEN '06' THEN 'Q2'         
        WHEN '07' THEN 'Q3' WHEN '08' THEN 'Q3' WHEN '09' THEN 'Q3'
        ELSE 'Q4'
END AS Quarter, 

    CASE strftime('%w', InvoiceDate) 
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        ELSE 'Saturday' 
    END AS DayOfWeek
FROM invoices
LIMIT 15;
"""

df1 = pd.read_sql_query(query,conn)
print(df1)


#Exercise 2: Revenue by quarter across all years.
print("\n===Exercise 2 : Revenue by quarter across all years===")

query2 = """
SELECT 
    strftime('%Y', InvoiceDate) AS year, 
    CASE strftime('%m', InvoiceDate)
        WHEN '01' THEN 'Q1' WHEN '02' THEN 'Q1' WHEN '03' THEN 'Q1'
        WHEN '04' THEN 'Q2' WHEN '05' THEN 'Q2' WHEN '06' THEN 'Q2'         
        WHEN '07' THEN 'Q3' WHEN '08' THEN 'Q3' WHEN '09' THEN 'Q3'
        ELSE 'Q4'
    END AS quarter,
    SUM(Total) AS revenue
FROM invoices
GROUP BY year, quarter
ORDER BY year, quarter;
"""

df2 = pd.read_sql_query(query2,conn)
print("\nRevenue by quarter across all years:")
print(df2)

# Exercise 3: Customer spend tiers using CASE WHEN
print("\n === Exercise 3: Customer spend tiers ===")

query3 = """ 
WITH customer_spend AS (
SELECT 
    c.FirstName ||' '|| c.LastName AS CustomerName,
    c.CustomerId,
    SUM(i.Total) AS Total_Spent
FROM customers c
JOIN invoices i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId,CustomerName
)
SELECT 
      *,
      CASE 
        WHEN Total_Spent >= 45 THEN 'Platinum'
        WHEN Total_Spent >= 35 THEN 'Gold'
        WHEN Total_Spent >= 25 THEN 'Silver'
        ELSE 'Bronze'
    END AS spend_tier
FROM customer_spend
ORDER BY Total_Spent DESC;
"""

df3 = pd.read_sql_query(query3,conn)
print("\nCustomer spend tiers:")
print(df3)


# Exercise 4: String functions — clean + standardise
print("\n=== Exercise 4: Clean and standardise country names ===")
query4 = """
SELECT DISTINCT
    Country                            AS            original,
    UPPER(Country)                     AS            uppercase,
    LOWER(Country)                     AS            lowercase,
    LENGTH(Country)                    AS            characterCount,
    SUBSTR(Country,1 ,3 )              AS            code_prefix,
    REPLACE(Country, 'United', 'U')    AS            shortened
FROM customers
ORDER BY Country;
"""

df4 = pd.read_sql_query(query4,conn)
print("\nCleaned and standardised country names:")
print(df4)

# Exercise 5: Combined — spend tier + best quarter per customer

q5 = """
WITH customer_quarterly AS (
    SELECT
        c.CustomerId,
        c.FirstName,
        c.LastName,
        CASE strftime('%m', i.InvoiceDate)
            WHEN '01' THEN 'Q1' WHEN '02' THEN 'Q1' WHEN '03' THEN 'Q1'
            WHEN '04' THEN 'Q2' WHEN '05' THEN 'Q2' WHEN '06' THEN 'Q2'
            WHEN '07' THEN 'Q3' WHEN '08' THEN 'Q3' WHEN '09' THEN 'Q3'
            ELSE 'Q4'
        END AS quarter,
        ROUND(SUM(i.Total), 2) AS quarterly_spend
    FROM customers c
    JOIN invoices i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId, c.FirstName, c.LastName, quarter
),
best_quarter AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY CustomerId ORDER BY quarterly_spend DESC) AS rn
    FROM customer_quarterly
),
total_spend AS (
    SELECT CustomerId, ROUND(SUM(Total), 2) AS total_spent
    FROM invoices
    GROUP BY CustomerId
)
SELECT
    bq.CustomerId,
    bq.FirstName,
    bq.LastName,
    bq.quarter        AS best_quarter,
    bq.quarterly_spend,
    ts.total_spent,
    CASE
        WHEN ts.total_spent >= 45 THEN 'Platinum'
        WHEN ts.total_spent >= 35 THEN 'Gold'
        WHEN ts.total_spent >= 25 THEN 'Silver'
        ELSE                           'Bronze'
    END AS spend_tier
FROM best_quarter bq
JOIN total_spend ts ON bq.CustomerId = ts.CustomerId
WHERE bq.rn = 1
ORDER BY ts.total_spent DESC;
"""
df5 = pd.read_sql_query(q5, conn)
print("\n=== Exercise 5: Spend Tier + Best Quarter Combined ===")
print(df5)

conn.close()