import time
import json
import logging
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv

# =========================
# Load environment variables
# =========================
load_dotenv()

# =========================
# Logging configuration
# =========================
logging.basicConfig(
    filename="amazon_scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# Product categories
# =========================
product_list = [
    "Shampoo","Soap","Toothpaste","ToothBrush","Deodorant",
    "Moisturizers","Facewash","hair oil","Sunscreens",
    "speakers","watches","computer accessories","headphones",
    "LED lights","Diapers","wipes","feeding bottles",
    "baby lotions","gift sets"
]

final_product_list = []

# =========================
# Start Selenium browser
# =========================
try:
    url = "https://www.amazon.in/"

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    logging.info("Amazon website opened successfully")

except Exception as e:
    logging.error(f"Error starting browser: {e}")
    raise

# =========================
# Handle popup if present
# =========================
try:
    continue_bar = driver.find_element(By.CLASS_NAME, "a-button-text")
    continue_bar.click()
except Exception:
    pass

wait = WebDriverWait(driver, 5)

# =========================
# Scraping loop
# =========================
for product in product_list:

    try:
        search_bar = wait.until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )

        search_bar.clear()
        search_bar.send_keys(product)
        search_bar.send_keys(Keys.ENTER)

        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        product_name_list = driver.find_elements(
            By.CSS_SELECTOR,
            "h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal"
        )

        price_list = driver.find_elements(By.CSS_SELECTOR, "span.a-price-whole")

        rating_list = driver.find_elements(By.CSS_SELECTOR, "span.a-icon-alt")

        for name, price, rating in zip(product_name_list, price_list, rating_list):

            try:
                price_value = price.text.replace(",", "") if price.text else 0
                rating_value = rating.text.split(" ")[0] if rating.text else 0

                final_product_list.append({
                    "product_category": product,
                    "product_name": name.text.strip(),
                    "price": float(price_value),
                    "rating": float(rating_value)
                })

            except Exception as e:
                logging.warning(f"Error processing product: {e}")

        logging.info(f"Successfully scraped {product}")

    except Exception as e:
        logging.error(f"Error scraping {product}: {e}")

driver.quit()

logging.info("Scraping completed")

# =========================
# Save JSON
# =========================
try:
    with open("products.json", "w") as file:
        json.dump(final_product_list, file, indent=4)

    logging.info("JSON file saved successfully")

except Exception as e:
    logging.error(f"Error saving JSON: {e}")

# =========================
# Database connection
# =========================
db_config = {
    "host": os.getenv("YOUR_HOST_NAME"),
    "user": os.getenv("YOUR_USER_NAME"),
    "password": os.getenv("YOUR_PASSWORD"),
    "database": os.getenv("YOUR_DATABASE")
}

try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    logging.info("Database connected successfully")

except Exception as e:
    logging.error(f"Database connection failed: {e}")
    raise

# =========================
# Create table if not exists
# =========================
create_table_query = """
CREATE TABLE IF NOT EXISTS products (
    product_category VARCHAR(100),
    product_name TEXT,
    price NUMERIC,
    rating NUMERIC
);
"""

cursor.execute(create_table_query)
conn.commit()

logging.info("Table checked/created")

# =========================
# Load JSON data
# =========================
with open("products.json", "r") as file:
    data = json.load(file)

# =========================
# Prepare records
# =========================
records = []

for row in data:
    records.append((
        row["product_category"],
        row["product_name"],
        row["price"],
        row["rating"]
    ))

# =========================
# Bulk insert
# =========================
insert_query = """
INSERT INTO products
(product_category, product_name, price, rating)
VALUES (%s, %s, %s, %s)
"""

try:
    execute_batch(cursor, insert_query, records)

    conn.commit()

    logging.info("Data inserted successfully")

except Exception as e:
    logging.error(f"Error inserting data: {e}")

cursor.close()
conn.close()

logging.info("Script finished successfully")