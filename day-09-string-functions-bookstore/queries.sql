-- Day 9 — String Functions: bookstore catalogue (SQL / SQLite).
-- Dataset: data/books.csv — 23 books from a small Indian bookstore
-- across 6 categories. The point of the day: text is data too — LIKE /
-- contains, LENGTH, SUBSTR, UPPER and concatenation let you search,
-- measure and reformat titles and author names. Same 6 business
-- questions as python_analysis.py — answers must match the pandas run.

-- Q1: Books per category and average price
SELECT category, COUNT(*) AS books,
       ROUND(AVG(price), 2) AS avg_price
FROM books
GROUP BY category
ORDER BY books DESC, avg_price DESC;

-- Q2: Titles containing "Guide"
SELECT title, author, category, price
FROM books
WHERE title LIKE '%Guide%'
ORDER BY title ASC;

-- Q3: Longest title in each category (ties included)
WITH lens AS (
    SELECT category, title, LENGTH(title) AS title_len
    FROM books
)
SELECT category, title, title_len
FROM lens
WHERE title_len = (SELECT MAX(LENGTH(title))
                   FROM books b2
                   WHERE b2.category = lens.category)
ORDER BY category ASC, title ASC;

-- Q4: Titles starting with "The"
SELECT title, author, category
FROM books
WHERE title LIKE 'The %'
ORDER BY title ASC;

-- Q5: Authors whose surname starts with "S"
-- (every author name is "Firstname Surname", so the surname is the text
-- after the first space)
SELECT title, author,
       SUBSTR(author, INSTR(author, ' ') + 1) AS surname
FROM books
WHERE SUBSTR(author, INSTR(author, ' ') + 1) LIKE 'S%'
ORDER BY surname ASC;

-- Q6: Shelf labels (UPPERCASE) for the 5 most expensive books
SELECT UPPER(title) || ' BY ' || UPPER(author) AS shelf_label, price
FROM books
ORDER BY price DESC
LIMIT 5;
