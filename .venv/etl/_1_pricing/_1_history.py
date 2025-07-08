import os
import time
import pandas as pd
from yahooquery import Ticker
from utils import TICKERS_CSV, PRICING_HISTORY_OUTPUT_DIR

# Where to save per-ticker CSVs
BATCH_SIZE = 5                            # Tickers per API call
SLEEP_BETWEEN_BATCHES = 2                 # Seconds delay between batches

def download_price_history(tickers: list, output_dir: str):
    t = Ticker(tickers)
    try:
        full_df = t.history(period='max')

        for ticker in tickers:
            try:
                if isinstance(full_df.index, pd.MultiIndex):
                    df = full_df.loc[ticker]
                else:
                    df = full_df  # Single ticker

                if df.empty or 'close' not in df.columns:
                    print(f"⚠️ No valid data for {ticker}")
                    continue

                df = df.reset_index()
                df['ticker'] = ticker

                # ✅ Reorder columns
                desired_order = ['date', 'ticker', 'open', 'high', 'low', 'close', 'adjclose', 'volume', 'dividends',
                                 'splits']
                df = df[desired_order]

                output_path = os.path.join(output_dir, f'{ticker}.csv')
                df.to_csv(output_path, index=False)
                print(f"✅ Saved {ticker} to {output_path}")

            except KeyError:
                print(f"❌ No data found for {ticker} in batch response")
            except Exception as e:
                print(f"❌ Failed for {ticker}: {e}")

    except Exception as e:
        print(f"❌ Batch failed for tickers {tickers}: {e}")

def main():
    os.makedirs(PRICING_HISTORY_OUTPUT_DIR, exist_ok=True)

    # Step 1: Load tickers
    df = pd.read_csv(TICKERS_CSV)
    tickers = df['Symbol'].dropna().unique().tolist()

    print(f"📄 Loaded {len(tickers)} tickers from CSV")

    # Step 2: Loop in batches
    for i in range(0, len(tickers), BATCH_SIZE):
        batch = tickers[i:i+BATCH_SIZE]
        print(f"\n⏳ Processing batch {i//BATCH_SIZE + 1} / {len(tickers)//BATCH_SIZE + 1}")
        download_price_history(batch, PRICING_HISTORY_OUTPUT_DIR)
        time.sleep(SLEEP_BETWEEN_BATCHES)

if __name__ == '__main__':
    main()

