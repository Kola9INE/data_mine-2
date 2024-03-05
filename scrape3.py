import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Instantiating Chrome webdriver
chrome_options = Options()
chrome_service = Service()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options, service=chrome_service)

# Creating list variables to contain results
NAME = []
PHONE = []
WEBADRESS = []
PHYSICAL_ADDRESS = []
EMAIL  = []

driver.get("https://www.californiasbdc.org/find-your-sbdc/")
driver.maximize_window()

time.sleep(5)

sbdc = driver.find_element(By.CLASS_NAME, "locations")
sbdc_list = sbdc.find_elements(By.TAG_NAME, "article")

for items in sbdc_list:
    name = items.find_element(By.TAG_NAME, "h3").text
    time.sleep(2)

    try:
        phone = items.find_element(By.CLASS_NAME, "entry-phone")
        phone_num = phone.find_element(By.TAG_NAME, "a").text
        time.sleep(2)
    except NoSuchElementException:
        phone_num = " "

    web = items.find_element(By.CLASS_NAME, "entry-website")
    web_link = web.find_element(By.TAG_NAME, "a").get_attribute('href')
    time.sleep(2)

    address = items.find_element(By.CLASS_NAME, "entry-address").text.replace('\n', ", ").strip()
    time.sleep(2)

    try:
        email_add = items.find_element(By.CLASS_NAME, "entry-email")
        email = email_add.find_element(By.TAG_NAME, "a").text
        time.sleep(2)
    except NoSuchElementException:
        email = ' '

    NAME.append(name)
    PHONE.append(phone_num)
    WEBADRESS.append(web_link)
    PHYSICAL_ADDRESS.append(address)
    EMAIL.append(email)

time.sleep(3)
driver.quit()

data = {"NAME":NAME,
        "PHONE":PHONE,
        "WEB_LINK":WEBADRESS,
        "ADDRESS":PHYSICAL_ADDRESS,
        "EMAIL":EMAIL}

df = pd.DataFrame(data)
df.to_csv("sbdc/sbdc.csv")