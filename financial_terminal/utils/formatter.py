from bs4 import BeautifulSoup as bs, Tag
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


    def convert_to_numeric(self, value):
        value = value.replace(',', '').replace('--', '0')
        multipliers = {'T': 1e12, 'B': 1e9, 'M': 1e6, 'K': 1e3, '%': 0.01}
        if value[-1] in multipliers:
            return float(value[:-1]) * multipliers[value[-1]]
        try:
            return float(value)
        except ValueError:
            return None


    def multiply_by_thousand(self, value):
        value *= 1000
        return value


    def format_valuation_measures(self, soup: bs) -> dict:
        table = soup.find('table', class_='yf-104jbnt')
        if not table:
            return None

        # Extract table headers
        headers = [header.text for header in table.find_all('th')]
        headers = [self.clean_whitespace(header) for header in headers]

        # Extract table rows
        rows = []
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if cells:
                cells = [self.clean_whitespace(cell.text) for cell in cells]
                rows.append(cells)

        # Combine headers and rows into a dictionary
        valuation_measures = {}
        for i in rows:
            valuation_measures[i[0]] = dict(zip(headers[1:], i[1:]))

        df = pd.DataFrame.from_dict(valuation_measures, orient='index')

        # Convert values to numeric
        for column in df.columns:
            df[column] = df[column].apply(self.convert_to_numeric)

        return df


    def format_financial_highlights_or_trading_information(self, soup: bs, html_element: int) -> dict:
        table = soup.find_all('div', class_='column yf-14j5zka')[html_element]
        if not table:
            return None

        financial_highlights = {}

        # Extract all values
        labels = [str(lables.text)for lables in table.find_all('td', class_='label yf-vaowmx')]
        values = [value.text for value in table.find_all('td', class_='value yf-vaowmx')]

        # Clean up the labels as they contain extra whitespace
        fixed_labels = [self.clean_whitespace(label) for label in labels]
        fixed_values = [self.clean_whitespace(value) for value in values]

        fixed_values = [self.convert_to_numeric(value) for value in fixed_values]

        # Remove footnotes for trading information
        if html_element == 1:
            fixed_labels = [self.remove_footnotes(label) for label in fixed_labels]

        if len(fixed_labels) == len(fixed_values):
            financial_highlights = dict(zip(fixed_labels, fixed_values))

        return financial_highlights


    def format_statistics(self, html_content) -> dict:
        data = {}
        soup = bs(html_content, 'html.parser')

        # VALUATION MEASURES
        valuation_measures = self.format_valuation_measures(soup)
        data['valuation_measures'] = valuation_measures

        # FINANCIAL HIGHLIGHTS
        financial_highlights = self.format_financial_highlights_or_trading_information(soup, html_element=0)  # 0 for financial highlights
        data['financial_highlights'] = financial_highlights

        # TRADING INFORMATION
        trading_information = self.format_financial_highlights_or_trading_information(soup, html_element=1)  # 1 for trading information
        data['trading_information'] = trading_information

        return data


    def format_financials(self, html_content) -> dict:
        soup = bs(html_content, 'html.parser')

        table = soup.find('div', class_='table yf-1pgoo1f')

        # Extract headers
        headers = [header.text for header in table.find('div', class_='row yf-1ezv2n5')]
        headers = [self.clean_whitespace(header) for header in headers]

        # Remove empty headers
        headers = [header for header in headers if header]

        financials = {}
        # Extract row values
        for row in table.find('div', class_='tableBody yf-1pgoo1f'):
            if isinstance(row, Tag):
                cell_values = [cell.text for cell in row.find_all('div')]
                cell_values = [self.clean_whitespace(cell) for cell in cell_values]

                # In some cases, the row contains an extra empty cell, we remove this
                cell_values = [cell for cell in cell_values if cell]

                # For some reason, the labels are repeated, we remove the duplicates by starting at the second index
                cell_values = cell_values[1:]

                if len(cell_values) == len(headers):
                    financials[cell_values[0]] = dict(zip(headers[1:], cell_values[1:]))

        df = pd.DataFrame.from_dict(financials, orient='index')

        # Convert values to numeric
        for column in df.columns:
            df[column] = df[column].apply(self.convert_to_numeric)

        # Multiply values by 1000, exept for Basic EPS and Diluted EPS
        for index, row in df.iterrows():
            if index not in ['Basic EPS', 'Diluted EPS']:
                df.loc[index] = row.apply(self.multiply_by_thousand)

        return df


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
                formatted_data[page] = self.format_financials(html_content)
            elif page == 'cash-flow':
                formatted_data[page] = self.format_financials(html_content)
        return formatted_data
