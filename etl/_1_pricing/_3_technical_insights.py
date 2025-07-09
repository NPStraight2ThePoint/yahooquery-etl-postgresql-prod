from path_utils import set_repo_root
set_repo_root()

from yahooquery import Ticker
import pandas as pd
import json
import os

from utils import TICKERS_CSV, PRICING_TECHNICAL_INSIGHTS_OUTPUT_DIR

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        if k == 'reports':  # Skip 'reports' key here
            continue
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            try:
                items.append((new_key, json.dumps(v)))
            except Exception:
                items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
    return dict(items)

def flatten_reports_to_df(reports_data):
    df = pd.json_normalize(reports_data)
    if 'tickers' in df.columns:
        df['tickers_str'] = df['tickers'].apply(lambda x: ','.join(x) if isinstance(x, list) else '')
    df = df.drop(columns=['tickers'], errors='ignore')
    return df

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_tickers_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    # Assuming the ticker symbols are in a column named 'ticker' or similar
    # Adjust the column name if needed
    tickers = df['Symbol'].dropna().unique().tolist()
    return tickers

def etl_loop():
    ensure_dir(PRICING_TECHNICAL_INSIGHTS_OUTPUT_DIR)

    tickers = get_tickers_from_csv(TICKERS_CSV)
    print(f"Loaded {len(tickers)} tickers from {TICKERS_CSV}")

    for symbol in tickers:
        print(f"Processing {symbol}...")
        try:
            tkr = Ticker(symbol)
            technical_insights = tkr.technical_insights

            if symbol not in technical_insights:
                print(f"  ⚠️ No technical insights found for {symbol}")
                continue

            raw_data = technical_insights[symbol]
            reports_data = raw_data.get('reports', None)

            flat_data = flatten_dict(raw_data)
            df_tech = pd.DataFrame([flat_data])

            tech_path = os.path.join(PRICING_TECHNICAL_INSIGHTS_OUTPUT_DIR, f"{symbol}_technical_insights.csv")
            df_tech.to_csv(tech_path, index=False)
            print(f"  ✅ Saved technical insights to {tech_path}")

            if reports_data:
                df_reports = flatten_reports_to_df(reports_data)
                reports_path = os.path.join(PRICING_TECHNICAL_INSIGHTS_OUTPUT_DIR, f"{symbol}_reports.csv")
                df_reports.to_csv(reports_path, index=False)
                print(f"  ✅ Saved reports to {reports_path}")
            else:
                print(f"  ⚠️ No reports data found for {symbol}")

        except Exception as e:
            print(f"  ❌ Error processing {symbol}: {e}")

def main():
    etl_loop()

if __name__ == "__main__":
    main()

