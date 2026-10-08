-- ============================================================
-- 00_schema.sql  (v3 — matches the real SA Data Hub downloads)
--
-- Tables:
--   youth_unemployment  : one row per quarter + age group ('15-24', '15-34')
--   national_indicators : national series (unemployment rate, labour
--                         force participation) in long format
--
-- Re-running this file drops and recreates both tables, so any
-- loaded data is cleared. Run load_data.py afterwards.
-- ============================================================

CREATE DATABASE IF NOT EXISTS sa_youth_unemployment;
USE sa_youth_unemployment;

-- Quarter is stored as 'YYYY-Qn' (e.g. '2025-Q4') so alphabetical
-- sorting is also chronological.

DROP TABLE IF EXISTS youth_unemployment;
CREATE TABLE youth_unemployment (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    quarter             VARCHAR(10)  NOT NULL,
    age_group           VARCHAR(10)  NOT NULL,   -- '15-24' or '15-34'
    unemployment_rate   DECIMAL(5,2) NULL,       -- percent, e.g. 61.20
    expanded_rate       DECIMAL(5,2) NULL,       -- broader measure, only for '15-34'
    neet_rate           DECIMAL(5,2) NULL        -- only for '15-24'; ANNUAL figure repeated per quarter
);

DROP TABLE IF EXISTS national_indicators;
CREATE TABLE national_indicators (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    quarter     VARCHAR(10)  NOT NULL,
    indicator   VARCHAR(50)  NOT NULL,   -- e.g. 'unemployment-national', 'lfpr-overall'
    title       VARCHAR(100) NOT NULL,
    value       DECIMAL(5,2) NOT NULL    -- percent
);

CREATE INDEX idx_youth_quarter ON youth_unemployment (quarter);
CREATE INDEX idx_youth_age     ON youth_unemployment (age_group);
CREATE INDEX idx_nat_quarter   ON national_indicators (quarter);
CREATE INDEX idx_nat_indicator ON national_indicators (indicator);
