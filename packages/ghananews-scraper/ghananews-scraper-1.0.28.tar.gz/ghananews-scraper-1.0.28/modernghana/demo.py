import csv
import time
import unicodedata

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options

# Set up Selenium options
chrome_options = Options()
# Run Chrome in headless mode
chrome_options.add_argument("--headless")
chrome_options.page_load_timeout = 600  # 300 seconds
chrome_options.implicitly_wait = 600    # 300 seconds

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

BASE_URL = 'https://www.modernghana.com/'
URL = 'https://www.modernghana.com/ghanahome/sports/'

# Open the webpage
driver.get(URL)

soup = BeautifulSoup(driver.page_source, "html.parser")
print(soup)

pages = soup.find_all("div", class_='cnda')

URLS = [BASE_URL + page_link.find("a")['href'] for page_link in pages]

print(URLS)

# URLS = [BASE_URL + page.a["href"] for page in soup.find_all('i', class_='fa fa-circle')]
# print(URLS)


if __name__ == '__main__':
    pass