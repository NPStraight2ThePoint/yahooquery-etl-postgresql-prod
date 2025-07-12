import os
import pandas as pd
from datetime import datetime
from utils import (
    PRICING_TECHNICAL_INSIGHTS_OUTPUT_DIR,
    MERGED_DIR
)

def postprocess_technical_insights(df):
    if 'instrumentInfo.technicalEvents.provider' in df.columns:
        df = df[df['instrumentInfo.technicalEvents.provider'].notna()]
    return df

def merge_csvs(input_dir, output_dir, output_filename, force_symbol=True, add_today_date=False, file_filter=None, postprocess=None):
    os.makedirs(output_dir, exist_ok=True)

    all_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    if file_filter:
        all_files = [f for f in all_files if file_filter in f]

    merged_df = pd.DataFrame()

    for file in all_files:
        filepath = os.path.join(input_dir, file)
        try:
            df = pd.read_csv(filepath)

            # ✅ Drop any unnamed columns (usually extra index columns)
            df = df.loc[:, ~df.columns.str.startswith('Unnamed')]

            merged_df = pd.concat([merged_df, df], ignore_index=True)

        except Exception as e:
            print(f"❌ Failed to process {file}: {e}")

    if add_today_date:
        today_str = datetime.today().strftime('%Y-%m-%d')
        merged_df.insert(0, 'date', today_str)

    if postprocess:
        merged_df = postprocess(merged_df)

    # ✅ Also ensure final merged_df has no lingering unnamed columns
    merged_df = merged_df.loc[:, ~merged_df.columns.str.startswith('Unnamed')]

    output_path = os.path.join(output_dir, output_filename)
    merged_df.to_csv(output_path, index=False)
    print(f"✅ Merged saved to: {output_path}")

def clean_reports_df(df):
    if 'symbol' in df.columns:
        df['symbol'] = df['symbol'].str.replace('_reports', '', regex=False)
    return df

def main():
    # === Technical Insights Merge (only *_technical_insights_flat.csv) ===
    merge_csvs(
        input_dir=PRICING_TECHNICAL_INSIGHTS_OUTPUT_DIR,
        output_dir=MERGED_DIR,
        output_filename='merged_technical_insights.csv',
        force_symbol=True,
        add_today_date=True,
        file_filter='technical_insights',
        postprocess=postprocess_technical_insights
      )

    # === Reports Merge (only *_technical_reports_flat.csv) ===
    merge_csvs(
        input_dir=PRICING_TECHNICAL_INSIGHTS_OUTPUT_DIR,
        output_dir=MERGED_DIR,
        output_filename='merged_reports.csv',
        force_symbol=True,
        add_today_date=True,
        file_filter='reports',
        postprocess=clean_reports_df
      )


if __name__ == '__main__':
    main()
