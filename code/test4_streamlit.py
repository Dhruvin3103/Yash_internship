import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
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
            image_data = {}
            try:image_data["src"] = card.find_element(By.TAG_NAME, "img").get_attribute("src")
            except Exception as e:image_data["src"] = None;print(e)
            try:image_data["rating"] = card.find_element(By.XPATH, f'//*[@id="product-grid"]/section[{i+1}]/div/a/div/figure/article/span').text
            except Exception as e:image_data["rating"] = None;print(e)
            try:image_data["name"] = card.find_element(By.TAG_NAME,f'h3').text
            except Exception as e:image_data["name"] =None;print(e)
            try:image_data["price"] = card.find_element(By.XPATH,f'//*[@id="product-grid"]/section[{i+1}]/div/section/section/span[1]').text
            except Exception as e:image_data["price"]=None;print(e)
            result.append(image_data)
            if more_images:
                product_link = card.find_element(By.XPATH, f'//*[@id="product-grid"]/section[{i+1}]/div/a')
                product_url = product_link.get_attribute("href")
                res = requests.get(product_url)
                soup = BeautifulSoup(res.text, 'html.parser')
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
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)
    result = []
    
    driver.get("https://www.amazon.in/")
    search_input = driver.find_element(By.ID, "twotabsearchtextbox")
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.RETURN)
    time.sleep(3)
    product_cards = driver.find_elements(By.CSS_SELECTOR, "img.s-image")
    print(len(product_cards))
    image_urls = [img.get_attribute("src") for img in product_cards]
    for i in image_urls[:5]:
        image_data = {}
        try:image_data["src"] = i
        except Exception as e:image_data["src"]=None;print(e)
        try:image_data["rating"] = 'to be added'
        except Exception as e:image_data["rating"]=None;print(e)
        try:image_data["name"] = 'to be added'
        except Exception as e:image_data["name"]=None;print(e)
        try:image_data["price"] = 'to be added '
        except Exception as e:image_data["price"]=None;print(e)
        result.append(image_data)
    # product_cards = driver.find_elements(By.CSS_SELECTOR, 'div.sg-col-inner')
    # print(len(product_cards))
    # for i in range(1,6):
        
    #     # src = driver.find_element(By.XPATH,f'').get_attribute('src')
    #     name = driver.find_element(By.CSS_SELECTOR,f'span.a-size-base-plus a-color-base a-text-normal')
    #     print(name)    
    # # for i,card in enumerate(product_cards):
    # #     try:
    #         src  = card.find_element(By.XPATH,f'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{i+1}]/div/div/span/div/div/div[2]/div/span/a/div/img').get_attribute('src')
    #         price = card.find_element(By.XPATH,f'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{i+1}]/div/div/div/div/span/div/div/div[2]/div[3]/div/div[1]/a/span/span[2]/span[2]').text
    #         rating = 'NA'
    #         name = card.find_element(By.XPATH,f'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{i+1}]/div/div/div/div/span/div/div/div[2]/div[2]/h2/a/span') 
    #         print(src,price,name,rating)
    #     except Exception as e:
    #         print('f up !!')
    #         pass
    # image_urls = [img.get_attribute("src") for img in product_cards]
    # for i in image_urls[:5]:
    #     result.append(i)
    driver.quit()
    return result

def scrape_from_ajio(search_query, more_images):
    driver = webdriver.Chrome()
    result = []
    driver.get("https://www.ajio.com/")
    search_input = driver.find_element(By.XPATH,'//*[@id="appContainer"]/div[1]/div/header/div[3]/div[2]/form/div/div/input')
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)
    product_cards = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div[1]/div/div')
    print(len(product_cards))
    
    for i,card in enumerate(product_cards[:5]):
        img_data = {}
        try: img_data['src'] = card.find_element(By.TAG_NAME,"img").get_attribute("src")
        except Exception as e:img_data['src']=None
        try:img_data['name'] = card.find_element(By.XPATH,f'//*[@id="{str(i)}"]/a/div/div[2]/div[2]').text
        except Exception as e:img_data['name']=None        
        try:img_data['price'] = card.find_element(By.CSS_SELECTOR,f'span.price  ').text
        except Exception as e:img_data['price'] = None
        try:img_data['rating'] = card.find_element(By.XPATH,f'//*[@id="{str(i)}"]/a/div/div[2]/div[3]/div/p').text
        except Exception as e:img_data['rating']='na'
        result.append(img_data)
    return result

def gr_scrape_top_search_results(search_query="shirt", website="Bewakoof", more_images=False):
    if website == "Bewakoof":
        results = scrape_from_bewakoof(search_query, more_images)
    elif website == "Amazon":
        results = scrape_from_amazon(search_query, more_images)
    elif website == "Ajio":
        results = scrape_from_ajio(search_query,more_images)
    images = []
    print(results)
    for data in results:
        response = requests.get(data['src'])
        img = Image.open(BytesIO(response.content))
        images.append((img, data['name'], data['rating'], data['price']))
    return images

st.title("Top Search Results")

search_query = st.text_input("Enter search query", "shirt")
website = st.radio("Select Website", ("Bewakoof", "Amazon","Ajio"))
more_images = st.checkbox("More Images", False)
if st.button("Search"):
    images_data = gr_scrape_top_search_results(search_query, website,more_images)
    if len(images_data):
        st.write('No data was scraped')
    cols = st.columns(5)  # Display 5 images per row
    for i, (img, name, rating, price) in enumerate(images_data):
        with cols[i % 5]:
            st.image(img, caption=f"{name}, {rating}⭐, {price}", use_column_width=True, output_format='JPEG')
            if st.button(label="Try on", key=i):
                st.write(f"You clicked on image {name}!")

# scrape_from_amazon('shirt',False)
