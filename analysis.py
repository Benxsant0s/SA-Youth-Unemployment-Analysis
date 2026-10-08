"""
analysis.py
Pulls key results from MySQL and builds three charts into images/.
Run after load_data.py.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from db import get_engine

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "images"
IMG_DIR.mkdir(exist_ok=True)

engine = get_engine()
sns.set_style("whitegrid")


def _finish(fig_name: str, ax, title: str, ylabel="Rate (%)"):
    ax.set_title(title)
    ax.set_xlabel("Quarter")
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    path = IMG_DIR / fig_name
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved {path.relative_to(BASE_DIR)}")


def chart_1_trend_over_time():
    """Unemployment rate over time, both age groups."""
    df = pd.read_sql(
        "SELECT quarter, age_group, unemployment_rate FROM youth_unemployment ORDER BY quarter",
        con=engine,
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    for group, data in df.groupby("age_group"):
        ax.plot(data["quarter"], data["unemployment_rate"], marker="o", label=group)
    ax.legend(title="Age Group")
    _finish("01_unemployment_trend.png", ax, "SA Youth Unemployment Rate Over Time", "Unemployment Rate (%)")


def chart_2_youth_vs_national():
    """Youth (15-24, 15-34) vs the national unemployment rate."""
    youth = pd.read_sql(
        "SELECT quarter, age_group, unemployment_rate AS rate FROM youth_unemployment",
        con=engine,
    )
    national = pd.read_sql(
        "SELECT quarter, value AS rate FROM national_indicators WHERE indicator = 'unemployment-national'",
        con=engine,
    )
    pivot = youth.pivot(index="quarter", columns="age_group", values="rate")
    pivot["National"] = national.set_index("quarter")["rate"]

    fig, ax = plt.subplots(figsize=(9, 5))
    pivot.plot(ax=ax, marker="o")
    _finish("02_youth_vs_national.png", ax, "Youth vs National Unemployment Rate", "Unemployment Rate (%)")


def chart_3_narrow_vs_expanded():
    """15-34: narrow vs expanded unemployment rate."""
    df = pd.read_sql(
        """SELECT quarter, unemployment_rate AS narrow, expanded_rate AS expanded
           FROM youth_unemployment WHERE age_group = '15-34' ORDER BY quarter""",
        con=engine,
    ).set_index("quarter")

    fig, ax = plt.subplots(figsize=(9, 5))
    df.plot(ax=ax, marker="o")
    _finish("03_narrow_vs_expanded.png", ax, "Ages 15-34: Narrow vs Expanded Unemployment Rate", "Unemployment Rate (%)")


if __name__ == "__main__":
    chart_1_trend_over_time()
    chart_2_youth_vs_national()
    chart_3_narrow_vs_expanded()
    print("\nAll charts generated. Check the images/ folder.")
