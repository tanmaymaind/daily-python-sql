# Day 6 — Data Cleaning: Nulls, Duplicates & Types

Day 6 is the unglamorous one — and probably the most important so far. A
Pune online grocery store's customer sign-up list arrived messy: the same
person signed up twice, emails were typed in different cases, phones came
with a `+91` prefix or too few digits, cities were spelled
inconsistently, and a few fields were blank. Before any analysis, the
data had to be cleaned — same rules in pandas and in SQLite, with
identical results.

## Dataset

`data/customers_raw.csv` — 22 raw sign-up rows, 7 columns
(`customer_id`, `name`, `email`, `phone`, `city`, `pincode`,
`signup_date`). The mess is deliberate, and all of it is realistic:

- Rows 12 and 22 are exact re-sign-ups of rows 2 and 7 (new `customer_id`,
  same everything else).
- Aarav, Priya, Rahul and Rohit each appear twice under the same email in
  different cases (`AARAV.SHARMA@GMAIL.COM` vs `aarav.sharma@gmail.com`).
- Missing values: Arjun has no email, Ananya and Sanjay have no phone,
  Pooja has no city.
- `mumbai` / `pune` in lowercase, `Pune ` with a trailing space.
- Divya's phone is `+91 9876543210`; Rohit's is only 9 digits.
- Kavya's pincode is `4000` and Sanjay's is `4110` — both too short.

## Cleaning rules (same in Python and SQL)

1. Drop exact duplicate rows (ignoring `customer_id`, which differs on a
   re-sign-up).
2. Compare emails case-insensitively; keep the first row per email.
3. Drop rows with no email — the customer cannot be contacted.
4. Trim and title-case city names; a blank city becomes `Unknown`.
5. Phone is valid when, after removing spaces and a leading `+91`, it is
   exactly 10 digits. Pincode is valid when exactly 6 digits.

## Questions & results

| # | Question | Answer |
|---|----------|--------|
| Q1 | Rows in the raw file / exact duplicates | 22 rows, 2 exact duplicates |
| Q2 | Missing values per column | email 1, phone 2, city 1, name 0, pincode 0, signup_date 0 |
| Q3 | Duplicate emails (case-insensitive) | 4 emails appear twice: aarav.sharma, priya.patel, rahul.verma, rohit.kumar — 4 extra rows |
| Q4 | Usable customers after cleaning | 22 → 20 after dropping exact duplicates → 18 after de-duplicating by email → **17** unique customers |
| Q5 | Customers per city (cleaned) | Pune 7, Mumbai 5, Nashik 2, Nagpur 2, Unknown 1 |
| Q6 | Phone / pincode validity (cleaned) | Phone: 14 valid, 1 invalid (Rohit Kumar), 2 missing. Pincode: 15 valid, 2 invalid (Kavya Nair, Sanjay Rao), 0 missing |

## Before / after cleaning

| Step | Rows left |
|------|-----------|
| Raw sign-ups, as the file arrived | 22 |
| After dropping exact duplicate rows | 20 |
| After keeping one row per email (case-insensitive) | 18 |
| After dropping rows with no email | **17 usable customers** |

## What I found

- 5 of the 22 rows (about 23%) were duplicates or unusable. Without cleaning, the store would report 22 customers when it really has 17 — and every per-customer number after that (average spend, repeat rate) would be quietly wrong.
- 4 people signed up twice with the same email typed in different cases. Counted raw, growth looks better than it is, and those 4 would get every offer and message twice.
- Even the cleaned list is not fully reachable: Rohit Kumar's phone has only 9 digits, and Kavya Nair's and Sanjay Rao's pincodes are too short. Those deliveries and calls would fail — a simple length check on the sign-up form would have stopped all three at the door.

## Python vs SQL approach

| Step | Python (pandas) | SQL (SQLite) |
|------|-----------------|--------------|
| Exact duplicates | `df.duplicated(subset=content_cols)` | `GROUP BY` all content columns, keep `MIN(customer_id)` |
| Missing values | `(df[col].str.strip() == "").sum()` | `SUM(CASE WHEN TRIM(col) = '' ...)` |
| Duplicate emails | `groupby(email.str.lower())` | `GROUP BY LOWER(TRIM(email)) HAVING COUNT(*) > 1` |
| First row per email | `drop_duplicates(subset="email_norm")` | `ROW_NUMBER() OVER (PARTITION BY LOWER(TRIM(email)) ...)` |
| City normalising | `str.strip().str.title()`, blank → `Unknown` | `UPPER(SUBSTR(...)) \|\| LOWER(SUBSTR(...))`, blank → `Unknown` |
| Phone/pincode check | `len == 10 / 6 and str.isdigit()` | `LENGTH(...) = 10 / 6 AND ... NOT GLOB '*[^0-9]*'` |

## How to run

```bash
python3 python_analysis.py   # pandas version
python3 sql_analysis.py      # loads the CSV into SQLite and runs queries.sql
```

Both print the same answers. The biggest lesson: **5 of the 22 rows (23%)
were unusable or duplicated** — cleaning first is what makes every later
analysis trustworthy. A dashboard built on dirty data is just a confident
mistake.
