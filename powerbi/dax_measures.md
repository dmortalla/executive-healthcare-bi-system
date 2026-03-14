# DAX Measures

This file documents the primary DAX measures used in the Executive Healthcare Business Intelligence System.

These measures are intended for use in the Power BI semantic model built from:

- fact_admissions
- dim_patients
- dim_departments
- dim_dates

---

## Total Patients

**Purpose:** Counts unique patients admitted to the hospital.

```DAX
Total Patients =
DISTINCTCOUNT(fact_admissions[patient_id])
```

---

## Total Admissions

**Purpose:** Counts all admission records.

```DAX
Total Admissions =
COUNTROWS(fact_admissions)
```

---

## Readmission Rate (%)

**Purpose:** Calculates the percentage of admissions marked as readmitted.

```DAX
Readmission Rate (%) =
DIVIDE(
    SUM(fact_admissions[readmitted]),
    COUNTROWS(fact_admissions),
    0
) * 100
```

---

## Average Length of Stay

**Purpose:** Returns the average number of days patients stay admitted.

```DAX
Average Length of Stay =
AVERAGE(fact_admissions[length_of_stay])
```

---

## Average Treatment Cost

**Purpose:** Returns the average treatment cost per admission.

```DAX
Average Treatment Cost =
AVERAGE(fact_admissions[treatment_cost])
```

---

## Total Treatment Cost

**Purpose:** Returns the total treatment cost across all admissions.

```DAX
Total Treatment Cost =
SUM(fact_admissions[treatment_cost])
```

---

## Department Utilization

**Purpose:** Shows patient volume handled by each department.

```DAX
Department Utilization =
COUNTROWS(fact_admissions)
```

---

## Readmitted Patients

**Purpose:** Counts total number of readmitted cases.

```DAX
Readmitted Patients =
SUM(fact_admissions[readmitted])
```

---

## Non-Readmitted Patients

**Purpose:** Counts admissions that were not readmitted.

```DAX
Non-Readmitted Patients =
COUNTROWS(fact_admissions) - SUM(fact_admissions[readmitted])
```

---

## Average Age

**Purpose:** Returns the average patient age.

```DAX
Average Age =
AVERAGE(fact_admissions[age])
```

---

## Admissions YTD

**Purpose:** Calculates year-to-date admissions.

```DAX
Admissions YTD =
TOTALYTD(
    [Total Admissions],
    dim_dates[date]
)
```

---

## Treatment Cost YTD

**Purpose:** Calculates year-to-date treatment cost.

```DAX
Treatment Cost YTD =
TOTALYTD(
    [Total Treatment Cost],
    dim_dates[date]
)
```

---

## Monthly Admissions

**Purpose:** Used in monthly trend visuals.

```DAX
Monthly Admissions =
[Total Admissions]
```

---

## Monthly Treatment Cost

**Purpose:** Used in monthly cost trend visuals.

```DAX
Monthly Treatment Cost =
[Total Treatment Cost]
```

---

## Readmission Rate by Department

**Purpose:** Used in department comparison visuals.

```DAX
Readmission Rate by Department =
DIVIDE(
    SUM(fact_admissions[readmitted]),
    COUNTROWS(fact_admissions),
    0
) * 100
```

---

## Average Length of Stay by Department

**Purpose:** Department comparison metric.

```DAX
Average Length of Stay by Department =
AVERAGE(fact_admissions[length_of_stay])
```

---

## Cost per Patient

**Purpose:** Measures average treatment cost per patient.

```DAX
Cost per Patient =
DIVIDE(
    [Total Treatment Cost],
    [Total Patients],
    0
)
```

---

## Admissions per Patient

**Purpose:** Shows average admissions per patient.

```DAX
Admissions per Patient =
DIVIDE(
    [Total Admissions],
    [Total Patients],
    0
)
```

---

# Suggested Dashboard Usage

## Executive KPI Cards

Use these measures as dashboard cards:

- Total Patients
- Total Admissions
- Readmission Rate (%)
- Average Length of Stay
- Average Treatment Cost
- Total Treatment Cost

---

## Executive Overview Page

Recommended visuals:

- KPI cards for hospital metrics
- Line chart: Monthly Admissions
- Bar chart: Admissions by Department
- Pie/Donut: Insurance Type Distribution
- Monthly patient trends

---

## Hospital Operations Page

Recommended visuals:

- Admissions by Department
- Average Length of Stay by Department
- Total Admissions trend
- Cost by Department

---

## Clinical Outcomes Page

Recommended visuals:

- Readmission Rate by Department
- Readmitted vs Non-Readmitted Patients
- Diagnosis distribution
- Length of stay by diagnosis

---

## Patient Demographics Page

Recommended visuals:

- Average Age
- Admissions by Gender
- Admissions by Insurance Type
- Admissions by Age Group

---

## Financial Performance Page

Recommended visuals:

- Total Treatment Cost
- Average Treatment Cost
- Treatment Cost YTD
- Cost per Patient
- Cost by Department

---

# Model Requirements

For these measures to work correctly in Power BI:

1. fact_admissions[date] must relate to dim_dates[date]
2. dim_dates must be marked as the official Date Table
3. readmitted must be stored as numeric (0/1)
4. treatment_cost, length_of_stay, and age must be numeric

---

# Naming Recommendation

Keep measure names **executive-friendly**.

Good examples:

- Total Patients
- Readmission Rate (%)
- Average Length of Stay
- Cost per Patient

Avoid overly technical naming in dashboard visuals.
