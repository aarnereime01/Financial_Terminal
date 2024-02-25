import pandas as pd

from .scrapers.yahooAPI import YahooFinanceAPI
from .scrapers.insiders import Insiders

class Ticker:
    def __init__(self, ticker: str, freq: str = 'annual'):
        self.ticker = ticker.upper()
        self.freq = freq

        self._financials = YahooFinanceAPI(self.ticker, self.freq)
        self._indsiders = Insiders(self.ticker)

    def __repr__(self) -> str:
        return f'Ticker: {self.ticker}'
    
    @property
    def balance_sheet(self) -> pd.DataFrame:
        return self._financials.get_balance_sheet()
    
    @property
    def income_statement(self) -> pd.DataFrame:
        return self._financials.get_income_statement()
    
    @property
    def cash_flow(self) -> pd.DataFrame:
        return self._financials.get_cash_flow()
    
    @property
    def insider(self) -> pd.DataFrame:
        return self._indsiders.get_insider_transactions()
    
    @property
    def historical(self) -> pd.DataFrame:
        return self._financials.fetch_historical()