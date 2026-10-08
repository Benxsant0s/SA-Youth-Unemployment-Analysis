"""
sadatahub.py
Helpers for reading the SA Data Hub CSV downloads. Each file starts
with a couple of '#' comment lines, then a header row beginning 'id,'.
"""

import re
import pandas as pd


def read_sadatahub(path) -> pd.DataFrame:
    with open(path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    header_idx = next(
        (i for i, line in enumerate(lines) if line.strip().lower().startswith("id,")),
        None,
    )
    if header_idx is None:
        raise ValueError(f"Could not find the header row (starting 'id,') in {path}")

    return pd.read_csv(path, skiprows=header_idx, encoding="utf-8-sig")


def convert_period(period: str) -> str:
    """'Q1 2022' -> '2022-Q1'. Annual periods ('2024') are returned as-is."""
    p = str(period).strip()
    m = re.fullmatch(r"Q(\d)\s+(\d{4})", p)
    if m:
        return f"{m.group(2)}-Q{m.group(1)}"
    if re.fullmatch(r"\d{4}", p):
        return p
    raise ValueError(f"Unexpected period format: {period!r}")
