import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests
import time

def scrape_from_bewakoof(search_query, more_images):
    driver = webdriver.Chrome()
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
            name = card.find_element(By.TAG_NAME,f'h3').text
            price = card.find_element(By.XPATH,f'//*[@id="product-grid"]/section[{i+1}]/div/section/section/span[1]').text
            if image_src:
                image_data["src"] = image_src
                image_data["alt"] = image_alt
                image_data["rating"] = rating
                image_data["name"] = name
                image_data["price"] = price
                result.append(image_data)
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
                        result.append(image_data)
        except Exception as e:
            print(e)
    print(result)
    driver.quit()
    return result        

def scrape_from_amazon(search_query, more_images):
    driver = webdriver.Chrome()
    result = []
    driver.get("https://www.amazon.in/")
    search_input = driver.find_element(By.ID, "twotabsearchtextbox")
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)
    product_cards = driver.find_elements(By.CSS_SELECTOR, "img.s-image")
    image_urls = [img.get_attribute("src") for img in product_cards]
    for i in image_urls[:5]:
        result.append(i)
    driver.quit()
    return result

def gr_scrape_top_search_results(search_query="shirt", website="Bewakoof", more_images=False):
    if website == "Bewakoof":
        results = scrape_from_bewakoof(search_query, more_images)
    elif website == "Amazon":
        results = scrape_from_amazon(search_query, more_images)
    images = []
    print(results)
    for data in results:
        response = requests.get(data['src'])
        img = Image.open(BytesIO(response.content))
        images.append((img, data['name'], data['rating'], data['price']))
    return images

st.title("Top Search Results")

search_query = st.text_input("Enter search query", "shirt")
website = st.radio("Select Website", ("Bewakoof", "Amazon"))

if st.button("Search"):
    images_data = gr_scrape_top_search_results(search_query, website)

    cols = st.columns(5)  # Display 5 images per row
    for i, (img, name, rating, price) in enumerate(images_data):
        with cols[i % 5]:
            st.image(img, caption=f"{name}, {rating}, {price}", use_column_width=True, output_format='JPEG')
            if st.button(label="Click Me", key=i):
                st.write(f"You clicked on image {name}!")
