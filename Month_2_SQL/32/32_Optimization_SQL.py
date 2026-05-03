#Build 5 exercises

#Exercise 1: Run EXPLAIN QUERY PLAN on a basic query, understand the output.
#Exercise 3: Create an index on a column, re-run EXPLAIN, compare output.
#Exercise 4: Measure query pattern differences (SCAN vs SEARCH).
#Exercise 5: Drop the index and observe the revert.

import sqlite3
import pandas as pd 
conn = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')
cursor = conn.cursor()

#Exercise 1: Run EXPLAIN QUERY PLAN on a basic query, understand the output.
print("=== Exercise 1: EXPLAIN QUERY PLAN baseline ===")
cursor.execute("""
    EXPLAIN QUERY PLAN
    SELECT c.FirstName, c.LastName, SUM(i.Total) AS total_spent
    FROM customers c
    JOIN invoices i ON c.CustomerId = i.CustomerId
    WHERE c.Country = 'Germany'
    GROUP BY c.CustomerId
""")
for row in cursor.fetchall():
    print(row)

#Exercise 2: Show all existing indexes in Chinook.
print ("\n Excercise 2 : Show all exsisting indexes in Chinook.db")
exsisting = pd.read_sql_query("""
        SELECT name,tbl_name,sql
        FROM sqlite_master 
        WHERE type = 'index'
        ORDER BY tbl_name
        """,conn)

print(exsisting.to_string())

# Exercise 3: Create an index on Country, re-run EXPLAIN
# Before Creating Index 

cursor.execute ("""CREATE INDEX IF NOT EXISTS idx_customers_country ON customers(Country)""")
conn.commit()
print ("Index Created")

cursor.execute(""" 
        EXPLAIN QUERY PLAN
        SELECT c.FirstName, c.LastName, SUM(i.Total) AS total_spent
        FROM customers c
        JOIN invoices i ON c.CustomerId =i.CustomerId
               WHERE c.Country = 'Germany'
        GROUP BY c.CustomerID
    """)

for row in cursor.fetchall():
    print(row)

# Exercise 4: Create index on invoices.CustomerId (join column)
cursor.execute("CREATE INDEX IF NOT EXISTS idx_invoices_customerid ON invoices(CustomerId)")
conn.commit()

cursor.execute (""" 
        EXPLAIN QUERY PLAN
        SELECT c.FirstName, c.LastName, SUM(i.Total) AS total_spent
        FROM customers c
        JOIN invoices i ON c.CustomerId =i.CustomerId
        GROUP BY c.CustomerID
        ORDER by total_spent DESC
                
    """)

for row in cursor.fetchall():
    print(row)


# Exercise 5: Drop indexes and observe revert

cursor.execute("DROP INDEX IF EXISTS idx_customers_country")
cursor.execute("DROP INDEX IF EXISTS idx_invoices_customerid")
conn.commit()
print("Indexes dropped.")

cursor.execute("""
    EXPLAIN QUERY PLAN
    SELECT c.FirstName, c.LastName, SUM(i.Total) AS total_spent
    FROM customers c
    JOIN invoices i ON c.CustomerId = i.CustomerId
    WHERE c.Country = 'Germany'
    GROUP BY c.CustomerId
""")
for row in cursor.fetchall():
    print(row)

notes = """
WHEN TO ADD AN INDEX:
- Columns frequently used in WHERE filters
- Columns used in JOIN conditions
- Columns used in ORDER BY on large tables

WHEN NOT TO ADD AN INDEX:
- Small tables (full scan is fast enough)
- Columns with very low cardinality (e.g. a boolean flag)
- Tables with heavy INSERT/UPDATE load (indexes slow writes)

CHINOOK COLUMNS THAT WOULD BENEFIT MOST:
- invoices.CustomerId (join column, used constantly)
- customers.Country (frequent filter in marketing queries)
- invoice_items.InvoiceId (join column in line-level queries)
- tracks.GenreId (frequent filter in genre analysis)
"""
print(notes)

conn.close()