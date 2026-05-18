-- Day 37: SCD Modeling and Fact Alignment (Question Sheet Only)
-- Timebox: 120 minutes total
-- Mode: Attempt-first, no answer key.
-- Data source: chinook.db

-- ==================================================
-- Study First (Required)
-- ==================================================
-- Read: 37_pre_study_material.md (30-40 min max)
-- Start timed blocks only after passing the Start Rule.

-- ==================================================
-- Session Outcome (today)
-- ==================================================
-- 1) You can design SCD1 and SCD2 customer dimensions.
-- 2) You can align fact rows to correct customer version.
-- 3) You can run quality checks for versioned dimensions.


-- ==================================================
-- Block A (0-20 min): Concept Warmup (write in comments)
-- ==================================================
-- A1) In 4 lines, compare SCD1 vs SCD2.
SCD 1 is when you dont want to use old attribute values for historical analysis. SCD 2 is when you want to keep history of attribute changes and use old values for historical analysis. SCD 1 is easier to implement and maintain, but SCD 2 provides more accurate historical analysis. SCD 1 is suitable for attributes that do not change frequently, while SCD 2 is suitable for attributes that change frequently and are important for analysis.
-- A2) Which customer attributes in Chinook would you treat as SCD2 and why?
I would treat city and company as SCD 2 attributes because they can change over time and are important for analysis. For example, if a customer moves to a different city or changes their company, we would want to keep track of that history for accurate analysis of customer behavior and revenue by city and company.
-- A3) Write the fact grain for today in one sentence.
The fact grain for today is at the invoice line level, where each row represents a single invoice line item with its associated customer and track information, along with the date of the invoice and the revenue generated from that line item.
-- A4) Why can wrong SCD join logic inflate revenue?
Wrong SCD join logic can inflate revenue because if you join fact rows to the wrong version of the customer dimension (e.g., using a current version instead of the correct historical version), you may attribute revenue to the wrong customer attributes (e.g., city or company). This can lead to overestimating revenue for certain segments or time periods, as you may be counting revenue that should be associated with a different customer version. Additionally, if you have multiple versions of a customer and your join logic does not correctly filter for the appropriate effective date range, you could end up counting the same revenue multiple times across different versions.


-- ==================================================
-- Block B (20-85 min): Build Tables (timed)
-- ==================================================
-- Naming rule: prefix training_ for all tables.

-- Q1 (15 min)
-- Create a source snapshot table for customers.
-- Table: training_stg_customer_snapshot
-- Required columns:
--   snapshot_date, customer_id, first_name, last_name, company, city, country, email
-- Task detail:
--   create at least 2 snapshot dates (simulate change in city or company for a few customers).

-- TODO: Write your SQL here


-- Q2 (15 min)
-- Build SCD Type 1 dimension from latest snapshot.
-- Table: training_dim_customer_scd1
-- Required columns:
--   customer_key, customer_id, full_name, company, city, country, email, updated_at
-- Rule:
--   one row per customer_id using latest snapshot only.

-- TODO: Write your SQL here


-- Q3 (20 min)
-- Build SCD Type 2 dimension from snapshot history.
-- Table: training_dim_customer_scd2
-- Required columns:
--   customer_sk, customer_id, full_name, company, city, country, email,
--   effective_from, effective_to, is_current
-- Rules:
--   1) Keep version history per customer_id.
--   2) Exactly one current row per customer_id.
--   3) Close old rows with effective_to.

-- TODO: Write your SQL here


-- Q4 (15 min)
-- Build a fact table at invoice line grain using existing invoice/invoice_items.
-- Table: training_fct_sales_v2
-- Required columns:
--   sales_key, invoice_line_id, invoice_id, customer_id, track_id, fact_date,
--   quantity, unit_price, gross_amount

-- TODO: Write your SQL here


-- Q5 (15 min)
-- Create a view/table that joins fact rows to SCD2 customer versions.
-- Table or view name: training_mart_sales_customer
-- Join condition must include business key + date-range validity.
-- Output columns:
--   invoice_id, invoice_line_id, fact_date, customer_id, customer_sk, city, country, gross_amount

-- TODO: Write your SQL here


-- ==================================================
-- Block C (85-110 min): Validation and Analysis
-- ==================================================
-- C1) Check no duplicate current SCD2 rows per customer_id.
-- C2) Check no overlapping effective date windows per customer_id.
-- C3) Top 10 cities by gross_amount from training_mart_sales_customer.
-- C4) Compare revenue by country using SCD1 vs SCD2 output and note one difference.

-- TODO: Write your SQL here


-- ==================================================
-- Block D (110-120 min): Reflection
-- ==================================================
-- D1) Where did your SCD2 logic break first?
-- D2) How did you verify current-row correctness?
-- D3) What will you automate on Day 38?


-- ==================================================
-- End-Of-Session Recap Questionnaire (Previous Day: Day 36)
-- ==================================================
-- 1) Define fact grain from Day 36 in one sentence.
-- 2) Why was date_key useful in your Day 36 model?
-- 3) Name the 3 dimensions you built and one column from each.
-- 4) Which validation query gave you the most confidence and why?
-- 5) What is one common reason totals mismatch between fact and source?
-- 6) In star schema terms, why avoid storing too much text in fact tables?
-- 7) What was your biggest Day 36 bottleneck?
-- 8) Rate Day 36 confidence (1-10) for building a simple warehouse model from scratch.


-- ==================================================
-- Self-Scoring
-- ==================================================
-- [ ] Completed all timed blocks in 120 min
-- [ ] Built SCD1 and SCD2 tables
-- [ ] Implemented date-range fact-to-SCD2 join
-- [ ] Completed Day 36 recap questionnaire
