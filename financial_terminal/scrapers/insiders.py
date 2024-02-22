from bs4 import BeautifulSoup
import requests
import pandas as pd

class Insiders:
    def __init__(self, ticker: str):
        self.ticker = ticker

        self.filing_date = {
            '1w': '7',
            '2w': '14',
            '1m': '30',
            '2m': '60',
            '3m': '90',
            '6m': '180',
            '1y': '365',
            '2y': '730',
            '4y': '1461',
        }

    def get_insider_transactions(self, period: str = '1y'):
        data_dict = {}
        url = f'http://openinsider.com/screener?s={self.ticker}&o=&pl=&ph=&ll=&lh=&fd={self.filing_date[period]}&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find_all('table')[11]
        columns = [th.text for th in table.find('tr').find_all('th')]
        columns = [x.replace('\xa0', ' ').strip() for x in columns]

        rows = table.find_all('tr')[1:] 
        for idx, row in enumerate(rows):
            filing_date = row.find_all('div')[0].text
            trade_date = row.find_all('div')[1].text
            ticker = row.find_all('a')[1].text
            insider_name = row.find_all('a')[2].text
            title = row.find_all('td')[5].text
            trade_type = row.find_all('td')[6].text
            price = row.find_all('td')[7].text
            quantity = row.find_all('td')[8].text
            owned = row.find_all('td')[9].text
            owned_change = row.find_all('td')[10].text
            value = row.find_all('td')[11].text
            data_dict[idx] = [filing_date, trade_date, ticker, insider_name, title, trade_type, price, quantity, owned, owned_change, value]

        df = pd.DataFrame.from_dict(data_dict, orient='index', columns=columns[1:12])
        return df
    