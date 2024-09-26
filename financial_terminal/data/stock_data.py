from .scraper import Scraper
from ..utils import formatter as fmt
import time


class StockData(Scraper):
    
    def __init__(self, ticker: str):
        super().__init__(f'https://finance.yahoo.com/quote/{ticker.upper()}/')
        self.ticker = ticker.upper()
        
        self.main()

    def get_data(self):
        data = self.parse()
        return data
    
    def format_data(self, data: dict):
        return fmt.format_data(data)
    
    def main(self):
        """
        Scrapes the data and formats it, after formatting, we make calculations on several hand picked
        metrics to determine the stocks "quality", then it will serve as a row with values for each
        metric in the database (really just a pandas dataframe). 
        """
        data = self.get_data()
        
        self.format_data(data)