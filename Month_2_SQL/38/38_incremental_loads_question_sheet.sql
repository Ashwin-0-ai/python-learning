-- Day 38: Incremental Loads and Basic Orchestration (Question Sheet Only)
-- Timebox: 120 minutes total
-- Mode: Attempt-first, no answer key.
-- Data source: chinook.db

-- ==================================================
-- Study First (Required)
-- ==================================================
-- Read: 38_pre_study_material.md (30-40 min max)
-- Start timed blocks only after passing the Start Rule.

-- ==================================================
-- Session Outcome (today)
-- ==================================================
-- 1) You can design a watermark-driven incremental pipeline.
-- 2) You can load incremental fact rows without duplicates.
-- 3) You can write post-load quality checks and update pipeline state safely.


-- ==================================================
-- Block A (0-20 min): Pipeline Design Notes (write in comments)
-- ==================================================
-- A1) Compare full refresh vs incremental load in 4 lines.
A full refresh reloads all data from the source, while an incremental load only processes new or changed data since the last load. Full refreshes can be simpler but are less efficient for large datasets, whereas incremental loads require more complex logic to track changes but are faster and more resource-efficient. Incremental loads often rely on a watermark (e.g., last updated timestamp or max ID) to identify new data, while full refreshes do not need this mechanism.
-- A2) What should be your watermark for today and why?
The watermark for today should be the last_invoice_id from the training_etl_state table because it allows us to track the highest invoice_id that has been processed in previous runs. This way, we can ensure that we only load new invoice lines with invoice_id greater than the last processed one, making our incremental load efficient and avoiding duplicates.
-- A3) Define idempotency in one sentence.
Idempotency is the property of a process that allows it to be executed multiple times without changing the result beyond the initial application, ensuring that reruns do not create duplicates or unintended side effects.
-- A4) List 3 failure modes in incremental pipelines.
1) Duplicate data due to missing or incorrect watermark updates.
2) Data loss if the watermark is set incorrectly, causing new data to be skipped.   
3) Inconsistent state if the pipeline fails after loading data but before updating the watermark, leading to potential reprocessing of the same data on the next run.


-- ==================================================
-- Block B (20-85 min): Build Incremental Framework (timed)
-- ==================================================
-- Naming rule: prefix all artifacts with training_.

-- Q1 (10 min)
-- Create pipeline state table.
-- Table: training_etl_state
-- Required columns:
--   pipeline_name (PK), last_invoice_id, last_run_at
-- Insert one initial row for pipeline_name = 'sales_incremental' if missing.

-- TODO: Write your SQL here


-- Q2 (15 min)
-- Create target incremental fact table.
-- Table: training_fct_sales_incremental
-- Required columns:
--   invoice_line_id (unique key), invoice_id, customer_id, track_id,
--   invoice_date, quantity, unit_price, gross_amount, loaded_at
-- Add uniqueness so reruns do not duplicate rows.

-- TODO: Write your SQL here


-- Q3 (20 min)
-- Write incremental load SQL using watermark from training_etl_state.
-- Load only rows with invoice_id > last_invoice_id.
-- Populate gross_amount and loaded_at.
-- Ensure idempotent behavior (no duplicates on rerun).

-- TODO: Write your SQL here


-- Q4 (10 min)
-- Update watermark after load.
-- Rule:
--   set last_invoice_id to MAX(invoice_id) from target table for this pipeline.
--   set last_run_at to current timestamp.
-- Only do this after quality checks pass.

-- TODO: Write your SQL here


-- Q5 (10 min)
-- Simulate a second run and prove no duplicate inserts happen.
-- Provide one query showing duplicate count by invoice_line_id is zero.

-- TODO: Write your SQL here


-- ==================================================
-- Block C (85-110 min): Data Quality and Monitoring Queries
-- ==================================================
-- C1) Row count loaded in this run (hint: use loaded_at window if needed).
-- C2) Reconcile incremental gross_amount vs source gross_amount for loaded invoice_id range.
-- C3) Null checks on key fields (invoice_line_id, invoice_id, customer_id, track_id).
-- C4) Top 5 customers by gross_amount from incremental table.

-- TODO: Write your SQL here


-- ==================================================
-- Block D (110-120 min): Orchestration Reflection
-- ==================================================
-- D1) Write a 6-step pseudo DAG for this pipeline.
-- D2) At which step should pipeline fail-fast?
-- D3) What alert metric would you track first in production?


-- ==================================================
-- End-Of-Session Recap Questionnaire (Previous Day: Day 37)
-- ==================================================
-- 1) What is the key difference between SCD1 and SCD2 in one line?
SCD1 overwrites old values, while SCD2 creates new rows to preserve history.
-- 2) Why do SCD2 tables need effective_from and effective_to?
They define the time range during which each row version is valid, allowing you to track changes over time.
-- 3) What does is_current help you filter quickly?
It allows you to quickly filter for the most recent version of each row without checking date ranges.
-- 4) Why can joining fact to SCD2 without date logic be wrong?
It can lead to incorrect results by joining to multiple versions of the dimension row, causing duplicates or mismatches.
-- 5) Name one validation check to catch SCD2 data quality issues.
One check is to ensure that there are no overlapping effective date ranges for the same natural key, which would indicate data integrity issues.
-- 6) When would you still choose SCD1 for a field?
You might choose SCD1 for a field that is not critical for historical analysis and where you only care about the current value, such as a non-analytical attribute or a field that changes frequently without needing to track history.
-- 7) What was your hardest part in Day 37 implementation?
The hardest part was ensuring the correct handling of effective dates and maintaining data integrity when inserting new versions of rows in the SCD2 table, especially when dealing with updates to existing records.
-- 8) Rate Day 37 confidence (1-10) for building versioned dimensions.
I would rate my confidence as an 7 for building versioned dimensions after completing Day 37's exercises and understanding the concepts of SCD1 and SCD2.


-- ==================================================
-- Self-Scoring
-- ==================================================
-- [ ] Completed all timed blocks in 120 min
-- [ ] Implemented watermark + incremental load
-- [ ] Verified idempotent rerun behavior
-- [ ] Completed Day 37 recap questionnaire
