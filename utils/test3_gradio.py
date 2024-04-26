import gradio as gr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests
import time
import gradio as gr

def scrape_from_bewakoof(search_query,more_images):
    driver = webdriver.Chrome()
    print("bewakoof --------> : ")
    driver.get("https://shop.bewakoof.com/")
    search_input = driver.find_element(By.CSS_SELECTOR, ".search-input-field")
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)
    product_cards = driver.find_elements(By.CSS_SELECTOR, "section.product-card-container")
    result = []
    for i, card in enumerate(product_cards[:5]):
        try:
            product_name = card.find_element(By.TAG_NAME, "img")
            image_data = {}
            image_src = product_name.get_attribute("src")
            image_alt = product_name.get_attribute("alt")
            rating = card.find_element(By.XPATH, f'//*[@id="product-grid"]/section[{i+1}]/div/a/div/figure/article/span').text
            if image_src:
                image_data["src"] = image_src
                image_data["alt"] = image_alt
                image_data["rating"] = rating
                result.append(image_data['src'])
            print(image_data, '<-- prod_name')
            product_link = card.find_element(By.XPATH, f'//*[@id="product-grid"]/section[{i+1}]/div/a')
            product_url = product_link.get_attribute("href")
            res = requests.get(product_url)
            soup = BeautifulSoup(res.text, 'html.parser')
            if more_images:
                swiper_slides = soup.find_all('figure', class_='swiper-slide')
                for swiper_slide in swiper_slides[:4]:
                    img_tag = swiper_slide.find('img')
                    if img_tag:
                        image_src = img_tag['src']
                        image_alt = img_tag.get('alt', '')
                        image_data = {"src": "https:"+image_src, "alt": image_alt}
                        result.append(image_data["src"])
                        print(f"more images : \n {image_data}")
        except Exception as e:
            print(e)
    return result        
    
def scrape_from_amazon(search_query, more_images):
    driver = webdriver.Chrome()
    result = []
    driver.get("https://www.amazon.in/")
    print('Amazon  ---- > ')
    search_input = driver.find_element(By.ID, "twotabsearchtextbox")
    print('serach element ')
    print(search_input.text)
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)
    product_cards = driver.find_elements(By.CSS_SELECTOR, "img.s-image")
    print(len(product_cards))
    image_urls = [img.get_attribute("src") for img in product_cards]
    for i in image_urls[:5]:
        result.append(i)
    driver.quit()
    print(result)
    return result

def gr_scrape_top_search_results(search_query="shirt", more_images=True):
    results = scrape_from_bewakoof(search_query, more_images)
    print('in displaying ')
    print(results,'res')
    images = []
    for url in results:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        print(img)
        images.append(img)
    print(images)
    print('hellu')
    return images

iface = gr.Interface(
    gr_scrape_top_search_results,
    ["text", "checkbox"],
    ['image','image','image','image','image'],
    title="Top Search Results",
)
iface.launch()
