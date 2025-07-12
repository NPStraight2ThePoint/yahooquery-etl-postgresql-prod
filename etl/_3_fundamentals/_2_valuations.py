import os
import sys

# Add project root to sys.path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import os
import pandas as pd
from yahooquery import Ticker
from utils import TICKERS_CSV, FUNDAMENTALS_OUTPUT_DIR

os.makedirs(FUNDAMENTALS_OUTPUT_DIR, exist_ok=True)

def save_valuation_for_ticker(ticker):
    tkr = Ticker(ticker)
    val = tkr.valuation_measures

    if isinstance(val, dict):
        val_data = val.get(ticker)
        if val_data:
            df = pd.DataFrame([val_data])
            df['ticker'] = ticker
            output_path = os.path.join(FUNDAMENTALS_OUTPUT_DIR, f"{ticker}_valuation.csv")
            df.to_csv(output_path, index=False)
            print(f"Saved {ticker} valuation (dict) to {output_path}")
        else:
            print(f"No valuation data for {ticker} (dict case)")
    elif isinstance(val, pd.DataFrame):
        # val is already a DataFrame
        df = val.copy()
        df['ticker'] = ticker
        output_path = os.path.join(FUNDAMENTALS_OUTPUT_DIR, f"{ticker}_valuation.csv")
        df.to_csv(output_path, index=False)
        print(f"Saved {ticker} valuation (DataFrame) to {output_path}")
    else:
        print(f"Unexpected data format for {ticker}: {type(val)}")


def main():
    tickers = pd.read_csv(TICKERS_CSV)['Symbol'].dropna().unique().tolist()
    for ticker in tickers:
        save_valuation_for_ticker(ticker)

if __name__ == '__main__':
    main()
