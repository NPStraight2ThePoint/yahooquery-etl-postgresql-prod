import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from utils import STATIC_DIR

def scrape_sp500_tickers(output_dir: str, save_csv: bool = True) -> list:
    """
    Scrapes the list of S&P 500 tickers from Wikipedia and optionally saves to CSV.

    Args:
        output_dir (str): Folder to save CSV output
        save_csv (bool): Whether to save the scraped data as CSV

    Returns:
        List[str]: List of ticker symbols
    """
    os.makedirs(output_dir, exist_ok=True)

    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})
    df = pd.read_html(str(table))[0]

    tickers = df['Symbol'].tolist()

    if save_csv:
        output_path = os.path.join(output_dir, 'Tickers.csv')
        df.to_csv(output_path, index=False)
        print(f"✅ Saved S&P 500 tickers to: {output_path}")

    return tickers

if __name__ == '__main__':
    tickers = scrape_sp500_tickers(STATIC_DIR)
    print(f"✅ Total tickers scraped: {len(tickers)}")
