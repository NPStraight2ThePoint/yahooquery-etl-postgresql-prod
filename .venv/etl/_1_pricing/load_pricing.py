import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import numpy as np
import datetime
from utils import (
    PRICING_HISTORY_OUTPUT_DIR,
    MERGED_DIR,
    DB_PARAMS,
    PRICING_HISTORY_TABLE_NAME,
    OPTION_CHAIN_TABLE_NAME,
    PRICING_TECHNICAL_INSIGHTS_TABLE_NAME,
    PRICING_TECHNICAL_REPORTS_TABLE_NAME, rename_map
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

    # === 3. Load Technical Insights ===
    try:
        print("📥 Loading Technical Insights...")
        path_insights = os.path.join(MERGED_DIR, 'merged_technical_insights.csv')
        df_insights = pd.read_csv(path_insights, parse_dates=['date'], low_memory=False, dtype={'ms_summary_date': str})

        # Lowercase and replace dots, then rename columns per mapping
        df_insights.columns = [col.lower().replace('.', '_') for col in df_insights.columns]
        df_insights.rename(columns=rename_map, inplace=True)

        # Convert epoch ms column to datetime if exists
        if 'ms_summary_date' in df_insights.columns:
            df_insights['ms_summary_date'] = pd.to_datetime(
                df_insights['ms_summary_date'], unit='ms', errors='coerce'
            )
            df_insights['ms_summary_date'] = df_insights['ms_summary_date'].apply(
                lambda x: x.to_pydatetime() if pd.notnull(x) else None
            )

        # Convert all other datetime64 columns properly and handle NaT
        for col in df_insights.select_dtypes(include=['datetime64[ns]']).columns:
            df_insights[col] = df_insights[col].apply(lambda x: x.to_pydatetime() if pd.notnull(x) else None)

        # Replace NaN and empty strings in all object columns with None
        for col in df_insights.select_dtypes(include='object').columns:
            df_insights[col] = df_insights[col].replace({pd.NA: None, np.nan: None, "": None})

        # Fill blanks or None in these two columns with today's date string
        today_str = datetime.date.today().isoformat()  # 'YYYY-MM-DD'
        for col in ['ms_summary_date', 'research_date']:
            if col in df_insights.columns:
                df_insights[col] = df_insights[col].fillna(today_str)
                df_insights.loc[df_insights[col].astype(str).str.strip() == '', col] = today_str

        # Also replace any remaining NaN with None in entire dataframe
        df_insights = df_insights.where(pd.notnull(df_insights), None)

        print("Final columns before insert:")
        print(df_insights.columns.tolist())

        insert_dataframe(conn, df_insights, PRICING_TECHNICAL_INSIGHTS_TABLE_NAME)
    except Exception as e:
        print(f"❌ Failed to load technical insights: {e}")

    # === 4. Load Technical Reports ===
    try:
        print("📥 Loading Technical Reports...")
        path_reports = os.path.join(MERGED_DIR, 'merged_reports.csv')
        df_reports = pd.read_csv(path_reports, parse_dates=['date', 'reportDate'], low_memory=False)

        # Cleanup: lowercase and rename dot notation
        df_reports.columns = [col.lower().replace('.', '_') for col in df_reports.columns]

        insert_dataframe(conn, df_reports, PRICING_TECHNICAL_REPORTS_TABLE_NAME)
    except Exception as e:
        print(f"❌ Failed to load technical reports: {e}")

    conn.close()

if __name__ == '__main__':
    main()
