"""Day 10 — CTEs in Detail: monthly profitability on ~2,000 orders (Python / pandas).

Dataset: data/orders.csv — 2,008 rows of a Pune electronics store's orders,
Jan-Oct 2026 (synthetic practice data, seed 42; see README for the dirt
that was planted in it). Same 6 business questions as queries.sql —
answers must match the SQL run.

Cleaning (identical in both scripts):
  1. drop rows with a missing cost_price,
  2. drop rows with quantity <= 0,
  3. drop duplicate order_id values (keep the first),
  4. tidy the category text into its canonical name.
"""
from decimal import Decimal, ROUND_HALF_UP

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

CANONICAL = {
    "mobile": "Mobile",
    "laptop": "Laptop",
    "accessories": "Accessories",
    "tv & audio": "TV & Audio",
    "home appliances": "Home Appliances",
}


def round2(x):
    """Round half-up to 2 decimals, like SQLite ROUND()."""
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


df = pd.read_csv("data/orders.csv")
print(f"Raw rows in CSV: {len(df)}")

# --- cleaning ---
n_missing_cost = df["cost_price"].isna().sum()
df = df.dropna(subset=["cost_price"])
n_bad_qty = (df["quantity"] <= 0).sum()
df = df[df["quantity"] > 0]
n_dupes = df.duplicated(subset=["order_id"]).sum()
df = df.drop_duplicates(subset=["order_id"], keep="first")
df["category"] = df["category"].str.strip().str.lower().map(CANONICAL)
print(f"Dropped: {n_missing_cost} missing cost_price, {n_bad_qty} bad quantity, "
      f"{n_dupes} duplicate order_id")
print(f"Clean orders: {len(df)}")
print()

# --- derived columns ---
df["revenue"] = df["selling_price"] * df["quantity"]
df["profit"] = (df["selling_price"] - df["cost_price"]) * df["quantity"]
df["month"] = df["order_date"].str.slice(0, 7)

# Q1: monthly summary — the first CTE in queries.sql
monthly = (df.groupby("month")
             .agg(orders=("order_id", "count"),
                  revenue=("revenue", "sum"),
                  profit=("profit", "sum"))
             .reset_index())
monthly["margin_pct"] = (monthly["profit"] / monthly["revenue"] * 100).map(round2)
print("Q1 — Monthly summary (revenue, profit, margin)")
print(monthly.to_string(index=False))
print()

# Q2: rank the months by profit — the second CTE (RANK on top of Q1)
monthly["profit_rank"] = monthly["profit"].rank(method="min", ascending=False).astype(int)
print("Q2 — Months ranked by profit")
print(monthly[["month", "profit", "profit_rank"]]
      .sort_values("profit_rank").to_string(index=False))
best = monthly.loc[monthly["profit"].idxmax()]
worst = monthly.loc[monthly["profit"].idxmin()]
print(f"Best month: {best['month']} (profit Rs. {best['profit']:,}); "
      f"worst: {worst['month']} (profit Rs. {worst['profit']:,})")
print()

# Q3: best category in each month — RANK() PARTITION BY month
month_cat = (df.groupby(["month", "category"])
               .agg(profit=("profit", "sum"))
               .reset_index())
month_cat["cat_rank"] = (month_cat.groupby("month")["profit"]
                         .rank(method="min", ascending=False).astype(int))
best_cat = month_cat[month_cat["cat_rank"] == 1].sort_values("month")
print("Q3 — Best category in each month (by profit)")
print(best_cat.to_string(index=False))
print()

# Q4: category summary with margin band — same bands as Day 5
cat = (df.groupby("category")
         .agg(products=("product", "nunique"),
              orders=("order_id", "count"),
              revenue=("revenue", "sum"),
              profit=("profit", "sum"))
         .reset_index())
cat["margin_pct"] = (cat["profit"] / cat["revenue"] * 100).map(round2)
cat["margin_band"] = cat["margin_pct"].apply(
    lambda m: "High" if m >= 30 else ("Medium" if m >= 20 else "Low"))
print("Q4 — Category summary with margin band (High >= 30%, Medium >= 20%)")
print(cat.sort_values("profit", ascending=False).to_string(index=False))
print()

# Q5: month-on-month profit growth — LAG() on the monthly CTE
monthly["prev_profit"] = monthly["profit"].shift(1)
monthly["mom_growth_pct"] = (
    (monthly["profit"] - monthly["prev_profit"]) / monthly["prev_profit"] * 100
).map(lambda x: round2(x) if pd.notna(x) else None)
print("Q5 — Month-on-month profit growth (LAG on the monthly CTE)")
print(monthly[["month", "profit", "prev_profit", "mom_growth_pct"]]
      .to_string(index=False))
best_growth = monthly.loc[monthly["mom_growth_pct"].idxmax()]
print(f"Biggest jump: {best_growth['month']} "
      f"(+{best_growth['mom_growth_pct']}% vs {best_growth['prev_profit']:,} "
      f"the month before)")
print()

# Q6: top 3 months by profit, and the category that drove each one
top3 = monthly.nsmallest(3, "profit_rank")[["month", "profit", "profit_rank"]]
top3 = top3.merge(best_cat[["month", "category"]], on="month")
print("Q6 — Top 3 months and the category that drove each")
print(top3.to_string(index=False))
print()

print(f"TOTAL — clean orders: {len(df)}, total revenue Rs. "
      f"{int(df['revenue'].sum()):,}, total profit Rs. {int(df['profit'].sum()):,}, "
      f"overall margin {round2(df['profit'].sum() / df['revenue'].sum() * 100)}%")

# --- chart: monthly profit, best month highlighted ---
plt.figure(figsize=(10, 5))
colors = ["#c0392b" if m == best["month"] else "#2e86c1"
          for m in monthly["month"]]
plt.bar(monthly["month"], monthly["profit"], color=colors)
plt.ylabel("Profit (Rs.)")
plt.title("Monthly profit, Jan–Oct 2026 (best month in red)")
for i, v in enumerate(monthly["profit"]):
    plt.text(i, v + 8000, f"{v / 100000:.1f}L", ha="center", fontsize=8)
plt.tight_layout()
plt.savefig("chart.svg", format="svg")
print("Chart saved to chart.svg")
