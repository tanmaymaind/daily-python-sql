"""Day 10 — CTEs in Detail: monthly profitability (SQL / SQLite).

Loads data/orders.csv into an in-memory SQLite database and runs
every query from queries.sql, printing the results. Answers must match
python_analysis.py. Empty cost_price values in the CSV become NULL.
"""
import csv
import sqlite3

with open("data/orders.csv", newline="") as f:
    rows = list(csv.DictReader(f))

for r in rows:
    r["selling_price"] = int(r["selling_price"])
    r["cost_price"] = int(r["cost_price"]) if r["cost_price"] else None
    r["quantity"] = int(r["quantity"])

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE orders (
        order_id TEXT,
        order_date TEXT,
        product TEXT,
        category TEXT,
        city TEXT,
        selling_price INTEGER,
        cost_price INTEGER,
        quantity INTEGER
    )
""")
conn.executemany(
    "INSERT INTO orders VALUES (:order_id, :order_date, :product,"
    " :category, :city, :selling_price, :cost_price, :quantity)",
    rows,
)
conn.commit()

with open("queries.sql") as f:
    sql = f.read()

# Split on semicolons, keeping the comment headers that name each question.
statements = [s.strip() for s in sql.split(";") if s.strip()]

for stmt in statements:
    # Print the question header comment (e.g. "-- Q1: ...")
    header = [ln.strip() for ln in stmt.splitlines()
              if ln.strip().startswith("-- Q")]
    if header:
        print(header[0].lstrip("- ").strip())
    cur = conn.execute(stmt)
    cols = [d[0] for d in cur.description]
    print(" | ".join(cols))
    for row in cur.fetchall():
        print(" | ".join(str(v) for v in row))
    print()

conn.close()
