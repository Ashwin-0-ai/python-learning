# Revision CTE and Window Function 
# Before we start woking on snowflake , I want to do a quick review on CTE and window function

from ast import pattern
import sqlite3
import pandas as pd
from sqlalchemy import CTE 

conn = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')
cursor = conn.cursor() 

# CTE 1 : Find all customers who have spent more than the average customer total spend. Show their full name and total spent, ordered highest first.

query = """
with customer_spend AS(
    SELECT 
          c.CustomerId                     AS customer_id,
          c.FirstName||' '||c.LastName     AS full_name,
          SUM(i.Total)                     AS total_spent
    FROM customers c
    JOIN invoices i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId
)
    SELECT 
            customer_id,
            full_name,
            total_spent
    FROM customer_spend
    WHERE total_spent > (SELECT AVG(total_spent) FROM customer_spend)
    ORDER BY total_spent DESC;
    """
df = pd.read_sql_query(query,conn)
print(df) 


# CTE 2 : CTE 2 — Chained CTEs (the key one)
# Using two chained CTEs:

#CTE 1: total revenue per country
#CTE 2: number of customers per country
#Final SELECT: country, total revenue, customer count, and average spend per customer


query_2 = """
          WITH country_revenue AS (
                        SELECT 
                              i.BillingCountry    AS country,
                              SUM(i.Total)        AS total_revenue
                        FROM invoices i
                        GROUP BY i.BillingCountry
          ),
                country_customers AS (
                        SELECT 
                              c.Country           AS country,
                              COUNT(CustomerId)   AS customer_count
                        FROM customers c 
                        GROUP BY c.Country
          )
        

         SELECT  
                r.country, 
                r.total_revenue,
                c.customer_count,
                r.total_revenue / c.customer_count AS avg_spend_per_customer
            FROM country_revenue r
            JOIN country_customers c ON r.country = c.country
            ORDER BY avg_spend_per_customer DESC;
         """

df_2 = pd.read_sql_query(query_2,conn)
print(df_2)


# CTE 3 : CTE 3 — Business question
    #Find the top 3 best-selling genres by total revenue. But exclude any genre where total revenue came from fewer than 5 unique invoices.

query_3 = """
WITH genre_revenue AS (
    SELECT
        g.Name                          AS genre,
        SUM(il.UnitPrice * il.Quantity) AS total_revenue,
        COUNT(DISTINCT i.InvoiceId)     AS unique_invoices
    FROM genres g
    JOIN tracks t        ON g.GenreId    = t.GenreId
    JOIN invoice_items il ON t.TrackId    = il.TrackId
    JOIN invoices i      ON il.InvoiceId = i.InvoiceId
    GROUP BY g.GenreId, g.Name
),

filtered_genres AS (
    SELECT
        genre,
        total_revenue,
        unique_invoices
    FROM genre_revenue
    WHERE unique_invoices >= 5          -- exclude genres with thin invoice coverage
)

SELECT
    genre,
    ROUND(total_revenue, 2) AS total_revenue,
    unique_invoices
FROM filtered_genres
ORDER BY total_revenue DESC
LIMIT 3;
"""
df_3 = pd.read_sql_query(query_3,conn)
print(df_3)



# +++++++++++++++++++++++++++++++++++++++++++++++++ BLOCK 2 : Window Function ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Window 1 — ROW_NUMBER
#Rank each customer within their country by total spend. Show country, customer name, total spend, and their rank within that country. Only show rank 1 and 2 per country.

query_4 = """
          WITH customer_spend_country AS (
                SELECT 
                      i.BillingCountry      AS country,
                      i.CustomerId          AS customer_id,
                      SUM(i.Total)          AS total_spent,
                      c.FirstName||' '||c.LastName AS full_name
                FROM invoices i
                JOIN customers c ON i.CustomerId = c.CustomerId
                GROUP BY i.BillingCountry, i.CustomerId
                ),

            ranked_customers AS (
                SELECT 
                      country,
                      customer_id,
                      full_name,
                      total_spent,
                      ROW_NUMBER() OVER (PARTITION BY country ORDER BY total_spent DESC) AS country_rank
                FROM customer_spend_country
                   )
                SELECT country, full_name, total_spent, country_rank 
                FROM ranked_customers;
          """
df_4 = pd .read_sql_query(query_4,conn)
print(df_4[df_4['country_rank'] <= 2][['country','full_name','total_spent','country_rank']])

#Window 2 — LAG (the interview favourite)
#Calculate month-over-month revenue change. Show each month, total revenue, previous month revenue, and the difference. Use LAG().
q_5 = """
           WITH monthly_revenue AS (
                SELECT 
                      strftime('%Y-%m', i.InvoiceDate) AS month,
                      SUM(i.Total)                     AS total_revenue
                FROM invoices i 
                GROUP BY month
                ORDER BY month 
    )
                SELECT
                       month, 
                       total_revenue,
                       LAG(total_revenue) OVER (ORDER BY month) AS previous_month_revenue,
                       total_revenue - LAG(total_revenue) OVER (ORDER BY month) AS revenue_change
                       FROM monthly_revenue;
"""
df_5 = pd.read_sql_query(q_5,conn)
print(df_5)


#Window 3 — Running total
#Show a running cumulative total of revenue across all invoices ordered by date. Each row should show the invoice date, that invoice's total, and the cumulative total up to that point.

q_6 = """
         with daily_revenue AS (
                SELECT 
                      strftime('%Y-%m-%d', InvoiceDate) AS day,
                      SUM(Total)         AS daily_total
                FROM invoices 
                GROUP BY day
                ORDER BY day 
            )

                 SELECT 
                        day,
                        daily_total,
                        SUM (daily_total) OVER (ORDER BY day) AS cumulative_revenue
                 FROM daily_revenue;
"""
df_6 = pd.read_sql_query(q_6,conn)
print(df_6)

#Window 4 — RANK vs DENSE_RANK (know the difference)
#Rank all tracks by total quantity sold. Use both RANK() and DENSE_RANK() in the same query to show the difference. Show track name, total quantity sold, RANK, and DENSE_RANK.

q_7 = """
         WITH track_sales AS ( 
               SELECT 
                     t.Name                  AS track_name,
                     SUM(il.Quantity)        AS total_quantity
                FROM tracks t 
                JOIN invoice_items il ON t.Trackcd Id = il.TrackId
                GROUP BY t.TrackId,t.Name
                ORDER BY total_quantity DESC
               )
               SELECT 
                        track_name,
                        total_quantity,
                        RANK() OVER (ORDER BY total_quantity DESC) AS sales_rank,
                        DENSE_RANK() OVER (ORDER BY total_quantity DESC) AS sales_dense_rank
                FROM track_sales;
"""

df_7 = pd.read_sql_query(q_7,conn)
print(df_7)