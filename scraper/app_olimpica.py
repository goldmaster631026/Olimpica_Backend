from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pandas as pd
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Chrome WebDriver
def scraping_olimpica():
    driver = webdriver.Chrome()
    driver.set_window_position(-10000,0)

    url_num = 0

    # Define the URLs to scrape and corresponding CSV file names
    url_addresses = [
        "https://www.olimpica.com/arroz?_q=arroz&map=ft&page=",
        "https://www.olimpica.com/aceite?_q=aceite&map=ft&page=",
        "https://www.olimpica.com/leche?_q=leche&map=ft&page=",
        "https://www.olimpica.com/detergente?_q=detergente&map=ft&page="
    ]
    csv_file = ["rice_olimpica.csv", "oil_olimpica.csv", "milk_olimpica.csv", "detergente_olimpica.csv"]

    # Loop through each URL address D
    for url in url_addresses:
        page_number = 1  # Reset page number for each product category
        
        brands = []
        productNames = []
        prices = []
        timestamps = []

        while True:
            # Define the URL of the website to scrape
            full_url = f'{url}{page_number}'  # Construct the full URL
            driver.get(full_url)
            
            
            if full_url == "https://www.olimpica.com/arroz?_q=arroz&map=ft&page=1":
                tooltip_close_button = driver.find_element(By.CSS_SELECTOR, ".fc-button-label").click()
                tooltip_close_button = driver.find_element(By.CSS_SELECTOR, ".olimpica-flash-0-x-tooltipClose").click()
            time.sleep(10)
            try:
                product_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.vtex-search-result-3-x-galleryItem.vtex-search-result-3-x-galleryItem--normal.vtex-search-result-3-x-galleryItem--grid-3.pa4')))
                length=len(product_elements)
                
                for product in product_elements:
                    # Scrape brand, product name, and price
                    brand = product.find_element(By.CSS_SELECTOR, '.vtex-product-summary-2-x-productBrandName')
                    
                    productName = product.find_element(By.CSS_SELECTOR, '.vtex-product-summary-2-x-productNameContainer.mv0.vtex-product-summary-2-x-nameWrapper.overflow-hidden.c-on-base.f5')
                    
                    price = product.find_element(By.CSS_SELECTOR, '.false.olimpica-dinamic-flags-0-x-listPrices')
                    
                    brands.append(brand.text)
                    productNames.append(productName.text)
                    prices.append(price.text) # Switch back to the main window
                    timestamps.append(datetime.now())
                # print(brands,"\n")
                # print(productNames,"\n")
                # print(prices)
                
                print(length)
                if length < 12:
                    break
            except Exception as e:
                continue
            page_number += 1
                # Exit loop if there is an issue loading products
        # Create a DataFrame and save to CSV for each URL category
        df = pd.DataFrame({
            'Timestamp': timestamps,
            'brand': brands,
            'Name': productNames,
            'Price': prices
        })
        
        df.to_csv(csv_file[url_num], index=False)  # Save DataFrame to corresponding CSV file
        
        url_num += 1  # Increment URL number for next category

    # Close the WebDriver after all scraping is done
    driver.quit()
