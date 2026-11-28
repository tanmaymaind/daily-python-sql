"""Day 11 — Subqueries: classic interview questions on ~500 employees (Python / pandas).

Dataset: data/employees.csv (524 rows) + data/orders.csv (624 rows) for a
Pune IT-services company (synthetic practice data, seed 42; see README for
the dirt that was planted in it). Same 6 business questions as queries.sql —
answers must match the SQL run.

Cleaning (identical in both scripts):
  1. employees: drop rows with a missing salary,
  2. drop rows with salary <= 0,
  3. drop duplicate employee_id values (keep the first),
  4. tidy the department text into its canonical name.
  5. orders: drop rows with a missing order_amount,
  6. drop duplicate order_id values (keep the first).

Every question below is a subquery in SQL: a scalar subquery (Q1, Q6),
a correlated subquery (Q2), a MAX-inside-MAX subquery (Q3), a subquery
in HAVING (Q4) and NOT EXISTS (Q5). In pandas each one is a two-step
job: compute the inner value first, then filter with it — exactly what
a subquery does.
"""
from decimal import Decimal, ROUND_HALF_UP

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DEPT_CANON = {
    "engineering": "Engineering",
    "sales": "Sales",
    "finance": "Finance",
    "hr": "HR",
    "marketing": "Marketing",
    "operations": "Operations",
}


def round2(x):
    """Round half-up to 2 decimals, like SQLite ROUND()."""
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def inr(x):
    return f"Rs. {x:,.0f}"


emp = pd.read_csv("data/employees.csv")
ord_ = pd.read_csv("data/orders.csv")
print(f"Raw rows: {len(emp)} employees, {len(ord_)} orders")

# --- cleaning (employees) ---
n_missing_sal = emp["salary"].isna().sum()
emp = emp.dropna(subset=["salary"])
n_bad_sal = (emp["salary"] <= 0).sum()
emp = emp[emp["salary"] > 0]
n_dup_emp = emp.duplicated(subset=["employee_id"]).sum()
emp = emp.drop_duplicates(subset=["employee_id"], keep="first")
emp["department"] = emp["department"].str.strip().str.lower().map(DEPT_CANON)
print(f"Employees dropped: {n_missing_sal} missing salary, {n_bad_sal} salary <= 0, "
      f"{n_dup_emp} duplicate employee_id")
print(f"Clean employees: {len(emp)}")

# --- cleaning (orders) ---
n_missing_amt = ord_["order_amount"].isna().sum()
ord_ = ord_.dropna(subset=["order_amount"])
n_dup_ord = ord_.duplicated(subset=["order_id"]).sum()
ord_ = ord_.drop_duplicates(subset=["order_id"], keep="first")
print(f"Orders dropped: {n_missing_amt} missing order_amount, {n_dup_ord} duplicate order_id")
print(f"Clean orders: {len(ord_)}")
print()

# Q1: employees earning above the company average salary (scalar subquery)
avg_sal = emp["salary"].mean()
above_avg = emp[emp["salary"] > avg_sal].sort_values("salary", ascending=False)
print(f"Q1 — Company average salary: {inr(round2(avg_sal))}")
print(f"     Employees above average: {len(above_avg)} of {len(emp)} "
      f"({round2(100 * len(above_avg) / len(emp))}%)")
print(f"     Their average salary: {inr(round2(above_avg['salary'].mean()))}")
print("     Top 5: " + "; ".join(
    f"{r['name']} ({r['department']}, {inr(r['salary'])})" for _, r in above_avg.head(5).iterrows()))
print()

# Q2: employees earning above their OWN department's average (correlated subquery)
dept_avg = emp.groupby("department")["salary"].transform("mean")
above_dept = emp[emp["salary"] > dept_avg]
per_dept = (above_dept.groupby("department").size()
            .reindex(emp.groupby("department").size().index, fill_value=0))
print("Q2 — Employees above their own department average:")
for d in sorted(emp["department"].unique()):
    da = emp.loc[emp["department"] == d, "salary"].mean()
    print(f"     {d}: {per_dept[d]} of {(emp['department'] == d).sum()} "
          f"(dept avg {inr(round2(da))})")
print(f"     Total above own dept average: {len(above_dept)}")
print()

# Q3: second-largest order amount (MAX inside MAX)
largest = ord_["order_amount"].max()
second = ord_.loc[ord_["order_amount"] < largest, "order_amount"].max()
second_rows = ord_[ord_["order_amount"] == second]
print(f"Q3 — Largest order: {inr(largest)}")
print(f"     Second-largest order: {inr(second)} "
      f"({len(second_rows)} order(s): " + ", ".join(
          f"{r['order_id']} by {r['employee_id']}" for _, r in second_rows.iterrows()) + ")")
print()

# Q4: departments whose average salary is above the company average (subquery in HAVING)
dept_summary = (emp.groupby("department")["salary"]
                .agg(["count", "mean"]).reset_index())
rich_depts = dept_summary[dept_summary["mean"] > avg_sal].sort_values("mean", ascending=False)
print("Q4 — Departments with average salary above the company average:")
for _, r in rich_depts.iterrows():
    print(f"     {r['department']}: {int(r['count'])} employees, avg {inr(round2(r['mean']))}")
print()

# Q5: employees who never placed an order (NOT EXISTS)
ordered_ids = set(ord_["employee_id"])
never = emp[~emp["employee_id"].isin(ordered_ids)].sort_values("salary", ascending=False)
print(f"Q5 — Employees with no orders at all: {len(never)} of {len(emp)}")
print("     Highest-paid with no orders: " + "; ".join(
    f"{r['name']} ({r['department']}, {inr(r['salary'])})" for _, r in never.head(3).iterrows()))
print()

# Q6: orders above the average order amount (scalar subquery)
avg_amt = ord_["order_amount"].mean()
big = ord_[ord_["order_amount"] > avg_amt]
print(f"Q6 — Average order amount: {inr(round2(avg_amt))}")
print(f"     Orders above average: {len(big)} of {len(ord_)} "
      f"({round2(100 * len(big) / len(ord_))}%), worth {inr(big['order_amount'].sum())} "
      f"of {inr(ord_['order_amount'].sum())} total "
      f"({round2(100 * big['order_amount'].sum() / ord_['order_amount'].sum())}%)")
print()

# --- chart: average salary by department vs company average ---
order = dept_summary.sort_values("mean")
colors = ["#c0392b" if m > avg_sal else "#2e86ab" for m in order["mean"]]
fig, ax = plt.subplots(figsize=(9, 4.6))
ax.barh(order["department"], order["mean"], color=colors)
ax.axvline(avg_sal, color="#e67e22", linestyle="--", linewidth=1.5,
           label=f"Company average {inr(round2(avg_sal))}")
for i, v in enumerate(order["mean"]):
    ax.text(v + 1500, i, inr(round2(v)), va="center", fontsize=9)
ax.set_xlabel("Average salary (Rs.)")
ax.set_title("Average salary by department — who beats the company average?")
ax.legend(loc="lower right")
ax.set_xlim(0, max(order["mean"]) * 1.18)
fig.tight_layout()
fig.savefig("chart.svg")
print("Chart saved to chart.svg")
