"""
generate_kpis.py

Purpose
-------
Generate an executive KPI summary table from the processed fact table.

Output
------
- data/processed/executive_kpi_table.csv
"""

from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
FACT_PATH = REPO_ROOT / "data" / "processed" / "fact_admissions.csv"
OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "executive_kpi_table.csv"


def load_fact_table(path: Path) -> pd.DataFrame:
    """Load the processed fact admissions table."""
    if not path.exists():
        raise FileNotFoundError(
            f"Processed fact table not found at: {path}\n"
            "Run prepare_healthcare_data.py first."
        )
    return pd.read_csv(path)


def calculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate executive KPI summary values."""
    total_patients = df["patient_id"].nunique()
    total_admissions = len(df)
    readmission_rate_pct = round(df["readmitted"].mean() * 100, 2)
    avg_length_of_stay = round(df["length_of_stay"].mean(), 2)
    avg_treatment_cost = round(df["treatment_cost"].mean(), 2)
    total_treatment_cost = round(df["treatment_cost"].sum(), 2)

    kpi_df = pd.DataFrame(
        {
            "metric": [
                "Total Patients",
                "Total Admissions",
                "Readmission Rate (%)",
                "Average Length of Stay",
                "Average Treatment Cost",
                "Total Treatment Cost",
            ],
            "value": [
                total_patients,
                total_admissions,
                readmission_rate_pct,
                avg_length_of_stay,
                avg_treatment_cost,
                total_treatment_cost,
            ],
        }
    )
    return kpi_df


def main() -> None:
    """Create and save KPI summary table."""
    fact_df = load_fact_table(FACT_PATH)
    kpi_df = calculate_kpis(fact_df)

    assert not kpi_df.empty, "KPI table is empty."

    kpi_df.to_csv(OUTPUT_PATH, index=False)

    print("Executive KPI table generated successfully.")
    print(kpi_df.to_string(index=False))


if __name__ == "__main__":
    main()