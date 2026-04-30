# Build 4 queries in Chinook
#Query 2: Monthly revenue with next month (LEAD) forecast view.
#Query 3: Running total of revenue over time.
#Query 4: 3-month moving average of revenue.

#Query 1: Monthly revenue with previous month (LAG) and month-over-month change.
import sqlite3 
import pandas as pd 

conn = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')
cursor = conn.cursor()

query =""" 
WITH monthly AS (
    SELECT 
        strftime('%Y-%m', InvoiceDate) AS Month,
        SUM(Total) AS Revenue
    FROM invoices 
    GROUP BY Month
    ORDER BY Month
)
SELECT
Month,
Revenue,
LAG(Revenue,1) OVER (ORDER BY Month) AS previous_month_revenue,
ROUND(Revenue - LAG(Revenue,1) OVER (ORDER BY Month),2) AS month_over_month_change,
ROUND(100 * (Revenue - LAG(Revenue,1) OVER (ORDER BY Month)) / LAG(Revenue,1) OVER (ORDER BY Month),1) AS month_over_month_pct_change 
FROM monthly;
"""

df1 = pd.read_sql_query(query,conn)
print("\n Monthly Revenue With Previous month and month-over-month change:")
print(df1)

#Query 2: Monthly revenue with next month (LEAD) forecast view.
query2 = """
WITH MONTHLY AS (
SELECT 
    strftime('%Y-%m', InvoiceDate) AS Month,
    SUM(Total) AS REVENUE
    FROM invoices 
    GROUP BY Month
    ORDER BY Month
)
SELECT 
Month,
Revenue,
LEAD(Revenue,1) OVER (ORDER BY Month) AS next_month_revenue_forecast
FROM monthly;
"""

df2 = pd.read_sql_query(query2,conn)
print("\n Monthly Revenue with next month forecast:")
print(df2)

# Q3: Running total of revenue over time
query3 = """
WITH MONTHLY AS (
SELECT 
      strftime('%Y-%m', InvoiceDate) AS Month,
      SUM(Total) AS REVENUE
      FROM invoices 
        GROUP BY Month
        ORDER BY Month
)
SELECT
       Month,
       Revenue,
       ROUND(SUM(Revenue) OVER (ORDER BY Month),2) AS running_total_revenue
FROM monthly;
"""
df3 = pd.read_sql_query(query3,conn)
print("\n Running total of revenue over time:")
print(df3)

# Q4: 3-month moving average
query4 = """
WITH MONTHLY AS(
SELECT
      strftime('%Y-%m', InvoiceDate ) AS Month,
      SUM(Total) AS REVENUE
      FROM invoices 
      GROUP BY Month
      ORDER BY Month
      )

      SELECT 
        Month,
        REVENUE,
        ROUND(AVG(Revenue) OVER (ORDER BY Month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2) AS moving_avg_3_months
    FROM monthly;
      """

df4 = pd.read_sql_query(query4,conn)
print("\n 3-month moving average of revenue:")  
print(df4)
