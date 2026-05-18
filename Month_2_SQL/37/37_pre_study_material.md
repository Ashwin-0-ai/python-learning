# Day 37 Pre-Study Material (30-40 min max)

Complete this before opening the timed sheet.

## 1) What You Are Learning Today

1. Dimensional modeling decisions after staging.
2. SCD Type 1 vs SCD Type 2 for customer attributes.
3. Building a fact table that can work with SCD dimensions.
4. Basic incremental-load thinking (not full production ELT yet).

## 2) Concepts To Revise (10-12 min)

1. SCD Type 1:
- Overwrite old values.
- No history.
- Best for corrected/non-historical attributes.

2. SCD Type 2:
- Keep history by versioning rows.
- Add effective_from, effective_to, is_current.
- Best when business needs point-in-time analysis.

3. Surrogate key vs business key:
- business key: source identifier (example: customer_id).
- surrogate key: warehouse-generated row identifier for dimensions.

4. Fact-to-dimension join rule:
- Join facts to the correct dimension version using date conditions for SCD2.

## 3) SQL Patterns To Recall (10-12 min)

1. Window ranking for latest version:
```sql
ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY snapshot_date DESC)
```

2. Current-row filter pattern:
```sql
WHERE is_current = 1
```

3. Date-range join idea for SCD2:
```sql
fact_date >= effective_from
AND (effective_to IS NULL OR fact_date < effective_to)
```

4. Data quality checks:
- duplicate current rows per business key
- null business keys
- count reconciliation after joins

## 4) Practical Modeling Checklist (5-8 min)

Before starting timer, write these 4 lines in your notes:

1. Fact grain = one row per invoice line item.
2. Customer business key = CustomerId.
3. SCD2 validity columns = effective_from, effective_to, is_current.
4. Join safety rule = never join fact directly to non-versioned history table without date condition.

## 5) Start Rule

Start Day 37 timed work only if:

1. You can explain SCD1 vs SCD2 in under 30 seconds.
2. You can describe one real attribute that should be SCD2.
3. You can write a date-range join from memory.
