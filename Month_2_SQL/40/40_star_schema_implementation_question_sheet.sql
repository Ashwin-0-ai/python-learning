-- Day 40: Implement a Star Schema for Analytics Reporting (Question Sheet Only)
-- Timebox: 120 minutes total
-- Mode: Attempt-first, no answer key.
-- Data source: chinook.db

-- ==================================================
-- Study First (Required)
-- ==================================================
-- Read: 40_pre_study_material.md (30-40 min max)
-- Start timed blocks only after passing the Start Rule.

-- ==================================================
-- Session Outcome (today)
-- ==================================================
-- 1) You can define and implement a fact table at invoice-line grain.
-- 2) You can model dimensions for reporting and filtering.
-- 3) You can validate joins and prove business usefulness with KPI queries.


-- ==================================================
-- Block A (0-20 min): Design Notes (write in comments)
-- ==================================================
-- A1) Write the grain of your sales fact table in one sentence.
-- A. g The grain of the sales fact table is at the invoice line level, meaning each record represents a single line item on an invoice, capturing details such as the specific track sold, quantity, unit price, and associated customer and date information.

-- A2) List the dimensions you will build and why each one matters.
-- A. g 1) Date Dimension: This allows for time-based analysis, enabling trends and seasonality to be identified in sales data. 
        2) Customer Dimension: This provides insights into customer demographics and purchasing behavior, which is crucial for targeted marketing and customer relationship management.
        3) Track Dimension: This captures details about the products being sold (tracks), allowing for analysis of sales performance by genre, artist, and media type, which can inform inventory and promotional strategies.

-- A3) Name 3 business questions your star schema should answer.
-- A. g 1) What is the monthly revenue trend over the past year?
        2) Who are the top 5 customers by total gross amount spent?
        3) Which music genres are generating the most revenue?

-- A4) What is one risk if you skip grain definition before building the fact table?
-- A. g Skipping grain definition can lead to a fact table that is too aggregated or too detailed, which can cause issues with data accuracy and performance. For example, if the grain is not clearly defined, you might end up with duplicate records or incorrect aggregations, making it difficult to derive meaningful insights from the data.


-- ==================================================
-- Block B (20-85 min): Build the Star Schema (timed)
-- ==================================================
-- Naming rule: prefix all artifacts with training_.

-- Q1 (10 min)
-- Create a date dimension from invoice dates.
-- Table: training_dim_date
-- Required columns:
--   date_key, calendar_date, year, month, month_name, quarter

-- TODO: Write your SQL here


-- Q2 (10 min)
-- Create a customer dimension from customers.
-- Table: training_dim_customer
-- Required columns:
--   customer_key, customer_id, full_name, country, city, company

-- TODO: Write your SQL here


-- Q3 (15 min)
-- Create a track dimension by joining tracks, albums, artists, genres, and media_types.
-- Table: training_dim_track
-- Required columns:
--   track_key, track_id, track_name, album_title, artist_name, genre_name, media_type_name, unit_price

-- TODO: Write your SQL here


-- Q4 (20 min)
-- Create the fact table at invoice-line grain.
-- Table: training_fct_sales
-- Required columns:
--   sales_key, invoice_line_id, invoice_id, customer_id, track_id, date_key,
--   quantity, unit_price, gross_amount
-- Rule:
--   gross_amount = quantity * unit_price

-- TODO: Write your SQL here



-- ==================================================
-- Block C (85-110 min): KPI Queries and Reporting Proof
-- ==================================================
-- C1) Monthly revenue trend using training_fct_sales + training_dim_date.
-- C2) Top 5 customers by gross_amount using training_fct_sales + training_dim_customer.
-- C3) Revenue by genre using training_fct_sales + training_dim_track.
-- C4) One additional business query of your choice.

-- TODO: Write your SQL here


-- ==================================================
-- Block D (110-120 min): Modeling Reflection
-- ==================================================
-- D1) Why is invoice-line grain a strong fact grain for this dataset?
-- AD1. g Invoice-line grain is a strong fact grain for this dataset because it captures the most granular level of sales data, allowing for detailed analysis of each transaction. This granularity enables accurate aggregation and filtering across various dimensions (such as date, customer, and track), providing flexibility in reporting and insights generation. Additionally, it allows for precise calculation of key performance indicators (KPIs) like gross amount, which is essential for understanding revenue and profitability at a detailed level.

-- D2) Which dimension would you add next if this became a production model?
-- AD2. g If this became a production model, the next dimension I would add is a "Store Dimension" (or "Sales Channel Dimension") to capture information about where the sales are occurring (e.g., online, in-store, mobile app). This would allow for analysis of sales performance across different channels and help identify trends and opportunities for growth in specific sales avenues.

-- D3) What check would you automate first in an orchestration pipeline?
-- AD3. g The first check I would automate in an orchestration pipeline is a data quality check to ensure that there are no null values in critical fields such as customer_id, track_id, and date_key in the fact table. This is crucial because null values in these fields can lead to inaccurate reporting and analysis, and catching these issues early in the pipeline can prevent downstream errors and maintain the integrity of the data model.    


-- ==================================================
-- End-Of-Session Recap Questionnaire (Previous Day: Day 39)
-- ==================================================
-- 1) Why do overlap windows reduce risk in incremental pipelines?
A. g Overlap windows reduce risk in incremental pipelines by providing a buffer period during which data can be reprocessed without affecting the overall integrity of the dataset. This means that if there are any issues or errors during the initial load, the overlap window allows for a safe replay of the data without causing duplicates or inconsistencies in the final output. It essentially creates a safety net that ensures data quality and reliability, even in the face of unexpected failures or changes in the source data.

-- 2) What makes a backfill replay-safe?
A. g A backfill is considered replay-safe when it can be executed multiple times without causing duplicate records or inconsistencies in the data. This typically involves implementing idempotent logic, such as using unique keys or timestamps to ensure that only new or updated records are processed during each run. Additionally, maintaining a state or checkpoint system can help track which data has already been processed, further ensuring that replays do not lead to data integrity issues.

-- 3) Why is dedupe logic required during reruns?
A. g Dedupe logic is required during reruns to prevent the creation of duplicate records in the dataset. When a pipeline is rerun, especially in cases of backfills or overlap windows, there is a risk that the same data may be processed multiple times. Dedupe logic helps to identify and eliminate these duplicates, ensuring that the final dataset remains accurate and consistent. This is crucial for maintaining data integrity and providing reliable insights from the data.

-- 4) What state fields did you track on Day 39?
A. g On Day 39, I tracked state fields such as the last processed timestamp, the highest ID processed, and a status flag to indicate whether the last run was successful or if it encountered errors. These fields help in managing the incremental load process by providing a clear record of what data has been processed and allowing for safe replays if necessary.

-- 5) Why should state update happen only after quality checks pass?
A. g State updates should happen only after quality checks pass to ensure that the pipeline's state accurately reflects the successful processing of data. If the state is updated before quality checks, there is a risk that the pipeline may mark data as processed even if it contains errors or inconsistencies. This can lead to inaccurate reporting and analysis, as well as difficulties in troubleshooting and correcting issues later on. By updating the state only after quality checks pass, you maintain the integrity of the data and ensure that any necessary reprocessing can be done safely without affecting downstream systems.

-- 6) What reconciliation check did you use yesterday?
A. g The reconciliation check I used yesterday was a record count comparison between the source and target tables after the incremental load. This involved comparing the number of records processed in the source with the number of records inserted or updated in the target to ensure that all expected data was accounted for and that there were no discrepancies.

-- 7) What part of Day 39 was most difficult?
A. g The most difficult part of Day 39 was implementing the dedupe logic during reruns, as it required careful consideration of the unique identifiers and timestamps to ensure that duplicates were effectively eliminated without accidentally removing valid records. It was a challenge to design the logic in a way that would work seamlessly during both normal runs and backfills, while also maintaining the integrity of the dataset.

-- 8) Rate Day 39 confidence (1-10) for building replay-safe incremental loads.
A. g I would rate my confidence for building replay-safe incremental loads at an 8. I feel comfortable with the concepts and have a good understanding of the necessary checks and logic to implement, but I recognize that there may still be edge cases or complexities that could arise in a production environment that I haven't fully encountered yet.



-- ==================================================
-- Self-Scoring
-- ==================================================
-- [ ] Completed all timed blocks in 120 min
-- [ ] Built at least 3 dimensions and 1 fact table
-- [ ] Validated joins and foreign keys
-- [ ] Ran at least 3 KPI queries on the finished model
-- [ ] Completed Day 39 recap questionnaire
