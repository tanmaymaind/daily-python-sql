# Day 8 — HAVING vs WHERE: Food-Delivery Orders

Day 8 is about a distinction that trips up a lot of people, me included:
`WHERE` and `HAVING` look similar but they filter at different moments.
`WHERE` filters rows **before** grouping; `HAVING` filters groups
**after** grouping. So the same ₹300 cut-off can give you two different
answers — and Q5 shows exactly that, on purpose. Same 6 questions in
pandas and in SQLite, with identical results.

## Dataset

`data/orders.csv` — 24 orders, 10 columns (`order_id`, `customer_name`,
`city`, `cuisine`, `item`, `quantity`, `unit_price`, `order_date`,
`status`, `rating`). 22 orders delivered, 2 cancelled (Rohan Desai's
Dal Makhani and Vikram Singh's Pizza — both have no rating). Order
amount = `quantity × unit_price`. Cities: Mumbai, Pune, Nagpur, Nashik.

## Questions & results

| # | Question | Answer |
|---|----------|--------|
| Q1 | Revenue by city (Delivered orders only — WHERE) | Mumbai ₹2,957 (7 orders); Pune ₹1,930 (7); Nagpur ₹1,320 (4); Nashik ₹1,090 (4). Total delivered revenue ₹7,297 |
| Q2 | Cities with total delivered revenue above ₹1,500 (HAVING) | 2 — Mumbai ₹2,957 and Pune ₹1,930. Nagpur and Nashik drop out |
| Q3 | Customers who ordered more than once (HAVING COUNT) | 10 of 11 customers — only Rohan Desai has a single delivered order. Sneha Kulkarni leads with 3 orders (₹510); Arjun Mehta spent the most (₹1,160 in 2 orders) |
| Q4 | Cuisines with avg rating ≥ 4.0 and 3+ rated orders (HAVING × 2) | 5 — North Indian 4.50 (4 orders), South Indian 4.38 (4), Biryani 4.25 (4), Chinese 4.25 (4), Maharashtrian 4.17 (3). Fast Food fails on rating (3.33) |
| Q5 | Same ₹300 cut-off, two filters | WHERE on rows: all 4 cities have orders above ₹300 (Mumbai 4 orders / ₹2,177; Nagpur 3 / ₹1,140; Pune 2 / ₹880; Nashik 2 / ₹780). HAVING on groups: only Mumbai (avg ₹422.43) and Nagpur (avg ₹330.00) average above ₹300 — Pune (₹275.71) and Nashik (₹272.50) drop out because their many small orders drag the average down |
| Q6 | Top 3 customers by spend (total spend above ₹700) | Arjun Mehta ₹1,160; Aarav Patil ₹880; Vikram Singh ₹780. 5 customers in total spent above ₹700 |

## The same data, two filters

| Filter | Cities left | Cities |
|--------|-------------|--------|
| `WHERE` — delivered orders only, revenue grouped by city | 4 | Mumbai, Pune, Nagpur, Nashik |
| `HAVING` — of those, total delivered revenue above ₹1,500 | 2 | Mumbai, Pune |

In one line: **WHERE filters rows before grouping, HAVING filters groups after grouping.**

## What I found

- Only 2 of the 4 cities cross ₹1,500 in delivered revenue, and Mumbai (₹2,957) plus Pune (₹1,930) together bring ₹4,887 of the ₹7,297 total — about 67%. Nagpur and Nashik together are just a third of the business.
- The same ₹300 cut-off answers two different questions. Every city has *some* orders above ₹300 (a WHERE question), but only Mumbai (average ₹422.43) and Nagpur (average ₹330.00) *average* above ₹300 (a HAVING question). Pune (₹275.71) and Nashik (₹272.50) run on many small orders — judging them by their biggest orders alone would flatter them.
- 10 of the 11 customers ordered more than once — this business runs on repeat customers. The only single-order customer is Rohan Desai, and his second order was one of the two cancelled ones.

## Python vs SQL approach

| Step | Python (pandas) | SQL (SQLite) |
|------|-----------------|--------------|
| Row filter before grouping | `df[df["status"] == "Delivered"]` then `groupby` | `WHERE status = 'Delivered'` before `GROUP BY` |
| Group filter after grouping | filter the grouped frame (`q1[q1["revenue"] > 1500]`, `.query(...)`) | `HAVING SUM(...) > 1500`, `HAVING COUNT(*) > 1` |
| Two HAVING conditions | `.query("avg_rating >= 4.0 and rated_orders >= 3")` | `HAVING AVG(rating) >= 4.0 AND COUNT(rating) >= 3` |
| Row vs group contrast (Q5) | `delivered[delivered["amount"] > 300]` vs grouped `.query("avg_order_value > 300")` | CTE computing `amount`, then `WHERE amount > 300` vs `HAVING AVG(amount) > 300` |
| Top N with a group filter | `.query("total_spend > 700").sort_values(...).head(3)` | `HAVING SUM(...) > 700 ... ORDER BY total_spend DESC LIMIT 3` |
| Order amount | `df["amount"] = df["quantity"] * df["unit_price"]` | `quantity * unit_price` (or a CTE when reused) |

## How to run

```bash
python3 python_analysis.py   # pandas version
python3 sql_analysis.py      # loads the CSV into SQLite and runs queries.sql
```

Both print the same answers. The biggest lesson: **WHERE and HAVING
answer different questions** — "which orders are big?" (WHERE, rows)
is not the same as "which cities have big *average* orders?" (HAVING,
groups). Filter in the wrong place and the answer changes without any
error telling you — Q5 shows it clearly: Pune and Nashik look strong on
big orders but fall below ₹300 on average order value.
