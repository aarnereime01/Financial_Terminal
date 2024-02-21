import pandas as pd

from .scrapers.fundamentals import Fundamentals
from .scrapers.insiders import Insiders

class Ticker:
    def __init__(self, ticker: str, freq: str = 'annual'):
        self.ticker = ticker
        self.freq = freq

        self._fundamentals = Fundamentals(self.ticker, self.freq)
        self._indsiders = Insiders(self.ticker)

    def __repr__(self) -> str:
        return f'Ticker of stock: {self.ticker}'
    
    @property
    def balance_sheet(self) -> pd.DataFrame:
        return self._fundamentals.get_balance_sheet()
    
    @property
    def income_statement(self) -> pd.DataFrame:
        return self._fundamentals.get_income_statement()
    
    @property
    def cash_flow(self) -> pd.DataFrame:
        return self._fundamentals.get_cash_flow()