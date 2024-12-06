import requests
import time
import pandas as pd
import os


"""
This script is used to fetch company ids from morningstar api. This is kinda a one time operation,
so you can run this script once and then comment out the code in the main.py file.

Hence, the shitty code quality/structure :)
"""

class APIHandler:
        
        def __init__(self, url: str):
            self.url = url
            
            self.headers = {
                'Apikey': 'lstzFDEOhfFNMLikKa0am9mgEKLBl49T',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)',
                'Cookie': ... # Cookie will eventually expire, so you need to update it with a new one, use inspect element in your browser to get the cookie,
            }
            
        def get_data(self):
            response = requests.get(self.url, headers=self.headers)
            return response
    
class CompanyID:
    
    def __init__(self, stocks: dict):
        self.stocks = stocks
        self.file_path = '/Users/arnereime/Documents/Financial_Terminal/financial_terminal_3/data/companyids.csv'
        self.get_comapny_ids()
        
    def calculate_remaining_stocks(self):
        companyid = pd.read_csv(self.file_path)
        finished_stocks = companyid['Symbol'].tolist()
        remaining_stocks = [symbol for symbol in self.stocks.keys() if symbol not in finished_stocks]
        return remaining_stocks
         
    def get_comapny_ids(self):
        
        remaining_stocks = self.calculate_remaining_stocks()
        print(f'Number of remaining stocks: {len(remaining_stocks)}')
        
        new_data = []
        
        for i, stock_symbol in enumerate(remaining_stocks):
            print(f'{i+1}/{len(remaining_stocks)}')
            print(f'Fetching data for {stock_symbol}')
            
            stock_symbol = stock_symbol.replace('/', '.')
            
            url_1 = f'https://www.morningstar.com/api/v2/stocks/xnys/{stock_symbol.lower()}'
            url_2 = f'https://www.morningstar.com/api/v2/stocks/xnas/{stock_symbol.lower()}'

            # first try NYSE
            api_handler = APIHandler(url_1)
            data = api_handler.get_data()
            if data:
                # check status code
                print(data.status_code)
                if data.status_code == 202:
                    break
                new_data.append({'Symbol': stock_symbol, 'CompanyId': data.json()['page']['securityID']})
            else:
                api_handler = APIHandler(url_2)
                data = api_handler.get_data()
                if data:
                    print(data.status_code)
                    if data.status_code == 202:
                        break
                    new_data.append({'Symbol': stock_symbol, 'CompanyId': data.json()['page']['securityID']})
                else:
                    print(f'No data found for {stock_symbol}')
        
        df = pd.DataFrame(new_data)
        
        if os.path.exists(self.file_path):
            # Append without rewriting the header
            df.to_csv(self.file_path, mode='a', index=False, header=False)
        else:
            # Write with the header for the first time
            df.to_csv(self.file_path, mode='w', index=False)
        
        
        
