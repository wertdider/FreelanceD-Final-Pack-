from scraper import FreelancerScraper
from positions_dict import positions

def scrape_all_positions():
    for position in positions:
        print(f"🚀 Scraping {position}")
        scraper = FreelancerScraper(position)
        scraper.scrape_freelancers()
        scraper.close()

if __name__ == "__main__":
    scrape_all_positions()
