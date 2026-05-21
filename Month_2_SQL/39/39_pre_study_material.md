# Day 39 Pre-Study Material (30-40 min max)

Complete this before starting the timed question sheet.

## 1) Today's Theme

Late-arriving data, replay-safe backfills, and partition-style incremental strategy.

By the end of Day 39, you should be able to:

1. Explain why late-arriving rows break naive watermark logic.
2. Design an overlap-window incremental filter.
3. Build a replay-safe load that avoids duplicates.
4. Validate backfill correctness with reconciliation checks.
5. Define when to advance watermark vs when to stop and alert.

## 2) Core Concepts To Revise (10-12 min)

1. Late-arriving data:
- Source rows can appear after your last run with old business dates.
- Strict `id > watermark` can miss updates tied to older dates.

2. Overlap window:
- Reprocess a recent range each run (for example, last 3 days).
- Combine with dedupe key logic so reruns stay idempotent.

3. Backfill:
- Historical reprocessing over a chosen date range.
- Must be deterministic and safe to rerun.

4. Replay-safe load:
- Same inputs should produce same final target state.
- Usually requires unique keys + `ON CONFLICT DO UPDATE`.

## 3) SQL Patterns To Recall (10-12 min)

1. Effective watermark with overlap:
```sql
-- logical example
WHERE source_event_date >= date(last_successful_run_at, '-3 day')
```

2. Idempotent upsert pattern:
```sql
INSERT INTO target_table (...)
SELECT ...
ON CONFLICT(business_key) DO UPDATE SET ...;
```

3. Backfill parameter pattern:
```sql
-- pseudo parameters
WHERE invoice_date BETWEEN :backfill_start AND :backfill_end
```

4. Reconciliation check:
```sql
SELECT
  ROUND(SUM(target_amount), 2) AS tgt_sum,
  ROUND(SUM(source_amount), 2) AS src_sum;
```

## 4) Orchestration Thinking (5-8 min)

For each daily run, follow this order:

1. Read pipeline state.
2. Decide extraction window (watermark + overlap).
3. Load with upsert rules.
4. Run data quality and reconciliation checks.
5. Advance watermark only on success.
6. Emit run metrics (rows loaded, rows updated, run window).

## 5) Start Rule

Start the timed Day 39 sheet only if:

1. You can explain why overlap windows reduce data-loss risk.
2. You can state one natural dedupe key for sales fact rows.
3. You can describe replay-safe behavior in one line.
