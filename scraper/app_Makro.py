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
def scraping_Makro():
    driver = webdriver.Chrome()
    driver.set_window_position(-10000,0)
    num_pages = 19
    num_pages = 30

    url_num = 0

    url_addresses = [ 'https://tienda.makro.com.co/search?name=arroz',  
            'https://tienda.makro.com.co/search?name=aceite',  
            'https://tienda.makro.com.co/search?name=leche',  
            'https://tienda.makro.com.co/search?name=detergente']
    
    csv_file = ["rice_Makro.csv", "oil_Makro.csv", "milk_Makro.csv", "detergent_Makro.csv"]

    for url in url_addresses:
        driver.get(url)
        time.sleep(10)
        product_elements = driver.find_elements(By.CSS_SELECTOR, "div.styles__StyledCard-sc-3jvmda-0.LSTlO")
        length=len(product_elements)
        
        brands = []
        productNames = []
        prices = []
        timestamps = []
        brands = []
        productNames = []
        prices = []
        timestamps = []

        for i in range(length):

            try: 
                driver.get(url)
                time.sleep(5)
                product_elements = driver.find_elements(By.CSS_SELECTOR, "div.styles__StyledCard-sc-3jvmda-0.LSTlO")
                product_elements[i].click()
                time.sleep(10)
                
                brand = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.styles-sc-k9yd3a-1.jcSiZT")))
                
                productName = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.DetailName__DetailNameStyles-sc-173f5q0-0.cTkTkv.prod__name")))
                
                price = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.DetailBasePrice__DetailBasePriceStyles-sc-1hromxy-0.jQtrSh.base__price")))
                
                brands.append(brand.text)
                productNames.append(productName.text)
                prices.append(price.text)
                timestamps.append(datetime.now())
                
            except Exception as e:
                    print(f"Error occurred :: {e}")
            
            print(brands)
            print(productNames)
            print(prices)
            # driver.back()
                
        # Create a DataFrame and save to CSV
        df = pd.DataFrame({
            'Timestamp': timestamps,
            'brand': brands,
            'Name': productNames,
            'Price': prices
        })

        df.to_csv(csv_file[url_num], index=False)
        url_num += 1

    # Close the WebDriver
    driver.quit()
