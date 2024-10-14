from .scraper_temp import Scraper
from ..utils.formatter_temp import Formatter
from ..utils.metric_calculations_temp import Calculations

import pandas as pd
import os


class StockDataHandler():

    def __init__(self, tickers: str):
        self.master_csv_path = self.get_master_csv_path()
        self.tickers = self.validate_tickers(tickers)
        self.formatter = Formatter()
        
    
    def validate_tickers(self, tickers: list[str]) -> list[str]:
        """Checks that the tickers input is a list of strings and returns a list of uppercase tickers"""
        if not isinstance(tickers, list):
            raise ValueError("Tickers must be a list of strings, for example ['aapl', 'msft']")
        
        tickers = [ticker.upper() for ticker in tickers]
        
        # Remove tickers that already exist in the master csv file
        try:
            master_df = pd.read_csv(self.master_csv_path)
            
            master_df_tickers = set(master_df['ticker'].values)
            new_tickers = set(tickers)
            
            tickers = list(new_tickers - master_df_tickers)
        except pd.errors.EmptyDataError:
            pass
        
        print(f"Number of tickers to process: {len(tickers)}")
        return tickers
        
        
    def get_master_csv_path(self):
        """
        Checks if the master csv file exists, if not, it creates it.
        (Master csv file is the file that holds all the stock data)
        """
        path = os.path.join('financial_terminal/data', 'master.csv')
        
        if os.path.exists(path):
            return path
        else:
            # Create the an empty csv file
            with open(path, 'w') as f:
                f.write('')
            return path


    def get_html_page_source(self, ticker) -> dict:
        """Retrieves raw data by scraping"""
        return Scraper(ticker).parse_pages()


    def format_data(self, data: dict) -> dict:
        """Formats the scraped data"""
        return self.formatter.format_all(data)
    

    def update_database(self, metrics: dict) -> None:
        """
        use key as headers and values as rows
        save to master csv file
        """
        # Get the master csv file
        try:
            master_df = pd.read_csv(self.master_csv_path)
        except pd.errors.EmptyDataError:
            # Create an empty DataFrame with predefined columns if file is empty
            master_df = pd.DataFrame(columns=list(metrics.keys()))
        
        # Add the metrics data to the master csv file
        master_df.loc[len(master_df)] = list(metrics.values())
        
        master_df.to_csv(self.master_csv_path, index=False)
        
    
    def sort_stocks_into_sectors(self):
        """
        Sorts the stocks from the master csv file into sectors and save them into each sector's csv file.
        """
        df = pd.read_csv(self.master_csv_path)
        
        sectors = df['sector'].unique()
        
        for sector in sectors:
            sector_df = df[df['sector'] == sector]
            sector_df.to_csv(f'financial_terminal/data/{sector}.csv', index=False)
            self.give_scores(sector_df, sector)
            
    
    def give_scores(self, score_df, sector):
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
            'pe_ratio': True,
            'ps_ratio': True,
            'pb_ratio': True,
            'pfcf_ratio': True,
            'pocf_ratio': True,
            'pegr_ratio': True,
            'ev_to_ebitda': True
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
        score_df[['ticker', 'Total Score']].to_csv(f'financial_terminal/data/stock_scores_{sector}.csv', index=False)


    def main(self) -> None:
        """
        Scrapes the data and formats it, after formatting, we make calculations on several hand picked
        metrics to determine the stocks "quality", then it will serve as a row with values for each
        metric in the database (really just a pandas dataframe). 
        """
        count = 1
        for ticker in self.tickers:
            print(f"Processing {ticker}")
            html_page_source = self.get_html_page_source(ticker)
            formatted_data = self.format_data(html_page_source)
            formatted_data['ticker'] = ticker
            metrics = Calculations(formatted_data).main()
            
            self.update_database(metrics)
            print(f"Processed {count}/{len(self.tickers)}")
            print('-----------------------------------')
            print()
            count += 1
            
            
        # self.sort_stocks_into_sectors()
        
