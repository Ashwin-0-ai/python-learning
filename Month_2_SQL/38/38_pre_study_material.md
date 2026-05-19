# Day 38 Pre-Study Material (30-40 min max)

Complete this before starting the timed question sheet.

## 1) Today’s Theme

Incremental loading and basic pipeline orchestration mindset.

By the end of Day 38, you should be able to:

1. Explain full refresh vs incremental load.
2. Build a watermark-based incremental fact load.
3. Upsert dimension-style changes with safe logic.
4. Write data quality checks that run after each load.
5. Document a simple daily orchestration flow.

## 2) Core Concepts To Revise (10-12 min)

1. Full refresh:
- Rebuilds entire target table every run.
- Easy to reason about.
- Expensive at scale.

2. Incremental load:
- Loads only new/changed data since last run.
- Requires state tracking (watermark).
- Faster and cheaper.

3. Watermark:
- A stored "last processed" value (timestamp, id, date key).
- Next run filters source rows > watermark.

4. Idempotency:
- Running the same pipeline twice should not duplicate data.
- Achieved with dedupe keys and MERGE/UPSERT logic.

## 3) SQL Patterns To Recall (10-12 min)

1. State table pattern:
```sql
CREATE TABLE IF NOT EXISTS training_etl_state (
  pipeline_name TEXT PRIMARY KEY,
  last_invoice_id INTEGER,
  last_run_at TEXT
);
```

2. Read watermark safely:
```sql
COALESCE((SELECT last_invoice_id FROM training_etl_state WHERE pipeline_name = 'sales_incremental'), 0)
```

3. Incremental extraction:
```sql
SELECT *
FROM invoices
WHERE InvoiceId > <watermark>;
```

4. Upsert in SQLite pattern:
```sql
INSERT INTO target_table (...)
SELECT ...
ON CONFLICT(key_col) DO UPDATE SET ...;
```

## 4) Orchestration Thinking (5-8 min)

For each run, follow this order:

1. Read watermark.
2. Extract incremental source rows.
3. Transform and load to targets.
4. Run quality checks.
5. Update watermark only if checks pass.

## 5) Start Rule

Start the timed Day 38 sheet only if:

1. You can explain how a bad watermark can cause data loss.
2. You can name one dedupe key for fact loading.
3. You can describe idempotency in one line.
