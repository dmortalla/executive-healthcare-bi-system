# 📏 KPI Definitions

## 👥 Total Patients

Number of unique patients represented in the admissions data.

## 🏥 Admissions

Total number of admission records.

## 🔁 Readmission Rate

Percentage of admission records classified as readmitted by the project's binary transformation of the source `readmitted` field.

For this implementation:

```text
NO           → Not readmitted
Other values → Readmitted
```

This metric should not be interpreted specifically as a 30-day readmission rate.

## 🛏️ Average Length of Stay

Average number of days represented by the `length_of_stay` field across admission records.

## 💵 Treatment Cost per Patient

Derived treatment-cost indicator used for analytical demonstration.

The source dataset does not provide actual treatment costs. The project creates a proxy using available utilization variables such as procedures, medications, visits, and length of stay.

The resulting values should not be interpreted as actual hospital charges, reimbursements, or accounting records.

## 🏨 Department Utilization

Total admission volume associated with each department.
