from financial_terminal import ticker
import pandas as pd

apple = ticker.Ticker("AAPL")

res = apple.balance_sheet
print(res)

        
    