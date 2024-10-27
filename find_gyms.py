from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def parse_page(link):
    options = Options()
    # options.headless = True  # Uncomment if you want to run in headless mode

    service = Service('/Users/camillephares/Downloads/chromedriver-mac-x64/chromedriver')
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(link)
        
        # Wait for the page to fully load (adjust time if needed)
        time.sleep(5)
        
        # Get the page source after the JavaScript has rendered the content
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find all state headlines and corresponding locations-area divs
        state_headlines = soup.find_all('div', class_='headline')
        locations_areas = soup.find_all('div', class_='locations-area')
        
        states_and_cities = {}

        # Iterate over states and locations
        for state, locations_area in zip(state_headlines, locations_areas):
            # Extract state name and clean it
            state_name = state.get_text(strip=True).strip().split(' ')[0]

            # Find all city spans in the current locations area
            cities = locations_area.find_all('span')
            city_names = [
                city.get_text(strip=True).replace('|', '').strip()
                for city in cities if city.get_text(strip=True).replace('|', '').strip()
            ]

            # Add to dictionary, using state as key and city names as values
            states_and_cities[state_name] = city_names

        print(states_and_cities)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

parse_page("https://www.24hourfitness.com/gyms/")
