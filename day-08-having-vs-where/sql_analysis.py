"""Day 8 — HAVING vs WHERE: food-delivery orders (SQL / SQLite).

Loads data/orders.csv into an in-memory SQLite database and runs
every query from queries.sql, printing the results. Answers must match
python_analysis.py. rating is NULL for cancelled orders (blank in the
CSV); quantity and unit_price are INTEGER.
"""
import csv
import sqlite3

with open("data/orders.csv", newline="") as f:
    rows = list(csv.DictReader(f))

# Blank rating becomes NULL, quantity / unit_price become INTEGER.
for r in rows:
    r["order_id"] = int(r["order_id"])
    r["quantity"] = int(r["quantity"])
    r["unit_price"] = int(r["unit_price"])
    r["rating"] = float(r["rating"]) if r["rating"] else None

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE orders (
        order_id INTEGER,
        customer_name TEXT,
        city TEXT,
        cuisine TEXT,
        item TEXT,
        quantity INTEGER,
        unit_price INTEGER,
        order_date TEXT,
        status TEXT,
        rating REAL
    )
""")
conn.executemany(
    "INSERT INTO orders VALUES (:order_id, :customer_name, :city,"
    " :cuisine, :item, :quantity, :unit_price, :order_date, :status,"
    " :rating)",
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
