"""Day 1 — Sales analysis with pandas.

Business questions (same questions as queries.sql, answered in Python):
  Q1  Total revenue
  Q2  Revenue by region
  Q3  Revenue by category
  Q4  Top 3 products by revenue
  Q5  Average order value
  Q6  Total units sold

Run:  python3 python_analysis.py
"""

import pandas as pd

df = pd.read_csv("data/sales.csv")
df["amount"] = df["quantity"] * df["unit_price"]

print("Q1 — Total revenue: Rs.", f"{df['amount'].sum():,.0f}")
print()
print("Q2 — Revenue by region:")
print(df.groupby("region")["amount"].sum().sort_values(ascending=False).to_string())
print()
print("Q3 — Revenue by category:")
print(df.groupby("category")["amount"].sum().sort_values(ascending=False).to_string())
print()
print("Q4 — Top 3 products by revenue:")
print(df.groupby("product")["amount"].sum().sort_values(ascending=False).head(3).to_string())
print()
print("Q5 — Average order value: Rs.", f"{df['amount'].mean():,.2f}")
print("Q6 — Total units sold:", int(df["quantity"].sum()))

# --- Chart (added 2026-11-27) -------------------------------------------
# Revenue by region, bar chart -> chart.svg
# (Re-reads the CSV and recomputes Q2; prints nothing.)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_d = pd.read_csv("data/sales.csv")
_d["amount"] = _d["quantity"] * _d["unit_price"]
_by_region = _d.groupby("region")["amount"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(_by_region.index, _by_region.values, color="#1565c0")
for i, v in enumerate(_by_region.values):
    ax.text(i, v + 6000, f"Rs. {v:,.0f}", ha="center", fontsize=9)
ax.set_ylabel("Revenue (Rs.)")
ax.set_title("Revenue by region")
ax.set_ylim(0, _by_region.max() * 1.15)
fig.tight_layout()
fig.savefig("chart.svg", format="svg")
plt.close(fig)
