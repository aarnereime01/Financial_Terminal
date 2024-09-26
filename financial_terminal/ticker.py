import pandas as pd

from .scrapers.financials import Financials

class Ticker:
    def __init__(self, ticker: str, freq: str = 'annual'):
        self.ticker = ticker.upper()
        self.freq = freq

        self._financials = Financials(self.ticker, self.freq)
        self._summray
        
        self._balance_sheet = self._financials.get_balance_sheet()
        self._income_statement = self._financials.get_income_statement()
        self._cash_flow = self._financials.get_cash_flow()
        
        self._summary = self._financials.get_summary()

    def __repr__(self) -> str:
        return f'Ticker: {self.ticker}'
    
    @property
    def balance_sheet(self) -> pd.DataFrame:
        return self._balance_sheet
    
    @property
    def income_statement(self) -> pd.DataFrame:
        return self._income_statement
    
    @property
    def cash_flow(self) -> pd.DataFrame:
        return self._cash_flow
    
    @property
    def summary(self) -> pd.DataFrame:
        return self._summary
    
