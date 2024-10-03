# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# import time
# import random
# from multiprocessing import Pool


# class Scraper:
#     BASE_SLEEP_TIME = 1  # Min sleep time between requests
#     MAX_SLEEP_TIME = 2  # Max sleep time between requests

#     def __init__(self, base_url: str):
#         self.base_url = base_url
#         self.driver = webdriver.Chrome(options=self.setup_driver())

#     def setup_driver(self) -> webdriver.ChromeOptions:
#         options = webdriver.ChromeOptions()
#         options.add_argument('--disable-search-engine-choice-screen')
#         # options.add_argument('--headless')  # Hide chrome will scraping
#         prefs = {"profile.managed_default_content_settings.images": 2,
#          "profile.default_content_settings.cookies": 2}
#         options.add_experimental_option("prefs", prefs)
#         options.add_argument("--disable-gpu")
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-extensions")

#         return options

#     def random_sleep(self, min_sleep: int = BASE_SLEEP_TIME, max_sleep: int = MAX_SLEEP_TIME) -> None:
#         time.sleep(random.uniform(min_sleep, max_sleep))

#     def close(self) -> None:
#         self.driver.quit()


# class YahooFinanceScraper(Scraper):
#     PAGES = [
#             'key-statistics',
#             'financials',
#             'balance-sheet',
#             'cash-flow'
#         ]

#     def __init__(self, ticker: str):
#         self.ticker = ticker.upper()
#         super().__init__(f'https://finance.yahoo.com/quote/{self.ticker}/')
#         self.passed_privacy_popup = False

#     def bypass_privacy_popup(self) -> None:
#         """
#         Each time we initialize a new driver and scrape the YahooFinance webpage we're prompted with a
#         privacy pop-up, this code snippet bypasses the pop-up by denying the privacy setting.
#         """
#         try:
#             privacy_button = WebDriverWait(self.driver, 30).until(
#                 EC.element_to_be_clickable(
#                     (By.NAME, 'reject'))
#             )
#             privacy_button.click()
#             self.passed_privacy_popup = True
#         except Exception as e:
#             print(f"Error handling the privacy pop-up: {e}")

#     def expand_all(self) -> None:
#         """
#         Clicks on a button called "Expand All" that expands all values in the financial table, to ensure that
#         we retrieve every financial detail about the selected stock.
#         """
#         try:
#             expand_button = WebDriverWait(self.driver, 10).until(
#                 EC.element_to_be_clickable(
#                     (By.CLASS_NAME, 'expand'))
#             )
#             expand_button.click()
            
#             # Wait for the table to expand
#             WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located(
#                     (By.CLASS_NAME, 'row_lv-1_yf-1xjz32c'))
#             )
#         except Exception as e:
#             print(f"Error expanding buttons: {e}")
            
#     def worker(self, page):
#         driver = webdriver.Chrome(options=self.setup_driver())
#         try:
#             self.bypass_privacy_popup(driver)
#             return self.fetch_page_content(page, driver)
#         finally:
#             driver.quit()

#     def fetch_page_content(self, page) -> str:
#         """
#         Modifies the url to be scraped, then checks if we need to bypass a pop-up,
#         followed by clicking the expand all button, lastly we retrieve the page source code.
#         """
#         url = self.base_url + page + '/'
#         self.driver.get(url)

#         if not self.passed_privacy_popup:
#             self.bypass_privacy_popup()
            
#         max_attempts = 5
#         attempts = 0

#         if page in ['financials', 'balance-sheet', 'cash-flow']:
#             # Try spamming the expand button since it sometimes doesn't work on the first try
#             while attempts < max_attempts:
#                 try:
#                     self.expand_all()
#                     break
#                 except:
#                     attempts += 1

#         html = self.driver.page_source
#         return html

#     def parse_pages(self) -> dict:
#         """
#         Parses the content of all required pages and returns a dictionary.
#         """
#         start_time = time.time()
#         data = {}
#         # urls = [self.base_url + page + '/' for page in self.PAGES]
#         # print(urls)
#         # with Pool(4) as p:
#         #     data = p.map(self.fetch_page_content, urls)
#         #     print(data)
#         for page in self.PAGES:
#             print(f"Fetching {page} data...")
#             try:
#                 html = self.fetch_page_content(page)
#                 data[page] = html
#                 self.random_sleep()
#             except Exception as e:
#                 print(f"Failed to fetch content for {page}: {e}")

#         self.close()
#         print(f"Time elapsed: {time.time() - start_time}")
#         return data


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
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_settings.cookies": 2
        }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")

        return options

    def close(self) -> None:
        self.driver.quit()


class YahooFinanceScraper():
    PAGES = [
            'key-statistics',
            'financials',
            'balance-sheet',
            'cash-flow'
        ]


    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.scrape_url = f'https://finance.yahoo.com/quote/{self.ticker}/'
        self.passed_privacy_popup = False


    def bypass_privacy_popup(self, driver) -> None:
        """
        Each time we initialize a new driver and scrape the YahooFinance webpage we're prompted with a
        privacy pop-up, this code snippet bypasses the pop-up by denying the privacy setting.
        """
        try:
            privacy_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(
                    (By.NAME, 'reject'))
            )
            privacy_button.click()
            self.passed_privacy_popup = True
        except Exception as e:
            print(f"Error handling the privacy pop-up: {e}")


    def expand_all(self, driver) -> None:
        """
        Clicks on a button called "Expand All" that expands all values in the financial table, to ensure that
        we retrieve every financial detail about the selected stock.
        """
        try:
            expand_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'expand'))
            )
            expand_button.click()
            
            # # Wait for the table to expand
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located(
            #         (By.CLASS_NAME, 'row_lv-1_yf-1xjz32c'))
            # )
        except Exception as e:
            print(f"Error expanding buttons: {e}")
            
            
    def worker(self, page):
        driver = Driver().driver
        
        try:
            return self.fetch_page_content(page, driver)
        finally:
            driver.close()

    def fetch_page_content(self, page, driver) -> str:
        """
        Modifies the url to be scraped, then checks if we need to bypass a pop-up,
        followed by clicking the expand all button, lastly we retrieve the page source code.
        """
        driver.get(page)
        self.bypass_privacy_popup(driver)

        if page in [f'https://finance.yahoo.com/quote/{self.ticker}/financials/',
                    f'https://finance.yahoo.com/quote/{self.ticker}/balance-sheet/',
                    f'https://finance.yahoo.com/quote/{self.ticker}/cash-flow/']:
            # Try spamming the expand button since it sometimes doesn't work on the first try
            self.expand_all(driver)

        html = driver.page_source
        return html

    def parse_pages(self) -> dict:
        """
        Parses the content of all required pages and returns a dictionary.
        """
        start_time = time.time()
        
        pages_to_scrape = [self.scrape_url + page + '/' for page in self.PAGES]
        
        with Pool(len(pages_to_scrape)) as p:
            data = p.map(self.worker, pages_to_scrape)
            
        print(f"Time elapsed: {time.time() - start_time}")
        return dict(zip(self.PAGES, data))
