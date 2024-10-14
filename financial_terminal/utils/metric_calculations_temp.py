class Calculations:
    
    def __init__(self, data):
        self.data = data
        
        
    def pe_ration(self):
        try:
            return self.data.get('ratios').loc['Price to Earnings Ratio'].iloc[0]
        except:
            return None
    
    def ps_ratio(self):
        try:
            return self.data.get('ratios').loc['Price to Sales Ratio'].iloc[0]
        except:
            return None
        
    def pb_ratio(self):
        try:
            return self.data.get('ratios').loc['Price to Book Ratio'].iloc[0]
        except:
            return None
        
    def pfcf_ratio(self):
        try:
            return self.data.get('ratios').loc['Price to Free Cash Flow Ratio'].iloc[0]
        except:
            return None
        
    
    def pocf_ratio(self):
        try:
            return self.data.get('ratios').loc['Price to Operating Cash Flow Ratio'].iloc[0]
        except:
            return None
        
        
    def price_to_earnings_growth_ratio(self):
        try:
            return self.data.get('ratios').loc['Price Earnings to Growth Ratio'].iloc[0]
        except:
            return None
        
        
    def ev_to_ebitda(self):
        try:
            return self.data.get('ratios').loc['EV to EBITDA'].iloc[0]
        except:
            return None
        
    
    def main(self):
        metrics = {
            'ticker': self.data.get('ticker'),
            'industry': self.data.get('profile').get('Industry'),
            'sector': self.data.get('profile').get('Sector'),
            'employees': int(self.data.get('profile').get('Number of Employees')),
            'pe_ratio': self.pe_ration(),
            'ps_ratio': self.ps_ratio(),
            'pb_ratio': self.pb_ratio(),
            'pfcf_ratio': self.pfcf_ratio(),
            'pocf_ratio': self.pocf_ratio(),
            'pegr_ratio': self.price_to_earnings_growth_ratio(),
            'ev_to_ebitda': self.ev_to_ebitda(),
        }
        
        return metrics