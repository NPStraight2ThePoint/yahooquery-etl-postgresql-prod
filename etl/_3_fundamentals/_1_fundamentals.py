from path_utils import set_repo_root
set_repo_root()

import os
import time
import pandas as pd
from yahooquery import Ticker
from functools import reduce
from utils import TICKERS_CSV, FUNDAMENTALS_OUTPUT_DIR

BATCH_SIZE = 5
SLEEP_TIME = 2

# --- Flatten JSON per section ---
def flatten_json(data_dict, section):
    flat = []
    for ticker, content in data_dict.items():
        if isinstance(content, dict):
            row = {'ticker': ticker}
            for k, v in content.items():
                row[f"{section}_{k}"] = v
            flat.append(row)
    return pd.DataFrame(flat)

# --- Get and merge all fundamentals for batch ---
def get_summary_fundamentals(batch):
    t = Ticker(batch)

    segments = {
        'summary': flatten_json(t.summary_detail, "summary"),
        'keystats': flatten_json(t.key_stats, "keystats"),
        'fin': flatten_json(t.financial_data, "fin"),
        'price': flatten_json(t.price, "price"),
        'profile': flatten_json(t.asset_profile, "profile")
    }
    return segments

def save_segment_df(df, segment_name, batch_index):
    os.makedirs(FUNDAMENTALS_OUTPUT_DIR, exist_ok=True)
    # Filename per segment per batch (no append, overwrite each batch's file)
    output_path = os.path.join(FUNDAMENTALS_OUTPUT_DIR, f'{segment_name}_batch{batch_index+1}.csv')
    df = df.groupby('ticker').first().reset_index()  # clean duplicates in batch if any
    df.to_csv(output_path, mode='w', header=True, index=False)
    print(f"✅ Saved batch {batch_index+1} segment '{segment_name}' to {output_path}")

def main():
    tickers = pd.read_csv(TICKERS_CSV)['Symbol'].dropna().unique().tolist()
    total_batches = (len(tickers) + BATCH_SIZE - 1) // BATCH_SIZE

    for i in range(0, len(tickers), BATCH_SIZE):
        batch = tickers[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        print(f"🔄 Batch {batch_num}/{total_batches}: {batch}")

        try:
            segments = get_summary_fundamentals(batch)
            for segment_name, df in segments.items():
                save_segment_df(df, segment_name, batch_num - 1)
        except Exception as e:
            print(f"❌ Failed batch {batch}: {e}")

        time.sleep(SLEEP_TIME)

    print(f"\n✅ All batches processed. Separate CSVs per segment and batch saved in:\n{FUNDAMENTALS_OUTPUT_DIR}")

if __name__ == '__main__':
    main()

