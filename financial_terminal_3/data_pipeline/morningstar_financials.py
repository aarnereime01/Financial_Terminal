import requests
import time
import pandas as pd

class APIHandler:
        
        def __init__(self, url: str):
            self.url = url
            
            self.headers = {
                'Apikey': 'lstzFDEOhfFNMLikKa0am9mgEKLBl49T',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)',
            }
            
            self.params = {
            }
            
        def get_data(self):
            response = requests.get(self.url, headers=self.headers, params=self.params)
            return response.json()
    
class MorningstarFinancials:
    
    def __init__(self, stocks: dict):
        self.stocks = stocks
        self.stock_company_ids = self.get_stock_company_ids()
        
    def get_stock_company_ids(self):
        ...
        
    def get_income_statement(self, company_id: str):
        url = f'https://api-global.morningstar.com/sal-service/v1/stock/newfinancials/{company_id}/incomeStatement/detail?dataType=A&reportType=A&locale=en&languageId=en&locale=en&clientId=MDC&component=sal-equity-financials-details&version=4.30.0'

    
    
        
    