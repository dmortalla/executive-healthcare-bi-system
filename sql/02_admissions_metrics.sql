-- ============================================================
-- File: 02_admissions_metrics.sql
-- Purpose: Generate hospital admissions trend metrics
-- ============================================================

-- Daily admissions
SELECT
    CAST(admission_date AS DATE) AS admission_day,
    COUNT(*) AS admissions
FROM hospital_admissions
GROUP BY CAST(admission_date AS DATE)
ORDER BY admission_day;

-- Monthly admissions
SELECT
    EXTRACT(YEAR FROM CAST(admission_date AS DATE)) AS year,
    EXTRACT(MONTH FROM CAST(admission_date AS DATE)) AS month,
    COUNT(*) AS admissions
FROM hospital_admissions
GROUP BY
    EXTRACT(YEAR FROM CAST(admission_date AS DATE)),
    EXTRACT(MONTH FROM CAST(admission_date AS DATE))
ORDER BY year, month;

-- Admissions by department
SELECT
    department,
    COUNT(*) AS admissions
FROM hospital_admissions
GROUP BY department
ORDER BY admissions DESC;

-- Admissions by gender
SELECT
    gender,
    COUNT(*) AS admissions
FROM hospital_admissions
GROUP BY gender
ORDER BY admissions DESC;

-- Admissions by insurance type
SELECT
    insurance_type,
    COUNT(*) AS admissions
FROM hospital_admissions
GROUP BY insurance_type
ORDER BY admissions DESC;