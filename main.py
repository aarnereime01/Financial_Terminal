from financial_terminal.data_retrieval import stock_data_handler as sd
from financial_terminal.data_retrieval import xml_handler as xh

import pandas as pd
import os
import requests
import bs4 as bs
import time


def get_sp500_tickers():
    """
    Get the tickers of the S&P 500 companies.
    """
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable sticky-header'})
    
    ticker_data = {}

    # find all tr inside tbody
    for row in table.find_all('tr')[1:]:
        
        ticker = row.find_all('td')[0].get_text(strip=True)
        
        ticker_data[ticker] = {
            'Sector': row.find_all('td')[2].get_text(strip=True),
            'Sub-Industry': row.find_all('td')[3].get_text(strip=True),
            'CIK': row.find_all('td')[6].get_text(strip=True),
        }
    
    return ticker_data
        

if __name__ == '__main__':
    tickers = get_sp500_tickers()
    print(f'Found {len(tickers)} tickers')
    
    xh.XMLHandler('COST', '0000909832').main()
    
    # Scrape the data for each stock
    # sd.StockDataHandler(tickers).main()
    
    
    