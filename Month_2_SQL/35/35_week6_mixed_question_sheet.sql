-- Day 35 Week 6 Review: Mixed SQL Timed Set (Chinook)
-- Timebox: 120 minutes total
-- DB: chinook.db
-- Rule: Attempt all questions before opening answer key.

-- =====================================
-- Section A: Timed Interview Practice
-- =====================================

-- Q1 (Easy, 10 min)
-- Top 10 tracks by total revenue.
-- Expected columns: TrackId, Name, total_revenue
-- Sort: total_revenue DESC
SELECT
    t.TrackId,
    t.Name,
    ROUND(SUM(il.UnitPrice * il.Quantity), 2) AS total_revenue
FROM invoice_items il
JOIN tracks t
    ON il.TrackId = t.TrackId
GROUP BY t.TrackId, t.Name
ORDER BY total_revenue DESC
LIMIT 10;


-- Q2 (Easy-Medium, 15 min)
-- Country-level KPIs: customers, invoices, revenue.
-- Expected columns: Country, customer_count, invoice_count, total_revenue, avg_revenue_per_customer
-- Sort: total_revenue DESC
SELECT
    c.Country,
    COUNT(DISTINCT c.CustomerId) AS customer_count,
    COUNT(DISTINCT i.InvoiceId) AS invoice_count,
    ROUND(SUM(i.Total), 2) AS total_revenue,
    ROUND(SUM(i.Total) / NULLIF(COUNT(DISTINCT c.CustomerId), 0), 2) AS avg_revenue_per_customer
FROM customers c
LEFT JOIN invoices i
    ON c.CustomerId = i.CustomerId
GROUP BY c.Country
ORDER BY total_revenue DESC;


-- Q3 (Medium, 20 min)
-- Monthly revenue with running total and 3-month moving average.
-- Expected columns: month, revenue, running_revenue, moving_avg_3m
-- Sort: month ASC
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
    ROUND(
        SUM(revenue) OVER (
            ORDER BY month
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS running_revenue,
    ROUND(
        AVG(revenue) OVER (
            ORDER BY month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moving_avg_3m
FROM monthly
ORDER BY month;


-- Q4 (Medium, 20 min)
-- For each genre, return top 2 customers by spend.
-- Expected columns: GenreId, GenreName, CustomerId, CustomerName, genre_spend, rn
-- Sort: GenreName ASC, rn ASC
WITH genre_customer_spend AS (
    SELECT
        g.GenreId,
        g.Name AS GenreName,
        c.CustomerId,
        c.FirstName || ' ' || c.LastName AS CustomerName,
        ROUND(SUM(il.UnitPrice * il.Quantity), 2) AS genre_spend
    FROM invoice_items il
JOIN invoices i
    ON il.InvoiceId = i.InvoiceId
JOIN customers c
    ON i.CustomerId = c.CustomerId
JOIN tracks t
    ON il.TrackId = t.TrackId
JOIN genres g
    ON t.GenreId = g.GenreId
    GROUP BY g.GenreId, g.Name, c.CustomerId, CustomerName
), ranked AS (
    SELECT
        GenreId,
        GenreName,
        CustomerId,
        CustomerName,
        genre_spend,
        ROW_NUMBER() OVER (
            PARTITION BY GenreId
            ORDER BY genre_spend DESC, CustomerId ASC
        ) AS rn
    FROM genre_customer_spend
)
SELECT
    GenreId,
    GenreName,
    CustomerId,
    CustomerName,
    genre_spend,
    rn
FROM ranked
WHERE rn <= 2
ORDER BY GenreName, rn;


-- Q5 (Hard, 25 min)
-- Customer retention proxy:
-- Mark each invoice as NEW if first invoice month for that customer, else RETURNING.
-- Then aggregate by month and customer_type.
-- Expected columns: month, customer_type, customer_count, revenue
-- Sort: month ASC, customer_type ASC
WITH invoice_months AS (
    SELECT
        i.InvoiceId,
        i.CustomerId,
        strftime('%Y-%m', i.InvoiceDate) AS month,
        i.Total,
        MIN(strftime('%Y-%m', i.InvoiceDate)) OVER (
            PARTITION BY i.CustomerId
        ) AS first_month
    FROM invoices i
), typed AS (
    SELECT
        month,
        CustomerId,
        Total,
        CASE
            WHEN month = first_month THEN 'NEW'
            ELSE 'RETURNING'
        END AS customer_type
    FROM invoice_months
)
SELECT
    month,
    customer_type,
    COUNT(DISTINCT CustomerId) AS customer_count,
    ROUND(SUM(Total), 2) AS revenue
FROM typed
GROUP BY month, customer_type
ORDER BY month, customer_type;


-- Q6 (Hard, 30 min)
-- Build a reusable customer segmentation output with CASE WHEN.
-- Segment rules based on total lifetime spend:
-- >= 40: Platinum | >= 30: Gold | >= 20: Silver | else Bronze
-- Also include invoice_count and avg_order_value.
-- Expected columns: CustomerId, CustomerName, total_spent, invoice_count, avg_order_value, segment
-- Sort: total_spent DESC
WITH customer_ltv AS (
    SELECT
        c.CustomerId,
        c.FirstName || ' ' || c.LastName AS CustomerName,
        ROUND(SUM(i.Total), 2) AS total_spent,
        COUNT(i.InvoiceId) AS invoice_count,
        ROUND(SUM(i.Total) / NULLIF(COUNT(i.InvoiceId), 0), 2) AS avg_order_value
    FROM customers c
    JOIN invoices i
        ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId, CustomerName
)
SELECT
    CustomerId,
    CustomerName,
    total_spent,
    invoice_count,
    avg_order_value,
    CASE
        WHEN total_spent >= 40 THEN 'Platinum'
        WHEN total_spent >= 30 THEN 'Gold'
        WHEN total_spent >= 20 THEN 'Silver'
        ELSE 'Bronze'
    END AS segment
FROM customer_ltv
ORDER BY total_spent DESC;


-- ========================
-- Day 35 Self-Scoring
-- ========================
-- 1) Completed all 6 queries within 120 minutes: [ ]
-- 2) Correct use of at least one window frame clause: [ ]
-- 3) One clean CTE chain with readable aliases: [ ]
-- 4) Commit and push done: [ ]
