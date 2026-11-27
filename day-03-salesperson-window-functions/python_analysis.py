"""Day 3 — Salesperson performance with pandas (window functions).

Business questions (same questions as queries.sql, answered in Python):
  Q1  Rank salespeople by total revenue within each region (RANK)
  Q2  Running total of revenue per region across months (cumulative SUM)
  Q3  Top 3 salespeople overall by total revenue (ROW_NUMBER)
  Q4  Month-over-month revenue growth per salesperson (LAG)
  Q5  Best month for each salesperson (ROW_NUMBER per salesperson)
  Q6  Each salesperson's total vs their region's average (AVG window)

Run:  python3 python_analysis.py
"""

import pandas as pd

df = pd.read_csv("data/monthly_sales.csv")

totals = (df.groupby(["region", "salesperson"], as_index=False)["revenue"]
          .sum().rename(columns={"revenue": "total_revenue"}))

print("Q1 — Salespeople ranked by total revenue within each region:")
ranked = totals.copy()
ranked["rank_in_region"] = (ranked.groupby("region")["total_revenue"]
                            .rank(ascending=False, method="min").astype(int))
ranked = ranked.sort_values(["region", "rank_in_region"])
print(ranked.to_string(index=False))
print()
print("Q2 — Running total of revenue per region, month by month:")
monthly = (df.groupby(["region", "month"], as_index=False)["revenue"]
           .sum().rename(columns={"revenue": "month_revenue"}))
monthly = monthly.sort_values(["region", "month"])
monthly["running_total"] = monthly.groupby("region")["month_revenue"].cumsum()
print(monthly.to_string(index=False))
print()
print("Q3 — Top 3 salespeople overall by total revenue:")
top3 = (totals.sort_values(["total_revenue", "salesperson"],
                           ascending=[False, True]).head(3).copy())
top3["overall_rank"] = range(1, len(top3) + 1)
print(top3[["overall_rank", "salesperson", "region", "total_revenue"]]
      .to_string(index=False))
print()
print("Q4 — Month-over-month revenue growth per salesperson (%):")
mom = df.sort_values(["salesperson", "month"]).copy()
mom["prev_revenue"] = mom.groupby("salesperson")["revenue"].shift(1)
mom["growth_pct"] = ((mom["revenue"] - mom["prev_revenue"])
                     / mom["prev_revenue"] * 100).round(1)
prev_list = [None if pd.isna(v) else int(v) for v in mom["prev_revenue"]]
growth_list = [None if pd.isna(v) else v for v in mom["growth_pct"]]
print(f"{'salesperson':<15}{'month':<10}{'revenue':>9}{'prev_revenue':>14}{'growth_pct':>12}")
for (_, r), prev, growth in zip(mom.iterrows(), prev_list, growth_list):
    print(f"{r['salesperson']:<15}{r['month']:<10}{r['revenue']:>9}"
          f"{str(prev):>14}{str(growth):>12}")
print()
print("Q5 — Best month for each salesperson:")
best = df.copy()
best["rn"] = (best.groupby("salesperson")["revenue"]
              .rank(ascending=False, method="first").astype(int))
best = best[best["rn"] == 1].sort_values("salesperson")
print(best[["salesperson", "region", "month", "revenue"]]
      .to_string(index=False))
print()
print("Q6 — Each salesperson's total vs their region's average:")
vs_avg = totals.copy()
vs_avg["region_avg"] = (vs_avg.groupby("region")["total_revenue"]
                        .transform("mean")).astype(int)
vs_avg["diff_from_avg"] = (vs_avg["total_revenue"] - vs_avg["region_avg"]).astype(int)
vs_avg = vs_avg.sort_values(["region", "total_revenue"], ascending=[True, False])
print(vs_avg.to_string(index=False))
print()
print("Total revenue (all salespeople, Jul–Sep 2026): Rs.",
      f"{df['revenue'].sum():,.0f}")

# --- Chart (added 2026-11-27) -------------------------------------------
# Running total of revenue per region across months, line chart -> chart.svg
# (Re-reads the CSV and recomputes Q2; prints nothing.)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_d = pd.read_csv("data/monthly_sales.csv")
_m = (_d.groupby(["region", "month"], as_index=False)["revenue"]
      .sum().rename(columns={"revenue": "month_revenue"}))
_m = _m.sort_values(["region", "month"])
_m["running_total"] = _m.groupby("region")["month_revenue"].cumsum()
fig, ax = plt.subplots(figsize=(8, 4.5))
for region, g in _m.groupby("region"):
    ax.plot(g["month"], g["running_total"], marker="o", label=region)
ax.set_ylabel("Running total revenue (Rs.)")
ax.set_title("Running total of revenue by region (Jul–Sep 2026)")
ax.legend()
fig.tight_layout()
fig.savefig("chart.svg", format="svg")
plt.close(fig)
