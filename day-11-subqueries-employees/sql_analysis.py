"""Day 11 — Subqueries: classic interview questions (SQL / SQLite).

Loads data/employees.csv and data/orders.csv into an in-memory SQLite
database, builds the cleaned views exactly the way python_analysis.py
cleans the CSVs, then runs every query from queries.sql. Answers must
match python_analysis.py. Empty salary / order_amount values in the
CSVs become NULL.
"""
import csv
import sqlite3

with open("data/employees.csv", newline="") as f:
    emps = list(csv.DictReader(f))
with open("data/orders.csv", newline="") as f:
    ords = list(csv.DictReader(f))

for r in emps:
    r["salary"] = int(r["salary"]) if r["salary"] else None
for r in ords:
    r["order_amount"] = int(r["order_amount"]) if r["order_amount"] else None

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE employees (
        employee_id TEXT, name TEXT, department TEXT,
        city TEXT, salary INTEGER, joining_date TEXT
    )
""")
conn.execute("""
    CREATE TABLE orders (
        order_id TEXT, employee_id TEXT, order_date TEXT,
        order_amount INTEGER, city TEXT
    )
""")
conn.executemany(
    "INSERT INTO employees VALUES (:employee_id, :name, :department,"
    " :city, :salary, :joining_date)",
    emps,
)
conn.executemany(
    "INSERT INTO orders VALUES (:order_id, :employee_id, :order_date,"
    " :order_amount, :city)",
    ords,
)

# Same cleaning as python_analysis.py, as views every query can use.
conn.execute("""
    CREATE VIEW cleaned_emp AS
    SELECT employee_id, name,
           CASE LOWER(TRIM(department))
               WHEN 'engineering' THEN 'Engineering'
               WHEN 'sales' THEN 'Sales'
               WHEN 'finance' THEN 'Finance'
               WHEN 'hr' THEN 'HR'
               WHEN 'marketing' THEN 'Marketing'
               WHEN 'operations' THEN 'Operations'
               ELSE TRIM(department)
           END AS department,
           city, salary, joining_date
    FROM employees
    WHERE salary IS NOT NULL AND salary > 0
      AND rowid IN (SELECT MIN(rowid) FROM employees GROUP BY employee_id)
""")
conn.execute("""
    CREATE VIEW cleaned_ord AS
    SELECT order_id, employee_id, order_date, order_amount, city
    FROM orders
    WHERE order_amount IS NOT NULL
      AND rowid IN (SELECT MIN(rowid) FROM orders GROUP BY order_id)
""")
conn.commit()

print(f"Clean employees: {conn.execute('SELECT COUNT(*) FROM cleaned_emp').fetchone()[0]}")
print(f"Clean orders: {conn.execute('SELECT COUNT(*) FROM cleaned_ord').fetchone()[0]}")
print()

with open("queries.sql") as f:
    sql = f.read()

statements = [s.strip() for s in sql.split(";") if s.strip()]

for stmt in statements:
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
