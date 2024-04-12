from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np
from itertools import chain


def scrape_top_search_results(search_query):
    driver = webdriver.Chrome()
    driver.get("https://shop.bewakoof.com/")  # Replace "https://example.com" with the actual website URL
    
    # Find the search input element and input the search query
    search_input = driver.find_element(By.CSS_SELECTOR, ".search-input-field")  # Use CSS selector to find the search input field
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.RETURN)  # Press Enter to perform the search
    
    # Wait for the search results to load (adjust wait time as needed)
    time.sleep(5)  # You may need to adjust this wait time based on the website's loading speed
    
    # Find the search results elements
    product_cards = driver.find_elements(By.CSS_SELECTOR, "section.product-card-container")  # Adjust the CSS selector for search result items

    for i,card in enumerate(product_cards[:5]):
        try:
            product_name = card.find_element(By.TAG_NAME, "img")
            image_data = []
            image_src = product_name.get_attribute("src")
            image_alt = product_name.get_attribute("alt")
            if image_src: 
                image_data.append({"src": image_src, "alt": image_alt})
            print(image_data,'<-- prod_name')
            rating = card.find_element(By.XPATH, F'//*[@id="product-grid"]/section[{i}]/div/a/div/figure/article/span').text
            print(rating)
        except Exception as e:
            print('exec')
    # product_rating = card.find_element(By.CSS_SELECTOR, "article svg + span").text
    #     product_price = card.find_element(By.CSS_SELECTOR, "section.flex-wrap span.productPrice").text
    #     product_data.append({"name": product_name, "rating": product_rating, "price": product_price})
    
    # # Close the WebDriver
    # driver.quit()
    # print(product_data)
    return []

user_search_query = 'shirt'
top_5_results = scrape_top_search_results(user_search_query)
print("Top 5 search results:")
# # for i, data in enumerate(top_5_results, 1):
#     print(f"Product {i}:")
#     print(f"Name: {data['name']}")
#     print(f"Rating: {data['rating']}")
#     print(f"Price: {data['price']}")
#     print()