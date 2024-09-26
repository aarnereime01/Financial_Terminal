from .scrapers.historical import Historical

class Index:
    
    def __init__(self, index: str, range: str) -> None:
        self.index = self.validate_index(index.upper())
        self.range = range
        
        self._historical = Historical(self.index, self.range)
        
    def __repr__(self) -> str:
        return f'Index: {self.index}'
    
    def validate_index(self, index: str) -> bool:
        if index in ['^IXIC', '^DJI', '^GSPC']:
            return index
    
    @property
    def historical(self):
        return self._historical.get_historical()
        
    