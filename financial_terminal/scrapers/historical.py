import requests
from datetime import datetime
import pandas as pd

class Historical:
    
    def __init__(self, ticker: str):
        self.ticker = ticker
        
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
        
    def _format(self, data: dict) -> pd.DataFrame:
        df = pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0])
        df['date'] = pd.to_datetime(data['chart']['result'][0]['timestamp'], unit='s')
        df.set_index('date', inplace=True)
        return df
        
    def get_historical(self):
        response = self.fetch_historical()
        return self._format(response)