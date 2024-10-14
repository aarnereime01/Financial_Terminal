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
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_settings.cookies": 2
        }
        options.add_experimental_option("prefs", prefs)
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"
        ]
        
        user_agent = random.choice(user_agents)
        options.add_argument(f'user-agent={user_agent}')

        return options


class Scraper:
    BASE_SLEEP_TIME = 4  # Min sleep time between requests
    MAX_SLEEP_TIME = 7  # Max sleep time between requests
    
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.base_url = 'https://discountingcashflows.com/company/'
        
        self.page_paths = [
            'profile',
            'income-statement',
            'balance-sheet-statement',
            'cash-flow-statement',
            'ratios',
            # 'earnings'
        ]
        
    
    def random_sleep(self, min_sleep: int = BASE_SLEEP_TIME, max_sleep: int = MAX_SLEEP_TIME) -> None:
        """
        Sleeps for a random amount of time between min_sleep and max_sleep to not get blocked by the website.
        Later we will implement a more sophisticated way to avoid getting blocked.
        """
        time.sleep(random.uniform(min_sleep, max_sleep))
        
        
    def get_original_values(self, driver) -> None:
        """
        Changes the span tag to show the original values of the financial data.
        """
        try:
            dropdown = driver.find_element(By.XPATH, '//details[@x-ref="valueFormatDropdown"]')
            dropdown.click()

            # Then locate and click the "Original" option
            original_element = driver.find_element(By.XPATH, '//a[contains(text(), "Original")]')
            original_element.click()
            self.random_sleep()
        except Exception as e:
            print(f"Error handling the original values button: {e}")
            
    
    def worker(self, page):
        """
        Worker function that initializes a driver and calls on a function to fetch the content of a page.
        """
        driver = Driver().driver
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        try:
            return self.fetch_page_content(page, driver)
        finally:
            driver.quit()
            print(f'Quit driver for {page}')
            
    
    def fetch_page_content(self, page, driver) -> str:
        """
        Main function that fetches the content of a page.
        """
        url = self.base_url + self.ticker + '/' + page + '/'
        driver.get(url)
        self.random_sleep()
        
        waiting_map = {
            'income-statement': 'ltm-revenue.formatted-value',
            'cash-flow-statement': 'ltm-netIncome.formatted-value',
            'ratios': 'ltm-priceEarningsRatio.formatted-value'
        }
        
        if page in ['income-statement', 'cash-flow-statement', 'ratios']:
            # Check if the header in the table contains 'LTM', if not we dont need to wait for the element
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'td.{waiting_map[page]}')))
                except:
                    print(f"Error waiting for the table to load, refreshing page for {page}")
                    driver.refresh()
                    driver.refresh()
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'td.{waiting_map[page]}')))
                

        if page in ['income-statement', 'balance-sheet-statement', 'cash-flow-statement']:
            self.get_original_values(driver)

        html = driver.page_source
        return html
    
    
    def parse_pages(self) -> dict:
        """
        Scrapes the website for 
        """
        start_time = time.time()
        
        # Scrape the pages in parallel
        with Pool(len(self.page_paths)) as p:
            data = p.map(self.worker, self.page_paths)
            
        print(f"Time elapsed: {time.time() - start_time}")
        return dict(zip(self.page_paths, data))