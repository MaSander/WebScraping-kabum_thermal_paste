from numbers import Number
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

import pandas as pd

def treatment_price(str_data):
    str_data = str_data.replace('R$', '').strip()
    str_data = str_data.replace(',', '.')
    try:
        return float(str_data)
    except ValueError:
        return None

def treatment_gram(str_data):
    str_data = re.search(r'\b\d{1,3}(?:[.,]\d)?\s?(g|gr|grs|gramas|gramo|gramos)\b\.?', str_data.lower())
    if str_data:
        str_data = str_data.group(0)
        str_data = str_data.replace(',', '.')
        re_numbers = re.findall(r'\d+[.,]?\d*', str_data)
        return float(''.join(re_numbers))

def treatment_thermal_conductivity(str_data):
    # 3,05 w/mk
    str_data = re.search(r'\b\d{1,2}(?:[.,]\d)?\s*w(?:\/|\s+)m[·-]?k\b|\b\d{1,2}(?:[.,]\d)?\s*w\b', str_data.lower())
    if str_data:
        str_data = str_data.group(0)
        str_data = str_data.replace(',', '.')
        re_numbers = re.findall(r'\d+(?:.\d+)?', str_data)
        return float(''.join(re_numbers))

# Function to get all product links from a page
def get_product(driver, page_number):
    url = f"https://www.kabum.com.br/hardware/coolers/pasta-termica?page_number={page_number}&page_size=100"
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".productCard"))
        )

        # Get all product
        products_extracted = []
        products = driver.find_elements(By.CSS_SELECTOR, ".productCard")
        for product in products:
            link = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            name = product.find_element(By.CLASS_NAME, "nameCard").text.strip()
            price = product.find_element(By.CLASS_NAME, "priceCard").text.strip()
            products_extracted.append({
                "thermal_conductivity": treatment_thermal_conductivity(name),
                "gram": treatment_gram(name),
                "price": treatment_price(price),
                "name": name,
                "link": link,
            })
        return products_extracted
    except Exception as ex:
        print(ex)
        return []

async def scraping_kabum_thermal_paste():
    print("starting web scraping")
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Run in headless mode
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    all_product = []
    page = 0

    while True:
        page += 1
        print('\r' + f"loading page {page}...", end='')
        product = get_product(driver, page)
        if not product:
            break
        all_product.extend(product)
        time.sleep(5)  # Add delay between requests

    print("")
    driver.quit()

    df = pd.DataFrame(all_product)
    df = df.dropna()
    df.to_csv('thermal_pastes.csv', index=False)
    return df
