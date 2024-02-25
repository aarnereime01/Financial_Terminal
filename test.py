from financial_terminal import ticker
import plotly.express as px

stock = ticker.Ticker('msft')
df = stock.historical

fig = px.line(df, x=df.index, y="close", title='Microsoft Stock Price')
fig.show()