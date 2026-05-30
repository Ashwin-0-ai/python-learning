import sqlite3

conn = sqlite3.connect(r'D:\Mission_Blitzkreig\Month_2_SQL\29_copilot\chinook.db')
conn.row_factory = sqlite3.Row  # needed so row.keys() works

def q1_create_state_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS training_etl_state_v2 (
            pipeline_name            TEXT    PRIMARY KEY,
            last_successful_run_at   TEXT    NOT NULL,
            overlap_days             INTEGER NOT NULL DEFAULT 3,
            last_max_invoice_id      INTEGER,
            last_run_status          TEXT    NOT NULL DEFAULT 'INIT'
        )
    """)

    conn.execute("""
        INSERT OR IGNORE INTO training_etl_state_v2
            (pipeline_name, last_successful_run_at, overlap_days,
             last_max_invoice_id, last_run_status)
        VALUES
            ('sales_overlap_incremental', '2010-12-31 00:00:00', 3, NULL, 'INIT')
    """)

    conn.commit()

    row = conn.execute("""
        SELECT * FROM training_etl_state_v2
        WHERE pipeline_name = 'sales_overlap_incremental'
    """).fetchone()

    print("Q1 state row:")
    for key in row.keys():
        print(f"  {key:<30} {row[key]}")


q1_create_state_table(conn)  # <-- this was missing


#Q2 (15 min)
#-- Create target table for overlap loads.
#-- Table: training_fct_sales_overlap
#-- Required columns:invoice_date, quantity, unit_price, gross_amount,extracted_window_start, extracted_window_end, loaded_at


def q2_create_fact_table(conn):
    conn.execute("DROP TABLE IF EXISTS training_fct_sales_overlap")
    
    conn.execute("""
        CREATE TABLE training_fct_sales_overlap (
            invoice_line_id         INTEGER PRIMARY KEY,
            invoice_id              INTEGER NOT NULL,
            customer_id             INTEGER NOT NULL,
            track_id                INTEGER NOT NULL,
            invoice_date            TEXT    NOT NULL,
            quantity                INTEGER NOT NULL,
            unit_price              REAL    NOT NULL,
            gross_amount            REAL    NOT NULL,
            extracted_window_start  TEXT    NOT NULL,
            extracted_window_end    TEXT    NOT NULL,
            loaded_at               TEXT    NOT NULL
        )
    """)

    conn.commit()
    print("================Q2: training_fct_sales_overlap created successfully=======================")

q2_create_fact_table(conn)



#Q3 (20 min)
#Write incremental extraction + load SQL using overlap logic.
#Rules:
#--   1) derive window_start from last_successful_run_at minus overlap_days.
#--   2) window_end is current timestamp.
#--   3) load invoice rows where InvoiceDate is between window_start and window_end.
#--   4) apply idempotent upsert behavior on invoice_line_id.

def q3_overlap_load(conn):
    state = conn.execute("""
        SELECT last_successful_run_at, overlap_days
        FROM training_etl_state_v2
        WHERE pipeline_name = 'sales_overlap_incremental'
    """).fetchone()

    from datetime import datetime, timedelta
    last_run     = datetime.fromisoformat(state["last_successful_run_at"])
    overlap      = state["overlap_days"]
    window_start = (last_run - timedelta(days=overlap)).strftime("%Y-%m-%d %H:%M:%S")
    window_end   = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Q3 window: {window_start} --> {window_end}")

    conn.execute("""
        INSERT INTO training_fct_sales_overlap (
            invoice_line_id, invoice_id, customer_id, track_id,
            invoice_date, quantity, unit_price, gross_amount,
            extracted_window_start, extracted_window_end, loaded_at
        )
        SELECT
            ii.InvoiceLineId,
            i.InvoiceId,
            i.CustomerId,
            ii.TrackId,
            i.InvoiceDate,
            ii.Quantity,
            ii.UnitPrice,
            ROUND(ii.Quantity * ii.UnitPrice, 2),
            :window_start,
            :window_end,
            :window_end
        FROM invoice_items ii
        JOIN invoices i ON ii.InvoiceId = i.InvoiceId
        WHERE i.InvoiceDate >= :window_start
          AND i.InvoiceDate <  :window_end

        ON CONFLICT(invoice_line_id) DO UPDATE SET
            invoice_id             = excluded.invoice_id,
            customer_id            = excluded.customer_id,
            track_id               = excluded.track_id,
            invoice_date           = excluded.invoice_date,
            quantity               = excluded.quantity,
            unit_price             = excluded.unit_price,
            gross_amount           = excluded.gross_amount,
            extracted_window_start = excluded.extracted_window_start,
            extracted_window_end   = excluded.extracted_window_end,
            loaded_at              = excluded.loaded_at
    """, {"window_start": window_start, "window_end": window_end})

    conn.commit()

    row_count = conn.execute(
        "SELECT COUNT(*) AS cnt FROM training_fct_sales_overlap"
    ).fetchone()["cnt"]
    print(f"Q3 rows in fact table: {row_count}")

    return window_start, window_end


window_start, window_end = q3_overlap_load(conn)


#-- Q4 (10 min)
#-- Write post-load checks.
#-- C1) duplicate check on invoice_line_id must be zero.
#-- C2) null checks on key columns.
#-- C3) reconciliation: compare SUM(gross_amount) between source and target for current window.

def q4_quality_checks(conn, window_start, window_end):
    all_pass = True

    # C1 — duplicate check
    dup = conn.execute("""
        SELECT
            COUNT(*)                        AS total_rows,
            COUNT(DISTINCT invoice_line_id) AS distinct_keys
        FROM training_fct_sales_overlap
    """).fetchone()

    dup_count = dup["total_rows"] - dup["distinct_keys"]
    c1_pass   = dup_count == 0
    print(f"C1 dup check  : {'PASS' if c1_pass else 'FAIL'} (dups={dup_count})")
    if not c1_pass:
        all_pass = False

    # C2 — null check
    null_count = conn.execute("""
        SELECT COUNT(*) AS null_rows
        FROM training_fct_sales_overlap
        WHERE invoice_line_id IS NULL
           OR invoice_id      IS NULL
           OR customer_id     IS NULL
           OR invoice_date    IS NULL
           OR gross_amount    IS NULL
    """).fetchone()["null_rows"]

    c2_pass = null_count == 0
    print(f"C2 null check : {'PASS' if c2_pass else 'FAIL'} (nulls={null_count})")
    if not c2_pass:
        all_pass = False

    # C3 — reconciliation
    src_sum = conn.execute("""
        SELECT ROUND(SUM(ii.Quantity * ii.UnitPrice), 2) AS src_sum
        FROM invoice_items ii
        JOIN invoices i ON ii.InvoiceId = i.InvoiceId
        WHERE i.InvoiceDate >= :ws
          AND i.InvoiceDate <  :we
    """, {"ws": window_start, "we": window_end}).fetchone()["src_sum"] or 0.0

    tgt_sum = conn.execute("""
        SELECT ROUND(SUM(gross_amount), 2) AS tgt_sum
        FROM training_fct_sales_overlap
        WHERE extracted_window_start = :ws
    """, {"ws": window_start}).fetchone()["tgt_sum"] or 0.0

    delta   = round(abs(src_sum - tgt_sum), 4)
    c3_pass = delta <= 0.01
    print(f"C3 recon check: {'PASS' if c3_pass else 'FAIL'} (src={src_sum}, tgt={tgt_sum}, delta={delta})")
    if not c3_pass:
        all_pass = False

    print(f"Overall       : {'ALL PASS' if all_pass else 'FAILED'}")
    return all_pass

#-- Q5 (10 min)
#- State update rule:
#- if checks pass, update last_successful_run_at, last_max_invoice_id, last_run_status='SUCCESS'
#- else keep watermark values unchanged and set last_run_status='FAILED'
#- Implement this control logic in SQL statements/pseudocode comments.

def q5_conditional_state_update(conn, window_end, checks_pass):
    if checks_pass:
        max_id = conn.execute(
            "SELECT MAX(invoice_line_id) AS mx FROM training_fct_sales_overlap"
        ).fetchone()["mx"]

        conn.execute("""
            UPDATE training_etl_state_v2
            SET last_successful_run_at = :run_at,
                last_max_invoice_id    = :max_id,
                last_run_status        = 'SUCCESS'
            WHERE pipeline_name = 'sales_overlap_incremental'
        """, {"run_at": window_end, "max_id": max_id})

        print(f"Q5: watermark advanced to {window_end}")

    else:
        conn.execute("""
            UPDATE training_etl_state_v2
            SET last_run_status = 'FAILED'
            WHERE pipeline_name = 'sales_overlap_incremental'
        """)

        print("Q5: checks failed — watermark frozen, status set to FAILED")

    conn.commit()


checks_pass = q4_quality_checks(conn, window_start, window_end)
q5_conditional_state_update(conn, window_end, checks_pass)
conn.close()