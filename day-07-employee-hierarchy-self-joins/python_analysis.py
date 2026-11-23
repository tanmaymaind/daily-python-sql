"""Day 7 — Employee Hierarchy: self-joins (Python / pandas).

Dataset: 20 employees of a Pune IT services company
(data/employees.csv). Every employee except the CEO reports to another
employee in the same table, so the table joins to itself. Same 6 business
questions as queries.sql — answers must match the SQL run.
"""
import pandas as pd

df = pd.read_csv("data/employees.csv")
# manager_id is blank for the CEO; keep it numeric-friendly for the merge.
df["manager_id"] = pd.to_numeric(df["manager_id"], errors="coerce")

# The self-join: each employee matched to the row of their own manager.
mgr = df[["emp_id", "name", "salary"]].rename(
    columns={"emp_id": "manager_id", "name": "manager_name",
             "salary": "manager_salary"})
joined = df.merge(mgr, on="manager_id", how="left")

# ---- Q1: every employee with their manager's name ------------------------
print("Q1 — Every employee with their manager's name")
q1 = joined[["emp_id", "name", "department", "manager_name",
             "salary"]].sort_values("emp_id")
print(q1.to_string(index=False))
print(f"Employees: {len(q1)}, employees with no manager: "
      f"{int(q1['manager_name'].isna().sum())}")
print()

# ---- Q2: employees who earn more than their direct manager ---------------
print("Q2 — Employees who earn more than their direct manager")
q2 = joined[joined["salary"] > joined["manager_salary"]].copy()
q2["diff"] = q2["salary"] - q2["manager_salary"]
q2 = q2[["name", "salary", "manager_name", "manager_salary",
         "diff"]].sort_values("diff", ascending=False)
print(q2.to_string(index=False))
print(f"Employees earning more than their manager: {len(q2)}")
print()

# ---- Q3: direct reports and team salary bill per manager -----------------
print("Q3 — Direct reports and team salary bill per manager")
q3 = (df.dropna(subset=["manager_id"])
      .groupby("manager_id")
      .agg(reports=("emp_id", "count"),
           team_salary_bill=("salary", "sum"))
      .reset_index()
      .merge(df[["emp_id", "name"]], left_on="manager_id",
             right_on="emp_id", how="left")
      .rename(columns={"name": "manager_name"})
      [["manager_name", "reports", "team_salary_bill"]]
      .sort_values(["reports", "manager_name"],
                   ascending=[False, True]))
print(q3.to_string(index=False))
print(f"Managers with at least one report: {len(q3)}, "
      f"total direct reports: {int(q3['reports'].sum())}")
print()

# ---- Q4: headcount and average salary by department -----------------------
print("Q4 — Headcount and average salary by department")
q4 = (df.groupby("department")
      .agg(headcount=("emp_id", "count"),
           avg_salary=("salary", lambda s: round(s.mean(), 2)))
      .reset_index()
      .sort_values(["headcount", "department"],
                   ascending=[False, True]))
print(q4.to_string(index=False))
print(f"Total salary bill: {int(df['salary'].sum())}")
print()

# ---- Q5: organisation depth — employees per level from the CEO -----------
print("Q5 — Organisation depth (levels from the CEO)")
by_id = df.set_index("emp_id")
level_of = {}


def level(emp_id):
    if emp_id not in level_of:
        mgr_id = by_id.loc[emp_id, "manager_id"]
        level_of[emp_id] = 0 if pd.isna(mgr_id) else level(int(mgr_id)) + 1
    return level_of[emp_id]


levels = pd.Series({e: level(e) for e in df["emp_id"]})
q5 = (levels.value_counts().sort_index().rename_axis("level")
      .reset_index(name="employees"))
print(q5.to_string(index=False))
print(f"Deepest level: {int(levels.max())}")
print()

# ---- Q6: full reporting chain for Nikhil Gupta, bottom-up -----------------
print("Q6 — Reporting chain for Nikhil Gupta (bottom-up)")
chain = []
emp_id = int(df.loc[df["name"] == "Nikhil Gupta", "emp_id"].iloc[0])
step = 0
while True:
    row = by_id.loc[emp_id]
    mgr_id = row["manager_id"]
    mgr_name = None if pd.isna(mgr_id) else by_id.loc[int(mgr_id), "name"]
    chain.append({"step": step, "name": row["name"],
                  "department": row["department"],
                  "salary": int(row["salary"]),
                  "manager_name": mgr_name})
    if pd.isna(mgr_id):
        break
    emp_id = int(mgr_id)
    step += 1
q6 = pd.DataFrame(chain)
print(q6.to_string(index=False))
print(f"Chain length (including Nikhil): {len(q6)}")
