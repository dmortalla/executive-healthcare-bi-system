-- ============================================================
-- File: 01_data_quality_checks.sql
-- Purpose: Validate healthcare admissions dataset quality
-- ============================================================

-- Total row count
SELECT COUNT(*) AS total_rows
FROM hospital_admissions;

-- Unique patient count
SELECT COUNT(DISTINCT patient_id) AS unique_patients
FROM hospital_admissions;

-- Check for missing admission dates
SELECT COUNT(*) AS missing_admission_dates
FROM hospital_admissions
WHERE admission_date IS NULL;

-- Check for missing department values
SELECT COUNT(*) AS missing_departments
FROM hospital_admissions
WHERE department IS NULL OR TRIM(department) = '';

-- Check for missing diagnosis values
SELECT COUNT(*) AS missing_diagnoses
FROM hospital_admissions
WHERE diagnosis IS NULL OR TRIM(diagnosis) = '';

-- Check for invalid length_of_stay values
SELECT COUNT(*) AS invalid_length_of_stay
FROM hospital_admissions
WHERE length_of_stay IS NULL
   OR length_of_stay < 0;

-- Department distribution
SELECT
    department,
    COUNT(*) AS admission_count
FROM hospital_admissions
GROUP BY department
ORDER BY admission_count DESC;

-- Duplicate admission check
SELECT
    patient_id,
    admission_date,
    department,
    diagnosis,
    COUNT(*) AS duplicate_count
FROM hospital_admissions
GROUP BY patient_id, admission_date, department, diagnosis
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;