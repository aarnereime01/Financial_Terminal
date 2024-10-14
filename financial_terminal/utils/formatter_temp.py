from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np


class Formatter:


    def format_profile(self, html_content) -> dict:
        soup = bs(html_content, 'html.parser')
        
        container_div = soup.find('div', class_='grid grid-cols-1 sm:grid-cols-3 gap-3')
        
        span_elements = container_div.find_all('span')
        span_texts = [span.get_text(strip=True) for span in span_elements]

        h2_elements = container_div.find_all('h2')
        h2_texts = [h2.get_text(strip=True) for h2 in h2_elements]
        
        return dict(zip(h2_texts, span_texts))
        

    def format_statements(self, html_content) -> pd.DataFrame:
        soup = bs(html_content, 'html.parser')
        
        table = soup.find('table', id='report-table')
        
        headers = [header.get_text(strip=True) for header in table.find('thead').find_all('th')] # get the headers
        headers = headers[1:]  # remove the first header as this has nothing to do with the data
        headers = [header[0:4] for header in headers] # get the first 4 characters of the header (the year)
        headers[0] = headers[0].replace('(', '') # Remove the parantheses from the first element
        
        data = {}
        for row in table.find('tbody').find_all('tr'):
            cells = row.find_all('td')
            data[cells[0].get_text(strip=True)] = [cell.get_text(strip=True).replace(',', '') for cell in cells[1:]]
            
        df = pd.DataFrame.from_dict(data, orient='index', columns=headers)

        # Remove report filing from index
        df = df.iloc[1:]
        
        # Convert values to numeric
        for column in df.columns:
            # print(f"Converting column: {column}")
            df[column] = pd.to_numeric(df[column], errors='coerce')
            
        return df
    
    
    def process_percentages(self, value):
        if isinstance(value, str) and '%' in value:
            return float(value.replace('%', '')) / 100
        return value
    
        
    def format_ratios(self, html_content) -> dict:
        soup = bs(html_content, 'html.parser')
        
        table = soup.find('table', id='report-table')
        
        headers = [header.get_text(strip=True) for header in table.find('thead').find_all('th')] # get the headers
        headers = headers[1:]  # remove the first header as this has nothing to do with the data
        headers = [header[0:4] for header in headers] # get the first 4 characters of the header (the year)
        headers[0] = headers[0].replace('(', '') # Remove the parantheses from the first element
        
        data = {}
        for row in table.find('tbody').find_all('tr'):
            cells = row.find_all('td')
            data[cells[0].get_text(strip=True)] = [cell.get_text(strip=True).replace(',', '') for cell in cells[1:]]
            
        df = pd.DataFrame.from_dict(data, orient='index', columns=headers)
        
        # df.drop([
        #     'Price Ratios',
        #     'Liquidity Ratios',
        #     'Margins',
        #     'Return',
        #     'Turnover Ratios',
        #     'Per Share Items (USD)',
        #     'Dividend Ratios'
        # ], inplace=True)
        
        df.replace('', np.nan, inplace=True)
        df.fillna(0.0, inplace=True)
        
        for col in df.columns:
            df[col] = df[col].apply(self.process_percentages)
        
        # Convert values to numeric
        for column in df.columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')
            
        return df
        
        
    def format_earnings(self, html_content) -> dict:
        ...


    def format_all(self, data: dict) -> dict:
            """Formats all the data and returns the processed dictionary"""
            formatted_data = {}
            for page, html_content in data.items():
                if page == 'profile':
                    formatted_data[page] = self.format_profile(html_content)
                elif page == 'income-statement':
                    formatted_data[page] = self.format_statements(html_content)
                elif page == 'balance-sheet-statement':
                    formatted_data[page] = self.format_statements(html_content)
                elif page == 'cash-flow-statement':
                    formatted_data[page] = self.format_statements(html_content)
                elif page == 'ratios':
                    formatted_data[page] = self.format_ratios(html_content)
                elif page == 'earnings':
                    formatted_data[page] = self.format_earnings(html_content)
                    
            return formatted_data