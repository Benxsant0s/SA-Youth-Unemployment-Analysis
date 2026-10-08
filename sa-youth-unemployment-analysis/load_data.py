"""
load_data.py
Transforms the raw SA Data Hub CSVs in data/ and loads them into MySQL.

Before running:
1. Run 00_schema.sql in MySQL Workbench / the MySQL CLI.
2. Copy .env.example to .env and fill in your MySQL password.
3. pip install -r requirements.txt
4. python load_data.py

Safe to re-run: tables are emptied before loading, so no duplicates.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import text

from db import get_engine
from sadatahub import read_sadatahub, convert_period
from transform_youth_data import build_youth_table

DATA_DIR = Path(__file__).resolve().parent / "data"

NATIONAL_FILES = [
    DATA_DIR / "sa-data-hub_unemployment_2026-10-06.csv",
    DATA_DIR / "sa-data-hub_labour-force-participation_2026-10-06.csv",
]


def build_national_table() -> pd.DataFrame:
    frames = []
    for path in NATIONAL_FILES:
        df = read_sadatahub(path)
        df["quarter"] = df["period"].apply(convert_period)
        frames.append(df.rename(columns={"id": "indicator"})[["quarter", "indicator", "title", "value"]])
    out = pd.concat(frames, ignore_index=True)
    return out.sort_values(["indicator", "quarter"]).reset_index(drop=True)


def reload_table(df: pd.DataFrame, table: str, engine) -> None:
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {table}"))
    df.to_sql(table, con=engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into '{table}'")


def main():
    engine = get_engine()

    youth = build_youth_table()
    youth.to_csv(DATA_DIR / "youth_unemployment_clean.csv", index=False)
    national = build_national_table()
    national.to_csv(DATA_DIR / "national_indicators_clean.csv", index=False)

    reload_table(youth, "youth_unemployment", engine)
    reload_table(national, "national_indicators", engine)

    print("\nDone. Quick check:")
    print("  SELECT * FROM youth_unemployment LIMIT 10;")
    print("  SELECT * FROM national_indicators LIMIT 10;")


if __name__ == "__main__":
    main()
