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
def scraping_exito():
    driver = webdriver.Chrome()
    driver.set_window_position(-10000,0)
    page_number = 0
    brands = []
    productNames = []
    prices = []
    url_num = 0
    timestamps = []

    # Define the URLs to scrape and corresponding CSV file names
    url_addresses = [
        "https://www.exito.com/s?q=arroz&sort=score_desc&page=",
        "https://www.exito.com/s?q=aceite&sort=score_desc&page=",
        "https://www.exito.com/s?q=leche&sort=score_desc&page=",
        "https://www.exito.com/s?q=detergente&sort=score_desc&page="
    ]
    csv_file = ["rice_exito.csv", "oil_exito.csv", "milk_exito.csv", "detergent_exito.csv"]

    # Loop through each URL address
    for url in url_addresses:
        page_number = 0  
        while True:
            # Define the URL of the website to scrape
            full_url = f'{url}{page_number}'  # Construct the full URL
            driver.get(full_url)
            actions = ActionChains(driver)

            time.sleep(1)  # Allow time for the page to load

            # Locate product elements on the page
            product_elements = driver.find_element(By.CSS_SELECTOR, '.product-grid_fs-product-grid___qKN2').find_elements(By.TAG_NAME, "li")
            product_num = len(product_elements)

            for product in product_elements:
                try:
                    time.sleep(1)  # Allow time for elements to load

                    # Open product details in a new tab
                    actions.key_down(Keys.CONTROL).click(product).key_up(Keys.CONTROL).perform()
                    product_page = driver.window_handles[-1]
                    driver.switch_to.window(product_page)

                    time.sleep(1)  # Allow time for product page to load
                    
                    # Scrape brand, product name, and price
                    brand = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-title_product-title__specification__UTjNc"))
                    )
                    
                    productName = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-title_product-title__heading___mpLA"))
                    )
                    
                    price = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".ProductPrice_container__price__XmMWA"))
                    )

                    # Append scraped data to lists
                    brands.append(brand.text)
                    productNames.append(productName.text)
                    prices.append(price.text)
                    timestamps.append(datetime.now())

                except Exception as e:
                    print(f"Error occurred while scraping product: {e}")
                
                driver.close() 
                driver.switch_to.window(driver.window_handles[0])  # Switch back to the main window

            if product_num < 16:  # Break if there are fewer than expected products on the page
                break 

            page_number += 1  # Move to the next page      

        # Create a DataFrame and save to CSV for each URL category
        df = pd.DataFrame({
            'Timestamp': timestamps,
            'brand': brands,
            'Name': productNames,
            'Price': prices
        })

        df.to_csv(csv_file[url_num], index=False)  # Save DataFrame to corresponding CSV file

        url_num += 1  
        

    # Close the WebDriver after all scraping is done
    driver.quit()
    
    
    
    
            #     full_url = f'{url}{page_number}'  # Construct the full URL
            # driver.get(full_url)
            # actions = ActionChains(driver)

            # time.sleep(1)  # Allow time for the page to load

            # # Locate product elements on the page
            # product_elements = driver.find_element(By.CSS_SELECTOR, '.product-grid_fs-product-grid___qKN2').find_elements(By.TAG_NAME, "li")
            # product_num = len(product_elements)