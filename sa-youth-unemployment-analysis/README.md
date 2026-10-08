# South African Youth Unemployment: A SQL & Python Analysis

![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-4479A1?logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-SQLAlchemy-150458?logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end data project that cleans public labour-market data, loads it into
MySQL, and uses SQL (joins, aggregations, window functions and CTEs) to explore
how youth unemployment in South Africa has moved from **2022 to 2025**, and how
it compares with the national rate.

South Africa has one of the highest youth unemployment rates in the world. In
this dataset, the **15-24 rate was 61.2%** and the **15-34 rate was 45.5%** in
2025-Q4, against a national rate of 31.4%.

---

## Results at a glance

![Youth vs national unemployment rate](images/02_youth_vs_national.png)

| Measure (2025-Q4) | Rate |
|---|---|
| Youth unemployment, ages 15-24 | 61.2% |
| Youth unemployment, ages 15-34 | 45.5% |
| Expanded rate, ages 15-34 (includes discouraged work-seekers) | 60.8% |
| National unemployment rate | 31.4% |
| NEET rate, ages 15-24 (2025, annual) | 37.2% |

- Youth unemployment is **roughly 14 to 30 percentage points above the national
  rate**, depending on the age band.
- Rates trended slightly downward over the period: the 15-24 rate fell from
  63.9% (2022-Q1) to 61.2% (2025-Q4), and the 15-34 rate from 46.2% to 45.5%.
- Including discouraged work-seekers lifts the 15-34 rate by about 15 points
  (45.5% to 60.8% in 2025-Q4).

<details>
<summary>More charts</summary>

![Youth unemployment trend](images/01_unemployment_trend.png)
![Narrow vs expanded unemployment, ages 15-34](images/03_narrow_vs_expanded.png)

</details>

## Questions this project answers

- How has youth unemployment (15-24 and 15-34) moved from 2022 to 2025?
- How does the 15-24 group compare to the 15-34 group?
- How far above the national rate is youth unemployment?
- How much higher is the expanded rate (including discouraged work-seekers)?
- What do the quarter-over-quarter and year-over-year trends look like?
- How has the NEET (not in employment, education or training) rate shifted?

## Tech stack

- **MySQL 8.0+** (required for window functions and CTEs)
- **Python 3.9+**: pandas, SQLAlchemy, PyMySQL, python-dotenv, matplotlib, seaborn

## Project structure

```
.
├── sql/
│   ├── 00_schema.sql            # Creates the database and tables
│   ├── 01_basic.sql             # SELECT, WHERE, ORDER BY, basic subquery
│   ├── 02_intermediate.sql      # GROUP BY, HAVING, CASE, JOIN, subqueries
│   └── 03_advanced.sql          # Window functions (LAG, RANK, running AVG), CTEs
├── data/                        # Raw SA Data Hub CSV downloads
├── images/                      # Charts produced by analysis.py
├── db.py                        # Shared MySQL connection helper (reads .env)
├── sadatahub.py                 # Helpers for reading SA Data Hub CSVs
├── transform_youth_data.py      # Reshapes raw youth data (long -> wide)
├── load_data.py                 # Transforms and loads everything into MySQL
├── analysis.py                  # Queries MySQL and generates the charts
├── inspect_csv.py               # Diagnostic for inspecting new CSV downloads
├── requirements.txt
├── .env.example                 # Template for your database credentials
└── LICENSE
```

## Getting started

### Prerequisites

- MySQL 8.0+ running locally (or reachable from your machine)
- Python 3.9+

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/sa-youth-unemployment-analysis.git
cd sa-youth-unemployment-analysis

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure database credentials

```bash
cp .env.example .env            # Windows: copy .env.example .env
```

Open `.env` and set `DB_PASSWORD` (and `DB_USER` / `DB_HOST` if yours differ).
`.env` is listed in `.gitignore`, so your credentials stay local.

### 3. Create the database and tables

Run `sql/00_schema.sql` in MySQL Workbench, or from the CLI:

```bash
mysql -u root -p < sql/00_schema.sql
```

> Re-running this file drops and recreates the tables, clearing any loaded data.

### 4. Load the data

```bash
python load_data.py
```

This cleans the raw CSVs in `data/`, writes the cleaned versions alongside them,
and loads both tables into MySQL. It is safe to re-run: tables are emptied
before loading, so no duplicates are created.

### 5. Run the queries

Open `sql/01_basic.sql`, `sql/02_intermediate.sql` and `sql/03_advanced.sql` in
MySQL Workbench and run them against the `sa_youth_unemployment` database.

### 6. Generate the charts

```bash
python analysis.py
```

Charts are saved to `images/`.

## What the SQL covers

| File | Concepts |
|---|---|
| `sql/01_basic.sql` | `SELECT`, `WHERE`, `ORDER BY`, basic subqueries |
| `sql/02_intermediate.sql` | `GROUP BY`, `HAVING`, `CASE`, `JOIN`, subqueries |
| `sql/03_advanced.sql` | Window functions (`LAG`, `RANK`, running `AVG`), CTEs |

## Data

| Table | Contents |
|---|---|
| `youth_unemployment` | One row per quarter and age group (15-24, 15-34): unemployment rate, expanded rate, NEET rate |
| `national_indicators` | National series in long format: unemployment rate and labour force participation |

**Sources**

- **Statistics South Africa (Stats SA)**: Quarterly Labour Force Survey (QLFS),
  [statssa.gov.za](https://www.statssa.gov.za)
- **SA Data Hub**: pre-cleaned CSV exports of Stats SA unemployment and youth
  unemployment series. The files in `data/` are downloads from this source.

Please refer to the original publishers for terms of use of the underlying data.

## Limitations

- Youth data covers **2022-Q1 to 2025-Q4 only** (16 quarters).
- The **NEET rate is published annually**. The yearly value is repeated for each
  quarter of that year, and 2019-2021 are dropped because there is no quarterly
  youth data for those years. Treat NEET as a yearly figure.
- **No provincial data** is included in the downloads, so comparisons are
  national only.
- The `labour-force-participation` series in the unemployment file (~42-43%)
  conflicts with the `lfpr-overall` series (~60%). It appears to be a different
  measure (for example an absorption rate) published under the same name. Verify
  against Stats SA before relying on it.
- QLFS methodology changes over time can affect long-run comparisons.

## Roadmap

- [ ] Load the full historical time series (2015 to present)
- [ ] Add gender and population-group breakdowns
- [ ] Add industry-level employment data to see where youth are finding work
- [ ] Build a small Streamlit dashboard on top of the database

## License

Released under the [MIT License](LICENSE).
