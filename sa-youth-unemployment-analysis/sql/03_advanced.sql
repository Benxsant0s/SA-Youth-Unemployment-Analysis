-- ============================================================
-- 03_advanced.sql (v3) — window functions and CTEs.
-- Requires MySQL 8.0+.
-- ============================================================
USE sa_youth_unemployment;

-- Q1: Quarter-over-quarter change, 15-24
SELECT
    quarter,
    unemployment_rate,
    LAG(unemployment_rate) OVER (ORDER BY quarter) AS previous_rate,
    ROUND(unemployment_rate - LAG(unemployment_rate) OVER (ORDER BY quarter), 2) AS change_vs_previous
FROM youth_unemployment
WHERE age_group = '15-24'
ORDER BY quarter;

-- Q2: Same for 15-34, to compare volatility
SELECT
    quarter,
    unemployment_rate,
    LAG(unemployment_rate) OVER (ORDER BY quarter) AS previous_rate,
    ROUND(unemployment_rate - LAG(unemployment_rate) OVER (ORDER BY quarter), 2) AS change_vs_previous
FROM youth_unemployment
WHERE age_group = '15-34'
ORDER BY quarter;

-- Q3: Rank quarters by 15-24 unemployment WITHIN each year
-- (PARTITION BY restarts the ranking every year; 1 = worst quarter)
SELECT
    LEFT(quarter, 4) AS year,
    quarter,
    unemployment_rate,
    RANK() OVER (PARTITION BY LEFT(quarter, 4) ORDER BY unemployment_rate DESC) AS rank_in_year
FROM youth_unemployment
WHERE age_group = '15-24'
ORDER BY quarter;

-- Q4: Running average of the 15-24 rate
SELECT
    quarter,
    unemployment_rate,
    ROUND(AVG(unemployment_rate) OVER (
        ORDER BY quarter ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_avg
FROM youth_unemployment
WHERE age_group = '15-24'
ORDER BY quarter;

-- Q5: CTE — yearly average youth (15-34) rate vs yearly national rate
WITH youth_by_year AS (
    SELECT LEFT(quarter, 4) AS year, AVG(unemployment_rate) AS youth_avg
    FROM youth_unemployment
    WHERE age_group = '15-34'
    GROUP BY LEFT(quarter, 4)
),
national_by_year AS (
    SELECT LEFT(quarter, 4) AS year, AVG(value) AS national_avg
    FROM national_indicators
    WHERE indicator = 'unemployment-national'
    GROUP BY LEFT(quarter, 4)
)
SELECT
    y.year,
    ROUND(y.youth_avg, 2)    AS youth_avg,
    ROUND(n.national_avg, 2) AS national_avg,
    ROUND(y.youth_avg - n.national_avg, 2) AS gap
FROM youth_by_year y
JOIN national_by_year n ON n.year = y.year
ORDER BY y.year;

-- Q6: Year-over-year change — each quarter vs the same quarter a year
-- earlier (LAG with an offset of 4 rows), for 15-24
SELECT
    quarter,
    unemployment_rate,
    LAG(unemployment_rate, 4) OVER (ORDER BY quarter) AS same_quarter_last_year,
    ROUND(unemployment_rate - LAG(unemployment_rate, 4) OVER (ORDER BY quarter), 2) AS yoy_change
FROM youth_unemployment
WHERE age_group = '15-24'
ORDER BY quarter;

-- Q7: CTE — do 15-24 unemployment and NEET move together?
WITH youth_15_24 AS (
    SELECT quarter, unemployment_rate, neet_rate
    FROM youth_unemployment
    WHERE age_group = '15-24'
)
SELECT
    quarter,
    unemployment_rate,
    neet_rate,
    LAG(neet_rate) OVER (ORDER BY quarter) AS previous_neet_rate
FROM youth_15_24
ORDER BY quarter;
