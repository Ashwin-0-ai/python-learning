import sqlite3
import pandas as pd
from datetime import datetime

# ── Single connection for the whole file ────────────────────────────────────
conn = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')
cursor = conn.cursor()

# ════════════════════════════════════════════════════════════════════════════
# Q1 — Create staging snapshot table
# ════════════════════════════════════════════════════════════════════════════

cursor.execute("DROP TABLE IF EXISTS training_stg_customer_snapshot")

cursor.execute("""
    CREATE TABLE training_stg_customer_snapshot (
        snapshot_date  TEXT,
        customer_id    INTEGER,
        first_name     TEXT,
        last_name      TEXT,
        company        TEXT,
        city           TEXT,
        country        TEXT,
        email          TEXT
    )
""")
conn.commit()
print("training_stg_customer_snapshot created successfully.")

# Snapshot 1
cursor.execute("""
    INSERT INTO training_stg_customer_snapshot
    SELECT
        '2024-01-01' AS snapshot_date,
        CustomerId   AS customer_id,
        FirstName    AS first_name,
        LastName     AS last_name,
        Company      AS company,
        City         AS city,
        Country      AS country,
        Email        AS email
    FROM customers
""")

# Snapshot 2
cursor.execute("""
    INSERT INTO training_stg_customer_snapshot
    SELECT
        '2024-02-01' AS snapshot_date,
        CustomerId   AS customer_id,
        FirstName    AS first_name,
        LastName     AS last_name,
        Company      AS company,
        City         AS city,
        Country      AS country,
        Email        AS email
    FROM customers
""")

conn.commit()
print("Both snapshots inserted successfully.")

# Simulate changes in snapshot 2 only
cursor.execute("""
    UPDATE training_stg_customer_snapshot
    SET city = 'Berlin'
    WHERE customer_id = 1 AND snapshot_date = '2024-02-01'
""")

cursor.execute("""
    UPDATE training_stg_customer_snapshot
    SET company = 'New Ventures Ltd'
    WHERE customer_id = 2 AND snapshot_date = '2024-02-01'
""")

cursor.execute("""
    UPDATE training_stg_customer_snapshot
    SET city = 'Toronto', country = 'Canada'
    WHERE customer_id = 3 AND snapshot_date = '2024-02-01'
""")

conn.commit()
print("Changes simulated.")

# Verify changes
df_check = pd.read_sql("""
    SELECT snapshot_date, customer_id, first_name, city, country, company
    FROM training_stg_customer_snapshot
    WHERE customer_id IN (1, 2, 3)
    ORDER BY customer_id, snapshot_date
""", conn)

print(df_check)

# ════════════════════════════════════════════════════════════════════════════
# Q2 — Build SCD Type 1 dimension
# ════════════════════════════════════════════════════════════════════════════

cursor.execute("DROP TABLE IF EXISTS training_dim_customer_scd1")

cursor.execute("""
    CREATE TABLE training_dim_customer_scd1 (
        customer_key  INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id   INTEGER,
        full_name     TEXT,
        company       TEXT,
        city          TEXT,
        country       TEXT,
        email         TEXT,
        updated_at    TEXT
    )
""")

conn.commit()
print("training_dim_customer_scd1 created successfully.")

# Pull latest snapshot
df = pd.read_sql("""
    SELECT
        customer_id,
        first_name || ' ' || last_name AS full_name,
        company,
        city,
        country,
        email
    FROM training_stg_customer_snapshot
    WHERE snapshot_date = (
        SELECT MAX(snapshot_date)
        FROM training_stg_customer_snapshot
    )
""", conn)

print(f"Rows pulled from latest snapshot: {len(df)}")

# Add updated_at in Python
df['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Load into SCD1 table
df.to_sql(
    name='training_dim_customer_scd1',
    con=conn,
    if_exists='append',
    index=False
)

conn.commit()
print("SCD1 dimension loaded successfully.")

# Verify
verify = pd.read_sql("""
    SELECT *
    FROM training_dim_customer_scd1
    ORDER BY customer_key
    LIMIT 10
""", conn)

print(verify)

# Duplicate check
dup_check = pd.read_sql("""
    SELECT customer_id, COUNT(*) AS row_count
    FROM training_dim_customer_scd1
    GROUP BY customer_id
    HAVING COUNT(*) > 1
""", conn)

if dup_check.empty:
    print("\n✅ No duplicates — one row per customer_id confirmed.")
else:
    print("\n⚠️ Duplicates found:")
    print(dup_check)


#Q3 (20 min)
#-- Build SCD Type 2 dimension from snapshot history.
#-- Table: training_dim_customer_scd2
#-- Required columns:
#--   customer_sk, customer_id, full_name, company, city, country, email,
#--   effective_from, effective_to, is_current
#-- Rules:
#--   1) Keep version history per customer_id.
#--   2) Exactly one current row per customer_id.
#--   3) Close old rows with effective_to.


cursor.execute("DROP TABLE IF EXISTS training_dim_customer_scd2")

cursor.execute("""
               CREATE TABLE training_dim_customer_scd2(
                   customer_sk INTEGER PRIMARY KEY AUTOINCREMENT,
                   customer_id INTEGER,
                   full_name TEXT,
                   company TEXT,
                   city TEXT,
                   country TEXT,
                   email TEXT,
                   effective_from TEXT,
                   effective_to TEXT,
                   is_current INTEGER
               )
               """)

conn.commit()
print("Table training_dim_customer_scd2 created successfully.")

# Snapshot 1 :

df_snap1 = pd.read_sql("""
                          SELECT 
                            customer_id,
                            first_name||' '||last_name AS full_name,
                            company,
                            city,
                            country,
                            email,
                       snapshot_date
                FROM training_stg_customer_snapshot
                WHERE snapshot_date = (
                       SELECT MIN(snapshot_date)
                       FROM training_stg_customer_snapshot
                       )                   
                       """, conn)

print(f" Snapshot 1 rows :{len(df_snap1)}")

# SnapShot 2 :
df_snap2 = pd.read_sql("""
                            SELECT 
                            customer_id,
                            first_name||' '||last_name AS full_name,
                            company,
                            city,
                            country,
                            email,
                          snapshot_date
                FROM training_stg_customer_snapshot
                WHERE snapshot_date = (
                       SELECT MAX(snapshot_date)
                       FROM training_stg_customer_snapshot
                       )                   
                       """,conn)

print(f"Snapshot 2 rows :{len(df_snap2)}")


# Detect Changes 
# Merge snapshot on customer_id
# Compare city,company,country 

merged = df_snap1.merge(
    df_snap2,
    on='customer_id',
    suffixes=('_snap1', '_snap2')
)

# Identify Changes 
changed_mask = ( 
    (merged['city_snap1']     != merged['city_snap2']) |
    (merged['company_snap1']  != merged['company_snap2']) |
    (merged['country_snap1']  != merged['country_snap2'])
)


changed_ids = merged.loc[changed_mask, 'customer_id'].tolist()

print (f" Changed customer IDs : {changed_ids}")

# Building version 1 row 

snap2_date = df_snap2['snapshot_date'].iloc[0]

df_v1 = df_snap1.copy()
df_v1['effective_from'] = df_v1['snapshot_date']
df_v1['effective_to']   = df_v1['customer_id'].apply(lambda cid:0 if cid in changed_ids else None)
df_v1['is_current']     = df_v1['customer_id'].apply(lambda cid:0 if cid in changed_ids else 1 )
df_v1.drop(columns=['snapshot_date'],inplace=True)

print(f" Version 1 rows built : {len(df_v1)}")

# Building version 2 row 

df_v2 = df_snap2[df_snap2['customer_id'].isin(changed_ids)].copy()
df_v2['effective_from'] = df_v2['snapshot_date']
df_v2['effective_to']   = None
df_v2['is_current']     = 1
df_v2.drop(columns=['snapshot_date'], inplace=True)

print(f"Version 2 rows built (changed customers only): {len(df_v2)}")


df_final = pd.concat([df_v1, df_v2], ignore_index=True)
df_final = df_final.sort_values(
    by=['customer_id', 'effective_from']
).reset_index(drop=True)

print(f"Total rows to load: {len(df_final)}")

df_final.to_sql(
    name='training_dim_customer_scd2',
    con=conn,
    if_exists='append',
    index=False
)

conn.commit()
print("SCD2 dimension loaded successfully.")




