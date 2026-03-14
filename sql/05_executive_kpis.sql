-- ============================================================
-- File: 05_executive_kpis.sql
-- Purpose: Executive KPI summary for dashboard validation
-- ============================================================

SELECT
    COUNT(DISTINCT patient_id) AS total_patients,
    COUNT(*) AS total_admissions,
    ROUND(100.0 * SUM(readmitted) / COUNT(*), 2) AS readmission_rate_pct,
    ROUND(AVG(length_of_stay), 2) AS avg_length_of_stay,
    ROUND(AVG(treatment_cost), 2) AS avg_treatment_cost,
    ROUND(SUM(treatment_cost), 2) AS total_treatment_cost
FROM hospital_admissions;