import json

class Calculations:
    
    def __init__(self, data):
        self.data = data
        
        
    def pe_ratio(self):
        """
        The price-to-earnings (P/E) ratio is the proportion of a company's share price to its earnings per share. 
        A high P/E ratio could mean that a company's stock is overvalued or that investors expect high growth rates.
        
        Formula: P/E ratio = Market value per share / Earnings per share
        """
        try:
            trailing_pe_ratio = self.data.get('key-statistics').get('valuation_measures').loc['Trailing P/E', 'Current']
            forward_pe_ratio = self.data.get('key-statistics').get('valuation_measures').loc['Forward P/E', 'Current']
        except:
            trailing_pe_ratio = None
            forward_pe_ratio = None
        return trailing_pe_ratio, forward_pe_ratio
    
    
    def peg_ratio(self):
        """
        The 'PEG ratio' (price/earnings to growth ratio) is a valuation metric for determining the relative trade-off 
        between the price of a stock, the earnings generated per share (EPS), and the company's expected growth. 
        In general, the P/E ratio is higher for a company with a higher growth rate.
        
        Formula: PEG ratio = (Market value per share / Earnings per share) / Earnings Per Share growth rate
        """
        try:
            peg_ratio = self.data.get('key-statistics').get('valuation_measures').loc['PEG Ratio (5yr expected)', 'Current']
        except:
            peg_ratio = None
        return peg_ratio
    
    
    def pb_ratio(self):
        """
        You can calculate the price-to-book, or P/B, ratio by dividing a company's stock price by its book value per share, 
        which is defined as its total assets minus any liabilities. This can be useful when you're conducting a 
        thorough analysis of a stock.
        
        Formula: P/B ratio = Market value per share / Book value per share
        """
        try:
            pb_ratio = self.data.get('key-statistics').get('valuation_measures').loc['Price/Book', 'Current']
        except:
            pb_ratio = None
        return pb_ratio
    
    
    def ps_ratio(self):
        """
        The price-to-sales (P/S) ratio is a valuation ratio that compares a company's stock price to its revenues. 
        It is an indicator of the value placed on each dollar of a company's sales or revenues.
        
        Formula: P/S ratio = Market value per share / Sales per share
        """
        try:
            ps_ratio = self.data.get('key-statistics').get('valuation_measures').loc['Price/Sales', 'Current']
        except:
            ps_ratio = None
        return ps_ratio
    
    
    def enterprise_value_revenue(self):
        """
        The Enterprise Value to Revenue Multiple is a valuation metric used to value a business by dividing its 
        enterprise value (equity plus debt minus cash) by its annual revenue
        
        Formula: EV/R = Enterprise Value / Revenue
        """
        try:
            evr = self.data.get('key-statistics').get('valuation_measures').loc['Enterprise Value/Revenue', 'Current']
        except:
            evr = None
        return evr
        
    def enterprise_value_ebitda(self):
        """
        Enterprise value-to-sales (EV/sales) is a financial ratio that measures how much it would cost to 
        purchase a company's value in terms of its sales. 
        
        Formula: EV/EBITDA = Enterprise Value / Earnings Before Interest, Taxes, Depreciation, and Amortization
        """
        try:
            eve = self.data.get('key-statistics').get('valuation_measures').loc['Enterprise Value/EBITDA', 'Current']
        except:
            eve = None
        return eve
    
    
    def profit_margin(self):
        """
        Profit margin is a common measure of the degree to which a company or a particular business activity makes money. 
        Expressed as a percentage, it represents the portion of a company's sales revenue that it gets to keep as a profit, 
        after subtracting all of its costs.
        
        Formula: Profit Margin = Net Income / Revenue
        """
        try:
            profit_margin = self.data.get('key-statistics').get('financial_highlights').get('Profit Margin')
        except:
            profit_margin = None
        return profit_margin
    
    
    def operating_margin(self):
        """
        Operating margin is a measure of a company's profitability, and an indicator of how well it is being managed and 
        how risky it is. Operating margin is calculated by dividing operating income by revenue.
        
        Formula: Operating Margin = Operating Income / Revenue
        """
        try:
            operating_margin = self.data.get('key-statistics').get('financial_highlights').get('Operating Margin (ttm)')
        except:
            operating_margin = None
        return operating_margin
    
    
    def return_on_assets(self):
        """
        Return on assets (ROA) is an indicator of how profitable a company is relative to its total assets. ROA gives an idea 
        as to how efficient management is at using its assets to generate earnings.
        
        Formula: ROA = Net Income / Total Assets
        """
        try:
            roa = self.data.get('key-statistics').get('financial_highlights').get('Return on Assets (ttm)')
        except:
            roa = None
        return roa
    
    
    def return_on_equity(self):
        """
        Return on equity (ROE) is a measure of financial performance calculated by dividing net income by shareholders' equity.
        
        Formula: ROE = Net Income / Shareholders' Equity
        """
        try:
            roe = self.data.get('key-statistics').get('financial_highlights').get('Return on Equity (ttm)')
        except:
            roe = None
        return roe
    
    
    def revenue_by_mkt_cap(self):
        """
        Revenue by market capitalization is a metric that shows how much revenue a company generates for every dollar of 
        market capitalization. It is calculated by dividing the company's revenue by its market capitalization.
        """
        try:
            mkt_cap = self.data.get('key-statistics').get('valuation_measures').loc['Market Cap', 'Current']
            revenue = self.data.get('key-statistics').get('financial_highlights').get('Revenue (ttm)')
            revenue_by_mkt_cap = revenue / mkt_cap
        except:
            revenue_by_mkt_cap = None
        return revenue_by_mkt_cap
    
    
    def gross_profit(self):
        """
        Gross profit is the profit a company makes after deducting the costs associated with making and selling its products,
        or the costs associated with providing its services. Gross profit will appear on a company's income statement.
        """
        try:
            gross_profit = self.data.get('financials').loc['Gross Profit', 'TTM']
        except:
            gross_profit = None
        return gross_profit 
    
    
    def quarterly_revenue_growth_yoy(self):
        """
        The quarterly revenue growth year-over-year is the percentage change in revenue from the same quarter a year ago.
        """
        try:
            revenue_growth = self.data.get('key-statistics').get('financial_highlights').get('Quarterly Revenue Growth (yoy)')
        except:
            revenue_growth = None
        return revenue_growth
    
    
    def quarterly_earnings_growth_yoy(self):
        """
        The quarterly earnings growth year-over-year is the percentage change in earnings from the same quarter a year ago.
        """
        try:
            earnings_growth = self.data.get('key-statistics').get('financial_highlights').get('Quarterly Earnings Growth (yoy)')
        except:
            earnings_growth = None
        return earnings_growth
    
    
    def gross_profit_by_mkt_cap(self):
        """
        Gross profit by market capitalization is a metric that shows how much gross profit a company generates for every 
        dollar of market capitalization. It is calculated by dividing the company's gross profit by its market capitalization.
        """
        try:
            mkt_cap = self.data.get('key-statistics').get('valuation_measures').loc['Market Cap', 'Current']
            gross_profit = self.data.get('financials').loc['Gross Profit', 'TTM']
            gross_profit_by_mkt_cap = gross_profit / mkt_cap
        except:
            gross_profit_by_mkt_cap = None
        return gross_profit_by_mkt_cap
    
    
    def net_income(self):
        """
        Net income is the total amount of money a company has left over after all its expenses have been paid, 
        including cost of goods sold, operating expenses, interest, and taxes. 
        """
        try:
            net_income = self.data.get('financials').loc['Net Income', 'TTM']
        except:
            net_income = None
        return net_income
    
    
    def net_income_by_mkt_cap(self):
        """
        Net income by market capitalization is a metric that shows how much net income a company generates for every 
        dollar of market capitalization. It is calculated by dividing the company's net income by its market capitalization.
        """
        try:
            mkt_cap = self.data.get('key-statistics').get('valuation_measures').loc['Market Cap', 'Current']
            net_income = self.data.get('financials').loc['Net Income', 'TTM']
            net_income_by_mkt_cap = net_income / mkt_cap
        except: 
            net_income_by_mkt_cap = None
        return net_income_by_mkt_cap
    
    
    def debt_to_equity_ratio(self):
        """
        The debt-to-equity ratio is a financial ratio indicating the relative proportion of shareholders' equity 
        and debt used to finance a company's assets. 
        """
        try:
            total_debt_equity = self.data.get('key-statistics').get('financial_highlights').get('Total Debt/Equity (mrq)')
        except:
            total_debt_equity = None
        return total_debt_equity
        
    
    def asset_to_liability_ratio(self):
        """
        The asset-to-liability ratio is a metric that shows the proportion of a company's assets to its liabilities. 
        It is calculated by dividing the company's total assets by its total liabilities. 
        """
        # pick the first row as it contains the total assets
        try:
            total_assets = self.data.get('balance-sheet').loc['Total Assets'].iloc[0]
            total_liabilities = self.data.get('balance-sheet').loc['Total Non Current Liabilities Net Minority Interest'].iloc[0]
            asset_to_liability_ratio = total_assets / total_liabilities
        except:
            asset_to_liability_ratio = None
        return asset_to_liability_ratio
    
    
    def operating_cash_flow(self):
        """
        Operating cash flow (OCF) is a measure of the amount of cash generated by a company's normal business operations.
        """
        try:
            ocf = self.data.get('cash-flow').loc['Operating Cash Flow'].iloc[0]
        except:
            ocf = None
        return ocf
    
    
    def operating_cash_flow_by_mkt_cap(self):
        """
        Operating cash flow by market capitalization is a metric that shows how much operating cash flow a company generates 
        for every dollar of market capitalization. It is calculated by dividing the company's operating cash flow by its 
        market capitalization.
        """
        try:
            mkt_cap = self.data.get('key-statistics').get('valuation_measures').loc['Market Cap', 'Current']
            ocf = self.data.get('cash-flow').loc['Operating Cash Flow'].iloc[0]
            ocf_by_mkt_cap = ocf / mkt_cap
        except:
            ocf_by_mkt_cap = None
        return ocf_by_mkt_cap
    
    
    def levered_free_cash_flow(self):
        """
        Levered free cash flow (LFCF) is the cash flow that is left over after a company has paid its obligations.
        """
        try:
            lfcf = self.data.get('cash-flow').loc['Free Cash Flow'].iloc[0]
        except: 
            lfcf = None
        return lfcf
    
    
    def levered_free_cash_flow_by_mkt_cap(self):
        """
        Levered free cash flow by market capitalization is a metric that shows how much levered free cash flow a company 
        generates for every dollar of market capitalization. It is calculated by dividing the company's levered free cash 
        flow by its market capitalization.
        """
        try:
            mkt_cap = self.data.get('key-statistics').get('valuation_measures').loc['Market Cap', 'Current']
            lfcf = self.data.get('cash-flow').loc['Free Cash Flow'].iloc[0]
            lfcf_by_mkt_cap = lfcf / mkt_cap
        except:
            lfcf_by_mkt_cap = None
        return lfcf_by_mkt_cap

        
    def main(self):
        """
        Calculates all metrics for the stocks.
        """
        trailing_pe_ratio, forward_pe_ratio = self.pe_ratio()
        
        metrics = {
            # VALUATION METRICS
            'trailing_pe_ratio': trailing_pe_ratio,
            'forward_pe_ratio': forward_pe_ratio,
            'peg_ratio': self.peg_ratio(),
            'pb_ratio': self.pb_ratio(),
            'ps_ratio': self.ps_ratio(),
            'enterprise_value_revenue': self.enterprise_value_revenue(),
            'enterprise_value_ebitda': self.enterprise_value_ebitda(),
            
            # PROFITABILITY METRICS
            'profit_margin': self.profit_margin(),
            'operating_margin': self.operating_margin(),
            
            # MANAGEMENT EFFICIENCY METRICS
            'return_on_assets': self.return_on_assets(), 
            'return_on_equity': self.return_on_equity(),
            
            # INCOME STATEMENT METRICS
            'revenue_by_mkt_cap': self.revenue_by_mkt_cap(),
            'quarterly_revenue_growth_yoy': self.quarterly_revenue_growth_yoy(),
            'quarterly_earnings_growth_yoy': self.quarterly_earnings_growth_yoy(),
            'gross_profit': self.gross_profit(),
            'gross_profit_by_mkt_cap': self.gross_profit_by_mkt_cap(),
            'net_income': self.net_income(),
            'net_income_by_mkt_cap': self.net_income_by_mkt_cap(),
            
            # BALANCE SHEET METRICS
            'debt_to_equity_ratio': self.debt_to_equity_ratio(),
            'asset_to_liability_ratio': self.asset_to_liability_ratio(),
            
            # CASH FLOW METRICS
            'operating_cash_flow': self.operating_cash_flow(),
            'operating_cash_flow_by_mkt_cap': self.operating_cash_flow_by_mkt_cap(),
            'levered_free_cash_flow': self.levered_free_cash_flow(),
            'levered_free_cash_flow_by_mkt_cap': self.levered_free_cash_flow_by_mkt_cap()
            
        }
        # print(json.dumps(metrics, indent=4))
        return metrics