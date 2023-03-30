import time

from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("detach", True)

CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"
GOOGLE_SHEETS = "https://forms.gle/Nrnn8JcrSQAvMy3L6"

ZILLOW = "https://www.zillow.com/brooklyn-new-york-ny/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A43.18435549759412%2C%22east%22%3A-69.25950652343751%2C%22south%22%3A39.75281661400167%2C%22west%22%3A-75.68650847656251%7D%2C%22mapZoom%22%3A8%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A350089%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22min%22%3A1800%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A37607%2C%22regionType%22%3A17%7D%2C%7B%22regionId%22%3A44269%2C%22regionType%22%3A6%7D%5D%7D"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 "
                  "Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(ZILLOW, headers=header)
zillow_webpage = response.text
soup = BeautifulSoup(zillow_webpage, "html.parser")
apartments = soup.find_all(name="div", class_="StyledCard-c11n-8-73-8__sc-rmiu6p-0")

price_list = []
link_list = []
address_list = []
for apartment in apartments:
    # For the price
    if "+" in apartment.select("div div span")[0].getText():
        price = apartment.select("div div span")[0].getText().split("/")[0].split("$")[1].split("+")[0]
    else:
        price = apartment.select("div div span")[0].getText().split("/")[0].split("$")[1]

    # For the link
    if "https://" in apartment.select("div a")[0].get("href"):
        link = apartment.select("div a")[0].get("href")
    else:
        link = "https://www.zillow.com" + apartment.select("div a")[0].get("href")

    # For the address
    address = apartment.select("div a")[0].getText()

    price_list.append(price)
    link_list.append(link)
    address_list.append(address)

print(price_list)
print(link_list)
print(address_list)


service = ChromeService(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)





for i in range(len(address_list)):
    driver.get(GOOGLE_SHEETS)
    driver.maximize_window()
    address_box = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div['
                                                     '2]/div/div[1]/div/div[1]/input')
    rent_box = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div['
                                                  '2]/div/div[1]/div/div[1]/input')
    link_box = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div['
                                                  '2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div['
                                                       '1]/div/span/span')

    time.sleep(2)
    address_box.send_keys(address_list[i])
    rent_box.send_keys(price_list[i])
    link_box.send_keys(link_list[i])
    submit_button.click()




