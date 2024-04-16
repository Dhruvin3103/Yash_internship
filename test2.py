from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time

def scrape_top_search_results(search_query,more_images):
    driver = webdriver.Chrome()
    link = ["https://shop.bewakoof.com/","https://www.myntra.com/"]
    print("bewakoof --------> : ")
    driver.get("https://shop.bewakoof.com/") 
    search_input = driver.find_element(By.CSS_SELECTOR, ".search-input-field") 
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.RETURN) 
    time.sleep(5)  
    product_cards = driver.find_elements(By.CSS_SELECTOR, "section.product-card-container")  # Adjust the CSS selector for search result items
    result = []
    for i, card in enumerate(product_cards[:5]):
        try:
            product_name = card.find_element(By.TAG_NAME, "img")
            image_data = []
            image_src = product_name.get_attribute("src")
            image_alt = product_name.get_attribute("alt")
            rating = card.find_element(By.XPATH, f'//*[@id="product-grid"]/section[{i+1}]/div/a/div/figure/article/span').text
            if image_src: 
                image_data.append({"src": image_src, "alt": image_alt, "rating": rating})
            print(image_data, '<-- prod_name')
            product_link = card.find_element(By.XPATH, f'//*[@id="product-grid"]/section[{i+1}]/div/a')
            product_url = product_link.get_attribute("href")
            res = requests.get(product_url)
            soup = BeautifulSoup(res.text, 'html.parser')
            # with  open('test.txt', 'w', encoding='utf-8') as file:
            #     file.write(str(soup.prettify))
            # print(soup.prettify())
            if more_images:
                swiper_slides = soup.find_all('figure', class_='swiper-slide')
                image_data_list = []
                for swiper_slide in swiper_slides[:4]:
                    img_tag = swiper_slide.find('img')
                    if img_tag:
                        image_src = img_tag['src']
                        image_alt = img_tag.get('alt', '')
                        image_data = {"src": "https:"+image_src, "alt": image_alt}
                        image_data_list.append(image_data)
                print(f"more images : \n {image_data_list}")
        except Exception as e:
            print(e)
        result.append(image_data)
    #now its turn for amazon :)
    driver.get("https://www.amazon.in/")
    print('Amazon  ---- > ')
    search_input = driver.find_element(By.ID,"twotabsearchtextbox")
    print('serach element ')
    print(search_input.text)
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)
    product_cards = driver.find_elements(By.CSS_SELECTOR,"img.s-image")
    print(len(product_cards))
    image_urls = [img.get_attribute("src") for img in product_cards]
    for i in image_urls[:5]:
        print(i)
    # for url in product_cards[:2]:
    #     prod_url = url.get_attribute("href")
    #     res = requests.get(prod_url)
    #     soup = BeautifulSoup(res.text, 'html.parser')
    #     with  open('test.txt', 'w', encoding='utf-8') as file:
    #         file.write(str(soup.prettify))
    #     url.click()
        
    #     time.sleep(5)
    #     print
    #     for i in range(2):
    #         img_tag = driver.find_element(By.CLASS_NAME,f'li.a-spacing-small item imageThumbnail a-declarative')
    #         print(img_tag.text,"<-- anythung here ")
    #         print(img_tag.get_attribute("src"),img_tag.get_attribute("alt"))
    
    driver.quit()
    return []
    

res = scrape_top_search_results('shirt',True)
print(res)
