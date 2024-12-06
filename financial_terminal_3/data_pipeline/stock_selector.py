import pandas as pd
import os

class StockSelector:
    
    def __init__(self):
        self.cwd = os.getcwd()
        self.nasdaq_stock_screener_csv_path = os.path.join(self.cwd, 'financial_terminal_3/data/nasdaq_screener.csv')
        self.stock_list = self.get_stock_list()
        
        
    def get_stock_screen_data(self) -> pd.DataFrame:
        try:
            return pd.read_csv(self.nasdaq_stock_screener_csv_path)
        except FileNotFoundError:
            print('File not found, Please visit https://www.nasdaq.com/market-activity/stocks/screener to download the csv file and place it in the data folder with name: nasdaq_screener.csv')
            return None
        
        
    def get_stock_list(self) -> pd.DataFrame:
        
        stocks_df = self.get_stock_screen_data()
        stocks_df = stocks_df[stocks_df['Market Cap'] > 20_000_000_000] # Filter out stocks with market cap less than 10 billion

        stock_dict = stocks_df.set_index('Symbol')[['Sector', 'Industry', 'Market Cap']].to_dict(orient='index')
        
        # Handle nan values
        for symbol, info in stock_dict.items():
            # BRK.A and BRK.B have no sector or industry info, but we will put them in the finance sector
            if symbol == 'BRK/A' or symbol == 'BRK/B':
                stock_dict[symbol]['Sector'] = 'Finance'
                stock_dict[symbol]['Industry'] = 'Insurance - Diversified'
            if pd.isna(info['Sector']):
                stock_dict[symbol]['Sector'] = 'Unknown'
            if pd.isna(info['Industry']):
                stock_dict[symbol]['Industry'] = 'Unknown'
                
        return stock_dict     
