from selenium import webdriver
import scrape_match_data as sd
import scrape_match_urls as sc
import json
import time
import database

def main():
    supabase = database.get_client()

    print('Initializing WebDriver...')

    # Initialize the local Chrome WebDriver
    driver = webdriver.Chrome()  # This automatically starts ChromeDriver

    try:
        print('Retrieving match URLs...')
        
        # Get the list of match URLs
        urls = sc.get_match_urls(driver)

        # Iterate over each URL and scrape data with a delay
        for base_url in urls:
            print(f'Navigating to {base_url}...')
            driver.get(base_url)
            
            # Scrape the match data for the current URL
            match_data = sd.scrape_match_data(driver, base_url)

            database.insert_for_match(match_data, supabase)
            
            # Wait for 10 seconds before the next request
            time.sleep(10)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Ensure the WebDriver is closed properly
        driver.quit()
        print('WebDriver session closed.')

if __name__ == "__main__":
    main()
