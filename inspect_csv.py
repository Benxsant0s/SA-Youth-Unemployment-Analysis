"""
inspect_csv.py
Diagnostic script: figures out where the real header row is in a
downloaded CSV, and lists the distinct indicators/titles inside it,
so we know exactly what data is available before loading it properly.

Usage:
    python inspect_csv.py path/to/your_downloaded_file.csv
"""

import sys
import pandas as pd

if len(sys.argv) < 2:
    print("Usage: python inspect_csv.py path/to/your_downloaded_file.csv")
    sys.exit(1)

file_path = sys.argv[1]

# Step 1: find which line number the real header is on, by looking
# for a line that starts with "id," (based on the header you confirmed)
with open(file_path, "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

header_line_index = None
for i, line in enumerate(lines):
    if line.strip().lower().startswith("id,"):
        header_line_index = i
        break

if header_line_index is None:
    print("Could not automatically find a line starting with 'id,'.")
    print("Here are the first 15 lines of the file so we can find it manually:\n")
    for i, line in enumerate(lines[:15]):
        print(f"{i}: {line.rstrip()}")
    sys.exit(0)

print(f"Found header row at line {header_line_index} (0-indexed).")
print(f"Header: {lines[header_line_index].strip()}\n")

# Step 2: load the CSV starting from that header row
df = pd.read_csv(file_path, skiprows=header_line_index, encoding="utf-8-sig")

print(f"Loaded {len(df)} rows.")
print(f"Columns: {list(df.columns)}\n")

# Step 3: show every distinct indicator/title in the file
title_col = "title" if "title" in df.columns else df.columns[1]
print(f"Distinct values in '{title_col}':")
for val in df[title_col].unique():
    print(f"  - {val}")

series_col = "series_name" if "series_name" in df.columns else None
if series_col:
    print(f"\nDistinct values in '{series_col}':")
    for val in df[series_col].unique():
        print(f"  - {val}")

# Step 4: show period range
period_col = "period" if "period" in df.columns else None
if period_col:
    print(f"\nPeriod range: {df[period_col].min()} to {df[period_col].max()}")
    print(f"Number of distinct periods: {df[period_col].nunique()}")

print("\nFirst 5 rows:")
print(df.head())
