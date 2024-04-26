import streamlit as st
import replicate
import tempfile
import time
import requests
import cloudinary.uploader
from PIL import Image
from io import BytesIO
from gradio_client import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from test4_streamlit import scrape_from_bewakoof,scrape_from_amazon,scrape_from_ajio
# from gif_gen import create_gif
from decouple import config


class MultiViewDiffusionModel:
    def __init__(self):
        self.client = Client("dylanebert/multi-view-diffusion")
    def make_prediction(self, image_url, text_input):
        result = self.client.predict(image_url, text_input, api_name="/image_to_mv")
        output_image = Image.open(result)
        return output_image
replicate = replicate.Client(api_token=config('REPLICATE_API_TOKEN'))
# Set page title
st.set_page_config(page_title="SOTA VTON")
# Title
st.title("State Of The Art VTON")
# Tabs
tabs = st.tabs(["VTON", "Garment Search","multiview"])
# VTON Tab

def enhance(img):
    print(img)
    print('running','gif wala ')
    output = replicate.run(
        "batouresearch/magic-image-refiner:507ddf6f977a7e30e46c0daefd30de7d563c72322f9e4cf7cbac52ef0f667b13",
        input={
                "hdr": 1,
                "image": img,
                "steps": 30,
                "prompt": "a fashion model posing for a photoshoot",
                "scheduler": "K_EULER_ANCESTRAL",
                "creativity": 0.40,
                "guess_mode": False,
                "resolution": "2048",
                "resemblance": 0.70,
                "guidance_scale": 7,
                "negative_prompt": "ugly face , malformed hands,teeth, tooth, open mouth, longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, mutant"
            }
    )
    print(output)
    return output

def create_gif(image_path, duration=500):
    upload_result = cloudinary.uploader.upload(image_path)["secure_url"]
    image_path = enhance(upload_result)
    # image_data = response.content  
    images = crop_image(image_path[0])
    gif_bytes = BytesIO()
    images[0].save(
        gif_bytes,
        format='GIF',
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )
    gif_bytes.seek(0)
    with open('output.gif', 'wb') as f:
        f.write(gif_bytes.getvalue())
    return gif_bytes.getvalue()
    
def crop_image(image_url):
    response = requests.get(image_url, stream=True)
    image = Image.open(response.raw)
    width, height = image.size
    rows, cols = 2, 2
    sub_width = width // cols
    sub_height = height // rows
    extracted_img = []
    for y in range(rows):
        for x in range(cols):
            left = x * sub_width
            upper = y * sub_height
            right = left + sub_width
            lower = upper + sub_height
            sub_image = image.crop((left, upper, right, lower))
            extracted_img.append(sub_image)
    
    return extracted_img

with tabs[0]:
    # Sidebar
    st.write("use the side bar ")
    with st.sidebar:
        # Image input fields
        garment_image = st.file_uploader("Garment Image", type=["jpg", "png", "jpeg"])
        model_image = st.file_uploader("Model Image", type=["jpg", "png", "jpeg"])

        # Radio button for category selection
        category = st.radio("Select Category", ["upper_body", "lower_body", "dresses"])

        # Text input box for garment description
        garment_description = st.text_input("Garment Description")

        # Run button
        run_button = st.button("Run")

    # Output area
    output_area = st.empty()

    # Display uploaded garment image
    if garment_image:
        col1, col2 = st.columns(2)
        with col1:
            st.image(garment_image, caption="Garment Image", use_column_width=True)

    # Display uploaded model image
    if model_image:
        if 'col1' not in locals() or 'col2' not in locals():
            col1, col2 = st.columns(2)
        with col2:
            st.image(model_image, caption="Model Image", use_column_width=True)

    # Run the Replicate API when the run button is clicked
    if run_button and garment_image and model_image:
        with st.spinner("Running the model..."):
            # Save garment image to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_garment_img:
                tmp_garment_img.write(garment_image.read())
                garment_img_path = tmp_garment_img.name

            # Save model image to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_model_img:
                tmp_model_img.write(model_image.read())
                model_img_path = tmp_model_img.name

            output = replicate.run(
                "cuuupid/idm-vton:5c6712b51ff45af53bba0e88d4a5ec33fad0a85de32462e3d3cbcf51b53d5d37",
                input={
                    "seed": 42,
                    "steps": 30,
                    "category": category,
                    "garm_img": open(garment_img_path, "rb"),
                    "human_img": open(model_img_path, "rb"),
                    "garment_des": garment_description,
                },
            )

            # Download the output image from the URL
            output_image = Image.open(requests.get(output, stream=True).raw)

            # Save output image to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_output_img:
                output_image.save(tmp_output_img.name)
                output_img_path = tmp_output_img.name

            # Display output image
            output_area.image(output_image, use_column_width=True, caption="Output Image")

# Garment Search Tab
with tabs[1]:
    st.title("Garment Search")

    search_query = st.text_input("Enter search query", "shirt")
    website = st.radio("Select Website", ("Bewakoof", "Amazon", "Ajio"))
    more_images = st.checkbox("More Images", False)

    if st.button("Search"):
        with st.spinner("Searching for garments..."):
            if website == "Bewakoof":
                results = scrape_from_bewakoof(search_query, more_images)
            elif website == "Amazon":
                results = scrape_from_amazon(search_query, more_images)
            elif website == "Ajio":
                results = scrape_from_ajio(search_query, more_images)

            images = []
            for data in results:
                response = requests.get(data['src'])
                img = Image.open(BytesIO(response.content))
                images.append((img, data['name'], data['rating'], data['price']))

            if not images:
                st.warning("No data was scraped.")
            else:
                cols = st.columns(5)  # Display 5 images per row
                for i, (img, name, rating, price) in enumerate(images):
                    with cols[i % 5]:
                        st.image(img, caption=f"{name}, {rating}⭐, {price}", use_column_width=True, output_format='JPEG')
                        if st.button(label="Try on", key=i):
                            st.write(f"You clicked on image {name}!")

                            # Add code to set the selected image as the garment image in the VTON tab
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_garment_img:
                                img.save(tmp_garment_img.name)
                                garment_img_path = tmp_garment_img.name

                            with tabs[0].sidebar.form("garment_image_form"):
                                st.image(img, caption="Selected Garment Image", use_column_width=True)
                                submit_button = st.form_submit_button("Use Selected Image")

                            if submit_button:
                                tabs[0].sidebar.upload_state.value = img

with tabs[2]:
    st.title("Multi-View Diffusion")

    if 'output_img_path' in locals():
        text_input = 'fashion model standing for a photo shoot'
        model = MultiViewDiffusionModel()
        # if st.button("Generate Output"):
        with st.spinner("wait for gif to get generate ...."):
            if text_input:
                # image_url = upload_result["secure_url"]
                res_image = model.make_prediction(output_img_path, text_input)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_output_img:
                    res_image.save(tmp_output_img.name)
                    res_img_path = tmp_output_img.name
                output_gif = create_gif(res_img_path)
                st.image(output_gif, caption="Output Image", use_column_width=True)
            else:
                st.warning("Please provide a description.")
    else:
        st.write("No output image available. Please run the model in the VTON tab first.")
    
