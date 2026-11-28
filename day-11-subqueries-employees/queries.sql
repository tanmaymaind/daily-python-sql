-- Day 11 — Subqueries: classic interview questions on ~500 employees.
-- Same cleaning as python_analysis.py, done once in CTEs so every
-- question below works on the same clean tables:
--   cleaned_emp: drop missing salary, drop salary <= 0, drop duplicate
--     employee_id (keep first row), tidy department text.
--   cleaned_ord: drop missing order_amount, drop duplicate order_id.

-- Q1: Employees earning above the company average salary (scalar subquery).
SELECT COUNT(*) AS above_avg_count,
       ROUND(AVG(salary), 2) AS their_avg_salary
FROM cleaned_emp
WHERE salary > (SELECT AVG(salary) FROM cleaned_emp);

-- Q1b: the top 5 above-average earners.
SELECT employee_id, name, department, salary
FROM cleaned_emp
WHERE salary > (SELECT AVG(salary) FROM cleaned_emp)
ORDER BY salary DESC
LIMIT 5;

-- Q2: Employees earning above their OWN department's average (correlated subquery).
SELECT department, COUNT(*) AS above_dept_avg_count
FROM cleaned_emp e
WHERE salary > (SELECT AVG(salary) FROM cleaned_emp WHERE department = e.department)
GROUP BY department
ORDER BY department;

-- Q3: Second-largest order amount (a MAX inside a MAX).
SELECT MAX(order_amount) AS second_largest_order
FROM cleaned_ord
WHERE order_amount < (SELECT MAX(order_amount) FROM cleaned_ord);

-- Q3b: which order(s) is it, and who placed them?
SELECT order_id, employee_id, order_amount
FROM cleaned_ord
WHERE order_amount = (
    SELECT MAX(order_amount) FROM cleaned_ord
    WHERE order_amount < (SELECT MAX(order_amount) FROM cleaned_ord)
);

-- Q4: Departments whose average salary beats the company average (subquery in HAVING).
SELECT department, COUNT(*) AS headcount, ROUND(AVG(salary), 2) AS avg_salary
FROM cleaned_emp
GROUP BY department
HAVING AVG(salary) > (SELECT AVG(salary) FROM cleaned_emp)
ORDER BY avg_salary DESC;

-- Q5: Employees who never placed an order (NOT EXISTS).
SELECT COUNT(*) AS never_ordered_count
FROM cleaned_emp e
WHERE NOT EXISTS (
    SELECT 1 FROM cleaned_ord o WHERE o.employee_id = e.employee_id
);

-- Q5b: the highest-paid of them.
SELECT employee_id, name, department, salary
FROM cleaned_emp e
WHERE NOT EXISTS (
    SELECT 1 FROM cleaned_ord o WHERE o.employee_id = e.employee_id
)
ORDER BY salary DESC
LIMIT 3;

-- Q6: Orders above the average order amount (scalar subquery).
SELECT COUNT(*) AS big_orders,
       SUM(order_amount) AS big_orders_total,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cleaned_ord), 2) AS pct_of_orders,
       ROUND(100.0 * SUM(order_amount) / (SELECT SUM(order_amount) FROM cleaned_ord), 2) AS pct_of_value
FROM cleaned_ord
WHERE order_amount > (SELECT AVG(order_amount) FROM cleaned_ord);
