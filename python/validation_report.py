"""
validation_report.py

Purpose
-------
Run lightweight validation checks against processed BI tables and print
a recruiter-friendly verification summary.

Checks
------
- fact_admissions exists and is non-empty
- dim_patients exists and is non-empty
- dim_departments exists and is non-empty
- dim_dates exists and is non-empty
- executive_kpi_table exists and is non-empty
"""

from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = REPO_ROOT / "data" / "processed"

FILES_TO_VALIDATE = {
    "fact_admissions": PROCESSED_DIR / "fact_admissions.csv",
    "dim_patients": PROCESSED_DIR / "dim_patients.csv",
    "dim_departments": PROCESSED_DIR / "dim_departments.csv",
    "dim_dates": PROCESSED_DIR / "dim_dates.csv",
    "executive_kpi_table": PROCESSED_DIR / "executive_kpi_table.csv",
}


def load_csv(path: Path) -> pd.DataFrame:
    """Load a CSV file with existence check."""
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return pd.read_csv(path)


def main() -> None:
    """Run validation report."""
    loaded_tables = {}

    for name, path in FILES_TO_VALIDATE.items():
        df = load_csv(path)
        assert not df.empty, f"{name} is empty."
        loaded_tables[name] = df

    fact_df = loaded_tables["fact_admissions"]

    total_patients = fact_df["patient_id"].nunique()
    total_admissions = len(fact_df)
    readmission_rate_pct = round(fact_df["readmitted"].mean() * 100, 2)
    avg_length_of_stay = round(fact_df["length_of_stay"].mean(), 2)
    avg_treatment_cost = round(fact_df["treatment_cost"].mean(), 2)

    print("=" * 60)
    print("EXECUTIVE HEALTHCARE BI SYSTEM - VALIDATION REPORT")
    print("=" * 60)
    print(f"fact_admissions rows      : {len(loaded_tables['fact_admissions']):,}")
    print(f"dim_patients rows         : {len(loaded_tables['dim_patients']):,}")
    print(f"dim_departments rows      : {len(loaded_tables['dim_departments']):,}")
    print(f"dim_dates rows            : {len(loaded_tables['dim_dates']):,}")
    print(f"executive_kpi_table rows  : {len(loaded_tables['executive_kpi_table']):,}")
    print("-" * 60)
    print(f"Total Patients            : {total_patients:,}")
    print(f"Total Admissions          : {total_admissions:,}")
    print(f"Readmission Rate (%)      : {readmission_rate_pct}")
    print(f"Avg Length of Stay        : {avg_length_of_stay}")
    print(f"Avg Treatment Cost        : {avg_treatment_cost}")
    print("=" * 60)
    print("Validation completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()