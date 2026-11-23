-- Day 7 — Employee Hierarchy: self-joins (SQL / SQLite).
-- Dataset: data/employees.csv — 20 employees of a Pune IT services
-- company. Every employee except the CEO reports to another employee
-- in the same table, so the table joins to itself. Same 6 business
-- questions as python_analysis.py — answers must match the pandas run.

-- Q1: Every employee with their manager's name
SELECT e.emp_id, e.name, e.department, m.name AS manager_name, e.salary
FROM employees e
LEFT JOIN employees m ON m.emp_id = e.manager_id
ORDER BY e.emp_id;

-- Q2: Employees who earn more than their direct manager
SELECT e.name, e.salary, m.name AS manager_name,
       m.salary AS manager_salary, e.salary - m.salary AS diff
FROM employees e
JOIN employees m ON m.emp_id = e.manager_id
WHERE e.salary > m.salary
ORDER BY diff DESC;

-- Q3: Direct reports and team salary bill per manager
SELECT m.name AS manager_name, COUNT(*) AS reports,
       SUM(e.salary) AS team_salary_bill
FROM employees e
JOIN employees m ON m.emp_id = e.manager_id
GROUP BY m.emp_id, m.name
ORDER BY reports DESC, manager_name ASC;

-- Q4: Headcount and average salary by department
SELECT department, COUNT(*) AS headcount,
       ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY department
ORDER BY headcount DESC, department ASC;

-- Q5: Organisation depth (levels from the CEO) — recursive CTE
WITH RECURSIVE levels(emp_id, level) AS (
    SELECT emp_id, 0 FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.emp_id, l.level + 1
    FROM employees e
    JOIN levels l ON e.manager_id = l.emp_id
)
SELECT level, COUNT(*) AS employees
FROM levels
GROUP BY level
ORDER BY level;

-- Q6: Reporting chain for Nikhil Gupta (bottom-up) — recursive CTE
WITH RECURSIVE chain(step, emp_id, name, department, salary, manager_id) AS (
    SELECT 0, emp_id, name, department, salary, manager_id
    FROM employees
    WHERE name = 'Nikhil Gupta'
    UNION ALL
    SELECT step + 1, e.emp_id, e.name, e.department, e.salary,
           e.manager_id
    FROM employees e
    JOIN chain c ON e.emp_id = c.manager_id
)
SELECT c.step, c.name, c.department, c.salary, m.name AS manager_name
FROM chain c
LEFT JOIN employees m ON m.emp_id = c.manager_id
ORDER BY c.step;
