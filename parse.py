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
import re
from datetime import date, datetime

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


def parse_size(size):
    try:
        # Matches integers/decimals and optional fractions
        pattern = r"(\d+\.?\d*)(?:\s+(\d+/\d+))?"
        matches = re.findall(pattern, size.strip())
        
        clean_values = []
        for number, fraction in matches:
            val = float(number)
            if fraction:
                num, den = fraction.split('/')
                val += int(num) / int(den)
            clean_values.append(val)
        
        # Return the first value as width and second as height
        # Using [:2] ensures we don't crash if more than 2 numbers are found
        width, height = clean_values[:2]
        
        return width, height
    except:
        return "N/A", "N/A"

def dolla_remover(number):
    return int(number.strip("$").replace(",", ""))

def parse_price(price):
    try:
        price = dolla_remover(price.strip().split()[2]) 
        # Returns int
        return price

    except:
        return "N/A"
        
def parse_estimate(estimate):
    try:
        decon = estimate.strip().split()
        
        lowbound = dolla_remover(decon[1])
        highbound = dolla_remover(decon[3])  
        # lowbound, highound
        return lowbound, highbound
    except:
        return "N/A", "N/A"

def parse_date(date):
    try:
        date = date.split("|")[0].strip()
        decon = date.strip().split()

        year = int(decon[2].strip(","))
        day = int(decon[1].strip(","))
        month = int(datetime.strptime(decon[0].strip(","), "%B").month)

        return day, month, year

    except Exception as e:
        print(e)
        return "N/A","N/A","N/A"

    
    
width, height = parse_size("22     1/4 x 25  in,")
print(width)
print(height)

lowbound, highbound = parse_estimate("      estimate:          $30,000 - $50,000 CAD")
print(lowbound)
print(highbound)

price = parse_price("     sold for: $35,100      ")
print(price)

day, month, year = parse_date("November 25, 2010 | 10:00 PM")
print(day)
print(month)
print(year)