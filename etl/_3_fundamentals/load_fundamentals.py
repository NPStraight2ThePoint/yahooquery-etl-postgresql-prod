import os
import sys

# Add project root to sys.path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import psycopg2
import json
import ast
from psycopg2.extras import execute_values
from utils import (
    conn_params,
    FUNDAMENTALS_FINANCIAL_DATA, FUNDAMENTALS_KEY_STATS, FUNDAMENTALS_PRICE_DATA,
    FUNDAMENTALS_PROFILE_DATA, FUNDAMENTALS_SUMMARY_DATA, FUNDAMENTALS_VALUATION, FUNDAMENTALS_OFFICERS,
    FUNDAMENTALS_FINANCIAL_DATA_TABLE_NAME, FUNDAMENTALS_KEY_STATS_TABLE_NAME, FUNDAMENTALS_PRICE_DATA_TABLE_NAME,
    FUNDAMENTALS_PROFILE_DATA_TABLE_NAME, FUNDAMENTALS_SUMMARY_DATA_TABLE_NAME, FUNDAMENTALS_VALUATION_TABLE_NAME,
    FUNDAMENTALS_OFFICERS_TABLE_NAME
)

def clean_officers_df(df):
    money_cols = ['exercisedValue', 'totalPay', 'unexercisedValue']
    for col in money_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, NaN if invalid

    int_cols = ['fiscalYear', 'maxAge', 'yearBorn']
    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce', downcast='integer')

    df = df.where(pd.notnull(df), None)  # Replace NaN with None for SQL NULL
    return df

# --- Fix JSON Columns ---
def fix_json_columns(df, json_columns):
    for col in json_columns:
        if col in df.columns:
            def safe_json(x):
                try:
                    return json.dumps(ast.literal_eval(x)) if pd.notna(x) else None
                except Exception:
                    return None
            df[col] = df[col].apply(safe_json)
    return df

def load_csv_to_db(csv_path, table_name):
    print(f"📥 Loading CSV: {csv_path} into table: {table_name}")

    df = pd.read_csv(csv_path)

    # Convert 'date' from dd/mm/yyyy to proper date object
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce').dt.date

    # Officer-specific cleaning: convert money and int columns and handle nulls
    if table_name == FUNDAMENTALS_OFFICERS_TABLE_NAME:
        money_cols = ['exercisedValue', 'totalPay', 'unexercisedValue']
        for col in money_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        int_cols = ['fiscalYear', 'maxAge', 'yearBorn']
        for col in int_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce', downcast='integer')

    # Fix problematic JSON columns for profile (existing code)
    if table_name == FUNDAMENTALS_PROFILE_DATA_TABLE_NAME:
        df = fix_json_columns(df, ['profile_companyOfficers', 'profile_executiveTeam'])

    # Replace NaN with None so psycopg2 inserts SQL NULL
    df = df.where(pd.notnull(df), None)

    # Prepare SQL and insert rows as before
    cols = df.columns.tolist()
    insert_query = f"""
        INSERT INTO {table_name} ({', '.join(cols)}) 
        VALUES %s
    """
    values = [tuple(x) for x in df.to_numpy()]

    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                execute_values(cur, insert_query, values)
            conn.commit()
        print(f"✅ {len(df)} rows inserted into {table_name}")
    except Exception as e:
        print(f"❌ Error inserting into {table_name}: {e}")

# --- Main function to call from orchestrator ---
def main():
    load_csv_to_db(FUNDAMENTALS_FINANCIAL_DATA, FUNDAMENTALS_FINANCIAL_DATA_TABLE_NAME)
    load_csv_to_db(FUNDAMENTALS_KEY_STATS, FUNDAMENTALS_KEY_STATS_TABLE_NAME)
    load_csv_to_db(FUNDAMENTALS_PRICE_DATA, FUNDAMENTALS_PRICE_DATA_TABLE_NAME)
    load_csv_to_db(FUNDAMENTALS_PROFILE_DATA, FUNDAMENTALS_PROFILE_DATA_TABLE_NAME)
    load_csv_to_db(FUNDAMENTALS_SUMMARY_DATA, FUNDAMENTALS_SUMMARY_DATA_TABLE_NAME)
    load_csv_to_db(FUNDAMENTALS_VALUATION, FUNDAMENTALS_VALUATION_TABLE_NAME)
    load_csv_to_db(FUNDAMENTALS_OFFICERS, FUNDAMENTALS_OFFICERS_TABLE_NAME)  # <-- Added officers load here

# --- Run when executed directly ---
if __name__ == '__main__':
    main()
