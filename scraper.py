import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from positions_dict import positions  # Import dictionary of job positions

class FreelancerScraper:
    def __init__(self, search_term):
        self.search_term = search_term
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def open_page(self, url):
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="results"]'))
            )
            print(f"✅ Page loaded: {url}")
            return True
        except Exception:
            print(f"❌ Page load failed or no more results: {url}")
            return False

    def scrape_freelancers(self):
        freelancers_data = []
        page = 1
        count = 0  # Track how many profiles we scraped

        while count < 20:
            print(f"🔍 Scraping {self.search_term} - Page {page}...")
            url = f"https://hubstafftalent.net/search/profiles?search%5Bkeywords%5D={self.search_term}&page={page}"
            if not self.open_page(url):
                break
            
            freelancers = self.driver.find_elements(By.XPATH, '//*[@id="results"]/div[2]/div[3]/div[2]')
            print(f"📌 Found {len(freelancers)} freelancers on page {page}.")

            for freelancer in freelancers:
                if count >= 20:  # Stop after scraping 20 profiles
                    break

                name = self.get_text(freelancer, './/a', 'N/A')
                position = self.get_text(freelancer, './/div[3]', 'N/A')
                country = self.get_text(freelancer, './/span', 'N/A')
                skills = self.get_text(freelancer, './/div[5]', 'N/A')
                rate = self.get_text(freelancer, './/div[2]/div[2]', 'N/A')

                print(f"📝 [{count+1}] {name} | {position} | {country} | {skills} | {rate}")
                freelancers_data.append([name, position, country, skills, rate, self.search_term])

                count += 1  # Increase count after scraping a freelancer
            
            page += 1
            time.sleep(2)  # Prevent bans
        
        print("✅ Scraping complete.")
        return freelancers_data

    def get_text(self, element, xpath, default_value):
        try:
            text = element.find_element(By.XPATH, xpath).text.strip()
            return text if text else default_value
        except Exception:
            return default_value

    def close(self):
        print("🛑 Closing browser.")
        self.driver.quit()
