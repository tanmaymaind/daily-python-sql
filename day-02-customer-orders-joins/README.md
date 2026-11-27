# Day 2 — Customer & Orders: JOINs

Day 2 is about the question sitting underneath every shop: who actually
buys, and who never does? I've got 15 customers and 24 orders, and I
answered it with JOINs in pandas — `merge` is the pandas equivalent of
SQL's `INNER` and `LEFT JOIN`.

## Business questions

| # | Question | Python | SQL idea |
|---|----------|--------|----------|
| Q1 | How many customers placed at least one order? | `merge(how="inner")` + `nunique()` | `INNER JOIN` |
| Q2 | Which customers never placed an order? | `~isin(...)` on customer_id | `LEFT JOIN ... IS NULL` |
| Q3 | Top 5 customers by total revenue | `merge` + `groupby + sort + head(5)` | `JOIN + GROUP BY` |
| Q4 | Revenue and order count by city | `merge` + `groupby('city')` | `JOIN + GROUP BY` |
| Q5 | Customers with more than one order | `groupby + filter` | `JOIN + GROUP BY + HAVING` |
| Q6 | Top 3 customers' share of total revenue | top 3 total ÷ grand total | subquery |

## Results (verified — ran the Python script)

- **Customers who ordered:** 12 of 15 — 3 never ordered: Suresh Kumar (Chennai), Meera Pillai (Bengaluru), Rahul Gupta (Nagpur)
- **Top 5 by revenue:** Aarav Sharma ₹70,597 · Sneha Kulkarni ₹64,999 · Divya Reddy ₹50,097 · Kavya Joshi ₹36,597 · Vikram Singh ₹32,997
- **Revenue by city:** Mumbai ₹1,60,093 (8 orders) · Pune ₹55,594 · Hyderabad ₹50,097 · Delhi ₹38,294 — Mumbai is nearly half the business
- **Repeat customers:** 9 customers ordered more than once
- **Top 3 share:** the top 3 customers alone are 52.0% of total revenue (₹1,85,693 of ₹3,57,071)

Three customers are half the revenue. That's the kind of thing you only
notice once you join the tables — the customers file on its own would
never tell you that.

## Files

- `data/customers.csv` — the dataset (15 customers)
- `data/orders.csv` — the dataset (24 orders)
- `python_analysis.py` — pandas analysis with `merge` (`python3 python_analysis.py`)

## What I practised

- pandas: `merge` with `how="inner"` / `how="left"`, `~isin()` for the "never ordered" set, `groupby` after a join
- SQL thinking: `INNER JOIN` keeps only the matches, `LEFT JOIN ... IS NULL` finds the ones with no match at all

What stuck with me: a `LEFT JOIN ... IS NULL` is the fastest way to
find the customers you're about to lose — the ones who signed up and
never came back. And when 3 customers are half your revenue, you protect
those relationships first.
