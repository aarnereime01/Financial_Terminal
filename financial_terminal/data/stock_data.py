from .scraper import YahooFinanceScraper
from ..utils.formatter import Formatter
import json


class StockData():

    def __init__(self, ticker: str):
        self.scraper = YahooFinanceScraper(ticker)
        self.ticker = ticker.upper()
        self.formatter = Formatter()

    def get_raw_data(self) -> dict:
        """Retrieves raw data by scraping"""
        return self.scraper.parse_pages()

    def format_data(self, data: dict) -> dict:
        """Formats the scraped data"""
        return self.formatter.format_all(data)

    def main(self) -> None:
        """
        Scrapes the data and formats it, after formatting, we make calculations on several hand picked
        metrics to determine the stocks "quality", then it will serve as a row with values for each
        metric in the database (really just a pandas dataframe). 
        """
        raw_data = self.get_raw_data()
        formatted_data = self.format_data(raw_data)
        print(formatted_data)
        print(f"Formatted Data for {self.ticker}")
