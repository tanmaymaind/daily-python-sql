-- Day 1 — Sales analysis in SQL (SQLite).
-- Same business questions as python_analysis.py, answered in SQL.
-- Table: sales(order_id, date, region, product, category, quantity, unit_price)

-- Q1: Total revenue
SELECT ROUND(SUM(quantity * unit_price), 2) AS total_revenue FROM sales;

-- Q2: Revenue by region
SELECT region, ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM sales GROUP BY region ORDER BY revenue DESC;

-- Q3: Revenue by category
SELECT category, ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM sales GROUP BY category ORDER BY revenue DESC;

-- Q4: Top 3 products by revenue
SELECT product, ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM sales GROUP BY product ORDER BY revenue DESC LIMIT 3;

-- Q5: Average order value
SELECT ROUND(AVG(quantity * unit_price), 2) AS avg_order_value FROM sales;

-- Q6: Total units sold
SELECT SUM(quantity) AS total_units FROM sales;
