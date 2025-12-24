from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
# from Parsing import parse_artist, parse_date, parse_essay, parse_estimate, parse_price, parse_size, parse_title
import traceback
# from Email import send_error_email
import random
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.options import Options
from parse import parse_date, parse_estimate, parse_price, parse_size, dolla_remover
import re

def human_delay(min_seconds=2, max_seconds=5):
    """
    Pauses execution for a random amount of time to mimic human browsing.
    """
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

# To find the element and return the raw text
def get_element_text(driver, by, selector, default_val="N/A"):
    try:
        return driver.find_element(by, selector).text
    except:
        return default_val
    
service = Service() 

options = Options()
# 1. This tells the browser to only log FATAL errors, ignoring warnings and info
options.add_argument('--log-level=3')
# 2. This specifically hides the "DevTools listening on..." and other terminal clutter
options.add_experimental_option('excludeSwitches', ['enable-logging'])

target_url = "https://www.heffel.com/Auction/LotDetails_E?Request=iZTDNdl2DfJc8jRi4pFzNF4FyYcqe80krsL77dDV7HDF/lKvrfVDv9VkS+iiRu0Wfqhu3A+/6rNzSZj1x/A+qmCV50DrPgm1jmilpc8pxcrWXO5y4u6An8e0KbO+YF82JYKxLrMyB15WiWUf7+uzvS7sXL5DnCIAdnRNDNxpyZKaO6wGtEYw6dqAYmrMyXoYrwi8h52tpZv/mPi8mFhlOHelvn2uj6hg" 

# ---------------------

try:
    # Define the headers (column names) as a list
    column_names = ['Auction', 'Lot', 'Artist', 'Title', 'Day', 'Month', 'Year', 'Price', 'Lowbound', 'Highbound',  'Width', 'Height', 'Essay', 'Provenance', 'Image']

    # Create the empty DataFrame using the 'columns' parameter
    df = pd.DataFrame(columns=column_names)
    
    # Start the session using the Edge WebDriver
    # This will open a new Edge browser window
    print("Starting Edge WebDriver...")
    driver = webdriver.Edge(service=service, options=options)

    # Take action on the browser (Navigate to the website)
    print(f"Navigating to: {target_url}")
    driver.get(target_url)

    auction = get_element_text(driver, By.ID, "MainContent_AuctionInfo_divInfo")
    print(auction.replace("\n", "; "))

    try:
        image_link = driver.find_element(By.ID, "MainContent_bigImage").get_attribute("src")
    except:
        image_link = "N/A"
    print(image_link)

    lot_number = get_element_text(driver, By.ID, "MainContent_lotNumber")
    print(lot_number)

    artist = get_element_text(driver, By.ID, "MainContent_HyperLinkArtistName")
    print(artist)

    title = get_element_text(driver, By.ID, "MainContent_itemTitle")
    print(title)

    medium = get_element_text(driver, By.ID, "MainContent_media")
    print(medium)

    size = get_element_text(driver, By.ID, "MainContent_dimensionIN")
    width, height = parse_size(size)
    print(width, height)

    estimate = get_element_text(driver, By.ID, "MainContent_estimate")
    print(estimate)
    lowbound, highbound = parse_estimate(estimate)
    print(f"{lowbound} - {highbound}")

    price = get_element_text(driver, By.ID, "MainContent_soldFor")
    print(parse_price(price))

    provenance = get_element_text(driver, By.ID, "MainContent_provenance").replace("\n", "; ")
    print(provenance)

    essay = get_element_text(driver, By.ID, "MainContent_essay")
    print(essay)

    date = get_element_text(driver, By.ID, "MainContent_AuctionInfo_divInfo").split("\n")
    print(parse_date(date[len(date) - 1]))


    


except Exception as e:
    print(f"An error occurred during WebDriver operation: {e}")

    # Capture the full "traceback" (the specific lines where it failed)
    full_error = traceback.format_exc()
    
    # Send the email notification
    # send_error_email(full_error)

finally:
    # 5. End the session (Close the browser)
    # This is crucial for releasing system resources
    if 'driver' in locals() and driver:
        print("Quitting the WebDriver session.")
        driver.quit()

    pd.set_option('display.max_columns', None)
    print(df.head(3))
    # df.to_csv('auction_results.csv', index=False)



width, height = parse_size("22 x 25 3/4 in,")
print