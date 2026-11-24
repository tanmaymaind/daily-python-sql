"""Day 8 — HAVING vs WHERE: food-delivery orders (Python / pandas).

Dataset: 24 food-delivery orders from 5 Indian cities
(data/orders.csv), including 2 cancelled orders with no rating.
The point of the day: WHERE filters rows *before* grouping, HAVING
filters groups *after* grouping. Same 6 business questions as
queries.sql — answers must match the SQL run.
"""
import pandas as pd

df = pd.read_csv("data/orders.csv")
df["amount"] = df["quantity"] * df["unit_price"]
delivered = df[df["status"] == "Delivered"].copy()
print(f"Orders: {len(df)}, delivered: {len(delivered)}, "
      f"cancelled: {int((df['status'] == 'Cancelled').sum())}")
print()

# ---- Q1: revenue by city, delivered orders only (WHERE) ------------------
print("Q1 — Revenue by city (Delivered orders only)")
q1 = (delivered.groupby("city")
      .agg(orders=("order_id", "count"),
           revenue=("amount", "sum"))
      .reset_index()
      .sort_values(["revenue", "city"], ascending=[False, True]))
print(q1.to_string(index=False))
print(f"Total delivered revenue: {int(delivered['amount'].sum())}")
print()

# ---- Q2: cities with total delivered revenue above Rs. 1,500 (HAVING) ----
print("Q2 — Cities with total delivered revenue above Rs. 1,500")
q2 = q1[q1["revenue"] > 1500]
print(q2.to_string(index=False))
print(f"Cities above Rs. 1,500: {len(q2)}")
print()

# ---- Q3: customers who ordered more than once (HAVING COUNT) ------------
print("Q3 — Customers who ordered more than once")
q3 = (delivered.groupby(["customer_name", "city"])
      .agg(orders=("order_id", "count"),
           total_spend=("amount", "sum"))
      .reset_index()
      .query("orders > 1")
      .sort_values(["orders", "total_spend"],
                   ascending=[False, False]))
print(q3.to_string(index=False))
print(f"Repeat customers (2+ orders): {len(q3)}")
print()

# ---- Q4: cuisines with avg rating >= 4.0 and 3+ rated orders (HAVING) ----
print("Q4 — Cuisines with avg rating >= 4.0 and 3+ rated orders")
rated = delivered.dropna(subset=["rating"])
q4 = (rated.groupby("cuisine")
      .agg(rated_orders=("rating", "count"),
           avg_rating=("rating", lambda s: round(s.mean(), 2)))
      .reset_index()
      .query("avg_rating >= 4.0 and rated_orders >= 3")
      .sort_values(["avg_rating", "cuisine"],
                   ascending=[False, True]))
print(q4.to_string(index=False))
print(f"Cuisines passing both filters: {len(q4)}")
print()

# ---- Q5: the contrast — WHERE on rows vs HAVING on groups ----------------
print("Q5a — Revenue by city from orders above Rs. 300 only (WHERE on rows)")
q5a = (delivered[delivered["amount"] > 300]
       .groupby("city")
       .agg(big_orders=("order_id", "count"),
            revenue=("amount", "sum"))
       .reset_index()
       .sort_values(["revenue", "city"], ascending=[False, True]))
print(q5a.to_string(index=False))
print(f"Cities with at least one order above Rs. 300: {len(q5a)}")
print()
print("Q5b — Cities whose AVERAGE order value is above Rs. 300 "
      "(HAVING on groups)")
q5b = (delivered.groupby("city")
       .agg(orders=("order_id", "count"),
            avg_order_value=("amount", lambda s: round(s.mean(), 2)))
       .reset_index()
       .query("avg_order_value > 300")
       .sort_values(["avg_order_value", "city"],
                    ascending=[False, True]))
print(q5b.to_string(index=False))
print(f"Cities with average order value above Rs. 300: {len(q5b)}")
print()

# ---- Q6: top 3 customers by spend, total spend above Rs. 700 ------------
print("Q6 — Top 3 customers by spend (total spend above Rs. 700)")
q6 = (delivered.groupby(["customer_name", "city"])
      .agg(orders=("order_id", "count"),
           total_spend=("amount", "sum"))
      .reset_index()
      .query("total_spend > 700")
      .sort_values("total_spend", ascending=False)
      .head(3))
print(q6.to_string(index=False))
print(f"Customers with total spend above Rs. 700: "
      f"{int((delivered.groupby('customer_name')['amount'].sum() > 700).sum())}")
