import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from positions_dict import positions  # Import dictionary of job positions

class FreelancerScraper:
    def __init__(self, search_term, all_freelancers):
        self.search_term = search_term
        self.all_freelancers = all_freelancers  # Store all data in a shared list
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
                EC.presence_of_all_elements_located((By.XPATH, '/html/body/content/div/div[3]/section/main/div/div[3]/div/div[2]/ul/li'))
            )
            print(f"Page loaded successfully: {url}")
            return True
        except TimeoutException:
            print(f"Page load timed out or no more results: {url}")
            return False

    def scrape_freelancers(self):
        page = 1
        while page <= 39:
            print(f"Scraping {self.search_term} - Page {page}...")
            url = f"{positions[self.search_term]}?page={page}"
            if not self.open_page(url):
                break
            
            freelancers = self.driver.find_elements(By.XPATH, '/html/body/content/div/div[3]/section/main/div/div[3]/div/div[2]/ul/li')
            if not freelancers:
                print("No more freelancers found. Ending scraping.")
                break

            print(f"Found {len(freelancers)} freelancers on page {page}.")
            
            for freelancer in freelancers:
                name = self.get_text(freelancer, './div/div[1]/a', 'N/A')
                skills = self.get_text(freelancer, './div/div[1]/p', 'N/A')
                country = self.get_text(freelancer, './div/div[1]/div[2]', 'N/A')
                salary = self.get_text(freelancer, './div/div[2]/div[2]/div[2]', 'N/A')
                rating = self.get_text(freelancer, '//*[@id="startRow"]/div/div[2]/ul/li[7]/div/div[2]/div[1]/a', 'N/A')
                
                # Print each freelancer's data
                print(f"Scraping Freelancer - Name: {name}, Skills: {skills}, Country: {country}, Salary: {salary}, Rating: {rating}")
                
                # Add job category to the data
                self.all_freelancers.append([name, skills, country, salary, rating, self.search_term])
            
            page += 1
            time.sleep(2)  # Avoid IP bans
        
        return self.all_freelancers

    def get_text(self, element, xpath, default_value):
        try:
            text = element.find_element(By.XPATH, xpath).text
            return text.strip() if text.strip() else default_value
        except Exception:
            return default_value

    def close(self):
        print("Closing the browser.")
        self.driver.quit()


def scrape_all_positions():
    all_freelancers = []  # Shared list to store all data
    for position in positions:
        print(f"Starting to scrape: {position}")
        scraper = FreelancerScraper(position, all_freelancers)
        scraper.scrape_freelancers()
        scraper.close()

    # Save all data to one CSV file
    save_to_csv(all_freelancers)


def save_to_csv(freelancers_data):
    filename = 'all_freelancers_data.csv'
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Skills', 'Country', 'Hourly Rate', 'Rating', 'Category'])  # CSV header
        writer.writerows(freelancers_data)  # Writing the freelancer data rows
        print(f"All data saved to {filename}")


if __name__ == "__main__":
    scrape_all_positions()
