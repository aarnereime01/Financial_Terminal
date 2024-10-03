from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import random
from multiprocessing import Pool

class Driver:
    
    def __init__(self):
        self.driver = webdriver.Chrome(options=self.setup_driver())


    def setup_driver(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-search-engine-choice-screen')
        options.add_argument('--headless')  # Hide chrome will scraping
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_settings.cookies": 2
        }
        options.add_experimental_option("prefs", prefs)

        return options


    def close(self) -> None:
        self.driver.quit()


class YahooFinanceScraper():
    BASE_SLEEP_TIME = 1  # Min sleep time between requests
    MAX_SLEEP_TIME = 2  # Max sleep time between requests

    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.scrape_url = f'https://finance.yahoo.com/quote/{self.ticker}/'
        
        
    def random_sleep(self, min_sleep: int = BASE_SLEEP_TIME, max_sleep: int = MAX_SLEEP_TIME) -> None:
        """
        Sleeps for a random amount of time between min_sleep and max_sleep to not get blocked by the website.
        Later we will implement a more sophisticated way to avoid getting blocked.
        """
        time.sleep(random.uniform(min_sleep, max_sleep))


    def bypass_privacy_popup(self, driver) -> None:
        """
        Each time we initialize a new driver and scrape the YahooFinance webpage we're prompted with a
        privacy pop-up, this code snippet bypasses the pop-up by denying the privacy setting.
        """
        try:
            privacy_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.NAME, 'reject')))
            privacy_button.click()
        except Exception as e:
            print(f"Error handling the privacy pop-up: {e}")


    def expand_all(self, driver) -> None:
        """
        Clicks on a button called "Expand All" that expands all values in the financial table, to ensure that
        we retrieve every financial detail about the selected stock. Then we wait for the table to expand to
        make sure we get all the data.
        """
        try:
            expand_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'expand')))
            expand_button.click()
            
            # Wait for the table to expand
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.lv-1.yf-1xjz32c")))
        except Exception as e:
            print(f"Error expanding buttons: {e}")
            
            
    def worker(self, page):
        """
        Worker function that initializes a driver and calls on a function to fetch the content of a page.
        """
        driver = Driver().driver
        
        try:
            return self.fetch_page_content(page, driver)
        finally:
            driver.close()
            self.random_sleep()


    def fetch_page_content(self, page, driver) -> str:
        """
        Main function that fetches the content of a page.
        """
        driver.get(page)
        self.bypass_privacy_popup(driver)

        if page in [f'https://finance.yahoo.com/quote/{self.ticker}/financials/',
                    f'https://finance.yahoo.com/quote/{self.ticker}/balance-sheet/',
                    f'https://finance.yahoo.com/quote/{self.ticker}/cash-flow/']:
            self.expand_all(driver)

        html = driver.page_source
        return html


    def parse_pages(self) -> dict:
        """
        Makes a list of pages to scrape and then scrapes them in parallel by using the multiprocessing library.
        In this multiprocessing method we initialize the length of the pool to the number of pages we want to scrape.
        """
        page_paths = [
            'key-statistics',
            'financials',
            'balance-sheet',
            'cash-flow'
        ]
        
        start_time = time.time()
        
        pages_to_scrape = [self.scrape_url + page + '/' for page in page_paths]
        # Scrape the pages in parallel
        with Pool(len(pages_to_scrape)) as p:
            data = p.map(self.worker, pages_to_scrape)
            
        print(f"Time elapsed: {time.time() - start_time}")
        return dict(zip(page_paths, data))
