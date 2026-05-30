# Day 40 practice runner template (question-only scaffold)
# Use this file to execute your own Day 40 SQL attempts against chinook.db.
# No answer key is included in this template.

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "29_copilot" / "chinook.db"


def run_sql(cur, sql, params=None, fetch=False):
    cur.execute(sql, params or ())
    if fetch:
        return cur.fetchall()
    return None


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Block A TODO:
    # Write your fact grain and design notes separately before coding.

    # Block B Q1 TODO:
    # Create training_dim_date.

    # Block B Q2 TODO:
    # Create training_dim_customer.

    # Block B Q3 TODO:
    # Create training_dim_track.

    # Block B Q4 TODO:
    # Create training_fct_sales.

    # Block B Q5 TODO:
    # Run row-count, null, and unmatched-join checks.

    # Block C TODO:
    # Add KPI queries for monthly revenue, top customers, and genre revenue.

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
