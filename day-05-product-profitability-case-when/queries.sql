-- Day 5 — Product Profitability: CASE WHEN & CTEs (SQLite)
-- Dataset: products (20 rows, Pune electronics store)
-- Same 6 business questions as python_analysis.py — answers must match.

-- Q1: margin band per product (CASE WHEN)
SELECT product, category, selling_price,
       ROUND((selling_price - cost_price) * 100.0 / selling_price, 2) AS margin_pct,
       CASE
           WHEN (selling_price - cost_price) * 100.0 / selling_price >= 40 THEN 'High'
           WHEN (selling_price - cost_price) * 100.0 / selling_price >= 20 THEN 'Medium'
           ELSE 'Low'
       END AS margin_band
FROM products
ORDER BY margin_pct DESC;

-- Q2: products and total profit per margin band
WITH margins AS (
    SELECT product,
           (selling_price - cost_price) * units_sold AS total_profit,
           CASE
               WHEN (selling_price - cost_price) * 100.0 / selling_price >= 40 THEN 'High'
               WHEN (selling_price - cost_price) * 100.0 / selling_price >= 20 THEN 'Medium'
               ELSE 'Low'
           END AS margin_band
    FROM products
)
SELECT margin_band, COUNT(*) AS products, SUM(total_profit) AS total_profit
FROM margins
GROUP BY margin_band
ORDER BY CASE margin_band WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END;

-- Q2b: total profit across all products
SELECT SUM((selling_price - cost_price) * units_sold) AS total_profit_all
FROM products;

-- Q3: products priced above their category's average selling price (CTE)
WITH category_avg AS (
    SELECT category, AVG(selling_price) AS avg_price
    FROM products
    GROUP BY category
)
SELECT p.product, p.category, p.selling_price,
       ROUND(c.avg_price, 2) AS category_avg_price
FROM products p
JOIN category_avg c ON p.category = c.category
WHERE p.selling_price > c.avg_price
ORDER BY p.category, p.selling_price DESC;

-- Q4: stock status (CASE WHEN) and units sold by status
WITH stocked AS (
    SELECT product, units_sold,
           CASE
               WHEN stock_qty = 0 THEN 'Out of stock'
               WHEN stock_qty < 5 THEN 'Low stock'
               ELSE 'In stock'
           END AS stock_status
    FROM products
)
SELECT stock_status, COUNT(*) AS products, SUM(units_sold) AS units_sold
FROM stocked
GROUP BY stock_status
ORDER BY CASE stock_status WHEN 'In stock' THEN 1 WHEN 'Low stock' THEN 2 ELSE 3 END;

-- Q4b: which products are out of stock
SELECT product FROM products WHERE stock_qty = 0 ORDER BY product;

-- Q5: category summary (CTE: aggregate once, reuse)
WITH category_summary AS (
    SELECT category,
           COUNT(*) AS products,
           SUM(selling_price * units_sold) AS revenue,
           SUM((selling_price - cost_price) * units_sold) AS total_profit,
           AVG((selling_price - cost_price) * 100.0 / selling_price) AS avg_margin_pct
    FROM products
    GROUP BY category
)
SELECT category, products, revenue, total_profit,
       ROUND(avg_margin_pct, 2) AS avg_margin_pct
FROM category_summary
ORDER BY total_profit DESC;

-- Q6: top 3 products by total profit
SELECT product, category,
       (selling_price - cost_price) * units_sold AS total_profit,
       ROUND((selling_price - cost_price) * 100.0 / selling_price, 2) AS margin_pct
FROM products
ORDER BY total_profit DESC
LIMIT 3;
