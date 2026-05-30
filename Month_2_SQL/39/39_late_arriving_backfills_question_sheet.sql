-- Day 39: Late-Arriving Data and Backfill-Safe Incremental Loads (Question Sheet Only)
-- Timebox: 120 minutes total
-- Mode: Attempt-first, no answer key.
-- Data source: chinook.db

-- ==================================================
-- Study First (Required)
-- ==================================================
-- Read: 39_pre_study_material.md (30-40 min max)
-- Start timed blocks only after passing the Start Rule.

-- ==================================================
-- Session Outcome (today)
-- ==================================================
-- 1) You can design overlap-window incremental extraction.
-- 2) You can rerun loads safely without duplicate fact rows.
-- 3) You can validate and control backfill quality before committing state.


-- ==================================================
-- Block A (0-20 min): Design Notes (write in comments)
-- ==================================================
-- A1) In 4 lines, explain why strict watermark-only extraction can miss data.
A. Strict watermark-only extraction relies on the assumption that all relevant data arrives in order and on time. However, if there are late-arriving records (e.g., due to upstream delays or corrections), they may have timestamps earlier than the last successful run, causing them to be missed entirely. This can lead to incomplete datasets and inaccurate reporting. An overlap window allows for reprocessing a recent time range to capture any late-arriving data, mitigating this risk.
-- A2) Propose an overlap window for this dataset and justify your choice.
A. For the chinook dataset, an overlap window of 7 days could be appropriate. This means that each incremental load would reprocess data from the last 7 days, which is a reasonable timeframe to capture any late-arriving records without causing excessive duplication. This window size balances the need to catch late data while minimizing the amount of redundant processing and potential duplicates.
-- A3) Define replay-safe load behavior in one sentence.
A. Replay-safe load behavior ensures that rerunning the same load process does not create duplicate records or corrupt existing data, allowing for safe reprocessing in case of failures or backfills.
-- A4) List 3 production risks when running backfills.
A. 1) Data duplication: Backfills can create duplicate records if not handled properly, leading to inflated metrics and inaccurate reporting. 
   2) State corruption: If the backfill process updates state (e.g., watermarks) before validation, it can corrupt the pipeline's state and cause future loads to miss data. 
   3) Performance degradation: Backfilling large volumes of data can strain system resources and impact the performance of regular incremental loads, potentially causing delays or failures in production.


-- ==================================================
-- Block B (20-85 min): Build Replay-Safe Incremental + Overlap (timed)
-- ==================================================
-- Naming rule: prefix all artifacts with training_.

-- Q1 (10 min)
-- Create/extend pipeline state table to support overlap strategy.
-- Table: training_etl_state_v2
-- Required columns:
--   pipeline_name (PK), last_successful_run_at, overlap_days, last_max_invoice_id, last_run_status
-- Insert one initial row for pipeline_name = 'sales_overlap_incremental' if missing.

-- TODO: Write your SQL here


-- Q2 (15 min)
-- Create target table for overlap loads.
-- Table: training_fct_sales_overlap
-- Required columns:
--   invoice_line_id (unique key), invoice_id, customer_id, track_id,
--   invoice_date, quantity, unit_price, gross_amount,
--   extracted_window_start, extracted_window_end, loaded_at

-- TODO: Write your SQL here


-- Q3 (20 min)
-- Write incremental extraction + load SQL using overlap logic.
-- Rules:
--   1) derive window_start from last_successful_run_at minus overlap_days.
--   2) window_end is current timestamp.
--   3) load invoice rows where InvoiceDate is between window_start and window_end.
--   4) apply idempotent upsert behavior on invoice_line_id.

-- TODO: Write your SQL here


-- Q4 (10 min)
-- Write post-load checks.
-- C1) duplicate check on invoice_line_id must be zero.
-- C2) null checks on key columns.
-- C3) reconciliation: compare SUM(gross_amount) between source and target for current window.

-- TODO: Write your SQL here


-- Q5 (10 min)
-- State update rule:
--   if checks pass, update last_successful_run_at, last_max_invoice_id, last_run_status='SUCCESS'
--   else keep watermark values unchanged and set last_run_status='FAILED'
-- Implement this control logic in SQL statements/pseudocode comments.

-- TODO: Write your SQL here


-- ==================================================
-- End-Of-Session Recap Questionnaire (Previous Day: Day 38)
-- ==================================================
-- 1) What is incremental load in one line?
A. Incremental load is a data processing technique that extracts and loads only the new or changed records since the last successful run, rather than reprocessing the entire dataset.
-- 2) Why is watermark state needed?
A. Watermark state is needed to track the last successful extraction point (e.g., timestamp or max ID) so that subsequent incremental loads can efficiently identify and process only the new or updated records, ensuring data freshness while minimizing processing time and resource usage.
-- 3) What makes a load idempotent?
A. A load is idempotent if it can be run multiple times without causing unintended side effects, such as creating duplicate records or corrupting existing data. This typically involves using unique keys and upsert logic to ensure that reprocessing the same data does not alter the final state beyond the intended outcome.
-- 4) Why should watermark update happen only after checks pass?
A. Watermark updates should happen only after checks pass to ensure that the pipeline's state accurately reflects the last successful load. If the watermark is updated before validation, it could lead to missed data in future runs if the current load fails or produces incorrect results, as the pipeline would assume that all data up to the new watermark has been successfully processed.
-- 5) Name one duplicate-prevention key from Day 38 implementation.
A. One duplicate-prevention key from Day 38 implementation is the invoice_line_id, which serves as a unique identifier for each record in the sales data, allowing for idempotent upsert operations to prevent duplicates during incremental loads and backfills.
-- 6) What is one quality check you used on Day 38 and why?
A. One quality check used on Day 38 was the reconciliation of total gross_amount between the source and target for the current load window. This check is important because it helps ensure that the data has been accurately extracted and loaded without any loss or duplication, providing confidence in the integrity of the loaded data before updating the pipeline state.
-- 7) What was your biggest Day 38 bottleneck?
A. The biggest bottleneck on Day 38 was designing the idempotent upsert logic to handle potential duplicates during incremental loads, as it required careful consideration of the unique keys and how to manage state updates without causing data corruption.
-- 8) Rate Day 38 confidence (1-10) for building a watermark pipeline.
A. I would rate my confidence for building a watermark pipeline at an 7, as I have a solid understanding of the concepts and have successfully implemented incremental loads with watermark state management, but I recognize that there are always edge cases and optimizations to consider in a production environment.


-- ==================================================
-- Self-Scoring
-- ==================================================
-- [ ] Completed all timed blocks in 120 min
-- [ ] Built overlap-window incremental logic
-- [ ] Designed backfill-safe rerun strategy
-- [ ] Completed Day 38 recap questionnaire
