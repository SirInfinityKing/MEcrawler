# Zapisywanie do bazy danych

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time
import re
import sqlite3

# Ustawienie sterownika Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Nawiązanie połączenia z bazą danych SQLite
conn = sqlite3.connect('me.db')
c = conn.cursor()

# Utworzenie tabeli, jeśli nie istnieje
c.execute('''CREATE TABLE IF NOT EXISTS mediaexpert (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kategoria TEXT NOT NULL,
                nazwa TEXT NOT NULL,
                cena REAL NOT NULL,
                data_dodania DATE NOT NULL,
                UNIQUE(kategoria, nazwa, data_dodania)
             );''')

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
        except TimeoutException:
            print(f"Strona {page_number} nie zawiera więcej produktów lub nie istnieje.")
            break

        # Znalezienie produktów i cen
        products = driver.find_elements(By.CSS_SELECTOR, "div.offers-list div.offer-box h2.name")
        prices = driver.find_elements(By.CSS_SELECTOR, "div.offers-list div.offer-box div.price-box div.prices-section div.main-price span.whole")

        # Ekstrakcja danych i zapis do bazy danych
        for product, price in zip(products, prices):
            kategoria = "Pralki i suszarki"
            nazwa = product.text.strip()
            cena = float(re.sub(r'[^\d.]', '', price.text))  # Usunięcie wszystkiego oprócz cyfr i kropki
            data_dodania = time.strftime('%Y-%m-%d')  # Aktualna data

            # Dodawanie rekordu do bazy danych, ignorowanie duplikatów
            c.execute('''INSERT OR IGNORE INTO mediaexpert (kategoria, nazwa, cena, data_dodania)
                         VALUES (?, ?, ?, ?)''', (kategoria, nazwa, cena, data_dodania))

        conn.commit()  # Zatwierdź zmiany w bazie danych

        page_number += 1  # Przejście do następnej strony
        time.sleep(2)  # Krótkie oczekiwanie przed przejściem do kolejnej strony

except Exception as e:
    print(f"Wystąpił błąd: {e}")

finally:
    # Zamknięcie przeglądarki
    driver.quit()
    # Zamknięcie połączenia z bazą danych
    conn.close()

print("Dane zapisane do bazy danych SQLite.")
