import pandas as pd
from collections import defaultdict


def format_json_to_df(data: dict) -> pd.DataFrame:
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