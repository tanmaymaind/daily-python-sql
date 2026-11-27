"""Day 2 — Run the SQL analysis.

Loads data/customers.csv and data/orders.csv into an in-memory SQLite
database, then runs every query from queries.sql and prints the results.

Run:  python3 sql_analysis.py
"""

import csv
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute(
    "CREATE TABLE customers ("
    "customer_id INTEGER, name TEXT, city TEXT, signup_date TEXT)"
)
cur.execute(
    "CREATE TABLE orders ("
    "order_id INTEGER, customer_id INTEGER, order_date TEXT, "
    "product TEXT, category TEXT, quantity INTEGER, unit_price REAL)"
)

with open("data/customers.csv", newline="") as f:
    rows = list(csv.DictReader(f))
cur.executemany(
    "INSERT INTO customers VALUES (?, ?, ?, ?)",
    [(r["customer_id"], r["name"], r["city"], r["signup_date"]) for r in rows],
)
with open("data/orders.csv", newline="") as f:
    rows = list(csv.DictReader(f))
cur.executemany(
    "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)",
    [(r["order_id"], r["customer_id"], r["order_date"], r["product"],
      r["category"], r["quantity"], r["unit_price"]) for r in rows],
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
