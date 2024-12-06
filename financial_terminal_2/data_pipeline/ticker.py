from ..utils.label_mapper import LabelMapper

import json


class TickerData:
    
    def __init__(self, ticker: str, industry: str, sector: str, cik: str, company_foldername: str):
        self.ticker = ticker
        self.industry = industry
        self.sector = sector
        self.cik = cik
        self.data = self.unpack_data(company_foldername)
        
        
    def __str__(self):
        return f"Ticker: {self.ticker}, Industry: {self.industry}, Sector: {self.sector}, CIK: {self.cik}"
    
    
    def unpack_data(self, company_foldername: str) -> dict:
        """Read the data from the json file."""
        with open(f"{company_foldername}/cik{self.cik}.json", "r") as f:
            data = json.load(f)
            return data
    
    
    def make_label_mapper(self) -> dict:
        """
        Creates a label mapper from the metric labels to the standard labels.
        This is necessary since the metric labels differ from company to company.
        """
        
        lm = LabelMapper(self.data)
        label_mapper = lm.label_mapper
            
        return label_mapper
    
    
    def main(self):
        label_mapper = self.make_label_mapper()
        print(json.dumps(label_mapper, indent=4))