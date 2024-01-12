from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import re

# Ustawienie sterownika Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Lista do przechowywania danych produktów
data_to_write = []

try:
    page_number = 1  # Zaczynamy od pierwszej strony

    while True:
        # Budowanie URL-a dla kolejnych stron
        url = f"https://www.mediaexpert.pl/agd/pralki-i-suszarki/pralki?page={page_number}"
        driver.get(url)

        # Oczekiwanie na załadowanie produktów
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.offers-list div.offer-box h2.name"))
            )
        except:
            print(f"Strona {page_number} nie zawiera więcej produktów lub nie istnieje.")
            break

        # Znalezienie produktów i cen
        products = driver.find_elements(By.CSS_SELECTOR, "div.offers-list div.offer-box h2.name")
        prices = driver.find_elements(By.CSS_SELECTOR, "div.offers-list div.offer-box div.price-box div.prices-section div.main-price span.whole")

        # Ekstrakcja danych
        for product, price in zip(products, prices):
            product_name = product.text.strip()
            product_price = re.sub(r'[^\d]', '', price.text)  # Usunięcie wszystkiego oprócz cyfr
            data_to_write.append([product_name, product_price])

        page_number += 1  # Przejście do następnej strony
        time.sleep(2)  # Krótkie oczekiwanie przed przejściem do kolejnej strony

finally:
    # Zapis do pliku CSV
    with open('products_and_prices.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nazwa produktu', 'Cena'])
        writer.writerows(data_to_write)

    # Zamknięcie przeglądarki
    driver.quit()

print("Dane zapisane do pliku CSV.")
