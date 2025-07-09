import os
import pandas as pd
from yahooquery import Ticker
from utils import TICKERS_CSV, FINANCIAL_STATEMENTS_OUTPUT_DIRS

def ensure_all_dirs():
    for category_dict in FINANCIAL_STATEMENTS_OUTPUT_DIRS.values():
        for path in category_dict.values():
            if not os.path.exists(path):
                os.makedirs(path)

def get_tickers_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df['Symbol'].dropna().unique().tolist()

def fetch_and_save_financials(ticker):
    try:
        print(f"📡 Fetching financials for {ticker}")
        tkr = Ticker(ticker)

        # Statements
        statements = {
            'BS_A': ('balance_sheet', 'annual', tkr.balance_sheet(frequency='a')),
            'BS_Q': ('balance_sheet', 'quarterly', tkr.balance_sheet(frequency='q')),
            'IS_A': ('income_statement', 'annual', tkr.income_statement(frequency='a')),
            'IS_Q': ('income_statement', 'quarterly', tkr.income_statement(frequency='q')),
            'CF_A': ('cash_flow', 'annual', tkr.cash_flow(frequency='a')),
            'CF_Q': ('cash_flow', 'quarterly', tkr.cash_flow(frequency='q')),
        }

        for label, (statement_type, freq, df) in statements.items():
            if isinstance(df, pd.DataFrame) and not df.empty:
                # Insert ticker symbol as first column
                df.insert(0, 'symbol', ticker)

                out_dir = FINANCIAL_STATEMENTS_OUTPUT_DIRS[statement_type][freq]
                file_path = os.path.join(out_dir, f"{ticker}_{label}.csv")
                df.to_csv(file_path, index=False)
                print(f"  ✅ Saved {label} to {file_path}")
            else:
                print(f"  ⚠️ No data for {ticker} - {label}")

    except Exception as e:
        print(f"❌ Error fetching financials for {ticker}: {e}")


def main():
    print("🚀 Starting _1_financial_statements.main()")
    ensure_all_dirs()

    tickers = get_tickers_from_csv(TICKERS_CSV)
    print(f"📄 Loaded {len(tickers)} tickers")

    for ticker in tickers:
        fetch_and_save_financials(ticker)

    print("✅ Done with _1_financial_statements.main()")


if __name__ == "__main__":
    main()
