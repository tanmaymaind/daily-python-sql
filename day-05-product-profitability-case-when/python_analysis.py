"""Day 5 — Product Profitability: CASE WHEN & CTEs (Python / pandas).

Dataset: 20 products of a Pune electronics store (data/products.csv).
Same 6 business questions as queries.sql — answers must match the SQL run.
"""
import numpy as np
import pandas as pd

df = pd.read_csv("data/products.csv")

# Derived columns
df["margin_pct"] = (df["selling_price"] - df["cost_price"]) / df["selling_price"] * 100
df["profit_per_unit"] = df["selling_price"] - df["cost_price"]
df["revenue"] = df["selling_price"] * df["units_sold"]
df["total_profit"] = df["profit_per_unit"] * df["units_sold"]

# Q1: margin band per product (CASE WHEN equivalent)
conditions = [df["margin_pct"] >= 40, df["margin_pct"] >= 20]
choices = ["High", "Medium"]
df["margin_band"] = np.select(conditions, choices, default="Low")

print("Q1 — Margin band per product")
print(df[["product", "category", "selling_price", "margin_pct", "margin_band"]]
      .sort_values("margin_pct", ascending=False).to_string(index=False))
print()

# Q2: products and total profit per margin band
band = (df.groupby("margin_band")
          .agg(products=("product", "count"), total_profit=("total_profit", "sum"))
          .reindex(["High", "Medium", "Low"]))
print("Q2 — Products and total profit per margin band")
print(band.to_string())
print(f"Total profit (all products): Rs. {df['total_profit'].sum():,}")
print()

# Q3: products priced above their category's average selling price
# (CTE/subquery equivalent: category average via groupby transform)
df["category_avg_price"] = df.groupby("category")["selling_price"].transform("mean")
above = df[df["selling_price"] > df["category_avg_price"]].sort_values("category")
print("Q3 — Products priced above their category average selling price")
print(above[["product", "category", "selling_price", "category_avg_price"]]
      .to_string(index=False))
print(f"Count: {len(above)} of {len(df)} products")
print()

# Q4: stock status (CASE WHEN) and units sold by status
def stock_status(qty):
    if qty == 0:
        return "Out of stock"
    if qty < 5:
        return "Low stock"
    return "In stock"

df["stock_status"] = df["stock_qty"].apply(stock_status)
stock = (df.groupby("stock_status")
           .agg(products=("product", "count"), units_sold=("units_sold", "sum"))
           .reindex(["In stock", "Low stock", "Out of stock"]))
print("Q4 — Stock status")
print(stock.to_string())
print("Out-of-stock products:",
      ", ".join(df.loc[df["stock_status"] == "Out of stock", "product"]))
print()

# Q5: category summary — revenue, total profit, average margin
# (CTE equivalent: aggregate once, then reuse)
cat = (df.groupby("category")
         .agg(products=("product", "count"),
              revenue=("revenue", "sum"),
              total_profit=("total_profit", "sum"),
              avg_margin_pct=("margin_pct", "mean"))
         .sort_values("total_profit", ascending=False))
print("Q5 — Category summary")
print(cat.to_string(float_format=lambda x: f"{x:,.2f}"))
print()

# Q6: top 3 products by total profit
top3 = df.nlargest(3, "total_profit")[["product", "category", "total_profit", "margin_pct"]]
print("Q6 — Top 3 products by total profit")
print(top3.to_string(index=False))
