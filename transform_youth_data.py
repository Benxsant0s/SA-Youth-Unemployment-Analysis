"""
transform_youth_data.py
Reshapes the raw SA Data Hub youth file (long format: one row per
indicator per period) into the wide format the youth_unemployment
table expects (one row per quarter + age group).

NOTE on NEET: the source publishes the NEET rate ANNUALLY (e.g. '2024'),
while everything else is quarterly. The annual NEET value is applied to
every quarter of that year, and years with no quarterly data
(2019-2021) are dropped. Treat NEET as a yearly figure when analysing.

Usage:
    python transform_youth_data.py [path/to/youth_unemployment_raw.csv]
Writes data/youth_unemployment_clean.csv
"""

import sys
from pathlib import Path

import pandas as pd

from sadatahub import read_sadatahub, convert_period

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = BASE_DIR / "data" / "youth_unemployment_raw.csv"
OUTPUT = BASE_DIR / "data" / "youth_unemployment_clean.csv"


def classify(title: str):
    t = str(title)
    if "NEET" in t:
        return "15-24", "neet_rate"
    if "15-24" in t or "15–24" in t:
        return "15-24", "unemployment_rate"
    if "Expanded" in t:
        return "15-34", "expanded_rate"
    if "15-34" in t or "15–34" in t:
        return "15-34", "unemployment_rate"
    return None, None


def build_youth_table(input_path=DEFAULT_INPUT) -> pd.DataFrame:
    df = read_sadatahub(input_path)
    df["period"] = df["period"].apply(convert_period)
    df[["age_group", "metric"]] = df["title"].apply(lambda t: pd.Series(classify(t)))

    unclassified = df[df["age_group"].isna()]
    if len(unclassified):
        print("Warning: dropping unclassified rows:")
        print(unclassified[["title"]].drop_duplicates().to_string(index=False))
        df = df.dropna(subset=["age_group"])

    # Split annual (NEET) from quarterly rows
    is_annual = ~df["period"].str.contains("Q")
    quarterly, annual = df[~is_annual], df[is_annual]

    wide = quarterly.pivot_table(
        index=["period", "age_group"], columns="metric", values="value", aggfunc="first"
    ).reset_index().rename(columns={"period": "quarter"})

    for col in ["unemployment_rate", "expanded_rate", "neet_rate"]:
        if col not in wide.columns:
            wide[col] = pd.NA

    # Apply the annual NEET value to each quarter of that year (15-24 only)
    neet_by_year = annual[annual["metric"] == "neet_rate"].set_index("period")["value"]
    year = wide["quarter"].str[:4]
    mask = wide["age_group"] == "15-24"
    wide.loc[mask, "neet_rate"] = year[mask].map(neet_by_year)

    wide = wide[["quarter", "age_group", "unemployment_rate", "expanded_rate", "neet_rate"]]
    return wide.sort_values(["quarter", "age_group"]).reset_index(drop=True)


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
    wide = build_youth_table(src)
    wide.to_csv(OUTPUT, index=False)
    print(f"Wrote {len(wide)} rows to {OUTPUT}")
    print(f"Quarters covered: {wide['quarter'].min()} to {wide['quarter'].max()}")
    print(wide.head(10).to_string(index=False))
