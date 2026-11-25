# Daily Python & SQL for Data Analysis

One small, real data-analysis exercise every day — Python (pandas) and SQL
(SQLite) answering the same business questions on the same dataset, so the
two skills grow together.

## How it works

- Each day lives in its own `day-NN-name/` folder.
- Every day has: a small dataset (`data/`), a Python analysis
  (`python_analysis.py`), the same analysis in SQL (`queries.sql` +
  `sql_analysis.py`), and a short write-up (`README.md`) with the real results.
- Everything runs with free, local tools: Python 3, pandas, and SQLite
  (built into Python). No paid services, no API keys.

## Rules

- Real runnable code only — every script is run before it is pushed, and the
  write-up carries the real measured numbers.
- One day = one small exercise. Small and daily beats big and rare.
- Never backdate commits.

## Progress

| Day | Exercise | Skills |
|-----|----------|--------|
| 01 | [Sales Analysis: Revenue by Region & Product](day-01-sales-analysis/) ✅ | pandas groupby, SQL GROUP BY / ORDER BY / LIMIT |
| 02 | [Customer & Orders: JOINs](day-02-customer-orders-joins/) ✅ | pandas merge, SQL JOIN / LEFT JOIN / HAVING / subquery |
| 03 | [Salesperson Performance: Window Functions](day-03-salesperson-window-functions/) ✅ | pandas rank/cumsum/shift, SQL RANK / ROW_NUMBER / LAG / window SUM & AVG |
| 04 | [Monthly Sales Trend: Date Functions](day-04-monthly-sales-trend/) ✅ | pandas dt.strftime/dt.quarter/dt.dayofweek, SQL strftime / LAG / CASE |
| 05 | [Product Profitability: CASE WHEN & CTEs](day-05-product-profitability-case-when/) ✅ | pandas np.select / groupby.transform / nlargest, SQL CASE WHEN / CTEs / JOIN |
| 06 | [Data Cleaning: Nulls, Duplicates & Types](day-06-data-cleaning-customers/) ✅ | pandas duplicated / str.strip / str.title / isdigit, SQL DISTINCT / ROW_NUMBER / TRIM / GLOB |
| 07 | [Employee Hierarchy: Self-Joins](day-07-employee-hierarchy-self-joins/) ✅ | pandas self-merge / recursive climb, SQL self-JOIN / WITH RECURSIVE CTE |
| 08 | [HAVING vs WHERE: Food-Delivery Orders](day-08-having-vs-where/) ✅ | pandas groupby filter / .query, SQL WHERE vs HAVING / CTE |
| 09 | [String Functions: Bookstore Catalogue](day-09-string-functions-bookstore/) ✅ | pandas str.contains / str.len / str.split / str.upper, SQL LIKE / LENGTH / SUBSTR / INSTR / UPPER / \|\| |
