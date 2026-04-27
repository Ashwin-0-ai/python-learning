# See the DB to understand 
import sqlite3
import pandas as pd

conn = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')
cursor = conn.cursor()

tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)

# Exercise 1 : Show first 10 customer 
cursor.execute("PRAGMA table_info(customers)")
cols = cursor.fetchall()
for col in cols:
    print(col)

# Customer has 2 columns related to name :FirstName & LastName
# Code to show first 10 customer 

query = """
SELECT FirstName, LastName
FROM customers
LIMIT 10
"""
df_top10 = pd.read_sql_query(query,conn)
print("\n Top 10 names of customers:")
print(df_top10)


# Excercise 2 : Show the customers from GERMANY 
query_germany = """
SELECT FirstName, LastName, Country
FROM customers
WHERE Country = 'Germany'
"""
df_germany = pd.read_sql_query(query_germany,conn)
print("\n Customers from Germany:")
print(df_germany)


#Exercise 3 : Count customers per country 
query_count = """
SELECT Country, 
COUNT(*) AS CustomerCount
FROM customers
GROUP BY Country
"""

df_count = pd.read_sql_query(query_count,conn)
print("\n Number of customers per country:")
print(df_count)

# Exercise 4: Countries with more than 5 customers
query_5 = """
SELECT Country 
FROM customers
GROUP BY Country
HAVING COUNT(*) > 5
"""
df_5 = pd.read_sql_query(query_5,conn)

print("\n Countries with more than 5 customers:")
print(df_5)

# Exercise 5: List invoice count per customer
query_invoice = """ 
SELECT FirstName, LastName
FROM customers
JOIN invoices ON customers.CustomerID = invoices.CustomerID
GROUP BY customers.CustomerID"""

df_invoice = pd.read_sql_query(query_invoice,conn)
print("\n Incoice count per customer:")
print(df_invoice)


#Exercise 6: Top 5 customers by total spent
# Want to see the invoice table 's columns
cursor.execute("PRAGMA table_info(invoices)")
cols_invoice = cursor.fetchall()
for col in cols_invoice:
    print(col)

query_top5 = """
SELECT FirstName, LastName,
SUM(Total) AS TotalSpent
FROM customers
JOIN invoices ON customers.CustomerID = invoices.CustomerID
GROUP BY customers.CustomerID
ORDER BY TotalSpent DESC
LIMIT 5
"""

df_top5 = pd.read_sql_query(query_top5,conn)
print("\n Top 5 customers by total spent:")
print(df_top5)

# More Excercises :
#1.Country level revenue summary 
#1.a Want to see country level table 
cursor.execute("PRAGMA table_info(invoices)")
cols_customers = cursor.fetchall()
for col in cols_customers:
    print(col)

query_country_revenue = """ 
SELECT Country,
SUM(Total) AS TotalRevenue
FROM customers
JOIN invoices ON customers.CustomerID = invoices.CustomerID
GROUP BY Country
"""

df_country_revenue = pd.read_sql_query(query_country_revenue, conn)
print("\n Country level revenue summary:")
print(df_country_revenue)

# Monthly Revenue & Monthly Rank 
query_monthly_ranked = """
WITH monthly_revenue AS (
    SELECT strftime('%Y-%m', InvoiceDate) AS Month,
           SUM(Total) AS MonthlyRevenue
    FROM invoices
    GROUP BY Month
)
SELECT Month,
       MonthlyRevenue,
       RANK() OVER (ORDER BY MonthlyRevenue DESC) AS RevenueRank
FROM monthly_revenue
ORDER BY Month
"""

df_ranked = pd.read_sql_query(query_monthly_ranked, conn)
print("\n Monthly Revenue with Rank:")
print(df_ranked)


# Top Customer Per country 
query_top_customer_country = """
WITH CustomerSpend AS (
    SELECT 
        CustomerID,
        FirstName,
        LastName,
        Country,
        (SELECT SUM(Total) 
         FROM invoices 
         WHERE invoices.CustomerID = customers.CustomerID) AS TotalSpent
    FROM customers
),

TopPerCountry AS (
    SELECT *
    FROM CustomerSpend c1
    WHERE TotalSpent = (
        SELECT MAX(TotalSpent)
        FROM CustomerSpend c2
        WHERE c2.Country = c1.Country
    )
)

SELECT FirstName, LastName, Country, TotalSpent
FROM TopPerCountry
ORDER BY Country
"""

df_top_customer_country = pd.read_sql_query(query_top_customer_country, conn)
print("\nTop customer per country:")
print(df_top_customer_country)

#CTE 4: customers above country average spend.
query_above_avg = """
WITH CustomerAvg AS (
    SELECT 
        CustomerID, 
        FirstName, 
        LastName, 
        Country,
        (SELECT AVG(Total)
         FROM invoices
         WHERE invoices.CustomerID = customers.CustomerID) AS AvgSpend
    FROM customers
),

AvgPerCountry AS 
(
    SELECT Country, AVG(AvgSpend) AS CountryAvgSpend
    FROM CustomerAvg
    GROUP BY Country
    )
SELECT ca.FirstName, ca.LastName, ca.Country, ca.AvgSpend,apc.CountryAvgSpend
FROM CustomerAvg ca
JOIN AvgPerCountry apc ON ca.Country = apc.Country
WHERE ca.AvgSpend > apc.CountryAvgSpend
ORDER BY ca.Country,ca.AvgSpend DESC
"""

df_avg_country = pd.read_sql_query(query_above_avg,conn)
print("\n Customers above country average spend:")
print(df_avg_country)
