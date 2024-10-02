from bs4 import BeautifulSoup as bs
from collections import defaultdict
from pprint import pprint
import pandas as pd


class Formatter:
    """Handles the formatting of scraped data"""

    def clean_whitespace(self, text):
        return ' '.join(text.split())
    
    def remove_footnotes(self, text):
        txt = text.split(' ')
        if txt[-1].isnumeric():
            return ' '.join(txt[:-1])
        else:
            return text

    def format_valuation_measures(self, soup: bs) -> dict:
        table = soup.find('table', class_='yf-104jbnt')
        if not table:
            return None

        # Extract table headers
        headers = [header.text for header in table.find_all('th')]

        # Extract table rows
        rows = []
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if cells:
                rows.append([cell.text for cell in cells])

        # Combine headers and rows into a dictionary
        valuation_measures = {}
        for i in rows:
            valuation_measures[i[0]] = dict(zip(headers[1:], i[1:]))

        return pd.DataFrame.from_dict(valuation_measures, orient='index')

    def format_financial_highlights_or_trading_information(self, soup: bs, html_element: int) -> dict:
        table = soup.find_all('div', class_='column yf-14j5zka')[html_element]
        if not table:
            return None

        financial_highlights = {}

        # Extract all values
        labels = [str(lables.text)
                  for lables in table.find_all('td', class_='label yf-vaowmx')]
        values = [value.text for value in table.find_all(
            'td', class_='value yf-vaowmx')]

        # Clean up the labels as they contain extra whitespace
        fixed_labels = [self.clean_whitespace(label) for label in labels]
        
        # Remove footnotes for trading information
        if html_element == 1:
            fixed_labels = [self.remove_footnotes(label) for label in fixed_labels]

        if len(fixed_labels) == len(values):
            financial_highlights = dict(zip(fixed_labels, values))

        return financial_highlights

    def format_statistics(self, html_content) -> dict:
        data = {}
        soup = bs(html_content, 'html.parser')

        # VALUATION MEASURES
        valuation_measures = self.format_valuation_measures(soup)
        data['valuation_measures'] = valuation_measures

        # FINANCIAL HIGHLIGHTS
        financial_highlights = self.format_financial_highlights_or_trading_information(
            soup, html_element=0)  # 0 for financial highlights
        data['financial_highlights'] = financial_highlights

        # TRADING INFORMATION
        trading_information = self.format_financial_highlights_or_trading_information(
            soup, html_element=1)  # 1 for trading information
        data['trading_information'] = trading_information

        return data

    def format_financials(self, html_content) -> dict:
        """Formats the financials data"""
        return ...

    def format_balance_sheet(self, html_content) -> dict:
        """Formats the balance sheet data"""
        return ...

    def format_cash_flow(self, html_content) -> dict:
        """Formats the cash flow data"""
        return ...

    def format_all(self, data: dict) -> dict:
        """Formats all the data and returns the processed dictionary"""
        formatted_data = {}
        for page, html_content in data.items():
            if page == 'key-statistics':
                formatted_data[page] = self.format_statistics(html_content)
            elif page == 'financials':
                formatted_data[page] = self.format_financials(html_content)
            elif page == 'balance-sheet':
                formatted_data[page] = self.format_balance_sheet(html_content)
            elif page == 'cash-flow':
                formatted_data[page] = self.format_cash_flow(html_content)
        return formatted_data
