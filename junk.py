# from collections import defaultdict
# import requests
# import pandas as pd
# import datetime
# import re
# import json

# from .const import fundamentals_keys


# class Fundamentals:
#     def __init__(self, ticker: str, include_trailing: bool):
#         self.ticker = ticker
#         self.include_trailing = include_trailing

#         self.period1 = '493590046'
#         self.period2 = self.convert_to_time_unix()


#     def convert_to_time_unix(self) -> int:
#         date = datetime.datetime.now()
#         return int(date.timestamp())

#     def http_request(self, wanted_financial: str) -> None:
#         url = f'https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{self.ticker}'
#         get_types = ','.join(fundamentals_keys[wanted_financial])

#         headers = {
#             'Postman-Token': '',
#             'Host': 'query2.finance.yahoo.com',
#             'User-Agent': 'PostmanRuntime/7.32.3',
#             'Accept': '*/*',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Connection': 'keep-alive'
#         }

#         query_params = {
#             'padTimeSeries': 'true',
#             'type': get_types,
#             'merge': 'false',
#             'period1': self.period1,
#             'period2': self.period2,
#             'corsDomain': 'finance.yahoo.com',
#         }

#         try:
#             response = requests.get(url, headers=headers, params=query_params)
#             response.raise_for_status()  # Raise an exception for HTTP errors
#             return response.json()
#         except requests.exceptions.RequestException as e:
#             print(f"Request failed: {e}")
#             return None

#     def make_dataframe(self, data: dict) -> pd.DataFrame:
#         data_dict = defaultdict(dict)

#         for entry in data['timeseries']['result']:
            
#             # Category of income statement
#             category = entry['meta']['type'][0]
#             category_fixed = category[0].upper() + category[1:]
#             category_name = category_fixed.replace('Trailing', '').replace('Annual', '')
#             category_name = re.findall('[A-Z][^A-Z]*', category_name)
#             category_name = ' '.join(category_name)

#             # Date and value
#             try:
#                 for value_entry in entry[category]:
#                     date = value_entry['asOfDate'].split('-')[0]
#                     value = value_entry['reportedValue']['raw']

#                     data_dict.setdefault(category_name, {}).setdefault(date, value)
#             except:
#                 pass

#         data_df = pd.DataFrame.from_dict(data_dict, orient='index')
#         data_df.reset_index(inplace=True)
#         data_df.rename(columns={'index': 'Category'}, inplace=True)

        
#         return data_df

#     def get_income_statement(self) -> None:
#         data = self.http_request('financials')
#         data_df = self.make_dataframe(data)

#         return data_df