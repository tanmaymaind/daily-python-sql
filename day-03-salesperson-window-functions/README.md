# Day 3 — Salesperson Performance: Window Functions

Day 3 is the one where window functions finally clicked for me. Monthly
revenue for 8 salespeople across 4 regions (24 rows, Jul–Sep 2026) — I
did it in SQL with `RANK()`, running totals and `LAG()`, and then found
the pandas equivalents (`rank`, `cumsum`, `shift`). Same questions, same
answers, both ways.

## Business questions

| # | Question | Python | SQL |
|---|----------|--------|-----|
| Q1 | Rank salespeople by total revenue within each region | `groupby + rank(method='min')` | `RANK() OVER (PARTITION BY region ...)` |
| Q2 | Running total of revenue per region, month by month | `groupby + cumsum()` | `SUM(...) OVER (PARTITION BY region ORDER BY month)` |
| Q3 | Top 3 salespeople overall by total revenue | `sort_values + head(3)` | `ROW_NUMBER() OVER (ORDER BY total DESC)` |
| Q4 | Month-over-month revenue growth per salesperson | `groupby + shift(1)` | `LAG(revenue) OVER (PARTITION BY salesperson ...)` |
| Q5 | Best month for each salesperson | `groupby + rank(method='first')` | `ROW_NUMBER() OVER (PARTITION BY salesperson ORDER BY revenue DESC)` |
| Q6 | Each salesperson's total vs their region's average | `groupby + transform('mean')` | `AVG(total) OVER (PARTITION BY region)` |

## Results (verified — Python and SQL agree exactly)

- **Total revenue (Jul–Sep 2026):** ₹75,65,000
- **Rank within region:** Mumbai — Aarav Sharma #1 (₹15,65,000), Sneha Kulkarni #2 (₹12,45,000) · Pune — Priya Nair #1 (₹10,10,000), Rohit Deshmukh #2 (₹7,55,000) · Nashik — Vikram Joshi #1 (₹6,50,000), Ananya Patil #2 (₹5,65,000) · Nagpur — Karan Singh #1 (₹9,60,000), Meera Iyer #2 (₹8,15,000)
- **Running totals by region:** Mumbai ₹8,00,000 → ₹17,15,000 → ₹28,10,000 · Pune ₹5,05,000 → ₹11,00,000 → ₹17,65,000 · Nashik ₹3,45,000 → ₹7,60,000 → ₹12,15,000 · Nagpur ₹5,85,000 → ₹11,40,000 → ₹17,75,000
- **Top 3 overall:** Aarav Sharma ₹15,65,000 · Sneha Kulkarni ₹12,45,000 · Priya Nair ₹10,10,000
- **Month-over-month growth:** biggest jump — Ananya Patil +21.9% in Aug, Aarav Sharma +24.5% in Sep · only fall — Karan Singh −17.4% in Aug (then +15.8% in Sep) · steadiest — Meera Iyer +12.5% then +13.0%
- **Best month:** September for 7 of 8 salespeople — the exception is Karan Singh, whose best month was July (₹3,45,000)
- **Vs region average:** Aarav +₹1,60,000 above Mumbai's ₹14,05,000 · Priya +₹1,27,500 above Pune's ₹8,82,500 · Vikram +₹42,500 above Nashik's ₹6,07,500 · Karan +₹72,500 above Nagpur's ₹8,87,500

September was the best month for almost everyone — 7 out of 8 people.
That's the sort of pattern you only see once you line the months up
side by side.

## Files

- `data/monthly_sales.csv` — the dataset (24 rows: 8 salespeople × 3 months)
- `python_analysis.py` — pandas analysis (`python3 python_analysis.py`)
- `queries.sql` — the SQL queries
- `sql_analysis.py` — loads the CSV into in-memory SQLite and runs the queries (`python3 sql_analysis.py`)

## What I practised

- pandas: `groupby + rank`, `cumsum` for running totals, `shift` for previous-row values, `transform('mean')` for group averages
- SQL: `RANK()`, `ROW_NUMBER()`, `SUM() OVER`, `LAG()`, `AVG() OVER` — window functions with `PARTITION BY`

What stuck with me: window functions answer questions a plain `GROUP
BY` can't — ranks, running totals and "compared to the average" all need
the rows to stay visible while the calculation happens around them.
