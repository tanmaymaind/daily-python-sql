"""Day 9 — String Functions: bookstore catalogue (SQL / SQLite).

Loads data/books.csv into an in-memory SQLite database and runs
every query from queries.sql, printing the results. Answers must match
python_analysis.py. price and stock are INTEGER.
"""
import csv
import sqlite3

with open("data/books.csv", newline="") as f:
    rows = list(csv.DictReader(f))

for r in rows:
    r["book_id"] = int(r["book_id"])
    r["price"] = int(r["price"])
    r["stock"] = int(r["stock"])

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE books (
        book_id INTEGER,
        title TEXT,
        author TEXT,
        category TEXT,
        price INTEGER,
        stock INTEGER
    )
""")
conn.executemany(
    "INSERT INTO books VALUES (:book_id, :title, :author,"
    " :category, :price, :stock)",
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
