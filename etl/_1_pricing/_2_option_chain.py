import os
import pandas as pd
from yahooquery import Ticker
from time import sleep
from utils import TICKERS_CSV, PRICING_OPTION_CHAIN_OUTPUT_DIR

os.makedirs(PRICING_OPTION_CHAIN_OUTPUT_DIR, exist_ok=True)

# Load tickers
tickers = pd.read_csv(TICKERS_CSV)['Symbol'].dropna().unique().tolist()

def main():

    for symbol in tickers:
        print(f"🔄 Processing {symbol}...")

        try:
            tkr = Ticker(symbol)
            df = tkr.option_chain  # Already flattened multi-index DataFrame

            # Reset index (expiration & optionType are index levels)
            df = df.reset_index()
            df['symbol'] = symbol  # Ensure ticker column exists

            # Optional: reorder or rename columns
            cols = ['symbol', 'expiration', 'optionType', 'contractSymbol', 'strike',
                    'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'impliedVolatility',
                    'inTheMoney']
            df = df[cols]

            # Save to CSV
            file_path = os.path.join(PRICING_OPTION_CHAIN_OUTPUT_DIR, f"{symbol}.csv")
            df.to_csv(file_path, index=False)

            print(f"✅ Saved: {file_path}")
            sleep(0.5)  # Prevent rate limit

        except Exception as e:
            print(f"❌ Failed for {symbol}: {e}")
            continue

if __name__ == '__main__':
    main()


