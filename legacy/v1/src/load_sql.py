"""Load the simulated transactions into SQLite for the SQL analytics in sql/fraud_queries.sql."""
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "transactions.csv")
df["ts"] = pd.to_datetime(df.ts).dt.strftime("%Y-%m-%d %H:%M:%S")
df["ts_epoch"] = (pd.to_datetime(df.ts) - pd.Timestamp("1970-01-01")) // pd.Timedelta(seconds=1)
con = sqlite3.connect(ROOT / "data" / "txnvigil.db")
df.to_sql("txn", con, if_exists="replace", index=False)
con.execute("CREATE INDEX IF NOT EXISTS ix_user_ts ON txn(user_id, ts_epoch)")
con.execute("CREATE INDEX IF NOT EXISTS ix_payee ON txn(payee_id, user_id)")
con.commit()
print(f"loaded {len(df):,} rows into data/txnvigil.db (table txn)")
