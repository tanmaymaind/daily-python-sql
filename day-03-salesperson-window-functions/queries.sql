-- Day 3 — Salesperson performance in SQL (SQLite window functions).
-- Same business questions as python_analysis.py, answered in SQL.
-- Table: monthly_sales(salesperson, region, month, deals_closed, revenue)

-- Q1: Rank salespeople by total revenue within each region (RANK)
WITH totals AS (
  SELECT region, salesperson, SUM(revenue) AS total_revenue
  FROM monthly_sales GROUP BY region, salesperson
)
SELECT region, salesperson, total_revenue,
       RANK() OVER (PARTITION BY region ORDER BY total_revenue DESC) AS rank_in_region
FROM totals ORDER BY region, rank_in_region;

-- Q2: Running total of revenue per region, month by month (cumulative SUM)
WITH monthly AS (
  SELECT region, month, SUM(revenue) AS month_revenue
  FROM monthly_sales GROUP BY region, month
)
SELECT region, month, month_revenue,
       SUM(month_revenue) OVER (PARTITION BY region ORDER BY month) AS running_total
FROM monthly ORDER BY region, month;

-- Q3: Top 3 salespeople overall by total revenue (ROW_NUMBER)
WITH totals AS (
  SELECT region, salesperson, SUM(revenue) AS total_revenue
  FROM monthly_sales GROUP BY region, salesperson
),
ranked AS (
  SELECT salesperson, region, total_revenue,
         ROW_NUMBER() OVER (ORDER BY total_revenue DESC, salesperson) AS overall_rank
  FROM totals
)
SELECT overall_rank, salesperson, region, total_revenue
FROM ranked WHERE overall_rank <= 3 ORDER BY overall_rank;

-- Q4: Month-over-month revenue growth per salesperson (LAG)
SELECT salesperson, month, revenue,
       LAG(revenue) OVER (PARTITION BY salesperson ORDER BY month) AS prev_revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (PARTITION BY salesperson ORDER BY month))
             / LAG(revenue) OVER (PARTITION BY salesperson ORDER BY month), 1) AS growth_pct
FROM monthly_sales ORDER BY salesperson, month;

-- Q5: Best month for each salesperson (ROW_NUMBER per salesperson)
WITH ranked AS (
  SELECT salesperson, region, month, revenue,
         ROW_NUMBER() OVER (PARTITION BY salesperson ORDER BY revenue DESC) AS rn
  FROM monthly_sales
)
SELECT salesperson, region, month, revenue
FROM ranked WHERE rn = 1 ORDER BY salesperson;

-- Q6: Each salesperson's total vs their region's average (AVG window)
WITH totals AS (
  SELECT region, salesperson, SUM(revenue) AS total_revenue
  FROM monthly_sales GROUP BY region, salesperson
)
SELECT region, salesperson, total_revenue,
       CAST(ROUND(AVG(total_revenue) OVER (PARTITION BY region), 0) AS INTEGER) AS region_avg,
       CAST(total_revenue - ROUND(AVG(total_revenue) OVER (PARTITION BY region), 0) AS INTEGER) AS diff_from_avg
FROM totals ORDER BY region, total_revenue DESC;

-- Q7: Total revenue (all salespeople, Jul-Sep 2026)
SELECT SUM(revenue) AS total_revenue FROM monthly_sales;
