from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pandas as pd
import time
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


def scraping_D1():
    driver = webdriver.Chrome()
    driver.set_window_position(-10000, 0)

    url_num = 0

    urls = [ 'https://domicilios.tiendasd1.com/search?name=arroz',
            'https://domicilios.tiendasd1.com/search?name=aceite',
            'https://domicilios.tiendasd1.com/search?name=leche',
            'https://domicilios.tiendasd1.com/search?name=detergente']
    
    csv_file = ["rice_D1.csv", "oil_D1.csv", "milk_D1.csv", "detergent_D1.csv"]
    
    if not os.path.exists('data'):
        os.makedirs('data')

    for url_num, url in enumerate(urls):
        driver.get(url)
        time.sleep(10)
        product_elements = driver.find_elements(By.CSS_SELECTOR, "div.styles__StyledCard-sc-3jvmda-0.LSTlO")
        length = len(product_elements)
        
        brands = []
        productNames = []
        prices = []
        timestamps = []
        # brands = []
        # productNames = []
        # prices = []
        # timestamps = []

        for i in range(length):

            try: 
                driver.get(url)
                time.sleep(5)
                product_elements = driver.find_elements(By.CSS_SELECTOR, "div.styles__StyledCard-sc-3jvmda-0.LSTlO")
                product_elements[i].click()
                time.sleep(1)
                
                brand = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.styles-sc-k9yd3a-1.jcSiZT")))
                
                productName = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.DetailName__DetailNameStyles-sc-173f5q0-0.cTkTkv.prod__name")))
                
                price = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.DetailBasePrice__DetailBasePriceStyles-sc-1hromxy-0.jQtrSh.base__price")))
                
                brands.append(brand.text)
                productNames.append(productName.text)
                prices.append(price.text)
                timestamps.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                
            except Exception as e:
                    print(f"Error occurred: {e}")
                    
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

        # df.to_csv(csv_file[url_num], index=False)
        
        csv_file_path = os.path.join('data', f'D1_{url_num}.csv')
    
        # Save the DataFrame to a CSV file in the "data" folder
        df.to_csv(csv_file_path, index=False)
    
        url_num += 1
    
    # Close the WebDriver
    driver.quit()
