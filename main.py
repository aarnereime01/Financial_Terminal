from financial_terminal.data_retrieval import stock_data_handler as sd

import pandas as pd
import os
import requests
import bs4 as bs


def get_sp500_tickers():
    """
    Get the tickers of the S&P 500 companies.
    """
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable sticky-header'})
    
    tickers = []

    # find all tr inside tbody
    for row in table.find_all('tr')[1:]:
        ticker = row.find_all('td')[0].text
        tickers.append(ticker)
        
    tickers = [s.replace('\n', '') for s in tickers]
    tickers = list(filter(None, tickers))
    
    return tickers

if __name__ == '__main__':
    tickers = get_sp500_tickers()
    
    # Scrape the data for each stock
    sd.StockDataHandler(tickers).main()
    
    
    