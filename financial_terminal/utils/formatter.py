import pandas as pd
from collections import defaultdict


def format_financials(data: dict) -> pd.DataFrame:
    data_dict = defaultdict(dict)
    for entry in data['timeseries']['result']:
        category = entry['meta']['type'][0]
        category_name = category.replace('trailing', '').replace('annual', '').replace('quarterly', '')
        try:
            for value_entry in entry[category]:
                if category[0] == 't':
                    date = 'TTM'
                    value = value_entry['reportedValue']['raw']
                else:
                    date = '/'.join(value_entry['asOfDate'].split('-'))
                    value = value_entry['reportedValue']['raw']  
            
                data_dict[category_name][date] = value
        except:
            pass
        
    data_df = pd.DataFrame.from_dict(data_dict, orient='index')
    data_df = data_df.sort_index(axis=0)
    
    return data_df


def format_insiders(df: pd.DataFrame) -> pd.DataFrame:
    df['Filing Date'] = pd.to_datetime(df['Filing Date'])
    df['Trade Date'] = pd.to_datetime(df['Trade Date'])
    df['Price'] = df['Price'].str.replace('$', '').astype(float)
    df['Qty'] = df['Qty'].str.replace(',', '').astype(int)
    df['Owned'] = df['Owned'].str.replace(',', '').astype(int)
    df['Owned Change'] = df['Owned Change'].str.replace('+', '').str.replace('-', '').str.replace('%', '').astype(float) / 100
    df['Value'] = df['Value'].str.replace('$', '').str.replace(',', '').astype(float)
    
    return df