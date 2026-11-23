"""Day 7 — Employee Hierarchy: self-joins (SQL / SQLite).

Loads data/employees.csv into an in-memory SQLite database and runs
every query from queries.sql, printing the results. Answers must match
python_analysis.py. manager_id is NULL for the CEO (blank in the CSV).
"""
import csv
import sqlite3

with open("data/employees.csv", newline="") as f:
    rows = list(csv.DictReader(f))

# Blank manager_id becomes NULL, salary becomes INTEGER.
for r in rows:
    r["manager_id"] = int(r["manager_id"]) if r["manager_id"] else None
    r["salary"] = int(r["salary"])

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE employees (
        emp_id INTEGER,
        name TEXT,
        department TEXT,
        manager_id INTEGER,
        salary INTEGER,
        joining_date TEXT
    )
""")
conn.executemany(
    "INSERT INTO employees VALUES (:emp_id, :name, :department,"
    " :manager_id, :salary, :joining_date)",
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
