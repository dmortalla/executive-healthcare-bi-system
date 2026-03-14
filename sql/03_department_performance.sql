-- ============================================================
-- File: 03_department_performance.sql
-- Purpose: Evaluate department-level hospital performance
-- ============================================================

SELECT
    department,
    COUNT(*) AS total_admissions,
    COUNT(DISTINCT patient_id) AS unique_patients,
    ROUND(AVG(length_of_stay), 2) AS avg_length_of_stay,
    ROUND(AVG(treatment_cost), 2) AS avg_treatment_cost,
    ROUND(SUM(treatment_cost), 2) AS total_treatment_cost
FROM hospital_admissions
GROUP BY department
ORDER BY total_admissions DESC;

-- Department performance by diagnosis mix
SELECT
    department,
    diagnosis,
    COUNT(*) AS diagnosis_count
FROM hospital_admissions
GROUP BY department, diagnosis
ORDER BY department, diagnosis_count DESC;