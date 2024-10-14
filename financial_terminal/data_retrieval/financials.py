from datetime import datetime
import requests
from collections import defaultdict
import pandas as pd


from ..utils import const
from bs4 import BeautifulSoup as bs


class Financials:

    def __init__(self, ticker: str, freq: str):
        self.ticker = ticker
        self.freq = self.check_valid_frequency(freq)

    def check_valid_frequency(self, freq: str) -> str:
        if freq in ['annual', 'quarterly']:
            return freq
        else:
            raise ValueError(
                'Frequency must be either "annual" or "quarterly"')

    def fetch_financial(self, name: str, freq: str):
        url = f'https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{
            self.ticker}'

        trailing_categories = ','.join(
            ['trailing' + x for x in const.fundamentals[name]])
        other_categories = ','.join(
            [freq + x for x in const.fundamentals[name]])
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
            response = requests.get(
                url, headers=headers, params=query_parameters)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def format_financials(self, data: dict) -> pd.DataFrame:
        data_dict = defaultdict(dict)
        for entry in data['timeseries']['result']:
            category = entry['meta']['type'][0]
            category_name = category.replace('trailing', '').replace(
                'annual', '').replace('quarterly', '')
            try:
                for value_entry in entry[category]:
                    if category[0] == 't':
                        date = 'TTM'
                        value = value_entry['reportedValue']['raw']
                    else:
                        date = '/'.join(value_entry['asOfDate'].split('-'))
                        value = value_entry['reportedValue']['raw']

                    data_dict[category_name][date] = value
            except:
                pass

        data_df = pd.DataFrame.from_dict(data_dict, orient='index')
        data_df = data_df.sort_index(axis=0)

        return data_df

    def get_balance_sheet(self):
        response = self.fetch_financial('balance-sheet', self.freq)
        return self.format_financials(response)

    def get_income_statement(self):
        response = self.fetch_financial('income-statement', self.freq)
        return self.format_financials(response)

    def get_cash_flow(self):
        response = self.fetch_financial('cash-flow', self.freq)
        return self.format_financials(response)


class Summary:

    def __inti__(self, ticker: str):
        self.ticker = ticker
        
    def scrape_summary(self):
        url = f'https://finance.yahoo.com/quote/{self.ticker.upper}/'
        
    
