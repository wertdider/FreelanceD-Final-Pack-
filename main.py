from scraper import FreelancerScraper, save_to_csv
from positions_dict import positions

def scrape_all_positions():
    all_freelancers = []  # Shared list to store all data
    for position in positions:
        print(f"Starting to scrape: {position}")
        scraper = FreelancerScraper(position, all_freelancers)  # Pass shared list
        scraper.scrape_freelancers()
        scraper.close()

    # Save all data to one CSV file after all scraping is done
    save_to_csv(all_freelancers)

if __name__ == "__main__":
    scrape_all_positions()
