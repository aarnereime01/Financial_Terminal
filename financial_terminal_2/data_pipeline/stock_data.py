import os
import requests
import zipfile
import pandas as pd
import bs4 as bs


class SecGovData:
    
    def __init__(self, company_foldername: str):    
        self.zip_url = 'https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip'
        self.zip_filename = 'companyfacts.zip'
        self.company_foldername = company_foldername
        
        self.cwd = os.getcwd()
        self.zip_path = os.path.join(self.cwd, self.zip_filename)
        self.company_foldername_path = os.path.join(self.cwd, self.company_foldername)
        
        self.headers = {
            'User-Agent': 'aarnereime01@gmail.com',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov'
        }
        
        self.download_and_extract_zip()
                
        
    def check_if_zip_exists(self):
        """Checks if the folder file exists"""
        if os.path.exists(self.company_foldername_path):
            return True
        
        
    def download_and_extract_zip(self):
        """Downloads the zip file and extracts it"""
        if self.check_if_zip_exists():
            print(f"Folder file already exists: {self.company_foldername_path}")
            return
        
        # Download the file with streaming enabled
        print(f"Downloading {self.zip_url}...")
        with requests.get(self.zip_url, stream=True, headers=self.headers) as response:
            response.raise_for_status()  # Check for any HTTP errors
            with open(self.zip_path, 'wb') as zip_file:
                for chunk in response.iter_content(chunk_size=1000):
                    zip_file.write(chunk)
        print(f"Download complete: {self.zip_path}")

        # Check if the file was successfully downloaded
        if os.path.exists(self.zip_path):
            # Extract the contents of the zip file
            print(f"Extracting {self.zip_path}...")
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.company_foldername_path)
            print(f"Extraction complete. Files extracted to: {self.company_foldername_path}")

            # Optionally, remove the zip file after extraction
            os.remove(self.zip_path)
            print(f"Removed the zip file: {self.zip_path}")
        else:
            print("Download failed: The file does not exist.")
                        
            
class SP500:
    
    def __init__(self, company_foldername: str):
        self.company_foldername = company_foldername
        self.tickers = self.get_sp500_tickers()
        
        # Retrieve the data from the SEC website, then delete the files that are not in the S&P 500
        SecGovData(company_foldername)
        self.delete_cik_files(self.tickers)
    
    
    def get_sp500_tickers(self) -> dict:
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
                'sector': row.find_all('td')[2].get_text(strip=True),
                'sub_industry': row.find_all('td')[3].get_text(strip=True),
                'cik': row.find_all('td')[6].get_text(strip=True),
            }
        
        return ticker_data
    
    
    def delete_cik_files(self, tickers: dict) -> None:
        cik = set()

        for ticker in tickers:
            cik_number = tickers[ticker]['cik']
            cik.add(cik_number)
    
        for filename in os.listdir(self.company_foldername):
            if filename.endswith(".json"):
                cik_number = filename.split('.')[0][3:]
                if cik_number not in cik:
                    os.remove(f'{self.company_foldername}/{filename}')
                    
        print(f'Number of stocks in CompanyFacts: {len(os.listdir(self.company_foldername))}')