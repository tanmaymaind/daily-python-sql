-- Day 8 — HAVING vs WHERE: food-delivery orders (SQL / SQLite).
-- Dataset: data/orders.csv — 24 food-delivery orders from 5 Indian
-- cities, including 2 cancelled orders with no rating. The point of
-- the day: WHERE filters rows *before* grouping, HAVING filters groups
-- *after* grouping. Same 6 business questions as python_analysis.py —
-- answers must match the pandas run.

-- Q1: Revenue by city (Delivered orders only)
SELECT city, COUNT(*) AS orders,
       SUM(quantity * unit_price) AS revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY city
ORDER BY revenue DESC, city ASC;

-- Q2: Cities with total delivered revenue above Rs. 1,500
SELECT city, COUNT(*) AS orders,
       SUM(quantity * unit_price) AS revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY city
HAVING SUM(quantity * unit_price) > 1500
ORDER BY revenue DESC, city ASC;

-- Q3: Customers who ordered more than once
SELECT customer_name, city, COUNT(*) AS orders,
       SUM(quantity * unit_price) AS total_spend
FROM orders
WHERE status = 'Delivered'
GROUP BY customer_name, city
HAVING COUNT(*) > 1
ORDER BY orders DESC, total_spend DESC;

-- Q4: Cuisines with avg rating >= 4.0 and 3+ rated orders
SELECT cuisine, COUNT(rating) AS rated_orders,
       ROUND(AVG(rating), 2) AS avg_rating
FROM orders
WHERE status = 'Delivered'
GROUP BY cuisine
HAVING AVG(rating) >= 4.0 AND COUNT(rating) >= 3
ORDER BY avg_rating DESC, cuisine ASC;

-- Q5a: Revenue by city from orders above Rs. 300 only (WHERE on rows)
WITH amounts AS (
    SELECT city, quantity * unit_price AS amount
    FROM orders
    WHERE status = 'Delivered'
)
SELECT city, COUNT(*) AS big_orders, SUM(amount) AS revenue
FROM amounts
WHERE amount > 300
GROUP BY city
ORDER BY revenue DESC, city ASC;

-- Q5b: Cities whose AVERAGE order value is above Rs. 300 (HAVING on groups)
WITH amounts AS (
    SELECT city, quantity * unit_price AS amount
    FROM orders
    WHERE status = 'Delivered'
)
SELECT city, COUNT(*) AS orders,
       ROUND(AVG(amount), 2) AS avg_order_value
FROM amounts
GROUP BY city
HAVING AVG(amount) > 300
ORDER BY avg_order_value DESC, city ASC;

-- Q6: Top 3 customers by spend (total spend above Rs. 700)
SELECT customer_name, city, COUNT(*) AS orders,
       SUM(quantity * unit_price) AS total_spend
FROM orders
WHERE status = 'Delivered'
GROUP BY customer_name, city
HAVING SUM(quantity * unit_price) > 700
ORDER BY total_spend DESC
LIMIT 3;
