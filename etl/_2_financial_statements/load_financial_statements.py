import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from utils import MERGED_DIR_CLEAN, conn_params

filename_to_table_stub = {
    'cash_flow': 'cashflow',
    'income_statement': 'income_statement',
    'balance_sheet': 'balance_sheet',
}

# --- Loader Function ---
def load_csv_to_postgres(csv_path, table_name):
    print(f"📄 Loading {os.path.basename(csv_path)} into {table_name}...")

    df = pd.read_csv(csv_path)

    # Convert 'asOfDate' if exists
    if 'asOfDate' in df.columns:
        df['asOfDate'] = pd.to_datetime(df['asOfDate'], format='%Y-%m-%d', errors='coerce').dt.date


    # Replace NaN with None for SQL compatibility
    df = df.where(pd.notnull(df), None)

    # Generate insert query
    cols = df.columns.tolist()
    insert_query = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES %s"
    values = [tuple(row) for row in df.to_numpy()]

    # Insert into DB
    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                execute_values(cur, insert_query, values)
            conn.commit()
        print(f"✅ {len(df)} rows inserted into {table_name}")
    except Exception as e:
        print(f"❌ Failed to insert into {table_name}: {e}")

def main():
    for filename in os.listdir(MERGED_DIR_CLEAN):
        if not filename.endswith('.csv'):
            continue

        base = os.path.splitext(filename)[0].lower()

        # Only include files that match known statement types
        if not any(key in base for key in filename_to_table_stub.keys()):
            continue  # skip unknown types silently

        parts = base.split('_')
        if len(parts) >= 2:
            statement_type = '_'.join(parts[:-1])  # e.g. 'balance_sheet'
            frequency = parts[-1]  # e.g. 'annual'

            statement_map = {
                'balance_sheet': 'bs',
                'income_statement': 'is',
                'cash_flow': 'cf'
            }

            freq_map = {
                'annual': 'a',
                'quarterly': 'q'
            }

            stub = statement_map.get(statement_type)
            freq = freq_map.get(frequency)

            if stub and freq:
                table_name = f"yahooquery.financial_statements_{stub}_{freq}"
            else:
                continue  # silently skip if invalid mapping
        else:
            continue  # skip files with unexpected format

        full_path = os.path.join(MERGED_DIR_CLEAN, filename)
        load_csv_to_postgres(csv_path=full_path, table_name=table_name)

if __name__ == '__main__':
    main()





