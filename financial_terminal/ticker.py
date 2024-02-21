import pandas as pd

from .tickerbase import TickerBase


class Ticker(TickerBase):

    def __init__(self, ticker: str):
        super().__init__(ticker)


    @property
    def balance_sheet(self) -> pd.DataFrame:
        return self.get_balance_sheet()