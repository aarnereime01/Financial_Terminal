import pandas as pd

from .scrapers.fundamentals import Fundamentals
from .scrapers.insiders import Insiders

class TickerBase:

    def __init__(self, ticker: str):
        self.ticker = ticker

        self._fundamentals = Fundamentals(self.ticker)
        self._indsiders = Insiders(self.ticker)

    def __repr__(self) -> str:
        return f'Ticker of stock: {self.ticker}'
    
    def get_balance_sheet(self) -> pd.DataFrame:
        return self._fundamentals.get_balance_sheet()