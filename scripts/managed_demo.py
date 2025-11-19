# managed_demo.py — demo for managed MySQL (Cloud SQL)
# Prereqs:
#   pip install sqlalchemy pymysql pandas python-dotenv
#
# Env vars (.env at repo root):
#   MAN_DB_HOST, MAN_DB_PORT, MAN_DB_USER, MAN_DB_PASS, MAN_DB_NAME

import os, time
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

print("[DEBUG] managed_demo.py starting...")

# --- 0) Load environment ---
load_dotenv(".env", override=True)

MAN_DB_HOST = os.getenv("MAN_DB_HOST")
MAN_DB_PORT = os.getenv("MAN_DB_PORT", "3306")
MAN_DB_USER = os.getenv("MAN_DB_USER")
MAN_DB_PASS = os.getenv("MAN_DB_PASS")
MAN_DB_NAME = os.getenv("MAN_DB_NAME")

print("[ENV] MAN_DB_HOST:", MAN_DB_HOST)
print("[ENV] MAN_DB_PORT:", MAN_DB_PORT)
print("[ENV] MAN_DB_USER:", MAN_DB_USER)
print("[ENV] MAN_DB_NAME:", MAN_DB_NAME)

if not all([MAN_DB_HOST, MAN_DB_PORT, MAN_DB_USER, MAN_DB_PASS, MAN_DB_NAME]):
    raise RuntimeError("One or more MAN_DB_* environment variables are missing")

# --- 1) Connect to server (no DB) and ensure database exists ---
server_url = f"mysql+pymysql://{MAN_DB_USER}:{MAN_DB_PASS}@{MAN_DB_HOST}:{MAN_DB_PORT}/"
print("[STEP 1] Connecting to Managed MySQL (no DB):", server_url.replace(MAN_DB_PASS, "*****"))
t0 = time.time()

engine_server = create_engine(
    server_url,
    connect_args={"ssl": None},   # allow unencrypted for this homework
    pool_pre_ping=True,
)
with engine_server.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{MAN_DB_NAME}`"))
    conn.commit()
print(f"[OK] Ensured database `{MAN_DB_NAME}` exists on managed instance.")

# --- 2) Connect to the target database ---
db_url = f"mysql+pymysql://{MAN_DB_USER}:{MAN_DB_PASS}@{MAN_DB_HOST}:{MAN_DB_PORT}/{MAN_DB_NAME}"
print("[STEP 2] Connecting to DB URL:", db_url.replace(MAN_DB_PASS, "*****"))
engine = create_engine(
    db_url,
    connect_args={"ssl": None},
    pool_pre_ping=True,
)

# --- 3) Create a DataFrame and write to a table ---
table_name = "visits"
df = pd.DataFrame(
    [
        {"patient_id": 10, "visit_date": "2025-10-01", "bp_sys": 117, "bp_dia": 75},
        {"patient_id": 11, "visit_date": "2025-10-02", "bp_sys": 131, "bp_dia": 86},
        {"patient_id": 12, "visit_date": "2025-10-03", "bp_sys": 122, "bp_dia": 80},
        {"patient_id": 13, "visit_date": "2025-10-04", "bp_sys": 111, "bp_dia": 71},
        {"patient_id": 14, "visit_date": "2025-10-05", "bp_sys": 126, "bp_dia": 83},
    ]
)

print("[STEP 3] Writing DataFrame to table:", table_name)
df.to_sql(table_name, con=engine, if_exists="replace", index=False)
print("[OK] Wrote DataFrame to table on managed instance.")

# --- 4) Read back a quick check ---
print("[STEP 4] Reading back row count ...")
with engine.connect() as conn:
    count_df = pd.read_sql(f"SELECT COUNT(*) AS n_rows FROM `{table_name}`", con=conn)
print(count_df)

elapsed = time.time() - t0
print(f"[DONE] Managed path completed in {elapsed:.1f}s at {datetime.utcnow().isoformat()}Z")
