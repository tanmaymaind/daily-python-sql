-- Q1 — Total revenue and order count by month
SELECT strftime('%Y-%m', order_date) AS month,
       SUM(quantity * unit_price) AS total_revenue,
       COUNT(*) AS orders
FROM orders
GROUP BY month
ORDER BY month;

-- Q2 — Month-over-month revenue growth %
SELECT month, total_revenue, prev_revenue,
       ROUND((total_revenue - prev_revenue) * 100.0 / prev_revenue, 1) AS growth_pct
FROM (
    SELECT strftime('%Y-%m', order_date) AS month,
           SUM(quantity * unit_price) AS total_revenue,
           LAG(SUM(quantity * unit_price)) OVER (ORDER BY strftime('%Y-%m', order_date)) AS prev_revenue
    FROM orders
    GROUP BY month
)
ORDER BY month;

-- Q3 — Best month by revenue
SELECT strftime('%Y-%m', order_date) AS month,
       SUM(quantity * unit_price) AS total_revenue,
       COUNT(*) AS orders
FROM orders
GROUP BY month
ORDER BY total_revenue DESC
LIMIT 1;

-- Q4 — Average order value by month
SELECT strftime('%Y-%m', order_date) AS month,
       ROUND(AVG(quantity * unit_price), 2) AS avg_order_value
FROM orders
GROUP BY month
ORDER BY month;

-- Q5 — Weekend vs weekday orders
SELECT CASE WHEN strftime('%w', order_date) IN ('0', '6') THEN 'Weekend' ELSE 'Weekday' END AS day_type,
       COUNT(*) AS orders,
       SUM(quantity * unit_price) AS total_revenue
FROM orders
GROUP BY day_type
ORDER BY day_type;

-- Q6 — Quarterly totals (Q1 vs Q2 2026)
SELECT CASE WHEN CAST(strftime('%m', order_date) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1' ELSE 'Q2' END AS quarter,
       SUM(quantity * unit_price) AS total_revenue,
       COUNT(*) AS orders
FROM orders
GROUP BY quarter
ORDER BY quarter;
