from .stock_data import SP500
from .ticker import TickerData


class StockHandler():
    
    def __init__(self):
        self.company_foldername = 'companyfacts'
        self.sp_500 = SP500(self.company_foldername)
        
        
    def main(self):
        tickers = self.sp_500.tickers
        
        for ticker, values in tickers.items():
            stock = TickerData(
                ticker=ticker,
                industry=values.get('sub_industry'),
                sector=values.get('sector'),
                cik=values.get('cik'),
                company_foldername=self.company_foldername
            )
            
            print(stock)
            stock.main()
            break