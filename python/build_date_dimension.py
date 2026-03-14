"""
build_date_dimension.py

Purpose
-------
Generate a reusable date dimension table for Power BI time intelligence.

Output
------
- data/processed/dim_dates.csv
"""

from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
DATE_OUTPUT_PATH = PROCESSED_DIR / "dim_dates.csv"


def create_date_dimension(start_date: str, end_date: str) -> pd.DataFrame:
    """Create a date dimension table."""
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    dim_dates = pd.DataFrame({"date": dates})
    dim_dates["year"] = dim_dates["date"].dt.year
    dim_dates["quarter"] = dim_dates["date"].dt.quarter
    dim_dates["month"] = dim_dates["date"].dt.month
    dim_dates["month_name"] = dim_dates["date"].dt.month_name()
    dim_dates["day"] = dim_dates["date"].dt.day
    dim_dates["day_name"] = dim_dates["date"].dt.day_name()
    dim_dates["week"] = dim_dates["date"].dt.isocalendar().week.astype(int)

    return dim_dates


def main() -> None:
    """Build and save the date dimension."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    dim_dates = create_date_dimension(
        start_date="2018-01-01",
        end_date="2026-12-31",
    )

    assert not dim_dates.empty, "dim_dates is empty."

    dim_dates.to_csv(DATE_OUTPUT_PATH, index=False)

    print("Date dimension created successfully.")
    print(f"Rows in dim_dates: {len(dim_dates):,}")
    print(f"Saved to: {DATE_OUTPUT_PATH}")


if __name__ == "__main__":
    main()