-- Day 6 — Data Cleaning: nulls, duplicates & types (SQL / SQLite).
-- Same 6 business questions as python_analysis.py — answers must match.
-- Cleaning rules (identical in both):
--   * exact duplicate rows are dropped
--   * emails are compared case-insensitively, first row per email is kept
--   * rows with no email are dropped (customer cannot be contacted)
--   * city is trimmed and title-cased, blank city becomes 'Unknown'
--   * phone is valid when, after removing spaces and a leading +91,
--     it is exactly 10 digits, pincode is valid when exactly 6 digits.

-- Q1: Raw file size and exact duplicates
SELECT
    (SELECT COUNT(*) FROM customers_raw) AS total_rows,
    (SELECT COUNT(*) FROM customers_raw)
        - (SELECT COUNT(*) FROM (SELECT name, email, phone, city, pincode, signup_date FROM customers_raw GROUP BY name, email, phone, city, pincode, signup_date))
        AS exact_duplicate_rows;

-- Q2: Missing values per column
SELECT
    SUM(CASE WHEN TRIM(name) = '' THEN 1 ELSE 0 END) AS missing_name,
    SUM(CASE WHEN TRIM(email) = '' THEN 1 ELSE 0 END) AS missing_email,
    SUM(CASE WHEN TRIM(phone) = '' THEN 1 ELSE 0 END) AS missing_phone,
    SUM(CASE WHEN TRIM(city) = '' THEN 1 ELSE 0 END) AS missing_city,
    SUM(CASE WHEN TRIM(pincode) = '' THEN 1 ELSE 0 END) AS missing_pincode,
    SUM(CASE WHEN TRIM(signup_date) = '' THEN 1 ELSE 0 END) AS missing_signup_date
FROM customers_raw;

-- Q3: Duplicate emails (case-insensitive, ignoring blanks)
SELECT LOWER(TRIM(email)) AS email, COUNT(*) AS rows
FROM customers_raw
WHERE TRIM(email) <> ''
GROUP BY LOWER(TRIM(email))
HAVING COUNT(*) > 1
ORDER BY rows DESC, email;

SELECT COUNT(*) AS emails_appearing_more_than_once,
       SUM(cnt - 1) AS extra_rows_from_duplicate_emails
FROM (
    SELECT COUNT(*) AS cnt
    FROM customers_raw
    WHERE TRIM(email) <> ''
    GROUP BY LOWER(TRIM(email))
    HAVING COUNT(*) > 1
);

-- Q4: Customers after cleaning
WITH dedup AS (
    SELECT MIN(CAST(customer_id AS INTEGER)) AS customer_id,
           name, email, phone, city, pincode, signup_date
    FROM customers_raw
    GROUP BY name, email, phone, city, pincode, signup_date
),
ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY LOWER(TRIM(email))
               ORDER BY CAST(customer_id AS INTEGER)
           ) AS rn
    FROM dedup
)
SELECT
    (SELECT COUNT(*) FROM dedup) AS after_exact_dedup,
    (SELECT COUNT(*) FROM ranked WHERE rn = 1) AS after_email_dedup,
    (SELECT COUNT(*) FROM ranked WHERE rn = 1 AND TRIM(email) <> '')
        AS usable_unique_customers;

-- Q5: Customers per city (after cleaning)
WITH dedup AS (
    SELECT MIN(CAST(customer_id AS INTEGER)) AS customer_id,
           name, email, phone, city, pincode, signup_date
    FROM customers_raw
    GROUP BY name, email, phone, city, pincode, signup_date
),
ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY LOWER(TRIM(email))
               ORDER BY CAST(customer_id AS INTEGER)
           ) AS rn
    FROM dedup
),
cleaned AS (
    SELECT
        CASE WHEN TRIM(city) = '' THEN 'Unknown'
             ELSE UPPER(SUBSTR(TRIM(city), 1, 1))
                  || LOWER(SUBSTR(TRIM(city), 2))
        END AS city_clean
    FROM ranked
    WHERE rn = 1 AND TRIM(email) <> ''
)
SELECT city_clean, COUNT(*) AS customers
FROM cleaned
GROUP BY city_clean
ORDER BY customers DESC, city_clean;

-- Q6: Phone and pincode validity (cleaned customers)
WITH dedup AS (
    SELECT MIN(CAST(customer_id AS INTEGER)) AS customer_id,
           name, email, phone, city, pincode, signup_date
    FROM customers_raw
    GROUP BY name, email, phone, city, pincode, signup_date
),
ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY LOWER(TRIM(email))
               ORDER BY CAST(customer_id AS INTEGER)
           ) AS rn
    FROM dedup
),
cleaned AS (
    SELECT
        name,
        REPLACE(REPLACE(TRIM(phone), ' ', ''), '+91', '') AS phone_clean,
        TRIM(pincode) AS pincode_clean,
        TRIM(phone) AS phone_raw,
        TRIM(pincode) AS pincode_raw
    FROM ranked
    WHERE rn = 1 AND TRIM(email) <> ''
),
status AS (
    SELECT
        CASE WHEN phone_raw = '' THEN 'Missing'
             WHEN LENGTH(phone_clean) = 10
                  AND phone_clean NOT GLOB '*[^0-9]*' THEN 'Valid'
             ELSE 'Invalid' END AS phone_status,
        CASE WHEN pincode_raw = '' THEN 'Missing'
             WHEN LENGTH(pincode_clean) = 6
                  AND pincode_clean NOT GLOB '*[^0-9]*' THEN 'Valid'
             ELSE 'Invalid' END AS pincode_status,
        name
    FROM cleaned
)
SELECT 'phone' AS field, phone_status AS status, COUNT(*) AS customers
FROM status
GROUP BY phone_status
UNION ALL
SELECT 'pincode' AS field, pincode_status AS status, COUNT(*) AS customers
FROM status
GROUP BY pincode_status;

SELECT GROUP_CONCAT(name, ', ') AS customers_with_invalid_phone
FROM (
    WITH dedup AS (SELECT MIN(CAST(customer_id AS INTEGER)) AS customer_id, name, email, phone, city, pincode, signup_date FROM customers_raw GROUP BY name, email, phone, city, pincode, signup_date),
    ranked AS (
        SELECT *, ROW_NUMBER() OVER (
            PARTITION BY LOWER(TRIM(email))
            ORDER BY CAST(customer_id AS INTEGER)
        ) AS rn FROM dedup
    )
    SELECT name,
           REPLACE(REPLACE(TRIM(phone), ' ', ''), '+91', '') AS phone_clean
    FROM ranked
    WHERE rn = 1 AND TRIM(email) <> '' AND TRIM(phone) <> ''
      AND (LENGTH(REPLACE(REPLACE(TRIM(phone), ' ', ''), '+91', '')) <> 10
           OR REPLACE(REPLACE(TRIM(phone), ' ', ''), '+91', '')
              GLOB '*[^0-9]*')
);

SELECT GROUP_CONCAT(name, ', ') AS customers_with_invalid_pincode
FROM (
    WITH dedup AS (SELECT MIN(CAST(customer_id AS INTEGER)) AS customer_id, name, email, phone, city, pincode, signup_date FROM customers_raw GROUP BY name, email, phone, city, pincode, signup_date),
    ranked AS (
        SELECT *, ROW_NUMBER() OVER (
            PARTITION BY LOWER(TRIM(email))
            ORDER BY CAST(customer_id AS INTEGER)
        ) AS rn FROM dedup
    )
    SELECT name, TRIM(pincode) AS pincode_clean
    FROM ranked
    WHERE rn = 1 AND TRIM(email) <> '' AND TRIM(pincode) <> ''
      AND (LENGTH(TRIM(pincode)) <> 6
           OR TRIM(pincode) GLOB '*[^0-9]*')
);
