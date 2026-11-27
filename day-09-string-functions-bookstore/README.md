# Day 9 — String Functions: Bookstore Catalogue

Day 9 is about text. A small Indian bookstore wants its catalogue to work
harder — find the "Guide" books, spot the longest titles, group authors
by surname, and print tidy shelf labels. Text is data too: `LIKE` /
`contains`, `LENGTH`, `SUBSTR` / `INSTR`, `UPPER` and `||` concatenation
do the job in both pandas and SQLite, with identical results.

## Dataset

`data/books.csv` — 23 books, 6 columns (`book_id`, `title`, `author`,
`category`, `price`, `stock`). 6 categories: Fiction (8), Self-Help
(5), History (3), Exam Prep (3), Children (3), Biography (1). Total
stock: 889 copies. Every author name is "Firstname Surname", which is
what makes the Q5 surname trick work.

## Questions & results

| # | Question | Answer |
|---|----------|--------|
| Q1 | Books per category and average price | Fiction 8 (avg ₹411.63); Self-Help 5 (₹359.20); History 3 (₹549.33); Exam Prep 3 (₹533.00); Children 3 (₹216.00); Biography 1 (₹250.00). History has the highest average price |
| Q2 | Titles containing "Guide" | 3 — "The Guide" (₹299), "A Guide to Effective Communication" (₹299), "Indian Polity: A Complete Guide" (₹750) |
| Q3 | Longest title in each category | Self-Help 34 chars ("A Guide to Effective Communication"); Exam Prep 31 ("Indian Polity: A Complete Guide"); Biography 25 ("My Experiments with Truth"); History 24 ("The Argumentative Indian"); Children 15 ("The Jungle Book"); Fiction 23 — a three-way tie ("The God of Small Things", "The Immortals of Meluha", "The Inheritance of Loss") |
| Q4 | Titles starting with "The" | 9 of 23 (39.1%) — "The" is the most common opening word in the catalogue |
| Q5 | Authors whose surname starts with "S" | 3 — Amartya Sen ("The Argumentative Indian"), Vikram Seth ("A Suitable Boy"), Robin Sharma ("The Monk Who Sold His Ferrari") |
| Q6 | Shelf labels (UPPERCASE) for the 5 most expensive books | "A SUITABLE BOY BY VIKRAM SETH" ₹899; "INDIAN POLITY: A COMPLETE GUIDE BY M. LAXMIKANTH" ₹750; "INDIA AFTER GANDHI BY RAMACHANDRA GUHA" ₹699; "QUANTITATIVE APTITUDE BY R.S. AGGARWAL" ₹650; "ATOMIC HABITS BY JAMES CLEAR" ₹599 |

## What I found

- 9 of the 23 titles (39.1%) start with "The". The catalogue's naming is very repetitive — anyone searching or shelving by the first word hits the same word again and again, so the second word does the real work of finding a book.
- History has the highest average price (₹549.33) but only 3 books on the shelf. Fiction is the opposite: the biggest section (8 books) at a mid-level average (₹411.63). The shelf space — and most of the everyday selling — belongs to Fiction; History is premium but tiny.
- The most expensive book, "A Suitable Boy" at ₹899, costs about as much as 4 average Children's books (₹216 each). A handful of premium titles carry a big share of the catalogue's value, so those are the ones to keep in stock and on display.

## Python vs SQL approach

| Step | Python (pandas) | SQL (SQLite) |
|------|-----------------|--------------|
| Substring search | `df["title"].str.contains("Guide")` | `WHERE title LIKE '%Guide%'` |
| Starts-with | `df["title"].str.startswith("The ")` | `WHERE title LIKE 'The %'` |
| String length | `df["title"].str.len()` | `LENGTH(title)` |
| Longest per group | `groupby(...).transform("max")` filter | CTE with `LENGTH`, then `WHERE title_len = (SELECT MAX(...))` per category |
| Surname from full name | `df["author"].str.split().str[-1]` | `SUBSTR(author, INSTR(author, ' ') + 1)` |
| Uppercase + join | `str.upper() + " BY " + str.upper()` | `UPPER(title) \|\| ' BY ' \|\| UPPER(author)` |
| Average price | `round_half_up(s.mean())` — see note below | `ROUND(AVG(price), 2)` |
| Top N | `.nlargest(5, "price")` | `ORDER BY price DESC LIMIT 5` |

## Rounding note

This one caught me out, so it's worth writing down. Fiction's mean price
is exactly ₹411.625 (₹3,293 ÷ 8). Python's built-in `round()` uses
banker's rounding and gives ₹411.62, while SQLite's `ROUND()` rounds half
away from zero and gives ₹411.63. So the Python script rounds with
`decimal.Decimal` + `ROUND_HALF_UP` instead, and both scripts print the
same number. It's a small gotcha, but it's exactly the kind of thing
that bites you when the same analysis has to agree in two languages.

## What I learned

- **Rounding is not the same in every language.** Fiction's mean price
  is exactly ₹411.625 (₹3,293 ÷ 8). Python's built-in `round()` uses
  banker's rounding and gives ₹411.62, while SQLite's `ROUND()` rounds
  half away from zero and gives ₹411.63 — a 1-paisa difference that
  made the Python and SQL answers disagree. The Python script now
  rounds with `decimal.Decimal` + `ROUND_HALF_UP`, so both print
  ₹411.63. When the same analysis runs in two languages, even the
  rounding rule has to be agreed first.
- **String functions turn messy text into answerable questions** — a
  `LIKE '%Guide%'` finds the guidebooks, `LENGTH` finds the
  shelf-space hogs, and one `SUBSTR` + `INSTR` pulls every surname
  out of a full name.

## How to run

```bash
python3 python_analysis.py   # pandas version
python3 sql_analysis.py      # loads the CSV into SQLite and runs queries.sql
```

Both print the same answers. The biggest lesson: **string functions
turn messy text into answerable questions** — a `LIKE '%Guide%'` finds
the guidebooks, `LENGTH` finds the shelf-space hogs, and one `SUBSTR`
+ `INSTR` pulls every surname out of a full name.
