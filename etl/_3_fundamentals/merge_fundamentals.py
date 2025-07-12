import os
import sys

# Add project root to sys.path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
from glob import glob
from utils import FUNDAMENTALS_OUTPUT_DIR, MERGED_DIR_CLEAN

def reorder_and_add_date(df):
    """Ensure 'ticker' is first column and add 'date' as second column."""
    if 'ticker' in df.columns:
        ticker = df.pop('ticker')
        df.insert(0, 'ticker', ticker)
        today_str = pd.Timestamp.today().strftime('%d/%m/%Y')
        if 'date' not in df.columns:
            df.insert(1, 'date', today_str)
    return df

def reorder_officers_columns(df):
    # Drop 'age' if it exists
    df = df.drop(columns=['age'], errors='ignore')

    # Define new column order
    cols = df.columns.tolist()
    # Remove 'date' and 'ticker' from current list if present
    for col in ['date', 'ticker']:
        if col in cols:
            cols.remove(col)
    # Insert 'date' at position 0 and 'ticker' at position 1
    new_order = ['date', 'ticker'] + cols
    df = df[new_order]

    return df

def main():
    os.makedirs(MERGED_DIR_CLEAN, exist_ok=True)
    segments = ['summary', 'keystats', 'fin', 'price', 'profile']

    # Merge standard segments batch files
    for segment in segments:
        files = sorted(glob(os.path.join(FUNDAMENTALS_OUTPUT_DIR, f'{segment}_batch*.csv')))
        if not files:
            print(f"⚠️ No files found for segment '{segment}', skipping...")
            continue

        dfs = [pd.read_csv(f) for f in files]
        merged_df = pd.concat(dfs, axis=0, sort=True)
        merged_output_path = os.path.join(MERGED_DIR_CLEAN, f'{segment}_merged.csv')
        merged_df.to_csv(merged_output_path, index=False)
        print(f"✅ Merged {len(files)} batch files for segment '{segment}' into {merged_output_path}")

    # Merge valuation files (batch or per-ticker)
    valuation_files = sorted(glob(os.path.join(FUNDAMENTALS_OUTPUT_DIR, '*_valuation*.csv')))
    if valuation_files:
        dfs = [pd.read_csv(f) for f in valuation_files]
        merged_valuation = pd.concat(dfs, axis=0, sort=True)
        valuation_merged_path = os.path.join(MERGED_DIR_CLEAN, 'valuation_merged.csv')
        merged_valuation.to_csv(valuation_merged_path, index=False)
        print(f"✅ Merged {len(valuation_files)} valuation files into {valuation_merged_path}")
    else:
        print("⚠️ No valuation files found to merge.")

    # Merge officers files (per ticker)
    officer_files = sorted(glob(os.path.join(FUNDAMENTALS_OUTPUT_DIR, '*_officers*.csv')))
    if officer_files:
        dfs = [pd.read_csv(f) for f in officer_files]
        merged_officers = pd.concat(dfs, axis=0, sort=True)
        officers_merged_path = os.path.join(MERGED_DIR_CLEAN, 'officers_merged.csv')
        merged_officers.to_csv(officers_merged_path, index=False)
        print(f"✅ Merged {len(officer_files)} officer files into {officers_merged_path}")
    else:
        print("⚠️ No officer files found to merge.")

    # Update all *_merged.csv files
    for filename in os.listdir(MERGED_DIR_CLEAN):
        if filename.endswith('_merged.csv'):
            path = os.path.join(MERGED_DIR_CLEAN, filename)
            print(f"📄 Processing {filename} ...")
            df = pd.read_csv(path)

            if 'ticker' not in df.columns:
                print(f"ℹ️ Skipping {filename} (no 'ticker' column)...")
                continue

            if filename == 'officers_merged.csv':
                df = reorder_officers_columns(df)
            else:
                df = reorder_and_add_date(df)

            df.to_csv(path, index=False)
            print(f"✅ Updated {filename}")

    print("\n🎉 All merged CSV files updated!")

if __name__ == '__main__':
    main()
