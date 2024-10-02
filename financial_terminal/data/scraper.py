from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import random


class Scraper:
    BASE_SLEEP_TIME = 1  # Min sleep time between requests
    MAX_SLEEP_TIME = 3  # Max sleep time between requests

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.driver = webdriver.Chrome(options=self.setup_driver())

    def setup_driver(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-search-engine-choice-screen')
        options.add_argument('--headless')  # Hide chrome will scraping
        return options

    def random_sleep(self, min_sleep: int = BASE_SLEEP_TIME, max_sleep: int = MAX_SLEEP_TIME) -> None:
        time.sleep(random.uniform(min_sleep, max_sleep))

    def close(self) -> None:
        self.driver.quit()


class YahooFinanceScraper(Scraper):
    PAGES = ['key-statistics',
            #  'financials',
            #  'balance-sheet',
            #  'cash-flow'
             ]

    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        super().__init__(f'https://finance.yahoo.com/quote/{self.ticker}/')
        self.passed_privacy_popup = False

    def bypass_privacy_popup(self) -> None:
        """
        Each time we initialize a new driver and scrape the YahooFinance webpage we're prompted with a
        privacy pop-up, this code snippet bypasses the pop-up by denying the privacy setting.
        """
        try:
            privacy_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Avvis alle')]"))
            )
            privacy_button.click()
            self.passed_privacy_popup = True
        except Exception as e:
            print(f"Error handling the privacy pop-up: {e}")

    def expand_all(self) -> None:
        """
        Clicks on a button called "Expand All" that expands all values in the financial table, to ensure that
        we retrieve every financial detail about the selected stock.
        """
        try:
            expand_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(text(), 'Expand All')]"))
            )
            expand_button.click()
        except Exception as e:
            print(f"Error expanding buttons: {e}")

    def fetch_page_content(self, page) -> str:
        """
        Modifies the url to be scraped, then checks if we need to bypass a pop-up,
        followed by clicking the expand all button, lastly we retrieve the page source code.
        """
        url = self.base_url + page + '/'
        self.driver.get(url)

        if not self.passed_privacy_popup:
            self.bypass_privacy_popup()

        if page in ['financials', 'balance-sheet', 'cash-flow']:
            self.expand_all()

        html = self.driver.page_source
        return html

    def parse_pages(self) -> dict:
        """
        Parses the content of all required pages and returns a dictionary.
        """
        data = {}
        for page in self.PAGES:
            print(f"Fetching {page} data...")
            try:
                html = self.fetch_page_content(page)
                data[page] = html
                self.random_sleep()
            except Exception as e:
                print(f"Failed to fetch content for {page}: {e}")

        self.close()
        return data
