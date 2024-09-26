from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import random # For randomizing the sleep time between requests


class Scraper:

    def __init__(self, url: str):
        self.url = url
        self.driver = webdriver.Chrome(options=self.setup_driver())
        
        self.pages = {
            'statistics': 'key-statistics',
            'financials': 'financials',
            'balance_sheet': 'balance-sheet',
            'cash-flow': 'cash-flow',
            # 'analysis': 'analysis',
        }
        
        self.passed_privay_popup: bool = False

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-search-engine-choice-screen')
        options.add_argument('--headless')

        return options

    def bypass_privacy_popup(self, driver):
        try:
            # Modify the XPATH or class name as needed based on the button's HTML
            privacy_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Avvis alle')]"))
            )
            privacy_button.click()
            self.passed_privay_popup = True
        except Exception as e:
            print(f"Error handling the privacy pop-up: {e}")

    def expand_button(self, driver):
        try:
            # Modify the XPATH or class name as needed based on the button's HTML
            expand_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(text(), 'Expand All')]"))
            )
            expand_button.click()
        except Exception as e:
            print(f"Error expanding buttons: {e}")

    def fetch_page_content(self, param):
        try:
            self.driver.get(self.url + param + '/')
            if not self.passed_privay_popup:
                self.bypass_privacy_popup(self.driver)

            # Click expand all button to get all data for financials, balance_sheet and income_statement
            if param in ['financials', 'balance-sheet', 'cash-flow']:
                self.expand_button(self.driver)

            html = self.driver.page_source
            return html
        except Exception as e:
            print(f"Error fetching page content: {e}")
            return None

    def parse(self):
        data = {}
        
        for page in self.pages:
            print(f"Fetching {page} data...")
            page_content = self.fetch_page_content(self.pages[page])
            data[page] = bs(page_content, 'html.parser')
            time.sleep(random.randint(1, 5))
            
        self.driver.quit()
        return data
