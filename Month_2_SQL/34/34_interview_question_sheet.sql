-- Day 34 Interview Question Sheet (Chinook)
-- Timebox: 120 minutes total
-- DB: chinook.db
-- Rules: Solve Section A without looking at Section B answer key file.

-- =============================
-- Section A: Interview Prompts
-- =============================

-- Q1 (Easy): Count customers per country
-- Expected output columns: Country, customer_count
-- Sort: customer_count DESC
-- Timebox: 10 min
SELECT
    Country,
    COUNT(*) AS customer_count
FROM customers
GROUP BY Country
ORDER BY customer_count DESC;


-- Q2 (Easy): Top 5 customers by total spend
-- Expected output columns: CustomerId, FirstName, LastName, total_spent
-- Sort: total_spent DESC, limit 5
-- Timebox: 10 min
SELECT
    c.CustomerId,
    c.FirstName,
    c.LastName,
    ROUND(SUM(i.Total), 2) AS total_spent
FROM customers c
JOIN invoices i
    ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId, c.FirstName, c.LastName
ORDER BY total_spent DESC
LIMIT 5;


-- Q3 (Medium): Top 3 customers per country using ROW_NUMBER
-- Expected output columns: Country, CustomerId, FirstName, LastName, total_spent, rn
-- Sort: Country ASC, rn ASC
-- Timebox: 20 min
WITH customer_spend AS (
    SELECT
        c.Country,
        c.CustomerId,
        c.FirstName,
        c.LastName,
        ROUND(SUM(i.Total), 2) AS total_spent
    FROM customers c
    JOIN invoices i
        ON c.CustomerId = i.CustomerId
    GROUP BY c.Country, c.CustomerId, c.FirstName, c.LastName
), ranked AS (
    SELECT
        Country,
        CustomerId,
        FirstName,
        LastName,
        total_spent,
        ROW_NUMBER() OVER (
            PARTITION BY Country
            ORDER BY total_spent DESC
        ) AS rn
    FROM customer_spend
)
SELECT
    Country,
    CustomerId,
    FirstName,
    LastName,
    total_spent,
    rn
FROM ranked
WHERE rn <= 3
ORDER BY Country, rn;


-- Q4 (Medium): Monthly revenue with LAG and MoM change
-- Expected output columns: month, revenue, prev_month_revenue, mom_change, mom_pct_change
-- Sort: month ASC
-- Timebox: 20 min
WITH monthly AS (
    SELECT
        strftime('%Y-%m', InvoiceDate) AS month,
        ROUND(SUM(Total), 2) AS revenue
    FROM invoices
    GROUP BY month
)
SELECT
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(
        revenue - LAG(revenue, 1) OVER (ORDER BY month),
        2
    ) AS mom_change,
    ROUND(
        100.0 * (revenue - LAG(revenue, 1) OVER (ORDER BY month))
        / NULLIF(LAG(revenue, 1) OVER (ORDER BY month), 0),
        2
    ) AS mom_pct_change
FROM monthly
ORDER BY month;


-- Q5 (Hard): Best quarter per customer + spend tier using CASE WHEN
-- Expected output columns:
-- CustomerId, FirstName, LastName, best_quarter, quarterly_spend, total_spent, spend_tier
-- Timebox: 30 min
WITH customer_quarterly AS (
    SELECT
        c.CustomerId,
        c.FirstName,
        c.LastName,
        CASE
            WHEN CAST(strftime('%m', i.InvoiceDate) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
            WHEN CAST(strftime('%m', i.InvoiceDate) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
            WHEN CAST(strftime('%m', i.InvoiceDate) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
            ELSE 'Q4'
        END AS quarter,
        ROUND(SUM(i.Total), 2) AS quarterly_spend
    FROM customers c
    JOIN invoices i
        ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId, c.FirstName, c.LastName, quarter
), ranked_quarter AS (
    SELECT
        CustomerId,
        FirstName,
        LastName,
        quarter,
        quarterly_spend,
        ROW_NUMBER() OVER (
            PARTITION BY CustomerId
            ORDER BY quarterly_spend DESC
        ) AS rn
    FROM customer_quarterly
), total_spend AS (
    SELECT
        CustomerId,
        ROUND(SUM(Total), 2) AS total_spent
    FROM invoices
    GROUP BY CustomerId
)
SELECT
    rq.CustomerId,
    rq.FirstName,
    rq.LastName,
    rq.quarter AS best_quarter,
    rq.quarterly_spend,
    ts.total_spent,
    CASE
        WHEN ts.total_spent >= 45 THEN 'Platinum'
        WHEN ts.total_spent >= 35 THEN 'Gold'
        WHEN ts.total_spent >= 25 THEN 'Silver'
        ELSE 'Bronze'
    END AS spend_tier
FROM ranked_quarter rq
JOIN total_spend ts
    ON rq.CustomerId = ts.CustomerId
WHERE rq.rn = 1
ORDER BY ts.total_spent DESC;


-- =============================
-- Day 34 Self-Scoring
-- =============================
-- 1) Solved 5/5 queries under time limits: [ ]
-- 2) Explained one medium and one hard query verbally: [ ]
-- 3) Refactored alias/CTE names for readability: [ ]
-- 4) Commit and push done: [ ]
