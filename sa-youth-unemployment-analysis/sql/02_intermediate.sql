-- ============================================================
-- 02_intermediate.sql (v3) — GROUP BY, HAVING, CASE, JOIN, subqueries.
-- ============================================================
USE sa_youth_unemployment;

-- Q1: Average unemployment rate per age group
SELECT age_group, ROUND(AVG(unemployment_rate), 2) AS avg_rate
FROM youth_unemployment
GROUP BY age_group;

-- Q2: Average NEET rate (15-24 only; annual figure, so this averages
-- the yearly values weighted by 4 quarters each)
SELECT ROUND(AVG(neet_rate), 2) AS avg_neet_rate
FROM youth_unemployment
WHERE age_group = '15-24' AND neet_rate IS NOT NULL;

-- Q3: National indicators whose average is above 40% — HAVING filters
-- on the aggregated value
SELECT indicator, ROUND(AVG(value), 2) AS avg_value
FROM national_indicators
GROUP BY indicator
HAVING AVG(value) > 40
ORDER BY avg_value DESC;

-- Q4: Tier each quarter's 15-34 rate using CASE
SELECT
    quarter,
    unemployment_rate,
    CASE
        WHEN unemployment_rate >= 47 THEN 'High'
        WHEN unemployment_rate >= 46 THEN 'Medium'
        ELSE 'Low'
    END AS risk_tier
FROM youth_unemployment
WHERE age_group = '15-34'
ORDER BY quarter;

-- Q5: Quarters where the 15-34 rate was above its own overall average
-- (subquery calculates the average first)
SELECT quarter, unemployment_rate
FROM youth_unemployment
WHERE age_group = '15-34'
  AND unemployment_rate > (
      SELECT AVG(unemployment_rate)
      FROM youth_unemployment
      WHERE age_group = '15-34'
  )
ORDER BY unemployment_rate DESC;

-- Q6: JOIN — youth rates vs the national unemployment rate, per quarter
SELECT
    y.quarter,
    y.age_group,
    y.unemployment_rate AS youth_rate,
    n.value             AS national_rate,
    ROUND(y.unemployment_rate - n.value, 2) AS gap_vs_national
FROM youth_unemployment y
JOIN national_indicators n
    ON n.quarter = y.quarter
   AND n.indicator = 'unemployment-national'
ORDER BY y.quarter, y.age_group;

-- Q7: Narrow vs expanded rate for 15-34 — how much higher unemployment
-- looks once discouraged work-seekers are included
SELECT
    quarter,
    unemployment_rate AS narrow_rate,
    expanded_rate,
    ROUND(expanded_rate - unemployment_rate, 2) AS gap
FROM youth_unemployment
WHERE age_group = '15-34' AND expanded_rate IS NOT NULL
ORDER BY quarter;
