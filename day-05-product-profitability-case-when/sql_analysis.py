"""Day 5 — Product Profitability: CASE WHEN & CTEs (SQL / SQLite).

Loads data/products.csv into an in-memory SQLite database and runs every
query from queries.sql, printing the results. Answers must match
python_analysis.py.
"""
import csv
import sqlite3

with open("data/products.csv", newline="") as f:
    rows = list(csv.DictReader(f))

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE products (
        product TEXT,
        category TEXT,
        cost_price INTEGER,
        selling_price INTEGER,
        units_sold INTEGER,
        stock_qty INTEGER
    )
""")
conn.executemany(
    "INSERT INTO products VALUES (:product, :category, :cost_price,"
    " :selling_price, :units_sold, :stock_qty)",
    [{k: (int(v) if k != "product" and k != "category" else v)
      for k, v in row.items()} for row in rows],
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
