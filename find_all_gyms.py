from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def parse_page(link):
    # Takes a link to the 24 Hour Fitness website and returns a dict of all U.S. locations
    # with states as keys and lists of cities as values

    options = Options()
    service = Service(
        "/Users/camillephares/Downloads/chromedriver-mac-x64/chromedriver"
    )

    try:
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(link)

        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        state_headlines = soup.find_all("div", class_="headline")

        states_and_cities = {}

        # Iterate over each state and put its cities in the dictionary
        for state in state_headlines:

            state_name = (
                " ".join(state.get_text(strip=True).split(" ")[:2])
                if any(
                    keyword in state.get_text() for keyword in ["New", "South", "West"]
                )
                else state.get_text(strip=True).split(" ")[0]
            )

            locations_area = state.find_next("div", class_="locations-area")
            cities = locations_area.find_all("span") if locations_area else []
            city_names = [
                city.get_text(strip=True).replace("|", "").strip()
                for city in cities
                if city.get_text(strip=True).replace("|", "").strip()
            ]
            states_and_cities[state_name] = city_names

        print(states_and_cities)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


parse_page("https://www.24hourfitness.com/gyms/")

"""
results 11/01/2024:


gyms = {
    "California": [
        "Los Angeles",
        "Monterey",
        "Sacramento",
        "San Diego",
        "San Francisco",
        "Santa Barbara",
    ],
    "Colorado": ["Colorado Springs", "Denver"],
    "Florida": [
        "Apopka",
        "Homestead",
        "Lake Mary",
        "Miami",
        "Miami Gardens",
        "Orlando",
        "Plantation",
        "Winter Park",
    ],
    "Hawaii": ["Honolulu", "Kaneohe", "Kapolei", "Mililani", "Pearl City"],
    "New Jersey": [
        "Englewood Cliffs",
        "Paramus",
        "Piscataway",
        "Ramsey",
        "Springfield",
    ],
    "Nevada": ["Las Vegas"],
    "New York": [
        "East Northport",
        "Kew Gardens",
        "Nanuet",
        "Pelham Manor",
        "Scarsdale",
        "Valley Stream",
        "Yorktown Heights",
    ],
    "Oregon": [
        "Beaverton",
        "Clackamas",
        "Gladstone",
        "Hillsboro",
        "Portland",
        "Tigard",
    ],
    "Texas": ["Austin", "Dallas", "Houston"],
    "Virginia": ["Fairfax", "Falls Church"],
    "Washington": [
        "Bothell",
        "Issaquah",
        "Kent",
        "Lynnwood",
        "Redmond",
        "Seattle",
        "Tacoma",
        "Vancouver",
    ],
}
"""