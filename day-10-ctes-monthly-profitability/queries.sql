-- Day 10 — CTEs in Detail: monthly profitability on ~2,000 orders.
-- One CTE chain, built step by step: cleaned -> monthly -> ranked.
-- Every query below is self-contained: it starts from the same cleaning
-- CTE so it can be run on its own. Answers must match python_analysis.py.

-- Q1: Monthly summary — revenue, profit and margin per month.
-- CTE 1 (cleaned): drop the dirty rows, tidy the category text, and
-- pre-compute revenue and profit per order. CTE 2 (monthly) rolls it up.
WITH cleaned AS (
    SELECT order_id,
           SUBSTR(order_date, 1, 7) AS month,
           product,
           CASE LOWER(TRIM(category))
               WHEN 'mobile' THEN 'Mobile'
               WHEN 'laptop' THEN 'Laptop'
               WHEN 'accessories' THEN 'Accessories'
               WHEN 'tv & audio' THEN 'TV & Audio'
               WHEN 'home appliances' THEN 'Home Appliances'
           END AS category,
           selling_price * quantity AS revenue,
           (selling_price - cost_price) * quantity AS profit
    FROM orders
    WHERE cost_price IS NOT NULL
      AND quantity > 0
      AND rowid IN (SELECT MIN(rowid) FROM orders GROUP BY order_id)
),
monthly AS (
    SELECT month,
           COUNT(*) AS orders,
           SUM(revenue) AS revenue,
           SUM(profit) AS profit,
           ROUND(SUM(profit) * 100.0 / SUM(revenue), 2) AS margin_pct
    FROM cleaned
    GROUP BY month
)
SELECT month, orders, revenue, profit, margin_pct
FROM monthly
ORDER BY month;

-- Q2: Rank the months by profit — a second CTE (ranked) on top of monthly.
-- This is the whole point of a CTE chain: each step feeds the next.
WITH cleaned AS (
    SELECT order_id,
           SUBSTR(order_date, 1, 7) AS month,
           product,
           CASE LOWER(TRIM(category))
               WHEN 'mobile' THEN 'Mobile'
               WHEN 'laptop' THEN 'Laptop'
               WHEN 'accessories' THEN 'Accessories'
               WHEN 'tv & audio' THEN 'TV & Audio'
               WHEN 'home appliances' THEN 'Home Appliances'
           END AS category,
           selling_price * quantity AS revenue,
           (selling_price - cost_price) * quantity AS profit
    FROM orders
    WHERE cost_price IS NOT NULL
      AND quantity > 0
      AND rowid IN (SELECT MIN(rowid) FROM orders GROUP BY order_id)
),
monthly AS (
    SELECT month,
           COUNT(*) AS orders,
           SUM(revenue) AS revenue,
           SUM(profit) AS profit,
           ROUND(SUM(profit) * 100.0 / SUM(revenue), 2) AS margin_pct
    FROM cleaned
    GROUP BY month
),
ranked AS (
    SELECT month, orders, revenue, profit, margin_pct,
           RANK() OVER (ORDER BY profit DESC) AS profit_rank
    FROM monthly
)
SELECT month, profit, profit_rank
FROM ranked
ORDER BY profit_rank;

-- Q3: Best category in each month — RANK() PARTITION BY month.
WITH cleaned AS (
    SELECT order_id,
           SUBSTR(order_date, 1, 7) AS month,
           product,
           CASE LOWER(TRIM(category))
               WHEN 'mobile' THEN 'Mobile'
               WHEN 'laptop' THEN 'Laptop'
               WHEN 'accessories' THEN 'Accessories'
               WHEN 'tv & audio' THEN 'TV & Audio'
               WHEN 'home appliances' THEN 'Home Appliances'
           END AS category,
           selling_price * quantity AS revenue,
           (selling_price - cost_price) * quantity AS profit
    FROM orders
    WHERE cost_price IS NOT NULL
      AND quantity > 0
      AND rowid IN (SELECT MIN(rowid) FROM orders GROUP BY order_id)
),
month_cat AS (
    SELECT month, category, SUM(profit) AS profit
    FROM cleaned
    GROUP BY month, category
),
month_cat_ranked AS (
    SELECT month, category, profit,
           RANK() OVER (PARTITION BY month ORDER BY profit DESC) AS cat_rank
    FROM month_cat
)
SELECT month, category, profit
FROM month_cat_ranked
WHERE cat_rank = 1
ORDER BY month;

-- Q4: Category summary with margin band — the Day 5 analysis, redone on
-- the big dataset. Same bands as Day 5: High >= 30%, Medium >= 20%.
WITH cleaned AS (
    SELECT order_id,
           SUBSTR(order_date, 1, 7) AS month,
           product,
           CASE LOWER(TRIM(category))
               WHEN 'mobile' THEN 'Mobile'
               WHEN 'laptop' THEN 'Laptop'
               WHEN 'accessories' THEN 'Accessories'
               WHEN 'tv & audio' THEN 'TV & Audio'
               WHEN 'home appliances' THEN 'Home Appliances'
           END AS category,
           selling_price * quantity AS revenue,
           (selling_price - cost_price) * quantity AS profit
    FROM orders
    WHERE cost_price IS NOT NULL
      AND quantity > 0
      AND rowid IN (SELECT MIN(rowid) FROM orders GROUP BY order_id)
),
category_summary AS (
    SELECT category,
           COUNT(DISTINCT product) AS products,
           COUNT(*) AS orders,
           SUM(revenue) AS revenue,
           SUM(profit) AS profit,
           ROUND(SUM(profit) * 100.0 / SUM(revenue), 2) AS margin_pct
    FROM cleaned
    GROUP BY category
)
SELECT category, products, orders, revenue, profit, margin_pct,
       CASE WHEN margin_pct >= 30 THEN 'High'
            WHEN margin_pct >= 20 THEN 'Medium'
            ELSE 'Low' END AS margin_band
FROM category_summary
ORDER BY profit DESC;

-- Q5: Month-on-month profit growth — LAG() on the monthly CTE.
WITH cleaned AS (
    SELECT order_id,
           SUBSTR(order_date, 1, 7) AS month,
           product,
           CASE LOWER(TRIM(category))
               WHEN 'mobile' THEN 'Mobile'
               WHEN 'laptop' THEN 'Laptop'
               WHEN 'accessories' THEN 'Accessories'
               WHEN 'tv & audio' THEN 'TV & Audio'
               WHEN 'home appliances' THEN 'Home Appliances'
           END AS category,
           selling_price * quantity AS revenue,
           (selling_price - cost_price) * quantity AS profit
    FROM orders
    WHERE cost_price IS NOT NULL
      AND quantity > 0
      AND rowid IN (SELECT MIN(rowid) FROM orders GROUP BY order_id)
),
monthly AS (
    SELECT month,
           COUNT(*) AS orders,
           SUM(revenue) AS revenue,
           SUM(profit) AS profit,
           ROUND(SUM(profit) * 100.0 / SUM(revenue), 2) AS margin_pct
    FROM cleaned
    GROUP BY month
)
SELECT month, profit,
       LAG(profit) OVER (ORDER BY month) AS prev_profit,
       ROUND((profit - LAG(profit) OVER (ORDER BY month)) * 100.0
             / LAG(profit) OVER (ORDER BY month), 2) AS mom_growth_pct
FROM monthly
ORDER BY month;

-- Q6: Top 3 months by profit, and the category that drove each one —
-- the ranked CTE joined to the best-category-per-month CTE.
WITH cleaned AS (
    SELECT order_id,
           SUBSTR(order_date, 1, 7) AS month,
           product,
           CASE LOWER(TRIM(category))
               WHEN 'mobile' THEN 'Mobile'
               WHEN 'laptop' THEN 'Laptop'
               WHEN 'accessories' THEN 'Accessories'
               WHEN 'tv & audio' THEN 'TV & Audio'
               WHEN 'home appliances' THEN 'Home Appliances'
           END AS category,
           selling_price * quantity AS revenue,
           (selling_price - cost_price) * quantity AS profit
    FROM orders
    WHERE cost_price IS NOT NULL
      AND quantity > 0
      AND rowid IN (SELECT MIN(rowid) FROM orders GROUP BY order_id)
),
monthly AS (
    SELECT month,
           COUNT(*) AS orders,
           SUM(revenue) AS revenue,
           SUM(profit) AS profit,
           ROUND(SUM(profit) * 100.0 / SUM(revenue), 2) AS margin_pct
    FROM cleaned
    GROUP BY month
),
ranked AS (
    SELECT month, orders, revenue, profit, margin_pct,
           RANK() OVER (ORDER BY profit DESC) AS profit_rank
    FROM monthly
),
month_cat AS (
    SELECT month, category, SUM(profit) AS profit
    FROM cleaned
    GROUP BY month, category
),
month_cat_ranked AS (
    SELECT month, category, profit,
           RANK() OVER (PARTITION BY month ORDER BY profit DESC) AS cat_rank
    FROM month_cat
)
SELECT r.month, r.profit, r.profit_rank, b.category AS best_category
FROM ranked r
JOIN month_cat_ranked b ON b.month = r.month AND b.cat_rank = 1
WHERE r.profit_rank <= 3
ORDER BY r.profit_rank;
