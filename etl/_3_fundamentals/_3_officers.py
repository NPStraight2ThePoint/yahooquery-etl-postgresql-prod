import os
import sys

# Add project root to sys.path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
from yahooquery import Ticker
from utils import TICKERS_CSV, FUNDAMENTALS_OUTPUT_DIR

os.makedirs(FUNDAMENTALS_OUTPUT_DIR, exist_ok=True)

def save_officers_for_ticker(ticker):
    """Fetch company officers for a single ticker and save to individual CSV."""
    tkr = Ticker(ticker)
    officers = tkr.company_officers

    # Case 1: officers is a DataFrame (in rare cases like 'MMM')
    if isinstance(officers, pd.DataFrame):
        df = officers.copy()
        df.insert(0, 'ticker', ticker)
        df.insert(1, 'date', pd.Timestamp.today().strftime('%d/%m/%Y'))

        output_path = os.path.join(FUNDAMENTALS_OUTPUT_DIR, f"{ticker}_officers.csv")
        df.to_csv(output_path, index=False)
        print(f"✅ Saved {ticker} officers (DataFrame) to {output_path}")
        return

    # Case 2: officers is a dict {ticker: list}
    if isinstance(officers, dict):
        officer_list = officers.get(ticker)
        if isinstance(officer_list, list) and officer_list:
            df = pd.DataFrame(officer_list)
            df.insert(0, 'ticker', ticker)
            df.insert(1, 'date', pd.Timestamp.today().strftime('%d/%m/%Y'))

            output_path = os.path.join(FUNDAMENTALS_OUTPUT_DIR, f"{ticker}_officers.csv")
            df.to_csv(output_path, index=False)
            print(f"✅ Saved {ticker} officers (dict) to {output_path}")
        else:
            print(f"⚠️ No officer list for {ticker}")
    else:
        print(f"❌ Unexpected format for {ticker}: {type(officers)}")


def main():
    tickers = pd.read_csv(TICKERS_CSV)['Symbol'].dropna().unique().tolist()
    for ticker in tickers:
        save_officers_for_ticker(ticker)

if __name__ == '__main__':
    main()
