"""Day 4 — Monthly sales trend with pandas (date functions).

Business questions (same questions as queries.sql, answered in Python):
  Q1  Total revenue and order count by month (Jan–Jun 2026)
  Q2  Month-over-month revenue growth % (LAG / pct_change)
  Q3  Best month by revenue
  Q4  Average order value by month
  Q5  Weekend vs weekday orders — count and revenue
  Q6  Quarterly totals — Q1 vs Q2 2026

Run:  python3 python_analysis.py
"""

import pandas as pd

df = pd.read_csv("data/orders.csv", parse_dates=["order_date"])
df["amount"] = df["quantity"] * df["unit_price"]
df["month"] = df["order_date"].dt.strftime("%Y-%m")
df["quarter"] = "Q" + df["order_date"].dt.quarter.astype(str)
df["is_weekend"] = df["order_date"].dt.dayofweek >= 5

monthly = (df.groupby("month", as_index=False)
           .agg(total_revenue=("amount", "sum"),
                orders=("order_id", "count"),
                avg_order_value=("amount", "mean")))
monthly["avg_order_value"] = monthly["avg_order_value"].round(2)
monthly = monthly.sort_values("month")

print("Q1 — Total revenue and order count by month:")
print(monthly[["month", "total_revenue", "orders"]].to_string(index=False))
print()
print("Q2 — Month-over-month revenue growth %:")
mom = monthly.copy()
mom["prev_revenue"] = mom["total_revenue"].shift(1)
mom["growth_pct"] = ((mom["total_revenue"] - mom["prev_revenue"])
                     / mom["prev_revenue"] * 100).round(1)
print(mom[["month", "total_revenue", "prev_revenue", "growth_pct"]]
      .to_string(index=False))
print()
print("Q3 — Best month by revenue:")
best = monthly.loc[monthly["total_revenue"].idxmax()]
print(f"{best['month']} — Rs. {best['total_revenue']:,.0f} "
      f"from {int(best['orders'])} orders")
print()
print("Q4 — Average order value by month:")
print(monthly[["month", "avg_order_value"]].to_string(index=False))
print()
print("Q5 — Weekend vs weekday orders:")
wk = (df.groupby("is_weekend", as_index=False)
      .agg(orders=("order_id", "count"),
           total_revenue=("amount", "sum")))
wk["day_type"] = wk["is_weekend"].map({True: "Weekend", False: "Weekday"})
print(wk[["day_type", "orders", "total_revenue"]].to_string(index=False))
print()
print("Q6 — Quarterly totals (Q1 vs Q2 2026):")
qtr = (df.groupby("quarter", as_index=False)
       .agg(total_revenue=("amount", "sum"),
            orders=("order_id", "count")))
print(qtr.to_string(index=False))
print()
print("Total revenue (all 30 orders, Jan–Jun 2026): Rs.",
      f"{df['amount'].sum():,.0f}")

# --- Chart (added 2026-11-27) -------------------------------------------
# Month-wise revenue, line chart -> chart.svg
# (Re-reads the CSV and recomputes Q1; prints nothing.)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_d = pd.read_csv("data/orders.csv", parse_dates=["order_date"])
_d["amount"] = _d["quantity"] * _d["unit_price"]
_d["month"] = _d["order_date"].dt.strftime("%Y-%m")
_m = (_d.groupby("month", as_index=False)["amount"].sum()
      .sort_values("month"))
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(_m["month"], _m["amount"], marker="o", color="#6a1b9a")
for _, r in _m.iterrows():
    ax.annotate(f"Rs. {r['amount']:,.0f}", (r["month"], r["amount"]),
                textcoords="offset points", xytext=(0, 8),
                ha="center", fontsize=8)
ax.set_ylabel("Revenue (Rs.)")
ax.set_title("Revenue by month (Jan–Jun 2026)")
ax.set_ylim(0, _m["amount"].max() * 1.2)
fig.tight_layout()
fig.savefig("chart.svg", format="svg")
plt.close(fig)
