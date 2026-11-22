"""Day 6 — Data Cleaning: nulls, duplicates & types (SQL / SQLite).

Loads data/customers_raw.csv into an in-memory SQLite database and runs
every query from queries.sql, printing the results. Answers must match
python_analysis.py. All columns are TEXT so that blanks, leading '+' and
short pincodes survive exactly as they appear in the raw file.
"""
import csv
import sqlite3

with open("data/customers_raw.csv", newline="") as f:
    rows = list(csv.DictReader(f))

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE customers_raw (
        customer_id TEXT,
        name TEXT,
        email TEXT,
        phone TEXT,
        city TEXT,
        pincode TEXT,
        signup_date TEXT
    )
""")
conn.executemany(
    "INSERT INTO customers_raw VALUES (:customer_id, :name, :email,"
    " :phone, :city, :pincode, :signup_date)",
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
