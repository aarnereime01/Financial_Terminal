from financial_terminal.data import stock_data as sd
from financial_terminal.utils import metric_calculations as mc

import pandas as pd
import os
import requests
import bs4 as bs
import numpy as np

# display all rows
# pd.set_option('display.max_rows', None)

# Path to store the CSV file
FILE_PATH = "stock_metrics.csv"

def update_database(ticker, metrics):
    
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
    else:
        df = pd.DataFrame(columns=['ticker'] + list(metrics.keys()))
        
    # If the number of columns in the DataFrame is not equal to the number of metrics + 1 add the missing columns
    if len(df.columns) != len(metrics) + 1:
        missing_columns = list(set(metrics.keys()) - set(df.columns))
        for column in missing_columns:
            df[column] = None
            
    # Remove columns that are not in the metrics
    removed_columns = list(set(df.columns) - set(metrics.keys()) - {'ticker'})
    if removed_columns:
        df = df.drop(columns=removed_columns)
        
    # Check if the stock is already in the DataFrame
    if ticker in df['ticker'].values:
        # Update the stock metrics for all columns except the ticker
        df.loc[df['ticker'] == ticker, df.columns != 'ticker'] = list(metrics.values())
    else:
        # Add the stock to the DataFrame
        new_row = [ticker] + list(metrics.values())
        df.loc[len(df)] = new_row

    # Save the DataFrame to a CSV file
    df.to_csv(FILE_PATH, index=False)
    print(f"Updated the database for stock: {ticker}")
    
    
def give_scores(score_df):
    """
    For each column/metric in the DataFrame, sort the values in order given by a mapping that tells it to be 
    either ascending or descending, then rank the stocks based on the sorted values. Lower rank is better.
    """
    # System sorts in ascending order:
    # True -> Sorts from lowest to highest 
    # False -> Sorts from highest to lowest
    # The rank() gives 1 point to the first place, 2 points to the second place, and so on.
    # Therefore, the best stock will have the lowest rank/score.
    sorting_map = {
            # VALUATION METRICS
            'trailing_pe_ratio': True,
            'forward_pe_ratio': True,
            'peg_ratio': True,
            'pb_ratio': True,
            'ps_ratio': True,
            'enterprise_value_revenue': True,
            'enterprise_value_ebitda': True,
            
            # PROFITABILITY METRICS
            'profit_margin': False,
            'operating_margin': False,
            
            # MANAGEMENT EFFICIENCY METRICS
            'return_on_assets': False,
            'return_on_equity': False,
            
            # INCOME STATEMENT METRICS
            'revenue_by_mkt_cap': False,
            'quarterly_revenue_growth_yoy': False,
            'quarterly_earnings_growth_yoy': False,
            'gross_profit': False,
            'gross_profit_by_mkt_cap': False,
            'net_income': False,
            'net_income_by_mkt_cap': False,
            
            # BALANCE SHEET METRICS
            'debt_to_equity_ratio': True,
            'asset_to_liability_ratio': False,
            
            # CASH FLOW METRICS
            'operating_cash_flow': False,
            'operating_cash_flow_by_mkt_cap': False,
            'levered_free_cash_flow': False,
            'levered_free_cash_flow_by_mkt_cap': False,
        }
    
    scores = pd.DataFrame(index=score_df.index)

    for metric, order in sorting_map.items():
        # Sort the metric and assign ranks
        ranked = score_df[metric].rank(ascending=order)
            
        # Assign scores: highest rank gets highest score
        scores[metric + ' Score'] = ranked

    # Calculate total score as the sum of all individual scores
    score_df['Total Score'] = scores.sum(axis=1)
    
    # Sort the DataFrame by the total score in ascending order
    score_df = score_df.sort_values(by='Total Score', ascending=True)
    
    # Save the DataFrame of only ticker and total score
    score_df[['ticker', 'Total Score']].to_csv('stock_scores.csv', index=False)


def get_sp500_tickers(ignore_ticker_in_df=False):
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
    
    print(f"Found {len(tickers)} tickers")
    
    if not ignore_ticker_in_df:
        df = pd.read_csv(FILE_PATH)
        
        # get set of all tickers in the DataFrame
        tickers_in_df = set(df['ticker'])
        print(f"Found {len(tickers_in_df)} tickers in the DataFrame")
        
        # get set of all tickers from the S&P 500
        tickers = set(tickers)
        
        # get the difference between the two sets
        tickers = list(tickers - tickers_in_df)
        
        print(f"Found {len(tickers)} tickers not in the DataFrame")
    
    return tickers, len(tickers_in_df)

if __name__ == '__main__':
    print("Running the main function")
    stocks_to_process, stocks_in_df = get_sp500_tickers()
    count = 1
    for stock in stocks_to_process:
        print(f"Processing stock: {stock}")
        ticker = sd.StockData(stock) 
        formatted_data = ticker.main()

        # Calculate metrics for the stock
        metrics = mc.Calculations(formatted_data).main()
         
        # Update the stock metrics in the DataFrame
        update_database(ticker.ticker, metrics)
        
        print(f"Finished processing stock: {stock}, {count}/{len(stocks_to_process)}")
        count += 1    
    
    score_df = pd.read_csv(FILE_PATH).copy(deep=True)
    
    # Fill na with the averge value of the column
    score_df.fillna(score_df.select_dtypes(include=np.number).mean(), inplace=True)
    
    # Give scores to the stocks
    give_scores(score_df)