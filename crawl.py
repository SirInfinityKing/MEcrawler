from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment if you want to run in headless mode

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_product_name_and_price(url):
    driver.get(url)
    time.sleep(5)  # Give time for the page to load
    
    # Extracting product name
    product_name = driver.find_element(By.CSS_SELECTOR, 'a.is-animate.spark-link').text.strip()
    
    # Extracting product price
    product_price = driver.find_element(By.CSS_SELECTOR, 'span.whole').text.strip()

    driver.quit()
    
    return product_name, product_price

# Replace 'url' with the actual URL of the product page
product_url = 'https://www.mediaexpert.pl/agd/pralki-i-suszarki/pralki'
name, price = get_product_name_and_price(product_url)

print(f"Product Name: {name}")
print(f"Product Price: {price}")
