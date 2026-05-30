import sqlite3
import pandas as pd

conn   = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')
cursor = conn.cursor()

# ─────────────────────────────────────────────
# Q1 — training_dim_date
# ─────────────────────────────────────────────

DROP_DIM_DATE = "DROP TABLE IF EXISTS training_dim_date"

CREATE_DIM_DATE = """
CREATE TABLE training_dim_date AS
SELECT
    CAST(strftime('%Y%m%d', InvoiceDate) AS INTEGER)            AS date_key,
    DATE(InvoiceDate)                                           AS calendar_date,
    CAST(strftime('%Y', InvoiceDate) AS INTEGER)                AS year,
    CAST(strftime('%m', InvoiceDate) AS INTEGER)                AS month,
    CASE CAST(strftime('%m', InvoiceDate) AS INTEGER)
        WHEN 1  THEN 'January'   WHEN 2  THEN 'February'
        WHEN 3  THEN 'March'     WHEN 4  THEN 'April'
        WHEN 5  THEN 'May'       WHEN 6  THEN 'June'
        WHEN 7  THEN 'July'      WHEN 8  THEN 'August'
        WHEN 9  THEN 'September' WHEN 10 THEN 'October'
        WHEN 11 THEN 'November'  WHEN 12 THEN 'December'
    END                                                         AS month_name,
    (CAST(strftime('%m', InvoiceDate) AS INTEGER) - 1) / 3 + 1 AS quarter
FROM invoices
GROUP BY DATE(InvoiceDate)
ORDER BY date_key;
"""

cursor.execute(DROP_DIM_DATE)
cursor.execute(CREATE_DIM_DATE)
conn.commit()

count = cursor.execute("SELECT COUNT(*) FROM training_dim_date").fetchone()[0]
print(f"training_dim_date → {count} rows")
df = pd.read_sql("SELECT * FROM training_dim_date LIMIT 5", conn)
print(df.to_string(index=False))

# ─────────────────────────────────────────────
# Q2 — training_dim_customer
# ─────────────────────────────────────────────

DROP_DIM_CUSTOMER = "DROP TABLE IF EXISTS training_dim_customer"

CREATE_DIM_CUSTOMER = """
CREATE TABLE training_dim_customer AS
SELECT
    CustomerId                      AS customer_key,
    CustomerId                      AS customer_id,
    FirstName || ' ' || LastName    AS full_name,
    Country                         AS country,
    City                            AS city,
    COALESCE(Company, 'Individual') AS company
FROM customers
ORDER BY customer_key;
"""

cursor.execute(DROP_DIM_CUSTOMER)
cursor.execute(CREATE_DIM_CUSTOMER)
conn.commit()

count = cursor.execute("SELECT COUNT(*) FROM training_dim_customer").fetchone()[0]
print(f"\ntraining_dim_customer → {count} rows")
df = pd.read_sql("SELECT * FROM training_dim_customer LIMIT 5", conn)
print(df.to_string(index=False))

# ─────────────────────────────────────────────
# Q3 — training_dim_track
# ─────────────────────────────────────────────

DROP_DIM_TRACK = "DROP TABLE IF EXISTS training_dim_track"

CREATE_DIM_TRACK = """
CREATE TABLE training_dim_track AS
SELECT
    t.TrackId                      AS track_key,
    t.TrackId                      AS track_id,
    t.Name                         AS track_name,
    al.Title                       AS album_title,
    ar.Name                        AS artist_name,
    g.Name                         AS genre_name,
    mt.Name                        AS media_type_name,
    t.UnitPrice                    AS unit_price
FROM tracks       t
JOIN albums       al ON t.AlbumId     = al.AlbumId
JOIN artists      ar ON al.ArtistId   = ar.ArtistId
JOIN genres       g  ON t.GenreId     = g.GenreId
JOIN media_types  mt ON t.MediaTypeId = mt.MediaTypeId
ORDER BY track_key;
"""

cursor.execute(DROP_DIM_TRACK)
cursor.execute(CREATE_DIM_TRACK)
conn.commit()

count = cursor.execute("SELECT COUNT(*) FROM training_dim_track").fetchone()[0]
print(f"\ntraining_dim_track → {count} rows")
df = pd.read_sql("SELECT * FROM training_dim_track LIMIT 5", conn)
print(df.to_string(index=False))

# ─────────────────────────────────────────────
# Q4 — training_fct_sales
# ─────────────────────────────────────────────

DROP_FCT_SALES = "DROP TABLE IF EXISTS training_fct_sales"

CREATE_FCT_SALES = """
CREATE TABLE training_fct_sales AS
SELECT
    ii.InvoiceLineId                                        AS sales_key,
    ii.InvoiceLineId                                        AS invoice_line_id,
    ii.InvoiceId                                            AS invoice_id,
    i.CustomerId                                            AS customer_id,
    ii.TrackId                                              AS track_id,
    CAST(strftime('%Y%m%d', i.InvoiceDate) AS INTEGER)      AS date_key,
    ii.Quantity                                             AS quantity,
    ii.UnitPrice                                            AS unit_price,
    ii.Quantity * ii.UnitPrice                              AS gross_amount
FROM invoice_items ii
JOIN invoices       i ON ii.InvoiceId = i.InvoiceId
ORDER BY sales_key;
"""

cursor.execute(DROP_FCT_SALES)
cursor.execute(CREATE_FCT_SALES)
conn.commit()

count = cursor.execute("SELECT COUNT(*) FROM training_fct_sales").fetchone()[0]
print(f"\ntraining_fct_sales → {count} rows")

df = pd.read_sql("SELECT * FROM training_fct_sales LIMIT 5", conn)
print(df.to_string(index=False))

df_nulls = pd.read_sql("""
SELECT
    SUM(CASE WHEN customer_id  IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
    SUM(CASE WHEN track_id     IS NULL THEN 1 ELSE 0 END) AS null_track_id,
    SUM(CASE WHEN date_key     IS NULL THEN 1 ELSE 0 END) AS null_date_key,
    SUM(CASE WHEN gross_amount IS NULL THEN 1 ELSE 0 END) AS null_gross_amount
FROM training_fct_sales
""", conn)
print("\nNull check (all should be 0):")
print(df_nulls.to_string(index=False))

df_totals = pd.read_sql("""
SELECT
    COUNT(*)                        AS total_rows,
    SUM(quantity)                   AS total_units,
    ROUND(SUM(gross_amount), 2)     AS total_revenue,
    ROUND(AVG(gross_amount), 2)     AS avg_line_value,
    ROUND(MAX(gross_amount), 2)     AS max_line_value,
    ROUND(MIN(gross_amount), 2)     AS min_line_value
FROM training_fct_sales
""", conn)
print("\nBusiness totals:")
print(df_totals.to_string(index=False))

# ─────────────────────────────────────────────
# Block C — KPI queries
# ─────────────────────────────────────────────

print("\n======================= C1 — Monthly revenue trend =======================")
df_1 = pd.read_sql("""
SELECT
    d.year                          AS year,
    d.month                         AS month,
    d.month_name                    AS month_name,
    COUNT(f.sales_key)              AS total_transactions,
    SUM(f.quantity)                 AS total_units,
    ROUND(SUM(f.gross_amount), 2)   AS revenue
FROM training_fct_sales  f
JOIN training_dim_date   d ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month
""", conn)
print(df_1.to_string(index=False))
print(f"\nGrand total: ${df_1['revenue'].sum():,.2f}  ← must equal $2,328.60")

print("\n======================= C2 — Top 5 customers =============================")
df_2 = pd.read_sql("""
SELECT
    d.full_name                         AS customer,
    d.country                           AS country,
    d.city                              AS city,
    COUNT(f.sales_key)                  AS total_purchases,
    ROUND(SUM(f.gross_amount), 2)       AS total_spent
FROM training_fct_sales    f
JOIN training_dim_customer d ON f.customer_id = d.customer_id
GROUP BY d.customer_id
ORDER BY total_spent DESC
LIMIT 5
""", conn)
print(df_2.to_string(index=False))

print("\n======================= C3 — Revenue by genre ============================")
df_3 = pd.read_sql("""
SELECT
    d.genre_name                        AS genre,
    COUNT(f.sales_key)                  AS total_transactions,
    SUM(f.quantity)                     AS total_units,
    ROUND(SUM(f.gross_amount), 2)       AS revenue
FROM training_fct_sales f
JOIN training_dim_track d ON f.track_id = d.track_id
GROUP BY d.genre_name
ORDER BY revenue DESC
""", conn)
print(df_3.to_string(index=False))

print("\n======================= C4 — Customer x genre ============================")
df_4 = pd.read_sql("""
SELECT
    c.full_name                         AS customer,
    t.genre_name                        AS genre,
    COUNT(f.sales_key)                  AS total_transactions,
    SUM(f.quantity)                     AS total_units,
    ROUND(SUM(f.gross_amount), 2)       AS revenue
FROM training_fct_sales    f
JOIN training_dim_customer c ON f.customer_id = c.customer_id
JOIN training_dim_track    t ON f.track_id    = t.track_id
GROUP BY c.full_name, t.genre_name
ORDER BY revenue DESC
LIMIT 10
""", conn)
print(df_4.to_string(index=False))

