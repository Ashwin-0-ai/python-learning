# Day 39 practice runner template (question-only scaffold)
# Use this file to execute your own Day 39 SQL attempts against chinook.db.
# No answer key is included in this template.

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "chinook.db"


def run_sql(cur, sql, params=None, fetch=False):
    cur.execute(sql, params or ())
    if fetch:
        return cur.fetchall()
    return None


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Block B Q1 TODO:
    # Create/seed training_etl_state_v2.

    # Block B Q2 TODO:
    # Create training_fct_sales_overlap.

    # Block B Q3 TODO:
    # Implement overlap-window extraction + idempotent upsert.

    # Block B Q4 TODO:
    # Run duplicate/null/reconciliation checks.

    # Block B Q5 TODO:
    # Conditionally update pipeline state based on check results.

    # Block C TODO:
    # Add your backfill drill SQL and validation queries.

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
