# Day 36 Pre-Study Material (30-40 min max)

Use this before attempting the Day 36 question sheet.

## 1) Core Concepts You Must Know (10 min)

1. OLTP vs OLAP:
- OLTP: many small transactional writes, normalized tables, current operational state.
- OLAP: fewer but heavy analytical reads, denormalized/modeled structures, historical trend analysis.

2. Star schema basics:
- Fact table: numeric events at a fixed grain (for today: invoice line level).
- Dimension tables: descriptive attributes used for slicing (date, customer, track/product).
- Why it helps: simpler joins, faster BI queries, clearer business semantics.

3. Grain (critical):
- Always define grain before writing SQL.
- Today grain statement: one row per invoice item line.

## 2) Minimal SQL Patterns To Revise (10-15 min)

1. Create modeled tables:
```sql
DROP TABLE IF EXISTS training_dim_customer;
CREATE TABLE training_dim_customer AS
SELECT ...
FROM ...;
```

2. Build date key from date text in SQLite:
```sql
CAST(strftime('%Y%m%d', InvoiceDate) AS INTEGER) AS date_key
```

3. Robust metric math:
```sql
ROUND(SUM(quantity * unit_price), 2) AS gross_amount
```

4. Safe division:
```sql
SUM(x) / NULLIF(COUNT(y), 0)
```

## 3) Joins Map For Today (5 min)

1. Fact source:
- invoice_items -> invoices (for customer and invoice date)

2. Product dimension source:
- tracks -> albums -> artists
- tracks -> genres
- tracks -> media_types

3. Customer dimension source:
- customers

## 4) Validation Checklist (5 min)

Run these after modeling:

1. Fact row count:
```sql
SELECT COUNT(*) FROM training_fct_sales;
```

2. Revenue reconciliation:
```sql
SELECT ROUND(SUM(gross_amount), 2) FROM training_fct_sales;
SELECT ROUND(SUM(UnitPrice * Quantity), 2) FROM invoice_items;
```

3. Coverage check:
```sql
SELECT COUNT(DISTINCT customer_id) FROM training_fct_sales;
SELECT COUNT(DISTINCT CustomerId) FROM customers;
```

## 5) Interview Notes (optional 5 min)

Be ready to explain:

1. Why star schema is better for dashboards than normalized OLTP tables.
2. Why grain definition prevents double counting.
3. Why validation queries are mandatory in analytics engineering workflows.

## 6) Start Rule

Only start Day 36 timed questions after this is true:

- You can say the grain in one sentence.
- You can list all joins needed for training_dim_track.
- You know how to reconcile gross_amount totals.
