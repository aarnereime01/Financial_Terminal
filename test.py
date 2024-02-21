from financial_terminal import ticker

apple = ticker.Ticker("AAPL")

res = apple.balance_sheet

for entry in res['timeseries']['result']:
    print(entry)
    print('--------')
