#===========================================================
# Block B (20-85 min): Build Incremental Framework (timed)
# ==========================================================
# Naming rule: prefix all artifacts with training_.

import sqlite3
from datetime import datetime, timezone

conn = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')

cur = conn.cursor()

# ── Q1: Create state table ─────────────────────────────────────────────────────
#-- Q1 (10 min)
#-- Create pipeline state table.
#-- Table: training_etl_state
#-- Required columns:
#-- pipeline_name (PK), last_invoice_id, last_run_at
#-- Insert one initial row for pipeline_name = 'sales_incremental' if missing.


cur.execute("""
    CREATE TABLE IF NOT EXISTS training_etl_state (
        pipeline_name   TEXT    PRIMARY KEY,
        last_invoice_id INTEGER,
        last_run_at     TEXT
    )
""")

cur.execute("""
    INSERT INTO training_etl_state (pipeline_name, last_invoice_id, last_run_at)
    VALUES ('sales_incremental', 0, NULL)
    ON CONFLICT(pipeline_name) DO NOTHING
""")

# fix NULL watermark if seed row already existed with NULL
cur.execute("""
    UPDATE training_etl_state
    SET last_invoice_id = 0
    WHERE pipeline_name = 'sales_incremental'
    AND last_invoice_id IS NULL
""")

conn.commit()

cur.execute("SELECT * FROM training_etl_state")
print("Q1 state table:", cur.fetchall())

# ── Q2: Create target fact table ───────────────────────────────────────────────
#-- Q2 (15 min)
#-- Create target incremental fact table.
#-- Table: training_fct_sales_incremental
#-- Required columns:
#--   invoice_line_id (unique key), invoice_id, customer_id, track_id,
#--   invoice_date, quantity, unit_price, gross_amount, loaded_at
#-- Add uniqueness so reruns do not duplicate rows.


cur.execute("""
    CREATE TABLE IF NOT EXISTS training_fct_sales_incremental (
        invoice_line_id INTEGER PRIMARY KEY,
        invoice_id      INTEGER NOT NULL,
        customer_id     INTEGER NOT NULL,
        track_id        INTEGER NOT NULL,
        invoice_date    TEXT    NOT NULL,
        quantity        INTEGER NOT NULL,
        unit_price      REAL    NOT NULL,
        gross_amount    REAL    NOT NULL,
        loaded_at       TEXT    NOT NULL
    )
""")

conn.commit()

cur.execute("PRAGMA table_info(training_fct_sales_incremental)")
print("Q2 fact table columns:")
for col in cur.fetchall():
    print(" ", col)

# ── Q3: Incremental load ───────────────────────────────────────────────────────
#Q3 (20 min)
#-- Write incremental load SQL using watermark from training_etl_state.
#-- Load only rows with invoice_id > last_invoice_id.
#-- Populate gross_amount and loaded_at.
#-- Ensure idempotent behavior (no duplicates on rerun).


# read watermark
cur.execute("""
    SELECT COALESCE(
        (SELECT last_invoice_id
         FROM   training_etl_state
         WHERE  pipeline_name = 'sales_incremental'),
        0
    ) AS watermark
""")
watermark = cur.fetchone()[0]
print(f"\nQ3 watermark read: {watermark}")

# extract → transform → load
cur.execute("""
    INSERT INTO training_fct_sales_incremental (
        invoice_line_id,
        invoice_id,
        customer_id,
        track_id,
        invoice_date,
        quantity,
        unit_price,
        gross_amount,
        loaded_at
    )
    SELECT
        ii.InvoiceLineId,
        ii.InvoiceId,
        i.CustomerId,
        ii.TrackId,
        i.InvoiceDate,
        ii.Quantity,
        ii.UnitPrice,
        ii.Quantity * ii.UnitPrice      AS gross_amount,
        ?                               AS loaded_at
    FROM   invoice_items  ii
    JOIN   invoices        i  ON ii.InvoiceId = i.InvoiceId
    WHERE  ii.InvoiceId > ?
    ON CONFLICT(invoice_line_id)
    DO UPDATE SET
        invoice_id   = excluded.invoice_id,
        customer_id  = excluded.customer_id,
        track_id     = excluded.track_id,
        invoice_date = excluded.invoice_date,
        quantity     = excluded.quantity,
        unit_price   = excluded.unit_price,
        gross_amount = excluded.gross_amount,
        loaded_at    = excluded.loaded_at
""", (datetime.now(timezone.utc).isoformat(), watermark))

conn.commit()

cur.execute("""
    SELECT COUNT(*)                    AS total_rows,
           MIN(invoice_id)             AS min_invoice,
           MAX(invoice_id)             AS max_invoice,
           ROUND(SUM(gross_amount), 2) AS total_revenue
    FROM   training_fct_sales_incremental
""")
print("Q3 load result:", cur.fetchone())


#- Q4 (10 min)
#-- Update watermark after load.
#-- Rule:
#--   set last_invoice_id to MAX(invoice_id) from target table for this pipeline.
#--   set last_run_at to current timestamp.
#-- Only do this after quality checks pass.

# 1. Check the quality of the loaded data before updating the watermark

cur.execute("SELECT COUNT(*) FROM training_fct_sales_incremental WHERE invoice_id IS NULL")
null_check = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM training_fct_sales_incremental WHERE gross_amount<=0")
amount_check = cur.fetchone()[0]

print(f"Null check (must=0): {null_check}")
print(f"Negative amount check (must = 0) : {amount_check}")

# 2. Update watermark if check pass

if null_check == 0 and amount_check == 0: 
    
      cur.execute("""
                  UPDATE training_etl_state
                  SET last_invoice_id = (
                      SELECT MAX(invoice_id)
                      FROM   training_fct_sales_incremental
                  ),
                  last_run_at = ?
                  WHERE pipeline_name = 'sales_incremental'
                   """, (datetime.now(timezone.utc).isoformat(),))
      
      conn.commit()

      # Verify Update 
      cur.execute( "SELECT * FROM training_etl_state")
      print("Watermark Updated:",cur.fetchone())

else:
     print("Quality checks FAILED - watermark not updated. Pipeline Aborted")

#-- Q5 (10 min)
#-- Simulate a second run and prove no duplicate inserts happen.
#-- Provide one query showing duplicate count by invoice_line_id is zero.

# READ THE WATERMARK BEFORE THE SECOND RUN 
cur.execute("""
            SELECT COALESCE(
                 (SELECT last_invoice_id
                  FROM training_etl_state
                  WHERE pipeline_name = 'sales_incremental'),
                  0
            ) AS watermark
            """)

watermark = cur.fetchone()[0]
print(f"\n---- Watermark before second run: {watermark}---------------------------------")

# Run the same load again to simulate second run
cur.execute("""
            INSERT INTO training_fct_sales_incremental(
            invoice_line_id,
            invoice_id,
            customer_id,
            track_id,
            invoice_date,
            quantity,
            unit_price,
            gross_amount,
            loaded_at
            )

            SELECT 
                  ii.InvoiceLineId,
                  ii.InvoiceId,
                  i.CustomerId,
                  ii.TrackId,
                  i.InvoiceDate,
                  ii.Quantity,
                  ii.UnitPrice,
                  ii.Quantity * ii.UnitPrice  AS gross_amount,
                  ?                           AS loaded_at     

            FROM invoice_items ii
            JOIN invoices       i ON ii.InvoiceId = i.InvoiceId    
            WHERE ii.InvoiceId > ?
            ON CONFLICT(invoice_line_id)
            DO UPDATE SET
                  invoice_id   = excluded.invoice_id,
                  customer_id  = excluded.customer_id,
                  track_id     = excluded.track_id,
                  invoice_date = excluded.invoice_date,
                  quantity     = excluded.quantity,
                  unit_price   = excluded.unit_price,
                  gross_amount = excluded.gross_amount,
                  loaded_at    = excluded.loaded_at
             """, (datetime.now(timezone.utc).isoformat(), watermark))     

conn.commit()

cur.execute("""
    SELECT COUNT(*) AS duplicate_count
    FROM (
        SELECT   invoice_line_id
        FROM     training_fct_sales_incremental
        GROUP BY invoice_line_id
        HAVING   COUNT(*) > 1
    )
""")
duplicates = cur.fetchone()[0]
print(f"Duplicate invoice_line_id count (must = 0): {duplicates}")

# Step 4 — confirm total row count unchanged
cur.execute("SELECT COUNT(*) FROM training_fct_sales_incremental")
print(f"Total rows after second run (must stay 2240): {cur.fetchone()[0]}")
   
   
#===========================================================
#Block C (85-110 min): Data Quality and Monitoring Queries
#===========================================================
#C1) Row count loaded in this run (hint: use loaded_at window if needed).
#C2) Reconcile incremental gross_amount vs source gross_amount for loaded invoice_id range.
#C3) Null checks on key fields (invoice_line_id, invoice_id, customer_id, track_id).
#C4) Top 5 customers by gross_amount from incremental table.

# C1 (ROW COUNT) 

cur.execute("""
            SELECT DATE(loaded_at)       AS load_date,
            COUNT(*)                     AS rows_loaded,
            MIN(invoice_id)              AS first_invoice,
            MAX(invoice_id)              AS last_invoice
            FROM training_fct_sales_incremental
            GROUP BY DATE(loaded_at)
            ORDER BY load_date DESC
            """)

print("=========C1 - ROW COUNT PER RUN===================================")
for row in cur.fetchall():
      print(" ",row)


# C2 Reconcile gross_amount vs source
cur.execute("""
            SELECT 
                  'fact_table'   AS source,
                  ROUND(SUM(gross_amount),2) AS total_gross
            FROM training_fct_sales_incremental

            UNION ALL

            SELECT 
                  'source_tables' AS source,
                  ROUND(SUM(ii.Quantity * ii.UnitPrice),2) AS total_gross
            FROM invoice_items ii
            JOIN invoices       i ON ii.InvoiceId = i.InvoiceId
            """)

print("\n=========C2 - GROSS AMOUNT RECONCILIATION===================================")
for row in cur.fetchall():
     print(" ",row)


# C3 Null checks on key fields
cur.execute("""
    SELECT
        SUM(CASE WHEN invoice_line_id IS NULL THEN 1 ELSE 0 END) AS null_invoice_line_id,
        SUM(CASE WHEN invoice_id      IS NULL THEN 1 ELSE 0 END) AS null_invoice_id,
        SUM(CASE WHEN customer_id     IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
        SUM(CASE WHEN track_id        IS NULL THEN 1 ELSE 0 END) AS null_track_id
    FROM training_fct_sales_incremental
""")
print("\nC3 — Null checks (all must = 0):")
row = cur.fetchone()
print(f"  null_invoice_line_id : {row[0]}")
print(f"  null_invoice_id      : {row[1]}")
print(f"  null_customer_id     : {row[2]}")
print(f"  null_track_id        : {row[3]}")


# C4 Top 5 customers by gross_amount
cur.execute("""
    SELECT
        f.customer_id,
        c.FirstName || ' ' || c.LastName    AS customer_name,
        COUNT(*)                            AS total_purchases,
        ROUND(SUM(f.gross_amount), 2)       AS total_spent
    FROM   training_fct_sales_incremental f
    JOIN   customers                       c ON f.customer_id = c.CustomerId
    GROUP BY f.customer_id, customer_name
    ORDER BY total_spent DESC
    LIMIT 5
""")
print("\nC4 — Top 5 customers by gross amount:")
for row in cur.fetchall():
    print(f"  {row[1]:<25} | purchases: {row[2]} | spent: ${row[3]}")


#-- ==================================================
#-- Block D (110-120 min): Orchestration Reflection
#-- ==================================================
#-- D1) Write a 6-step pseudo DAG for this pipeline.
#-- D2) At which step should pipeline fail-fast?
#-- D3) What alert metric would you track first in production?

# ── D1: 6-step pseudo DAG ─────────────────────────────────────────────────────

dag = """
PIPELINE: sales_incremental
SCHEDULE: daily @ 02:00 UTC
================================================
STEP 1  read_watermark
        → query training_etl_state
        → output: last_invoice_id (integer)
        → fail if: state table missing or NULL returned
                ↓
STEP 2  extract_new_rows
        → SELECT from invoice_items JOIN invoices
        → filter: InvoiceId > watermark
        → output: raw row count
        → fail if: row count < 0 or source unreachable
                ↓
STEP 3  transform_and_load
        → calculate gross_amount = quantity * unit_price
        → stamp loaded_at = now()
        → upsert into training_fct_sales_incremental
        → output: rows inserted/updated
        → fail if: sqlite error or row count mismatch
                ↓
STEP 4  quality_checks
        → null check  : key fields must have 0 nulls
        → amount check: gross_amount must be > 0
        → reconcile   : fact total must match source total
        → output: pass / fail
        → fail if: ANY check returns non-zero
                ↓
STEP 5  update_watermark
        → SET last_invoice_id = MAX(invoice_id)
        → SET last_run_at     = now()
        → only runs if step 4 = pass
        → fail if: update affects 0 rows
                ↓
STEP 6  log_and_alert
        → log: rows loaded, run duration, watermark value
        → alert if: rows loaded = 0 (unexpected empty run)
        → alert if: any step failed
        → output: pipeline status = SUCCESS / FAILED
================================================
"""
print(dag)


# ── D2: Fail-fast step ────────────────────────────────────────────────────────
# ── D1: 6-step pseudo DAG ─────────────────────────────────────────────────────

dag = """
PIPELINE: sales_incremental
SCHEDULE: daily @ 02:00 UTC
================================================
STEP 1  read_watermark
        → query training_etl_state
        → output: last_invoice_id (integer)
        → fail if: state table missing or NULL returned
                ↓
STEP 2  extract_new_rows
        → SELECT from invoice_items JOIN invoices
        → filter: InvoiceId > watermark
        → output: raw row count
        → fail if: row count < 0 or source unreachable
                ↓
STEP 3  transform_and_load
        → calculate gross_amount = quantity * unit_price
        → stamp loaded_at = now()
        → upsert into training_fct_sales_incremental
        → output: rows inserted/updated
        → fail if: sqlite error or row count mismatch
                ↓
STEP 4  quality_checks
        → null check  : key fields must have 0 nulls
        → amount check: gross_amount must be > 0
        → reconcile   : fact total must match source total
        → output: pass / fail
        → fail if: ANY check returns non-zero
                ↓
STEP 5  update_watermark
        → SET last_invoice_id = MAX(invoice_id)
        → SET last_run_at     = now()
        → only runs if step 4 = pass
        → fail if: update affects 0 rows
                ↓
STEP 6  log_and_alert
        → log: rows loaded, run duration, watermark value
        → alert if: rows loaded = 0 (unexpected empty run)
        → alert if: any step failed
        → output: pipeline status = SUCCESS / FAILED
================================================
"""
print(dag)


# ── D2: Fail-fast step ────────────────────────────────────────────────────────

fail_fast = """
FAIL-FAST AT: STEP 2 — extract_new_rows

Reason:
  If the source returns zero rows when you expected new data,
  or the source tables are unreachable, there is no point
  running steps 3, 4, or 5. You would be loading nothing,
  running quality checks on nothing, and moving a watermark
  that should not move.

  Fail early = saves compute, prevents silent empty loads,
  forces an alert before bad state propagates downstream.

Rule:
  if extracted_row_count == 0 and watermark < MAX(source InvoiceId):
      raise PipelineError("Expected new rows but got none — investigate source")
"""
print(fail_fast)


# ── D3: First production alert metric ─────────────────────────────────────────

alert_metric = """
FIRST METRIC TO TRACK: rows_loaded_per_run

Why this first:
  Every other problem eventually shows up here.
  - Source broke?         → rows_loaded = 0
  - Watermark stuck?      → rows_loaded = 0
  - Filter too aggressive → rows_loaded = 0
  - Data exploded?        → rows_loaded abnormally high

Alert thresholds (example):
  CRITICAL : rows_loaded = 0        (nothing came through)
  WARNING  : rows_loaded > 10,000   (unexpected volume spike)
  INFO     : rows_loaded < 10       (suspiciously quiet day)

Second metric to add once rows_loaded is stable:
  → reconciliation_delta
     ABS(fact_total_gross - source_total_gross)
     must always = 0.00
     any non-zero value means money is missing or duplicated
"""
print(alert_metric)

