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
from parse import parse_date, parse_estimate, parse_price, parse_size
from Email import send_error_email

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

target_url = "https://www.heffel.com/Links/Results_Choose_E" 

# ---------------------

try:
    # Define the headers (column names) as a list
    column_names = ['Auction', 'Lot Number', 'Artist', 'Title', 'Day', 'Month', 'Year', 'Price', 'Lowbound', 'Highbound',  'Width', 'Height', 'Medium', 'Essay', 'Provenance', 'Image']

    # Create the empty DataFrame using the 'columns' parameter
    df = pd.DataFrame(columns=column_names)
    
    # Start the session using the Edge WebDriver
    # This will open a new Edge browser window
    print("Starting Edge WebDriver...")
    driver = webdriver.Edge(service=service, options=options)

    # Take action on the browser (Navigate to the website)
    print(f"Navigating to: {target_url}")
    driver.get(target_url)

    # This list contains the links to all the auctions of all years
    auction_links = []

    for year in range(2003, 2026):
        print(f"Switching to year: {year}")
        
        # Re-find the dropdown every time because the page refreshes
        dropdown = Select(driver.find_element(By.ID, "MainContent_cboYear"))
        
        # Trigger the change
        dropdown.select_by_visible_text(str(year))
        
        # Wait for the __doPostBack to finish loading the new data
        human_delay(5, 7)
        
        # Find the list of links for the current year
        auction_element_text = driver.find_elements(By.CSS_SELECTOR, '.font-bold')
        print(f"Found {len(auction_element_text)} elements")

        # Collect all the links. Start at the second one on each page because the first element is now what were looking for
        for element in auction_element_text[1:]:
            auction_links.append(element.find_element(By.TAG_NAME, "a").get_attribute('href'))
    
    for link in auction_links:

        driver.get(link)
        human_delay(5, 7)

        piece_link_elements_outer = driver.find_elements(By.CSS_SELECTOR, ".height-adj-md-0x.fixed_height_1")

        # Finding the right row to find the link in; piece_links contains all the piece links to the current auction
        piece_links = []
        for element in piece_link_elements_outer:
            piece_links.append(element.find_elements(By.TAG_NAME, "td")[1].find_element(By.TAG_NAME, 'a').get_attribute('href'))
        
        print(f"Found {len(piece_links)} pieces in this auction")

        # Traverse through the pieces for the current auction (This will only excecute if there are any)
        for piece in piece_links:
            
            # Navigate to the piece page
            driver.get(piece)
            human_delay(5, 7)

            # All the scraping logic
            auction = get_element_text(driver, By.ID, "MainContent_AuctionInfo_divInfo")
            print(auction.replace("\n", "; "))

            try:
                image_link = driver.find_element(By.ID, "MainContent_bigImage").get_attribute("src")
            except:
                image_link = "N/A"

            lot_number = get_element_text(driver, By.ID, "MainContent_lotNumber")

            artist = get_element_text(driver, By.ID, "MainContent_HyperLinkArtistName")

            title = get_element_text(driver, By.ID, "MainContent_itemTitle")

            medium = get_element_text(driver, By.ID, "MainContent_media")

            size = get_element_text(driver, By.ID, "MainContent_dimensionIN")
            width, height = parse_size(size)

            estimate = get_element_text(driver, By.ID, "MainContent_estimate")
            lowbound, highbound = parse_estimate(estimate)

            price = parse_price(get_element_text(driver, By.ID, "MainContent_soldFor"))

            provenance = get_element_text(driver, By.ID, "MainContent_provenance").replace("\n", "; ")

            essay = get_element_text(driver, By.ID, "MainContent_essay")

            date = get_element_text(driver, By.ID, "MainContent_AuctionInfo_divInfo").split("\n")
            day, month, year = parse_date(date[len(date) - 1])

            # Adding to the dataframe
            df.loc[len(df)] = [
            auction, lot_number, artist, title, day, month, year, 
            price, lowbound, highbound, width, height, medium, 
            essay, provenance, image_link
            ]

except Exception as e:
    print(f"An error occurred during WebDriver operation: {e}")

    # Capture the full "traceback" (the specific lines where it failed)
    full_error = traceback.format_exc()
    
    # Send the email notification
    send_error_email(full_error)

finally:
    # 5. End the session (Close the browser)
    # This is crucial for releasing system resources
    if 'driver' in locals() and driver:
        print("Quitting the WebDriver session.")
        driver.quit()

    pd.set_option('display.max_columns', None)
    print(df.head(3))
    # df.to_csv('auction_results.csv', index=False)