from data_pipeline.stock_selector import StockSelector
from financial_terminal_3.data_pipeline.morningstar_financials import Morningstar
from data_pipeline.morningstar_companyid import CompanyID

if __name__ == '__main__':

    stockselector = StockSelector()
    
    stock_list = stockselector.stock_list
    print(f'Number of stocks in stock list: {len(stock_list)}')
    # sector_counter = Counter([info['Sector'] for info in stock_list.values()])


