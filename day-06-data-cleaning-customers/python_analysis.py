"""Day 6 — Data Cleaning: nulls, duplicates & types (Python / pandas).

Dataset: 22 raw customer sign-ups for a Pune online grocery store
(data/customers_raw.csv). The file is deliberately messy: exact duplicate
rows, the same email in different cases, missing values, inconsistent
city casing/spacing, phones with a +91 prefix or too few digits, and
short pincodes. Same 6 business questions as queries.sql — answers must
match the SQL run.
"""
import pandas as pd

df = pd.read_csv("data/customers_raw.csv", dtype=str, keep_default_na=False)

# ---- Cleaning helpers (same rules as the SQL version) ---------------------
df["email_norm"] = df["email"].str.strip().str.lower()
df["city_norm"] = df["city"].str.strip().str.title()
df["phone_clean"] = (df["phone"].str.strip().str.replace(" ", "", regex=False)
                     .str.replace("+91", "", regex=False))
df["pincode_clean"] = df["pincode"].str.strip()

# Content columns define a sign-up; customer_id differs when the same
# person signs up again, so exact duplicates ignore the id.
CONTENT_COLS = ["name", "email", "phone", "city", "pincode", "signup_date"]

# ---- Q1: how big is the raw file, and how many exact duplicate rows? -----
print("Q1 — Raw file size and exact duplicates")
print(f"Rows in raw file: {len(df)}")
print(f"Exact duplicate rows: {int(df.duplicated(subset=CONTENT_COLS).sum())}")
print()

# ---- Q2: missing values per column ---------------------------------------
print("Q2 — Missing values per column")
for col in ["name", "email", "phone", "city", "pincode", "signup_date"]:
    missing = int((df[col].str.strip() == "").sum())
    print(f"  {col}: {missing}")
print()

# ---- Q3: duplicate emails (case-insensitive) ------------------------------
print("Q3 — Duplicate emails (case-insensitive, ignoring blanks)")
nonblank = df[df["email_norm"] != ""]
dup_emails = (nonblank.groupby("email_norm").size()
              .loc[lambda s: s > 1].sort_values(ascending=False))
print(dup_emails.to_string())
print(f"Email addresses appearing more than once: {len(dup_emails)}")
print(f"Extra rows from duplicate emails: {int((dup_emails - 1).sum())}")
print()

# ---- Q4: clean the data and count usable customers ------------------------
# Step 1: drop exact duplicate rows. Step 2: keep the first row per email
# (case-insensitive). Step 3: drop rows with no email at all.
clean = df.drop_duplicates(subset=CONTENT_COLS)
clean = clean.drop_duplicates(subset="email_norm", keep="first")
clean = clean[clean["email_norm"] != ""].copy()
clean["city_clean"] = clean["city_norm"].replace("", "Unknown")
print("Q4 — Customers after cleaning")
print(f"Rows after dropping exact duplicates: {len(df.drop_duplicates(subset=CONTENT_COLS))}")
print(f"Rows after de-duplicating by email: "
      f"{len(df.drop_duplicates(subset=CONTENT_COLS).drop_duplicates(subset='email_norm', keep='first'))}")
print(f"Usable unique customers (email present): {len(clean)}")
print()

# ---- Q5: customers per city (cleaned) -------------------------------------
print("Q5 — Customers per city (after cleaning)")
print(clean["city_clean"].value_counts().to_string())
print()

# ---- Q6: phone and pincode validity in the cleaned set --------------------
def phone_status(p):
    if p == "":
        return "Missing"
    if len(p) == 10 and p.isdigit():
        return "Valid"
    return "Invalid"

def pincode_status(p):
    if p == "":
        return "Missing"
    if len(p) == 6 and p.isdigit():
        return "Valid"
    return "Invalid"

clean["phone_status"] = clean["phone_clean"].apply(phone_status)
clean["pincode_status"] = clean["pincode_clean"].apply(pincode_status)
print("Q6 — Phone and pincode validity (cleaned customers)")
print("Phone:")
print(clean["phone_status"].value_counts()
      .reindex(["Valid", "Invalid", "Missing"], fill_value=0).to_string())
print("Pincode:")
print(clean["pincode_status"].value_counts()
      .reindex(["Valid", "Invalid", "Missing"], fill_value=0).to_string())
print()
print("Customers with an invalid phone:",
      ", ".join(clean.loc[clean["phone_status"] == "Invalid", "name"]))
print("Customers with an invalid pincode:",
      ", ".join(clean.loc[clean["pincode_status"] == "Invalid", "name"]))
