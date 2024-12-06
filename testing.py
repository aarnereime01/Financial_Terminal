# import json object from folder companyfacts

import json
import requests
import bs4 as bs
import os


def get_sp500_tickers():
    """
    Get the tickers of the S&P 500 companies.
    """
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable sticky-header'})
    
    ticker_data = {}

    # find all tr inside tbody
    for row in table.find_all('tr')[1:]:
        
        ticker = row.find_all('td')[0].get_text(strip=True)
        
        ticker_data[ticker] = {
            'Sector': row.find_all('td')[2].get_text(strip=True),
            'Sub-Industry': row.find_all('td')[3].get_text(strip=True),
            'CIK': row.find_all('td')[6].get_text(strip=True),
        }
    
    return ticker_data


def delete_cik_files(cik):
    for filename in os.listdir('companyfacts'):
        if filename.endswith(".json"):
            cik_number = filename.split('.')[0][3:]
            if cik_number not in cik:
                os.remove(f'companyfacts/{filename}')


def get_labels(cik_file):
    with open(f"companyfacts/{cik_file}", "r") as f:
        data = json.load(f)
        labels = [label for label in data.get('facts').get('us-gaap').keys()]
        return labels
        


if __name__ == "__main__":
    tickers = get_sp500_tickers()
    print(f'Found {len(tickers)} tickers')
    
    # cik = set()
    
    # for ticker in tickers:
    #     cik_number = tickers[ticker]['CIK']
    #     cik.add(cik_number)
        
    # delete_cik_files(cik)
    
    # print(len(cik))
    
    # # check length of companyfacts folder
    # print(len(os.listdir('companyfacts')))
    
    # data = {}
    # for cik_file in os.listdir('companyfacts'):
    #     labels = get_labels(cik_file)
    #     data[cik_file] = labels
        
    # # in data dict find all common labels for all companies
    # common_labels = set(data[list(data.keys())[0]])
    
    # for cik_file in data:
    #     common_labels = common_labels.intersection(set(data[cik_file]))
        
    # print(common_labels)
    
    sector = set()
    sub_industry = set()
    
    for ticker in tickers:
        sector.add(tickers[ticker]['Sector'])
        sub_industry.add(tickers[ticker]['Sub-Industry'])
        
    print(sector)
    print(sub_industry)
    
    print(len(sector))
    print(len(sub_industry)) 
        