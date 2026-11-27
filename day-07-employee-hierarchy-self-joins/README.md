# Day 7 — Employee Hierarchy: Self-Joins

Day 7 starts with a fun idea: a Pune IT services company keeps its whole
org chart in a single table. Every employee has a `manager_id` that
points at another row of the same table (blank only for the CEO). So one
table, joined to itself, becomes the whole organisation. I answered the
same 6 questions in pandas and in SQLite, with identical results.

## Dataset

`data/employees.csv` — 20 employees, 6 columns (`emp_id`, `name`,
`department`, `manager_id`, `salary`, `joining_date`). Three levels
below the CEO:

- Level 0: Rajesh Malhotra (CEO, Management, ₹1,80,000).
- Level 1: Priya Sharma (Sales), Arjun Mehta (Engineering),
  Kavya Nair (HR).
- Level 2: their 9 direct reports, including two team leads —
  Vikram Singh (Sales) and Sneha Kulkarni (Engineering).
- Level 3: 7 people reporting to Vikram and Sneha.
- The wrinkle I built in on purpose: two of Sneha's engineers earn more
  than she does (Nikhil Gupta ₹82,000 and Tanvi Shah ₹79,000 vs Sneha's
  ₹78,000).

## Questions & results

| # | Question | Answer |
|---|----------|--------|
| Q1 | Every employee with their manager's name | 20 employees; only the CEO (Rajesh Malhotra) has no manager |
| Q2 | Employees who earn more than their direct manager | 2 — Nikhil Gupta ₹82,000 vs Sneha Kulkarni ₹78,000 (+₹4,000); Tanvi Shah ₹79,000 vs Sneha ₹78,000 (+₹1,000) |
| Q3 | Direct reports & team salary bill per manager | Arjun Mehta 4 / ₹2,82,000; Sneha Kulkarni 4 / ₹2,73,000; Rajesh Malhotra 3 / ₹2,88,000; Priya Sharma 3 / ₹1,75,000; Vikram Singh 3 / ₹1,41,000; Kavya Nair 2 / ₹1,02,000 — 6 managers, 19 direct reports |
| Q4 | Headcount & average salary by department | Engineering 9 / ₹73,333.33; Sales 7 / ₹58,714.29; HR 3 / ₹63,333.33; Management 1 / ₹1,80,000. Total salary bill ₹14,41,000 |
| Q5 | Organisation depth (levels from the CEO) | Level 0: 1, Level 1: 3, Level 2: 9, Level 3: 7 — deepest level 3 |
| Q6 | Reporting chain for Nikhil Gupta (bottom-up) | Nikhil Gupta → Sneha Kulkarni → Arjun Mehta → Rajesh Malhotra — 4 people |

## Salary by hierarchy level

| Level | Employees | Total salary | Average salary |
|-------|-----------|--------------|----------------|
| 0 (CEO) | 1 | ₹1,80,000 | ₹1,80,000 |
| 1 | 3 | ₹2,88,000 | ₹96,000 |
| 2 | 9 | ₹5,59,000 | ₹62,111 |
| 3 | 7 | ₹4,14,000 | ₹59,143 |

## What I found

- 2 employees earn more than their own manager: Nikhil Gupta (₹82,000) and Tanvi Shah (₹79,000) both earn more than their team lead Sneha Kulkarni (₹78,000). That is an anomaly worth an HR look — either the lead is underpaid for her role, or her two engineers are priced above the person who reviews their work.
- Level 2 is where the people and the money sit: 9 of the 20 employees, and ₹5,59,000 of the ₹14,41,000 salary bill (about 39%). The middle of this org carries most of its cost.
- The pay step between Level 2 and Level 3 is tiny — average ₹62,111 vs ₹59,143, a gap of under ₹3,000. Juniors earn almost what the level above them earns, so a promotion here changes the title much more than the salary.

## Python vs SQL approach

| Step | Python (pandas) | SQL (SQLite) |
|------|-----------------|--------------|
| Self-join | `df.merge(df, left_on="manager_id", right_on="emp_id")` | `FROM employees e LEFT JOIN employees m ON m.emp_id = e.manager_id` |
| Earns more than manager | filter `salary > manager_salary`, `diff = salary - manager_salary` | `JOIN` on manager + `WHERE e.salary > m.salary` |
| Reports per manager | `groupby("manager_id").agg(count, sum)` | `GROUP BY m.emp_id, m.name` with `COUNT(*)` / `SUM(e.salary)` |
| Department averages | `groupby("department").agg(count, mean)` | `GROUP BY department` with `COUNT(*)` / `ROUND(AVG(salary), 2)` |
| Org depth | climb `manager_id` links recursively in Python | `WITH RECURSIVE` CTE from the CEO (`manager_id IS NULL`) |
| Reporting chain | walk up from Nikhil Gupta until `manager_id` is blank | `WITH RECURSIVE` CTE starting at Nikhil Gupta |

## How to run

```bash
python3 python_analysis.py   # pandas version
python3 sql_analysis.py      # loads the CSV into SQLite and runs queries.sql
```

Both print the same answers. The biggest lesson: **a self-join turns one
table into an org chart** — and the recursive CTE walks the whole chain
in a single query, which pandas can only do with an explicit loop.
