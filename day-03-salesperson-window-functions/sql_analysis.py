"""Day 3 — Run the SQL analysis.

Loads data/monthly_sales.csv into an in-memory SQLite database, then runs
every query from queries.sql and prints the results.

Run:  python3 sql_analysis.py
"""

import csv
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute(
    "CREATE TABLE monthly_sales ("
    "salesperson TEXT, region TEXT, month TEXT, "
    "deals_closed INTEGER, revenue INTEGER)"
)

with open("data/monthly_sales.csv", newline="") as f:
    rows = list(csv.DictReader(f))
cur.executemany(
    "INSERT INTO monthly_sales VALUES (?, ?, ?, ?, ?)",
    [(r["salesperson"], r["region"], r["month"],
      r["deals_closed"], r["revenue"]) for r in rows],
)

with open("queries.sql") as f:
    sql_text = f.read()

# Split into statements, keeping the -- Qn comment above each query as its label.
statements = [s.strip() for s in sql_text.split(";") if s.strip()]
for stmt in statements:
    lines = [ln for ln in stmt.splitlines() if ln.strip()]
    label = next((ln[3:].strip() for ln in lines if ln.startswith("-- Q")), "Query")
    query = "\n".join(ln for ln in lines if not ln.startswith("--"))
    cur.execute(query)
    cols = [d[0] for d in cur.description]
    print(label)
    print(" | ".join(cols))
    for row in cur.fetchall():
        print(" | ".join(str(v) for v in row))
    print()

con.close()
