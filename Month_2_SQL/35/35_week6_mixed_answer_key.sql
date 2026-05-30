-- Day 35 Week 6 Review: Answer Key (Chinook)
-- Use only after attempting the question sheet.

-- Q1
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

-- Q2
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

-- Q3
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

-- Q4
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

-- Q5
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

-- Q6
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
