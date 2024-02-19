import pandas as pd

from .scrapers.fundamentals import Fundamentals
from .scrapers.insiders import Insiders

class TickerBase:

    def __init__(self, ticker: str, exchange: str, currency: str):
        self.ticker = ticker
        self.exchange = exchange
        self.currency = currency

        self._fundamentals = Fundamentals(self._data, self.ticker)
        self._indsiders = Insiders(self._data, self.ticker)

    def __repr__(self) -> str:
        return f"{self.ticker} ({self.exchange})"
    
    def get_year_over_year(self) -> pd.DataFrame:
        pass