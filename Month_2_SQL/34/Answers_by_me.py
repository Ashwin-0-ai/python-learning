# Set up Database 
import sqlite3
import pandas as pd 

conn = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')
cursor = conn.cursor()

# Q1 (Easy): Count customers per country
q1 = """
SELECT Country,
COUNT(*) AS CustomerCount
FROM customers
GROUP BY COUNTRY
ORDER BY CustomerCount DESC
"""

df1 = pd.read_sql_query(q1,conn)
print ("\n========== Q1: Customers per Country==========")
print (df1)


#  Q2 (Easy): Top 5 customers by total spend
q2 ="""
SELECT 
    c.FirstName ||' '|| c.LastName AS CustomerName,
    SUM(i.Total) AS TotalSpend
FROM customers c
JOIN invoices i ON c.CustomerID = i.CustomerID
GROUP BY c.CustomerID
ORDER BY TotalSpend DESC
LIMIT 5;
"""

df2 = pd.read_sql_query(q2,conn)
print ("\n========== Q2: Top 5 Customers by Spend==========")
print (df2)

# Q3 (Medium): Top 3 customers per country using ROW_NUMBER

q3 = """
WITH customer_spend AS (
    SELECT
        c.Country,
        c.CustomerId,
        c.FirstName,
        c.LastName,
        ROUND(SUM(i.Total), 2) AS total_spent
    FROM customers c
    JOIN invoices i
        ON c.CustomerId = i.CustomerId
    GROUP BY c.Country, c.CustomerId, c.FirstName, c.LastName
), ranked AS (
    SELECT
        Country,
        CustomerId,
        FirstName,
        LastName,
        total_spent,
        ROW_NUMBER() OVER (
            PARTITION BY Country
            ORDER BY total_spent DESC
        ) AS rn
    FROM customer_spend
)
SELECT
    Country,
    CustomerId,
    FirstName,
    LastName,
    total_spent,
    rn
FROM ranked
WHERE rn <= 3
ORDER BY Country, rn;
"""

df3 = pd.read_sql_query(q3,conn)
print("\n========== Q3: Top 3 Customers per Country==========")
print(df3)

#-- Q4 (Medium): Monthly revenue with LAG and MoM change
#-- Expected output columns: month, revenue, prev_month_revenue, mom_change, mom_pct_change
q4 = """
WITH monthly_revenue AS (
    SELECT 
        strftime('%Y-%m', InvoiceDate) AS month,
        ROUND(SUM(Total), 2) AS revenue
    FROM invoices
    GROUP BY month
)
SELECT 
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(
        revenue - LAG(revenue, 1) OVER (ORDER BY month),
        2
    ) AS mom_change,
    ROUND(
        100.0 * (revenue - LAG(revenue, 1) OVER (ORDER BY month))
        / NULLIF(LAG(revenue, 1) OVER (ORDER BY month), 0),
        2
    ) AS mom_pct_change
FROM monthly_revenue
ORDER BY month;
"""

df4 = pd.read_sql_query(q4, conn)
print("\n========== Q4: Monthly Revenue with MoM Change ==========")
print(df4)

#Q5 (Hard): Best quarter per customer + spend tier using CASE WHEN
# Expected output columns:CustomerId, FirstName, LastName, best_quarter, quarterly_spend, total_spent, spend_tier

q5 = """
WITH customer_quarterly AS (
    SELECT
        c.CustomerId,
        c.FirstName || ' ' || c.LastName AS customer_name,
        strftime('%Y', i.InvoiceDate) || '-Q' ||
            ((CAST(strftime('%m', i.InvoiceDate) AS INTEGER) - 1) / 3 + 1) AS quarter,
        ROUND(SUM(i.Total), 2) AS quarterly_spend
    FROM invoices i
    JOIN customers c ON i.CustomerId = c.CustomerId
    GROUP BY c.CustomerId, quarter
),
ranked AS (
    SELECT
        CustomerId,
        customer_name,
        quarter,
        quarterly_spend,
        RANK() OVER (PARTITION BY CustomerId ORDER BY quarterly_spend DESC) AS spend_rank
    FROM customer_quarterly
),
best_quarters AS (
    SELECT
        CustomerId,
        customer_name,
        quarter AS best_quarter,
        quarterly_spend AS best_quarter_spend
    FROM ranked
    WHERE spend_rank = 1
)
SELECT
    customer_name,
    best_quarter,
    best_quarter_spend,
    CASE
        WHEN best_quarter_spend >= 20 THEN 'High Spender'
        WHEN best_quarter_spend >= 10 THEN 'Mid Spender'
        ELSE 'Low Spender'
    END AS spend_tier
FROM best_quarters
ORDER BY best_quarter_spend DESC;
"""

df5 = pd.read_sql_query(q5, conn)
print("\n========== Q5: Best Quarter per Customer + Spend Tier ==========")
print(df5)

conn.close()

