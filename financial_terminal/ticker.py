import pandas as pd

from .tickerbase import TickerBase


class Ticker(TickerBase):

    def __init__(self, ticker: str, exchange: str, currency: str):
        super().__init__(ticker, exchange, currency)


    @property
    def yearly_dividens(self) -> pd.DataFrame:
        return self.get_yearly_dividends()