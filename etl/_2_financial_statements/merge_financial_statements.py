from path_utils import set_repo_root
set_repo_root()

import os
import pandas as pd
from utils import FINANCIAL_STATEMENTS_DIR, MERGED_DIR_CLEAN

def main():
    # Folders to process
    folders = [
        ('Balance Sheet', 'Annual'),
        ('Balance Sheet', 'Quarterly'),
        ('Income Statement', 'Annual'),
        ('Income Statement', 'Quarterly'),
        ('Cash Flow', 'Annual'),
        ('Cash Flow', 'Quarterly'),
    ]

    os.makedirs(MERGED_DIR_CLEAN, exist_ok=True)

    for statement_type, period in folders:
        folder_path = os.path.join(FINANCIAL_STATEMENTS_DIR, statement_type, period)
        print(f"Merging files in: {folder_path}")

        all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

        # List to hold DataFrames
        dfs = []
        for file in all_files:
            try:
                df = pd.read_csv(file)
                dfs.append(df)
            except Exception as e:
                print(f"⚠️ Could not read {file}: {e}")

        if dfs:
            merged_df = pd.concat(dfs, ignore_index=True)

            # 🔹 Drop rows not in USD
            if 'currencyCode' in merged_df.columns:
                merged_df = merged_df[merged_df['currencyCode'] == 'USD']

            # Optional: remove duplicate rows by ticker + date
            if 'ticker' in merged_df.columns and 'date' in merged_df.columns:
                merged_df.drop_duplicates(subset=['ticker', 'date'], inplace=True)

            # Save merged CSV
            merged_csv_path = os.path.join(MERGED_DIR_CLEAN, f"{statement_type.replace(' ', '_')}_{period}.csv")
            merged_df.to_csv(merged_csv_path, index=False)
            print(f"✅ Saved merged CSV: {merged_csv_path}")
        else:
            print(f"⚠️ No files found in {folder_path} or all failed to load.")

if __name__ == "__main__":
    main()
