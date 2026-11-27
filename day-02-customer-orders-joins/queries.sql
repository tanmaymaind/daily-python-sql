-- Day 2 — Customer + orders analysis in SQL (SQLite JOINs).
-- Same business questions as python_analysis.py, answered in SQL.
-- Tables: customers(customer_id, name, city, signup_date),
--         orders(order_id, customer_id, order_date, product, category,
--                quantity, unit_price)
-- Note: an order's amount is quantity * unit_price (same as Python).

-- Q1: How many customers placed at least one order? (INNER JOIN)
SELECT COUNT(DISTINCT c.customer_id) AS customers_who_ordered,
       (SELECT COUNT(*) FROM customers) AS total_customers
FROM customers c
INNER JOIN orders o ON o.customer_id = c.customer_id;

-- Q2: Which customers never placed an order? (LEFT JOIN ... IS NULL)
SELECT c.customer_id, c.name, c.city
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.customer_id IS NULL
ORDER BY c.customer_id;

-- Q3: Top 5 customers by total revenue (JOIN + GROUP BY)
SELECT c.customer_id, c.name, c.city,
       SUM(o.quantity * o.unit_price) AS total_revenue
FROM customers c
INNER JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_revenue DESC, c.customer_id
LIMIT 5;

-- Q4: Revenue and order count by city (JOIN + GROUP BY)
SELECT c.city,
       COUNT(o.order_id) AS orders,
       SUM(o.quantity * o.unit_price) AS revenue
FROM customers c
INNER JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY revenue DESC;

-- Q5: Customers with more than one order (JOIN + GROUP BY + HAVING)
SELECT c.customer_id, c.name,
       COUNT(o.order_id) AS order_count,
       SUM(o.quantity * o.unit_price) AS total_spent
FROM customers c
INNER JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 1
ORDER BY order_count DESC, total_spent DESC, c.customer_id;

-- Q6: Top 3 customers' share of total revenue (subquery)
WITH totals AS (
  SELECT customer_id, SUM(quantity * unit_price) AS amount
  FROM orders GROUP BY customer_id
),
top3 AS (
  SELECT SUM(amount) AS top3_revenue FROM (
    SELECT amount FROM totals ORDER BY amount DESC LIMIT 3
  )
),
all_total AS (
  SELECT SUM(quantity * unit_price) AS total_revenue FROM orders
)
SELECT top3_revenue,
       total_revenue,
       ROUND(100.0 * top3_revenue / total_revenue, 2) AS top3_share_pct
FROM top3, all_total;
