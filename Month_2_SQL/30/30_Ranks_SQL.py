import sqlite3 
import pandas as pd 

conn = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')
cursor = conn.cursor() 

tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)

# Query 1 : Rank Customers by total Spend Global using All 3 functions ?; RANK() , DENSE_RANK() & ROW_NUMBER()
query_rank= """
SELECT 
    c.CustomerID,
    c.FirstName || ' ' || c.LastName AS CustomerName,
    c.City,
    c.Country,
    SUM(i.Total) AS Totalspent,

    RANK() OVER (ORDER BY SUM(i.Total) DESC) AS Rank_RANK,
    DENSE_RANK() OVER (ORDER BY SUM(i.Total) DESC) AS Rank_DENSE_RANK,
    ROW_NUMBER() OVER (ORDER BY SUM(i.Total) DESC) AS Rank_ROW_NUMBER   

FROM customers c
JOIN invoices i ON c.CustomerID = i.CustomerID
GROUP BY c.CustomerID, c.FirstName, c.LastName, c.City, c.Country
ORDER BY Totalspent DESC;
"""

print("\n Customer ranking by total spend:  ")
df_rank = pd.read_sql_query(query_rank, conn)

pd.set_option('display.max_columns', None)   
pd.set_option('display.width', None)     
print(df_rank)

# query 2 : Rank customers by spend within each country
query_rank_country ="""
SELECT 
    c.CustomerID,
    c.FirstName ||'  ' ||c.LastName AS CustomerName,
    c.City,
    c.Country,
    SUM(i.total) AS TotalSpent,
    
    RANK () OVER (PARTIONED BY c.Country ORDER BY SUM(i.Total) DESC) AS Rank_RANK,
    DENSE_RANK() OVER (PARTIONED BY c.Country ORDER BY SUM(i.Total) DESC) AS Rank_DENSE_RANK,
    ROW_NUMBER() OVER (PARTIONED BY c.Country ORDER BY SUM(i.Total) DESC) AS Rank_ROW_NUMBER
FROM customers c 
JOIN invoices i ON c.CustomerID = i.CustomerID
GROUP BY c.CustomerID, c.FirstName, c.LastName, c.City, c.Country
ORDER BY c.Country, TotalSpent DESC;
"""

# Query 3: Top 3 customers per country using ROW_NUMBER.
query_top3 = """
SELECT *
FROM (
    SELECT 
        c.CustomerId,
        c.FirstName || ' ' || c.LastName AS CustomerName,
        c.Country,
        SUM(i.Total) AS TotalSpent,
        ROW_NUMBER() OVER (PARTITION BY c.Country ORDER BY SUM(i.Total) DESC) AS RowNum
    FROM customers c
    JOIN invoices i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId, c.FirstName, c.LastName, c.Country
)
WHERE RowNum <= 3
ORDER BY Country, RowNum;
"""

df_top3 = pd.read_sql_query(query_top3, conn)
print("\n Top 3 customers per country:")        
print(df_top3)

# Query 4: Top invoice per customer using ROW_NUMBER on invoice total.
query_top_invoice = """
SELECT *
FROM (
    SELECT
        c.CustomerId,
        c.FirstName || ' ' || c.LastName AS CustomerName,
        c.Country,
        i.InvoiceId,
        i.InvoiceDate,
        i.Total AS InvoiceTotal,

        ROW_NUMBER() OVER (
            PARTITION BY c.CustomerId
            ORDER BY i.Total DESC
        ) AS rn

    FROM customers c
    JOIN invoices i ON c.CustomerId = i.CustomerId
)
WHERE rn = 1
ORDER BY InvoiceTotal DESC;
"""

df_top_invoice = pd.read_sql_query(query_top_invoice, conn)
print('\nTop Invoice per Customer (by Invoice Total):')
print(df_top_invoice.to_string(index=False))