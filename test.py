from financial_terminal import ticker

apple = ticker.Ticker('NVDA', freq='quarterly')
print(apple.income_statement)

        