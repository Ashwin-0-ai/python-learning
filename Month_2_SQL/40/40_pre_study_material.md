# Day 40 Pre-Study Material (30-40 min max)

Complete this before starting the timed question sheet.

## 1) Today's Theme

Star schema implementation for analytics workloads.

By the end of Day 40, you should be able to:

1. Define the grain of a fact table before writing SQL.
2. Separate descriptive attributes into dimensions and numeric events into a fact table.
3. Build a simple star schema from transactional source tables.
4. Validate referential joins between fact and dimensions.
5. Prove the model is useful with KPI queries.

## 2) Core Concepts To Revise (10-12 min)

1. Fact table grain:
- The grain is the meaning of one row.
- You must define it first or the model becomes inconsistent.
- For Chinook sales, a strong default grain is one row per invoice line.

2. Dimension table:
- Stores descriptive context used for filtering, grouping, and labeling.
- Examples: customer, track, date.
- Dimensions should be stable and readable.

3. Fact table:
- Stores measurable events.
- Examples: quantity, unit_price, gross_amount.
- Facts usually contain foreign keys to dimensions.

4. Star schema:
- One central fact table surrounded by dimension tables.
- Improves reporting clarity and makes KPI queries easier to reason about.

## 3) SQL Patterns To Recall (10-12 min)

1. Date key pattern:
```sql
CAST(strftime('%Y%m%d', InvoiceDate) AS INTEGER) AS date_key
```

2. Fact grain pattern:
```sql
SELECT
  ii.InvoiceLineId AS sales_key,
  ii.InvoiceId,
  ii.TrackId,
  i.CustomerId,
  ii.Quantity,
  ii.UnitPrice,
  ii.Quantity * ii.UnitPrice AS gross_amount
FROM invoice_items ii
JOIN invoices i
  ON ii.InvoiceId = i.InvoiceId;
```

3. Referential check pattern:
```sql
SELECT COUNT(*)
FROM fct_sales f
LEFT JOIN dim_customer d
  ON f.customer_id = d.customer_id
WHERE d.customer_id IS NULL;
```

4. KPI query pattern:
```sql
SELECT
  d.year,
  d.month,
  ROUND(SUM(f.gross_amount), 2) AS revenue
FROM fct_sales f
JOIN dim_date d
  ON f.date_key = d.date_key
GROUP BY d.year, d.month;
```

## 4) Modeling Rules For Today (5-8 min)

Follow this order:

1. Write the fact grain in one sentence.
2. Build dimensions first.
3. Build the fact table second.
4. Validate counts and joins.
5. Run 2 KPI queries before calling the model complete.

## 5) Suggested Minimum Star Schema

Build at least these tables:

1. `training_dim_date`
2. `training_dim_customer`
3. `training_dim_track`
4. `training_fct_sales`

If time remains, add one optional dimension only if it clearly improves reporting.

## 6) Start Rule

Start the timed Day 40 sheet only if:

1. You can state the grain of the fact table in one line.
2. You can explain the difference between a fact and a dimension.
3. You can name 2 KPI queries the finished model should support.
