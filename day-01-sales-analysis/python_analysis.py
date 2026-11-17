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
