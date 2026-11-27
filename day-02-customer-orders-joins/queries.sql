-- Q1 — How many customers placed at least one order? (INNER JOIN)
SELECT COUNT(DISTINCT c.customer_id) AS customers_with_orders
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- Q2 — Which customers never placed an order? (LEFT JOIN ... IS NULL)
SELECT c.customer_id, c.name, c.city
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id;

-- Q3 — Top 5 customers by total revenue (JOIN + GROUP BY)
SELECT c.customer_id, c.name, c.city,
       SUM(o.quantity * o.unit_price) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_spent DESC, c.customer_id ASC
LIMIT 5;

-- Q4 — Revenue and order count by city (JOIN + GROUP BY)
SELECT c.city, COUNT(o.order_id) AS orders,
       SUM(o.quantity * o.unit_price) AS revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY revenue DESC;

-- Q5 — Customers with more than one order (JOIN + GROUP BY + HAVING)
SELECT c.customer_id, c.name, COUNT(o.order_id) AS order_count,
       SUM(o.quantity * o.unit_price) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 1
ORDER BY order_count DESC, total_spent DESC, c.customer_id ASC;

-- Q6 — Top 3 customers' share of total revenue (subquery)
SELECT ROUND(100.0 * top3.total / all_orders.total, 2) AS top3_share_pct
FROM (SELECT SUM(quantity * unit_price) AS total FROM orders
      WHERE customer_id IN (
          SELECT customer_id FROM orders
          GROUP BY customer_id
          ORDER BY SUM(quantity * unit_price) DESC
          LIMIT 3)) AS top3,
     (SELECT SUM(quantity * unit_price) AS total FROM orders) AS all_orders;
