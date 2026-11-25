"""Day 9 — String Functions: bookstore catalogue (Python / pandas).

Dataset: 23 books from a small Indian bookstore (data/books.csv)
across 6 categories. The point of the day: text is data too — LIKE /
contains, LENGTH, SUBSTR, UPPER and concatenation let you search,
measure and reformat titles and author names. Same 6 business
questions as queries.sql — answers must match the SQL run.
"""
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP


def round_half_up(x, places=2):
    """Round like SQLite's ROUND (half away from zero), not pandas' default
    banker's rounding — e.g. Fiction's mean price 411.625 -> 411.63."""
    q = Decimal(1).scaleb(-places)
    return float(Decimal(str(x)).quantize(q, rounding=ROUND_HALF_UP))

df = pd.read_csv("data/books.csv")
print(f"Books: {len(df)}, categories: {df['category'].nunique()}, "
      f"total stock: {int(df['stock'].sum())}")
print()

# ---- Q1: books per category + average price -------------------------------
print("Q1 — Books per category and average price")
q1 = (df.groupby("category")
      .agg(books=("book_id", "count"),
           avg_price=("price", lambda s: round_half_up(s.mean())))
      .reset_index()
      .sort_values(["books", "avg_price"], ascending=[False, False]))
print(q1.to_string(index=False))
print()

# ---- Q2: titles containing "Guide" ---------------------------------------
print('Q2 — Titles containing "Guide"')
q2 = (df[df["title"].str.contains("Guide")]
      [["title", "author", "category", "price"]]
      .sort_values("title"))
print(q2.to_string(index=False))
print(f"Titles containing 'Guide': {len(q2)}")
print()

# ---- Q3: longest title in each category ----------------------------------
print("Q3 — Longest title in each category")
df["title_len"] = df["title"].str.len()
q3 = df[df["title_len"] == df.groupby("category")["title_len"].transform("max")]
q3 = q3[["category", "title", "title_len"]].sort_values(["category", "title"])
print(q3.to_string(index=False))
print(f"Longest title overall: "
      f"'{df.loc[df['title_len'].idxmax(), 'title']}' "
      f"({int(df['title_len'].max())} characters)")
print()

# ---- Q4: titles starting with "The" ---------------------------------------
print('Q4 — Titles starting with "The"')
q4 = df[df["title"].str.startswith("The ")][["title", "author", "category"]]
q4 = q4.sort_values("title")
print(q4.to_string(index=False))
print(f"Titles starting with 'The': {len(q4)} out of {len(df)} "
      f"({round(100 * len(q4) / len(df), 1)}%)")
print()

# ---- Q5: authors whose surname starts with "S" ---------------------------
print('Q5 — Authors whose surname starts with "S"')
df["surname"] = df["author"].str.split().str[-1]
q5 = df[df["surname"].str.startswith("S")][["title", "author", "surname"]]
q5 = q5.sort_values("surname")
print(q5.to_string(index=False))
print(f"Authors with a surname starting with 'S': {len(q5)}")
print()

# ---- Q6: UPPERCASE shelf labels for the 5 most expensive books -----------
print("Q6 — Shelf labels (UPPERCASE) for the 5 most expensive books")
top5 = df.nlargest(5, "price").copy()
top5["shelf_label"] = (top5["title"].str.upper() + " BY "
                       + top5["author"].str.upper())
q6 = top5[["shelf_label", "price"]].sort_values("price", ascending=False)
print(q6.to_string(index=False))
print()
