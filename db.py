"""
db.py
Shared database connection helper. Reads credentials from .env
(never hard-code a password in source files).
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def get_engine():
    password = os.getenv("DB_PASSWORD")
    if not password:
        raise SystemExit(
            "DB_PASSWORD is not set. Copy .env.example to .env and fill it in."
        )
    # URL.create escapes special characters in the password safely
    url = URL.create(
        "mysql+pymysql",
        username=os.getenv("DB_USER", "root").strip(),
        password=password.strip(),
        host=os.getenv("DB_HOST", "localhost").strip(),
        database=os.getenv("DB_NAME", "sa_youth_unemployment").strip(),
    )
    return create_engine(url)
