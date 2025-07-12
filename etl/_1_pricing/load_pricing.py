import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import numpy as np
import datetime
from utils import (
    MERGED_DIR,
    DB_PARAMS,
    PRICING_HISTORY_TABLE_NAME,
    OPTION_CHAIN_TABLE_NAME
)

# --- Insert DataFrame into Table ---
def insert_dataframe(conn, df, table_name):
    if df.empty:
        print(f"⚠️ Skipping empty DataFrame for {table_name}")
        return
    cols = ','.join(df.columns)
    values = [tuple(x) for x in df.to_numpy()]
    with conn.cursor() as cur:
        query = f"INSERT INTO {table_name} ({cols}) VALUES %s ON CONFLICT DO NOTHING"
        execute_values(cur, query, values)
    print(f"✅ Inserted into {table_name}: {len(df)} rows")

# --- Main Execution ---
def main():
    conn = psycopg2.connect(**DB_PARAMS)
    conn.autocommit = True

    # === 1. Load Historical Prices ===
    try:
        print("📥 Loading Historical Prices...")
        df_hist = pd.read_csv(os.path.join(MERGED_DIR, 'merged_history.csv'), parse_dates=['date'])
        insert_dataframe(conn, df_hist, PRICING_HISTORY_TABLE_NAME)
    except Exception as e:
        print(f"❌ Failed to load historical prices: {e}")

    # === 2. Load Option Chain ===
    try:
        print("📥 Loading Option Chain...")
        df_opt = pd.read_csv(os.path.join(MERGED_DIR, 'merged_option_chain.csv'), parse_dates=['date', 'expiration'])
        df_opt['inTheMoney'] = df_opt['inTheMoney'].astype(bool)
        insert_dataframe(conn, df_opt, OPTION_CHAIN_TABLE_NAME)
    except Exception as e:
        print(f"❌ Failed to load option chain: {e}")

    conn.close()

if __name__ == '__main__':
    main()
