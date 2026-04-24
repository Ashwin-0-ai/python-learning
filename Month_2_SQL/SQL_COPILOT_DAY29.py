# See the DB to understand 
import sqlite3
import pandas as pd

conn = sqlite3.connect('chinook.db')
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
