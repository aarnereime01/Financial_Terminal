from datetime import datetime
import requests

from ..utils.formatter import format_financials
from ..utils import const

class YahooFinanceAPI:
    def __init__(self, ticker: str, freq: str):
        self.ticker = ticker
        self.freq = freq
        
    def fetch_timeseries(self, name: str, freq: str):
        url = f'https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{self.ticker}'

        trailing_categories = ','.join(['trailing' + x for x in const.fundamentals[name]])
        other_categories = ','.join([freq + x for x in const.fundamentals[name]])
        comined_categories = ','.join([trailing_categories, other_categories])

        query_parameters = {
            'symbol': self.ticker,
            'type': comined_categories,
            'merge': 'false',
            'period1': '493590046',
            'period2': str(int(datetime.now().timestamp())),
            'corsDomain': 'finance.yahoo.com'
        }

        headers = {
            'Postman-Token': '',
            'Host': 'query1.finance.yahoo.com',
            'User-Agent': 'PostmanRuntime/7.36.1',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        try:
            response = requests.get(url, headers=headers, params=query_parameters)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        
    def fetch_historical(self):
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{self.ticker}'
        
        query_parameters = {
            'formatted': 'true',
            'region': 'US',
            'includeAdjustedClose': 'true',
            'interval': '1d',
            'period1': '378604800',
            'period2': str(int(datetime.now().timestamp())),
            'useYfid': 'true',
            'corsDomain': 'finance.yahoo.com'
        }

        headers = {
            'Postman-Token': '',
            'Host': 'query1.finance.yahoo.com',
            'User-Agent': 'PostmanRuntime/7.36.1',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        try:
            response = requests.get(url, headers=headers, params=query_parameters)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get_balance_sheet(self):
        response = self.fetch_timeseries('balance-sheet', self.freq)
        return format_financials(response)

    def get_income_statement(self):
        response = self.fetch_timeseries('income-statement', self.freq)
        return format_financials(response)

    def get_cash_flow(self):
        response = self.fetch_timeseries('cash-flow', self.freq)
        return format_financials(response)
    
    def get_statistics(self):
        response = self.fetch_timeseries('statistics', 'quarterly')
        return format_financials(response)
    
    


        