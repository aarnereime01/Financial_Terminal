from financial_terminal.data import stock_data as sd

if __name__ == '__main__':
    stock = sd.StockData('msft')
    stock.main()