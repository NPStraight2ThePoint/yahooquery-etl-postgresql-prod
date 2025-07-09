import os
import pandas as pd
from glob import glob
from utils import FUNDAMENTALS_OUTPUT_DIR, MERGED_DIR_CLEAN

def reorder_and_add_date(df):
    """Ensure 'ticker' is first column and add 'date' as second column."""
    if 'ticker' in df.columns:
        ticker = df.pop('ticker')
        df.insert(0, 'ticker', ticker)
        today_str = pd.Timestamp.today().strftime('%d/%m/%Y')
        df.insert(1, 'date', today_str)
    return df

def main():
    os.makedirs(MERGED_DIR_CLEAN, exist_ok=True)
    segments = ['summary', 'keystats', 'fin', 'price', 'profile']

    # Merge segment batch files
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

    # Update merged files with date and column order
    for filename in os.listdir(MERGED_DIR_CLEAN):
        if filename.endswith('.csv'):
            path = os.path.join(MERGED_DIR_CLEAN, filename)
            print(f"📄 Processing {filename} ...")
            df = pd.read_csv(path)

            if 'ticker' not in df.columns:
                print(f"⚠️ No 'ticker' column in {filename}, skipping...")
                continue

            df = reorder_and_add_date(df)
            df.to_csv(path, index=False)
            print(f"✅ Updated {filename}")

    print("\n🎉 All merged CSV files updated!")

# Allow script to be run directly or imported
if __name__ == '__main__':
    main()
