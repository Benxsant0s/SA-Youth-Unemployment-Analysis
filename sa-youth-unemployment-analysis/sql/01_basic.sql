-- ============================================================
-- 01_basic.sql (v3) — filtering, sorting, simple lookups.
-- ============================================================
USE sa_youth_unemployment;

-- Q1: Row count and quarters covered
SELECT COUNT(*) AS total_rows,
       MIN(quarter) AS earliest_quarter,
       MAX(quarter) AS latest_quarter
FROM youth_unemployment;

-- Q2: Latest quarter's unemployment rate for each age group
SELECT quarter, age_group, unemployment_rate
FROM youth_unemployment
WHERE quarter = (SELECT MAX(quarter) FROM youth_unemployment)
ORDER BY age_group;

-- Q3: 15-24 data, most recent first
SELECT quarter, unemployment_rate, neet_rate
FROM youth_unemployment
WHERE age_group = '15-24'
ORDER BY quarter DESC;

-- Q4: Latest national indicators (unemployment, participation)
SELECT indicator, title, quarter, value
FROM national_indicators n
WHERE quarter = (SELECT MAX(quarter) FROM national_indicators WHERE indicator = n.indicator)
ORDER BY indicator;

-- Q5: Quarters where the 15-24 unemployment rate exceeded 62%
SELECT quarter, unemployment_rate
FROM youth_unemployment
WHERE age_group = '15-24'
  AND unemployment_rate > 62
ORDER BY quarter;

-- Q6: Narrow (official) vs expanded rate for 15-34, most recent first
SELECT quarter, unemployment_rate, expanded_rate
FROM youth_unemployment
WHERE age_group = '15-34'
ORDER BY quarter DESC;
