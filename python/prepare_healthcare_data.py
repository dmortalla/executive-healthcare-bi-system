"""
prepare_healthcare_data.py

Purpose
-------
Load the real hospital admissions dataset, standardize fields, map the
source schema into a BI-friendly model, and generate processed tables.

Input
-----
data/raw/hospital_admissions.csv

Outputs
-------
data/processed/fact_admissions.csv
data/processed/dim_patients.csv
data/processed/dim_departments.csv

Dataset Notes
-------------
This version is designed for the UCI / Kaggle diabetes hospitals dataset:
Diabetes 130-US hospitals for years 1999-2008
"""

from pathlib import Path
from typing import List

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = REPO_ROOT / "data" / "raw" / "hospital_admissions.csv"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"

SOURCE_REQUIRED_COLUMNS: List[str] = [
    "encounter_id",
    "patient_nbr",
    "gender",
    "age",
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id",
    "time_in_hospital",
    "payer_code",
    "medical_specialty",
    "diag_1",
    "diag_2",
    "diag_3",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "readmitted",
]


def load_dataset(path: Path) -> pd.DataFrame:
    """Load the raw admissions dataset."""
    if not path.exists():
        raise FileNotFoundError(
            f"Raw dataset not found at: {path}\n"
            "Place hospital_admissions.csv inside data/raw/."
        )
    return pd.read_csv(path)


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to lowercase snake_case."""
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def validate_source_columns(df: pd.DataFrame) -> None:
    """Ensure all required source columns exist."""
    missing = [col for col in SOURCE_REQUIRED_COLUMNS if col not in df.columns]
    assert not missing, f"Missing required source columns: {missing}"


def normalize_readmitted(value: str) -> int:
    """Convert UCI readmission labels into binary values."""
    if pd.isna(value):
        return 0
    value = str(value).strip()
    return 0 if value == "NO" else 1


def age_band_to_numeric(age_band: str) -> float:
    """Convert age bands like '[70-80)' to midpoint values."""
    if pd.isna(age_band):
        return np.nan

    text = str(age_band).strip()
    if text in {"?", "Unknown/Invalid"}:
        return np.nan

    text = text.replace("[", "").replace(")", "")
    if "-" not in text:
        return np.nan

    low, high = text.split("-")
    try:
        return (float(low) + float(high)) / 2
    except ValueError:
        return np.nan


def build_admission_date(df: pd.DataFrame) -> pd.Series:
    """
    Create a synthetic admission date so we can support time intelligence.

    The source dataset does not include an actual admission date, so we create
    a reproducible date series for BI trending purposes.
    """
    start_date = pd.Timestamp("2020-01-01")
    date_offsets = np.arange(len(df)) % 1461  # ~4 years
    return start_date + pd.to_timedelta(date_offsets, unit="D")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Perform cleaning and create BI-friendly derived fields."""
    df = df.copy()

    # Normalize placeholder missing values
    df = df.replace("?", pd.NA)

    # Normalize gender
    df["gender"] = df["gender"].replace("Unknown/Invalid", pd.NA)

    # Convert readmitted to 0/1
    df["readmitted"] = df["readmitted"].apply(normalize_readmitted).astype(int)

    # Convert age band to numeric midpoint
    df["age_numeric"] = df["age"].apply(age_band_to_numeric)

    # Create synthetic admission date for BI time trend analysis
    df["admission_date"] = build_admission_date(df)

    # Map fields into business-friendly names
    df["patient_id"] = df["patient_nbr"]
    df["admission_id"] = df["encounter_id"]
    df["department"] = df["medical_specialty"].fillna("Unknown")
    df["diagnosis"] = df["diag_1"].fillna("Unknown")
    df["length_of_stay"] = pd.to_numeric(df["time_in_hospital"], errors="coerce")
    df["insurance_type"] = df["payer_code"].fillna("Unknown")

    # Create treatment cost proxy since source has no actual cost field
    df["treatment_cost"] = (
        pd.to_numeric(df["num_lab_procedures"], errors="coerce").fillna(0) * 15
        + pd.to_numeric(df["num_procedures"], errors="coerce").fillna(0) * 250
        + pd.to_numeric(df["num_medications"], errors="coerce").fillna(0) * 20
        + pd.to_numeric(df["number_outpatient"], errors="coerce").fillna(0) * 100
        + pd.to_numeric(df["number_emergency"], errors="coerce").fillna(0) * 300
        + pd.to_numeric(df["number_inpatient"], errors="coerce").fillna(0) * 500
        + pd.to_numeric(df["time_in_hospital"], errors="coerce").fillna(0) * 400
    ).astype(float)

    # Remove rows missing core keys
    df = df.dropna(subset=["patient_id", "admission_id", "admission_date"])

    # Guardrails
    df = df[df["length_of_stay"].fillna(0) >= 0]
    df = df[df["treatment_cost"].fillna(0) >= 0]

    return df


def build_fact_admissions(df: pd.DataFrame) -> pd.DataFrame:
    """Create the fact admissions table."""
    fact = pd.DataFrame(
        {
            "admission_id": df["admission_id"],
            "patient_id": df["patient_id"],
            "date": df["admission_date"],
            "department": df["department"],
            "diagnosis": df["diagnosis"],
            "length_of_stay": df["length_of_stay"],
            "readmitted": df["readmitted"],
            "treatment_cost": df["treatment_cost"],
            "insurance_type": df["insurance_type"],
            "gender": df["gender"],
            "age": df["age_numeric"],
        }
    )

    fact = fact.dropna(subset=["patient_id", "date"])
    return fact


def build_dim_patients(df: pd.DataFrame) -> pd.DataFrame:
    """Create patient dimension table with one row per patient."""
    dim_patients = (
        pd.DataFrame(
            {
                "patient_id": df["patient_id"],
                "gender": df["gender"],
                "age": df["age_numeric"],
                "insurance_type": df["insurance_type"],
            }
        )
        .sort_values(["patient_id", "age"], na_position="last")
        .groupby("patient_id", as_index=False)
        .agg(
            {
                "gender": "first",
                "age": "first",
                "insurance_type": "first",
            }
        )
        .sort_values("patient_id")
        .reset_index(drop=True)
    )
    return dim_patients


def build_dim_departments(df: pd.DataFrame) -> pd.DataFrame:
    """Create department dimension table."""
    dim_departments = (
        pd.DataFrame({"department": df["department"]})
        .drop_duplicates()
        .dropna()
        .sort_values("department")
        .reset_index(drop=True)
    )
    dim_departments["department_id"] = range(1, len(dim_departments) + 1)
    dim_departments = dim_departments[["department_id", "department"]]
    return dim_departments


def save_outputs(
    fact_admissions: pd.DataFrame,
    dim_patients: pd.DataFrame,
    dim_departments: pd.DataFrame,
) -> None:
    """Save processed outputs."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    fact_admissions.to_csv(PROCESSED_DIR / "fact_admissions.csv", index=False)
    dim_patients.to_csv(PROCESSED_DIR / "dim_patients.csv", index=False)
    dim_departments.to_csv(PROCESSED_DIR / "dim_departments.csv", index=False)


def main() -> None:
    """Run the data preparation pipeline."""
    df = load_dataset(RAW_PATH)
    df = standardize_column_names(df)
    validate_source_columns(df)
    df = clean_data(df)

    fact_admissions = build_fact_admissions(df)
    dim_patients = build_dim_patients(df)
    dim_departments = build_dim_departments(df)

    # Guardrails
    assert not fact_admissions.empty, "fact_admissions is empty."
    assert not dim_patients.empty, "dim_patients is empty."
    assert not dim_departments.empty, "dim_departments is empty."

    save_outputs(fact_admissions, dim_patients, dim_departments)

    print("Healthcare data preparation completed successfully.")
    print(f"Rows in fact_admissions: {len(fact_admissions):,}")
    print(f"Rows in dim_patients: {len(dim_patients):,}")
    print(f"Rows in dim_departments: {len(dim_departments):,}")


if __name__ == "__main__":
    main()