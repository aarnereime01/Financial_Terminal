from datetime import datetime
import requests

from ..utils.formatter import format_json_to_df
from ..utils import const

class Fundamentals:
    def __init__(self, ticker: str, freq: str):
        self.ticker = ticker
        self.freq = freq

    def get_balance_sheet(self):
        return self.fetch_timeseries('balance-sheet')

    def get_income_statement(self):
        return self.fetch_timeseries('income-statement')

    def get_cash_flow(self):
        return self.fetch_timeseries('cash-flow')

    def fetch_timeseries(self, name: str):
        url = f'https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{self.ticker}'

        trailing_categories = ','.join(['trailing' + x for x in const.fundamentals[name]])
        other_categories = ','.join([self.freq + x for x in const.fundamentals[name]])
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
            df = format_json_to_df(response.json())
            return df
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None


        