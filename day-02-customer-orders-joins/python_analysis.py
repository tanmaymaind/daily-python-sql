"""Day 2 — Customer + orders analysis with pandas (JOINs).

Business questions (same questions as queries.sql, answered in Python):
  Q1  How many customers placed at least one order? (INNER JOIN)
  Q2  Which customers never placed an order? (LEFT JOIN ... IS NULL)
  Q3  Top 5 customers by total revenue (JOIN + GROUP BY)
  Q4  Revenue and order count by city (JOIN + GROUP BY)
  Q5  Customers with more than one order (JOIN + GROUP BY + HAVING)
  Q6  Top 3 customers' share of total revenue (subquery)

Run:  python3 python_analysis.py
"""

import pandas as pd

customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv")
orders["amount"] = orders["quantity"] * orders["unit_price"]

# INNER JOIN: only customers who ordered.
inner = orders.merge(customers, on="customer_id", how="inner")

print("Q1 — Customers who placed at least one order:",
      int(inner["customer_id"].nunique()), "of", len(customers))
print()
print("Q2 — Customers who never ordered:")
never = customers[~customers["customer_id"].isin(orders["customer_id"])]
print(never[["customer_id", "name", "city"]].to_string(index=False))
print()
print("Q3 — Top 5 customers by total revenue:")
top5 = (inner.groupby(["customer_id", "name", "city"])["amount"]
        .sum().reset_index()
        .sort_values(["amount", "customer_id"], ascending=[False, True])
        .head(5))
print(top5.to_string(index=False))
print()
print("Q4 — Revenue and order count by city:")
by_city = (inner.groupby("city")
           .agg(orders=("order_id", "count"), revenue=("amount", "sum"))
           .sort_values("revenue", ascending=False))
print(by_city.to_string())
print()
print("Q5 — Customers with more than one order:")
repeat = (inner.groupby(["customer_id", "name"])
          .agg(order_count=("order_id", "count"), total_spent=("amount", "sum"))
          .query("order_count > 1").reset_index()
          .sort_values(["order_count", "total_spent", "customer_id"],
                       ascending=[False, False, True]))
print(repeat.to_string(index=False))
print()
total = orders["amount"].sum()
top3 = inner.groupby("customer_id")["amount"].sum().nlargest(3).sum()
print("Q6 — Top 3 customers' share of total revenue:",
      f"{round(100 * top3 / total, 2)}% "
      f"(Rs. {top3:,.0f} of Rs. {total:,.0f})")

# --- Chart (added 2026-11-27) -------------------------------------------
# Top 5 customers by revenue, horizontal bar chart -> chart.svg
# (Re-reads the CSVs and recomputes Q3; prints nothing.)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_cust = pd.read_csv("data/customers.csv")
_ord = pd.read_csv("data/orders.csv")
_ord["amount"] = _ord["quantity"] * _ord["unit_price"]
_top5 = (_ord.merge(_cust, on="customer_id", how="inner")
         .groupby(["customer_id", "name"])["amount"].sum().reset_index()
         .sort_values(["amount", "customer_id"], ascending=[True, True])
         .tail(5))
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(_top5["name"], _top5["amount"], color="#2e7d32")
for i, v in enumerate(_top5["amount"]):
    ax.text(v + 1500, i, f"Rs. {v:,.0f}", va="center", fontsize=9)
ax.set_xlabel("Total revenue (Rs.)")
ax.set_title("Top 5 customers by revenue")
ax.set_xlim(0, _top5["amount"].max() * 1.22)
fig.tight_layout()
fig.savefig("chart.svg", format="svg")
plt.close(fig)
