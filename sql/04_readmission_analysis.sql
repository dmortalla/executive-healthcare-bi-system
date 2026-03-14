-- ============================================================
-- File: 04_readmission_analysis.sql
-- Purpose: Analyze patient readmissions across dimensions
-- ============================================================

-- Overall readmission rate
SELECT
    ROUND(100.0 * SUM(readmitted) / COUNT(*), 2) AS overall_readmission_rate_pct
FROM hospital_admissions;

-- Readmission rate by department
SELECT
    department,
    ROUND(100.0 * SUM(readmitted) / COUNT(*), 2) AS readmission_rate_pct
FROM hospital_admissions
GROUP BY department
ORDER BY readmission_rate_pct DESC;

-- Readmission rate by diagnosis
SELECT
    diagnosis,
    ROUND(100.0 * SUM(readmitted) / COUNT(*), 2) AS readmission_rate_pct
FROM hospital_admissions
GROUP BY diagnosis
ORDER BY readmission_rate_pct DESC;

-- Readmission rate by insurance type
SELECT
    insurance_type,
    ROUND(100.0 * SUM(readmitted) / COUNT(*), 2) AS readmission_rate_pct
FROM hospital_admissions
GROUP BY insurance_type
ORDER BY readmission_rate_pct DESC;